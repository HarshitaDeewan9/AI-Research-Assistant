from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq
import os

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="gemma2-9b-it")

def node_ingest(state): return {"text": state["text"]}
def node_extract(state): return {"abstract": "Extracted abstract"}
def node_summarize(state): return {"summary": "Short summary"}
def node_qa(state): return {"qa": f"Answer to: {state['query']}"}

def run_langgraph_agent(text="", query=""):
    builder = StateGraph()
    builder.add_node("Ingest", node_ingest)
    builder.add_node("Extract", node_extract)
    builder.add_node("Summarize", node_summarize)
    builder.add_node("QA", node_qa)

    builder.set_entry_point("Ingest")
    builder.add_edge("Ingest", "Extract")
    builder.add_edge("Extract", "Summarize")
    builder.add_edge("Summarize", "QA")
    builder.add_edge("QA", END)

    graph = builder.compile()
    state = graph.invoke({"text": text, "query": query})
    return state