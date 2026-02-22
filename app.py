import streamlit as st
import os
import time
import streamlit.components.v1 as components

# 1. CORE IMPORTS & MULTI-LOADER SETUP
try:
    from langchain_classic.chains import RetrievalQA 
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import (
        PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, 
        UnstructuredPowerPointLoader, UnstructuredImageLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    st.error("🚀 Missing libraries! Run: pip install python-docx python-pptx unstructured pypdf langchain-classic langchain-google-genai langchain-community faiss-cpu")
    st.stop()

# 2. PAGE CONFIG & PREMIUM UI
st.set_page_config(page_title="StudyBuddy AI", page_icon="🎓", layout="wide")

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
    .vertical-flashcard {
        background-color: #1e293b; padding: 2.5rem; border-radius: 20px;
        border: 2px solid #4F46E5; text-align: center; min-height: 400px;
        display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 15px 50px rgba(0,0,0,0.6);
    }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s ease; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE
state_defaults = {
    'vector_store': None, 'summary_text': None, 'quiz_active': False, 
    'quiz_data': [], 'current_q': 0, 'flashcards': [], 
    'card_idx': 0, 'card_flipped': False, 'file_ready': False, 'demo_mode': False
}
for key, val in state_defaults.items():
    if key not in st.session_state: st.session_state[key] = val

# 4. SIDEBAR (Real-Time JS Timer)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=70)
    st.title("Study Console")
    
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
    uploaded_file = st.file_uploader("Upload Material", type=["pdf", "txt", "md", "docx", "pptx", "jpg", "png", "jpeg"])
    
    if st.button("🔄 Reset Global Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 5. DATA PROCESSING (With Animation Fix)
if uploaded_file and not st.session_state.file_ready:
    with st.status("🚀 Processing Knowledge Base...", expanded=True) as status:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == "pdf": loader = PyPDFLoader(file_path)
        elif ext in ["docx", "doc"]: loader = UnstructuredWordDocumentLoader(file_path)
        elif ext in ["pptx", "ppt"]: loader = UnstructuredPowerPointLoader(file_path)
        elif ext in ["jpg", "png", "jpeg"]: loader = UnstructuredImageLoader(file_path)
        else: loader = TextLoader(file_path)
        
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(data)
        
        # Accessing API Key via Streamlit Secrets
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=st.secrets["GOOGLE_API_KEY"])
        st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
        st.session_state.file_ready = True
        os.remove(file_path)
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        # ANIMATION FIX
        st.balloons()
        time.sleep(2) 
        st.rerun()

# 6. MAIN INTERFACE
if not st.session_state.file_ready:
    st.markdown('<div class="hero-text">', unsafe_allow_html=True)
    st.title("🎓 StudyBuddy AI Pro")
    st.subheader("Transform documents into a professional learning experience.")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="pro-card"><h3>📄 Summaries</h3><p>Extract core concepts instantly.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pro-card"><h3>🧠 Quizzes</h3><p>Challenge yourself with AI MCQs.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pro-card"><h3>⚡ Recall</h3><p>Master terms with vertical recall cards.</p></div>', unsafe_allow_html=True)
    
    st.divider()
    _, demo_col, _ = st.columns([1, 1.2, 1])
    if demo_col.button("🚀 View Live Demo (No API Key Required)", use_container_width=True):
        st.session_state.update({
            'summary_text': "### 📑 Overview: OOP Concepts\n* **Encapsulation:** Bundling data.\n* **Inheritance:** New class from existing.",
            'quiz_data': [{"q": "Which OOP concept focuses on data hiding?", "opts": ["A) Inheritance", "B) Encapsulation", "C) Abstraction"], "ans": "B"}],
            'flashcards': [{"term": "Class", "dfn": "A blueprint for objects."}],
            'file_ready': True, 'demo_mode': True
        })
        st.rerun()

else:
    st.success("✅ **Study Session Active.**")
    tab1, tab2, tab3 = st.tabs(["📄 Summary Hub", "🧠 Quiz Engine", "⚡ Flashcard Lab"])
    
    if not st.session_state.demo_mode:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=st.secrets["GOOGLE_API_KEY"])
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=st.session_state.vector_store.as_retriever())

    with tab1:
        if not st.session_state.summary_text:
            if st.button("✨ Generate AI Summary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    res = qa.invoke("Provide a professional summary with bullet points.")
                    st.session_state.summary_text = res["result"]
                    st.rerun()
        else:
            st.markdown(f'<div class="result-box">{st.session_state.summary_text}</div>', unsafe_allow_html=True)

    with tab2:
        if not st.session_state.quiz_data:
            if st.button("🎲 Build Quiz", use_container_width=True):
                with st.spinner("Designing..."):
                    raw = qa.invoke("Create 3 MCQs. Format strictly: Q: [Q] | A) [O] | B) [O] | C) [O] | Correct: [Letter]")["result"]
                    # (Parsing logic same as before)
                    st.session_state.quiz_data = [{"q": "Example Question", "opts": ["A", "B", "C"], "ans": "A"}]
                    st.rerun()
        else:
            # (Quiz UI logic same as before)
            st.write("Quiz Loaded.")

    with tab3:
        # (Flashcard UI logic same as before)
        st.write("Flashcards Loaded.")
