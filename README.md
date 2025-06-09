# Travel Assistant Chatbot

A modern, AI-powered travel assistant chatbot that helps users plan trips, get recommendations, and more. Built with FastAPI, Firebase, and OpenAI GPT-3.5 Turbo, featuring a sleek web interface.

---

## 🚀 Features

- **Travel-focused AI Assistant** (GPT-3.5 Turbo)
- **Conversational Memory** (Firebase Firestore)
- **Modern Web Interface** (Responsive, mobile-friendly)
- **Real-time Chat** with typing indicators
- **User Session Management** (local storage)
- **RESTful API** (FastAPI)
- **CORS Support** for frontend integration
- **Robust Error Handling** and loading states

---

## 🗂️ Project Structure

```
Travel Assistant/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── firebase_config.py
│   ├── openai_service.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Travel_Assistant.git
cd Travel_Assistant
```

### 2. Backend Setup

#### a. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### b. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (or use an existing one)
3. Go to **Project Settings > Service Accounts**
4. Generate a new private key
5. Save the JSON file as `backend/firebase_key.json` (do **not** commit this file)

#### c. OpenAI Setup

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Create a `.env` file in the `backend/` folder:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### 3. Run the Application

```bash
python main.py
```

### 4. Access the Chatbot

Open your browser and go to: [http://localhost:8000](http://localhost:8000)

---

## 📚 API Endpoints

- `GET /` — Serve frontend
- `POST /chat` — Send message and get AI response
- `GET /conversation/{user_id}` — Get conversation history
- `GET /health` — Health check

---

## 💡 Use Cases

- Destination recommendations
- Trip planning
- Travel logistics
- Activity suggestions
- Budget planning
- Travel tips and safety
---

