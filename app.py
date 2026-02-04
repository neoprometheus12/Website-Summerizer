import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from summarizer import summarize_website

# Load env variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Website Summarizer",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Snarky Website Summarizer")
st.write("Paste any website URL and get a fun, snarky summary.")

url = st.text_input("🌐 Enter website URL")

if st.button("Summarize"):
    if not url:
        st.warning("Please enter a URL")
    else:
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_website(url)
                st.markdown(summary)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
