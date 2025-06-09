from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
from datetime import datetime
from typing import List

from models import ChatRequest, ChatResponse, Message, Conversation
from firebase_config import FirebaseService
from openai_service import OpenAIService

app = FastAPI(title="Travel Assistant Chatbot", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Initialize services
firebase_service = FirebaseService()
openai_service = OpenAIService()

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse("../frontend/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        print(f"DEBUG: Received chat request for user_id: {request.user_id}")
        print(f"DEBUG: Request message: {request.message}")
        
        # Get user's conversation history
        user_conversations = firebase_service.get_user_conversations(request.user_id)
        print(f"DEBUG: Found {len(user_conversations)} existing conversations")
        
        # Use the most recent conversation or create a new one
        if user_conversations:
            current_conversation = user_conversations[0]
            conversation_id = current_conversation['conversation_id']
            messages = current_conversation.get('messages', [])
            print(f"DEBUG: Using existing conversation {conversation_id} with {len(messages)} messages")
            print(f"DEBUG: Existing messages: {messages}")
        else:
            conversation_id = str(uuid.uuid4())
            messages = []
            print(f"DEBUG: Creating new conversation with ID: {conversation_id}")
        
        # Add user message
        user_message = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        }
        messages.append(user_message)
        print(f"DEBUG: Added user message: {user_message}")
        
        # Prepare messages for OpenAI (only role and content)
        openai_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages[-10:]]
        print(f"DEBUG: Sending to OpenAI: {openai_messages}")
        
        # Generate AI response
        ai_response = openai_service.generate_response(openai_messages)
        print(f"DEBUG: Received AI response: {ai_response}")
        
        # Add AI message
        ai_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        messages.append(ai_message)
        print(f"DEBUG: Added AI message: {ai_message}")
        
        # Save/update conversation in Firebase
        if len(messages) == 2:  # New conversation
            conversation_data = {
                "user_id": request.user_id,
                "messages": messages,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            print(f"DEBUG: Saving new conversation: {conversation_data}")
            saved_id = firebase_service.save_conversation(conversation_data)
            if saved_id:
                conversation_id = saved_id
                print(f"DEBUG: New conversation saved with ID: {conversation_id}")
        else:  # Update existing conversation
            print(f"DEBUG: Updating existing conversation {conversation_id} with {len(messages)} messages")
            success = firebase_service.update_conversation(conversation_id, messages)
            print(f"DEBUG: Update success: {success}")
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        print(f"DEBUG: Full error traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/conversation/{user_id}")
async def get_conversation_history(user_id: str):
    """Get conversation history for a user"""
    try:
        print(f"DEBUG: API - Fetching conversations for user: {user_id}")
        
        # Check if user_id is valid
        if not user_id or user_id.strip() == "":
            raise HTTPException(status_code=400, detail="Invalid user ID")
            
        # Get conversations from Firebase
        conversations = firebase_service.get_user_conversations(user_id)
        
        # If no conversations found, return empty array but with a 200 status
        if not conversations:
            print(f"DEBUG: API - No conversations found for user {user_id}")
            return {"conversations": []}
            
        print(f"DEBUG: API - Returning {len(conversations)} conversations")
        
        # Return the conversations
        return {"conversations": conversations}
    except Exception as e:
        print(f"Error getting conversation history: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Travel Assistant Chatbot is running!"}

@app.post("/test/create_conversation/{user_id}")
async def create_test_conversation(user_id: str):
    """Create a test conversation for a user"""
    try:
        # Create a test conversation
        conversation_data = {
            "user_id": user_id,
            "messages": [
                {
                    "role": "user",
                    "content": "This is a test message",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "role": "assistant",
                    "content": "This is a test response",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "created_at": datetime.now(), # Changed to datetime object
            "updated_at": datetime.now()  # Changed to datetime object
        }
        
        # Save the conversation
        conversation_id = firebase_service.save_conversation(conversation_data)
        
        if not conversation_id:
            raise HTTPException(status_code=500, detail="Failed to create test conversation")
            
        return {
            "message": "Test conversation created successfully",
            "conversation_id": conversation_id,
            "user_id": user_id
        }
    except Exception as e:
        print(f"Error creating test conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)