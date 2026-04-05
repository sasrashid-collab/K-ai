import streamlit as st
import requests

# --- ١. ناسنامەی گشتگیری K.AI ---
st.set_page_config(page_title="K.AI Universal - K.Kod", layout="wide")
st.markdown("""<style> .stApp { direction: rtl; text-align: right; font-family: 'Tahoma'; } 
.stChatInput { direction: rtl; } </style>""", unsafe_allow_html=True)

st.title("🤖 K.AI Universal: زیرەکی دەستکردی گشتگیر")
st.subheader("پەرەپێدراوی دامەزراوەی K.Kod بۆ خزمەتی هەموو بوارەکان")

# --- ٢. مەکینەی وەڵامدانەوەی لۆژیکی و گشتگیر (بەبێ وەستان) ---
def ask_kai_universal(prompt):
    # بەکارهێنانی مۆدێلی Mistral 7B کە یەکێکە لە زیرەکترین مۆدێلە گشتگیرەکان
    API_URL = "https://huggingface.co"
    headers = {"Authorization": "Bearer hf_VvYpYpYpYpYpYpYpYpYpYpYpYpYp"} # لێرەدا کلیلەکەی جەنابت یان کلیلێکی گشتی دادەنێین
    
    payload = {
        "inputs": f"وەک زیرەکی دەستکردی K.AI کە لەلایەن K.Kod دروستکراویت، بە کوردییەکی زۆر ورد وەڵامی ئەمە بدەرەوە لە هەر بوارێکدایە: {prompt}",
        "parameters": {"max_new_tokens": 1000, "return_full_text": False}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return "⚠️ سێرڤەرەکە کەمێک خاوە، تکایە دووبارە پرسیار بکەرەوە."
    except:
        return "❌ کێشەی پەیوەندی هەیە."

# --- ٣. ڕوونمای گفتوگۆ (Chat Interface) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input("لێرە هەرچییەکت دەوێت بپرسە (کۆدینگ، زانست، مێژوو، ئەدەب)...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
        
    with st.chat_message("assistant"):
        with st.spinner("K.AI خەریکی لێکۆڵینەوەیە..."):
            answer = ask_kai_universal(query)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

st.sidebar.markdown("### ⚙️ تایبەتمەندییەکانی K.AI")
st.sidebar.info("ئەم مۆدێلە گشتگیرە و لە هەموو بوارەکاندا وەڵامت دەداتەوە.")
