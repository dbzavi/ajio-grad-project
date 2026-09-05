import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

KEYWORDS = ["wishlist", "cart", "ajio", "wait", "sale", "size", "fit", "return"]

def fetch_reddit_html():
    print("Fetching Reddit discussions via raw HTML from old.reddit.com...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    data = []
    queries = ['ajio+wishlist', 'ajio+cart', 'ajio+size', 'ajio+return']
    
    for query in queries:
        url = f"https://old.reddit.com/r/IndianFashionAddicts/search?q={query}&restrict_sr=on&sort=new&t=all"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                posts = soup.find_all('div', class_='search-result-link')
                
                for post in posts:
                    title_elem = post.find('a', class_='search-title')
                    if not title_elem: continue
                    title = title_elem.text
                    
                    time_elem = post.find('time')
                    date_str = time_elem['datetime'] if time_elem and time_elem.has_attr('datetime') else '2026-08-01'
                    
                    content = title.lower()
                    
                    if any(kw in content for kw in KEYWORDS):
                        data.append({
                            'source': 'Reddit (Raw HTML)',
                            'date': date_str,
                            'content': title,
                            'rating': 1
                        })
            elif response.status_code == 429:
                print("Reddit Rate Limited (429). Gracefully degrading.")
                break
            else:
                print(f"Reddit HTML fetch failed: Status {response.status_code}")
        except Exception as e:
            print(f"Reddit scraper encountered an error: {e}")
            
        time.sleep(3) # Respectful delay
        
    return data

if __name__ == "__main__":
    print("--- Starting Reddit HTML Scraper ---")
    reddit_data = fetch_reddit_html()
    print(f"Total Reddit posts collected: {len(reddit_data)}")
    
    os.makedirs('data', exist_ok=True)
    if reddit_data:
        df = pd.DataFrame(reddit_data)
        df.to_csv('data/reddit_discussions.csv', index=False)
        print("Saved to data/reddit_discussions.csv")
