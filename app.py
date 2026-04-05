import streamlit as st
import requests
import time

# --- ١. ڕێکخستنی ناسنامە ---
st.set_page_config(page_title="K.AI Pro - Always Online", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; } </style>""", unsafe_allow_html=True)

st.title("🤖 K.AI Pro: وەشانی هەمیشە ئامادە")
st.subheader("پەرەپێدراوی K.Kod")

# --- ٢. مەکینەی وەڵامدانەوەی زیرەک (بێ وەستان) ---
def get_kai_response(prompt):
    # ئەم مۆدێلە زۆر خێراترە و کەمتر دەوەستێت
    models = [
        "https://huggingface.co",
        "https://huggingface.co"
    ]
    
    headers = {"Authorization": "Bearer hf_VvYpYpYpYpYpYpYpYpYpYpYpYpYp"} # ئەمە تەنها نموونەیە
    
    for model_url in models:
        try:
            payload = {"inputs": f"You are K.AI by K.Kod. Answer in Kurdish: {prompt}", "parameters": {"max_new_tokens": 500}}
            response = requests.post(model_url, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()[0]['generated_text']
        except:
            continue
    return "ببورە جەنابت، سێرڤەرەکە کەمێک قەرەباڵغە. تکایە چرکەیەک بوەستە و دووبارە تاقی بکەرەوە."

# --- ٣. ڕوونمای بەکارهێنەر ---
user_query = st.text_area("چی دەپرسی لە K.AI؟", placeholder="بۆ نموونە: مێژووی کورد بە کورتی بنووسە...")

if st.button("بپرسە"):
    if user_query:
        with st.spinner("K.AI خەریکی وەڵامدانەوەیە..."):
            answer = get_kai_response(user_query)
            st.markdown("### 📝 وەڵامی K.AI:")
            st.info(answer)
    else:
        st.warning("تکایە سەرەتا پرسیارێک بنووسە.")

st.sidebar.info("K.AI ئێستا وەک مێشکێکی سەربەخۆ کار دەکات.")
