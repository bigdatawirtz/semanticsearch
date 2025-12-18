# 📚 Semanticsearch

A lightweight web application for semantic search over JSON documents using ChromaDB vector database.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-Interface-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-green)
![Ollama](https://img.shields.io/badge/Ollama-RAG%20Enabled-purple)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
</div>


## 🚀 Features

- **🎯 In-Memory Processing**: All data is stored in RAM - disappears when the app stops
- **✅ JSON Validation**: Only valid JSON files are accepted and processed
- **🔍 Semantic Search**: Find documents based on meaning, not just keywords
- **🤖 LLM-Powered Question Answering (Ollama)**: Ask a local LLM running on Ollama to answer your question using the retrieved document as context.
- **🎨 Gradio Web Interface**: User-friendly interface with tabs for upload and search

## 🤖 LLM Integration (Ollama)

This application supports Retrieval-Augmented Generation (RAG) using Ollama.

Workflow:
1. You upload documents.
2. You ask a question.
3. The app retrieves the most relevant document using ChromaDB.
4. The question and the retrieved document are sent to a local Ollama model.
5. The LLM generates a contextualized answer based on the document.

## 📋 Prerequisites

- Python 3.11
- pip
- Ollama servide (running on `http://localhost:11434`) (default model: llama3.3)

## 🎯 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/bigdatawirtz/semanticsearch.git
cd semanticsearch
```

### 2. Create Virtual Environment

```
conda create --name semanticsearch python=3.11
conda activate semanticsearch 
conda install pip
pip install -r requirements.txt
```

### 3. Running the app

```bash
python semanticsearch.py
```

The application will start and provide a local URL (typically `http://localhost:7860`).

## 🐳 Docker Support
You can also run the app in a container.

### 1. Build the Docker Image

```bash
docker build -t semanticsearch .
```

### 2. Run the container

```bash
docker run -p 7860:7860 semanticsearch
```

### 3. Access the App
Open your browser and navigate to `http://localhost:7860`