import os
from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model_name="gemma2-9b-it")

def qa_groq(question, pdf_paths):
    all_text = ""
    for path in pdf_paths:
        with open(path, "rb") as f:
            reader = PdfReader(f)
            all_text += "\n".join([p.extract_text() for p in reader.pages])
    prompt = f"Answer the question based on the following papers:\n\n{all_text[:12000]}\n\nQ: {question}"
    return llm([HumanMessage(content=prompt)]).content