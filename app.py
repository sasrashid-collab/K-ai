import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time

# --- ١. ڕێکخستنی بنەڕەتی لاپەڕە ---
st.set_page_config(page_title="K.AI Pro - K.Kod", layout="wide", page_icon="🤖")

# دروستکردنی فۆڵدەری مێشک ئەگەر بوونی نەبێت
if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

# ستایلی کوردی بۆ نیشاندانی دەقەکان (ڕاست بۆ چەپ)
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    p, h1, h2, h3, div, span, label { direction: rtl; text-align: right !important; font-family: 'Tahoma'; }
    .stTextInput, .stTextArea { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 پڕۆژەی زیرەکی دەستکردی K.AI")
st.subheader("خاوەن و سەرپەرشتیار: K.Kod")
st.info("ئەم سیستمە لەسەر بنەمای زانیارییە مێژووییەکانی کورد پەرە بەخۆی دەدات.")

# --- ٢. لۆژیکی خوێندنەوە و پاککردنەوەی لینکەکان ---
def learn_from_url(url):
    url = url.strip()
    # سڕینەوەی نیشانە زیادەکان لە سەرەتای لینک
    if url.startswith("."): url = url[1:]
    if not url.startswith(("http://", "https://")): url = "https://" + url
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # کاتی چاوەڕوانی بۆ ٦٠ چرکە زیاد کراوە بۆ ئەوەی وێبسایتە خاوەکان نەیبڕن
        response = requests.get(url, headers=headers, timeout=60)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # کۆکردنەوەی دەق لە پەرەگراف و ناونیشانەکان
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'span'])
        content = " ".join([t.get_text() for t in tags if len(t.get_text()) > 20])
        
        if len(content.strip()) > 30:
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n--- سەرچاوە: {url} ---\n{content}")
            return True, f"✅ سەرکەوتوو بوو: {len(content)} پیت وەرگیرا."
        else:
            return False, "⚠️ دەقێکی ئەوتۆ لەم لاپەڕەیەدا نەدۆزرایەوە."
    except Exception as e:
        return False, f"❌ هەڵە لە پەیوەندی: {str(e)}"

# --- ٣. ڕوونمای بەکارهێنەر (Sidebar) ---
st.sidebar.header("📚 فێربوونی K.AI")

# بژاردەی یەکەم: خوێندنەوەی لینکەکان
st.sidebar.markdown("### ١. لە ڕێگەی لینکەوە")
urls_area = st.sidebar.text_area("لینکەکان لێرە دابنێ (هەر لینکێک لە دێڕێک):", height=150)
if st.sidebar.button("دەستپێکردنی فێربوون"):
    if urls_area:
        links = urls_area.split('\n')
        for link in links:
            if link.strip():
                with st.spinner(f'خەریکی خوێندنەوەی: {link}'):
                    ok, msg = learn_from_url(link)
                    if ok: st.sidebar.success(msg)
                    else: st.sidebar.error(f"{link}: {msg}")
    else:
        st.sidebar.warning("تکایە سەرەتا لینکێک بنووسە.")

st.sidebar.divider()

# بژاردەی دووەم: پەیستی ڕاستەوخۆی دەق (بۆ جەنابت ئاسانترە)
st.sidebar.markdown("### ٢. فێربوونی ڕاستەوخۆ")
manual_data = st.sidebar.text_area("دەقێکی مێژوویی لێرە کۆپی-پەیست بکە:")
if st.sidebar.button("زیادکردن بۆ مێشک"):
    if manual_data:
        with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n--- دەقی دەستی ---\n{manual_data}")
        st.sidebar.success("✅ دەقەکە بە سەرکەوتوویی خرایە مێشکی K.AI")

# --- ٤. بەشی چات و پرسیارکردن ---
st.divider()
st.markdown("### 💬 گفتوگۆ لەگەڵ K.AI")
query = st.text_input("پرسیارەکەت لێرە بنووسە (بۆ نموونە: مێژووی کورد چییە؟):")

if query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            full_knowledge = f.read()
        
        # گەڕان بۆ دۆزینەوەی وەڵامێکی گونجاو
        if query.strip() in full_knowledge or any(word in full_knowledge for word in query.split()):
            st.markdown("#### 📖 وەڵامی K.AI بەپێی ئەو زانیارییانەی لایەتی:")
            # نیشاندانی بەشێک لە مێشکەکە کە پەیوەندی بە پرسیارەکەوە هەیە
            lines = [l for l in full_knowledge.split('\n') if len(l) > 40]
            response_text = "\n\n".join(lines[:10]) # نیشاندانی ١٠ پەرەگرافی یەکەم وەک وەڵامی تێروتەسەل
            st.write(response_text)
        else:
            st.warning("ببورە جەنابت، هێشتا زانیاری تەواوم لەسەر ئەم بابەتە نییە. تکایە لینک یان دەقێکی ترم بدەرێ تا فێری ببم.")
    else:
        st.info("سڵاو! من K.AIـم. هێشتا هیچ زانیارییەک لە مێشکمدا نییە، تکایە لە لای چەپەوە فێرم بکە.")

st.sidebar.write("---")
st.sidebar.write(f"وەشانی جێگیر: 3.5 | خاوەن: K.Kod")
