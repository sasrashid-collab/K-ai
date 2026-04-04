import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- ١. ڕێکخستنی بنەڕەتی و ستایلی کوردی ---
st.set_page_config(page_title="K.AI v5.0 - K.Kod", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; font-family: 'Tahoma'; } 
div.stButton > button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; }
.k-card { background-color: #f1f8e9; padding: 20px; border-right: 5px solid #2e7d32; margin: 10px 0; border-radius: 10px; } </style>""", unsafe_allow_html=True)

if not os.path.exists('K-Data'): os.makedirs('K-Data')

st.title("🤖 وەشانی زێڕینی K.AI")
st.subheader("پڕۆژەی نیشتمانیی K.Kod بۆ خزمەتی مێژووی کورد")

# --- ٢. لۆژیکی خوێندنەوەی قووڵ و بێ هەڵە ---
def deep_learn(url):
    url = url.strip().lstrip('.')
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # لادانی هەموو شتە زیادەکانی سایتەکە (ڕیکلام، مینیو، ئینگلیزی)
        for extra in soup(['script', 'style', 'nav', 'footer']): extra.decompose()
        
        # تەنها ناونیشان و پەرەگرافە کوردییەکان دەهێنین
        parts = soup.find_all(['h1', 'h2', 'h3', 'p'])
        clean_text = "\n\n".join([p.get_text().strip() for p in parts if len(p.get_text()) > 40])
        
        # فلتەرکردنی وشە بێگانەکان و هەڵەکانی گۆگڵ
        if "Something went wrong" in clean_text or len(clean_text) < 50:
            return False, "⚠️ ئەم لینکە زانیاری پاکی تێدا نییە."
            
        with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{clean_text}")
        return True, "✅ مێشکی K.AI بە زانیاری نوێ پڕ بووەوە."
    except: return False, "❌ کێشەیەک لە پەیوەندیدا هەیە."

# --- ٣. بەشی کۆنترۆڵ (Sidebar) ---
with st.sidebar:
    st.header("⚙️ بەڕێوەبردنی K.AI")
    if st.button("🗑️ پاککردنەوەی مێشک (Reset)"):
        if os.path.exists("K-Data/brain.txt"):
            os.remove("K-Data/brain.txt")
            st.success("مێشکی K.AI پاککرایەوە! ئێستا زانیاری نوێی بدەرێ.")
    
    st.divider()
    urls = st.text_area("لینکەکان (لێرە دایان بنێ):")
    if st.button("📖 دەستپێکردنی فێربوون"):
        for link in urls.split('\n'):
            if link: ok, msg = deep_learn(link); st.write(f"{msg}")

# --- ٤. بەشی گفتوگۆ و وەڵامدانەوە ---
query = st.text_input("چی دەپرسی دەربارەی مێژوو و ئەدەبی کورد؟")
if query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            knowledge = f.read()
        
        # گەڕانێکی وردتر بۆ دۆزینەوەی پەرەگرافە پەیوەندیدارەکان
        paragraphs = [p for p in knowledge.split('\n\n') if any(word in p for word in query.split())]
        
        if paragraphs:
            st.markdown("### 📜 وەڵامی تێروتەسەلی K.AI:")
            for p in paragraphs[:5]: # نیشاندانی ٥ باشترین پەرەگراف
                st.markdown(f'<div class="k-card">{p}</div>', unsafe_allow_html=True)
        else:
            st.warning("ببورە، ئەم بابەتەم هێشتا نەخوێندووەتەوە. لینکێکم بدەرێ تا فێری ببم.")
    else: st.info("مێشکی K.AI خاڵییە. تکایە لە لای چەپەوە مێژووی فێر بکە.")
