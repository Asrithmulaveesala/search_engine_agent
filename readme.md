# 🔎 AI Search Engine Agent

An intelligent AI-powered search assistant built with **LangChain, Groq, and Streamlit** that automatically selects the appropriate tool to answer user queries. It supports academic research through Arxiv, general knowledge through Wikipedia, and question answering over uploaded PDFs using Retrieval-Augmented Generation (RAG).



## ✨ Features

- **Intelligent Tool Selection:** Automatically chooses the appropriate tool based on the user's query.
- **Academic Research:** Searches scientific papers using Arxiv.
- **General Knowledge:** Retrieves information using Wikipedia.
- **PDF Question Answering:** Upload a PDF and ask questions about its content using RAG.
- **Vector Search:** Uses FAISS for efficient similarity search.
- **Local Embeddings:** Generates document embeddings using Ollama's `nomic-embed-text` model.
- **LLM Integration:** Uses Groq-powered `openai/gpt-oss-120b` for intelligent responses.
- **Interactive UI:** Provides a simple interface using Streamlit.

## 🛠️ Tech Stack

- Python
- LangChain
- Groq API
- Streamlit
- Arxiv API
- Wikipedia API
- Ollama
- FAISS
- Retrieval-Augmented Generation (RAG)

## 🏗️ Architecture

1. The user submits a query through the Streamlit interface.
2. The LangChain agent analyzes the query and selects an appropriate tool.
3. Arxiv handles academic research queries.
4. Wikipedia handles general knowledge queries.
5. For PDF-related questions, the document is split into chunks, embedded using Ollama, and indexed in FAISS.
6. Relevant PDF chunks are retrieved and passed to the language model.
7. The generated answer is displayed to the user.

## ⚙️ Prerequisites

- Python 3.11
- A Groq API key
- Ollama installed locally (for PDF RAG)
- The `nomic-embed-text` Ollama embedding model

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd langchain-agent-search-engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Pass this key to the agent through your application's configuration. Never commit your `.env` file to GitHub.

### 5. Set up Ollama for PDF RAG

Install Ollama and download the embedding model:

```bash
ollama pull nomic-embed-text
```

Ensure Ollama is running locally before using PDF question answering.

### 6. Run the application

```bash
streamlit run app.py
```

Replace `app.py` with your actual Streamlit entry-point filename if it differs.

## 📂 Project Structure

```text
langchain-agent-search-engine/
├── images/
│   └── screenshot.png
├── app.py
├── agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file is local and should not be committed to GitHub.

## 🔍 Example Use Cases

- Find research papers about large language models.
- Explore general concepts using Wikipedia.
- Upload a PDF research paper and ask questions about its contents.

## 🔮 Future Improvements

- Add conversation memory.
- Display source references for generated answers.
- Improve retrieval quality and response evaluation.
- Deploy the application for public access.

## 👨‍💻 Author

**Koushik Asrith Mulavisala**

[GitHub](https://github.com/Asrithmulavisala)

---

*Built as a hands-on project to explore AI agents, tool calling, and Retrieval-Augmented Generation.*
