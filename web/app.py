"""
LLM Career Placement Engine - Flask Web Application
Professional version with proper project structure
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path

# Import backend modules
from src.job_parser import JobParser
from src.skill_extractor import SkillExtractor
from src.matching_engine import MatchingEngine
from config import PROJECT_ROOT, WEIGHTS

# Configuration
class Config:
    """Application configuration"""
    UPLOAD_FOLDER = 'web/uploads'
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB
    TEMPLATE_FOLDER = 'web/templates'
    STATIC_FOLDER = 'web/static'

# Create Flask app
app = Flask(__name__, 
            template_folder=Config.TEMPLATE_FOLDER,
            static_folder=Config.STATIC_FOLDER,
            static_url_path='/static')

app.config.from_object(Config)

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
skill_extractor = SkillExtractor()
matching_engine = MatchingEngine(weights=WEIGHTS)
job_parser = JobParser()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_text_from_file(filepath):
    """Extract text from uploaded file"""
    filepath = str(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        if text.strip():
            return text
        else:
            raise ValueError("File is empty")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def validate_uploaded_file(filename):
    """Validate uploaded file"""
    if not filename:
        raise ValueError("No filename provided")
    
    # Check file extension
    allowed_extensions = {'txt', 'pdf', 'doc', 'docx'}
    if '.' not in filename:
        raise ValueError("File has no extension")
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"File type .{ext} not allowed. Allowed: {', '.join(allowed_extensions)}")
    
    return ext

# ============================================================================
# ROUTES - PAGES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

@app.route('/results')
def results():
    """Results page"""
    return render_template('results.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# ============================================================================
# API ROUTES - RESUME UPLOAD & PROCESSING
# ============================================================================

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload and skill extraction"""
    try:
        # Validate request
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No resume file provided'
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        try:
            ext = validate_uploaded_file(file.filename)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        
        # Save file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text
        resume_text = extract_text_from_file(filepath)
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({
                'success': False,
                'error': 'Resume too short. Minimum 50 characters required.'
            }), 400
        
        # Extract skills using Gemini
        extracted_skills = skill_extractor.extract_resume_skills(resume_text)
        
        return jsonify({
            'success': True,
            'message': 'Resume processed successfully',
            'filename': filename,
            'resume_preview': resume_text[:300] + '...',
            'extracted_skills': extracted_skills
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        }), 500

# ============================================================================
# API ROUTES - JOB MATCHING
# ============================================================================

@app.route('/api/match-jobs', methods=['POST'])
def match_jobs():
    """Find matching jobs for resume"""
    try:
        data = request.json
        resume_skills = data.get('extracted_skills', {})
        
        if not resume_skills:
            return jsonify({
                'success': False,
                'error': 'Invalid skills data'
            }), 400
        
        # Load jobs
        jobs_file = PROJECT_ROOT / "data" / "jobs.json"
        if not jobs_file.exists():
            return jsonify({
                'success': False,
                'error': 'Jobs database not found'
            }), 404
        
        with open(jobs_file, 'r') as f:
            jobs_data = json.load(f)
        
        # Process jobs
        job_requirements = []
        for idx, job in enumerate(jobs_data):
            parsed_job = job_parser.parse_job(job)
            parsed_job['job_index'] = idx
            
            # Extract skills with fallback
            try:
                job_text = job.get('job_description', '') + ' ' + json.dumps(job)
                job_skills = skill_extractor.extract_job_skills(job_text)
            except:
                job_skills = {
                    'required_skills': job.get('required_skills', []),
                    'nice_to_have': job.get('nice_to_have', []),
                    'experience_required': job.get('experience_required', 'junior')
                }
            
            parsed_job['extracted_requirements'] = job_skills
            job_requirements.append(parsed_job)
        
        # Match and rank
        matches = matching_engine.find_best_jobs_for_resume(
            job_requirements, 
            resume_skills, 
            top_k=10
        )
        
        # Format results
        results = [{
            'job_role': m['job_role'],
            'job_company': m['job_company'],
            'overall_score': round(m['overall_score'], 2),
            'component_scores': m['component_scores'],
            'job_index': m['job_index']
        } for m in matches]
        
        return jsonify({
            'success': True,
            'matches': results,
            'total_jobs': len(job_requirements),
            'matches_found': len(results)
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Matching error: {str(e)}'
        }), 500

# ============================================================================
# API ROUTES - JOB DETAILS
# ============================================================================

@app.route('/api/job-details/<int:job_index>', methods=['GET'])
def get_job_details(job_index):
    """Get detailed job information"""
    try:
        jobs_file = PROJECT_ROOT / "data" / "jobs.json"
        
        with open(jobs_file, 'r') as f:
            jobs_data = json.load(f)
        
        if job_index >= len(jobs_data):
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
        
        job_data = jobs_data[job_index]
        parsed_job = job_parser.parse_job(job_data)
        
        return jsonify({
            'success': True,
            'job': {
                'index': job_index,
                'role': parsed_job.get('role', 'N/A'),
                'company': parsed_job.get('company', 'N/A'),
                'description': parsed_job.get('job_description', 'N/A'),
                'requirements': parsed_job.get('required_skills', []),
                'nice_to_have': parsed_job.get('nice_to_have', []),
                'experience': parsed_job.get('experience_required', 'N/A'),
                'salary': parsed_job.get('salary_range', 'N/A')
            }
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# API ROUTES - ANALYTICS
# ============================================================================

@app.route('/api/evaluation-report', methods=['GET'])
def get_evaluation_report():
    """Get system evaluation report"""
    try:
        report_file = PROJECT_ROOT / "output" / "evaluation_report.json"
        
        if not report_file.exists():
            return jsonify({
                'success': False,
                'error': 'Report not found. Run main.py first.'
            }), 404
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 LLM CAREER PLACEMENT ENGINE - WEB SERVER")
    print("="*70)
    print("\n📱 Web Interface: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("ℹ️  About: http://localhost:5000/about")
    print("\n⏸️  Press Ctrl+C to stop the server\n")
    print("="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
