from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def generate_wordcloud(text, title="Keyword Cloud"):
    if not text.strip():
        st.info("No content to generate WordCloud.")
        return
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def show_topic_frequency(sections_dict):
    all_text = " ".join(sections_dict.values())
    words = [word.lower() for word in all_text.split() if len(word) > 4]
    freq = Counter(words).most_common(10)

    if not freq:
        st.info("No enough content for frequency chart.")
        return

    labels, counts = zip(*freq)
    fig, ax = plt.subplots()
    ax.bar(labels, counts, color='orange')
    ax.set_title("Top Keywords")
    ax.set_ylabel("Frequency")
    ax.set_xticklabels(labels, rotation=45)
    st.pyplot(fig)