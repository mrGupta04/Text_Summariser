import streamlit as st
st.set_page_config(page_title="Advanced Text Summarizer", page_icon="📝", layout="wide")

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup

# -------------------- NLTK SETUP --------------------
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
download_nltk_resources()

# -------------------- FUNCTIONS --------------------
def read_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return str(uploaded_file.read(), "utf-8")

def fetch_text_from_url(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([p.get_text() for p in paragraphs])
    except:
        return ""

def textrank_summarizer(text, num_sentences=3):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    stop_words = set(stopwords.words('english'))
    clean_sentences = [
        " ".join([w.lower() for w in word_tokenize(s) if w.isalpha() and w.lower() not in stop_words])
        for s in sentences
    ]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(clean_sentences)
    sim_matrix = cosine_similarity(X, X)

    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(sentences)), reverse=True)
    top_sentences = sorted(ranked_sentences[:num_sentences], key=lambda x: x[2])

    return " ".join([s for _, s, _ in top_sentences])

def extract_keywords(text, top_n=10):
    words = [w for w in word_tokenize(text.lower()) if w.isalpha() and w not in stopwords.words('english')]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [w for w, _ in top_words]

# -------------------- STREAMLIT APP --------------------
st.title("📝 Advanced Text Summarizer")

# -------------------- Sidebar --------------------
st.sidebar.header("Options")
summary_length = st.sidebar.slider("Summary Length (sentences)", 1, 10, 3)
show_keywords = st.sidebar.checkbox("Show Keywords", value=True)
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"], index=0)
top_n_keywords = st.sidebar.slider("Number of Keywords", 5, 20, 10)

# Colors based on theme
bg_color = "#0E1117" if theme == "Dark" else "#f9f9f9"
text_color = "white" if theme == "Dark" else "#111111"
card_bg = "#1F1F1F" if theme == "Dark" else "white"
card_shadow = "0px 4px 20px rgba(0,0,0,0.3)" if theme == "Dark" else "0px 4px 20px rgba(0,0,0,0.1)"

# -------------------- CSS Styling --------------------
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Helvetica', sans-serif;
}}
.stTextArea textarea {{ 
    border-radius:12px; padding:1rem; font-size:1rem; background-color:{card_bg}; color:{text_color}; border:none; 
}}
.stButton button {{ 
    width:100%; border-radius:12px; padding:0.8rem; font-size:1rem; background: linear-gradient(to right, #4CAF50, #45A049); color:white; border:none; font-weight:bold; transition:0.3s;
}}
.stButton button:hover {{
    background: linear-gradient(to right, #45A049, #4CAF50);
}}
.summary-box {{
    background-color:{card_bg}; 
    color:{text_color}; 
    padding:1.5rem; 
    border-radius:12px; 
    box-shadow:{card_shadow};
    border-left:5px solid #4CAF50; 
    margin-top:1rem;
    font-size:1.05rem;
}}
.download-btn button {{
    background-color:#FF5722;
    border:none;
    padding:0.5rem 1rem;
    border-radius:10px;
    color:white;
    font-weight:bold;
}}
.download-btn button:hover {{
    background-color:#E64A19;
}}
</style>
""", unsafe_allow_html=True)

# -------------------- Inputs --------------------
uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
text_input = st.text_area("Or paste text here:", height=200)
url_input = st.text_input("Or provide a webpage URL:")

text = ""
if uploaded_file:
    text = read_uploaded_file(uploaded_file)
elif url_input:
    text = fetch_text_from_url(url_input)
elif text_input:
    text = text_input

# -------------------- Generate Summary --------------------
if st.button("Generate Summary"):
    if text and len(text.strip()) > 50:
        with st.spinner("Generating summary..."):
            summary = textrank_summarizer(text, num_sentences=summary_length)
            st.markdown("### Summary")
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

            if show_keywords:
                keywords = extract_keywords(text, top_n=top_n_keywords)
                if keywords:
                    st.markdown("### Keywords")
                    st.markdown(f'<div class="summary-box">{", ".join(keywords)}</div>', unsafe_allow_html=True)

            st.download_button("Download Summary", summary, file_name="summary.txt")
    else:
        st.warning("Please provide text or upload a file (minimum 50 characters).")
