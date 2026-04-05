import streamlit as st
import requests
import os

# --- ١. ناسنامەی K.AI ---
st.set_page_config(page_title="K.AI Turbo - K.Kod", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; } </style>""", unsafe_allow_html=True)

st.title("🤖 K.AI Turbo: وەشانی بێ وەستان")
st.subheader("پەرەپێدراوی K.Kod - خێراترین وەشانی کورد")

# --- ٢. مەکینەی وەڵامدانەوەی زیرەک (بەکارهێنانی مۆدێلی جێگرەوە) ---
def ask_kai_turbo(prompt):
    # ئەم مۆدێلە لەسەر سێرڤەرێکی جیاوازە کە کەمتر دەوەستێت
    API_URL = "https://huggingface.co"
    # لێرەدا دەتوانیت کلیلەکەت دابنێیت بۆ ئەوەی هەرگیز نەوەستێت
    headers = {"Authorization": "Bearer hf_xxx"} 
    
    payload = {
        "inputs": f"You are K.AI by K.Kod. Always reply in Kurdish. User: {prompt}",
        "parameters": {"max_new_tokens": 700, "return_full_text": False}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return "⚠️ سێرڤەرەکە خەریکی خۆگەرمکردنەوەیە، تکایە یەک چرکەی تر دووبارەی بکەرەوە."
    except:
        return "❌ کێشەی پەیوەندی هەیە، تکایە ئینتەرنێتەکەت بپشکنە."

# --- ٣. بەشی گفتوگۆ ---
user_query = st.chat_input("لێرە هەرچییەکت دەوێت لە K.AI بپرسە...")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("K.AI خەریکی بیرکردنەوەیە..."):
            answer = ask_kai_turbo(user_query)
            st.write(answer)

st.sidebar.warning("تێبینی: ئەگەر وەڵامی نەدایەوە، تەنها یەکجار لاپەڕەکە نوێ بکەرەوە (Refresh).")
