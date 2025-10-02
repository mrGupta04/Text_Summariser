# Advanced Lightweight Text Summarizer 📝

A modern, feature-rich, and fully **lightweight text summarization web app** built using **Streamlit**, **NLTK**, **NetworkX**, and **scikit-learn**.  
No heavy transformer models or PyTorch required — works offline and fast!  

---

## Features

- **Flexible Summarization**
  - Summarize text by number of sentences or by percentage of original text.
  - Extractive summarization using **TextRank** algorithm.
  - Highlight most important sentences in the summary.

- **Keyword Extraction**
  - Top keywords extracted using **TF-IDF**.
  - Option to download keywords separately.

- **Text Statistics**
  - Word count, sentence count, character count, average sentence length.

- **Visualizations**
  - Word cloud of the most important words in the text.
  - Highlighting important sentences directly in the summary.

- **File Support**
  - Upload **PDF, DOCX, or TXT** files.
  - Supports multiple file uploads and combines text automatically.

- **Download Options**
  - Download summary and keywords as `.txt` files.

- **Lightweight & Fast**
  - Runs entirely on CPU.
  - No PyTorch, TensorFlow, or transformer models required.

---

## Live Demo

Try the app online here: **[Live Demo](https://share.streamlit.io/mrGupta04/Text_Summariser/main/app.py)**  

> Note: Replace the URL with your actual deployed Streamlit Cloud link once hosted.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/mrGupta04/Text_Summariser.git
cd Text_Summariser
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

> Or install manually:

```bash
pip install streamlit nltk networkx scikit-learn PyPDF2 python-docx wordcloud matplotlib
```

3. Run the app locally:

```bash
streamlit run app.py
```

---

## Usage

1. Upload files (PDF, DOCX, TXT) or paste text in the input box.  
2. Choose **summary mode**: by sentences or percentage.  
3. Set **summary length**, **number of keywords**, and optional **word cloud**.  
4. Click **Generate Summary**.  
5. View highlighted summary, keywords, statistics, and word cloud.  
6. Download summary and keywords using the provided buttons.

---

## Screenshots

*(Add your screenshots here for better presentation)*

---

## License

This project is open-source and free to use.  
Feel free to modify and share under the [MIT License](https://opensource.org/licenses/MIT).

---

## Author

**Aditya Gupta**  
GitHub: [mrGupta04](https://github.com/mrGupta04)
