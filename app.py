import streamlit as st
import os
import google.generativeai as genai
from summarizer import summarize_website

# -------------------------------------------------
# Page config (must be first Streamlit command)
# -------------------------------------------------
st.set_page_config(
    page_title="Snarky Website Summarizer",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------
# Configure Gemini (works for both local + cloud)
# -------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please set it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🧠 Snarky Website Summarizer")
st.write("Paste any website URL and get a fun, snarky summary.")

url = st.text_input("🌐 Enter website URL", placeholder="https://example.com")

# -------------------------------------------------
# Action
# -------------------------------------------------
if st.button("Summarize"):
    if not url.strip():
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_website(url)

        # Handle scraper / backend errors cleanly
        if summary.startswith("ERROR"):
            st.error(summary)
        else:
            st.markdown(summary)
