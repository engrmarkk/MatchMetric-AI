# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from ai.google_genai import GeminiClient
# from .models import ResumeHistory
#
#
# class ResumeConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         headers = dict(self.scope.get('headers', []))
#         print(f"Headers: {headers}")
#
#         # Check if cookie header is present
#         cookie_header = headers.get(b'cookie', b'').decode()
#         print(f"Cookie header: {cookie_header}")
#         user = self.scope["user"]
#         print(f"WebSocket connecting: User is {user}")
#         if not user.is_authenticated:
#             await self.close()
#         await self.accept()
#
#     async def receive(self, text_data=None, **kwargs):
#         if not text_data:
#             return
#
#         data = json.loads(text_data)
#         resume_text = data.get("resume_text")
#         job_desc = data.get("job_description")
#
#         gemini = GeminiClient()
#
#         try:
#             analysis_result = await sync_to_async(gemini.analyze_resume)(
#                 resume_text, job_desc
#             )
#
#             analysis_data = analysis_result.model_dump()
#
#             await self.save_history(resume_text, job_desc, analysis_data)
#
#             await self.send(
#                 text_data=json.dumps(
#                     {"status": "success", "ai_analysis": analysis_data}
#                 )
#             )
#
#         except Exception as e:
#             await self.send(
#                 text_data=json.dumps({"status": "failed", "message": str(e)})
#             )
#
#     @sync_to_async
#     def save_history(self, resume, jd, analysis):
#         ResumeHistory.objects.create(
#             user=self.scope["user"],
#             resume_text=resume,
#             job_description=jd,
#             ai_analysis=analysis,
#         )


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from ai.google_genai import GeminiClient
from .models import ResumeHistory


class ResumeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get session_id from query string
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        session_id = query_params.get('session_id', [None])[0]

        print(f"🔍 WebSocket connection attempt with session_id: {session_id}")

        if not session_id:
            print("❌ No session_id provided in URL")
            await self.close(code=4401)
            return

        # Authenticate user from session
        user = await self.get_user_from_session(session_id)

        if user and not user.is_anonymous:
            print(f"✅ WebSocket authenticated: {user.email} (ID: {user.id})")
            self.user = user

            # Set user in scope for other methods
            self.scope["user"] = user

            await self.accept()
            print("✅ WebSocket connection accepted")

            # Send welcome message (optional)
            await self.send(text_data=json.dumps({
                'type': 'connected',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message': 'WebSocket connection established'
            }))
        else:
            print(f"❌ WebSocket authentication failed for session: {session_id}")
            await self.close(code=4401)

    @database_sync_to_async
    def get_user_from_session(self, session_key):
        """
        Retrieve user from session key
        """
        try:
            # Get the session object
            session = Session.objects.get(session_key=session_key)

            # Check if session has expired
            from django.utils import timezone
            if session.expire_date < timezone.now():
                print(f"⚠️ Session {session_key} has expired")
                return None

            # Decode session data
            session_data = session.get_decoded()

            # Get user ID from session
            user_id = session_data.get('_auth_user_id')
            print(f"User ID from session: {user_id}")

            if user_id:
                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                    print(f"✅ Found user: {user.email} (ID: {user_id})")
                    return user
                except User.DoesNotExist:
                    print(f"❌ User with ID {user_id} not found")
                    return None
            else:
                print(f"❌ No _auth_user_id in session {session_key}")
                return None

        except Session.DoesNotExist:
            print(f"❌ Session with key {session_key} does not exist")
            return None
        except Exception as e:
            print(f"❌ Error retrieving user from session: {str(e)}")
            return None

    async def receive(self, text_data=None, **kwargs):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            resume_text = data.get("resume_text")
            job_desc = data.get("job_description")

            if not resume_text or not job_desc:
                await self.send(
                    text_data=json.dumps({
                        "status": "error",
                        "message": "Missing resume_text or job_description"
                    })
                )
                return

            gemini = GeminiClient()

            try:
                # Run Gemini analysis in thread pool (since it's blocking)
                analysis_result = await database_sync_to_async(gemini.analyze_resume)(
                    resume_text, job_desc
                )

                analysis_data = analysis_result.model_dump()

                # Save history
                await self.save_history(resume_text, job_desc, analysis_data)

                print(f"✅ Gemini analysis completed for user: {self.user.email}")
                print(f"✅ Gemini analysis data: {analysis_data}")

                await self.send(
                    text_data=json.dumps({
                        "status": "success",
                        "ai_analysis": analysis_data
                    })
                )

            except Exception as e:
                print(f"❌ Gemini analysis error: {str(e)}")
                await self.send(
                    text_data=json.dumps({
                        "status": "failed",
                        "message": str(e)
                    })
                )

        except json.JSONDecodeError as e:
            await self.send(
                text_data=json.dumps({
                    "status": "error",
                    "message": f"Invalid JSON: {str(e)}"
                })
            )
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            await self.send(
                text_data=json.dumps({
                    "status": "error",
                    "message": "Internal server error"
                })
            )

    @database_sync_to_async
    def save_history(self, resume, jd, analysis):
        try:
            # Use self.user instead of self.scope["user"]
            ResumeHistory.objects.create(
                user=self.user,
                resume_text=resume,
                job_description=jd,
                ai_analysis=analysis
            )
            print(f"✅ Resume history saved for user: {self.user.email}")
        except Exception as e:
            print(f"❌ Error saving resume history: {str(e)}")
            raise

    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user and not self.user.is_anonymous:
            print(f"🔌 WebSocket disconnected: {self.user.email} (Code: {close_code})")
        else:
            print(f"🔌 WebSocket disconnected (Code: {close_code})")
