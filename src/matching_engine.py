# Hybrid matching algorithm for resumes and jobs
import json
from typing import Dict, List, Any, Tuple
from collections import Counter
import math
from config import WEIGHTS

class MatchingEngine:
    """
    Hybrid matching engine combining:
    1. Skill overlap (Jaccard similarity)
    2. Semantic similarity (cosine similarity of skills)
    3. Experience matching
    4. Domain matching
    """
    
    EXPERIENCE_LEVELS = {
        "beginner": 0,
        "junior": 1,
        "intermediate": 2,
        "senior": 3,
        "expert": 4
    }
    
    def __init__(self, weights: Dict = None):
        self.weights = weights or WEIGHTS
    
    def calculate_match_score(self, resume_skills: Dict, job_requirements: Dict) -> Dict[str, Any]:
        """
        Calculate overall match score between resume and job
        
        Args:
            resume_skills: Extracted skills from resume
            job_requirements: Extracted requirements from job
            
        Returns:
            Dict with overall score and component scores
        """
        # Calculate component scores
        skill_score = self._calculate_skill_overlap(
            resume_skills.get("technical_skills", []),
            job_requirements.get("required_skills", []),
            job_requirements.get("nice_to_have", [])
        )
        
        semantic_score = self._calculate_semantic_similarity(resume_skills, job_requirements)
        
        experience_score = self._calculate_experience_match(
            resume_skills.get("experience_level", "junior"),
            job_requirements.get("experience_required", "junior")
        )
        
        domain_score = self._calculate_domain_match(
            resume_skills.get("domain_expertise", []),
            job_requirements.get("domain", "")
        )
        
        # Weighted overall score
        overall_score = (
            self.weights["skill_overlap"] * skill_score +
            self.weights["semantic_similarity"] * semantic_score +
            self.weights["experience_match"] * experience_score +
            self.weights["domain_match"] * domain_score
        )
        
        return {
            "overall_score": round(overall_score * 100, 2),
            "component_scores": {
                "skill_overlap": round(skill_score * 100, 2),
                "semantic_similarity": round(semantic_score * 100, 2),
                "experience_match": round(experience_score * 100, 2),
                "domain_match": round(domain_score * 100, 2)
            },
            "weights_used": self.weights
        }
    
    def _calculate_skill_overlap(self, resume_skills: List[str], required_skills: List[str], 
                                 nice_to_have: List[str]) -> float:
        """
        Calculate skill overlap using Jaccard similarity
        
        Score:
        - Exact match with required: 1.0
        - Match with nice_to_have: 0.5
        """
        resume_set = set(s.lower() for s in resume_skills)
        required_set = set(s.lower() for s in required_skills)
        nice_set = set(s.lower() for s in nice_to_have)
        
        if not required_set:
            return 0.5 if resume_set & nice_set else 0.0
        
        # Count matches
        required_matches = resume_set & required_set
        nice_matches = resume_set & nice_set
        
        # Score: 70% on required, 30% on nice_to_have
        required_score = len(required_matches) / len(required_set) if required_set else 0
        nice_score = len(nice_matches) / len(nice_set) if nice_set else 0
        
        return min(0.7 * required_score + 0.3 * nice_score, 1.0)
    
    def _calculate_semantic_similarity(self, resume_skills: Dict, job_requirements: Dict) -> float:
        """
        Rough semantic similarity based on skill count saturation
        """
        resume_count = len(resume_skills.get("technical_skills", []))
        required_count = len(job_requirements.get("required_skills", []))
        nice_count = len(job_requirements.get("nice_to_have", []))
        
        total_needed = required_count + nice_count
        
        # If person has more skills than needed, they're over-qualified (0.9)
        # If person has required count, they're perfect match (1.0)
        # If person has less, they're under-qualified (proportional)
        
        if total_needed == 0:
            return 0.5
        
        if resume_count >= total_needed:
            return 0.9 + (0.1 * min(resume_count / total_needed - 1, 1))
        else:
            return resume_count / total_needed
    
    def _calculate_experience_match(self, resume_level: str, job_level: str) -> float:
        """
        Calculate experience level match
        Perfect match: 1.0
        Over-qualified: 0.95
        Under-qualified: proportional decrease
        """
        resume_val = self.EXPERIENCE_LEVELS.get(resume_level.lower(), 1)
        job_val = self.EXPERIENCE_LEVELS.get(job_level.lower(), 1)
        
        if resume_val >= job_val:
            return 1.0
        else:
            # Under-qualified: 70% of match for each level below
            return max(0.7 ** (job_val - resume_val), 0.3)
    
    def _calculate_domain_match(self, resume_domains: List[str], job_domain: str) -> float:
        """
        Calculate domain expertise match
        """
        if not job_domain or not resume_domains:
            return 0.5
        
        resume_domains_lower = [d.lower() for d in resume_domains]
        
        # Direct match
        if job_domain.lower() in resume_domains_lower:
            return 1.0
        
        # Partial match
        for domain in resume_domains_lower:
            if job_domain.lower() in domain or domain in job_domain.lower():
                return 0.75
        
        return 0.5  # No match but not penalized
    
    def rank_resumes_for_job(self, resumes_with_skills: List[Dict], 
                            job_requirements: Dict, top_k: int = 10) -> List[Dict]:
        """
        Rank all resumes against a job
        
        Args:
            resumes_with_skills: List of dicts with 'name' and 'extracted_skills'
            job_requirements: Job requirement dict
            top_k: Return top K matches
            
        Returns:
            Sorted list of matches
        """
        matches = []
        
        for resume_data in resumes_with_skills:
            score_result = self.calculate_match_score(
                resume_data.get("extracted_skills", {}),
                job_requirements
            )
            
            matches.append({
                "resume_name": resume_data.get("name", "Unknown"),
                "resume_index": resume_data.get("resume_index", -1),
                "overall_score": score_result["overall_score"],
                "component_scores": score_result["component_scores"]
            })
        
        # Sort by overall score
        matches.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return matches[:top_k]
    
    def find_best_jobs_for_resume(self, jobs_with_skills: List[Dict],
                                 resume_skills: Dict, top_k: int = 5) -> List[Dict]:
        """
        Find best fitting jobs for a resume
        """
        matches = []
        
        for job_data in jobs_with_skills:
            score_result = self.calculate_match_score(
                resume_skills,
                job_data.get("extracted_requirements", {})
            )
            
            matches.append({
                "job_role": job_data.get("role", "Unknown"),
                "job_company": job_data.get("company", "Unknown"),
                "job_index": job_data.get("job_index", -1),
                "overall_score": score_result["overall_score"],
                "component_scores": score_result["component_scores"]
            })
        
        # Sort by overall score
        matches.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return matches[:top_k]


if __name__ == "__main__":
    engine = MatchingEngine()
    
    # Test data
    resume_skills = {
        "technical_skills": ["Python", "SQL", "Docker"],
        "soft_skills": ["Communication", "Problem Solving"],
        "experience_level": "intermediate",
        "domain_expertise": ["Software Engineering"]
    }
    
    job_requirements = {
        "required_skills": ["Python", "SQL"],
        "nice_to_have": ["Docker", "Kubernetes"],
        "experience_required": "intermediate",
        "role_category": "Software Engineer",
        "domain": "Software Engineering"
    }
    
    result = engine.calculate_match_score(resume_skills, job_requirements)
    print("Match Score Result:")
    print(json.dumps(result, indent=2))
