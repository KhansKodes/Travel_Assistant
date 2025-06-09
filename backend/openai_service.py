import openai
import os
from typing import List, Dict
from dotenv import load_dotenv
import json
from firebase_admin import credentials

load_dotenv()

class OpenAIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
        
        # Travel Assistant system prompt
        self.system_prompt = """
        You are a helpful Travel Assistant chatbot. Your role is to:
        
        1. Help users plan trips and vacations
        2. Provide destination recommendations based on preferences
        3. Suggest activities, restaurants, and attractions
        4. Help with travel logistics (flights, hotels, transportation)
        5. Share travel tips and safety information
        6. Assist with budget planning for trips
        7. Recommend the best times to visit destinations
        8. Help with packing lists and travel preparation
        
        Always be friendly, informative, and enthusiastic about travel.
        Ask follow-up questions to better understand the user's preferences.
        Provide specific and actionable advice when possible.
        Remember previous parts of the conversation to maintain context.
        """
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using OpenAI GPT-3.5 Turbo"""
        try:
            # Prepare messages with system prompt
            full_messages = [{"role": "system", "content": self.system_prompt}]
            full_messages.extend(messages)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=full_messages,
                max_tokens=500,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again." 