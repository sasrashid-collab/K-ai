import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import googlesearch # پێویستە لە requirements.txt زیاد بکرێت

# --- ١. ڕێکخستنی ناسنامەی گشتگیری K.AI ---
st.set_page_config(page_title="K.AI Ultra - K.Kod", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; } </style>""", unsafe_allow_html=True)

if not os.path.exists('K-Data'): os.makedirs('K-Data')

st.title("🤖 K.AI Ultra: زیرەکی دەستکردی گشتگیر")
st.subheader("پەرەپێدراوی دامەزراوەی K.Kod")

# --- ٢. مەکینەی گەڕانی ئۆتۆنۆم (بۆ ئەوەی خۆی زانیاری بدۆزێتەوە) ---
def autonomous_learn(topic):
    st.write(f"🔍 K.AI خەریکی گەڕانە بەدوای زانیاری دەربارەی: {topic}...")
    try:
        # گەڕان لە گووگڵ بۆ دۆزینەوەی ٥ باشترین سەرچاوە
        from googlesearch import search
        links = list(search(topic + " کوردی", num_results=5))
        
        for link in links:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(link, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            text = " ".join([p.get_text() for p in soup.find_all('p') if len(p.get_text()) > 50])
            
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{text}")
        return True
    except: return False

# --- ٣. ڕوونمای بەکارهێنەر ---
with st.sidebar:
    st.header("🧠 گەشەپێدانی ئۆتۆماتیکی")
    topic_to_learn = st.text_input("بابەتێک بنووسە بۆ ئەوەی K.AI خۆی فێری بێت:")
    if st.button("فەرمانی فێربوون بدە"):
        if topic_to_learn:
            if autonomous_learn(topic_to_learn):
                st.success(f"K.AI ئێستا دەربارەی {topic_to_learn} زۆر زیرەکتر بوو!")
            else: st.error("کێشەیەک لە گەڕاندا هەبوو.")

# --- ٤. گفتوگۆی گشتگیر ---
query = st.text_input("لێرە هەرچییەکت دەوێت لە K.AI بپرسە:")
if query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            brain = f.read()
        
        # دۆزینەوەی وەڵام لە مێشکە گشتگیرەکەدا
        results = [p for p in brain.split('\n') if any(w in p for w in query.split())]
        if results:
            st.info("\n".join(results[:10]))
        else:
            st.warning("ئەمە لە مێشکمدا نییە. فەرمانم پێ بدە لە لای چەپەوە بچمە ناو ئینتەرنێت و فێری ببم!")

