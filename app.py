import streamlit as st
import os
import time
import streamlit.components.v1 as components

# 1. CORE IMPORTS
try:
    from langchain_classic.chains import RetrievalQA 
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    st.error("🚀 Missing libraries! Ensure requirements.txt is correct.")
    st.stop()

# 2. UI STYLING
st.set_page_config(page_title="StudyBuddy AI Pro", page_icon="🎓", layout="wide")
st.markdown("<style>.stApp { background: #0f172a; } .result-box { background-color: #1e293b; padding: 25px; border-radius: 12px; border-left: 6px solid #4F46E5; color: #f1f5f9; }</style>", unsafe_allow_html=True)

# 3. SESSION STATE
if 'vector_store' not in st.session_state: st.session_state.vector_store = None
if 'summary_text' not in st.session_state: st.session_state.summary_text = None
if 'file_ready' not in st.session_state: st.session_state.file_ready = False

# 4. SIDEBAR
with st.sidebar:
    st.title("Study Console")
    uploaded_file = st.file_uploader("Upload Material", type=["pdf", "txt", "docx", "pptx"])
    if st.button("🔄 Reset Session"):
        st.session_state.clear()
        st.rerun()

# 5. DATA PROCESSING (The Quota Fix)
if uploaded_file and not st.session_state.file_ready:
    with st.status("🚀 Processing Knowledge Base...", expanded=True) as status:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
        
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == "pdf": loader = PyPDFLoader(file_path)
        elif ext == "docx": loader = UnstructuredWordDocumentLoader(file_path)
        elif ext == "pptx": loader = UnstructuredPowerPointLoader(file_path)
        else: loader = TextLoader(file_path)
        
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(data)
        
        # Using a reliable embedding model
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=st.secrets["GOOGLE_API_KEY"]
        )
        
        st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
        st.session_state.file_ready = True
        os.remove(file_path)
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        st.balloons()
        time.sleep(2) 
        st.rerun()

# 6. MAIN INTERFACE
if st.session_state.file_ready:
    st.success("✅ **Study Session Active.**")
    
    # SWITCHED TO 1.5 FLASH: Higher free-tier quota than 2.0
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest", 
        google_api_key=st.secrets["GOOGLE_API_KEY"], 
        temperature=0.3
    )
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=st.session_state.vector_store.as_retriever())

    if st.button("✨ Generate AI Summary", use_container_width=True):
        with st.spinner("Analyzing... (Rate limits may apply)"):
            try:
                time.sleep(1) # Pre-emptive 1s delay to prevent 429 errors
                res = qa.invoke("Provide a professional academic summary with bold headers.")
                st.session_state.summary_text = res["result"]
                st.rerun()
            except Exception as e:
                st.error("⚠️ Server Busy: Please wait 60 seconds and try again. This is a Google Free-Tier limit.")
            
    if st.session_state.summary_text:
        st.markdown(f'<div class="result-box">{st.session_state.summary_text}</div>', unsafe_allow_html=True)
else:
    st.title("🎓 StudyBuddy AI Pro")
    st.info("Please upload a document in the sidebar to begin.")
