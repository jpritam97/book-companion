# Book Companion

## Overview
**Book Companion** is an intelligent PDF assistant that transforms your documents into an interactive knowledge companion. Built with modern AI technology, it allows you to upload PDF documents and have natural conversations about their content. Whether you're studying textbooks, analyzing research papers, or reviewing legal documents, Book Companion helps you extract insights and answer questions through an intuitive chat interface.

## ScreenShots
<img width="1919" height="946" alt="Screenshot 2025-08-04 114201" src="https://github.com/user-attachments/assets/aed91267-b16a-46a6-b748-c210eb793d5e" />
<img width="1919" height="946" alt="Screenshot 2025-08-04 114840" src="https://github.com/user-attachments/assets/0657f3b3-c94c-441b-90d8-d3a7978f8c26" />
<img width="1919" height="943" alt="Screenshot 2025-08-04 120227" src="https://github.com/user-attachments/assets/b0caedb7-b181-4ab1-855e-b4f571ebc7e4" />




## ✨ Features

- 📚 **PDF Processing**: Upload and process any PDF document with automatic text extraction
- 🧠 **AI-Powered Chat**: Natural language conversations about your document content
- 🔍 **Semantic Search**: Find relevant information using advanced embedding technology
- 💬 **Conversation Memory**: Maintains context throughout your chat sessions
- 🎨 **Modern UI**: Beautiful, responsive interface built with Streamlit
- ⚡ **Fast Retrieval**: Efficient vector search using FAISS
- 🔄 **Session Management**: Reset conversations and start fresh anytime
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Embeddings: Hugging Face Sentence Transformers
  - Language Model: Together.ai (Mistral 7B)
- **Vector Database**: FAISS for efficient similarity search
- **Text Processing**: LangChain for document processing and conversation management
- **PDF Processing**: PyPDF2 and PyMuPDF for robust text extraction

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Book-Companion
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your API key**
   
   Get a free API key from [Together.ai](https://api.together.xyz) and update it in `model.py`:
   ```python
   together_api_key = "your_api_key_here"
   ```

6. **Run the application**
   ```bash
   streamlit run model.py
   ```

   The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Getting Started
1. **Upload a PDF**: Use the file uploader in the sidebar to upload your document
2. **Process Document**: Click "Process PDF" to extract and index the content
3. **Start Chatting**: Ask questions about your document in the chat interface
4. **Reset Conversation**: Use the "Reset Conversation" button to start fresh

### Example Questions
- "What are the main topics covered in this document?"
- "Can you summarize chapter 3?"
- "What does the document say about [specific topic]?"
- "Explain the key concepts in the introduction"

## 🔧 Configuration

### API Keys
The application requires a Together.ai API key for the language model. You can get a free key at [Together.ai](https://api.together.xyz).

### Model Settings
- **Embedding Model**: `multi-qa-mpnet-base-dot-v1` (Hugging Face)
- **Language Model**: Mistral 7B (via Together.ai)
- **Chunk Size**: 512 characters with 64 character overlap
- **Memory Window**: Maintains conversation context

## 📁 Project Structure

```
Book Companion/
├── model.py              # Main Streamlit application
├── ingest.py             # Document processing script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── data/                # Document storage
│   └── Labour Act.pdf   # Example document
├── vector_db/           # FAISS index storage
│   ├── index.faiss
│   └── index.pkl
└── venv/                # Virtual environment
```

## 🎯 Use Cases

- **Academic Research**: Analyze research papers and academic documents
- **Legal Documents**: Review contracts, legal texts, and regulations
- **Textbooks**: Study and understand complex educational materials
- **Business Reports**: Extract insights from company documents
- **Technical Manuals**: Get quick answers from technical documentation

## 🔮 Future Enhancements

- [ ] Multi-document support
- [ ] Document comparison features
- [ ] Export conversation history
- [ ] Custom embedding models
- [ ] Advanced search filters
- [ ] User authentication
- [ ] Collaborative features
- [ ] Mobile app version

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [Together.ai](https://together.ai/) for AI capabilities
- Uses [Hugging Face](https://huggingface.co/) models for embeddings
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss)

---

**Book Companion** - Your intelligent reading assistant powered by AI.







