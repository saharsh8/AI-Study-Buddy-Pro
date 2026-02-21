# 🎓 StudyBuddy AI Pro - Professional Academic Assistant
Infosys Internship Completion Project

StudyBuddy AI Pro is a sophisticated, Generative AI-powered educational platform designed to enhance learning productivity. It leverages Large Language Models (LLMs) to transform static documents into interactive study modules, featuring real-time analysis and active recall tools.

---

## 🚀 Technical Highlights & "Value Additions"
During the final phase of development, the following production-grade features were implemented to ensure a superior user experience:

* **Multi-Format Processing Engine:** Unlike standard RAG applications, this tool supports PDF, DOCX, PPTX, TXT, MD, and image-based notes (JPG/PNG) using specialized document loaders.
* **Synchronized Real-Time Timer:** A custom JavaScript-based focus timer that maintains precision even during heavy AI processing tasks.
* **Interactive Active Recall Lab:** A specialized vertical flashcard system designed for terminal-based memorization and long-term retention.
* **State-Gated UI Architecture:** Implemented advanced session state management to eliminate UI flickering and ensure a glitch-free user interface.
* **Exportable Insights:** One-click functionality to download AI-generated summaries for offline study.

---

## 🛠️ Tech Stack & Architecture
* **Core Model:** Google Gemini 3 Flash (State-of-the-art Generative AI).
* **Orchestration:** LangChain (RetrievalQA and Document Routing).
* **Vector Store:** FAISS (Facebook AI Similarity Search) for high-speed semantic retrieval.
* **Frontend:** Streamlit (Custom CSS injected for a premium SaaS aesthetic).

---

## ⚙️ Installation & Setup

1. **Clone the Project:**
   ```bash
   git clone [https://github.com/your-username/StudyBuddy-AI-Pro.git](https://github.com/your-username/StudyBuddy-AI-Pro.git)
   cd StudyBuddy-AI-Pro


2.Install Dependencies: 
  ```bash
  pip install -r requirements.txt


3.Configure Environment:

 .Create a .streamlit/secrets.toml file.

 .Add your API Key: GOOGLE_API_KEY = "YOUR_KEY_HERE".


4.Launch Application:
  ```bash
  streamlit run app.py


💡 About the Developer

   Developed by SAHARSH SRIVASTAVA as part of the Infosys Internship Program. This project demonstrates competency in Full-Stack Python development, AI integration, and professional UI/UX design.
