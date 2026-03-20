#  EDU_CHAT: AI-Powered Study Assistant
**A HACK-ATTACK PROJECT**

EDU_CHAT is an intelligent, context-aware educational chatbot designed to help students study more effectively. By combining standard PDF parsing, optical character recognition (OCR), advanced token compression, and the Gemini 2.5 Flash model, EDU_CHAT can read textbooks and answer student questions with high accuracy and low latency.

---

##  Key Features

###  Advanced AI & Processing Pipeline
* **Context-Aware Q&A:** Uses Google's Gemini 2.5 Flash API to answer questions based strictly on the selected textbook context and the current conversation history.
* **Token Compression (ScaleDown API):** Intelligently compresses massive textbook chapters before sending them to the LLM. Includes a real-time UI widget showing the original tokens, compressed tokens, and compression ratio.
* **Universal File Extractor:** Built-in Python engine (`PyMuPDF`) for lightning-fast standard PDF reading.
* **Automated OCR Fallback:** Automatically detects scanned PDFs or images and routes them through `Tesseract OCR` to extract text. 
* **Smart Caching System:** Saves processed PDF/OCR text as local `.txt` files with robust Unicode error handling (`errors='replace'`). Subsequent queries load instantly without re-running heavy extraction tasks.

###  Multimodal Input
* **Speech-to-Text (Voice Input):** Integrated Web Speech API allows students to ask questions using their microphone. Features a pulsing recording animation and is optimized for Indian English (`en-IN`) for high accuracy.
* **Attachment UI:** A sleek, animated `+` menu allowing users to select local files or open their device camera to snap photos of textbook pages (Frontend UI implemented, ready for backend routing).

###  Premium User Interface
* **Hackathon Splash Screen:** A timed, 2.5-second dark glassmorphism welcome screen featuring a floating logo, deep indigo gradient, and a pulsing neon "HACK-ATTACK PROJECT" animation.
* **Light / Dark Theme Toggle:** A single-click toggle that seamlessly switches the app from a dark slate theme to a clean light theme. Remembers user preference using browser `localStorage`.
* **Glassmorphism Authentication:** Beautifully designed Login and Registration pages featuring blurred semi-transparent cards, interactive input fields with floating glows, and animated backgrounds.
* **Real-time Chat UX:** Features smooth fade-in animations, "typing..." indicator bouncing dots, auto-scrolling, and formatted Markdown rendering for AI responses.

###  Session Management
* **Dynamic Sidebar:** Automatically logs chat history. Users can jump between different subjects and classes, and the app will reload the exact context and conversation history.
* **Database Integration:** Securely stores Users, Textbooks, Chat Sessions, and Chat Messages using SQLAlchemy.

---

##  Tech Stack

**Frontend:**
* HTML5, CSS3 (Custom variables, Keyframe animations, Glassmorphism)
* Vanilla JavaScript (Web Speech API, Fetch API, DOM manipulation)
* FontAwesome Icons

**Backend:**
* Python 3 & Flask (RESTful API routing)
* SQLAlchemy (Database ORM)
* PyMuPDF (`fitz`) & Pillow (`PIL`) (Document processing)
* Tesseract OCR (`pytesseract`) (Image-to-text conversion)

**AI & APIs:**
* Google GenAI (Gemini 2.5 Flash)
* ScaleDown API (Context compression)

---

##  Installation & Setup
.env content:
SCALEDOWN_API_KEY=API KEY.
GEMINI_API_KEY=API KEY.
DATABASE_URL=mysql+pymysql://USER:PASSWORD:PORT/DATABASE_NAME.

### 1. Prerequisites
* Python 3.8+
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.
  * *Windows users:* Update the `tesseract_cmd` path in `pdf_helper.py` to match your installation (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`).

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/edu-chat-assistant.git](https://github.com/YOUR_USERNAME/edu-chat-assistant.git)
cd edu-chat-assistant
