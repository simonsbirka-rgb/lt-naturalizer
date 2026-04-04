#!/usr/bin/env python3
"""
Collect real Lithuanian text samples from various sources.
"""

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import random
import re

HUMAN_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/human")
AI_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/ai")

def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return None
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_article_content(url, min_length=300):
    """Extract main content from a Lithuanian article."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'lt,en-US;q=0.7,en;q=0.3'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
            tag.decompose()
        
        # Try to find main content
        content_selectors = [
            'article', '.article-content', '.post-content', '.entry-content',
            '.content', 'main', '.main-content', '.text-content',
            '[itemprop="articleBody"]', '.article-body', '.story-content'
        ]
        
        text_parts = []
        for selector in content_selectors:
            elements = soup.select(selector)
            for el in elements:
                paragraphs = el.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if len(text) > 50:  # Skip very short paragraphs
                        text_parts.append(text)
        
        # If no content found with selectors, try all paragraphs
        if not text_parts:
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50:
                    text_parts.append(text)
        
        full_text = ' '.join(text_parts)
        full_text = clean_text(full_text)
        
        if len(full_text) >= min_length:
            return full_text
        return None
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def collect_from_lrt():
    """Collect from LRT news."""
    print("Collecting from LRT.lt...")
    urls = [
        "https://www.lrt.lt/naujienos/verslas",
        "https://www.lrt.lt/naujienos/mokslas-ir-it",
        "https://www.lrt.lt/naujienos/kultura"
    ]
    collected = 0
    
    for category_url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(category_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/naujienos/' in href and href.count('/') > 3:
                    if not href.startswith('http'):
                        href = 'https://www.lrt.lt' + href
                    article_links.append(href)
            
            for article_url in list(set(article_links))[:3]:
                if collected >= 5:
                    break
                print(f"  Trying: {article_url[:60]}...")
                text = extract_article_content(article_url)
                if text:
                    filename = HUMAN_DIR / f"lrt_news_{collected+1}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"    Saved: {len(text)} chars")
                    collected += 1
                time.sleep(1.5)
                
        except Exception as e:
            print(f"  Category error: {e}")
    
    return collected

def collect_from_delfi():
    """Collect from Delfi.lt."""
    print("Collecting from Delfi.lt...")
    # Try specific article URLs directly
    base_urls = [
        "https://www.delfi.lt/verslas/",
        "https://www.delfi.lt/mokslas/",
    ]
    collected = 0
    
    for base_url in base_urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(base_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'delfi.lt' in href and '.delfi.lt' not in href:
                    article_links.append(href)
            
            for article_url in list(set(article_links))[:3]:
                if collected >= 5:
                    break
                if not article_url.startswith('http'):
                    article_url = 'https:' + article_url if article_url.startswith('//') else 'https://www.delfi.lt' + article_url
                
                print(f"  Trying: {article_url[:60]}...")
                text = extract_article_content(article_url)
                if text:
                    filename = HUMAN_DIR / f"delfi_news_{collected+1}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"    Saved: {len(text)} chars")
                    collected += 1
                time.sleep(1.5)
                
        except Exception as e:
            print(f"  Error: {e}")
    
    return collected

def collect_from_wikipedia():
    """Collect Lithuanian Wikipedia articles."""
    print("Collecting from Lithuanian Wikipedia...")
    articles = [
        "https://lt.wikipedia.org/wiki/Lietuva",
        "https://lt.wikipedia.org/wiki/Vilnius",
        "https://lt.wikipedia.org/wiki/Lietuvių_kalba",
        "https://lt.wikipedia.org/wiki/Lietuvos_istorija",
        "https://lt.wikipedia.org/wiki/Kaunas"
    ]
    collected = 0
    
    for url in articles:
        try:
            print(f"  Fetching: {url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get main content
            content = soup.find('div', {'class': 'mw-parser-output'})
            if content:
                # Remove infoboxes and tables
                for tag in content(['table', 'div', 'sup', 'span']):
                    tag.decompose()
                
                paragraphs = content.find_all('p')
                text_parts = []
                for p in paragraphs:
                    text = p.get_text().strip()
                    # Filter out very short or citation-heavy paragraphs
                    if len(text) > 100 and text.count('[') < 5:
                        text_parts.append(text)
                
                full_text = ' '.join(text_parts[:10])  # Take first 10 substantial paragraphs
                full_text = clean_text(full_text)
                
                if len(full_text) >= 500:
                    title = url.split('/')[-1].replace('_', '')
                    filename = HUMAN_DIR / f"wikipedia_{title[:15]}_{collected+1}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(full_text)
                    print(f"    Saved: {len(full_text)} chars")
                    collected += 1
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(1)
    
    return collected

def create_sample_ai_texts():
    """Create sample AI-like Lithuanian texts for testing."""
    print("Creating AI-like sample texts...")
    
    # These are typical AI-generated Lithuanian text patterns
    # Based on common AI writing characteristics
    ai_samples = [
        """Dirbtinis intelektas yra revoliucinga technologija, kuri keičia mūsų pasaulį. Ši technologija leidžia kompiuteriams atlikti užduotis, kurios anksčiau reikalavo žmogaus intelekto. Dirbtinis intelektas gali analizuoti didelius duomenų kiekius, mokytis iš patirties ir priimti sprendimus.

Lietuvoje dirbtinis intelektas plėtojamas įvairiose srityse. Daugelis įmonių investuoja į šią technologiją, siekdamos pagerinti savo veiklos efektyvumą. Be to, Lietuvos universitetai vykdo tyrimus dirbtinio intelekto srityje.

Apskritai, dirbtinis intelektas turi didžiulį potencialą ateityje. Ši technologija gali padėti spręsti sudėtingas problemas ir pagerinti žmonių gyvenimo kokybę. Tačiau svarbu užtikrinti, kad dirbtinis intelektas būtų naudojamas atsakingai.""",

        """Nuotolinis darbas tapo itin populiarus pastaraisiais metais. Ši darbo forma suteikia daug privalumų tiek darbuotojams, tiek darbdaviams. Pirmiausia, nuotolinis darbas leidžia sutaupyti laiko, kuris anksčiau buvo skiriamas kelionėms į darbovietę.

Lietuvoje daugelis įmonių jau įdiegė nuotolinio darbo praktikas. Darbuotojai gali dirbti iš namų, kavinių ar kitų patogių vietų. Be to, ši darbo forma leidžia geriau suderinti darbo ir asmeninį gyvenimą.

Išvadai, nuotolinis darbas yra efektyvi darbo forma, kuri tęsis ir ateityje. Svarbu paminėti, kad ši praktika reikalauja savidisciplinos ir gero laiko valdymo.""",

        """Lietuvos švietimo sistema pergyvena reikšmingas permainas. Švietimo reformos tikslas - pagerinti mokymo kokybę ir parengti mokinius besimatančioms iššūkiams. Viena svarbiausių reformos krypčių yra skaitmeninimas.

Mokyklose vis dažniau naudojamos modernios technologijos. Mokiniai gali naudotis planšetiniais kompiuteriais, interaktyviomis lentomis ir įvairiomis mokymosi programomis. Be to, mokytojai vyksta mokymus, kad galėtų efektyviai naudotis šiomis priemonėmis.

Apskritai, švietimo reforma yra būtina Lietuvos ateiciai. Investicijos į švietimą bus atsipirksiančios ilguoju laikotarpiu. Svarbu užtikrinti, kad visi mokiniai turėtų lygias galimybes gauti kokybišką išsilavinimą.""",

        """Lietuvos žiema yra ypatingas metų laikas su savo unikaliais bruožais. Šalti orai, sniegas ir ledas sukuria nepakartojamą atmosferą. Žiema Lietuvoje tęsiasi nuo gruodžio iki vasario mėnesio.

Šaltasis metų laikas atneša įvairias pramogas ir tradicijas. Žmonės mėgsta slidinėti, čiuožinėti ir statyti sniego senius. Be to, Kalėdos ir Naujieji metai yra svarbios šventės, kurios vienija šeimas.

Kultūriniu požiūriu, žiema turi didelę reikšmę lietuvių tradicijoms. Daugelis papročių ir apeigų yra susiję su šiuo metų laiku. Pavyzdžiui, Kūčios yra sena tradicija, kurios metu šeimos susirenka prie bendro stalo.""",

        """Technologijų sektorius Lietuvoje auga itin sparčiai. Šalyje veikia daugybė technologijų įmonių, kurios kuria novatoriškus sprendimus. Fintech, žaidimų kūrimas ir programinės įrangos plėtra yra tarp svarbiausių sričių.

Vilnius ir Kaunas tapo svarbiais technologijų centrais. Šiuose miestuose veikia daug startup'ų ir inovacijų centrų. Be to, vyriausybė remia technologijų plėtrą per įvairias programas ir iniciatyvas.

Ateities perspektyvos atrodo labai optimistiškai. Tikimasi, kad technologijų sektorius toliau augs ir kurs naujas darbo vietas. Svarbu paminėti, kad Lietuva konkuruoja su kitomis Baltijos šalimis dėl investicijų į šią sritį.""",

        """Aplinkosaiga tampa vis svarbesne tema Lietuvoje. Žmonės vis dažniau susimąsto apie savo poveikį aplinkai ir bando gyventi tvarkingiau. Perdirbimas, atsinaujinantys energijos šaltiniai ir tvari transporto priemonės yra svarbios temos.

Vyriausybė įgyvendina įvairias aplinkosaugos iniciatyvas. Pavyzdžiui, skatinamas elektromobilių naudojimas ir atsinaujinančių energijos šaltinių plėtra. Be to, mokesčių politika nukreipta į taršos mažinimą.

Apskritai, ekologinis sąmoningumas auga tarp lietuvių. Vis daugiau žmonių renkasi tvarius produktus ir paslaugas. Ši tendencija yra teigiama ir turėtų tęstis ateityje."""
    ]
    
    collected = 0
    for i, text in enumerate(ai_samples):
        filename = AI_DIR / f"ai_sample_{collected+1}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  Created AI sample {collected+1}: {len(text)} chars")
        collected += 1
    
    return collected

def main():
    print("=" * 60)
    print("Lithuanian Corpus Collection")
    print("=" * 60)
    
    # Clear old placeholder files
    for f in HUMAN_DIR.glob("*.txt"):
        f.unlink()
    for f in AI_DIR.glob("*.txt"):
        f.unlink()
    
    print("\n[1/4] Collecting from Wikipedia...")
    wiki_count = collect_from_wikipedia()
    
    print("\n[2/4] Collecting from LRT...")
    lrt_count = collect_from_lrt()
    
    print("\n[3/4] Collecting from Delfi...")
    delfi_count = collect_from_delfi()
    
    print("\n[4/4] Creating AI samples...")
    ai_count = create_sample_ai_texts()
    
    print("\n" + "=" * 60)
    print("Collection Summary:")
    print(f"  Wikipedia articles: {wiki_count}")
    print(f"  LRT articles: {lrt_count}")
    print(f"  Delfi articles: {delfi_count}")
    print(f"  AI samples: {ai_count}")
    print(f"  Total human texts: {len(list(HUMAN_DIR.glob('*.txt')))}")
    print(f"  Total AI texts: {len(list(AI_DIR.glob('*.txt')))}")
    print("=" * 60)

if __name__ == "__main__":
    main()
