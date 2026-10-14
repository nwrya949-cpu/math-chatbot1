import streamlit as st

# ایمپورت کردن کلاس‌ها از فایل‌های دیگر پروژه
from config import BotConfig
from session_manager import ChatSessionManager
from bot_service import MathTutorService

# ۱. تنظیمات اولیه صفحه (باید اولین دستور Streamlit باشد)
st.set_page_config(
    page_title=BotConfig.PAGE_TITLE,
    page_icon=BotConfig.PAGE_ICON
)

# ۲. ساخت و کش کردن سرویس هوش مصنوعی (فقط یک‌بار ساخته می‌شود)
@st.cache_resource
def get_bot_service() -> MathTutorService:
    return MathTutorService(
        api_key=st.secrets["API_KEY"],
        base_url=st.secrets["BASE_URL"],
        model=st.secrets["MODEL"]
    )

# ۳. مقداردهی مدیر جلسه و سرویس بات
session = ChatSessionManager()
bot_service = get_bot_service()

# ۴. نوار کناری (Sidebar) برای پاک کردن تاریخچه
with st.sidebar:
    st.header("تنظیمات گفتگو")
    if st.button("پاک کردن تاریخچه چت 🗑️", use_container_width=True):
        session.clear_history()
        st.rerun()

# ۵. عنوان صفحه
st.title(f"{BotConfig.PAGE_ICON} {BotConfig.PAGE_TITLE}")
st.caption("دستیار هوشمند شما برای حل مسائل و مفاهیم ریاضی")

# ۶. نمایش تاریخچه پیام‌های قبلی
for message in session.get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ۷. دریافت ورودی جدید از کاربر
prompt = st.chat_input("سوال ریاضی خود را بپرسید...")

if prompt:
    # نمایش و ذخیره پیام کاربر
    session.add_user_message(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # دریافت و نمایش پاسخ دستیار به صورت استریم
    with st.chat_message("assistant"):
        try:
            api_payload = session.build_api_payload()
            stream = bot_service.stream_response(api_payload)
            
            # نمایش زنده پاسخ در رابط کاربری و دریافت متن کامل در پایان
            full_answer = st.write_stream(stream)
            
            # ذخیره پاسخ نهایی در تاریخچه
            session.add_assistant_message(full_answer)

        except RuntimeError as err:
            st.error(str(err))
            # حذف آخرین پیام کاربر تا تاریخچه چت خراب نشود
            session.remove_last_message()