# 🎨 Web Interface Guide

## Quick Start

### Option 1: Using Python Script (Recommended)
```bash
python run_app.py
```

### Option 2: Using Batch File (Windows)
```bash
run_webapp.bat
```

### Option 3: Direct Flask Command
```bash
flask run
```

The web server will start at: **http://localhost:5000**

---

## 🏠 Features

### 1. **Home Page** (`/`)
Upload your resume and get matched with the best job opportunities

**What you can do:**
- Drag and drop resume files (PDF or TXT)
- View extracted skills and information
- Get instant job matches
- Filter results by score

**Step-by-step:**
1. Upload a resume (PDF or TXT format)
2. System extracts: technical skills, experience level, domains, tools
3. Click "Find Matching Jobs"
4. View top 10 job matches with scores
5. Click "View Details" to see job description, requirements, salary

---

### 2. **Results Dashboard** (`/results`)
View and analyze your match results

**Displays:**
- Overall match score (0-100%)
- Component score breakdown:
  - Skill Overlap (40 weight)
  - Semantic Similarity (35 weight)
  - Experience Match (15 weight)
  - Domain Match (10 weight)
- Job description and requirements
- Salary range
- Nice-to-have skills

**Filtering:**
- Use score slider to filter by minimum match score
- See only relevant jobs

---

### 3. **Analytics Dashboard** (`/dashboard`)
System-wide performance metrics

**What's displayed:**
- **Summary Statistics:**
  - Total resumes processed (60)
  - Total jobs in database (22)
  - Average match score
  - Total comparisons made

- **Score Distribution:**
  - Histogram of all match scores
  - Visual representation of score ranges

- **Detailed Metrics:**
  - Mean, median, min, max scores
  - Standard deviation
  - Score distribution

- **Role-Based Analysis:**
  - Same-role matches vs different-role
  - Average scores for each category
  - Shows algorithm discrimination power

- **Algorithm Breakdown:**
  - Shows the 4-component matching algorithm
  - 40% Skill Overlap
  - 35% Semantic Similarity
  - 15% Experience Match
  - 10% Domain Match

- **Key Observations:**
  - Auto-generated insights
  - Algorithm performance notes

---

## 📡 API Endpoints

### Resume Upload
**POST** `/api/upload-resume`
```json
Request: multipart/form-data with 'resume' file
Response: {
  "success": true,
  "filename": "resume.pdf",
  "resume_text": "...",
  "extracted_skills": {
    "technical_skills": ["Python", "SQL"],
    "experience_level": "intermediate",
    "domains": ["Data Science"],
    "tools": ["TensorFlow"]
  }
}
```

### Match Jobs
**POST** `/api/match-jobs`
```json
Request: {
  "extracted_skills": { ... }
}
Response: {
  "success": true,
  "matches": [
    {
      "job_role": "Software Engineer",
      "job_company": "TechCorp",
      "overall_score": 85.5,
      "component_scores": { ... }
    }
  ],
  "total_jobs_searched": 22,
  "top_matches_shown": 10
}
```

### Job Details
**GET** `/api/job-details/<job_index>`
```json
Response: {
  "success": true,
  "job": {
    "role": "Data Scientist",
    "company": "DataXpress",
    "description": "...",
    "requirements": ["Python", "SQL"],
    "nice_to_have": ["ML models"],
    "experience_required": "Intermediate",
    "salary_range": "$80K - $120K"
  }
}
```

### Evaluation Report
**GET** `/api/evaluation-report`
```json
Response: {
  "summary": {
    "total_resumes": 60,
    "total_jobs": 22,
    "average_match_score": 74.25
  },
  "detailed_metrics": { ... },
  "observations": [...]
}
```

---

## 🎯 Workflow Example

### Scenario: Job-Seeking Software Engineer

1. **Open web interface:** `http://localhost:5000`

2. **Upload resume** (e.g., "John_Resume.pdf")
   - Extracts: "Python", "5 years experience", "Backend Development"

3. **Click "Find Matching Jobs"**
   - System searches all 22 jobs
   - Calculates 4-component match scores
   - Returns top 10 matches

4. **View Results**
   - Software Engineer @ TechCorp: 92%
   - Backend Dev @ DataXpress: 87%
   - Senior Dev @ CloudIt: 76%
   - ...

5. **Click "View Details" on top match**
   - See full job description
   - View required skills
   - Check salary range ($100K-130K)
   - Identify missing skills: "Docker", "Kubernetes"

6. **Check Dashboard** (`/dashboard`)
   - See system performance
   - Learn how algorithm works
   - View all 1,320 comparisons analysis

---

## 🔧 Technical Details

### Backend Stack
- **Framework:** Flask (Python)
- **LLM:** Google Gemini API
- **Database:** SQLite (data/placement_engine.db)
- **Algorithm:** Hybrid 4-component matching

### Frontend Stack
- **HTML:** Semantic markup
- **CSS:** Custom styling with CSS variables
- **JavaScript:** Vanilla JS (no frameworks)
- **Charts:** Chart.js for analytics

### File Structure
```
├── app.py                    # Flask application
├── templates/
│   ├── index.html           # Home page
│   ├── results.html         # Results page (optional)
│   └── dashboard.html       # Analytics dashboard
├── static/
│   ├── style.css            # Main stylesheet
│   ├── app.js               # Home page logic
│   └── dashboard.js         # Dashboard logic
├── uploads/                 # Uploaded resumes
└── data/
    ├── jobs.json            # Job database
    └── resumes.json         # Resume database
```

---

## 📊 Understanding the Scores

### Score Components (Total: 100%)

1. **Skill Overlap (40%)**
   - Jaccard similarity of technical skills
   - Does the resume have the required skills?
   - Example: Resume has 8/10 required skills = 80%

2. **Semantic Similarity (35%)**
   - Cosine similarity of skill embeddings
   - Are skills semantically related?
   - Example: "Python" matches "backend development"

3. **Experience Match (15%)**
   - Does experience level align?
   - Junior role needs: Junior/intermediate candidate
   - Senior role needs: Senior/expert candidate

4. **Domain Match (10%)**
   - Is domain expertise relevant?
   - Data Science background for Data role
   - Finance background for FinTech role

### Example Score Breakdown
```
Overall Score: 82.5%

Component Breakdown:
├─ Skill Overlap:         85% × 0.40 = 34.0%
├─ Semantic Similarity:   78% × 0.35 = 27.3%
├─ Experience Match:      90% × 0.15 = 13.5%
└─ Domain Match:          75% × 0.10 = 7.7%

Total: 34.0 + 27.3 + 13.5 + 7.7 = 82.5%
```

---

## ⚠️ Troubleshooting

### Issue: Flask won't start
**Solution:**
```bash
pip install flask
python run_app.py
```

### Issue: Port 5000 already in use
**Solution:**
```bash
# Change port in app.py
app.run(port=5001)  # Use 5001 instead
```

### Issue: No jobs database
**Solution:**
```bash
# First run the main pipeline
python main.py

# Then start the web interface
python run_app.py
```

### Issue: Resume not parsing
**Supported formats:** PDF, TXT
- Try converting to TXT
- Ensure file is not corrupted
- Try a different resume file

---

## 🚀 Production Deployment (Future Enhancement)

For production use:

1. **Enable HTTPS:**
   ```python
   from werkzeug.serving import run_simple
   run_simple(..., ssl_context='adhoc')
   ```

2. **Use production server:**
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

3. **Add database:**
   ```python
   # Use PostgreSQL instead of SQLite
   SQLALCHEMY_DATABASE_URI = 'postgresql://...'
   ```

4. **Add authentication:**
   ```python
   from flask_login import LoginManager
   ```

5. **Deploy on cloud:**
   - Heroku
   - AWS EC2
   - Google Cloud Platform
   - Azure App Service

---

## 📝 Notes

- The web app uses the existing data from `main.py`
- Resume uploads are temporary (stored in `uploads/` folder)
- Job database is fixed (60 synthetic jobs + resumes)
- For real data, integrate with LinkedIn API or job scraper

---

## Questions?

Refer to the main README.md for project overview and architecture details.
