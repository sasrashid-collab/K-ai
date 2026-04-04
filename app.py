import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="K.AI Pro - K.Kod", page_icon="📜", layout="wide")

# ستایلی کوردی بۆ نووسینەکان
st.markdown("""
    <style>
    .ststr { direction: rtl; text-align: right; }
    p, h1, h2, h3, div { direction: rtl; text-align: right; font-family: 'Tahoma'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 پڕۆژەی K.AI (وەشانی پێشکەوتوو)")
st.subheader("سەرپەرشتیار: K.Kod")

# دروستکردنی فۆڵدەری مێشک ئەگەر نەبێت
if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

# --- بەشی فێربوونی قووڵ (Sidebar) ---
st.sidebar.header("📚 فێربوونی بێ سنوور")
url_input = st.sidebar.text_input("لینکە کوردییەکە لێرە دابنێ:")

if st.sidebar.button("هەموو لاپەڕەکە بخوێنەوە"):
    if url_input:
        with st.spinner('K.AI خەریکی خوێندنەوەی تەواوی دەقەکەیە...'):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # لێرەدا هەموو پەرەگرافەکان کۆدەکەینەوە بەبێ سنوور
                all_paragraphs = soup.find_all('p')
                full_text = "\n".join([p.get_text() for p in all_paragraphs])
                
                if len(full_text) > 100:
                    with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n\n--- سەرچاوەی نوێ: {url_input} ---\n")
                        f.write(full_text)
                    st.sidebar.success(f"✅ {len(full_text)} پیتی نوێ خرایە مێشکی K.AI")
                else:
                    st.sidebar.warning("دەقێکی ئەوتۆ لەم لینکەدا نەدۆزرایەوە.")
            except Exception as e:
                st.sidebar.error(f"کێشە: {e}")

# --- بەشی چاتی زیرەک و وەڵامی تێروتەسەل ---
st.divider()
st.markdown("### 💬 پرسیار لە K.AI بکە")
user_query = st.text_input("چی دەپرسی دەربارەی مێژوو یان زمانی کورد؟")

if user_query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            brain_content = f.read()
        
        # لۆژیکی گەڕانی قووڵ
        keywords = user_query.split()
        matches = [line for line in brain_content.split('\n') if any(word in line for word in keywords)]
        
        if matches:
            st.markdown("#### 📝 وەڵامی K.AI:")
            # لێرەدا وەڵامێکی درێژتر (تا ١٥٠٠ پیت) نیشان دەدەین
            combined_response = "\n".join(matches[:15]) # ١٥ دێڕی یەکەم کە پەیوەندی هەیە
            st.write(combined_response if len(combined_response) > 10 else "ببورە، زانیارییەکانم تەنها دەربارەی گشتیاتن، لینکی زیاترم بدەرێ بۆ وەڵامی وردتر.")
        else:
            st.warning("ئەم بابەتەم هێشتا نەخوێندووەتەوە. تکایە لینکێکم بدەرێ تا فێری ببم.")
    else:
        st.info("مێشکی K.AI هێشتا خاڵییە، تکایە لە لای چەپەوە لینکێکی بدەرێ.")

st.sidebar.write("---")
st.sidebar.write("ئامۆژگاری: چەند لینک زیاتر بێت، وەڵامەکان تێروتەسەلتر دەبن.")
