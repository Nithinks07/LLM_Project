# Generate synthetic and sample resumes for testing
import json
import random
from pathlib import Path

class ResumeGenerator:
    """Generate diverse synthetic resumes"""
    
    NAMES = [
        "Arjun Kumar", "Priya Singh", "Rahul Patel", "Neha Gupta", "Vikram Sharma",
        "Isha Nair", "Aditya Verma", "Sneha Desai", "Rohan Mehta", "Anjali Reddy",
        "Karan Chopra", "Divya Iyer", "Sanjay Kumar", "Pooja Sinha", "Deepak Nair",
        "Zara Khan", "Nikhil Rao", "Riya Das", "Aryan Singh", "Shreya Bhat",
        "James Wilson", "Sarah Tech", "Michael Dev", "Emma Cloud", "David AI"
    ]
    
    EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "company.com", "tech.com"]
    
    EXPERIENCES = {
        "Software Engineer": {
            "technical_skills": [
                ["Python", "JavaScript", "SQL"], ["Java", "Spring Boot", "Docker"],
                ["C++", "System Design", "Microservices"], ["React", "Node.js", "MongoDB"],
                ["Python", "Django", "PostgreSQL"]
            ],
            "soft_skills": ["Problem Solving", "Team Collaboration", "Communication"],
            "years_range": (0, 8),
            "companies": ["Google", "Amazon", "Microsoft", "TCS", "Infosys", "Startup"]
        },
        "Data Scientist": {
            "technical_skills": [
                ["Python", "Machine Learning", "SQL"], ["R", "TensorFlow", "Pandas"],
                ["Python", "Statistics", "Big Data"], ["SQL", "Tableau", "Python"],
                ["PyTorch", "NLP", "Python"]
            ],
            "soft_skills": ["Data Analysis", "Statistical Thinking", "Presentation"],
            "years_range": (0, 7),
            "companies": ["Google", "Amazon", "Facebook", "Analytics Firm", "Startup"]
        },
        "Product Manager": {
            "technical_skills": [
                ["Product Strategy", "Analytics", "SQL"], ["User Research", "Metrics", "A/B Testing"],
                ["Roadmap Planning", "Agile", "Communication"], ["Data Analysis", "Wireframing", "SQL"]
            ],
            "soft_skills": ["Leadership", "Strategic Thinking", "Communication", "Negotiation"],
            "years_range": (1, 10),
            "companies": ["Google", "Amazon", "Microsoft", "Startup", "Amazon"]
        },
        "UX Designer": {
            "technical_skills": [
                ["Figma", "UI Design", "Prototyping"], ["Adobe XD", "User Research", "Wireframing"],
                ["UI/UX", "Interaction Design", "Sketch"], ["Design Systems", "CSS", "Figma"]
            ],
            "soft_skills": ["Creativity", "User Empathy", "Communication", "Problem Solving"],
            "years_range": (0, 8),
            "companies": ["Google", "Meta", "Apple", "Design Studio", "Startup"]
        },
        "DevOps Engineer": {
            "technical_skills": [
                ["Docker", "Kubernetes", "AWS"], ["Jenkins", "CI/CD", "Linux"],
                ["Terraform", "Cloud", "Monitoring"], ["Ansible", "AWS", "Python"],
                ["GCP", "Docker", "Databases"]
            ],
            "soft_skills": ["Problem Solving", "Automation", "System Thinking"],
            "years_range": (1, 9),
            "companies": ["Google", "Amazon", "Cloud Provider", "Tech Company", "Startup"]
        }
    }
    
    def generate_resume(self, role):
        """Generate a single synthetic resume"""
        experiences = self.EXPERIENCES.get(role, self.EXPERIENCES["Software Engineer"])
        
        name = random.choice(self.NAMES)
        email = f"{name.lower().replace(' ', '.')}@{random.choice(self.EMAIL_DOMAINS)}"
        phone = f"+91-{random.randint(90000, 99999)}-{random.randint(10000, 99999)}"
        
        years = random.randint(*experiences["years_range"])
        skills = random.choice(experiences["technical_skills"]) + random.sample(experiences["soft_skills"], 2)
        company = random.choice(experiences["companies"])
        
        resume = f"""
RESUME
======

Name: {name}
Email: {email}
Phone: {phone}
Location: Bangalore, India

PROFESSIONAL SUMMARY
{name} is a {role} with {years} years of experience. Skilled in building scalable solutions and driving business impact.

SKILLS
{', '.join(skills)}

EXPERIENCE
{role} at {company}
Duration: {years} years
- Developed and maintained critical systems
- Led cross-functional teams
- Improved performance and efficiency
- Implemented best practices and standards

EDUCATION
B.Tech in Computer Science
IIT/NIT/Top Engineering College
2015-2019

CERTIFICATIONS
- {random.choice(['AWS Certified', 'Google Cloud Certified', 'Azure Certified', 'Scrum Master'])}
"""
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "target_role": role,
            "years_experience": years,
            "resume_text": resume
        }
    
    def generate_dataset(self, num_resumes=60):
        """Generate a diverse dataset of resumes"""
        roles = list(self.EXPERIENCES.keys())
        resumes = []
        
        # Balanced distribution across roles
        per_role = num_resumes // len(roles)
        remaining = num_resumes % len(roles)
        
        for idx, role in enumerate(roles):
            count = per_role + (1 if idx < remaining else 0)
            for _ in range(count):
                resumes.append(self.generate_resume(role))
        
        return resumes


if __name__ == "__main__":
    generator = ResumeGenerator()
    resumes = generator.generate_dataset(60)
    
    output_path = Path(__file__).parent / "resumes.json"
    with open(output_path, "w") as f:
        json.dump(resumes, f, indent=2)
    
    print(f"✅ Generated {len(resumes)} synthetic resumes")
    print(f"📁 Saved to: {output_path}")
    print(f"\nSample Resume:")
    print(resumes[0])
