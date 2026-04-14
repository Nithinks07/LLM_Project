# Evaluation and testing module
import json
from typing import Dict, List, Any
from pathlib import Path
import statistics

class EvaluationEngine:
    """Evaluate matching algorithm performance"""
    
    def __init__(self):
        self.all_matches = []
        self.metrics = {}
    
    def add_match_result(self, resume_idx: int, job_idx: int, score: float, 
                        components: Dict[str, float], resume_role: str = None, 
                        job_role: str = None):
        """Record a match result"""
        self.all_matches.append({
            "resume_idx": resume_idx,
            "job_idx": job_idx,
            "overall_score": score,
            "component_scores": components,
            "resume_role": resume_role,
            "job_role": job_role,
            "is_same_role": resume_role == job_role if resume_role and job_role else None
        })
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate evaluation metrics"""
        if not self.all_matches:
            return {"error": "No matches to evaluate"}
        
        scores = [m["overall_score"] for m in self.all_matches]
        same_role_matches = [m for m in self.all_matches if m.get("is_same_role")]
        different_role_matches = [m for m in self.all_matches if not m.get("is_same_role")]
        
        same_role_scores = [m["overall_score"] for m in same_role_matches]
        different_role_scores = [m["overall_score"] for m in different_role_matches]
        
        self.metrics = {
            "total_comparisons": len(self.all_matches),
            "statistics": {
                "mean_score": round(statistics.mean(scores), 2),
                "median_score": round(statistics.median(scores), 2),
                "std_dev": round(statistics.stdev(scores), 2) if len(scores) > 1 else 0,
                "min_score": round(min(scores), 2),
                "max_score": round(max(scores), 2)
            },
            "role_analysis": {
                "same_role_matches": len(same_role_matches),
                "same_role_avg_score": round(statistics.mean(same_role_scores), 2) if same_role_scores else 0,
                "different_role_matches": len(different_role_matches),
                "different_role_avg_score": round(statistics.mean(different_role_scores), 2) if different_role_scores else 0
            }
        }
        
        return self.metrics
    
    def get_component_analysis(self) -> Dict[str, Any]:
        """Analyze individual component contributions"""
        if not self.all_matches:
            return {}
        
        component_names = ["skill_overlap", "semantic_similarity", "experience_match", "domain_match"]
        analysis = {}
        
        for component in component_names:
            scores = [m["component_scores"].get(component, 0) for m in self.all_matches]
            analysis[component] = {
                "mean": round(statistics.mean(scores), 2),
                "median": round(statistics.median(scores), 2),
                "min": round(min(scores), 2),
                "max": round(max(scores), 2)
            }
        
        return analysis
    
    def get_score_distribution(self, bins: int = 10) -> Dict[str, int]:
        """Get distribution of scores across bins"""
        if not self.all_matches:
            return {}
        
        scores = [m["overall_score"] for m in self.all_matches]
        min_score = min(scores)
        max_score = max(scores)
        
        # Create bins
        bin_edges = [min_score + (max_score - min_score) * i / bins for i in range(bins + 1)]
        distribution = {f"{round(bin_edges[i], 1)}-{round(bin_edges[i+1], 1)}": 0 for i in range(bins)}
        
        # Fill bins
        for score in scores:
            for i, (lower, upper) in enumerate(zip(bin_edges[:-1], bin_edges[1:])):
                if lower <= score <= upper:
                    bin_label = f"{round(lower, 1)}-{round(upper, 1)}"
                    distribution[bin_label] += 1
                    break
        
        return distribution
    
    def generate_report(self, output_path: Path = None) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        metrics = self.calculate_metrics()
        components = self.get_component_analysis()
        distribution = self.get_score_distribution()
        
        report = {
            "summary": {
                "total_matches_evaluated": metrics.get("total_comparisons", 0),
                "average_match_score": metrics.get("statistics", {}).get("mean_score", 0)
            },
            "detailed_metrics": metrics,
            "component_analysis": components,
            "score_distribution": distribution,
            "observations": self._generate_observations(metrics, components)
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✅ Report saved to {output_path}")
        
        return report
    
    def _generate_observations(self, metrics: Dict, components: Dict) -> List[str]:
        """Generate insights from metrics"""
        observations = []
        
        if metrics.get("statistics"):
            mean_score = metrics["statistics"].get("mean_score", 0)
            observations.append(f"Average match score is {mean_score}%, indicating {'strong' if mean_score > 70 else 'moderate' if mean_score > 50 else 'weak'} overall matching.")
        
        if metrics.get("role_analysis"):
            same_role_avg = metrics["role_analysis"].get("same_role_avg_score", 0)
            diff_role_avg = metrics["role_analysis"].get("different_role_avg_score", 0)
            
            if same_role_avg > diff_role_avg:
                observations.append(f"Same-role matches score {same_role_avg}% vs {diff_role_avg}% for different roles, showing good discriminative power.")
        
        if components.get("skill_overlap"):
            skill_score = components["skill_overlap"].get("mean", 0)
            observations.append(f"Skill overlap component averages {skill_score}%, suggesting {' good skill matching' if skill_score > 60 else 'potential skill gaps'}.")
        
        return observations


if __name__ == "__main__":
    evaluator = EvaluationEngine()
    
    # Test data
    evaluator.add_match_result(0, 0, 85.5, 
        {"skill_overlap": 90, "semantic_similarity": 80, "experience_match": 85, "domain_match": 80},
        "Software Engineer", "Software Engineer")
    
    evaluator.add_match_result(0, 1, 45.2,
        {"skill_overlap": 40, "semantic_similarity": 50, "experience_match": 45, "domain_match": 40},
        "Software Engineer", "Data Scientist")
    
    report = evaluator.generate_report()
    print(json.dumps(report, indent=2))
