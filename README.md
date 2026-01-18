# 🎤 Voice Assistant Chatbot (Streamlit)

A **voice-enabled conversational assistant** built with **Streamlit**, supporting **speech-to-text (STT)**, **LLM-powered responses**, and **text-to-speech (TTS)**.
The application is designed to run reliably on **Render** and uses **OpenAI APIs** for transcription and response generation.

---

## 🌐 Live Application

The application is deployed on Render and can be accessed here:

👉 https://voice-assistant-chatbot-s3zk.onrender.com/

---

## ✨ Features

* 🎙️ **Speech-to-Text (STT)** using OpenAI Whisper
* 💬 **Conversational AI** powered by GPT models via LangChain
* 🔊 **Text-to-Speech (TTS)** output using Google Text-to-Speech
* 🌍 **Multi-language support** (STT + TTS)
* ⚙️ **Configurable settings** (language, accent, speech rate)
* 🗝️ **Secure API key handling** (session-based, not persisted)
* ☁️ **Render-compatible** (no local file dependencies)

---

## 🏗️ Project Structure

```
.
├── app.py                     # Main Streamlit application
├── transcript.py              # Speech-to-text (Whisper)
├── response.py                # LLM response generation
├── pages/
│   ├── 0_api_key_config.py    # API key configuration page
│   └── 1_settings.py          # Language & TTS settings
├── requirements.txt
└── README.md
```

**Core modules:**

* `app.py` – UI, chat flow, audio handling, session management 
* `response.py` – GPT-based response generation using LangChain 
* `transcript.py` – Audio transcription using OpenAI Whisper 
* `pages/0_api_key_config.py` – API key entry and validation 
* `pages/1_settings.py` – Language, accent, and speech rate controls 

---

## 🔐 API Key Handling

* Users provide their **OpenAI API key** via the UI
* The key is:

  * Stored **only in Streamlit session state**
  * **Never written to disk**
  * Automatically cleared when the session ends

This design is safe for **public Render deployments**.

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deploying on Render

### Render Configuration

**Service Type:** Web Service
**Environment:** Python
**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### Important Notes for Render

* Audio files are handled using **temporary files** (Render-compatible)
* No persistent storage is required
* Session-based state works correctly across requests

---

## ⚙️ Settings & Customization

From the **Settings** page, users can configure:

* 🌍 **Language** (English, French, Spanish, German, etc.)
* 🎙️ **TTS Accent** (US, UK, India, Australia, Canada)
* 🐢 **Speech Rate** (normal or slow)
* 🎤 Enable/disable **voice input**
* 🔊 Enable/disable **voice output**

All settings are stored in `st.session_state`.

---

## 🧠 Model Details

* **Speech-to-Text:** `whisper-1`
* **Chat Model:** `gpt-4o`
* **Temperature:** `0` (deterministic, concise responses)

Responses are intentionally limited to **3–5 sentences** for clarity and usability.

---

## 🧪 Known Limitations

* Requires a valid OpenAI API key per session
* TTS uses `gTTS`, which requires an active internet connection
* Concurrent users each need their own API key

---

## 📽️ Demo Video

A full demo walkthrough video is available here:

👉 https://gesivak21.github.io/MyPortfolio/projects/voice-assistant-demo.html

The demo covers:

* Voice input and speech-to-text
* Conversational responses
* Text-to-speech output
* Language and settings customization

---

## 🔒 Rights & Usage

All rights are reserved.

* No license is granted for reuse, redistribution, or modification
* Use of this codebase requires **explicit permission from the author**

## 👩‍💻 Author

**G. Siva Kumar** | 📧 [gesivak21@example.com](mailto:gesivak21@gmail.com) | 🌐 [GitHub](https://github.com/gesivak21/Portfolio)

