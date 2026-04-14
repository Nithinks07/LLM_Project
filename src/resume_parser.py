# Resume parsing module
import json
from pathlib import Path
from typing import Dict, Any

class ResumeParser:
    """Parse resume data from various formats"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / "data"
        self.resumes_cache = None
    
    def load_resumes_from_json(self) -> list:
        """Load resumes from JSON file"""
        resumes_path = self.data_dir / "resumes.json"
        
        if resumes_path.exists():
            with open(resumes_path, 'r') as f:
                self.resumes_cache = json.load(f)
                return self.resumes_cache
        else:
            raise FileNotFoundError(f"Resumes file not found at {resumes_path}")
    
    def parse_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single resume and extract basic information
        
        Args:
            resume_data: Resume data dictionary with 'resume_text' key
            
        Returns:
            Parsed resume information
        """
        return {
            "name": resume_data.get("name", "Unknown"),
            "email": resume_data.get("email", ""),
            "phone": resume_data.get("phone", ""),
            "target_role": resume_data.get("target_role", ""),
            "years_experience": resume_data.get("years_experience", 0),
            "resume_text": resume_data.get("resume_text", ""),
            "raw_data": resume_data
        }
    
    def extract_text_from_resume(self, resume_data: Dict[str, Any]) -> str:
        """Extract plain text from resume"""
        return resume_data.get("resume_text", "")
    
    def get_all_resumes(self) -> list:
        """Get all parsed resumes"""
        if self.resumes_cache is None:
            self.load_resumes_from_json()
        
        return [self.parse_resume(r) for r in self.resumes_cache]
    
    def get_resume_by_index(self, index: int) -> Dict[str, Any]:
        """Get a specific resume by index"""
        if self.resumes_cache is None:
            self.load_resumes_from_json()
        
        if 0 <= index < len(self.resumes_cache):
            return self.parse_resume(self.resumes_cache[index])
        return None
    
    def filter_resumes_by_role(self, role: str) -> list:
        """Filter resumes by target role"""
        if self.resumes_cache is None:
            self.load_resumes_from_json()
        
        return [
            self.parse_resume(r) for r in self.resumes_cache 
            if r.get("target_role") == role
        ]


if __name__ == "__main__":
    parser = ResumeParser()
    resumes = parser.get_all_resumes()
    print(f"✅ Loaded {len(resumes)} resumes")
    print(f"\nFirst resume:\n{resumes[0]}")
