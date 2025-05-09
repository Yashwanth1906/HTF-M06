import os
from autogen import AssistantAgent, UserProxyAgent
from docx import Document
from agents.keyWordAgent import keyword_extractor_agent,user_proxy
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_config = {
"model": "gemma2-9b-it",
    "api_key": GROQ_API_KEY,
    "base_url": "https://api.groq.com/openai/v1",
    "temperature": 0.3,
}

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def analysis_word(docx_path):
    extracted_text = extract_text_from_docx(docx_path)
    user_proxy.send(
        recipient=keyword_extractor_agent,
        message=f"""
Extract document-related keywords from the following text:
\"\"\"{extracted_text}\"\"\"
"""
    )
    reply = keyword_extractor_agent.generate_reply(sender=user_proxy)
    user_proxy.receive(sender=keyword_extractor_agent, message=reply)
    return reply
