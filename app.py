import streamlit as st
import os
import time
import streamlit.components.v1 as components

# 1. CORE IMPORTS & DEPENDENCY CHECK
try:
    from langchain_classic.chains import RetrievalQA 
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import (
        PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, 
        UnstructuredPowerPointLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    st.error("🚀 Missing libraries! Check your requirements.txt.")
    st.stop()

# 2. PREMIUM UI STYLING
st.set_page_config(page_title="StudyBuddy AI Pro", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .hero-text { text-align: center; padding: 40px 0; }
    .pro-card {
        background-color: #1e293b; padding: 30px; border-radius: 15px;
        border: 1px solid #4F46E5; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: #f1f5f9; margin-bottom: 25px; text-align: center;
    }
    .result-box {
        background-color: #1e293b; padding: 25px; border-radius: 12px;
        border-left: 6px solid #4F46E5; line-height: 1.8; color: #f1f5f9;
    }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s ease; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE
if 'vector_store' not in st.session_state: st.session_state.vector_store = None
if 'summary_text' not in st.session_state: st.session_state.summary_text = None
if 'file_ready' not in st.session_state: st.session_state.file_ready = False

# 4. SIDEBAR
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=70)
    st.title("Study Console")
    
    # Focus Timer
    components.html("""
        <div id="timer" style="color: #4F46E5; font-size: 22px; font-family: sans-serif; font-weight: bold; text-align: center; background: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155;">00:00:00</div>
        <script>
            var seconds = 0;
            setInterval(function(){
                seconds++;
                var h = Math.floor(seconds/3600), m = Math.floor((seconds%3600)/60), s = seconds%60;
                document.getElementById('timer').innerHTML = (h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+":"+(s<10?"0"+s:s);
            }, 1000);
        </script>
    """, height=70)
    
    st.divider()
    uploaded_file = st.file_uploader("Upload Study Material", type=["pdf", "txt", "docx", "pptx"])
    
    if st.button("🔄 Reset Global Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 5. DATA PROCESSING (Gated with Stable Model Fix)
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
        
        # KEY FIX: Using stable auto-updated embedding alias
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=st.secrets["GOOGLE_API_KEY"]
        )
        st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
        st.session_state.file_ready = True
        os.remove(file_path)
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        # Animation delay
        st.balloons()
        time.sleep(2) 
        st.rerun()

# 6. MAIN INTERFACE
if not st.session_state.file_ready:
    st.markdown('<div class="hero-text">', unsafe_allow_html=True)
    st.title("🎓 StudyBuddy AI Pro")
    st.subheader("Transform documents into professional summaries.")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="pro-card"><h3>📄 Summaries</h3><p>Extract core concepts.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pro-card"><h3>🧠 Quizzes</h3><p>Challenge yourself.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pro-card"><h3>⚡ Recall</h3><p>Master terms.</p></div>', unsafe_allow_html=True)
else:
    st.success("✅ **Study Session Active.**")
    
    # KEY FIX: Using the stable Gemini Flash alias to avoid 404
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=st.secrets["GOOGLE_API_KEY"], 
        temperature=0.3
    )
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=st.session_state.vector_store.as_retriever())

    if st.button("✨ Generate AI Summary", use_container_width=True):
        with st.spinner("Analyzing..."):
            res = qa.invoke("Provide a professional academic summary with bold headers and bullet points.")
            st.session_state.summary_text = res["result"]
            st.rerun()
            
    if st.session_state.summary_text:
        st.markdown(f'<div class="result-box">{st.session_state.summary_text}</div>', unsafe_allow_html=True)
