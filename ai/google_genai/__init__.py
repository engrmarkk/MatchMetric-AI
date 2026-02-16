from google import genai
from google.genai import types
from ai import AnalysisResult


class GeminiClient:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-flash-latest"

    def generate_content(self, contents: str):
        return self.client.models.generate_content(model=self.model, contents=contents)

    def list_models(self):
        all_models = []
        for m in self.client.models.list():
            if "generateContent" in m.supported_actions:
                all_models.append(m.name)
        return all_models

    def analyze_resume(self, resume_text, job_description):
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"Resume: {resume_text}\nJD: {job_description}",
            config=types.GenerateContentConfig(
                system_instruction="You are a professional Resume Strategist. Compare the Resume with the Job Description.",
                response_mime_type="application/json",
                response_schema=AnalysisResult,
            ),
        )

        return response.parsed
