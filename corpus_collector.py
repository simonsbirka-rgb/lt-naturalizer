#!/usr/bin/env python3
"""
Lithuanian Corpus Collection Pipeline
Collects and processes human and AI Lithuanian text for frequency analysis.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import random

class CorpusCollector:
    def __init__(self):
        self.config = self.load_config()
        self.human_sources = self.config["human_sources"]
        self.ai_prompts = self.config["ai_prompts"]
        self.corpus_dir = Path("corpus")
        self.human_dir = self.corpus_dir / "human"
        self.ai_dir = self.corpus_dir / "ai"
        
        self.human_dir.mkdir(parents=True, exist_ok=True)
        self.ai_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        with open("config/analysis_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    
    def collect_human_corpus(self):
        """Collect human Lithuanian text from various sources"""
        print("Collecting human Lithuanian corpus...")
        
        # News sources
        self.collect_news_corpus()
        
        # Literary sources
        self.collect_literary_corpus()
        
        # Forum/social media
        self.collect_forum_corpus()
        
        # Administrative text
        self.collect_admin_corpus()
        
        print(f"Human corpus collection complete. Total files: {len(list(self.human_dir.glob('*.txt')))}")
    
    def collect_news_corpus(self):
        """Collect news articles from Lithuanian sources"""
        news_sources = [
            {"url": "https://www.15min.lt", "source": "15min"},
            {"url": "https://www.delfi.lt", "source": "delfi"},
            {"url": "https://www.lrytas.lt", "source": "lrytas"}
        ]
        
        for source in news_sources:
            print(f"Collecting from {source['source']}...")
            try:
                # Get main page
                response = requests.get(source["url"])
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find article links
                articles = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/'):
                        href = source["url"] + href
                    if source["source"] in href and ".html" in href:
                        articles.append(href)
                
                # Collect sample articles
                collected = 0
                for article_url in articles[:5]:  # Limit to 5 per source
                    try:
                        article_response = requests.get(article_url)
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        
                        # Extract text content
                        text_content = self.extract_article_text(article_soup)
                        
                        if text_content and len(text_content) > 500:  # Minimum length
                            filename = f"news_{source['source']}_{collected + 1}.txt"
                            with open(self.human_dir / filename, 'w', encoding='utf-8') as f:
                                f.write(text_content)
                            collected += 1
                            time.sleep(random.uniform(1, 3))  # Rate limiting
                    except Exception as e:
                        print(f"Error collecting article {article_url}: {e}")
                
                print(f"Collected {collected} articles from {source['source']}")
            except Exception as e:
                print(f"Error collecting from {source['source']}: {e}")
    
    def extract_article_text(self, soup):
        """Extract main text content from article soup"""
        # Remove scripts, styles, and navigation
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text_content = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        return text_content
    
    def collect_literary_corpus(self):
        """Collect literary text from digital collections"""
        print("Collecting literary corpus...")
        
        # For now, create placeholder files
        literary_texts = [
            "Literary text sample 1 - Lithuanian literature from digital archives",
            "Literary text sample 2 - Classic Lithuanian works",
            "Literary text sample 3 - Contemporary Lithuanian literature"
        ]
        
        for i, text in enumerate(literary_texts):
            filename = f"literary_{i + 1}.txt"
            with open(self.human_dir / filename, 'w', encoding='utf-8') as f:
                f.write(text)
    
    def collect_forum_corpus(self):
        """Collect forum and social media text"""
        print("Collecting forum corpus...")
        
        # For now, create placeholder files
        forum_texts = [
            "Forum discussion about Lithuanian culture and traditions",
            "Social media post about daily life in Lithuania",
            "Online community conversation about technology"
        ]
        
        for i, text in enumerate(forum_texts):
            filename = f"forum_{i + 1}.txt"
            with open(self.human_dir / filename, 'w', encoding='utf-8') as f:
                f.write(text)
    
    def collect_admin_corpus(self):
        """Collect administrative text"""
        print("Collecting administrative corpus...")
        
        # For now, create placeholder files
        admin_texts = [
            "Government document about public policy in Lithuania",
            "Official communication from Lithuanian institutions",
            "Administrative text about legal procedures"
        ]
        
        for i, text in enumerate(admin_texts):
            filename = f"admin_{i + 1}.txt"
            with open(self.human_dir / filename, 'w', encoding='utf-8') as f:
                f.write(text)
    
    def collect_from_website(self, url, source_name, num_articles=10, min_length=500):
        """
        Collect articles from a specific website.
        
        Args:
            url: Base URL of the website to scrape
            source_name: Name identifier for the source (used in filenames)
            num_articles: Maximum number of articles to collect (default: 10)
            min_length: Minimum text length in characters (default: 500)
        
        Returns:
            Number of articles successfully collected
        """
        print(f"Collecting from {source_name} ({url})...")
        collected = 0
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all article links
            articles = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Handle relative URLs
                if href.startswith('/'):
                    href = url.rstrip('/') + href
                elif not href.startswith('http'):
                    href = url.rstrip('/') + '/' + href
                
                # Filter for article-like URLs
                if self._is_article_url(href, source_name):
                    articles.append(href)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_articles = []
            for article in articles:
                if article not in seen:
                    seen.add(article)
                    unique_articles.append(article)
            
            print(f"Found {len(unique_articles)} unique article links")
            
            # Collect articles
            for article_url in unique_articles[:num_articles]:
                try:
                    article_response = requests.get(article_url, headers=headers, timeout=30)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    
                    # Extract text content
                    text_content = self.extract_article_text(article_soup)
                    
                    # Clean and validate
                    text_content = self._clean_text(text_content)
                    
                    if text_content and len(text_content) >= min_length:
                        # Generate unique filename
                        filename = f"{source_name}_{collected + 1}.txt"
                        filepath = self.human_dir / filename
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(text_content)
                        
                        collected += 1
                        print(f"  Collected: {filename} ({len(text_content)} chars)")
                    
                    # Rate limiting - be respectful to servers
                    time.sleep(random.uniform(1.5, 3.5))
                    
                except requests.RequestException as e:
                    print(f"  Error fetching {article_url}: {e}")
                except Exception as e:
                    print(f"  Error processing article: {e}")
            
            print(f"Successfully collected {collected} articles from {source_name}")
            
        except requests.RequestException as e:
            print(f"Error connecting to {source_name}: {e}")
        except Exception as e:
            print(f"Unexpected error collecting from {source_name}: {e}")
        
        return collected
    
    def _is_article_url(self, url, source_name):
        """Check if URL looks like an article page"""
        article_indicators = [
            '.html',
            '/article/',
            '/news/',
            '/straipsnis/',
            '/naujiena/',
            '/story/',
            '/post/'
        ]
        
        exclude_patterns = [
            '/tag/',
            '/tags/',
            '/category/',
            '/author/',
            '/page/',
            '/search',
            '/login',
            '/register',
            '#',
            '.jpg',
            '.png',
            '.gif',
            '.pdf'
        ]
        
        url_lower = url.lower()
        
        # Check if URL contains article indicators
        has_indicator = any(ind in url_lower for ind in article_indicators)
        
        # Check if URL should be excluded
        should_exclude = any(exc in url_lower for exc in exclude_patterns)
        
        return has_indicator and not should_exclude
    
    def _clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return None
        
        # Remove extra whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove common boilerplate patterns
        boilerplate = [
            'Subscribe to our newsletter',
            'Follow us on',
            'Share this article',
            'Read more:',
            'Prenumeruokite',
            'Sekite mus',
            'Bendrinti',
            'Skaitykite daugiau'
        ]
        
        for pattern in boilerplate:
            text = text.replace(pattern, '')
        
        return text.strip()
    
    def collect_ai_corpus(self):
        """Generate AI-generated Lithuanian text samples"""
        print("Generating AI corpus...")
        
        # Define prompts
        prompts = [
            "Explain the concept of artificial intelligence in Lithuanian, focusing on technological aspects",
            "Describe the benefits of remote work in Lithuania from a professional perspective",
            "Discuss the importance of education reform in Lithuania and its impact on society",
            "Write about the Lithuanian winter and its cultural significance",
            "Analyze the current state of technology in Lithuania and future trends"
        ]
        
        # AI models to use
        ai_models = ["chatgpt-4", "claude", "gemini"]
        
        for model in ai_models:
            print(f"Generating {model} samples...")
            for i, prompt in enumerate(prompts):
                try:
                    # Generate text (placeholder - actual API calls would go here)
                    ai_text = self.generate_ai_text(model, prompt)
                    
                    if ai_text and len(ai_text) > 300:
                        filename = f"{model}_{i + 1}.txt"
                        with open(self.ai_dir / filename, 'w', encoding='utf-8') as f:
                            f.write(ai_text)
                        time.sleep(random.uniform(2, 5))  # Rate limiting
                except Exception as e:
                    print(f"Error generating {model} sample {i + 1}: {e}")
        
        print(f"AI corpus generation complete. Total files: {len(list(self.ai_dir.glob('*.txt')))}")
    
    def generate_ai_text(self, model, prompt):
        """Generate text using AI model (placeholder for actual API calls)"""
        # Placeholder implementation - in real use, this would call actual AI APIs
        # For now, return sample text
        return f"AI-generated text sample for {model} with prompt: {prompt[:50]}..."
    
    def run(self):
        """Run the complete corpus collection"""
        self.collect_human_corpus()
        self.collect_ai_corpus()
        
        print("Corpus collection complete!")
        print(f"Human corpus: {len(list(self.human_dir.glob('*.txt')))} files")
        print(f"AI corpus: {len(list(self.ai_dir.glob('*.txt')))} files")

if __name__ == "__main__":
    collector = CorpusCollector()
    collector.run()
