# LLM Career Placement Engine - Backend

## 🎯 Project Overview

This is a **backend-first LLM-powered resume-job matching system** that uses:
- **Google Gemini API** for intelligent skill extraction
- **Hybrid matching algorithm** (LLM + rule-based)
- **SQLite** for data persistence
- **Python** for all core logic

## 📁 Project Structure

```
LLM_Project/
├── data/                          # Data generation and storage
│   ├── resume_generator.py       # Synthetic resume generation
│   ├── job_generator.py          # Job description generation
│   ├── resumes.json              # Generated resumes
│   ├── jobs.json                 # Generated jobs
│   └── placement_engine.db       # SQLite database
│
├── src/                           # Core backend modules
│   ├── llm_service.py            # Gemini API integration
│   ├── skill_extractor.py        # Extract skills using LLM
│   ├── resume_parser.py          # Parse resumes
│   ├── job_parser.py             # Parse job descriptions
│   ├── matching_engine.py        # Hybrid matching algorithm
│   └── database_manager.py       # SQLite operations
│
├── tests/                         # Testing and evaluation
│   └── evaluate.py               # Evaluation metrics
│
├── output/                        # Results and reports
│   ├── evaluation_report.json    # Performance metrics
│   └── complete_results.json     # Full results
│
├── config.py                      # Configuration
├── main.py                        # Main orchestrator
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Setup

```bash
# Navigate to project directory
cd LLM_Project

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Go to https://ai.google.dev/
2. Sign up for free and get your API key
3. Create `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### 3. Run Complete Pipeline

```bash
python main.py
```

This will:
- ✅ Generate 60 synthetic resumes + 22 job descriptions
- ✅ Extract skills using Gemini
- ✅ Calculate matching scores
- ✅ Store in SQLite database
- ✅ Generate evaluation report

## 📊 Output Files

After running `main.py`, check:

- **`output/evaluation_report.json`** - Performance metrics
- **`output/complete_results.json`** - Full matching results
- **`data/placement_engine.db`** - SQLite database with all data

## 🧠 Hybrid Matching Algorithm

**4-component scoring system:**

```
Overall Score = (0.40 × Skill Overlap) 
              + (0.35 × Semantic Similarity)
              + (0.15 × Experience Match)
              + (0.10 × Domain Match)

Result: 0-100 score
```

### Components:

1. **Skill Overlap (40%)** - Jaccard similarity of skills
2. **Semantic Similarity (35%)** - How well resume matches job scope
3. **Experience Match (15%)** - Years/level alignment
4. **Domain Match (10%)** - Industry/expertise alignment

## 📈 Expected Results

When pipeline completes, you'll see:

```
Average Match Score: ~65%
Same-Role Matches: 45-55% (higher scores)
Different-Role Matches: 30-40% (lower scores)
```

This shows the algorithm correctly identifies better matches for same roles.

## 🔧 Configuration

Edit `config.py` to customize:

```python
NUM_RESUMES = 60              # Number of synthetic resumes
NUM_JOBS = 22                 # Number of job descriptions
CORE_ROLES = [...]            # Roles to generate

# Matching weights
WEIGHTS = {
    "skill_overlap": 0.40,
    "semantic_similarity": 0.35,
    "experience_match": 0.15,
    "domain_match": 0.10
}
```

## 🧪 Testing Individual Components

### Generate Only Resumes & Jobs
```python
from data.resume_generator import ResumeGenerator
gen = ResumeGenerator()
resumes = gen.generate_dataset(60)
```

### Test LLM Service
```python
from src.llm_service import GeminiService
service = GeminiService()
response = service.call_gemini("Extract skills: Python, Java, SQL")
```

### Test Matching Engine
```python
from src.matching_engine import MatchingEngine
engine = MatchingEngine()
score = engine.calculate_match_score(resume_skills, job_requirements)
```

## 📊 Database Operations

```python
from src.database_manager import DatabaseManager
db = DatabaseManager()

# Query data
resumes = db.get_all_resumes()
jobs = db.get_all_jobs()

# Get statistics
stats = db.get_match_statistics()
```

## 🎓 What This Demonstrates

✅ **LLM Integration** - Working with Gemini API  
✅ **Data Processing** - Resume/job parsing  
✅ **Algorithm Design** - Hybrid matching  
✅ **Database Management** - SQLite operations  
✅ **Evaluation** - Performance metrics  
✅ **Scalability** - Handles 100+ resumes/jobs  

## 🔮 Next Steps (For Website)

Once backend is validated, add:
1. Flask API endpoints
2. HTML/React frontend
3. File upload (PDF resume parsing)
4. Real-time job search
5. User authentication

## ⚠️ Important Notes

- **First run will mock LLM** if API key not set (for testing)
- **Real LLM calls** once `.env` configured
- **~2-5 minutes** for full pipeline with Gemini API
- **Free tier** has rate limits (100 requests/minute)

## 📞 Troubleshooting

**API Not Working?**
- Check `.env` has valid GEMINI_API_KEY
- Verify internet connection
- Check API usage limits on dashboard

**Database Errors?**
- Delete `data/placement_engine.db` and rerun
- Ensure write permissions on `data/` folder

**Import Errors?**
- Run `pip install -r requirements.txt` again
- Ensure Python 3.8+

## 📚 Resources

- Gemini API: https://ai.google.dev/
- SQLite: https://www.sqlite.org/
- Jaccard Similarity: https://en.wikipedia.org/wiki/Jaccard_index
- Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity

---

**Status:** Backend Ready ✅  
**Next:** Frontend (when backend validated)
