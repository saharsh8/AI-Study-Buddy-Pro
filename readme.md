# 🎓 StudyBuddy AI Pro
**Advanced Generative AI Academic Assistant | Infosys SkillsBuild Internship Final Project**

StudyBuddy AI Pro is a high-performance educational dashboard that leverages **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** to transform static study materials into interactive learning experiences.

---

## 🚀 Key Features

* **Multi-Format Processing:** Seamlessly handles PDF, DOCX, PPTX, Images (OCR), and Text files.
  
* **Executive Summary Hub:** Generates structured, high-retention overviews with premium academic typography.
  
* **Interactive MCQ Engine:** Designs custom quizzes based on uploaded content to validate understanding.
  
* **Active Recall Flashcards:** Features a vertically-aligned, centered card lab for terminology mastery.
  
* **Real-Time Sync Timer:** A browser-side JavaScript timer that tracks study sessions without UI lag.

---

🎓 StudyBuddy AI Pro
Advanced Generative AI Academic Assistant | Infosys Internship Final Project


StudyBuddy AI Pro is a production-grade educational dashboard that utilizes Retrieval-Augmented Generation (RAG) to transform static documents into dynamic, interactive learning modules.


🧪 Quick Evaluation (Demo Mode)

Mentors and HR representatives can evaluate the application instantly without any technical setup or API keys.

Launch the App: Open the live deployment link.

Activate Demo: Click the "🚀 View Live Demo" button on the landing page.

Immediate Access: This unlocks the Summary, Quiz, and Flashcard modules populated with high-quality sample data regarding Object-Oriented Programming.

📂 Full Functionality: How to Upload Materials

To use the AI with your own study materials, follow these steps to link your Google Gemini API Key:


1. Local Configuration (Development)
   
   -Create a folder named **.streamlit** in the project root.

   -Inside that folder, create a file named ** secrets.toml.**

   -Add your Gemini API key in this exact format:

   -Ini, TOML

    **GOOGLE_API_KEY = "YOUR_API_KEY_HERE"**
   
   Security Note: Do not commit the .streamlit folder to GitHub to keep your key private.

3. Cloud Configuration (Deployment)

   -In the Streamlit Community Cloud dashboard, navigate to Settings > Secrets.

   -Paste the same GOOGLE_API_KEY = "..." line into the secrets text area and save.

4. Usage

   -Once configured, use the sidebar to upload PDF, DOCX, PPTX, or Image files.

   -The system will automatically process the knowledge base for real-time interaction.



🛠️ Tech Stack & Architecture

   -LLM Engine: Google Gemini 3 Flash (Optimized for speed and accuracy).


   -Vector Database: FAISS (Facebook AI Similarity Search) for efficient in-memory retrieval.


   -Orchestration: LangChain (RetrievalQA and Recursive Text Splitting).


   -UI/UX: Streamlit with premium CSS (Inter and Merriweather typography).


🚀 Key Learning Modules

   📄 Summary Hub: Context-aware executive overviews of dense materials.
   

   🧠 Quiz Engine: AI-generated MCQs to validate retention and understanding.
   

   ⚡ Flashcard Lab: Vertically-centered active recall cards for terminology mastery.
   

   ⏱️ Focus Timer: A real-time JavaScript-driven study timer for productivity tracking.

   
## ⚙️ Installation & Setup

1. **Clone the Project:**
   ```bash
   git clone [https://github.com/your-username/StudyBuddy-AI-Pro.git](https://github.com/your-username/StudyBuddy-AI-Pro.git)
   cd StudyBuddy-AI-Pro


2 **Install Dependencies: **
  ```bash
  pip install -r requirements.txt


3 **Configure Environment:**

 -Create a .streamlit/secrets.toml file.

 -Add your API Key: GOOGLE_API_KEY = "YOUR_KEY_HERE".

4 **Configure API Credentials**
   -The application requires a Google Gemini API Key to function.

   -Create a folder named .streamlit in the project root.

   -Inside that folder, create a file named secrets.toml.

**Add your key in the following format:
Ini, TOML
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"**


5 **Launch Application:**
  ```bash
  streamlit run app.py


💡 About the Developer

Developed by SAHARSH SRIVASTAVA as part of the Infosys Internship Program.
This project demonstrates competency in Full-Stack Python development, AI integration, and professional UI/UX design.
