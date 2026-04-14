# Extract skills from resumes and jobs using LLM
import json
from typing import Dict, List, Any
from pathlib import Path
from src.llm_service import GeminiService
from config import SKILL_EXTRACTION_PROMPT, JOB_ANALYSIS_PROMPT

class SkillExtractor:
    """Extract skills from resumes and jobs using LLM"""
    
    def __init__(self, gemini_service: GeminiService = None):
        self.llm = gemini_service or GeminiService()
        self.skill_cache = {}
    
    def extract_resume_skills(self, resume_text: str, resume_id: str = None) -> Dict[str, Any]:
        """
        Extract skills from resume using Gemini
        
        Args:
            resume_text: Raw resume text
            resume_id: Optional resume identifier for caching
            
        Returns:
            Dict with extracted skills, experience level, etc.
        """
        # Check cache
        if resume_id and resume_id in self.skill_cache:
            return self.skill_cache[resume_id]
        
        # Create prompt
        prompt = SKILL_EXTRACTION_PROMPT.format(resume_text=resume_text)
        
        # Call LLM
        response = self.llm.call_gemini(prompt)
        
        # Parse response
        skills_data = self.llm.extract_json_from_response(response)
        
        # Ensure required keys exist
        skills_data = self._normalize_skills_data(skills_data, "resume")
        
        # Cache result
        if resume_id:
            self.skill_cache[resume_id] = skills_data
        
        return skills_data
    
    def extract_job_skills(self, job_text: str, job_id: str = None) -> Dict[str, Any]:
        """
        Extract requirements from job description
        
        Args:
            job_text: Raw job description text
            job_id: Optional job identifier for caching
            
        Returns:
            Dict with required skills, experience level, etc.
        """
        # Check cache
        if job_id and job_id in self.skill_cache:
            return self.skill_cache[job_id]
        
        # Create prompt
        prompt = JOB_ANALYSIS_PROMPT.format(job_text=job_text)
        
        # Call LLM
        response = self.llm.call_gemini(prompt)
        
        # Parse response
        job_data = self.llm.extract_json_from_response(response)
        
        # Ensure required keys exist
        job_data = self._normalize_skills_data(job_data, "job")
        
        # Cache result
        if job_id:
            self.skill_cache[job_id] = job_data
        
        return job_data
    
    def _normalize_skills_data(self, data: Dict, data_type: str) -> Dict[str, Any]:
        """Normalize extracted data to consistent format"""
        if data_type == "resume":
            return {
                "technical_skills": data.get("technical_skills", []),
                "soft_skills": data.get("soft_skills", []),
                "experience_level": data.get("experience_level", "junior"),
                "domain_expertise": data.get("domain_expertise", [])
            }
        else:  # job
            return {
                "required_skills": data.get("required_skills", []),
                "nice_to_have": data.get("nice_to_have", []),
                "experience_required": data.get("experience_required", "junior"),
                "role_category": data.get("role_category", ""),
                "domain": data.get("domain", "")
            }
    
    def batch_extract_resume_skills(self, resumes: List[Dict]) -> List[Dict]:
        """Extract skills from multiple resumes"""
        results = []
        for idx, resume in enumerate(resumes):
            print(f"  Processing resume {idx+1}/{len(resumes)}...", end="\r")
            skills = self.extract_resume_skills(
                resume.get("resume_text", ""),
                resume_id=f"resume_{idx}"
            )
            results.append({
                "resume_index": idx,
                "name": resume.get("name", ""),
                "extracted_skills": skills
            })
        print(f"  ✅ Processed {len(resumes)} resumes           ")
        return results
    
    def batch_extract_job_skills(self, jobs: List[Dict]) -> List[Dict]:
        """Extract requirements from multiple jobs"""
        results = []
        for idx, job in enumerate(jobs):
            print(f"  Processing job {idx+1}/{len(jobs)}...", end="\r")
            skills = self.extract_job_skills(
                job.get("job_description", ""),
                job_id=f"job_{idx}"
            )
            results.append({
                "job_index": idx,
                "role": job.get("role", ""),
                "company": job.get("company", ""),
                "extracted_requirements": skills
            })
        print(f"  ✅ Processed {len(jobs)} jobs           ")
        return results


if __name__ == "__main__":
    extractor = SkillExtractor()
    
    # Test resume extraction
    sample_resume = """
    Python, Java, SQL, REST APIs, Microservices, Docker
    5 years experience as Software Engineer
    """
    
    skills = extractor.extract_resume_skills(sample_resume)
    print("Extracted Resume Skills:")
    print(json.dumps(skills, indent=2))
