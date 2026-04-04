#!/usr/bin/env python3
"""
Lithuanian Text Processing Pipeline
Handles tokenization, lemmatization, and POS tagging for corpus analysis.
"""

import os
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
import pickle

class TextProcessor:
    def __init__(self):
        self.config = self.load_config()
        self.particle_list = self.config["particle_list"]
        self.copula_forms = self.config["copula_forms"]
        self.corpus_dir = Path("corpus")
        self.processed_dir = self.corpus_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        with open("config/analysis_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    
    def process_corpus(self):
        """Process all text files in corpus"""
        print("Processing corpus...")
        
        # Process human corpus
        human_corpus = self.process_text_files(self.corpus_dir / "human", "human")
        
        # Process AI corpus
        ai_corpus = self.process_text_files(self.corpus_dir / "ai", "ai")
        
        # Save processed data
        self.save_processed_data(human_corpus, "human_corpus_processed.pkl")
        self.save_processed_data(ai_corpus, "ai_corpus_processed.pkl")
        
        print("Corpus processing complete!")
        print(f"Human corpus: {len(human_corpus)} files processed")
        print(f"AI corpus: {len(ai_corpus)} files processed")
    
    def process_text_files(self, corpus_path, corpus_type):
        """Process all text files in a corpus directory"""
        processed_data = []
        
        for file_path in corpus_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Process text
                processed = self.process_text(text, corpus_type)
                processed["file_name"] = file_path.name
                processed["corpus_type"] = corpus_type
                
                processed_data.append(processed)
                
                if len(processed_data) % 5 == 0:
                    print(f"Processed {len(processed_data)} files...")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        return processed_data
    
    def process_text(self, text, corpus_type):
        """Process individual text with all analysis steps"""
        # Tokenization
        tokens = self.tokenize(text)
        
        # Lemmatization (placeholder - would use actual Lithuanian lemmatizer)
        lemmas = self.lemmatize(tokens)
        
        # POS tagging (placeholder - would use actual POS tagger)
        pos_tags = self.pos_tag(tokens)
        
        # Analysis
        analysis = {
            "word_count": len(tokens),
            "sentence_count": self.count_sentences(text),
            "avg_sentence_length": self.calculate_avg_sentence_length(text),
            "type_token_ratio": self.calculate_ttr(tokens),
            "hapax_legomena": self.calculate_hapax_legomena(tokens),
            "particle_frequency": self.analyze_particles(tokens),
            "copula_density": self.analyze_copula(tokens),
            "morphological_complexity": self.analyze_morphology(tokens, pos_tags),
            "vocabulary_richness": self.calculate_vocabulary_richness(tokens)
        }
        
        return {
            "tokens": tokens,
            "lemmas": lemmas,
            "pos_tags": pos_tags,
            "analysis": analysis
        }
    
    def tokenize(self, text):
        """Tokenize text into words"""
        # Basic tokenization - would use actual Lithuanian tokenizer
        text = text.lower()
        text = re.sub(r'[^\w\sąčęėįšųūž]', ' ', text)  # Remove punctuation
        tokens = text.split()
        return tokens
    
    def lemmatize(self, tokens):
        """Lemmatize tokens (placeholder)"""
        # Placeholder - would use actual Lithuanian lemmatizer
        return tokens
    
    def pos_tag(self, tokens):
        """POS tagging (placeholder)"""
        # Placeholder - would use actual Lithuanian POS tagger
        return ["NOUN"] * len(tokens)  # Simplified for now
    
    def count_sentences(self, text):
        """Count sentences in text"""
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])
    
    def calculate_avg_sentence_length(self, text):
        """Calculate average sentence length"""
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        return np.mean(sentence_lengths) if sentence_lengths else 0
    
    def calculate_ttr(self, tokens):
        """Calculate Type-Token Ratio"""
        types = set(tokens)
        return len(types) / len(tokens) if tokens else 0
    
    def calculate_hapax_legomena(self, tokens):
        """Calculate hapax legomena rate"""
        token_counts = Counter(tokens)
        hapax = sum(1 for count in token_counts.values() if count == 1)
        return hapax / len(tokens) if tokens else 0
    
    def analyze_particles(self, tokens):
        """Analyze particle frequency"""
        particle_counts = Counter()
        
        for particle in self.particle_list:
            particle_counts[particle] = tokens.count(particle)
        
        # Calculate frequency per 1000 words
        total_words = len(tokens)
        particle_freq = {p: (count / total_words * 1000) if total_words > 0 else 0
                        for p, count in particle_counts.items()}
        
        return {
            "counts": particle_counts,
            "frequencies_per_1000": particle_freq,
            "total_particles": sum(particle_counts.values()),
            "particles_per_1000": (sum(particle_counts.values()) / total_words * 1000) 
                                 if total_words > 0 else 0
        }
    
    def analyze_copula(self, tokens):
        """Analyze copula density"""
        copula_counts = Counter()
        
        for form in self.copula_forms:
            copula_counts[form] = tokens.count(form)
        
        # Calculate frequency per 1000 words
        total_words = len(tokens)
        copula_freq = {f: (count / total_words * 1000) if total_words > 0 else 0
                      for f, count in copula_counts.items()}
        
        return {
            "counts": copula_counts,
            "frequencies_per_1000": copula_freq,
            "total_copula": sum(copula_counts.values()),
            "copula_per_1000": (sum(copula_counts.values()) / total_words * 1000) 
                              if total_words > 0 else 0
        }
    
    def analyze_morphology(self, tokens, pos_tags):
        """Analyze morphological complexity"""
        # Placeholder morphological analysis
        case_usage = {
            "genitive_chains": 0,  # Count of genitive case sequences
            "dative_usage": 0,      # Dative case frequency
            "aspectual_prefixes": 0 # Perfective vs imperfective prefixes
        }
        
        # Simplified morphological analysis
        for i, (token, pos) in enumerate(zip(tokens, pos_tags)):
            # Check for genitive chains (simplified)
            if pos == "NOUN" and i > 0 and pos_tags[i-1] == "NOUN":
                case_usage["genitive_chains"] += 1
            
            # Check for dative usage (simplified)
            if pos == "NOUN" and "dat" in token:  # Simplified check
                case_usage["dative_usage"] += 1
        
        return case_usage
    
    def calculate_vocabulary_richness(self, tokens):
        """Calculate vocabulary richness measures"""
        # Type-Token Ratio
        ttr = self.calculate_ttr(tokens)
        
        # Hapax legomena
        hapax = self.calculate_hapax_legomena(tokens)
        
        # Word length distribution
        word_lengths = [len(token) for token in tokens]
        avg_word_length = np.mean(word_lengths) if word_lengths else 0
        
        return {
            "ttr": ttr,
            "hapax_legomena": hapax,
            "avg_word_length": avg_word_length,
            "word_length_variance": np.var(word_lengths) if word_lengths else 0
        }
    
    def save_processed_data(self, data, filename):
        """Save processed data to file"""
        with open(self.processed_dir / filename, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saved processed data to {filename}")
    
    def load_processed_data(self, filename):
        """Load processed data from file"""
        with open(self.processed_dir / filename, 'rb') as f:
            return pickle.load(f)

if __name__ == "__main__":
    processor = TextProcessor()
    processor.process_corpus()
