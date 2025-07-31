import random
from typing import List, Dict, Tuple
from collections import deque

class AdaptiveRatingGenerator:
    def __init__(self):
        self.ratings_history: List[int] = []
        self.recent_20 = deque(maxlen=20)
        self.recent_100 = deque(maxlen=100)
        
        # Base probabilities - will be dynamically adjusted
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
        
    def _calculate_average(self, ratings: List[int]) -> float:
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)
    
    def _get_current_averages(self) -> Dict[str, float]:
        return {
            'recent_20': self._calculate_average(list(self.recent_20)),
            'recent_100': self._calculate_average(list(self.recent_100)),
            'overall': self._calculate_average(self.ratings_history)
        }
    
    def _adjust_probabilities(self) -> None:
        if len(self.ratings_history) < 5:
            return
            
        averages = self._get_current_averages()
        
        # Reset to base probabilities
        self.current_probabilities = self.base_probabilities.copy()
        
        # Adjust based on recent 20 performance
        if len(self.recent_20) >= 10:
            recent_20_avg = averages['recent_20']
            if recent_20_avg < self.target_20_avg:
                # Need to boost average - increase 5s, decrease 1s slightly
                boost_factor = (self.target_20_avg - recent_20_avg) * 0.8
                self.current_probabilities[5] = min(0.95, self.base_probabilities[5] + boost_factor)
                self.current_probabilities[1] = max(0.03, self.base_probabilities[1] - boost_factor * 0.5)
                
                # Redistribute remaining probability
                remaining = 1.0 - self.current_probabilities[5] - self.current_probabilities[1]
                self.current_probabilities[4] = remaining * 0.5
                self.current_probabilities[3] = remaining * 0.3
                self.current_probabilities[2] = remaining * 0.2
        
        # Adjust based on overall performance after 50+ ratings
        if len(self.ratings_history) >= 50:
            overall_avg = averages['overall']
            if overall_avg < self.target_overall_avg:
                # Fine-tune for long-term target
                fine_tune = (self.target_overall_avg - overall_avg) * 0.6
                self.current_probabilities[5] = min(0.96, self.current_probabilities[5] + fine_tune)
                self.current_probabilities[1] = max(0.02, self.current_probabilities[1] - fine_tune * 0.3)
                
                # Redistribute remaining for middle ratings
                remaining = 1.0 - self.current_probabilities[5] - self.current_probabilities[1]
                self.current_probabilities[4] = remaining * 0.5
                self.current_probabilities[3] = remaining * 0.3
                self.current_probabilities[2] = remaining * 0.2
        
        # Ensure constraint: 1s > (2s + 3s + 4s) 
        middle_ratings_total = self.current_probabilities[2] + self.current_probabilities[3] + self.current_probabilities[4]
        if self.current_probabilities[1] <= middle_ratings_total:
            # Adjust to maintain constraint
            self.current_probabilities[1] = middle_ratings_total + 0.05
            self.current_probabilities[5] = 1.0 - self.current_probabilities[1] - middle_ratings_total
    
    def _validate_constraints(self) -> bool:
        if not self.ratings_history:
            return True
            
        # Count occurrences
        counts = {i: self.ratings_history.count(i) for i in range(1, 6)}
        
        # Check if 1s > (2s + 3s + 4s)
        ones_count = counts[1]
        middle_count = counts[2] + counts[3] + counts[4]
        
        return ones_count >= middle_count
    
    def generate_rating(self) -> int:
        self._adjust_probabilities()
        
        # Create weighted choices
        ratings = list(self.current_probabilities.keys())
        weights = list(self.current_probabilities.values())
        
        # Generate random rating
        rating = random.choices(ratings, weights=weights, k=1)[0]
        
        # Store rating
        self.ratings_history.append(rating)
        self.recent_20.append(rating)
        self.recent_100.append(rating)
        
        return rating
    
    def get_statistics(self) -> Dict:
        if not self.ratings_history:
            return {"error": "No ratings generated yet"}
            
        averages = self._get_current_averages()
        counts = {i: self.ratings_history.count(i) for i in range(1, 6)}
        total_ratings = len(self.ratings_history)
        percentages = {i: (count / total_ratings * 100) for i, count in counts.items()}
        
        return {
            "total_ratings": total_ratings,
            "averages": averages,
            "counts": counts,
            "percentages": percentages,
            "constraints_satisfied": self._validate_constraints(),
            "current_probabilities": self.current_probabilities.copy(),
            "targets_met": {
                "20_sample": averages['recent_20'] >= self.target_20_avg if len(self.recent_20) >= 20 else "N/A",
                "100_sample": averages['recent_100'] >= self.target_100_avg if len(self.recent_100) >= 100 else "N/A",
                "overall": averages['overall'] >= self.target_overall_avg if total_ratings >= 100 else "N/A"
            }
        }
    
    def generate_batch(self, count: int) -> List[int]:
        return [self.generate_rating() for _ in range(count)]
    
    def reset(self) -> None:
        self.ratings_history.clear()
        self.recent_20.clear()
        self.recent_100.clear()
        self.current_probabilities = self.base_probabilities.copy()

# Example usage and testing
if __name__ == "__main__":
    generator = AdaptiveRatingGenerator()
    
    print("Generating 200 ratings with real-time monitoring...")
    print("=" * 60)
    
    for i in range(1, 201):
        rating = generator.generate_rating()
        
        if i % 20 == 0:
            stats = generator.get_statistics()
            print(f"\nAfter {i} ratings:")
            print(f"Recent 20 avg: {stats['averages']['recent_20']:.3f}")
            print(f"Overall avg: {stats['averages']['overall']:.3f}")
            print(f"Distribution: {stats['percentages']}")
            print(f"Constraints satisfied: {stats['constraints_satisfied']}")
            if i >= 100:
                print(f"Targets met: {stats['targets_met']}")