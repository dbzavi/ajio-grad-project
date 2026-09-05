import pandas as pd
import json
import os
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove excessive whitespace, newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ascii characters that might mess up prompt formatting
    text = text.encode('ascii', 'ignore').decode()
    return text.strip()

def preprocess_and_chunk(chunk_size=100):
    print("--- Starting Data Preprocessing & Chunking ---")
    input_file = 'data/raw_data.csv'
    output_dir = 'data/llm_payloads'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
        
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} raw records.")
    
    # Clean text
    df['content'] = df['content'].apply(clean_text)
    
    # Remove empty after cleaning
    df = df[df['content'].str.len() > 10]
    
    records = df.to_dict(orient='records')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Clear old chunks if any
    for old_file in os.listdir(output_dir):
        if old_file.endswith('.json'):
            os.remove(os.path.join(output_dir, old_file))
    
    # Chunking
    chunks_created = 0
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        chunk_file = os.path.join(output_dir, f'chunk_{chunks_created + 1}.json')
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=2)
            
        chunks_created += 1
        
    print(f"Successfully cleaned and split data into {chunks_created} chunks of max size {chunk_size}.")
    print(f"Payloads saved in '{output_dir}/'")

if __name__ == "__main__":
    # 100 reviews per chunk is very safe for most LLM context windows (around 10k-15k tokens usually)
    preprocess_and_chunk(chunk_size=100)
