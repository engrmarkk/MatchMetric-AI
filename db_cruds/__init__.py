from apis.users.models import User
from apis.resumehistory.models import ResumeHistory


# create user
def create_user(first_name, last_name, email, password):
    user = User.objects.create_user(
        first_name=first_name, last_name=last_name, email=email, password=password
    )
    return user


# email exists
def email_exists(email):
    return User.objects.filter(email=email).exists()


def save_resume_history(user, resume_text, job_description, ai_analysis):
    return ResumeHistory.objects.create(
        user=user,
        resume_text=resume_text[:1000],
        job_description=job_description[:1000],
        ai_analysis=ai_analysis
    )
