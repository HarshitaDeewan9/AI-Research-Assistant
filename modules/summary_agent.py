import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model_name="gemma2-9b-it")

def summarize_sections(sections):
    summaries = {}
    for sec, content in sections.items():
        if content:
            prompt = f"Summarize the following {sec}:\n\n{content}"
            summaries[sec] = llm([HumanMessage(content=prompt)]).content
    return summaries