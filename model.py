import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_together import Together
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
import PyPDF2
import fitz  # PyMuPDF
import tempfile
import hashlib
import time
import json
import base64

st.set_page_config(
    page_title="BookBot - Your Personal PDF Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for BookBot styling
st.markdown("""
<style>
    .main { padding: 0; }
    .stApp { 
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff; 
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        color: #ffffff !important;
        border-right: 1px solid #333;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed #667eea !important;
        border-radius: 12px !important;
        padding: 30px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
    }
    
    .stFileUploader > div {
        background: transparent !important;
        color: #ffffff !important;
    }
    
    .stFileUploader p,
    .stFileUploader span,
    .stFileUploader div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Chat message styling */
    .message-bubble {
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        line-height: 1.4;
    }
    
  
    
   
    
/* Chat container */
.chat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

.chat-message-container {
    display: flex;
    margin: 6px 0;
}

/* Align user's message to the right */
.chat-message-container.user {
    justify-content: flex-end;
}

/* Align assistant's message to the left */
.chat-message-container.assistant {
    justify-content: flex-start;
}

/* Bubble styling */
.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 10px 16px;
    border-radius: 25px;
    max-width: 80%;
    word-wrap: break-word;
    text-align: right;
    font-size: 16px;
}

/* Assistant bubble */
.assistant-bubble {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 25px;
    max-width: 80%;
    word-wrap: break-word;
    text-align: left;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    font-size: 16px;
}

    
    /* Welcome section */
    .welcome-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 40px 20px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 2px dashed #667eea;
        text-align: center;
    }
    
    .welcome-section h1 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 32px;
        font-weight: 700;
    }
    
    .welcome-section p {
        color: #6c757d;
        font-size: 18px;
        margin-bottom: 30px;
    }
    
    .welcome-section h3 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 20px;
    }
    
    .welcome-section ul {
        color: #34495e;
        font-size: 16px;
        line-height: 1.8;
        padding-left: 20px;
        text-align: left;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .welcome-section li {
        margin-bottom: 10px;
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
        color: #ffffff !important;
        padding: 12px 20px !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Make all text white by default */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {
        color: #ffffff !important;
    }
    
    /* Override for welcome section */
    .welcome-section * {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

if "current_pdf" not in st.session_state:
    st.session_state["current_pdf"] = None

if "vectordb" not in st.session_state:
    st.session_state["vectordb"] = None

if "pdf_pages" not in st.session_state:
    st.session_state["pdf_pages"] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

if "show_pdf_context" not in st.session_state:
    st.session_state["show_pdf_context"] = False

# Reset conversation function
def reset_conversation():
    st.session_state["messages"] = []
    if "memory" in st.session_state:
        st.session_state["memory"].clear()

# Cached embeddings function
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"}
    )

# Extract text with page information
def extract_text_with_pages(pdf_file):
    pdf_file.seek(0)  # Reset file pointer
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pages_data = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        pages_data.append({
            "page": page_num + 1,
            "text": text,
            "bbox": page.rect
        })
    
    doc.close()
    return pages_data

# Process PDF and create vector store
def process_pdf_with_pages(pdf_file):
    pdf_file.seek(0)  # Reset file pointer
    
    # Extract text with pages
    pages_data = extract_text_with_pages(pdf_file)
    
    # Combine all text for chunking
    all_text = ""
    for page_data in pages_data:
        all_text += f"Page {page_data['page']}: {page_data['text']}\n\n"
    
    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    chunks = text_splitter.split_text(all_text)
    
    # Create embeddings and vector store
    embeddings = get_embeddings()
    vectordb = FAISS.from_texts(chunks, embeddings)
    
    return vectordb, pages_data

# Get PDF hash for caching
def get_pdf_hash(pdf_file):
    pdf_file.seek(0)  # Reset file pointer
    try:
        content = pdf_file.read()
        return hashlib.md5(content).hexdigest()
    except:
        return str(time.time())  # Fallback hash

# Main layout with BookBot styling
st.markdown("""
<div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
    <h1 style="color: white; margin-bottom: 10px; font-size: 36px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">📚 BookBot</h1>
    <p style="color: #ecf0f1; font-size: 18px; margin: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Your AI-Powered PDF Assistant</p>
</div>
""", unsafe_allow_html=True)

# Move file uploader to sidebar
with st.sidebar:
    st.markdown("### 📄 PDF Upload")
    uploaded_file = st.file_uploader(
        label="Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to ask questions about"
    )
    
    st.markdown("---")
    
    # Reset button in sidebar
    if st.button("🗑️ Reset Chat", on_click=reset_conversation, use_container_width=True):
        st.rerun()

# Show document info once uploaded
if uploaded_file is not None:
    pdf_hash = get_pdf_hash(uploaded_file)
    
    if st.session_state["current_pdf"] != pdf_hash:
        st.session_state["current_pdf"] = pdf_hash
        
        with st.spinner("Processing PDF..."):
            try:
                vectordb, pages_data = process_pdf_with_pages(uploaded_file)
                st.session_state["vectordb"] = vectordb
                st.session_state["pdf_pages"] = pages_data
                st.success("✅ PDF processed successfully!")
            except Exception as e:
                st.error(f"❌ Failed to process PDF: {str(e)}")
                st.session_state["current_pdf"] = None
    
    # Info card in main area
    st.markdown(f"""
    <div class="info-card">
        <h4 style="color: white; margin-bottom: 8px; font-size: 14px;">📖 Document Info</h4>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 3px 0; font-size: 12px;"><strong>File:</strong> {uploaded_file.name}</p>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 3px 0; font-size: 12px;"><strong>Size:</strong> {uploaded_file.size:,} bytes</p>
    </div>
    """, unsafe_allow_html=True)



# Main content area with better structure
if uploaded_file is not None and st.session_state["vectordb"] is not None:
    # Chat interface with BookBot styling
    st.markdown("""
    <div class="chat-container">
        <h3 style="color: white;margin-top: 8px; margin-bottom: 8px; text-align: center; font-size: 20px;">💬 Legal Assistant Chat</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container with normal scrolling (newest at bottom, scroll up to see older messages)
    chat_area = st.container()
    
    with chat_area:
        # Display chat history with newest messages at the bottom
        st.markdown('<div class="chat-scroll-container">', unsafe_allow_html=True)
        st.markdown('<div class="chat-messages-wrapper">', unsafe_allow_html=True)
        
        # Display messages in chronological order (oldest first, newest at bottom)
        for i, message in enumerate(st.session_state["messages"]):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message-container user">
                    <div class="user-bubble">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-container assistant">
                    <div class="assistant-bubble">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-scroll to bottom JavaScript
        st.markdown("""
        <script>
            // Auto-scroll to bottom when new messages are added
            function scrollToBottom() {
                const chatContainer = document.querySelector('.chat-messages-wrapper');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
            
            // Scroll to bottom on page load
            window.addEventListener('load', scrollToBottom);
            
            // Scroll to bottom when new content is added
            const observer = new MutationObserver(scrollToBottom);
            const chatContainer = document.querySelector('.chat-messages-wrapper');
            if (chatContainer) {
                observer.observe(chatContainer, { childList: true, subtree: true });
            }
        </script>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    if "suggested_question" in st.session_state:
        input_prompt = st.session_state["suggested_question"]
        del st.session_state["suggested_question"]
    else:
        input_prompt = st.chat_input("Ask a question about the PDF...")
    
    # Handle user input and AI response
    if input_prompt:
        # Display user message
        st.markdown(f"""
        <div class="chat-message-container user">
            <div class="user-bubble">
                {input_prompt}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state["messages"].append({"role": "user", "content": input_prompt})
        
        # Generate AI response
        with st.spinner("🤔 Thinking..."):
            try:
                # Set up the LLM
                llm = Together(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    temperature=0.7,
                    max_tokens=1500,
                    together_api_key="b68f2588587cb665eb94e89cff6ddafce235a0c570566909f9049fc4837d64be"
                )
                
                # Create retriever from vector store
                retriever = st.session_state["vectordb"].as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 6}
                )
                
                # Enhanced prompt for direct, detailed answers
                prompt_template = """
<s>[INST]You are an expert assistant analyzing a PDF document. Provide a **detailed response** in your own formed sentences directly addressing the user's question.

Instructions:
- Do **not** write the answer as one big paragraph.
- Use **bullet points** or **clear, separate paragraphs** for each idea.
- Avoid headings like "Conclusion", "Overview", etc.
- Explain the answers to me instead of just dumping the facts
- Explain each idea with enough depth, using information from the PDF.

In each point or paragraph, make sure to include:
• Important details and key points, supporting facts and evidence, additional context and insights, relevant examples and explanations, and complete information in a well-organized manner.

Respond in a helpful and natural tone. Focus only on the context provided.

CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""

                
                prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])
                
                # Create conversational chain
                qa = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    memory=st.session_state["memory"],
                    retriever=retriever,
                    combine_docs_chain_kwargs={'prompt': prompt}
                )
                
                # Get response
                result = qa.invoke(input=input_prompt)
                response = result["answer"]
                
                # Display AI response
                st.markdown(f"""
                <div class="chat-message-container assistant">
                    <div class="assistant-bubble">
                        {response}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state["messages"].append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})

else:
    # Welcome section when no PDF is uploaded - using Streamlit native components
  st.markdown("""
<div style="text-align: center; padding: 40px 20px; background: #2b2b2b; border-radius: 15px; margin: 20px 0; box-shadow: 0 8px 32px rgba(255,255,255,0.1); border: 2px dashed #667eea;">
<h1 style="color: #ffffff; margin-bottom: 15px; font-size: 32px; font-weight: 700;">Welcome to BookBot! 📚</h1>
<p style="color: #cccccc; font-size: 18px; margin-bottom: 30px;">Upload a PDF document to start asking questions about it.</p>

<div style="text-align: left; max-width: 600px; margin: 0 auto;">
<h3 style="color: #ffffff; margin-bottom: 15px; font-size: 20px;">Features:</h3>
<div style="color: #dddddd; font-size: 16px; line-height: 1.8;">
<div style="margin-bottom: 10px;">📄 <strong>Scrollable PDF viewer</strong> - View your document while chatting</div>
<div style="margin-bottom: 10px;">💬 <strong>Interactive chat interface</strong> - Ask questions naturally</div>
<div style="margin-bottom: 10px;">📋 <strong>Detailed, structured answers</strong> - Get comprehensive responses</div>
<div style="margin-bottom: 10px;">🔍 <strong>Click to show answers in PDF context</strong> - See where answers come from</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)






# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.7); padding: 20px 0;">
    <p>📚 BookBot - Your AI-Powered PDF Assistant | 💬 Ask questions about any document!</p>
</div>
""", unsafe_allow_html=True)
