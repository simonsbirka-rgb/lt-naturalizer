#!/usr/bin/env python3
"""Fetch more Lithuanian articles."""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re
import urllib.parse

HUMAN_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/human")

def fetch_and_save(url, filename_prefix):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept-Language': 'lt,en-US;q=0.7,en;q=0.3'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            tag.decompose()
        
        # Get main content
        content_div = soup.find('div', {'class': 'mw-parser-output'}) or soup.find('article') or soup.find('main')
        
        if content_div:
            paragraphs = content_div.find_all('p')
        else:
            paragraphs = soup.find_all('p')
        
        text_parts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50]
        content = ' '.join(text_parts)
        content = re.sub(r'\s+', ' ', content)
        
        if len(content) >= 300:
            existing = len(list(HUMAN_DIR.glob(f"{filename_prefix}_*.txt")))
            filename = HUMAN_DIR / f"{filename_prefix}_{existing + 1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved: {filename.name} ({len(content)} chars)")
            return True
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    # Wikipedia articles with proper Lithuanian characters (URL encoded)
    wiki_articles = [
        "Lietuvių_kalba",
        "Lietuvos_kultūra", 
        "Kauno_miestas",
        "Klaipėda",
        "Lietuvos_istorija",
        "Šiauliai",
        "Panevėžys",
        "Nemunas",
        "Aukštaitija",
        "Žemaitija",
        "Dzūkija",
        "Suvalkija",
    ]
    
    print("Fetching Wikipedia articles with Lithuanian characters...")
    for article in wiki_articles:
        encoded = urllib.parse.quote(article)
        url = f"https://lt.wikipedia.org/wiki/{encoded}"
        print(f"  Trying: {article}")
        fetch_and_save(url, "wiki")
        time.sleep(0.3)
    
    total = len(list(HUMAN_DIR.glob("*.txt")))
    print(f"\nTotal human corpus files: {total}")

if __name__ == "__main__":
    main()
