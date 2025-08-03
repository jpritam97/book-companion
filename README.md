# JusticeBot

## Overview
**JusticeBot** is a lightweight legal assistant chatbot built to assist users with queries related to **Indian labor laws**. It takes one or more legal PDFs, breaks them into smaller parts, and uses AI to answer user questions based on that content. It works like a smart search engine with a chat interface, where users can ask questions and get accurate replies. The chatbot is built using modern tools like Streamlit (for the UI), FAISS (to store and search legal info), and advanced AI models from Hugging Face and Together.ai.
## Features
Features
- ✅ Extracts and processes legal text from PDFs.
- 🧠 Embeds knowledge using Hugging Face sentence transformers.
- 📦 Stores embeddings locally using FAISS.
- 🔍 Retrieves the most relevant legal context using semantic similarity.
- 🤖 Uses a powerful LLM (Mistral 7B) via Together.ai for generating answers.
- 💬 Interactive chat UI built with Streamlit.
- ♻️ Maintains conversation context using LangChain's memory.

## Setup Instructions

### 1. Clone the Repository and Navigate to Project Directory
```bash
git clone https://github.com/HardiDesai02/JusticeBot.git
cd JusticeBot
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
```
### 3. Activate the Virtual Environment
```bash
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Linux/macOS
```
### 4. Install Required Libraries
```bash
pip install -r requirements.txt
```

## Usage
### 1. Ingest Text Data
This step processes legal documents and builds the FAISS index and .pkl file for efficient retrieval.

```bash
python ingest.py
```
### 2. Run the Streamlit App
Start the chatbot interface using Streamlit.
```bash
streamlit run model.py
```
### API Key
This project uses Together.ai's Mistral-7B model. Replace the placeholder API key in model.py with your own:
```bash
together_api_key="your_api_key_here"
```
You can obtain a free API key from: https://api.together.xyz

## Use Case
This chatbot aims to:
- Help laypersons understand Indian Labour Law quickly.
- Reduce the time spent browsing dense legal documents.
- Provide a base prototype for future domain-specific legal bots.

## Future Scope
JusticeBot is currently focused on Indian labor law but can be extended to cover:
- Multi-document ingestion.
- Authentication.
- Custom UI with Streamlit components.
- Feedback mechanism for response quality.

