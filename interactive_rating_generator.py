import random
import json
import os
from typing import Dict, List, Optional
from collections import deque

class InteractiveRatingGenerator:
    def __init__(self, json_file: str = "ratings_data.json"):
        self.json_file = json_file
        
        # Incremental math variables
        self.total_count = 0
        self.total_sum = 0
        
        # Sliding windows with sum tracking
        self.recent_20 = deque(maxlen=20)
        self.recent_20_sum = 0
        self.recent_100 = deque(maxlen=100)
        self.recent_100_sum = 0
        
        # Full history for JSON persistence
        self.ratings_history: List[int] = []
        
        # Distribution counters for constraints
        self.distribution_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        # Base probabilities
        self.base_probabilities = {
            5: 0.90,  # 90% for rating 5
            1: 0.08,  # 8% for rating 1
            4: 0.01,  # 1% for rating 4
            3: 0.007, # 0.7% for rating 3
            2: 0.003  # 0.3% for rating 2
        }
        
        self.current_probabilities = self.base_probabilities.copy()
        
        # Target averages
        self.target_20_avg = 4.0
        self.target_100_avg = 4.8
        self.target_overall_avg = 4.85
        
        # Load existing data if available
        self.load_from_json()
    
    def load_from_json(self) -> None:
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
                    if 'ratings' in data and data['ratings']:
                        self.ratings_history = data['ratings']
                        self._rebuild_from_history()
                        print(f"Loaded {len(self.ratings_history)} existing ratings from {self.json_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Could not load existing data: {e}")
                print("Starting fresh...")
    
    def _rebuild_from_history(self) -> None:
        # Rebuild all incremental data from loaded history
        self.total_count = len(self.ratings_history)
        self.total_sum = sum(self.ratings_history)
        
        # Rebuild distribution counts
        for rating in self.ratings_history:
            self.distribution_counts[rating] += 1
        
        # Rebuild sliding windows
        if len(self.ratings_history) >= 20:
            recent_20_data = self.ratings_history[-20:]
            self.recent_20.extend(recent_20_data)
            self.recent_20_sum = sum(recent_20_data)
        else:
            self.recent_20.extend(self.ratings_history)
            self.recent_20_sum = sum(self.ratings_history)
        
        if len(self.ratings_history) >= 100:
            recent_100_data = self.ratings_history[-100:]
            self.recent_100.extend(recent_100_data)
            self.recent_100_sum = sum(recent_100_data)
        else:
            self.recent_100.extend(self.ratings_history)
            self.recent_100_sum = sum(self.ratings_history)
    
    def save_to_json(self) -> None:
        data = {
            'ratings': self.ratings_history,
            'total_count': self.total_count,
            'statistics': self.get_current_stats()
        }
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_overall_average(self) -> float:
        return self.total_sum / self.total_count if self.total_count > 0 else 0.0
    
    def get_recent_20_average(self) -> float:
        return self.recent_20_sum / len(self.recent_20) if self.recent_20 else 0.0
    
    def get_recent_100_average(self) -> float:
        return self.recent_100_sum / len(self.recent_100) if self.recent_100 else 0.0
    
    def _validate_constraints(self) -> bool:
        ones_count = self.distribution_counts[1]
        middle_count = self.distribution_counts[2] + self.distribution_counts[3] + self.distribution_counts[4]
        return ones_count >= middle_count
    
    def _adjust_probabilities(self) -> None:
        if self.total_count < 5:
            return
        
        # Reset to base probabilities
        self.current_probabilities = self.base_probabilities.copy()
        
        # Adjust based on recent 20 performance
        if len(self.recent_20) >= 10:
            recent_20_avg = self.get_recent_20_average()
            if recent_20_avg < self.target_20_avg:
                boost_factor = (self.target_20_avg - recent_20_avg) * 0.8
                self.current_probabilities[5] = min(0.95, self.base_probabilities[5] + boost_factor)
                self.current_probabilities[1] = max(0.03, self.base_probabilities[1] - boost_factor * 0.5)
                
                remaining = 1.0 - self.current_probabilities[5] - self.current_probabilities[1]
                self.current_probabilities[4] = remaining * 0.5
                self.current_probabilities[3] = remaining * 0.3
                self.current_probabilities[2] = remaining * 0.2
        
        # Adjust based on overall performance after 50+ ratings
        if self.total_count >= 50:
            overall_avg = self.get_overall_average()
            if overall_avg < self.target_overall_avg:
                fine_tune = (self.target_overall_avg - overall_avg) * 0.6
                self.current_probabilities[5] = min(0.96, self.current_probabilities[5] + fine_tune)
                self.current_probabilities[1] = max(0.02, self.current_probabilities[1] - fine_tune * 0.3)
                
                remaining = 1.0 - self.current_probabilities[5] - self.current_probabilities[1]
                self.current_probabilities[4] = remaining * 0.5
                self.current_probabilities[3] = remaining * 0.3
                self.current_probabilities[2] = remaining * 0.2
        
        # Ensure constraint: 1s > (2s + 3s + 4s)
        middle_ratings_total = self.current_probabilities[2] + self.current_probabilities[3] + self.current_probabilities[4]
        if self.current_probabilities[1] <= middle_ratings_total:
            self.current_probabilities[1] = middle_ratings_total + 0.05
            self.current_probabilities[5] = 1.0 - self.current_probabilities[1] - middle_ratings_total
    
    def generate_rating(self) -> int:
        self._adjust_probabilities()
        
        # Generate weighted random rating
        ratings = list(self.current_probabilities.keys())
        weights = list(self.current_probabilities.values())
        rating = random.choices(ratings, weights=weights, k=1)[0]
        
        # Update incremental counters
        self.total_count += 1
        self.total_sum += rating
        self.distribution_counts[rating] += 1
        
        # Update sliding windows with incremental math
        if len(self.recent_20) == 20:  # Window is full, remove oldest
            removed = self.recent_20[0]
            self.recent_20_sum -= removed
        self.recent_20.append(rating)
        self.recent_20_sum += rating
        
        if len(self.recent_100) == 100:  # Window is full, remove oldest
            removed = self.recent_100[0]
            self.recent_100_sum -= removed
        self.recent_100.append(rating)
        self.recent_100_sum += rating
        
        # Store in history for JSON persistence
        self.ratings_history.append(rating)
        
        # Save to JSON after each generation
        self.save_to_json()
        
        return rating
    
    def get_current_stats(self) -> Dict:
        if self.total_count == 0:
            return {"error": "No ratings generated yet"}
        
        percentages = {i: (count / self.total_count * 100) for i, count in self.distribution_counts.items()}
        
        return {
            "total_count": self.total_count,
            "overall_avg": self.get_overall_average(),
            "recent_20_avg": self.get_recent_20_average(),
            "recent_100_avg": self.get_recent_100_average(),
            "distribution_counts": self.distribution_counts.copy(),
            "distribution_percentages": percentages,
            "constraints_satisfied": self._validate_constraints(),
            "targets_met": {
                "20_sample": self.get_recent_20_average() >= self.target_20_avg if len(self.recent_20) >= 20 else "N/A",
                "100_sample": self.get_recent_100_average() >= self.target_100_avg if len(self.recent_100) >= 100 else "N/A",
                "overall": self.get_overall_average() >= self.target_overall_avg if self.total_count >= 100 else "N/A"
            }
        }
    
    def print_progress_report(self) -> None:
        stats = self.get_current_stats()
        print("\n" + "="*60)
        print(f"PROGRESS REPORT - After {stats['total_count']} ratings")
        print("="*60)
        print(f"Recent 20 Avg: {stats['recent_20_avg']:.3f}")
        if len(self.recent_100) >= 20:
            print(f"Recent 100 Avg: {stats['recent_100_avg']:.3f}")
        print(f"Overall Avg: {stats['overall_avg']:.3f}")
        print(f"Distribution: {stats['distribution_percentages']}")
        print(f"Constraints OK: {stats['constraints_satisfied']}")
        print(f"Targets Met: {stats['targets_met']}")
        print("="*60 + "\n")

    def load_historical_ratings(self, ratings: List[int]) -> None:
        """
        Load a list of historical ratings, update all internal state, and save to JSON.
        """
        self.ratings_history = ratings.copy()
        self._rebuild_from_history()
        self.save_to_json()

def main():
    generator = InteractiveRatingGenerator()
    
    print("Interactive Rating Generator")
    print("="*50)
    print("Press Enter to generate a rating")
    print("Type 'stats' to see detailed statistics")
    print("Type 'q' to quit")
    print("="*50)
    
    if generator.total_count > 0:
        print(f"Resuming with {generator.total_count} existing ratings...")
        stats = generator.get_current_stats()
        print(f"Current overall average: {stats['overall_avg']:.3f}")
    print()
    
    while True:
        user_input = input("Press Enter to generate (or 'stats'/'q'): ").strip().lower()
        
        if user_input == 'q':
            print("Goodbye! Data saved to", generator.json_file)
            break
        elif user_input == 'stats':
            generator.print_progress_report()
            continue
        elif user_input == '':
            # Generate new rating
            rating = generator.generate_rating()
            stats = generator.get_current_stats()
            
            print(f"Generated: {rating} | Count: {stats['total_count']} | Overall Avg: {stats['overall_avg']:.3f}")
            
            # Show progress report every 20 ratings
            if stats['total_count'] % 20 == 0:
                generator.print_progress_report()
        else:
            print("Invalid input. Press Enter to generate, 'stats' for statistics, or 'q' to quit.")

if __name__ == "__main__":
    main()