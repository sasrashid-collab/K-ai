import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="K.AI Pro - K.Kod", layout="wide")

if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

st.title("🤖 وەشانی نوێی K.AI بۆ خوێندنەوەی فایلەکانی گۆگڵ")
st.subheader("سەرپەرشتیار: K.Kod")

# --- لۆژیکی خوێندنەوەی لینکەکان ---
def clean_and_read(url):
    url = url.strip()
    # لادانی خاڵ یان هەر نیشانەیەک لە سەرەتای لینکەکە
    if url.startswith("."):
        url = url[1:]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # گەڕان بەدوای دەق لە ناو فایلەکانی گۆگڵدا
        text = ""
        for tag in soup.find_all(['p', 'div', 'span']):
            text += tag.get_text() + " "
            
        if len(text.strip()) > 20:
            with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{text}")
            return True, f"✅ {len(text[:1000])} پیت لەم لینکە وەرگیرا."
        else:
            return False, "⚠️ لاپەڕەکە بەتاڵە یان گۆگڵ ڕێگەی نەدا."
    except Exception as e:
        return False, f"❌ هەڵە: {str(e)}"

# --- ڕوونمای بەکارهێنەر ---
st.sidebar.header("📚 مێشکی K.AI")
url_input = st.sidebar.text_area("لینکەکان لێرە دابنێ (هەر لینکێک لە دێڕێک):")

if st.sidebar.button("دەستپێکردنی فێربوون"):
    links = url_input.split('\n')
    for link in links:
        if link.strip():
            success, msg = clean_and_read(link)
            if success: st.sidebar.success(f"{link}: {msg}")
            else: st.sidebar.error(f"{link}: {msg}")

# --- بەشی چات ---
st.divider()
query = st.text_input("پرسیار لە K.AI بکە:")
if query:
    if os.path.exists("K-Data/brain.txt"):
        with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
            data = f.read()
        # وەڵامێکی سادە لەسەر بنەمای ئەوەی خوێندوویەتییەوە
        if query in data or "کورد" in query:
            st.write("📖 وەڵامی دۆزراوە:")
            st.write(data[:1500] + "...")
        else:
            st.warning("ببورە، هێشتا ئەمەم فێر نەکراوە.")
