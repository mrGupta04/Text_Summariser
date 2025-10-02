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
from deep_translator import GoogleTranslator

# -------------------- NLTK SETUP --------------------
@st.cache_resource
def download_nltk_resources():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        st.error(f"Error downloading NLTK resources: {e}")

download_nltk_resources()

# -------------------- FUNCTIONS --------------------
def read_uploaded_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            return text.strip()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            return " ".join([para.text for para in doc.paragraphs if para.text.strip()])
        else:
            # Handle text files
            return str(uploaded_file.read(), "utf-8", errors='ignore')
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

def fetch_text_from_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        st.error(f"Error fetching URL: {e}")
        return ""

def textrank_summarizer(text, num_sentences=3):
    try:
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            return "No text available for summarization."
            
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text

        # Check if we have valid sentences after cleaning
        if len(sentences) <= 1:
            return "Not enough meaningful content to summarize."

        stop_words = set(stopwords.words('english'))
        clean_sentences = []
        
        for s in sentences:
            words = [w.lower() for w in word_tokenize(s) if w.isalpha() and w.lower() not in stop_words]
            if len(words) > 2:  # Only include sentences with meaningful content
                clean_sentences.append(" ".join(words))
        
        # If no clean sentences, return original text
        if not clean_sentences:
            return " ".join(sentences[:num_sentences])
            
        if len(clean_sentences) <= 1:
            return " ".join(sentences[:num_sentences])

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(clean_sentences)
        
        # Handle case where vectorization fails
        if X.shape[0] <= 1:
            return " ".join(sentences[:num_sentences])
            
        sim_matrix = cosine_similarity(X, X)

        nx_graph = nx.from_numpy_array(sim_matrix)
        scores = nx.pagerank(nx_graph)

        ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(sentences) if i < len(clean_sentences)), reverse=True)
        
        # Ensure we don't request more sentences than available
        actual_num = min(num_sentences, len(ranked_sentences))
        top_sentences = sorted(ranked_sentences[:actual_num], key=lambda x: x[2])

        return " ".join([s for _, s, _ in top_sentences]).strip()
        
    except Exception as e:
        return f"Error in summarization: {str(e)}"

def extract_keywords(text, top_n=10):
    try:
        if not text.strip():
            return []
            
        words = [w for w in word_tokenize(text.lower()) 
                if w.isalpha() and len(w) > 2 and w not in stopwords.words('english')]
        
        if not words:
            return []
            
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
            
        top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [w for w, _ in top_words if w.strip()]
    except Exception as e:
        st.error(f"Error extracting keywords: {e}")
        return []

# -------------------- STREAMLIT APP --------------------
st.title("📝 Advanced Text Summarizer")

# -------------------- Session State --------------------
if "translate_clicked" not in st.session_state:
    st.session_state.translate_clicked = False
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""
if "keywords" not in st.session_state:
    st.session_state.keywords = []

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
    line-height:1.6;
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
.info-box {{
    background-color:{card_bg};
    padding:1rem;
    border-radius:8px;
    margin:1rem 0;
    border-left:4px solid #2196F3;
}}
</style>
""", unsafe_allow_html=True)

# -------------------- Inputs --------------------
input_method = st.radio("Choose input method:", ["Text", "File Upload", "URL"], horizontal=True)

text = ""
if input_method == "File Upload":
    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if uploaded_file:
        text = read_uploaded_file(uploaded_file)
        if text:
            st.info(f"✅ File uploaded successfully! Text length: {len(text)} characters")

elif input_method == "URL":
    url_input = st.text_input("Enter webpage URL:")
    if url_input:
        if url_input.startswith(('http://', 'https://')):
            with st.spinner("Fetching content from URL..."):
                text = fetch_text_from_url(url_input)
            if text:
                st.info(f"✅ URL content fetched! Text length: {len(text)} characters")
            else:
                st.error("❌ Could not fetch content from URL. Please check the URL and try again.")
        else:
            st.warning("Please enter a valid URL starting with http:// or https://")

else:  # Text input
    text_input = st.text_area("Paste your text here:", height=200, 
                             placeholder="Enter your text here... (minimum 100 characters recommended)")
    text = text_input

# Display text stats if text is available
if text and len(text.strip()) > 0:
    st.markdown(f'<div class="info-box">📊 Text Statistics: {len(text)} characters, {len(text.split())} words, {len(sent_tokenize(text))} sentences</div>', 
                unsafe_allow_html=True)

languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
    "Arabic": "ar"
}

# -------------------- Generate Summary --------------------
if st.button("Generate Summary", type="primary"):
    if text and len(text.strip()) > 50:
        with st.spinner("🔍 Analyzing text and generating summary..."):
            summary = textrank_summarizer(text, num_sentences=summary_length)
            st.session_state.summary_text = summary

            st.markdown("### 📄 Summary")
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

            # Download original summary
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

            if show_keywords:
                keywords = extract_keywords(text, top_n=top_n_keywords)
                st.session_state.keywords = keywords
                if keywords:
                    st.markdown("### 🔑 Keywords")
                    st.markdown(f'<div class="summary-box">{", ".join(keywords)}</div>', unsafe_allow_html=True)

            st.session_state.translate_clicked = True
    else:
        st.warning("⚠️ Please provide sufficient text (minimum 50 characters).")

# -------------------- Translate --------------------
if st.session_state.translate_clicked and st.session_state.summary_text:
    st.markdown("---")
    st.markdown("### 🌐 Translate Summary")
    translate_lang = st.selectbox("Select target language:", list(languages.keys()), index=0)
    
    if st.button("Translate Summary"):
        if translate_lang != "English":
            try:
                with st.spinner(f"Translating to {translate_lang}..."):
                    translated = GoogleTranslator(
                        source='auto', 
                        target=languages[translate_lang]
                    ).translate(st.session_state.summary_text)
                    
                st.markdown(f"### 📄 Translated Summary ({translate_lang})")
                st.markdown(f'<div class="summary-box">{translated}</div>', unsafe_allow_html=True)
                
                st.download_button(
                    "📥 Download Translated Summary", 
                    translated, 
                    file_name=f"summary_{translate_lang.lower()}.txt",
                    key="download_translated"
                )
            except Exception as e:
                st.error(f"❌ Translation failed: {e}")
        else:
            st.info("ℹ️ Selected language is English. No translation needed.")
