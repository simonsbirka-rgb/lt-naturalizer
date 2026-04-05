#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

def is_valid_sample(text, source_url):
    """Check if sample meets criteria"""
    if len(text.split()) < 200:
        return False, "Too short"
    
    # Check if it's pre-2023
    try:
        if 'lrt.lt' in source_url:
            soup = BeautifulSoup(requests.get(source_url).text, 'html.parser')
            date_str = soup.find('time')['datetime'] if soup.find('time') else None
            if date_str:
                pub_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                if pub_date.year >= 2023:
                    return False, "Post-2022 source"
    except:
        pass
    
    # Check for human-written indicators
    if any(keyword in text.lower() for keyword in ['pranešimas', 'skelbimas', 'laiska', 'darbotvarkė']):
        return False, "Corporate template"
    
    return True, "Valid"

def collect_lrt_interviews():
    """Collect interviews from LRT.lt 2015-2021"""
    base_url = "https://www.lrt.lt/"
    interview_urls = [
        f"https://www.lrt.lt/naujienos/lietuva/12/1{i:02d}" for i in range(1, 13)
    ]
    
    collected = []
    for url in interview_urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='news-item')
            
            for article in articles:
                link = article.find('a')
                if link and '/lietuva/' in link['href']:
                    article_url = base_url + link['href'].lstrip('/')
                    article_resp = requests.get(article_url)
                    article_soup = BeautifulSoup(article_resp.text, 'html.parser')
                    
                    # Extract text
                    paragraphs = article_soup.find_all('p')
                    text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                    
                    valid, reason = is_valid_sample(text, article_url)
                    if valid:
                        collected.append({
                            'text': text,
                            'source': 'LRT.lt',
                            'url': article_url,
                            'reason': reason
                        })
                        if len(collected) >= 50:
                            return collected
        except Exception as e:
            continue
    
    return collected

def save_sample(text, filename, metadata):
    """Save sample with metadata"""
    with open(f'./corpus/human/{filename}', 'w', encoding='utf-8') as f:
        f.write(text)
    
    with open(f'./corpus/human/{filename}.meta.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def main():
    """Main collection function"""
    os.makedirs('./corpus/human', exist_ok=True)
    
    print("Phase 1: Corpus Construction")
    print("Collecting samples from LRT.lt...")
    
    # Collect from LRT
    lrt_samples = collect_lrt_interviews()
    print(f"Collected {len(lrt_samples)} LRT samples")
    
    # Save samples
    for i, sample in enumerate(lrt_samples[:20]):  # Limit to 20 for now
        filename = f"lrt_collected_{i+1}.txt"
        save_sample(sample['text'], filename, {
            'source': sample['source'],
            'url': sample['url'],
            'collection_date': str(datetime.now()),
            'status': 'valid'
        })
        print(f"Saved: {filename}")
    
    print("Corpus construction phase completed.")

if __name__ == "__main__":
    main()