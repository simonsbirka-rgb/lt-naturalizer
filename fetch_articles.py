#!/usr/bin/env python3
"""Fetch Lithuanian articles with better error handling."""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re

HUMAN_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/human")

def fetch_and_save(url, filename_prefix):
    """Fetch article and save to file."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'lt,en-US;q=0.7,en;q=0.3',
        'Cache-Control': 'no-cache'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        # Detect encoding from response
        if resp.encoding is None:
            resp.encoding = 'utf-8'
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
            tag.decompose()
        
        # Try multiple content selectors
        content = None
        selectors = [
            ('article', {}),
            ('div', {'class': 'article-content'}),
            ('div', {'class': 'content'}),
            ('div', {'class': 'post-content'}),
            ('div', {'class': 'entry-content'}),
            ('div', {'class': 'text-content'}),
            ('div', {'itemprop': 'articleBody'}),
            ('main', {}),
        ]
        
        for tag, attrs in selectors:
            elements = soup.find_all(tag, attrs) if attrs else soup.find_all(tag)
            if elements:
                text_parts = []
                for el in elements:
                    for p in el.find_all('p'):
                        t = p.get_text().strip()
                        if len(t) > 30:
                            text_parts.append(t)
                if text_parts:
                    content = ' '.join(text_parts)
                    break
        
        # Fallback: get all paragraphs
        if not content:
            paragraphs = soup.find_all('p')
            text_parts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30]
            content = ' '.join(text_parts)
        
        if content and len(content) >= 200:
            # Clean text
            content = re.sub(r'\s+', ' ', content)
            
            # Count existing files
            existing = len(list(HUMAN_DIR.glob(f"{filename_prefix}_*.txt")))
            filename = HUMAN_DIR / f"{filename_prefix}_{existing + 1}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved: {filename.name} ({len(content)} chars)")
            return True
        else:
            print(f"  Content too short or empty")
            return False
            
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    # More specific LRT article URLs
    lrt_urls = [
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888246/vilniaus-kolegijos-rektorius-atsistatydino-is-pareigu",
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888235/kaune-susidure-motociklas-ir-automobilis-suzeistas-zmogus",
        "https://www.lrt.lt/naujienos/pasaulis/5/2888229/jungtiniu-valstiju-aptarnavimo-sektoriai-rodikliai-gebejo-atsigauti-po-trumpo-smukimo",
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888216/seimo-nariai-siulo-del-valstybiniu-svenciu-dieno-sustabdyti-tv-baugsciu-rodyma",
        "https://www.lrt.lt/naujienos/verslas/4/2888208/kroviniu-vezejai-del-vairuotoju-stokos-priversti-moketi-didesnius-atlyginimus",
        "https://www.lrt.lt/naujienos/kultura/3/2888173/istorikas-teigia-kad-lietuviai-turi-zinoti-savo-istorija-bei-pagarba-praeiciai",
        "https://www.lrt.lt/naujienos/mokslas-ir-it/6/2888169/mokslininkai-atrado-nauja-buda-kaip-kovoti-su-vizvezys-liga",
        "https://www.lrt.lt/naujienos/sportas/10/2888162/zibenas-liko-vienas-klube-kol-sprendziasi-del-naujo-kontrakto",
        "https://www.lrt.lt/naujienos/nuomones/8/2888150/siginys-del-nauju-vertybiu-zmoniu-klaidinimas-ar-tikrove",
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888145/vilniuje-atidaryta-nauja-moderni-mokykla-su-ikimokyklinio-ugdymo-grupemis",
    ]
    
    print("Fetching LRT articles...")
    for url in lrt_urls:
        print(f"  Trying: ...{url[-40:]}")
        fetch_and_save(url, "lrt")
        time.sleep(0.5)
    
    # Try Lithuanian Wikipedia with ASCII URLs
    wiki_urls = [
        "https://lt.wikipedia.org/wiki/Vilniaus_miestas",
        "https://lt.wikipedia.org/wiki/Lietuvos_geografija", 
        "https://lt.wikipedia.org/wiki/Lietuviu_kalba",
        "https://lt.wikipedia.org/wiki/Lietuvos_ekonomika",
        "https://lt.wikipedia.org/wiki/Vilniaus_universitetas",
        "https://lt.wikipedia.org/wiki/Lietuvos_kultura",
        "https://lt.wikipedia.org/wiki/Lietuvos_istorija_(nepriklausomybes-laikotarpis)",
    ]
    
    print("\nFetching Wikipedia articles...")
    for url in wiki_urls:
        print(f"  Trying: ...{url.split('/')[-1][:30]}")
        fetch_and_save(url, "wiki")
        time.sleep(0.5)
    
    total = len(list(HUMAN_DIR.glob("*.txt")))
    print(f"\nTotal human corpus files: {total}")

if __name__ == "__main__":
    main()
