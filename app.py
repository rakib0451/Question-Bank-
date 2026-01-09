import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NCTB AI Tutor", layout="wide")

MASTER_PROMPT = """
তুমি একজন বিশেষজ্ঞ এআই টিউটর। ২০২৬ সালের শিক্ষাক্রম অনুযায়ী কাজ করো।
১. সারমর্ম: ৫ লাইন (কঠিন শব্দের পাশে বন্ধনীতে সহজ অর্থ)।
২. ১০টি সৃজনশীল কাজ: (সিরিয়ালসহ)।
৩. ১০টি শব্দার্থ ও ১০টি এমসিকিউ।
৪. উত্তর: শেষে "--- উত্তর নিচে দেওয়া হলো ---" সেকশনে থাকবে।
"""

st.title("📚 ২০২৬ স্মার্ট এআই টিউটর")

with st.sidebar:
    api_key = st.text_input("Gemini API Key দিন:", type="password")
    chapter = st.selectbox("অধ্যায় নির্বাচন করুন:", ["অধ্যায় ১", "অধ্যায় ২", "অধ্যায় ৩"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        # একদম লেটেস্ট মডেল নেম ফরমেট
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=MASTER_PROMPT)
        
        uploaded_file = st.file_uploader("বইয়ের PDF আপলোড করুন", type=["pdf"])

        if uploaded_file:
            if st.button(f"🚀 {chapter} লোড করো"):
                with st.spinner("তথ্য খোঁজা হচ্ছে..."):
                    try:
                        file_content = uploaded_file.getvalue()
                        response = model.generate_content([
                            {'mime_type': 'application/pdf', 'data': file_content},
                            f"Generate content for {chapter}"
                        ])
                        st.session_state.result = response.text
                    except Exception as e:
                        st.error(f"Error: {e}")

            if 'result' in st.session_state:
                st.markdown(st.session_state.result)
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.warning("চালু করতে সাইডবারে API Key দিন।")
