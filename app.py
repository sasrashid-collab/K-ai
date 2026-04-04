import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- بەشی ناسنامە و ستایل (Frontend) ---
st.set_page_config(page_title="K.AI Project", layout="centered")
st.title("🤖 پڕۆژەی K.AI")
st.subheader("خاوەن: K.Kod")
st.write("بەخێربێیت جەنابت! ئەمە دەسپێکی وێب ئەپڵیکەیشنی تایبەت بە کوردە.")

# --- بەشی لۆژیک و فێربوون (Backend) ---
def learn_from_link(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = "\n".join([p.get_text() for p in paragraphs])
        
        # پاشەکەوتکردن لە فۆڵدەری K-Data
        if not os.path.exists('K-Data'): os.makedirs('K-Data')
        with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
            f.write(f"\nسەرچاوە: {url}\n{text_content[:1000]}...\n")
        return True
    except:
        return False

# --- ڕوونمای بەکارهێنەر (Interface) ---
url_input = st.text_input("لینکە کوردییەکە لێرە دابنێ:")
if st.button("بدە بە K.AI"):
    if url_input:
        with st.spinner('خەریکم زانیارییەکان دەخوێنمەوە...'):
            success = learn_from_link(url_input)
            if success:
                st.success("✅ K.AI زانیارییەکەی وەرگرت و مێشکی پەرە سەند!")
            else:
                st.error("❌ ناتوانم ئەم لینکە بخوێنمەوە.")
    else:
        st.warning("تکایە سەرەتا لینکێک بنووسە.")

st.divider()
st.info("ئەم ئەپڵیکەیشنە لەسەر لاپتۆپەکەت بە کەمترین ڕام کار دەکات.")
