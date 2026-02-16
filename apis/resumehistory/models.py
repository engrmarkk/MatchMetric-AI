from django.db import models
from api_services.utils import hex_uuid


# Create your models here.
class ResumeHistory(models.Model):
    id = models.CharField(
        primary_key=True, max_length=32, default=hex_uuid, editable=False
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    resume_text = models.TextField()
    job_description = models.TextField()
    ai_analysis = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
