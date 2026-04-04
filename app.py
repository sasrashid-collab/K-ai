import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="K.AI Pro - K.Kod", layout="wide")

# دروستکردنی فۆڵدەری مێشک
if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

st.title("🤖 پڕۆژەی K.AI - وەشانی چارەسەرکەر")
st.subheader("سەرپەرشتیار: K.Kod")

# --- بەشی فێربوونی زیرەک (Sidebar) ---
st.sidebar.header("📚 فێربوونی مێشکی K.AI")

# ١. فێربوون لە ڕێگەی لینک (بە چاکسازی هەڵە)
url_input = st.sidebar.text_input("لینک لێرە دابنێ (نموونە: https://google.com):")

if st.sidebar.button("فێربوون لە لینک"):
    if url_input:
        clean_url = url_input.strip() # سڕینەوەی بۆشاییە زیادەکان
        if not clean_url.startswith(("http://", "https://")):
            clean_url = "https://" + clean_url
            
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(clean_url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            text = " ".join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2'])])
            
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{text}")
            st.sidebar.success("✅ لینکەکە بە سەرکەوتوویی خوێندرایەوە!")
        except Exception as e:
            st.sidebar.error(f"❌ کێشە لە لینکەکەدا هەیە: {str(e)}")

st.sidebar.divider()

# ٢. فێربوونی ڕاستەوخۆ (بەبێ لینک) - ئەمە بۆ جەنابت ئاسانترە
st.sidebar.header("✍️ فێربوونی ڕاستەوخۆ")
manual_text = st.sidebar.text_area("دەقێکی مێژوویی لێرە پەیست بکە:")
if st.sidebar.button("زیادکردن بۆ مێشک"):
    if manual_text:
        with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{manual_text}")
        st.sidebar.success("✅ دەقەکە زیادکرا!")

# --- بەشی چات و پرسیار ---
user_query = st.text_input("چی دەپرسی لە K.AI؟")
if user_query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            knowledge = f.read()
        
        if user_query.lower() in knowledge.lower() or "کورد" in user_query:
            st.write("📖 ئەوەی فێری بووم:")
            # گەڕان بۆ دۆزینەوەی ئەو بەشەی پرسیارەکەی تێدایە
            lines = knowledge.split('\n')
            relevant_lines = [line for line in lines if any(word in line for word in user_query.split())]
            st.write("\n".join(relevant_lines[:10]) if relevant_lines else knowledge[:1000])
        else:
            st.warning("ببورە، هێشتا زانیاریم لەسەر ئەمە نییە.")
    else:
        st.info("تکایە سەرەتا مێشکی K.AI پڕ بکە لە زانیاری.")
