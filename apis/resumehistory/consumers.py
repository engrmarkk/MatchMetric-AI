import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from ai.google_genai import GeminiClient
from .models import ResumeHistory


class ResumeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        print(f"WebSocket connecting: User is {user}")
        if not user.is_authenticated:
            await self.close()
        await self.accept()

    async def receive(self, text_data=None, **kwargs):
        if not text_data:
            return

        data = json.loads(text_data)
        resume_text = data.get("resume_text")
        job_desc = data.get("job_description")

        gemini = GeminiClient()

        try:
            analysis_result = await sync_to_async(gemini.analyze_resume)(
                resume_text, job_desc
            )

            analysis_data = analysis_result.model_dump()

            await self.save_history(resume_text, job_desc, analysis_data)

            await self.send(
                text_data=json.dumps(
                    {"status": "success", "ai_analysis": analysis_data}
                )
            )

        except Exception as e:
            await self.send(
                text_data=json.dumps({"status": "failed", "message": str(e)})
            )

    @sync_to_async
    def save_history(self, resume, jd, analysis):
        ResumeHistory.objects.create(
            user=self.scope["user"],
            resume_text=resume,
            job_description=jd,
            ai_analysis=analysis,
        )
