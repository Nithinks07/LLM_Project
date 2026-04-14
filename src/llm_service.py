# Google Gemini API integration
import json
import os
from typing import Dict, Any
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

print("API KEY:", os.getenv("GEMINI_API_KEY"))

class GeminiService:
    """Interface for Google Gemini API"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.init_client()
    
    def init_client(self):
        """Initialize Gemini client"""
        if not self.api_key or self.api_key == "AIzaSyBZw3oFq1WlJsSUe0SUHEQUDIQRNn6fHM4":
            print("⚠️  WARNING: GEMINI_API_KEY not set. Set it in .env file or environment variables.")
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
    
    def call_gemini(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Call Gemini API with a prompt
        
        Args:
            prompt: The prompt text
            temperature: Temperature for response (0-1)
            
        Returns:
            API response text
        """
        if self.client is None:
            return self._get_mock_response(prompt)
        
        try:
            response = self.client.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 1024
                }
            )
            return response.text
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return self._get_mock_response(prompt)
    
    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\n?(.*?)\n?```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except:
                    pass
            
            # Try to find JSON object
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
        Useful for testing without API key
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
    
    # Test prompt
    test_prompt = "Extract technical skills: Python, Java, SQL"
    response = service.call_gemini(test_prompt)
    print(f"Response: {response}")
