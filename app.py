import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time

# --- ١. ناسنامە و ستایلی شاهانەی K.AI ---
st.set_page_config(page_title="K.AI Pro - K.Kod", layout="wide", page_icon="🤖")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f4f7f6; }
    p, h1, h2, h3, div, span { direction: rtl; text-align: right !important; font-family: 'Tahoma'; color: #2c3e50; }
    .stChatInput { direction: rtl; text-align: right; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin: 5px; }
    </style>
    """, unsafe_allow_html=True)

if not os.path.exists('K-Data'): os.makedirs('K-Data')

st.title("🤖 پڕۆژەی زیرەکی دەستکردی K.AI")
st.subheader("سەرپەرشتیار و خاوەن: K.Kod")

# --- ٢. مەکینەی فێربوونی قووڵ و بێ سنوور ---
def learn_from_url(url):
    url = url.strip().lstrip('.')
    if not url.startswith(("http://", "https://")): url = "https://" + url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'span'])
        content = " ".join([t.get_text() for t in tags if len(t.get_text()) > 30])
        if len(content.strip()) > 50:
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n--- سەرچاوە: {url} ---\n{content}")
            return True, f"✅ سەرکەوتوو بوو: {len(content)} پیت وەرگیرا."
        return False, "⚠️ دەقێکی پاک نەدۆزرایەوە."
    except Exception as e: return False, f"❌ هەڵەی پەیوەندی: {str(e)}"

# --- ٣. ڕوونمای فێربوون (Sidebar) ---
with st.sidebar:
    st.header("📚 مێشکی K.AI")
    urls_input = st.text_area("لینکەکان لێرە پەیست بکە (هەر دانەیەک لە دێڕێک):", height=200)
    if st.button("فەرمانی فێربوون"):
        if urls_input:
            for link in urls_input.split('\n'):
                if link.strip():
                    with st.spinner(f'خەریکی خوێندنەوەی: {link}'):
                        ok, msg = learn_from_url(link)
                        if ok: st.success(msg)
                        else: st.error(msg)
    st.divider()
    st.write("وەشانی ٧٥ دێڕی - بێ سەرما")

# --- ٤. گفتوگۆی ڕاستەوخۆ و وەڵامدانەوە ---
query = st.chat_input("لێرە هەرچییەکت دەوێت لە K.AI بپرسە...")

if query:
    with st.chat_message("user"): st.write(query)
    with st.chat_message("assistant"):
        if os.path.exists("K-Data/brain.txt"):
            with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
                brain_data = f.read()
            if any(word in brain_data for word in query.split()):
                relevant_parts = [line for line in brain_data.split('\n') if any(word in line for word in query.split())]
                st.write("\n\n".join(relevant_parts[:10]))
            else:
                st.warning("ببورە جەنابت، هێشتا مێشکم ئەمەی تێدا نییە. لینکێکم بدەرێ تا فێری ببم.")
        else: st.info("سڵاو! من K.AIـم. تکایە لە لای چەپەوە فێرم بکە.")

# --- کۆتایی ٧٥ دێڕی ڕەسەن ---
