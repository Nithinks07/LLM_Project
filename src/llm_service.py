# Groq API integration (replaces Google Gemini)
import json
import os
from typing import Dict, Any
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

class GeminiService:
    """Interface for Groq API (drop-in replacement for Gemini)"""
    
    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.init_client()
    
    def init_client(self):
        """Initialize Groq client"""
        if not self.api_key:
            print("⚠️  WARNING: GROQ_API_KEY not set. Set it in .env file. Running in mock mode.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            print(f"✅ Groq client initialized with model: {self.model}")
    
    def call_gemini(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Call Groq API with a prompt (method name retained for compatibility)
        
        Args:
            prompt: The prompt text
            temperature: Temperature for response (0-1)
            
        Returns:
            API response text
        """
        if self.client is None:
            return self._get_mock_response(prompt)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            return self._get_mock_response(prompt)
    
    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'```json\n?(.*?)\n?```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except:
                    pass
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            return {"error": "Could not parse JSON from response"}
    
    def _get_mock_response(self, prompt: str) -> str:
        """
        Return mock response when API is not available
        """
        if "Extract technical and professional skills" in prompt:
            return json.dumps({
                "technical_skills": ["Python", "SQL", "System Design"],
                "soft_skills": ["Problem Solving", "Communication"],
                "experience_level": "intermediate",
                "domain_expertise": ["Software", "Databases"]
            })
        elif "Analyze this job description" in prompt:
            return json.dumps({
                "required_skills": ["Python", "SQL"],
                "nice_to_have": ["Docker", "AWS"],
                "experience_required": "intermediate",
                "role_category": "Software Engineer",
                "domain": "Technology"
            })
        else:
            return json.dumps({"status": "mock_response"})


if __name__ == "__main__":
    # Test the service
    service = GeminiService()
    test_prompt = "Extract technical skills: Python, Java, SQL"
    response = service.call_gemini(test_prompt)
    print(f"Response: {response}")
