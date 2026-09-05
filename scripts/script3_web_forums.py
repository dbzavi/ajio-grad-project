import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import itertools
import re

KEYWORDS = ["wishlist", "cart", "ajio", "wait", "sale", "size", "fit", "return"]

def fetch_youtube_comments():
    print("Fetching YouTube Comments using lightweight JSON endpoints...")
    downloader = YoutubeCommentDownloader()
    data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        search_resp = requests.get('https://www.youtube.com/results?search_query=ajio+clothing+haul', headers=headers)
        found_ids = re.findall(r'"videoId":"(.*?)"', search_resp.text)
        video_ids = list(set(found_ids))[:5] # Take top 5 unique videos
    except Exception as e:
        print("Could not fetch YouTube video IDs dynamically.", e)
        video_ids = []

    for vid in video_ids:
        try:
            comments = downloader.get_comments(vid, sort_by=SORT_BY_POPULAR)
            for comment in itertools.islice(comments, 100): # Max 100 per video
                text = str(comment.get('text', '')).lower()
                if any(kw in text for kw in KEYWORDS):
                    data.append({
                        'source': 'YouTube Comments',
                        'date': comment.get('time', '2026-08-01'),
                        'content': comment.get('text'),
                        'rating': comment.get('votes', 0)
                    })
        except Exception as e:
            print(f"Failed to fetch comments for video {vid}: {e}")
            
    return data

def fetch_trustpilot_html():
    print("Fetching Trustpilot reviews via raw HTML...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    data = []
    url = "https://www.trustpilot.com/review/ajio.com"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = soup.find_all('p', {'data-service-review-text-typography': 'true'})
            for r in reviews:
                text = r.get_text().lower()
                if any(kw in text for kw in KEYWORDS):
                    data.append({
                        'source': 'Trustpilot (Raw HTML)',
                        'date': '2026-08-01', 
                        'content': r.get_text(),
                        'rating': 1
                    })
        else:
             print(f"Trustpilot returned status: {response.status_code}")
    except Exception as e:
        print(f"Trustpilot fetch failed: {e}")
        
    return data

if __name__ == "__main__":
    print("--- Starting Web Forums Scraper ---")
    yt_data = fetch_youtube_comments()
    tp_data = fetch_trustpilot_html()
    
    all_data = yt_data + tp_data
    print(f"Total Web forum posts collected: {len(all_data)}")
    
    os.makedirs('data', exist_ok=True)
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('data/web_forums.csv', index=False)
        print("Saved to data/web_forums.csv")
