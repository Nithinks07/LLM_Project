# Generate diverse job descriptions for testing
import json
import random
from pathlib import Path

class JobGenerator:
    """Generate diverse job descriptions"""
    
    JOBS_DATA = {
        "Software Engineer": {
            "descriptions": [
                "We are looking for a Software Engineer to build scalable backend systems using Python and cloud technologies.",
                "Join our team as a Software Engineer and work on distributed systems, microservices, and cloud infrastructure.",
                "Hiring Software Engineer: Strong in Data Structures, System Design, and modern development practices."
            ],
            "required_skills": ["Python", "System Design", "SQL", "Git"],
            "nice_to_have": ["Docker", "Kubernetes", "MongoDB", "AWS"],
            "experience": "junior"
        },
        "Data Scientist": {
            "descriptions": [
                "Data Scientist needed to build ML models, analyze data, and derive actionable insights.",
                "Join our Analytics team as a Data Scientist. Work with Python, ML frameworks, and big data.",
                "Seeking Data Scientist: Strong background in Statistics, ML, and data engineering."
            ],
            "required_skills": ["Python", "Machine Learning", "SQL", "Statistics"],
            "nice_to_have": ["TensorFlow", "Spark", "Tableau", "Deep Learning"],
            "experience": "junior"
        },
        "Product Manager": {
            "descriptions": [
                "Product Manager to lead product strategy, roadmap, and go-to-market initiatives.",
                "Seeking experienced Product Manager with strong analytical and communication skills.",
                "PM role: Own product vision, drive prioritization, and collaborate with engineering and design."
            ],
            "required_skills": ["Product Strategy", "Analytics", "Communication", "User Research"],
            "nice_to_have": ["A/B Testing", "SQL", "Data Analysis", "Agile"],
            "experience": "intermediate"
        },
        "UX Designer": {
            "descriptions": [
                "UX Designer to craft user experiences, create wireframes, and user research.",
                "Design passionate UX Designer needed to build beautiful and intuitive interfaces.",
                "Hiring UX Designer: Expert in user research, prototyping, and design systems."
            ],
            "required_skills": ["UI/UX Design", "Figma", "User Research", "Prototyping"],
            "nice_to_have": ["Design Systems", "CSS", "HTML", "User Testing"],
            "experience": "junior"
        },
        "DevOps Engineer": {
            "descriptions": [
                "DevOps Engineer to manage CI/CD pipelines, infrastructure, and cloud systems.",
                "Seeking DevOps Engineer with expertise in containerization and orchestration.",
                "Hiring DevOps: Strong in Docker, Kubernetes, scripting, and cloud platforms."
            ],
            "required_skills": ["Docker", "CI/CD", "Linux", "Cloud Platforms"],
            "nice_to_have": ["Kubernetes", "Terraform", "Monitoring Tools", "Python"],
            "experience": "intermediate"
        }
    }
    
    COMPANIES = [
        "TechCorp", "DataStream", "CloudServices Inc", "FinTech Solutions",
        "AI Labs", "WebScale Systems", "Digital Innovations", "NextGen Tech",
        "SmartData Co", "CloudXpress", "Platform One"
    ]
    
    def generate_job(self, role):
        """Generate a single job description"""
        job_data = self.JOBS_DATA.get(role, self.JOBS_DATA["Software Engineer"])
        
        company = random.choice(self.COMPANIES)
        description = random.choice(job_data["descriptions"])
        salary_range = random.randint(4, 16)  # in lakhs
        
        job = f"""
JOB DESCRIPTION
===============

Company: {company}
Position: {role}
Location: Bangalore, India
Salary: ₹{salary_range}-{salary_range+3} LPA

DESCRIPTION:
{description}

REQUIREMENTS:
- {salary_range} years of experience in related field
- Strong problem-solving skills
- Team player with good communication
- Experience with {', '.join(random.sample(job_data['required_skills'], 2))}

NICE TO HAVE:
- Experience with {', '.join(random.sample(job_data['nice_to_have'], 2))}
- Experience with emerging technologies
- Contributions to open source

ABOUT US:
We are a fast-growing tech company focused on innovative solutions.
"""
        
        return {
            "role": role,
            "company": company,
            "job_description": job,
            "required_skills": job_data["required_skills"],
            "nice_to_have": job_data["nice_to_have"],
            "experience_required": job_data["experience"],
            "salary_range": f"{salary_range}-{salary_range+3} LPA"
        }
    
    def generate_dataset(self, num_jobs=22):
        """Generate diverse job descriptions"""
        roles = list(self.JOBS_DATA.keys())
        jobs = []
        
        # Balanced distribution
        per_role = num_jobs // len(roles)
        remaining = num_jobs % len(roles)
        
        for idx, role in enumerate(roles):
            count = per_role + (1 if idx < remaining else 0)
            for _ in range(count):
                jobs.append(self.generate_job(role))
        
        return jobs


if __name__ == "__main__":
    generator = JobGenerator()
    jobs = generator.generate_dataset(22)
    
    output_path = Path(__file__).parent / "jobs.json"
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)
    
    print(f"✅ Generated {len(jobs)} job descriptions")
    print(f"📁 Saved to: {output_path}")
    print(f"\nSample Job:")
    print(jobs[0])
