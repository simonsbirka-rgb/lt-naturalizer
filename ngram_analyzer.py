#!/usr/bin/env python3
"""
3-Gram Pattern Analyzer for Lithuanian Text
Identifies AI-specific and AI-overused word sequences
"""

import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set
import math

class NgramAnalyzer:
    def __init__(self, config_path: str = "config/analysis_config.json"):
        self.config = self._load_config(config_path)
        self.human_ngrams: Dict[int, Counter] = {2: Counter(), 3: Counter(), 4: Counter()}
        self.ai_ngrams: Dict[int, Counter] = {2: Counter(), 3: Counter(), 4: Counter()}
        self.human_total: int = 0
        self.ai_total: int = 0
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def tokenize(self, text: str) -> List[str]:
        tokens = []
        current = ""
        for char in text.lower():
            if char.isalnum() or char in 'ąčęėįšųūž':
                current += char
            else:
                if current:
                    tokens.append(current)
                    current = ""
        if current:
            tokens.append(current)
        return tokens
    
    def extract_ngrams(self, tokens: List[str], n: int) -> List[Tuple[str, ...]]:
        if len(tokens) < n:
            return []
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    
    def process_corpus(self, corpus_dir: str, is_ai: bool = False):
        corpus_path = Path(corpus_dir)
        if not corpus_path.exists():
            print(f"Warning: Corpus directory {corpus_dir} does not exist")
            return
        
        ngram_store = self.ai_ngrams if is_ai else self.human_ngrams
        total_store = self.ai_total if is_ai else self.human_total
        
        file_count = 0
        for file_path in corpus_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                tokens = self.tokenize(text)
                
                for n in [2, 3, 4]:
                    ngrams = self.extract_ngrams(tokens, n)
                    ngram_store[n].update(ngrams)
                
                if is_ai:
                    self.ai_total += len(tokens)
                else:
                    self.human_total += len(tokens)
                
                file_count += 1
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        print(f"Processed {file_count} files from {corpus_dir}")
    
    def calculate_frequency(self, ngram: Tuple[str, ...], counter: Counter, total_tokens: int) -> float:
        if total_tokens == 0:
            return 0.0
        return (counter[ngram] / total_tokens) * 1000
    
    def find_ai_specific_ngrams(self, n: int = 3, min_ai_count: int = 5, min_ratio: float = 5.0) -> List[Dict]:
        ai_specific = []
        
        for ngram, ai_count in self.ai_ngrams[n].items():
            if ai_count < min_ai_count:
                continue
            
            human_count = self.human_ngrams[n].get(ngram, 0)
            
            ai_freq = self.calculate_frequency(ngram, self.ai_ngrams[n], self.ai_total)
            human_freq = self.calculate_frequency(ngram, self.human_ngrams[n], self.human_total)
            
            if human_freq == 0:
                ratio = float('inf')
                ai_specific.append({
                    'ngram': ' '.join(ngram),
                    'ai_count': ai_count,
                    'human_count': 0,
                    'ai_freq_per_1000': round(ai_freq, 4),
                    'human_freq_per_1000': 0,
                    'ratio': 'infinity',
                    'type': 'ai_only'
                })
            else:
                ratio = ai_freq / human_freq
                if ratio >= min_ratio:
                    ai_specific.append({
                        'ngram': ' '.join(ngram),
                        'ai_count': ai_count,
                        'human_count': human_count,
                        'ai_freq_per_1000': round(ai_freq, 4),
                        'human_freq_per_1000': round(human_freq, 4),
                        'ratio': round(ratio, 2),
                        'type': 'ai_overused'
                    })
        
        ai_specific.sort(key=lambda x: x['ratio'] if isinstance(x['ratio'], float) else float('inf'), reverse=True)
        return ai_specific
    
    def find_human_specific_ngrams(self, n: int = 3, min_human_count: int = 5, min_ratio: float = 5.0) -> List[Dict]:
        human_specific = []
        
        for ngram, human_count in self.human_ngrams[n].items():
            if human_count < min_human_count:
                continue
            
            ai_count = self.ai_ngrams[n].get(ngram, 0)
            
            human_freq = self.calculate_frequency(ngram, self.human_ngrams[n], self.human_total)
            ai_freq = self.calculate_frequency(ngram, self.ai_ngrams[n], self.ai_total)
            
            if ai_freq == 0:
                human_specific.append({
                    'ngram': ' '.join(ngram),
                    'human_count': human_count,
                    'ai_count': 0,
                    'human_freq_per_1000': round(human_freq, 4),
                    'ai_freq_per_1000': 0,
                    'ratio': 'infinity',
                    'type': 'human_only'
                })
            else:
                ratio = human_freq / ai_freq
                if ratio >= min_ratio:
                    human_specific.append({
                        'ngram': ' '.join(ngram),
                        'human_count': human_count,
                        'ai_count': ai_count,
                        'human_freq_per_1000': round(human_freq, 4),
                        'ai_freq_per_1000': round(ai_freq, 4),
                        'ratio': round(ratio, 2),
                        'type': 'human_overused'
                    })
        
        human_specific.sort(key=lambda x: x['ratio'] if isinstance(x['ratio'], float) else float('inf'), reverse=True)
        return human_specific
    
    def get_top_ngrams(self, n: int = 3, top_k: int = 50) -> Dict[str, List[Dict]]:
        top_human = []
        for ngram, count in self.human_ngrams[n].most_common(top_k):
            freq = self.calculate_frequency(ngram, self.human_ngrams[n], self.human_total)
            top_human.append({
                'ngram': ' '.join(ngram),
                'count': count,
                'freq_per_1000': round(freq, 4)
            })
        
        top_ai = []
        for ngram, count in self.ai_ngrams[n].most_common(top_k):
            freq = self.calculate_frequency(ngram, self.ai_ngrams[n], self.ai_total)
            top_ai.append({
                'ngram': ' '.join(ngram),
                'count': count,
                'freq_per_1000': round(freq, 4)
            })
        
        return {'human': top_human, 'ai': top_ai}
    
    def calculate_ngram_burstiness(self, text: str, n: int = 3) -> Dict:
        tokens = self.tokenize(text)
        ngrams = self.extract_ngrams(tokens, n)
        
        if not ngrams:
            return {'burstiness': 0, 'max_concentration': 0}
        
        positions = defaultdict(list)
        for i, ngram in enumerate(ngrams):
            positions[ngram].append(i)
        
        max_concentrations = []
        for ngram, pos_list in positions.items():
            if len(pos_list) < 2:
                continue
            
            max_gap = max(pos_list[i+1] - pos_list[i] for i in range(len(pos_list)-1))
            concentration = len(pos_list) / max_gap if max_gap > 0 else 0
            max_concentrations.append(concentration)
        
        if not max_concentrations:
            return {'burstiness': 0, 'max_concentration': 0}
        
        return {
            'burstiness': sum(max_concentrations) / len(max_concentrations),
            'max_concentration': max(max_concentrations)
        }
    
    def generate_report(self, output_path: str = "reports/ngram_analysis.json") -> Dict:
        report = {
            'corpus_stats': {
                'human_total_tokens': self.human_total,
                'ai_total_tokens': self.ai_total
            },
            'top_3grams': self.get_top_ngrams(3, 50),
            'ai_specific_3grams': self.find_ai_specific_ngrams(3, min_ai_count=3, min_ratio=3.0)[:100],
            'human_specific_3grams': self.find_human_specific_ngrams(3, min_human_count=3, min_ratio=3.0)[:100],
            'ai_specific_2grams': self.find_ai_specific_ngrams(2, min_ai_count=5, min_ratio=3.0)[:50],
            'ai_specific_4grams': self.find_ai_specific_ngrams(4, min_ai_count=3, min_ratio=3.0)[:50]
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"N-gram analysis report saved to {output_path}")
        return report


def main():
    analyzer = NgramAnalyzer()
    
    analyzer.process_corpus("corpus/human", is_ai=False)
    analyzer.process_corpus("corpus/ai", is_ai=True)
    
    report = analyzer.generate_report()
    
    print("\n=== Top AI-Specific 3-grams ===")
    for item in report['ai_specific_3grams'][:10]:
        print(f"  {item['ngram']}: AI={item['ai_freq_per_1000']}/1000, Human={item['human_freq_per_1000']}/1000, Ratio={item['ratio']}")
    
    print("\n=== Top Human-Specific 3-grams ===")
    for item in report['human_specific_3grams'][:10]:
        print(f"  {item['ngram']}: Human={item['human_freq_per_1000']}/1000, AI={item['ai_freq_per_1000']}/1000, Ratio={item['ratio']}")


if __name__ == "__main__":
    main()
