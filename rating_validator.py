from adaptive_rating_system import AdaptiveRatingGenerator
from typing import List, Dict
import statistics

class RatingValidator:
    def __init__(self):
        self.generator = AdaptiveRatingGenerator()
    
    def test_target_compliance(self, num_ratings: int = 200) -> Dict:
        print(f"Testing with {num_ratings} ratings...")
        self.generator.reset()
        
        results = {
            'milestones': {},
            'final_stats': {},
            'compliance_summary': {}
        }
        
        # Track key milestones
        milestones = [20, 50, 100, 200] if num_ratings >= 200 else [20, 50, 100, num_ratings]
        
        for i in range(1, num_ratings + 1):
            rating = self.generator.generate_rating()
            
            if i in milestones:
                stats = self.generator.get_statistics()
                results['milestones'][i] = {
                    'overall_avg': stats['averages']['overall'],
                    'recent_20_avg': stats['averages']['recent_20'],
                    'distribution': stats['percentages'],
                    'constraints_ok': stats['constraints_satisfied']
                }
        
        # Final comprehensive analysis
        final_stats = self.generator.get_statistics()
        results['final_stats'] = final_stats
        
        # Compliance check
        compliance = {
            'constraint_satisfied': final_stats['constraints_satisfied'],
            'avg_20_target_met': final_stats['averages']['recent_20'] >= 4.0 if len(self.generator.recent_20) >= 20 else None,
            'avg_100_target_met': final_stats['averages']['recent_100'] >= 4.8 if len(self.generator.recent_100) >= 100 else None,
            'overall_target_met': final_stats['averages']['overall'] >= 4.8 if num_ratings >= 100 else None
        }
        results['compliance_summary'] = compliance
        
        return results
    
    def test_multiple_runs(self, num_runs: int = 10, ratings_per_run: int = 200) -> Dict:
        print(f"Running {num_runs} independent tests with {ratings_per_run} ratings each...")
        
        all_results = []
        success_count = 0
        
        for run in range(num_runs):
            print(f"Run {run + 1}/{num_runs}")
            result = self.test_target_compliance(ratings_per_run)
            all_results.append(result)
            
            # Count successful runs
            compliance = result['compliance_summary']
            if (compliance['constraint_satisfied'] and 
                compliance.get('overall_target_met', True) and
                compliance.get('avg_20_target_met', True)):
                success_count += 1
        
        # Aggregate statistics
        overall_averages = [r['final_stats']['averages']['overall'] for r in all_results]
        constraint_successes = [r['compliance_summary']['constraint_satisfied'] for r in all_results]
        
        summary = {
            'success_rate': success_count / num_runs,
            'average_overall_avg': statistics.mean(overall_averages),
            'std_overall_avg': statistics.stdev(overall_averages) if len(overall_averages) > 1 else 0,
            'constraint_success_rate': sum(constraint_successes) / num_runs,
            'min_avg': min(overall_averages),
            'max_avg': max(overall_averages),
            'all_results': all_results
        }
        
        return summary
    
    def analyze_distribution_over_time(self, num_ratings: int = 200) -> Dict:
        print(f"Analyzing distribution evolution over {num_ratings} ratings...")
        self.generator.reset()
        
        tracking_points = []
        checkpoint_interval = 10
        
        for i in range(1, num_ratings + 1):
            rating = self.generator.generate_rating()
            
            if i % checkpoint_interval == 0:
                stats = self.generator.get_statistics()
                tracking_points.append({
                    'rating_count': i,
                    'overall_avg': stats['averages']['overall'],
                    'recent_20_avg': stats['averages']['recent_20'] if len(self.generator.recent_20) >= 10 else None,
                    'distribution': stats['percentages'].copy(),
                    'constraints_ok': stats['constraints_satisfied']
                })
        
        return {
            'tracking_points': tracking_points,
            'final_stats': self.generator.get_statistics()
        }
    
    def stress_test_constraints(self) -> Dict:
        print("Stress testing constraint maintenance...")
        
        results = {}
        test_sizes = [50, 100, 200, 500, 1000]
        
        for size in test_sizes:
            print(f"Testing with {size} ratings...")
            self.generator.reset()
            
            ratings = self.generator.generate_batch(size)
            stats = self.generator.get_statistics()
            
            # Detailed constraint analysis
            counts = stats['counts']
            ones_count = counts[1]
            middle_count = counts[2] + counts[3] + counts[4]
            fives_count = counts[5]
            
            results[size] = {
                'constraint_met': ones_count > middle_count,
                'ones_count': ones_count,
                'middle_count': middle_count,
                'fives_count': fives_count,
                'overall_avg': stats['averages']['overall'],
                'distribution': stats['percentages']
            }
        
        return results
    
    def print_detailed_report(self, test_results: Dict) -> None:
        print("\n" + "="*80)
        print("DETAILED RATING SYSTEM VALIDATION REPORT")
        print("="*80)
        
        if 'milestones' in test_results:
            print("\nMILESTONE ANALYSIS:")
            print("-" * 40)
            for milestone, data in test_results['milestones'].items():
                print(f"\nAfter {milestone} ratings:")
                print(f"  Overall Average: {data['overall_avg']:.3f}")
                print(f"  Recent 20 Average: {data['recent_20_avg']:.3f}")
                print(f"  Constraints Satisfied: {data['constraints_ok']}")
                print(f"  Distribution: {data['distribution']}")
        
        if 'final_stats' in test_results:
            print(f"\nFINAL STATISTICS:")
            print("-" * 40)
            stats = test_results['final_stats']
            print(f"Total Ratings: {stats['total_ratings']}")
            print(f"Final Averages: {stats['averages']}")
            print(f"Distribution: {stats['percentages']}")
            print(f"Constraints Satisfied: {stats['constraints_satisfied']}")
            print(f"Targets Met: {stats['targets_met']}")
        
        if 'compliance_summary' in test_results:
            print(f"\nCOMPLIANCE SUMMARY:")
            print("-" * 40)
            compliance = test_results['compliance_summary']
            for key, value in compliance.items():
                print(f"  {key}: {value}")

# Example usage
if __name__ == "__main__":
    validator = RatingValidator()
    
    # Single test
    print("Running single test...")
    single_result = validator.test_target_compliance(200)
    validator.print_detailed_report(single_result)
    
    # Multiple runs test
    print("\n" + "="*80)
    print("Running multiple tests for reliability...")
    multi_result = validator.test_multiple_runs(5, 200)
    print(f"Success Rate: {multi_result['success_rate']:.2%}")
    print(f"Average Overall Average: {multi_result['average_overall_avg']:.3f}")
    print(f"Standard Deviation: {multi_result['std_overall_avg']:.3f}")
    print(f"Constraint Success Rate: {multi_result['constraint_success_rate']:.2%}")
    
    # Constraint stress test
    print("\n" + "="*80)
    print("Stress testing constraints...")
    stress_results = validator.stress_test_constraints()
    for size, result in stress_results.items():
        print(f"\n{size} ratings: Constraint met = {result['constraint_met']}")
        print(f"  1s: {result['ones_count']}, 2+3+4s: {result['middle_count']}, 5s: {result['fives_count']}")
        print(f"  Average: {result['overall_avg']:.3f}")