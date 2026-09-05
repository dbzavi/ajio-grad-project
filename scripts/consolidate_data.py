import pandas as pd
import os

def consolidate_and_clean():
    print("--- Consolidating and Cleaning Data ---")
    files = [
        'data/app_reviews.csv',
        'data/reddit_discussions.csv',
        'data/web_forums.csv'
    ]
    
    dfs = []
    for f in files:
        if os.path.exists(f):
            try:
                df = pd.read_csv(f)
                dfs.append(df)
            except pd.errors.EmptyDataError:
                print(f"Skipping {f} (Empty)")
                
    if not dfs:
        print("No data files found to consolidate.")
        return
        
    combined = pd.concat(dfs, ignore_index=True)
    print(f"Total raw rows collected across all sources: {len(combined)}")
    
    # Basic cleaning
    # 1. Drop rows with missing content
    combined.dropna(subset=['content'], inplace=True)
    
    # 2. Remove duplicates based on 'content'
    initial_len = len(combined)
    combined.drop_duplicates(subset=['content'], inplace=True)
    print(f"Removed {initial_len - len(combined)} duplicate entries.")
    
    # 3. Filter out very short entries (less than 20 characters usually aren't helpful for insights)
    initial_len = len(combined)
    combined = combined[combined['content'].astype(str).str.len() >= 20]
    print(f"Removed {initial_len - len(combined)} entries that were too short.")
    
    print(f"Final clean dataset size: {len(combined)} rows.")
    
    # Save as CSV and JSON
    combined.to_csv('data/raw_data.csv', index=False)
    combined.to_json('data/raw_data.json', orient='records', indent=2)
    print("Saved consolidated data to data/raw_data.csv and data/raw_data.json")

if __name__ == "__main__":
    consolidate_and_clean()
