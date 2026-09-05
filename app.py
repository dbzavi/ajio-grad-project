from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from groq import Groq
import markdown

import os

app = Flask(__name__, static_folder='dashboard', static_url_path='')
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

# Load dataset once at startup
df = pd.read_csv('data/raw_data.csv', on_bad_lines='skip')
raw_reviews = df.iloc[:, 2].dropna().astype(str).tolist()
raw_reviews = [r for r in raw_reviews if len(r) > 20]

def retrieve_context(query, top_k=7):
    # Simple keyword based retrieval
    stopwords = ['what', 'when', 'where', 'why', 'how', 'does', 'ajio', 'the', 'is', 'in', 'and', 'about', 'to', 'do', 'they', 'for', 'a', 'of', 'are', 'can', 'it']
    words = [w for w in ''.join(e for e in query if e.isalnum() or e.isspace()).lower().split() if len(w) > 3 and w not in stopwords]
    
    if not words:
        return raw_reviews[:top_k]
        
    scored_reviews = []
    for r in raw_reviews:
        r_low = r.lower()
        score = sum(1 for w in words if w in r_low)
        if score > 0:
            scored_reviews.append((score, r))
            
    scored_reviews.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in scored_reviews[:top_k]]

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'answer': 'Please ask a question.'})
        
    context = retrieve_context(query)
    context_str = "\n\n---\n\n".join(context)
    
    system_prompt = (
        "You are an expert AI UX Researcher analyzing e-commerce fashion data. "
        "Answer the user's question based STRICTLY on the provided user review context below. "
        "CRITICAL FORMATTING INSTRUCTION: Output your answer as a short, numbered or bulleted list. "
        "Provide a concise explanation (1-2 sentences max) for each point. "
        "DO NOT quote the actual reviews. DO NOT use markdown tables. DO NOT write long paragraphs. "
        "Keep the overall response extremely brief, high-level, and easy to read.\n"
        "STRICT GUARDRAILS:\n"
        "1. You must NOT perform any competitive analysis or compare AJIO to any other apps (e.g., Myntra, Amazon, etc.).\n"
        "2. If the user asks an irrelevant question or asks for a competitive analysis, you MUST reply EXACTLY with this phrase and nothing else: 'Sorry I can answer only with the context of reviews across different sources'\n\n"
        f"CONTEXT REVIEWS:\n{context_str}"
    )
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            model="openai/gpt-oss-20b",
            temperature=0.3,
            max_tokens=1024
        )
        raw_answer = response.choices[0].message.content
        
        import re
        
        clean_answer = raw_answer.strip()
        
        # 1. If it still leaks "Draft:", grab the draft text
        if "Draft:" in clean_answer:
            part = clean_answer.split("Draft:")[1]
            if "Final Check" in part:
                clean_answer = part.split("Final Check")[0]
            elif "Self-Correction" in part:
                clean_answer = part.split("Self-Correction")[0]
            else:
                clean_answer = part
                
        # 2. If it still leaks "Based on the provided reviews", often that's where the answer starts
        elif "Based on the provided reviews" in clean_answer:
            idx = clean_answer.rfind("Based on the provided reviews")
            clean_answer = clean_answer[idx:]
            
        clean_answer = clean_answer.strip()
            
        html_answer = markdown.markdown(clean_answer)
        return jsonify({'answer': html_answer})
    except Exception as e:
        print(f"Groq API Error: {e}", flush=True)
        return jsonify({'answer': "An error occurred while connecting to the Groq LLM API. Please ensure your API key is valid."})

@app.route('/api/predict_fit', methods=['POST'])
def predict_fit():
    data = request.json
    height = data.get('height', '')
    weight = data.get('weight', '')
    fit_pref = data.get('fit_preference', '')
    
    if not height or not weight or not fit_pref:
        return jsonify({'recommendation': 'Please provide height, weight, and fit preference.'})
        
    query = "fit size small tight large loose true to size length waist shoulder"
    context = retrieve_context(query, top_k=10)
    context_str = "\n\n---\n\n".join(context)
    
    system_prompt = (
        "You are an expert AI Fit Assistant for AJIO. "
        "The user wants a personalized sizing recommendation based on their body profile. "
        "CRITICAL INSTRUCTION: Output your answer as a short, confident paragraph (2-3 sentences). "
        "DO NOT use markdown, lists, or headers. Be extremely concise and authoritative. "
        "Recommend a specific size (e.g., S, M, L, XL) and briefly explain why based on the context.\n\n"
        f"USER PROFILE: Height: {height}, Weight: {weight}, Fit Preference: {fit_pref}\n\n"
        f"CONTEXT REVIEWS (about this product):\n{context_str}"
    )
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "What size should I get?"}
            ],
            model="openai/gpt-oss-20b",
            temperature=0.3,
            max_tokens=200
        )
        raw_answer = response.choices[0].message.content
        return jsonify({'recommendation': raw_answer.strip()})
    except Exception as e:
        print(f"Groq API Error: {e}", flush=True)
        return jsonify({'recommendation': "An error occurred while connecting to the AI Fit Predictor."})

if __name__ == '__main__':
    app.run(port=8888, debug=True)
