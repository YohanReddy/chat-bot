# from django.shortcuts import render
# from transformers import pipeline

# # Create your views here.
# summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

# def home (request):
#     if request.method == 'POST':
#         input = request.POST.get('input')
#         summary = summarizer(input, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
#         return render(request, 'index.html', {'summary': summary})
#     return render(request, 'index.html')




# from django.shortcuts import render
# import torch
# from transformers import pipeline

# def home(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('input')
#         pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.float32, device_map="auto")  # Convert torch_dtype to float32
#         messages = [
#             {
#                 "role": "system",
#                 "content": "You are a friendly chatbot who is here to help with any questions which I have.",
#             },
#             {"role": "user", "content": user_input},
#         ]
#         prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
#         outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
#         generated_text = outputs[0]["generated_text"]
#         return render(request, 'index.html', {'user_input': user_input, 'generated_text': generated_text})
#     return render(request, 'index.html')

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






# from django.shortcuts import render
# import requests

# API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
# headers = {"Authorization": "Bearer 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"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# def home(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('input')
#         try:
#             output = query({"inputs": user_input})  # Send user input directly without roles
#             generated_text = output[0]["generated_text"] if output else "No response"
#         except requests.exceptions.RequestException as e:
#             generated_text = "Error: Unable to fetch response from API. Please try again later."
#         return render(request, 'index.html', {'user_input': user_input, 'generated_text': generated_text})
#     return render(request, 'index.html')


# from django.shortcuts import render
# import requests

# API_URL = "https://api-inference.huggingface.co/models/Sharathhebbar24/chat_gpt2"
# headers = {"Authorization": "Bearer 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"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# def home(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('input')
#         try:
#             output = query({"inputs": user_input})
#             generated_text = output[0]["generated_text"] if output else "No response"
#         except requests.exceptions.RequestException as e:
#             generated_text = "Error: Unable to fetch response from API. Please try again later."
#         return render(request, 'index.html', {'user_input': user_input, 'generated_text': generated_text})
#     return render(request, 'index.html')
