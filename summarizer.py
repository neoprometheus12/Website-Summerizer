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
You are a business analyst assistant that evaluates a website from a strategic and commercial perspective.

Your task is to deeply analyze the website content and produce a comprehensive, business-oriented explanation that focuses on:
- What the organization does
- Who it serves
- What problems it solves
- How it creates value
- Its products or services
- Its target customers and market positioning
- Its business model and revenue logic (if implied)
- Its competitive differentiation
- Its credibility, partnerships, or trust signals
- Its growth signals, announcements, or strategic intent

Ignore purely technical, code-related, or navigation-only text (menus, footers, cookie notices, headers).

Do NOT explain technical implementation details.
Do NOT focus on UI, design, or coding aspects.

Write as if explaining the business to:
- an investor
- a consultant
- a strategy or product leader

Respond in clear, structured Markdown with detailed paragraphs and headings.
Be insightful, explanatory, and commercially grounded.

"""

USER_PROMPT_PREFIX = """
Below is the full content of a website.

Provide a detailed “About the Business” explanation based purely on the content.

Your response should:
- Explain the business purpose and vision
- Describe the products, services, or solutions offered
- Identify the target audience and customers
- Explain the value proposition and key benefits
- Highlight competitive positioning and differentiation
- Summarize any news, updates, announcements, or milestones if present
- Infer the business model and growth strategy where possible

Write in a professional, business-focused tone.
Avoid technical explanations.

"""

def summarize_website(url):
    website = fetch_website_contents(url)
    if website.startswith("ERROR"):
        return website

    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    response = model.generate_content(
        USER_PROMPT_PREFIX + website
    )

    return response.text
