from django.shortcuts import render
import requests
from pymongo import MongoClient
from django.conf import settings

API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def home(request):
    if request.method == 'POST':
        user_input = request.POST.get('input')
        output = query({"inputs": user_input})
        generated_text = output[0]["generated_text"] if output else "No response"
        
        try:
            mongo_uri = settings.DATABASES['default']['CLIENT']['host']
            db_name = settings.DATABASES['default']['NAME']
            collection_name = 'messages'
            client = MongoClient(mongo_uri)
            db = client[db_name]
            messages_collection = db[collection_name]
            
            # Insert the message into MongoDB
            result = messages_collection.insert_one({'input': user_input, 'generated_text': generated_text})
            print("Inserted ID:", result.inserted_id)  # Debugging statement
            
            # Fetch all previous messages from MongoDB after inserting the new message
            previous_messages = list(messages_collection.find({}, {'_id': 0}))
            
        except Exception as e:
            print("MongoDB Error:", e)  # Debugging statement
            previous_messages = []
        
        return render(request, 'index.html', {'user_input': user_input, 'generated_text': generated_text, 'previous_messages': previous_messages})
    
    return render(request, 'index.html')


