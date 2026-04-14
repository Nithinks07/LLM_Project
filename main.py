# Main orchestrator - Run the complete matching pipeline
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import NUM_RESUMES, NUM_JOBS
from data.resume_generator import ResumeGenerator
from data.job_generator import JobGenerator
from src.resume_parser import ResumeParser
from src.job_parser import JobParser
from src.llm_service import GeminiService
from src.skill_extractor import SkillExtractor
from src.matching_engine import MatchingEngine
from src.database_manager import DatabaseManager
from tests.evaluate import EvaluationEngine

from dotenv import load_dotenv
load_dotenv()

def main():
    print("🚀 LLM Career Placement Engine - Complete Pipeline")
    print("=" * 60)
    
    # ✅ Step 1: Generate synthetic data
    print("\n📊 Step 1: Generating synthetic dataset...")
    resume_gen = ResumeGenerator()
    job_gen = JobGenerator()
    
    resumes = resume_gen.generate_dataset(NUM_RESUMES)
    jobs = job_gen.generate_dataset(NUM_JOBS)
    
    # Save to JSON
    resumes_path = PROJECT_ROOT / "data" / "resumes.json"
    jobs_path = PROJECT_ROOT / "data" / "jobs.json"
    
    with open(resumes_path, 'w') as f:
        json.dump(resumes, f, indent=2)
    with open(jobs_path, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print(f"  ✅ Generated {len(resumes)} resumes")
    print(f"  ✅ Generated {len(jobs)} jobs")
    
    # ✅ Step 2: Parse resume and jobs
    print("\n📖 Step 2: Parsing resumes and jobs...")
    resume_parser = ResumeParser(PROJECT_ROOT / "data")
    job_parser = JobParser(PROJECT_ROOT / "data")
    
    parsed_resumes = resume_parser.get_all_resumes()
    parsed_jobs = job_parser.get_all_jobs()
    
    print(f"  ✅ Parsed {len(parsed_resumes)} resumes")
    print(f"  ✅ Parsed {len(parsed_jobs)} jobs")
    
    # ✅ Step 3: Extract skills using LLM
    print("\n🤖 Step 3: Extracting skills using Gemini API...")
    gemini = GeminiService()
    extractor = SkillExtractor(gemini)
    
    print("  📝 Extracting resume skills...")
    resume_skills = extractor.batch_extract_resume_skills(parsed_resumes)
    
    print("  📝 Extracting job requirements...")
    job_requirements = extractor.batch_extract_job_skills(parsed_jobs)
    
    # ✅ Step 4: Calculate matches
    print("\n⚡ Step 4: Calculating resume-job matches...")
    engine = MatchingEngine()
    evaluator = EvaluationEngine()
    
    all_scores = {}
    
    # For each resume, find top 5 matching jobs
    for resume_idx, resume_data in enumerate(resume_skills):
        resume_name = resume_data.get("name", "Unknown")
        resume_role = resume_data.get("target_role", "Unknown")
        resume_skills_extracted = resume_data.get("extracted_skills", {})
        
        top_jobs = engine.find_best_jobs_for_resume(job_requirements, resume_skills_extracted, top_k=5)
        
        if resume_idx < 3:  # Print first 3 as sample
            print(f"\n  Resume: {resume_name} ({resume_role})")
            for job_match in top_jobs:
                print(f"    → {job_match['job_role']} at {job_match['job_company']}: {job_match['overall_score']}%")
        
        # Record for evaluation
        for job_req in job_requirements:
            score_result = engine.calculate_match_score(
                resume_skills_extracted,
                job_req.get("extracted_requirements", {})
            )
            
            evaluator.add_match_result(
                resume_idx,
                job_req.get("job_index", -1),
                score_result["overall_score"],
                score_result["component_scores"],
                resume_role,
                job_req.get("role", "")
            )
    
    # ✅ Step 5: Store in database
    print("\n💾 Step 5: Storing data in SQLite database...")
    db = DatabaseManager(PROJECT_ROOT / "data" / "placement_engine.db")
    db.clear_all_data()
    
    db.batch_insert_resumes(parsed_resumes)
    db.batch_insert_jobs(parsed_jobs)
    
    print(f"  ✅ Stored {len(parsed_resumes)} resumes in database")
    print(f"  ✅ Stored {len(parsed_jobs)} jobs in database")
    
    # ✅ Step 6: Generate evaluation report
    print("\n📊 Step 6: Generating evaluation report...")
    report = evaluator.generate_report(PROJECT_ROOT / "output" / "evaluation_report.json")
    
    print("\n📈 EVALUATION RESULTS:")
    print(f"  Total Comparisons: {report['summary']['total_matches_evaluated']}")
    print(f"  Average Match Score: {report['summary']['average_match_score']}%")
    
    print("\n📊 Detailed Statistics:")
    stats = report["detailed_metrics"]["statistics"]
    print(f"  Mean Score: {stats['mean_score']}%")
    print(f"  Median Score: {stats['median_score']}%")
    print(f"  Min-Max: {stats['min_score']}% - {stats['max_score']}%")
    print(f"  Std Dev: {stats['std_dev']}")
    
    print("\n🎯 Role-Based Analysis:")
    role_analysis = report["detailed_metrics"]["role_analysis"]
    print(f"  Same-Role Matches: {role_analysis['same_role_matches']} (avg: {role_analysis['same_role_avg_score']}%)")
    print(f"  Different-Role Matches: {role_analysis['different_role_matches']} (avg: {role_analysis['different_role_avg_score']}%)")
    
    print("\n💡 Observations:")
    for obs in report["observations"]:
        print(f"  • {obs}")
    
    # ✅ Step 7: Save sample results
    print("\n📁 Step 7: Saving sample results...")
    sample_results = {
        "total_resumes": len(parsed_resumes),
        "total_jobs": len(parsed_jobs),
        "sample_matching": all_scores,
        "evaluation_metrics": report
    }
    
    with open(PROJECT_ROOT / "output" / "complete_results.json", 'w') as f:
        json.dump(sample_results, f, indent=2)
    
    print("  ✅ Results saved to output/complete_results.json")
    print("  ✅ Report saved to output/evaluation_report.json")
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    main()
