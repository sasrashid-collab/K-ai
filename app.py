import streamlit as st
import os

# وەشانی شکۆمەندی و سەربەخۆی K.AI - پێشکەشە بە K.Kod
st.set_page_config(page_title="K.AI Independent", layout="wide")
st.markdown("<style>div{direction:rtl; text-align:right; font-family:'Tahoma';}</style>", unsafe_allow_html=True)

st.title("🤖 K.AI: زیرەکی دەستکردی سەربەخۆ")
st.subheader("خاوەن و دامەزرێنەر: جەنابی K.Kod")

if not os.path.exists('K-Data/brain.txt'):
    st.info("سڵاو جەنابت! من ئامادەم بۆ فێربوون. تکایە لە Sidebar زانیاریم پێ بدە.")

# وەڵامدانەوە تەنها لەسەر بنەمای مێشکی ناوخۆیی
query = st.chat_input("لێرە پرسیار بکە...")
if query:
    if os.path.exists('K-Data/brain.txt'):
        with open('K-Data/brain.txt', 'r', encoding='utf-8') as f:
            brain = f.read()
        results = [line for line in brain.split('\n') if query in line]
        if results:
            st.success("\n".join(results[:5]))
        else:
            st.warning("ئەمەم لە مێشکدا نییە، تکایە فێرم بکە.")
    else:
        st.error("مێشکم هێشتا خاڵییە.")

with st.sidebar:
    st.header("🛠️ ژووری پەرەپێدان")
    txt = st.text_area("زانیاری لێرە بنووسە بۆ مێشکی K.AI:")
    if st.button("پاشەکەوت بکە"):
        with open('K-Data/brain.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{txt}")
        st.success("فێربووم!")
