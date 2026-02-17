from apis.users.models import User
from apis.resumehistory.models import ResumeHistory
from django.core.paginator import Paginator


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
        ai_analysis=ai_analysis,
    )


def get_user_resume_histories(user, page, per_page):

    queryset = ResumeHistory.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(queryset, per_page)

    try:
        page_obj = paginator.page(page)
    except:
        return {
            "page": page,
            "per_page": per_page,
            "total_items": paginator.count,
            "total_pages": paginator.num_pages,
            "data": [],
        }

    return {
        "page": page,
        "per_page": per_page,
        "total_items": paginator.count,
        "total_pages": paginator.num_pages,
        "data": [
            {
                "id": history.id,
                "resume_text": history.resume_text,
                "job_description": history.job_description,
                "ai_analysis": history.ai_analysis,
                "created_at": history.created_at,
            }
            for history in page_obj.object_list
        ],
    }
