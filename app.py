import streamlit as st
import requests
import os

# --- ١. ڕێکخستنی ناسنامەی K.AI Coder ---
st.set_page_config(page_title="K.AI Coder - K.Kod", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; } 
code { direction: ltr; text-align: left; background-color: #1e1e1e; color: #d4d4d4; padding: 10px; display: block; border-radius: 5px; }
</style>""", unsafe_allow_html=True)

st.title("🤖 K.AI Ultra Coder")
st.subheader("زیرەکی دەستکردی گشتگیر و کۆدنوس - پەرەپێدراوی K.Kod")

# --- ٢. مەکینەی وەڵامدانەوە و کۆدنووسین (بەکارهێنانی API بێبەرامبەر) ---
def ask_kai(prompt):
    # لێرەدا K.AI پەیوەندی بە مۆدێلێکی بەهێزەوە دەکات بۆ وەڵامدانەوەی گشتگیر
    headers = {"Authorization": "Bearer YOUR_FREE_API_KEY"} # لێرە دەتوانین API کلیلی بێبەرامبەر دابنێین
    api_url = "https://huggingface.co"
    
    payload = {"inputs": f"You are K.AI created by K.Kod. Answer in Kurdish and provide code if asked: {prompt}"}
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        return response.json()[0]['generated_text']
    except:
        return "ببورە، لە ئێستادا ناتوانم وەڵامت بدەمەوە. تکایە پەیوەندی ئینتەرنێتەکەت بپشکنە."

# --- ٣. ڕوونمای بەکارهێنەر ---
st.info("جەنابت دەتوانیت لێرە داوای نووسینی کۆد، شیکاری کێشە، یان هەر پرسیارێکی تر بکەیت.")

user_input = st.text_area("چی بۆ K.AI بنووسم؟", placeholder="بۆ نموونە: کۆدێکی پایتۆنم بۆ بنووسە بۆ لێکدانی دوو ژمارە...")

if st.button("ناردن بۆ K.AI"):
    if user_input:
        with st.spinner("K.AI خەریکی بیرکردنەوە و کۆدنووسینە..."):
            answer = ask_kai(user_input)
            st.markdown("### 📝 وەڵامی K.AI:")
            st.write(answer)
    else:
        st.warning("تکایە سەرەتا شتێک بنووسە.")

# --- ٤. بەشی فێربوونی بەردەوام لە GitHub ---
st.sidebar.header("🛠️ گەشەپێدانی K.Kod")
st.sidebar.write("ئەم وەشانە توانای نووسینی کۆد و لۆژیکی بیرکاری هەیە.")
