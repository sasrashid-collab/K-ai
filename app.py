import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- ڕێکخستنی ناسنامەی K.AI ---
st.set_page_config(page_title="K.AI by K.Kod", page_icon="🤖")
st.title("🤖 پڕۆژەی زیرەکی دەستکردی K.AI")
st.markdown("### خاوەن و سەرپەرشتیار: **K.Kod**")
st.info("ئەم مۆدێلە لەسەر بنەمای زانیارییە کوردییەکان پەرە بەخۆی دەدات.")

# دروستکردنی فۆڵدەری زانیاری ئەگەر نەبێت
if not os.path.exists('K-Data'):
    os.makedirs('K-Data')

# --- بەشی یەکەم: خوێندنەوەی لینک (فێربوون) ---
st.sidebar.header("📚 مێشکی K.AI دەوڵەمەند بکە")
url_input = st.sidebar.text_input("لینکێکی کوردی لێرە دابنێ:")
if st.sidebar.button("فێری بکە"):
    if url_input:
        with st.spinner('خەریکم زانیارییەکان دەخوێنمەوە...'):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text, 'html.parser')
                text = " ".join([p.get_text() for p in soup.find_all('p')])
                
                with open("K-Data/brain.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{text[:2000]}") # پاشەکەوتکردنی ٢٠٠٠ پیتی یەکەم
                st.sidebar.success("✅ زانیاری نوێ وەرگیرا!")
            except:
                st.sidebar.error("❌ کێشەیەک لە لینکەکەدا هەیە.")

# --- بەشی دووەم: چات و وەڵامدانەوە (Search) ---
st.divider()
user_query = st.text_input("چی دەپرسی لە K.AI؟ (بۆ نموونە: مێژووی کورد چییە؟)")

if user_query:
    with st.chat_message("assistant"):
        # لێرەدا K.AI دەگەڕێت لەناو ئەو فایلەی کە پێشتر فێری بووە
        if os.path.exists("K-Data/brain.txt"):
            with open("K-Data/brain.txt", "r", encoding="utf-8") as f:
                knowledge = f.read()
            
            # گەڕانێکی سادە بۆ دۆزینەوەی وەڵام (وەک نموونە)
            if user_query.lower() in knowledge.lower() or "کورد" in user_query:
                st.write(f"وەک یاریدەدەرێکی K.Kod، ئەوەی فێری بووم دەربارەی '{user_query}':")
                st.write(knowledge[:500] + "...") # نیشاندانی بەشێک لە زانیارییەکە
            else:
                st.write("ببورە جەنابت، هێشتا زانیاری تەواوم نییە لەسەر ئەم بابەتە. تکایە لینکێکی ترم بدەرێ تا فێری ببم.")
        else:
            st.write("سڵاو! من K.AIـم. تکایە سەرەتا لە ڕێگەی لایەنی چەپەوە چەند لینکێکم بدەرێ تا فێری ببم و وەڵامت بدەمەوە.")

st.sidebar.write("---")
st.sidebar.write("وەشانی: 1.0 (Beta)")
