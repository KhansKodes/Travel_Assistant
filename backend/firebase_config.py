import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import Dict, List, Optional
from datetime import datetime

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate('firebase_key.json')
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
        self.conversations_collection = 'conversations'
    
    def save_conversation(self, conversation_data: Dict) -> str:
        """Save conversation to Firestore"""
        try:
            print(f"DEBUG: Saving conversation data: {conversation_data}")
            # Create a new document reference
            doc_ref = self.db.collection(self.conversations_collection).document()
            
            # Add the document ID as conversation_id to the data
            conversation_data['conversation_id'] = doc_ref.id
            
            # Set the data in Firestore
            doc_ref.set(conversation_data)
            
            print(f"DEBUG: Conversation saved with ID: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation by ID"""
        try:
            doc = self.db.collection(self.conversations_collection).document(conversation_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
    
    def update_conversation(self, conversation_id: str, messages: List[Dict]) -> bool:
        """Update conversation with new messages"""
        try:
            doc_ref = self.db.collection(self.conversations_collection).document(conversation_id)
            doc_ref.update({
                'messages': messages,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            print(f"DEBUG: Updated conversation {conversation_id} with {len(messages)} messages")
            return True
        except Exception as e:
            print(f"Error updating conversation: {e}")
            return False
    
    def get_user_conversations(self, user_id: str) -> List[Dict]:
        """Get all conversations for a user"""
        try:
            print(f"DEBUG: Querying conversations for user_id={user_id}")
            conversations = []
            
            # First, let's check if the collection exists and has any documents
            collection_ref = self.db.collection(self.conversations_collection)
            all_docs = collection_ref.limit(1).stream()
            has_docs = any(True for _ in all_docs)
            print(f"DEBUG: Collection {self.conversations_collection} exists and has documents: {has_docs}")
            
            # Simple query that only filters by user_id
            query = collection_ref.where('user_id', '==', user_id)
            
            print(f"DEBUG: Executing query for user_id={user_id}")
            docs = query.stream()
            
            for doc in docs:
                conv_data = doc.to_dict()
                print(f"DEBUG: Found conversation document: {conv_data}")
                print(f"DEBUG: Document ID: {doc.id}")
                print(f"DEBUG: Document data: {conv_data}")
                conv_data['conversation_id'] = doc.id
                conversations.append(conv_data)
            
            # Sort conversations by updated_at in memory
            conversations.sort(key=lambda x: x.get('updated_at', datetime.min), reverse=True)
            # Limit to 5 conversations
            conversations = conversations[:5]
            
            print(f"DEBUG: Total conversations found for user {user_id}: {len(conversations)}")
            if len(conversations) == 0:
                print(f"DEBUG: No conversations found for user {user_id}")
                # Let's check what documents exist in the collection
                all_docs = collection_ref.limit(10).stream()
                print("DEBUG: First 10 documents in collection:")
                for doc in all_docs:
                    print(f"DEBUG: Document ID: {doc.id}, Data: {doc.to_dict()}")
            
            return conversations
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            print(f"DEBUG: Full error details: {str(e)}")
            return []