import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, 'data', 'raw_data.csv')
try:
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    raw_reviews = df.iloc[:, 2].dropna().astype(str).tolist()
    raw_reviews = [r for r in raw_reviews if len(r) > 20]
except Exception as e:
    print(f"Error loading dataset: {e}")
    raw_reviews = ["This is a sample review because the dataset failed to load."]

def retrieve_context(query, top_k=7):
    stopwords = ['what', 'when', 'where', 'why', 'how', 'does', 'ajio', 'the', 'is', 'in', 'and', 'about', 'to', 'do', 'they', 'for', 'a', 'of', 'are', 'can', 'it']
    words = [w for w in ''.join(e for e in query if e.isalnum() or e.isspace()).lower().split() if len(w) > 3 and w not in stopwords]
    
    if not words:
        return raw_reviews[:top_k]
        
    scored_reviews = []
    for r in raw_reviews:
        score = sum(1 for w in words if w in r.lower())
        if score > 0:
            scored_reviews.append((score, r))
            
    scored_reviews.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in scored_reviews[:top_k]]

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    
    context_reviews = retrieve_context(query)
    context_str = "\n".join([f"- {r}" for r in context_reviews])
    
    system_prompt = (
        "You are an AI shopping assistant for AJIO. Answer the user's question based ONLY on the following real customer reviews.\n"
        "Be very concise (2-3 sentences max). If the answer isn't in the reviews, say you don't have enough data.\n\n"
        f"CONTEXT REVIEWS:\n{context_str}"
    )
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=150
        )
        raw_answer = response.choices[0].message.content
        return jsonify({'answer': raw_answer.strip()})
    except Exception as e:
        print(f"Groq API Error: {e}", flush=True)
        return jsonify({'answer': "An error occurred while connecting to the AI."})
