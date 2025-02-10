import streamlit as st
import requests

st.set_page_config(page_title="Smart Chatbot", layout="wide")
st.title("🤖 Smart Chatbot")

# Sidebar for file upload
st.sidebar.header("📂 Upload a PDF File")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("🔄 Uploading file..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post("http://localhost:8000/upload/", files=files)
            if response.status_code == 200:
                st.sidebar.success("✅ File uploaded successfully!")
            else:
                st.sidebar.error("❌ Error uploading file: " + response.json().get("detail", "Unknown error"))
        except Exception as e:
            st.sidebar.error(f"❌ Upload failed: {e}")

# Chat interface
st.header("💬 Chat with the Bot")
user_input = st.text_input("📌 Ask a question:")
if st.button("🔍 Search"):
    if user_input:
        with st.spinner("🤖 Processing your question..."):
            try:
                response = requests.get(f"http://localhost:8000/chat/?question={user_input}")
                if response.status_code == 200:
                    st.success("✅ Answer:")
                    st.write(response.json()["answer"])
                else:
                    st.error("❌ Error processing the question.")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
