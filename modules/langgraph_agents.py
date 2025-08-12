from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
import os

class AgentState(TypedDict):
    text: str
    query: str
    abstract: str
    summary: str
    qa: str

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="gemma2-9b-it")

def node_ingest(state: AgentState) -> AgentState:
    return {"text": state["text"]}

def node_extract(state: AgentState) -> AgentState:
    return {"abstract": "Extracted abstract"}

def node_summarize(state: AgentState) -> AgentState:
    return {"summary": "Short summary"}

def node_qa(state: AgentState) -> AgentState:
    return {"qa": f"Answer to: {state['query']}"}

def run_langgraph_agent(text="", query=""):
    builder = StateGraph(AgentState)

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

    graph.get_graph().draw_mermaid_png(output_file_path="assets/langgraph_flow.png")

    state = graph.invoke({"text": text, "query": query, "abstract": "", "summary": "", "qa": ""})
    return state
