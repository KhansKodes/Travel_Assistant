<<<<<<< HEAD
=======
<<<<<<< HEAD
# Travel-Assistant
=======
>>>>>>> 1a1896c (Initial commit of Travel Assistant project)
# Travel Assistant Chatbot - Complete Project

## Project Structure
```
travel-chatbot/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── firebase_config.py
│   ├── openai_service.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── firebase_key.json (you'll need to add this)
└── README.md
```

## Backend Files

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
firebase-admin==6.2.0
openai==1.3.7
python-dotenv==1.0.0
pydantic==2.5.0
python-multipart==0.0.6
```


### 2. Firebase Setup
1. Go to Firebase Console (https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Go to Project Settings > Service Accounts
4. Generate a new private key
5. Save the JSON file as `firebase_key.json` in the root directory

### 3. OpenAI Setup
1. Get your OpenAI API key from https://platform.openai.com/
2. Create a `.env` file in the backend folder
3. Add your API key: `OPENAI_API_KEY=your_api_key_here`

### 4. Run the Application
```bash
cd backend
python main.py
```

### 5. Access the Chatbot
Open your browser and go to: http://localhost:8000

## Features

✅ **Travel-focused AI Assistant** using GPT-3.5 Turbo
✅ **Conversational Memory** with Firebase Firestore
✅ **Simple Web Interface** with modern design
✅ **Real-time Chat** with typing indicators
✅ **User Session Management** with local storage
✅ **Responsive Design** for mobile and desktop
✅ **Error Handling** and loading states
✅ **RESTful API** with FastAPI
✅ **CORS Support** for frontend integration

## API Endpoints

- `GET /` - Serve frontend
- `POST /chat` - Send message and get response
- `GET /conversation/{user_id}` - Get conversation history
- `GET /health` - Health check

The chatbot specializes in travel assistance and can help with:
- Destination recommendations
- Trip planning
- Travel logistics
- Activity suggestions
- Budget planning
- Travel tips and safety
<<<<<<< HEAD
- And much more! 
=======
- And much more! 
>>>>>>> cafafa2 (Initial commit of Travel Assistant project)
>>>>>>> 1a1896c (Initial commit of Travel Assistant project)
