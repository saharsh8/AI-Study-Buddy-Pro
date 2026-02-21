import streamlit as st
import os
import time
import streamlit.components.v1 as components

# 1. CORE IMPORTS
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

# 2. PREMIUM UI STYLING
st.set_page_config(page_title="Infosys Internship: StudyBuddy AI", page_icon="🎓", layout="wide")

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
    }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s ease; }
    [data-testid="stSidebar"] img { display: block; margin: 0 auto 10px auto; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE
state_defaults = {
    'vector_store': None, 'summary_text': None, 'quiz_active': False, 
    'quiz_data': [], 'current_q': 0, 'flashcards': [], 
    'card_idx': 0, 'card_flipped': False, 'file_ready': False
}
for key, val in state_defaults.items():
    if key not in st.session_state: st.session_state[key] = val

# 4. SIDEBAR (With Live JavaScript Timer)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=70)
    st.title("Study Console")
    
    # Live Timer Alternative (JavaScript based)
    st.subheader("⏱️ Live Focus Timer")
    components.html("""
        <div id="timer" style="color: #4F46E5; font-size: 24px; font-family: sans-serif; font-weight: bold; text-align: center; background: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155;">
            00:00:00
        </div>
        <script>
            var seconds = 0;
            function updateTimer() {
                seconds++;
                var hrs = Math.floor(seconds / 3600);
                var mins = Math.floor((seconds - (hrs * 3600)) / 60);
                var secs = seconds % 60;
                document.getElementById('timer').innerHTML = 
                    (hrs < 10 ? "0" + hrs : hrs) + ":" + 
                    (mins < 10 ? "0" + mins : mins) + ":" + 
                    (secs < 10 ? "0" + secs : secs);
            }
            setInterval(updateTimer, 1000);
        </script>
    """, height=70)
    
    st.divider()
    uploaded_file = st.file_uploader("Upload Material", type=["pdf", "txt", "md", "docx", "pptx", "jpg", "png", "jpeg"])
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 5. DATA PROCESSING (Gated for stability)
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
        status.update(label="✅ Success! Document Analyzed.", state="complete", expanded=False)
        st.balloons()
        st.rerun()

# 6. MAIN INTERFACE
if not st.session_state.file_ready:
    st.markdown('<div class="hero-text">', unsafe_allow_html=True)
    st.title("🎓 StudyBuddy AI Pro")
    st.subheader("Transform documents into a professional learning experience.")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="pro-card"><h3>📄 Summaries</h3><p>Extract core concepts and bold takeaways in seconds.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pro-card"><h3>🧠 Quizzes</h3><p>Challenge yourself with AI-generated interactive MCQs.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pro-card"><h3>⚡ Recall</h3><p>Master terminology with vertical active recall cards.</p></div>', unsafe_allow_html=True)
    st.info("👈 **Get Started:** Upload your study material in the sidebar to begin.")

else:
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=st.session_state.vector_store.as_retriever())
    
    tab1, tab2, tab3 = st.tabs(["📄 Summary Hub", "🧠 Quiz Engine", "⚡ Flashcard Lab"])

    with tab1:
        if not st.session_state.summary_text:
            st.markdown('<div class="pro-card"><h3>Executive Summary</h3><p>Generate a professional overview of your document.</p></div>', unsafe_allow_html=True)
            _, col, _ = st.columns([1, 1, 1])
            if col.button("✨ Generate AI Summary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    res = qa.invoke("Provide a professional summary with clear bold headers.")
                    st.session_state.summary_text = res["result"]
                    st.rerun()
        else:
            st.markdown(f'<div class="result-box">{st.session_state.summary_text}</div>', unsafe_allow_html=True)
            st.download_button("💾 Export Summary", st.session_state.summary_text, file_name="Summary.txt")

    with tab2:
        if not st.session_state.quiz_active:
            st.markdown('<div class="pro-card"><h3>Interactive MCQs</h3><p>Test your material retention with AI-designed questions.</p></div>', unsafe_allow_html=True)
            _, col, _ = st.columns([1, 1, 1])
            if col.button("🎲 Build Quiz", use_container_width=True):
                with st.spinner("Designing Quiz..."):
                    prompt = "Create 3 MCQs. Format strictly: Q: [Q] | A) [O] | B) [O] | C) [O] | Correct: [Letter]"
                    raw = qa.invoke(prompt)["result"]
                    parsed = []
                    for line in raw.strip().split('\n'):
                        parts = line.split('|')
                        if len(parts) >= 5:
                            parsed.append({"q": parts[0].replace("Q:", "").strip(), "opts": [parts[1].strip(), parts[2].strip(), parts[3].strip()], "ans": parts[4].replace("Correct:", "").strip()})
                    st.session_state.quiz_data = parsed
                    st.session_state.quiz_active = True
                    st.rerun()
        else:
            idx = st.session_state.current_q
            if idx < len(st.session_state.quiz_data):
                item = st.session_state.quiz_data[idx]
                st.markdown(f"#### Question {idx+1}: {item['q']}")
                choice = st.radio("Select Answer:", item["opts"], key=f"q_{idx}")
                if st.button("Submit Answer", use_container_width=True):
                    if choice[0] == item["ans"]: st.success("Correct!")
                    else: st.error(f"Incorrect. Answer was {item['ans']}")
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                st.success("Quiz Completed!")
                if st.button("Restart Quiz"):
                    st.session_state.quiz_active = False
                    st.rerun()

    with tab3:
        if not st.session_state.flashcards:
            st.markdown('<div class="pro-card"><h3>Vertical Flashcards</h3><p>Master terminology with active recall cards.</p></div>', unsafe_allow_html=True)
            _, col, _ = st.columns([1, 1, 1])
            if col.button("🗂️ Generate Cards", use_container_width=True):
                with st.spinner("Extracting..."):
                    prompt = "Extract 5 terms. Format: TERM: [Name] | DEF: [Explanation]"
                    res = qa.invoke(prompt)["result"]
                    cards = []
                    for line in res.strip().split('\n'):
                        if " | " in line:
                            parts = line.split(" | ")
                            cards.append({"term": parts[0].replace("TERM:","").strip(), "dfn": parts[1].replace("DEF:","").strip()})
                    st.session_state.flashcards = cards
                    st.rerun()
        else:
            c_idx = st.session_state.card_idx
            card = st.session_state.flashcards[c_idx]
            header = "Definition" if st.session_state.card_flipped else "Term"
            content = card["dfn"] if st.session_state.card_flipped else card["term"]
            _, col, _ = st.columns([1, 1.5, 1])
            with col:
                st.markdown(f'<div class="vertical-flashcard"><h3>{header}</h3><hr><p>{content}</p></div>', unsafe_allow_html=True)
                n1, n2, n3 = st.columns([1, 1, 1])
                with n1:
                    if st.button("⬅️", disabled=(c_idx == 0), use_container_width=True): 
                        st.session_state.card_idx -= 1; st.session_state.card_flipped = False; st.rerun()
                with n2:
                    if st.button("🔄", use_container_width=True): 
                        st.session_state.card_flipped = not st.session_state.card_flipped; st.rerun()
                with n3:
                    if st.button("➡️", disabled=(c_idx == len(st.session_state.flashcards)-1), use_container_width=True): 
                        st.session_state.card_idx += 1; st.session_state.card_flipped = False; st.rerun()