🎓 StudyBuddy AI Pro
Advanced Generative AI Academic Assistant  Infosys SkillsBuild Internship Final Project
StudyBuddy AI Pro is a high-performance educational dashboard that leverages Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to transform static study materials into interactive learning experiences. Designed for students, educators, and professionals, it provides summaries, quizzes, flashcards, and productivity tools—all powered by cutting-edge AI.

🚀 Features
- Multi-Format Processing
Upload and process PDF, DOCX, PPTX, images (OCR), and plain text files.
- Executive Summary Hub
Generate structured, high-retention overviews with academic typography.
- Interactive Quiz Engine
Create custom MCQs from uploaded content to validate understanding.
- Active Recall Flashcards
Use vertically-aligned flashcards for terminology mastery.
- Real-Time Focus Timer
Track study sessions with a browser-side JavaScript timer.

🧪 Quick Demo Mode
Mentors and HR representatives can evaluate the app instantly without setup:
- Launch the live deployment link.
- Click 🚀 View Live Demo on the landing page.
- Access preloaded modules (Summary, Quiz, Flashcards) with sample Object-Oriented Programming content.
- Run `pip install -r requirements.txt` to install dependencies.

📂 Using Your Own Materials
To unlock full functionality with your study materials:
Local Setup
- Create a folder named .streamlit in the project root.
- Inside, add a file secrets.toml with your Gemini API key:
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"


⚠️ Security Note: Never commit .streamlit to GitHub.

Cloud Setup
- In Streamlit Community Cloud, go to Settings → Secrets.
- Paste the same GOOGLE_API_KEY line and save.
Upload files via the sidebar to generate summaries, quizzes, and flashcards in real time.

🛠 Tech Stack & Architecture
- LLM Engine: Google Gemini 3 Flash (optimized for speed & accuracy)
- Vector Database: FAISS for efficient in-memory retrieval
- Orchestration: LangChain (RetrievalQA, Recursive Text Splitting)
- UI/UX: Streamlit with premium CSS (Inter & Merriweather typography)

📚 Learning Modules
- 📄 Summary Hub – Context-aware executive overviews
- 🧠 Quiz Engine – AI-generated MCQs for retention checks
- ⚡ Flashcard Lab – Active recall cards for terminology mastery
- ⏱ Focus Timer – Real-time productivity tracking

⚙️ Installation & Setup
- Clone the Repository
git clone https://github.com/saharsh8/AI-Study-Buddy-Pro.git
cd AI-Study-Buddy-Pro
- Install Dependencies
pip install -r requirements.txt
- Configure API Credentials
- Create .streamlit/secrets.toml
- Add:
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
- Run the Application
streamlit run app.py



👨‍💻 About the Developer
Developed by Saharsh Srivastava as part of the Infosys SkillsBuild Internship Program.
This project demonstrates full-stack Python development, AI integration, and professional UI/UX design.

📜 License
This project is licensed under the [Looks like the result wasn't safe to show. Let's switch things up and try something else!].

🔑 Improvements Made
- Structured sections (Features, Demo, Setup, Tech Stack, Modules, Installation, License).
- Recruiter-friendly language emphasizing technical depth and professional polish.
- Clear step-by-step instructions with code blocks.
- Security best practices highlighted.
- Consistent formatting with icons for readability.
