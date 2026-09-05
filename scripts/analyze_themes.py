import json
import os
import re

THEMES = {
    "Sizing Uncertainty & Return Friction": [
        "size", "fit", "wrong size", "exchange", "return", "refund", "reject", "chart", "large", "small"
    ],
    "Visual Trust Deficit (Expectation vs Reality)": [
        "photo", "review", "picture", "reality", "fake", "look like", "color", "material", "quality", "different"
    ],
    "Logistics & Delivery Paranoia": [
        "delay", "delivery", "late", "wait", "shadowfax", "logistics", "courier", "cancel", "never came"
    ],
    "Price & Offer Wait": [
        "price", "sale", "offer", "discount", "wait", "cost", "expensive", "drop", "coupon"
    ],
    "Platform UI/UX & Wishlist Limit": [
        "capacity", "70", "limit", "maximum", "save", "full", "glitch", "bug", "slow", "ui", "cart"
    ]
}

def analyze():
    print("--- Starting Batch Theme Analysis ---")
    payload_dir = 'data/llm_payloads'
    
    results = {theme: {"count": 0, "quotes": []} for theme in THEMES.keys()}
    
    for filename in os.listdir(payload_dir):
        if not filename.endswith('.json'): continue
        with open(os.path.join(payload_dir, filename), 'r', encoding='utf-8') as f:
            chunk = json.load(f)
            
        for review in chunk:
            content = review.get('content', '').lower()
            if not content: continue
            
            matched_themes = []
            for theme, keywords in THEMES.items():
                if any(re.search(r'\b' + kw + r'\b', content) for kw in keywords):
                    results[theme]["count"] += 1
                    matched_themes.append(theme)
            
            for theme in matched_themes:
                if len(content) > 50 and len(results[theme]["quotes"]) < 3:
                    results[theme]["quotes"].append(review.get('content').replace('\n', ' '))

    report = "# AI Discovery Insights Report\n\n"
    report += "> [!NOTE]\n> **Objective:** Summarize the top reasons users abandon or postpone wishlists based on 1,000+ scraped reviews across App Stores and Social Media.\n\n"
    report += "## Top Frictions Quantified\n\n"
    
    sorted_themes = sorted(results.items(), key=lambda x: x[1]["count"], reverse=True)
    
    for theme, data in sorted_themes:
        report += f"### {theme}\n"
        report += f"- **Frequency:** {data['count']} mentions\n"
        report += "- **Psychological Barrier:** This theme represents a major friction point stopping users from converting wishlist items to purchases.\n"
        report += "- **Verbatim Quotes:**\n"
        for q in data['quotes']:
            report += f"  > \"{q}\"\n"
        report += "\n"
        
    os.makedirs('docs', exist_ok=True)
    with open('docs/discovery_insights.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print("Analysis complete. Report generated at docs/discovery_insights.md")

if __name__ == "__main__":
    analyze()
