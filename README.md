# 📝 Text Summarizer  

![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)  
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)  
![License](https://img.shields.io/badge/License-MIT-green)  

⚡ A **modern, lightweight, and feature-rich text summarization web app** built with **Streamlit**, **NLTK**, **NetworkX**, and **scikit-learn**.  
No heavy transformer models, no GPU requirements — **just fast, offline summarization**.  

👉 [**Live Demo Here**](https://mrgupta04-text-summariser-app-zaelg9.streamlit.app/)  

---

## 📸 Preview  

![App Screenshot](https://github.com/mrGupta04/certificate/blob/main/Text_sum.png?raw=true)


---

## ✨ Features  

🔹 **Flexible Summarization**  
- Summarize by number of sentences or by percentage of original text.  
- Uses the **TextRank algorithm** for extractive summarization.  
- Highlights important sentences in the summary.  

🔹 **Keyword Extraction**  
- Extract top keywords using **TF-IDF**.  
- Download keywords as a `.txt` file.  

🔹 **Text Statistics**  
- Word count, sentence count, character count, and average sentence length.  

🔹 **Visualizations**  
- Beautiful **Word Cloud** for top keywords.  
- Highlighted summary display.  

🔹 **File Support**  
- Upload **PDF, DOCX, TXT** files.  
- Supports multiple uploads and merges text automatically.  

🔹 **🌍 Translation**  
- Translate summaries into multiple languages:  
  `English, Spanish, French, German, Hindi, Chinese`.  
- Powered by **GoogleTranslator** (`deep-translator`).  

🔹 **Download Options**  
- Export summaries, translations, and keywords as `.txt`.  

🔹 **💡 Lightweight & Fast**  
- Runs on **CPU only** — no PyTorch, TensorFlow, or GPUs required.  

---

## 🚀 Installation  

1️⃣ Clone the repository  

```bash
git clone https://github.com/mrGupta04/Text_Summariser.git
cd Text_Summariser
```

2️⃣ Install dependencies  

```bash
pip install -r requirements.txt
```

Or install manually:  

```bash
pip install streamlit nltk networkx scikit-learn PyPDF2 python-docx wordcloud matplotlib deep-translator
```

3️⃣ Run the app  

```bash
streamlit run app.py
```

---

## 🛠 Usage  

1. Upload a file (**PDF, DOCX, TXT**) or paste text.  
2. Select **summary mode** → by sentences or percentage.  
3. Choose **summary length**, **keywords count**, or enable **Word Cloud**.  
4. (Optional) Enable **translation** and pick a target language.  
5. Click **Generate Summary** 
6. View **summary, keywords, statistics, and translation**.  
7. Download results as `.txt` files.  

---



## 👨‍💻 Author  

**Aditya Gupta**  
🔗 [GitHub: mrGupta04](https://github.com/mrGupta04)  

---

