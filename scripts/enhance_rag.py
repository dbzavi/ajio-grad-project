import pandas as pd
import json

try:
    df = pd.read_csv('data/raw_data.csv', on_bad_lines='skip')
    # Assuming the review text is in the 3rd column based on previous logs
    reviews = df.iloc[:, 2].dropna().astype(str).tolist()
    
    # Filter out very short ones to keep data.js clean
    reviews = [r for r in reviews if len(r) > 20]
    
    with open('dashboard/data.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split off the old generateRagResponse function
    if 'function generateRagResponse' in content:
        content = content.split('function generateRagResponse')[0]

    js_code = f"""
const rawReviews = {json.dumps(reviews)};

function generateRagResponse(query) {{
    const q = query.toLowerCase();
    
    // 1. Check exact predefined context.md questions
    for (let item of ragDatabase) {{
        if (item.keywords.some(kw => q.includes(kw))) {{
            return item.answer;
        }}
    }}
    
    // 2. Dynamic Search on raw dataset (Keyword Retrieval)
    // Extract meaningful words from query
    const stopwords = ['what', 'when', 'where', 'why', 'how', 'does', 'ajio', 'the', 'is', 'in', 'and', 'about', 'to', 'do', 'they', 'for', 'a', 'of', 'are', 'can', 'it'];
    const words = q.replace(/[^\w\s]/gi, '').split(' ').filter(w => w.length > 3 && !stopwords.includes(w));
    
    if (words.length === 0) return "I need a few more specific keywords to search the database. What exactly are you looking for?";
    
    let matches = [];
    for (let r of rawReviews) {{
        let rLow = r.toLowerCase();
        // If the review contains AT LEAST ONE of the keywords
        if (words.some(w => rLow.includes(w))) {{
            matches.push(r);
        }}
    }}
    
    if (matches.length > 0) {{
        const count = matches.length;
        // Sort matches by relevance (how many keywords they hit)
        matches.sort((a, b) => {{
            let aScore = words.filter(w => a.toLowerCase().includes(w)).length;
            let bScore = words.filter(w => b.toLowerCase().includes(w)).length;
            return bScore - aScore;
        }});
        
        const bestMatch = matches[0];
        
        return `I searched the raw dataset and found **${{count}} reviews** discussing your keywords (${{words.join(', ')}}). <br><br>Here is a direct verbatim quote from the data:<br> <em>"${{bestMatch}}"</em>`;
    }}
    
    return "I couldn't find specific mentions of that in the 1,000+ review dataset. The data primarily focuses on sizing, returns, delivery delays, trust deficits, and UI limits. Try asking about 'refunds' or 'delivery'.";
}}
"""
    with open('dashboard/data.js', 'w', encoding='utf-8') as f:
        f.write(content + js_code)
        
    print("Successfully enhanced data.js with dynamic raw data retrieval.")
except Exception as e:
    print(f"Error: {e}")
