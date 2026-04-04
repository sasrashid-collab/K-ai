import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import re

# --- ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="K.AI Pro - K.Kod", layout="wide")

if not os.path.exists('K-Data'): os.makedirs('K-Data')

# ستایلی ڕاست-بۆ-چەپ و جوانکاری
st.markdown("""<style> .stApp { direction: rtl; text-align: right; } p, h1, h2, h3, div { font-family: 'Tahoma'; line-height: 1.8; } </style>""", unsafe_allow_html=True)

st.title("🤖 وەشانی پڕۆی K.AI")
st.subheader("سەرپەرشتیار: K.Kod")

# --- فلتەرکردنی دەقەکان (لادانی هەڵەکانی گۆگڵ) ---
def clean_kurdish_text(text):
    # لادانی ڕستە ئینگلیزییەکانی گۆگڵ و هەڵەکان
    bad_phrases = ["Something went wrong", "URL isn't available", "Google Share", "Sign in", "Terms of Service"]
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not any(phrase in line for phrase in bad_phrases) and len(line.strip()) > 30:
            cleaned_lines.append(line.strip())
    return "\n\n".join(cleaned_lines)

# --- لۆژیکی فێربوون ---
def learn_from_url(url):
    url = url.strip().lstrip('.')
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        raw_text = " ".join([t.get_text() for t in soup.find_all(['p', 'h1', 'h2', 'span'])])
        final_text = clean_kurdish_text(raw_text)
        
        if len(final_text) > 50:
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{final_text}")
            return True, "✅ مێشک نوێکرایەوە."
        return False, "⚠️ دەقێکی کوردی پاک نەدۆزرایەوە."
    except: return False, "❌ کێشەی پەیوەندی."

# --- ڕوونمای بەکارهێنەر (Sidebar) ---
with st.sidebar:
    st.header("📚 ژووری فێربوون")
    urls = st.text_area("لینکەکان (هەر دانەیەک لە دێڕێک):")
    if st.button("فێری بکە"):
        for link in urls.split('\n'):
            if link: 
                ok, msg = learn_from_url(link)
                st.write(f"{link[:20]}... : {msg}")

# --- بەشی چاتی زیرەک (ئەنجام) ---
st.divider()
query = st.text_input("پرسیارەکەت بنووسە (بۆ نموونە: عەلائەدین سەجادی کێیە؟)")

if query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            brain = f.read()
        
        # گەڕانی زیرەک بەدوای وەڵامدا
        words = query.split()
        paragraphs = brain.split('\n\n')
        results = [p for p in paragraphs if any(w in p for w in words)]
        
        if results:
            st.markdown("### 📖 ئەنجامی لێکۆڵینەوەی K.AI:")
            for res in results[:3]: # تەنها ٣ باشترین وەڵام نیشان دەدەین
                st.info(res)
        else:
            st.warning("ببورە، هێشتا زانیاری تەواوم لەسەر ئەمە نییە.")
    else:
        st.write("سڵاو! من K.AIـم. تکایە سەرەتا مێشکم پڕ بکە.")
