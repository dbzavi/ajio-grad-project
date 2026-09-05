import pandas as pd
from google_play_scraper import reviews, Sort
from app_store_scraper import AppStore
from datetime import datetime, timedelta
import re
import os

# Keywords to filter relevant reviews (updated to include 'size', 'fit' as per edge-case mitigations)
KEYWORDS = ["wishlist", "cart", "wait", "save", "size", "fit"]

def fetch_play_store_reviews():
    print("Fetching Play Store reviews for AJIO...")
    ajio_reviews, _ = reviews(
        'com.ril.ajio',
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=150000  # High limit, we'll break early when we hit 1 year
    )
    
    one_year_ago = datetime.now() - timedelta(days=365)
    filtered_reviews = []
    
    for r in ajio_reviews:
        review_date = r.get('at')
        if review_date and review_date < one_year_ago:
            # Since they are sorted NEWEST, if we hit an older date, we can stop processing further
            break
            
        content = str(r.get('content', '')).lower()
        if any(keyword in content for keyword in KEYWORDS):
            filtered_reviews.append({
                'source': 'Play Store',
                'date': review_date,
                'content': r.get('content'),
                'rating': r.get('score')
            })
    return filtered_reviews

def fetch_app_store_reviews():
    print("Fetching App Store reviews for AJIO...")
    try:
        ajio = AppStore(country='in', app_name='ajio-online-shopping-app', app_id='1111631522')
        ajio.review(how_many=50000)
    except Exception as e:
        print(f"Failed to fetch app store reviews: {e}")
        return []
        
    one_year_ago = datetime.now() - timedelta(days=365)
    filtered_reviews = []
    
    for r in ajio.reviews:
        review_date = r.get('date')
        if review_date and review_date < one_year_ago:
            # Stop if older than 1 year
            break
            
        content = str(r.get('review', '')).lower()
        if any(keyword in content for keyword in KEYWORDS):
            filtered_reviews.append({
                'source': 'App Store',
                'date': review_date,
                'content': r.get('review'),
                'rating': r.get('rating')
            })
    return filtered_reviews

if __name__ == "__main__":
    print("--- Starting App Reviews Scraper (1-Year Horizon) ---")
    play_reviews = fetch_play_store_reviews()
    app_reviews = fetch_app_store_reviews()
    
    all_reviews = play_reviews + app_reviews
    print(f"Total filtered app reviews collected (last 1 year): {len(all_reviews)}")
    
    os.makedirs('data', exist_ok=True)
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv('data/app_reviews.csv', index=False)
        print("Saved to data/app_reviews.csv")
