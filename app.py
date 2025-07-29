import streamlit as st
from modules.layout import set_centered_layout
from modules.ingest import ingest_arxiv_paper, ingest_ieee_paper
from modules.section_splitter import extract_sections
from modules.summary_agent import summarize_sections
from modules.qa_agent import qa_groq
from modules.langgraph_agents import run_langgraph_agent
from modules.comparator import compare_papers, calculate_similarity
from PyPDF2 import PdfReader
from modules.visualizer import generate_wordcloud, show_topic_frequency
import os

IEEE_API_KEY = os.getenv("IEEE_API_KEY")
IEEE_ENABLED = IEEE_API_KEY and IEEE_API_KEY != "your_key_here"

set_centered_layout()

st.sidebar.title("📄 Upload or Search Papers")

uploaded_files = st.sidebar.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
arxiv_query = st.sidebar.text_input("Search Arxiv")

papers = []

if arxiv_query:
    path = ingest_arxiv_paper(arxiv_query)
    if path: papers.append(path)

if IEEE_ENABLED:
    ieee_query = st.sidebar.text_input("Search IEEE Paper:")
    if ieee_query:
        path = ingest_ieee_paper(ieee_query)
        if path: papers.append(path)
else:
    st.sidebar.info("🔒 IEEE integration is temporarily disabled. Awaiting API activation.")

if uploaded_files:
    for file in uploaded_files:
        path = os.path.join("assets", file.name)
        with open(path, "wb") as f: f.write(file.read())
        papers.append(path)

st.title("📚 AI Research Assistant")
st.markdown("Use the assistant to summarize, extract, and query research papers.")

query = st.text_input("Ask a question about your uploaded/search papers:")

if query:
    st.subheader("🧠 Assistant Answer:")
    answer = qa_groq(query, papers)
    st.success(answer)

if papers:
    for pdf_path in papers:
        if os.path.basename(pdf_path).lower() == "sample.pdf":
            continue  # skip displaying summary for sample.pdf

        st.subheader(f"📄 {os.path.basename(pdf_path)}")

        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

        sections = extract_sections(text)
        summaries = summarize_sections(sections)

        # Show section summaries
        for sec, summary in summaries.items():
            st.markdown(f"**{sec}**: {summary}")

        # 🔍 Visual Insights (WordCloud + Frequency Chart)
        st.markdown("### 📊 Visual Insights")

        combined_text = " ".join(sections.values())

        # Generate and show WordCloud
        generate_wordcloud(combined_text)

        # Show bar chart of frequent terms
        show_topic_frequency(sections)

        st.markdown("---")

    # Comparison Section
    st.subheader("📊 Paper Comparison")

    # Show comparison dashboard if multiple papers uploaded/searched
    if len(papers) >= 2:
        st.markdown("## 🧾 Paper Comparison Dashboard")
        comparison_data = compare_papers(papers)

        section_options = ["Abstract", "Methodology", "Results", "Conclusion"]
        selected_section = st.selectbox("🔍 Select Section to Compare", section_options)

        col1, col2 = st.columns(2)

        for i in range(0, len(comparison_data), 2):
            with col1:
                if i < len(comparison_data):
                    paper = comparison_data[i]
                    st.markdown(f"### 📘 {paper['filename']}")
                    st.markdown(f"**{selected_section} Summary:** {paper['summaries'].get(selected_section, 'N/A')}")

            with col2:
                if i + 1 < len(comparison_data):
                    paper = comparison_data[i + 1]
                    st.markdown(f"### 📘 {paper['filename']}")
                    st.markdown(f"**{selected_section} Summary:** {paper['summaries'].get(selected_section, 'N/A')}")

        #Similarity Score
        if len(comparison_data) == 2:
            text1 = comparison_data[0]["sections"].get(selected_section, "")
            text2 = comparison_data[1]["sections"].get(selected_section, "")
            similarity = calculate_similarity(text1, text2)
            st.info(f"🔗 Similarity Score for **{selected_section}**: **{similarity}%**")

else:
    st.info("Upload or search for papers to get summaries and papers comparison.")

#Footer
st.markdown("Built by Harshita Deewan and Team Mentox")