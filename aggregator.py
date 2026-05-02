import feedparser
import json
import datetime

# 1. TAILOR YOUR SOURCES: Add any RSS feed URLs here
SOURCES = [
    'https://news.google.com/rss',
    'https://techcrunch.com/feed/'
]

# 2. TAILOR YOUR TOPICS: Only articles with these words will be saved
KEYWORDS = ['AI', 'Space', 'Python', 'Green Energy']

def fetch_and_filter():
    tailored_news = []
    
    for url in SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Check if any keyword is in the title or summary
            content_to_check = (entry.title + entry.get('summary', '')).lower()
            if any(key.lower() in content_to_check for key in KEYWORDS):
                tailored_news.append({
                    'title': entry.title,
                    'link': entry.link,
                    'date': entry.get('published', str(datetime.date.today())),
                    'source': url.split('/')[2] # Extracts the domain name
                })

    # Save the results to a JSON file
    with open('tailored_news.json', 'w') as f:
        json.dump(tailored_news[:20], f, indent=4) # Keep the top 20 matches

if __name__ == "__main__":
    fetch_and_filter()
