import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI
import google.generativeai as genai


load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

# Check the key
if not api_key:
    print("No API key was found - please check your .env file and ensure GEMINI_API_KEY is set")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them")
else:
    print("API key found and looks good so far!")



# If you get an error running this cell, then please head over to the troubleshooting notebook!

SYSTEM_PROMPT = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

USER_PROMPT_PREFIX = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.
"""

def summarize_website(url):
    website = fetch_website_contents(url)
    if website.startswith("ERROR"):
        return website

    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    response = model.generate_content(
        USER_PROMPT_PREFIX + website
    )

    return response.text
