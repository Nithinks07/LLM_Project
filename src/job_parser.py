# Job description parsing module
import json
from pathlib import Path
from typing import Dict, Any

class JobParser:
    """Parse and process job descriptions"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / "data"
        self.jobs_cache = None
    
    def load_jobs_from_json(self) -> list:
        """Load jobs from JSON file"""
        jobs_path = self.data_dir / "jobs.json"
        
        if jobs_path.exists():
            with open(jobs_path, 'r') as f:
                self.jobs_cache = json.load(f)
                return self.jobs_cache
        else:
            raise FileNotFoundError(f"Jobs file not found at {jobs_path}")
    
    def parse_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a single job description"""
        return {
            "role": job_data.get("role", ""),
            "company": job_data.get("company", ""),
            "job_description": job_data.get("job_description", ""),
            "required_skills": job_data.get("required_skills", []),
            "nice_to_have": job_data.get("nice_to_have", []),
            "experience_required": job_data.get("experience_required", ""),
            "salary_range": job_data.get("salary_range", ""),
            "raw_data": job_data
        }
    
    def extract_text_from_job(self, job_data: Dict[str, Any]) -> str:
        """Extract plain text from job description"""
        return job_data.get("job_description", "")
    
    def get_all_jobs(self) -> list:
        """Get all parsed jobs"""
        if self.jobs_cache is None:
            self.load_jobs_from_json()
        
        return [self.parse_job(j) for j in self.jobs_cache]
    
    def get_job_by_index(self, index: int) -> Dict[str, Any]:
        """Get a specific job by index"""
        if self.jobs_cache is None:
            self.load_jobs_from_json()
        
        if 0 <= index < len(self.jobs_cache):
            return self.parse_job(self.jobs_cache[index])
        return None
    
    def filter_jobs_by_role(self, role: str) -> list:
        """Filter jobs by role"""
        if self.jobs_cache is None:
            self.load_jobs_from_json()
        
        return [
            self.parse_job(j) for j in self.jobs_cache 
            if j.get("role") == role
        ]
    
    def get_unique_roles(self) -> list:
        """Get all unique job roles"""
        if self.jobs_cache is None:
            self.load_jobs_from_json()
        
        return list(set(j.get("role", "") for j in self.jobs_cache))


if __name__ == "__main__":
    parser = JobParser()
    jobs = parser.get_all_jobs()
    print(f"✅ Loaded {len(jobs)} jobs")
    print(f"Roles: {parser.get_unique_roles()}")
    print(f"\nFirst job:\n{jobs[0]}")
