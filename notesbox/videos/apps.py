from django.apps import AppConfig
from django.conf import settings  
import google.generativeai as genai
class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'
    gemini_model = None
    def ready(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            VideosConfig.gemini_model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",  # Your model
                generation_config={  # Your config
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                },
            )
        except Exception as e:
            print(f"Error initializing Gemini: {e}")