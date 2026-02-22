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

# 2. PAGE CONFIG & PREMIUM TYPOGRAPHY
st.set_page_config(page_title="StudyBuddy AI", page_icon="🎓", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Merriweather:ital,wght@0,400;0,700&display=swap" rel="stylesheet">
    <style>
    .stApp { background: #0f172a; font-family: 'Inter', sans-serif; }
    .hero-text { text-align: center; padding: 40px 0; }
    .pro-card {
        background-color: #1e293b; padding: 30px; border-radius: 15px;
        border: 1px solid #4F46E5; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: #f1f5f9; margin-bottom: 25px; text-align: center;
    }
    .result-box {
        background-color: #1e293b; padding: 35px; border-radius: 16px;
        border-left: 8px solid #6366f1; line-height: 2;
        font-family: 'Merriweather', serif; font-size: 1.15rem;
        color: #e2e8f0; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .vertical-flashcard {
        background-color: #1e293b; padding: 3rem; border-radius: 24px;
        border: 2px solid #6366f1; display: flex; flex-direction: column;
        align-items: center; justify-content: center; text-align: center;
        min-height: 450px; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    .vertical-flashcard h3 {
        font-family: 'Inter', sans-serif; text-transform: uppercase;
        letter-spacing: 0.1em; font-size: 0.9rem; color: #818cf8; margin-bottom: 1.5rem;
    }
    .vertical-flashcard p {
        font-family: 'Merriweather', serif; font-size: 1.6rem;
        font-weight: 700; color: #f1f5f9; margin: 0;
    }
    .stButton>button { border-radius: 12px; font-weight: 600; font-family: 'Inter', sans-serif; transition: 0.3s ease; }
    [data-testid="stSidebar"] img { display: block; margin: 0 auto 10px auto; border-radius: 10px; }
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
        <div id="timer" style="color: #4F46E5; font-size: 22px; font-family: 'Inter', sans-serif; font-weight: bold; text-align: center; background: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155;">00:00:00</div>
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

# 5. DATA PROCESSING (Gated with Balloon Animation Fix)
if uploaded_file and not st.session_state.file_ready:
    with st.status("🚀 Initializing Knowledge Base...", expanded=True) as status:
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
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)
        st.session_state.file_ready = True
        os.remove(file_path)
        status.update(label="✅ Success!", state="complete", expanded=False)
        
        # ANIMATION FIX: Pause briefly so the browser can render balloons
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
    with c1: st.markdown('<div class="pro-card"><h3>📄 Summaries</h3><p>Extract core concepts and takeaways instantly.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pro-card"><h3>🧠 Quizzes</h3><p>Validate retention with interactive AI MCQs.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pro-card"><h3>⚡ Recall</h3><p>Master terms with centered flashcards.</p></div>', unsafe_allow_html=True)
    
    st.divider()
    _, demo_col, _ = st.columns([1, 1.3, 1])
    if demo_col.button("🚀 View Live Demo (No API Key Required)", use_container_width=True):
        st.session_state.update({
            'summary_text': """### 📑 Overview: Object-Oriented Programming (OOP)

* **Encapsulation:** The bundling of data and methods into a single unit.
* **Inheritance:** A mechanism where a new class inherits properties from an existing class.
* **Polymorphism:** Allowing different classes to be treated as instances of the same superclass.
* **Abstraction:** Hiding complex implementation details to show only essential features.""",
            'quiz_data': [{"q": "Which OOP concept focuses on data hiding?", "opts": ["A) Inheritance", "B) Encapsulation", "C) Abstraction"], "ans": "B"}],
            'flashcards': [{"term": "Class", "dfn": "A blueprint or template for creating objects."}, {"term": "Object", "dfn": "A specific instance of a class."}],
            'file_ready': True, 'demo_mode': True
        })
        st.rerun()
    st.info("👈 **Upload a file** in the sidebar to begin your custom session.")

else:
    st.success("✅ **Study Session Active.**" if not st.session_state.demo_mode else "🚀 **Demo Mode Active.**")
    tab1, tab2, tab3 = st.tabs(["📄 Summary Hub", "🧠 Quiz Engine", "⚡ Flashcard Lab"])
    
    if not st.session_state.demo_mode:
        llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=st.session_state.vector_store.as_retriever())

    with tab1:
        if not st.session_state.summary_text:
            st.markdown('<div class="pro-card"><h3>Executive Summary</h3><p>Generate a professional overview of your document.</p></div>', unsafe_allow_html=True)
            if st.button("✨ Generate AI Summary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    res = qa.invoke("Provide a professional summary with clear bold headers and bullet points.")
                    st.session_state.summary_text = res["result"]
                    st.rerun()
        else:
            st.markdown(f'<div class="result-box">{st.session_state.summary_text}</div>', unsafe_allow_html=True)
            st.download_button("💾 Export Summary", st.session_state.summary_text, file_name="Summary.txt")

    with tab2:
        if not st.session_state.quiz_data:
            st.markdown('<div class="pro-card"><h3>Interactive MCQs</h3><p>Test your material retention with AI-designed questions.</p></div>', unsafe_allow_html=True)
            if st.button("🎲 Build Quiz", use_container_width=True):
                with st.spinner("Designing..."):
                    prompt = "Create 3 MCQs. Format strictly: Q: [Q] | A) [O] | B) [O] | C) [O] | Correct: [Letter]"
                    raw = qa.invoke(prompt)["result"]
                    parsed = []
                    for line in raw.strip().split('\n'):
                        parts = line.split('|')
                        if len(parts) >= 5: parsed.append({"q": parts[0].replace("Q:", "").strip(), "opts": [parts[1].strip(), parts[2].strip(), parts[3].strip()], "ans": parts[4].replace("Correct:", "").strip()})
                    st.session_state.quiz_data = parsed; st.rerun()
        else:
            idx = st.session_state.current_q
            if idx < len(st.session_state.quiz_data):
                item = st.session_state.quiz_data[idx]
                st.progress(idx / len(st.session_state.quiz_data))
                st.markdown(f"#### Question {idx+1}: {item['q']}")
                choice = st.radio("Select Answer:", item["opts"], key=f"q_{idx}")
                if st.button("Submit Answer", use_container_width=True):
                    if choice[0] == item["ans"]: st.success("Correct!")
                    else: st.error(f"Incorrect. Answer was {item['ans']}")
                    st.session_state.current_q += 1; st.rerun()
            else:
                st.success("Quiz Completed!"); st.button("Restart Quiz", on_click=lambda: st.session_state.update({'quiz_data': [], 'current_q': 0}))

    with tab3:
        if not st.session_state.flashcards:
            st.markdown('<div class="pro-card"><h3>Flashcards</h3><p>Master terminology with active recall.</p></div>', unsafe_allow_html=True)
            if st.button("🗂️ Generate Cards", use_container_width=True):
                with st.spinner("Extracting..."):
                    res = qa.invoke("Extract 5 terms. Format: TERM: [Name] | DEF: [Explanation]")["result"]
                    cards = []
                    for line in res.strip().split('\n'):
                        if " | " in line:
                            p = line.split(" | "); cards.append({"term": p[0].replace("TERM:","").strip(), "dfn": p[1].replace("DEF:","").strip()})
                    st.session_state.flashcards = cards; st.rerun()
        else:
            c_idx = st.session_state.card_idx; card = st.session_state.flashcards[c_idx]
            header = "Definition" if st.session_state.card_flipped else "Term"
            content = card["dfn"] if st.session_state.card_flipped else card["term"]
            _, col, _ = st.columns([1, 1.5, 1])
            with col:
                st.markdown(f'<div class="vertical-flashcard"><h3>{header}</h3><hr><p>{content}</p></div>', unsafe_allow_html=True)
                n1, n2, n3 = st.columns([1, 1, 1])
                if n1.button("⬅️", disabled=(c_idx == 0), use_container_width=True): 
                    st.session_state.card_idx -= 1; st.session_state.card_flipped = False; st.rerun()
                if n2.button("🔄", use_container_width=True): 
                    st.session_state.card_flipped = not st.session_state.card_flipped; st.rerun()
                if n3.button("➡️", disabled=(c_idx == len(st.session_state.flashcards)-1), use_container_width=True): 
                    st.session_state.card_idx += 1; st.session_state.card_flipped = False; st.rerun()
