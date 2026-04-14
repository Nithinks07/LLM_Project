from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from pathlib import Path
from src.job_parser import JobParser
from src.skill_extractor import SkillExtractor
from src.matching_engine import MatchingEngine
from src.database_manager import DatabaseManager
from config import PROJECT_ROOT, WEIGHTS

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
skill_extractor = SkillExtractor()
matching_engine = MatchingEngine(weights=WEIGHTS)
job_parser = JobParser()

def extract_text_from_file(filepath):
    """Extract text from TXT file or simple PDF-like text"""
    filepath = str(filepath)
    
    try:
        # Try reading as text file first
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        if text.strip():
            return text
        else:
            raise Exception("File is empty")
    
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

@app.route('/')
def index():
    """Home page - resume upload interface"""
    return render_template('index.html')

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload and parsing"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        resume_text = extract_text_from_file(filepath)
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Resume file is empty or too short. Please upload a valid resume with at least 50 characters.'}), 400
        
        # Extract skills using Gemini LLM
        extracted_skills = skill_extractor.extract_resume_skills(resume_text)
        
        # Store session data
        session_data = {
            'resume_text': resume_text,
            'extracted_skills': extracted_skills,
            'filename': filename
        }
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and parsed successfully',
            'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text,
            'extracted_skills': extracted_skills,
            'filename': filename
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route('/api/match-jobs', methods=['POST'])
def match_jobs():
    """Match resume with available jobs"""
    try:
        data = request.json
        resume_skills = data.get('extracted_skills', {})
        
        # Load all jobs from the generated dataset
        jobs_file = PROJECT_ROOT / "data" / "jobs.json"
        
        if not jobs_file.exists():
            return jsonify({'error': 'Jobs database not found. Please run main.py first.'}), 400
        
        with open(jobs_file, 'r') as f:
            jobs_data = json.load(f)
        
        # Parse jobs to extract requirements
        job_requirements = []
        for idx, job in enumerate(jobs_data):
            # Parse job using JobParser
            parsed_requirements = job_parser.parse_job(job)
            parsed_requirements['job_index'] = idx
            parsed_requirements['original_data'] = job
            
            # Extract skills from job - just get the job description text
            job_text = job.get('job_description', '') + ' ' + json.dumps(job)
            try:
                job_skills = skill_extractor.extract_job_skills(job_text)
            except:
                # Fallback if skill extraction fails
                job_skills = {
                    'required_skills': job.get('required_skills', []),
                    'nice_to_have': job.get('nice_to_have', []),
                    'experience_required': job.get('experience_required', 'junior')
                }
            
            parsed_requirements['extracted_requirements'] = job_skills
            job_requirements.append(parsed_requirements)
        
        # Match resume with all jobs
        matches = matching_engine.find_best_jobs_for_resume(
            job_requirements, 
            resume_skills, 
            top_k=10
        )
        
        # Format results
        results = []
        for match in matches:
            results.append({
                'job_role': match['job_role'],
                'job_company': match['job_company'],
                'overall_score': round(match['overall_score'], 2),
                'component_scores': match['component_scores'],
                'job_index': match['job_index']
            })
        
        return jsonify({
            'success': True,
            'matches': results,
            'total_jobs_searched': len(job_requirements),
            'top_matches_shown': len(results)
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error matching jobs: {str(e)}'}), 500

@app.route('/api/job-details/<int:job_index>')
def get_job_details(job_index):
    """Get detailed information about a specific job"""
    try:
        jobs_file = PROJECT_ROOT / "data" / "jobs.json"
        
        with open(jobs_file, 'r') as f:
            jobs_data = json.load(f)
        
        if job_index >= len(jobs_data):
            return jsonify({'error': 'Job not found'}), 404
        
        job = jobs_data[job_index]
        parsed_job = job_parser.parse_job(job)
        
        return jsonify({
            'success': True,
            'job': {
                'index': job_index,
                'role': parsed_job.get('role', 'N/A'),
                'company': parsed_job.get('company', 'N/A'),
                'description': parsed_job.get('job_description', 'N/A'),
                'requirements': parsed_job.get('required_skills', []),
                'nice_to_have': parsed_job.get('nice_to_have', []),
                'experience_required': parsed_job.get('experience_required', 'N/A'),
                'salary_range': parsed_job.get('salary_range', 'N/A')
            }
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error fetching job details: {str(e)}'}), 500

@app.route('/results')
def results():
    """Results page - displays match results"""
    return render_template('results.html')

@app.route('/api/evaluation-report')
def evaluation_report():
    """Get the evaluation report"""
    try:
        report_file = PROJECT_ROOT / "output" / "evaluation_report.json"
        
        if not report_file.exists():
            return jsonify({'error': 'Evaluation report not found'}), 404
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'error': f'Error loading report: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
