import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time

# --- ١. ڕێکخستنی ناسنامە و دیزاینی شاهانەی K.AI ---
st.set_page_config(page_title="K.AI Mega Pro - K.Kod", layout="wide", page_icon="🤖")

# ستایلی پێشکەوتوو بۆ ئەوەی سیستمەکە لە هەموو لایەکەوە کوردی بێت و "سەرمای نەبێت"
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="st-"] {
        direction: rtl;
        text-align: right;
        font-family: 'Noto Sans Arabic', Tahoma, sans-serif;
    }
    .stApp { background-color: #f8f9fa; }
    .main-card {
        background-color: white;
        padding: 30 inline-block;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-right: 8px solid #1a73e8;
        margin-bottom: 20px;
    }
    .stChatInput { border-top: 2px solid #1a73e8 !important; }
    </style>
    """, unsafe_allow_html=True)

if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

# نازناوی پڕۆژەکە
st.title("🤖 پڕۆژەی گەورەی K.AI Ultra")
st.markdown("### بنکەی زیرەکی دەستکردی نیشتمانی - سەرپەرشتیار: **K.Kod**")
st.divider()

# --- ٢. مەکینەی فێربوونی قووڵ و گەڕانی ئۆتۆماتیکی (Autonomous Engine) ---
def kai_engine_search(topic):
    """ئەم بەشە مێشکی K.AIـە کە خۆی دەچێتە ناو ئینتەرنێت کاتێک زانیاری نییە"""
    search_query = topic.replace(" ", "_")
    # گەڕان لە ویکیپیدیای کوردی وەک سەرچاوەی سەرەکی
    url = f"https://wikipedia.org{search_query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # دەرهێنانی تەواوی پەرەگرافەکان بۆ ئەوەی وەڵامەکە تێروتەسەل بێت
            paragraphs = soup.find_all(['p', 'h2', 'h3'])
            content = "\n\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 40])
            
            if len(content) > 100:
                with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n\n--- فێربوونی خۆکار لەسەر: {topic} ---\n{content}")
                return content
        return None
    except Exception as e:
        return None

# --- ٣. بەڕێوەبردنی مێژووی گفتوگۆ (Chat Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانی چاتەکانی پێشوو
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ٤. لۆژیکی وەڵامدانەوە و فێربوونی خودکار (Real-time Processing) ---
query = st.chat_input("لێرە پرسیار لە K.AI بکە یان بابەتێک بنووسە بۆ فێربوون...")

if query:
    # ١. نیشاندانی پرسیاری بەکارهێنەر
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # ٢. وەڵامدانەوەی K.AI
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # گەڕان لە مێشکی ناوخۆیی (K-Data)
        found_in_brain = False
        if os.path.exists("K-Data/brain.txt"):
            with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
                brain_knowledge = f.read()
            
            # لۆژیکی گەڕانی ورد لە ناو پەرەگرافەکان
            lines = brain_knowledge.split('\n\n')
            relevant_lines = [l for l in lines if any(word in l for word in query.split() if len(word) > 2)]
            
            if relevant_lines:
                full_response = "📖 **ئەوەی لە مێشکمدا دۆزیمەوە:**\n\n" + "\n\n".join(relevant_lines[:5])
                found_in_brain = True

        # ئەگەر لە مێشکدا نەبوو، یەکسەر دەچێت بۆ گەڕانی ئۆتۆماتیکی (خۆکار)
        if not found_in_brain:
            with st.spinner(f"🔍 K.AI خەریکی گەڕان و فێربوونی خۆکارە دەربارەی: {query}"):
                new_data = kai_engine_search(query)
                if new_data:
                    full_response = f"✅ **من فێری بابەتێکی نوێ بووم دەربارەی {query}:**\n\n" + new_data[:2000] + "..."
                else:
                    full_response = "ببورە جەنابت، نە لە مێشکمدا زانیاریم هەبوو نە لە ئینتەرنێت سەرچاوەیەکی پاکم بۆ دۆزییەوە."

        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- ٥. لایەنی بەڕێوەبردن (Sidebar Control) ---
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.header("⚙️ بەڕێوەبردنی K.AI")
    st.info(f"وەشانی: Mega Pro 1.0\nخاوەن: K.Kod")
    
    if st.button("🗑️ سڕینەوەی مێشک و مێژوو"):
        if os.path.exists("K-Data/brain.txt"):
            os.remove("K-Data/brain.txt")
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.write("ئەم وێب ئەپە تایبەتە بە کۆمەڵگەی K.Kod بۆ پەرەپێدانی زیرەکی دەستکردی کوردی.")
