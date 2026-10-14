
from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError
)
from config import BotConfig


class MathTutorService:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

    def stream_response(self, api_messages: list):
        """ارسال درخواست به صورت استریم برای نمایش لحظه‌ای پاسخ"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=BotConfig.TEMPERATURE,
                stream=True
            )
            return stream

        except AuthenticationError:
            raise RuntimeError(
                "خطای احراز هویت: کلید API معتبر نیست."
            )

        except RateLimitError:
            raise RuntimeError(
                "محدودیت تعداد درخواست. لطفاً کمی صبر کنید."
            )

        except APIConnectionError:
            raise RuntimeError(
                "خطا در برقراری ارتباط با سرور."
            )

        except APIError as e:
            raise RuntimeError(
                f"خطای سرویس API: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"خطای پیش‌بینی نشده: {e}"
            )
