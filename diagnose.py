import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.skill_extractor import SkillExtractor
from src.matching_engine import MatchingEngine
from src.job_parser import JobParser

def main(resume_path):
    print(f"\n📄 Reading Resume: {resume_path} ...")
    try:
        with open(resume_path, 'r', encoding='utf-8', errors='ignore') as f:
            resume_text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
        
    print("\n🤖 Diagnosing skills using LLM...")
    extractor = SkillExtractor()
    extracted_skills = extractor.extract_resume_skills(resume_text)
    
    print("\n✨ Extracted Resume Traits:")
    print(json.dumps(extracted_skills, indent=2))
    
    print("\n🔍 Matching with Jobs dataset...")
    jobs_file = PROJECT_ROOT / "data" / "jobs.json"
    
    if not jobs_file.exists():
        print("Error: data/jobs.json not found! Please run main.py first.")
        return
        
    with open(jobs_file, 'r') as f:
        jobs_data = json.load(f)
        
    job_parser = JobParser()
    job_requirements = []
    
    for idx, job in enumerate(jobs_data):
        parsed = job_parser.parse_job(job)
        parsed['job_index'] = idx
        # Use fallback for job requirements to avoid API rate limits since we just need to test
        parsed['extracted_requirements'] = {
            'required_skills': job.get('required_skills', []),
            'nice_to_have': job.get('nice_to_have', []),
            'experience_required': job.get('experience_required', 'junior')
        }
        job_requirements.append(parsed)
        
    engine = MatchingEngine()
    matches = engine.find_best_jobs_for_resume(job_requirements, extracted_skills, top_k=5)
    
    print("\n🏆 Top 5 Job Matches:")
    for m in matches:
        print(f"  → {m['job_role']} at {m['job_company']} (Score: {m['overall_score']:.2f}%)")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnose.py <path_to_resume_file>")
        print("Example: python diagnose.py sample_resume.txt")
        sys.exit(1)
    main(sys.argv[1])
