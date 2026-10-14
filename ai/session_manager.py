import streamlit as st
from config import BotConfig


class ChatSessionManager:
    def __init__(self):
        # مقداردهی اولیه حافظه در صورت عدم وجود
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def get_messages(self) -> list:
        return st.session_state.messages

    def add_user_message(self, content: str):
        st.session_state.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        st.session_state.messages.append({"role": "assistant", "content": content})

    def remove_last_message(self):
        """در صورت بروز خطا در API، آخرین پیام بی‌پاسخ کاربر را حذف می‌کند"""
        if st.session_state.messages:
            st.session_state.messages.pop()

    def clear_history(self):
        st.session_state.messages = []

    def build_api_payload(self) -> list:
        """ترکیب پرامپت سیستم با تاریخچه پیام‌ها برای ارسال به مدل"""
        return [
            {"role": "system", "content": BotConfig.SYSTEM_PROMPT}
        ] + st.session_state.messages