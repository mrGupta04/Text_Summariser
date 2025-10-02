import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string, re
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx
from PyPDF2 import PdfReader

# Download required NLTK data
for resource in ["punkt", "stopwords"]:
    try:
        nltk.data.find(f"tokenizers/{resource}" if resource=="punkt" else f"corpora/{resource}")
    except LookupError:
        nltk.download(resource)

# -------------------- FUNCTIONS --------------------

def read_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return str(uploaded_file.read(), "utf-8")

# Extractive summarizer using TextRank
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

# Keyword extraction using NLTK (no spaCy)
def extract_keywords(text, top_n=10):
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stopwords.words('english')]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [w for w, _ in top_words]

# -------------------- STREAMLIT APP --------------------

st.set_page_config(page_title="Advanced Text Summarizer", page_icon="📝", layout="wide")

st.markdown("""
            
<style>
.stTextArea textarea { 
            border-radius:10px;
            padding:1rem; 
            font-size:1rem;
            }
.stButton button
             { width:100%; 
            border-radius:10px;
            padding:0.75rem; 
            font-size:1rem;
            background-color:#4CAF50; 
            color:white;
            border:none;}
.summary-box {
            background-color:#f8f9fa;
            color:black;
            padding:1.5rem; 
            border-radius:10px; 
            border-left:4px solid #4CAF50;
            margin-top:1rem;}
</style>

            
""", unsafe_allow_html=True)


st.title("📝Text Summarizer")

# Sidebar options
st.sidebar.header("Options")
summary_length = st.sidebar.slider("Summary Length (sentences)", min_value=1, max_value=10, value=3)
show_keywords = st.sidebar.checkbox("Show Keywords", value=True)

# File upload or text input
uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT) or paste text below:", type=["pdf", "docx", "txt"])
text_input = st.text_area("Or paste text here:", height=250)

text = ""
if uploaded_file:
    text = read_uploaded_file(uploaded_file)
elif text_input:
    text = text_input

# Generate summary
if st.button("Generate Summary"):
    if text and len(text.strip()) > 50:
        with st.spinner("Generating summary..."):
            summary = textrank_summarizer(text, num_sentences=summary_length)
            
            st.markdown("### Summary")
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

            # Keywords
            if show_keywords:
                keywords = extract_keywords(text)
                if keywords:
                    st.markdown("### Keywords")
                    st.markdown(", ".join(keywords))

            # Download button
            st.download_button("Download Summary", summary, file_name="summary.txt")
    else:
        st.warning("Please provide text or upload a file (minimum 50 characters).")
