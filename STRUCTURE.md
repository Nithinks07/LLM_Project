# Project Structure

## Directory Organization

```
LLM_Project/
│
├── web/                                    # NEW: Web Application
│   ├── app.py                             # Professional Flask application
│   ├── templates/                         # HTML templates
│   │   ├── index.html                     # Home page with upload & matching
│   │   ├── dashboard.html                 # Analytics dashboard
│   │   ├── about.html                     # About page
│   │   └── results.html                   # Results page
│   ├── static/                            # Static assets
│   │   ├── css/
│   │   │   └── main.css                   # Professional styling (800+ lines)
│   │   ├── js/
│   │   │   ├── main.js                    # Home page logic (400+ lines)
│   │   │   └── dashboard.js               # Analytics visualization
│   │   └── img/                           # Images (for future use)
│   └── uploads/                           # Uploaded resume storage
│
├── src/                                    # Backend Modules
│   ├── __init__.py
│   ├── llm_service.py                     # Google Gemini API wrapper
│   ├── skill_extractor.py                 # Extract skills from resumes
│   ├── matching_engine.py                 # 4-component matching algorithm
│   ├── database_manager.py                # Database operations
│   ├── resume_parser.py                   # Parse resume data
│   ├── job_parser.py                      # Parse job descriptions
│   └── evaluate.py                        # System evaluation
│
├── data/                                   # Generated Data
│   ├── __init__.py
│   ├── resumes.json                       # 60+ Resume profiles
│   ├── jobs.json                          # 22 Job listings
│   ├── job_generator.py                   # Generate job data
│   ├── resume_generator.py                # Generate resume data
│   └── placement_engine.db                # SQLite database
│
├── tests/                                  # Testing
│   ├── __init__.py
│   └── evaluate.py                        # Evaluation metrics
│
├── llmenv/                                 # Python Virtual Environment
│   ├── Scripts/
│   │   └── python.exe                     # Python 3.13 executable
│   └── Lib/
│       └── site-packages/                 # Installed packages
│
├── output/                                 # Output directory for reports
│
├── main.py                                 # Orchestration pipeline
├── config.py                               # Configuration & constants
├── setup_verify.py                         # Verification script
├── requirements.txt                        # Python dependencies
│
├── README.md                               # Project documentation
├── QUICK_START.md                          # Getting started guide
├── PROJECT_SUMMARY.md                      # Executive summary
├── VIVA_GUIDE.md                           # Presentation guide
└── STRUCTURE.md                            # This file
```

## Key Components

### Web Application (`web/`)
- **Flask Backend** (`app.py`): REST API with 7 routes
  - Pages: Home (`/`), Dashboard (`/dashboard`), Results (`/results`), About (`/about`)
  - APIs: Upload (`/api/upload-resume`), Match (`/api/match-jobs`), Details (`/api/job-details/<id>`), Report (`/api/evaluation-report`)
  
- **Frontend** (`templates/` + `static/`)
  - HTML5 semantic templates with Jinja2 templating
  - Modern CSS with custom properties and responsive design
  - JavaScript with Vanilla DOM manipulation (no jQuery/React)
  - Chart.js for analytics visualization

### Backend Services (`src/`)
- **LLM Service**: Google Gemini API integration for skill extraction
- **Skill Extractor**: Parse and categorize skills from unstructured text
- **Matching Engine**: Hybrid algorithm combining:
  - 40% Skill-based matching (cosine similarity)
  - 35% Semantic similarity (LLM understanding)
  - 15% Experience level matching
  - 10% Domain expertise matching
- **Database Manager**: SQLite for persistent data storage
- **Parsers**: Resume and Job description parsing utilities

### Data Layer (`data/`)
- **resumes.json**: 60+ generated resume profiles with varied skills/experience
- **jobs.json**: 22 job listings across multiple roles and industries
- **Database**: SQLite for structured queries and analysis

## Technology Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| **Frontend** | HTML5 + CSS3 + JavaScript | No frameworks - lightweight & fast |
| **Framework** | Flask 3.0.2 | Lightweight Python web framework |
| **Backend** | Python 3.13 | High-level programming language |
| **Database** | SQLite | Lightweight relational database |
| **API** | Google Gemini API | Advanced LLM for skill extraction |
| **ML** | scikit-learn | Machine learning utilities |
| **Utilities** | numpy, pandas | Data processing libraries |
| **Viz** | Chart.js | Client-side charting library |

## File Size Summary

```
web/app.py                  ~300 lines
web/static/css/main.css     ~800 lines
web/static/js/main.js       ~400 lines
web/static/js/dashboard.js  ~150 lines
web/templates/index.html    ~200 lines
web/templates/dashboard.html ~300 lines
web/templates/about.html    ~350 lines

Total: ~2,500 lines of web code
```

## Data Summary

- **Resumes Processed**: 60+
- **Jobs Analyzed**: 22
- **Total Comparisons**: 1,320
- **Average Match Score**: 74.25%
- **Database Size**: ~500KB

## Setup & Deployment

### Quick Start
```bash
# Activate virtual environment
cd LLM_Project
.\llmenv\Scripts\Activate.ps1

# Start web application
python web/app.py
```

The web app will be available at `http://localhost:5000`

### Required Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (for LLM features)
- `PYTHONPATH`: Should include project root for module imports

### Dependencies
See `requirements.txt` for complete list of Python packages and versions.

## Workflow

1. **User uploads resume** → Flask API validates and stores file
2. **AI extracts skills** → Gemini API analyzes resume and identifies skills
3. **Skills are matched** → System compares against 22 job listings
4. **Results are ranked** → 4-component algorithm generates match scores
5. **Results displayed** → Frontend shows ranked jobs with breakdowns
6. **Analytics available** → Dashboard shows system performance metrics

## Future Enhancements

- [ ] User authentication and profile management
- [ ] Job recommendation engine
- [ ] Skill development tracking
- [ ] Integration with actual job boards (LinkedIn, Indeed, etc.)
- [ ] Mobile application
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Resume optimization suggestions
