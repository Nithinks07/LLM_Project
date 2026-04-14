# Configuration for LLM Career Placement Engine
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure directories exist
[d.mkdir(exist_ok=True) for d in [DATA_DIR, OUTPUT_DIR]]

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
GEMINI_MODEL = "gemini-1.5-flash"

# Database paths
SQLITE_DB = DATA_DIR / "placement_engine.db"
RESUMES_JSON = DATA_DIR / "resumes.json"
JOBS_JSON = DATA_DIR / "jobs.json"
SKILLS_DB = DATA_DIR / "skills_database.json"

# Dataset sizes
NUM_RESUMES = 60
NUM_JOBS = 22
CORE_ROLES = ["Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "DevOps Engineer"]

# Matching algorithm weights
WEIGHTS = {
    "skill_overlap": 0.40,
    "semantic_similarity": 0.35,
    "experience_match": 0.15,
    "domain_match": 0.10
}

# LLM Prompt templates
SKILL_EXTRACTION_PROMPT = """
Extract technical and professional skills from this resume. Return as a structured JSON with:
- technical_skills: list of technical skills
- soft_skills: list of soft skills
- experience_level: 'beginner', 'intermediate', or 'advanced'
- domain_expertise: list of domains/industries

Resume:
{resume_text}

Return only valid JSON, no markdown.
"""

JOB_ANALYSIS_PROMPT = """
Analyze this job description and extract required skills and qualifications. Return as structured JSON with:
- required_skills: list of required technical skills
- nice_to_have: list of nice-to-have skills
- experience_required: 'beginner', 'junior', 'intermediate', or 'senior'
- role_category: the role category
- domain: primary domain/industry

Job Description:
{job_text}

Return only valid JSON, no markdown.
"""
