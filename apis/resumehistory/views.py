from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from api_services.const_response import return_response
from api_services.status_messages import StatusResponse as Res
import rest_framework.status as http_status
from db_cruds import save_resume_history, get_user_resume_histories
from pdf_extract.pypdf_extractor import PyPDFExtractor
from ai.google_genai import GeminiClient


class UploadResumeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def post(self, request) -> Response:
        # resume file
        resume = request.FILES.get("resume")
        if not resume:
            return return_response(
                Res.FAILED,
                http_status.HTTP_400_BAD_REQUEST,
                "Resume file is required",
            )
        pdf_extractor = PyPDFExtractor(resume)
        text = pdf_extractor.extract_text()
        return return_response(
            Res.SUCCESS, http_status.HTTP_200_OK, "Resume uploaded", text
        )


# tailor resume view (Use the Websocket instead of this)
class TailorResumeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def post(self, request) -> Response:
        # resume file
        resume = request.FILES.get("resume")
        job_description = request.data.get("job_description")
        if not resume:
            return return_response(
                Res.FAILED,
                http_status.HTTP_400_BAD_REQUEST,
                "Resume file is required",
            )

        if not job_description:
            return return_response(
                Res.FAILED,
                http_status.HTTP_400_BAD_REQUEST,
                "Job description is required",
            )

        pdf_extractor = PyPDFExtractor(resume)
        resume_text = pdf_extractor.extract_text()

        # Call Gemini API to tailor the resume
        gemini = GeminiClient()
        ai_analysis = gemini.analyze_resume(resume_text, job_description)
        analysis_data = ai_analysis.model_dump()

        save_resume_history(request.user, resume_text, job_description, analysis_data)
        return return_response(
            Res.SUCCESS,
            http_status.HTTP_200_OK,
            "Resume tailored",
            {"ai_analysis": analysis_data},
        )


# get histories
class GetHistoriesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        per_page = int(request.query_params.get("per_page", 10))
        histories = get_user_resume_histories(request.user, page, per_page)
        return return_response(
            Res.SUCCESS,
            http_status.HTTP_200_OK,
            "Histories retrieved",
            histories,
        )
