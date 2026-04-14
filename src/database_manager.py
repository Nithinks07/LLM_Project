# Database manager for storing and retrieving data
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class DatabaseManager:
    """Manage SQLite database for resumes, jobs, and matches"""
    
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or Path(__file__).parent.parent / "data" / "placement_engine.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                target_role TEXT,
                years_experience INTEGER,
                resume_text TEXT,
                extracted_skills JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                company TEXT,
                job_description TEXT,
                required_skills JSON,
                nice_to_have JSON,
                experience_required TEXT,
                extracted_requirements JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                job_id INTEGER,
                overall_score REAL,
                component_scores JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_resume(self, resume_data: Dict) -> int:
        """Insert a resume into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resumes (name, email, phone, target_role, years_experience, resume_text)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            resume_data.get("name"),
            resume_data.get("email"),
            resume_data.get("phone"),
            resume_data.get("target_role"),
            resume_data.get("years_experience"),
            resume_data.get("resume_text")
        ))
        
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return resume_id
    
    def insert_job(self, job_data: Dict) -> int:
        """Insert a job into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO jobs (role, company, job_description, required_skills, nice_to_have, experience_required)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            job_data.get("role"),
            job_data.get("company"),
            job_data.get("job_description"),
            json.dumps(job_data.get("required_skills", [])),
            json.dumps(job_data.get("nice_to_have", [])),
            job_data.get("experience_required")
        ))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return job_id
    
    def insert_match(self, resume_id: int, job_id: int, match_score: float, 
                     component_scores: Dict) -> int:
        """Insert a match result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO matches (resume_id, job_id, overall_score, component_scores)
            VALUES (?, ?, ?, ?)
        ''', (
            resume_id,
            job_id,
            match_score,
            json.dumps(component_scores)
        ))
        
        match_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return match_id
    
    def batch_insert_resumes(self, resumes: List[Dict]) -> List[int]:
        """Insert multiple resumes"""
        ids = []
        for resume in resumes:
            ids.append(self.insert_resume(resume))
        return ids
    
    def batch_insert_jobs(self, jobs: List[Dict]) -> List[int]:
        """Insert multiple jobs"""
        ids = []
        for job in jobs:
            ids.append(self.insert_job(job))
        return ids
    
    def get_resume(self, resume_id: int) -> Dict:
        """Get resume by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "phone": result[3],
                "target_role": result[4],
                "years_experience": result[5],
                "resume_text": result[6]
            }
        return None
    
    def get_job(self, job_id: int) -> Dict:
        """Get job by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "role": result[1],
                "company": result[2],
                "job_description": result[3]
            }
        return None
    
    def get_all_resumes(self) -> List[Dict]:
        """Get all resumes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes')
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": r[0],
                "name": r[1],
                "email": r[2],
                "phone": r[3],
                "target_role": r[4],
                "years_experience": r[5]
            }
            for r in results
        ]
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs')
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": r[0],
                "role": r[1],
                "company": r[2]
            }
            for r in results
        ]
    
    def get_match_statistics(self) -> Dict:
        """Get matching statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM matches')
        total_matches = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(overall_score) FROM matches')
        avg_score = cursor.fetchone()[0]
        
        cursor.execute('SELECT MAX(overall_score) FROM matches')
        max_score = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_matches": total_matches,
            "average_score": round(avg_score, 2) if avg_score else 0,
            "max_score": round(max_score, 2) if max_score else 0
        }
    
    def clear_all_data(self):
        """Clear all data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM matches')
        cursor.execute('DELETE FROM resumes')
        cursor.execute('DELETE FROM jobs')
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db = DatabaseManager()
    stats = db.get_match_statistics()
    print(f"Database Statistics: {stats}")
