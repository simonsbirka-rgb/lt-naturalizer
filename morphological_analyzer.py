#!/usr/bin/env python3
"""
Morphological Complexity Analyzer for Lithuanian Text
Analyzes case patterns, aspectual prefixes, participle systems
"""

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class MorphologicalStats:
    case_counts: Dict[str, int]
    genitive_chains: List[int]
    dative_patterns: Dict[str, int]
    participle_counts: Dict[str, int]
    aspectual_prefixes: Dict[str, int]
    noun_adjective_ratio: float
    verb_noun_ratio: float

class MorphologicalAnalyzer:
    def __init__(self, config_path: str = "config/analysis_config.json"):
        self.config = self._load_config(config_path)
        
        self.cases = {
            'vardininkas': ['as', 'is', 'ys', 'a', 'ė', 'us', 'uo'],
            'kilmininkas': ['o', 'io', 'ės', 'aus', 'ies', 'os', 'ės'],
            'naudininkas': ['ui', 'iui', 'ai', 'ei', 'ui', 'iai', 'ai', 'ei'],
            'galininkas': ['ą', 'ą', 'į', 'ią', 'ą', 'ą', 'u', 'iu', 'en', 'enį'],
            'įnagininkas': ['u', 'iu', 'a', 'ia', 'umi', 'iumi', 'ia', 'e'],
            'vietininkas': ['e', 'yje', 'uje', 'yje', 'uje', 'en', 'enyje'],
            'šauksmininkas': ['ai', 'i', 'y', 'au', 'ie', 'ė', 'as', 'iau']
        }
        
        self.aspectual_prefixes = {
            'perfective': ['pa', 'pri', 'nu', 'už', 'iš', 'at', 'pri', 'su', 'per', 'ap', 'para', 'paraš'],
            'imperfective': ['be', 'te', 'ne']
        }
        
        self.participle_endings = {
            'esamasis_dalyvis': ['antis', 'iantis', 'ąs', 'iantį', 'anti', 'iančią'],
            'būtasis_dalyvis': ['ęs', 'ę', 'usi', 'ęs', 'usi', 'ę'],
            'būtasis_dalyvis_veikiamasis': ['tas', 'tas', 'ta', 'tą', 'tą', 'tų'],
            'būtasis_dalyvis_neveikiamasis': ['tas', 'ta', 'tą', 'tų', 'tasis'],
            'pusdalyvis': ['damas', 'dama', 'damą', 'dami', 'damos'],
            'padalyvis': ['nant', 'dant', 'dama', 'damas'],
            'būdinys': ['te', 'tin', 'tina']
        }
        
        self.human_stats: List[MorphologicalStats] = []
        self.ai_stats: List[MorphologicalStats] = []
        
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
    
    def detect_case(self, word: str, context: List[str] = None) -> Optional[str]:
        word_lower = word.lower()
        
        for case, endings in self.cases.items():
            for ending in endings:
                if word_lower.endswith(ending):
                    if len(word_lower) - len(ending) >= 2:
                        return case
        return None
    
    def detect_genitive_chains(self, tokens: List[str]) -> List[int]:
        chains = []
        current_chain = 0
        
        for i, token in enumerate(tokens):
            case = self.detect_case(token)
            if case == 'kilmininkas':
                current_chain += 1
            else:
                if current_chain > 0:
                    chains.append(current_chain)
                current_chain = 0
        
        if current_chain > 0:
            chains.append(current_chain)
        
        return chains
    
    def detect_participle(self, word: str) -> Optional[str]:
        word_lower = word.lower()
        
        for participle_type, endings in self.participle_endings.items():
            for ending in endings:
                if word_lower.endswith(ending):
                    if len(word_lower) - len(ending) >= 3:
                        return participle_type
        return None
    
    def detect_aspectual_prefix(self, word: str) -> Optional[str]:
        word_lower = word.lower()
        
        for prefix_type, prefixes in self.aspectual_prefixes.items():
            for prefix in prefixes:
                if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
                    return prefix_type
        return None
    
    def estimate_pos_distribution(self, tokens: List[str]) -> Dict[str, int]:
        pos_counts = defaultdict(int)
        
        noun_endings = ['as', 'is', 'ys', 'a', 'ė', 'us', 'uo', 'uo', 'ė']
        verb_endings = ['ti', 'a', 'i', 'o', 'ė', 's', 'ia', 'ame', 'iate', 'o', 'ė']
        adjective_endings = ['as', 'a', 'is', 'i', 'us', 'i', 'as', 'a', 'esnis', 'esnė']
        
        for token in tokens:
            detected = False
            
            for ending in verb_endings:
                if token.endswith(ending) and len(token) > len(ending) + 1:
                    pos_counts['verb'] += 1
                    detected = True
                    break
            
            if not detected:
                for ending in adjective_endings:
                    if token.endswith(ending) and len(token) > len(ending) + 2:
                        pos_counts['adjective'] += 1
                        detected = True
                        break
            
            if not detected:
                for ending in noun_endings:
                    if token.endswith(ending) and len(token) > len(ending) + 1:
                        pos_counts['noun'] += 1
                        detected = True
                        break
            
            if not detected:
                pos_counts['other'] += 1
        
        return dict(pos_counts)
    
    def analyze_text(self, text: str) -> MorphologicalStats:
        tokens = self.tokenize(text)
        
        if not tokens:
            return MorphologicalStats(
                case_counts={},
                genitive_chains=[],
                dative_patterns={},
                participle_counts={},
                aspectual_prefixes={},
                noun_adjective_ratio=0.0,
                verb_noun_ratio=0.0
            )
        
        case_counts = defaultdict(int)
        for token in tokens:
            case = self.detect_case(token)
            if case:
                case_counts[case] += 1
        
        genitive_chains = self.detect_genitive_chains(tokens)
        
        dative_patterns = defaultdict(int)
        for i, token in enumerate(tokens):
            if self.detect_case(token) == 'naudininkas':
                if i > 0:
                    dative_patterns[f"prev_{tokens[i-1][:4]}"] += 1
                if i < len(tokens) - 1:
                    dative_patterns[f"next_{tokens[i+1][:4]}"] += 1
        
        participle_counts = defaultdict(int)
        for token in tokens:
            participle = self.detect_participle(token)
            if participle:
                participle_counts[participle] += 1
        
        aspectual_prefixes = defaultdict(int)
        for token in tokens:
            aspect = self.detect_aspectual_prefix(token)
            if aspect:
                aspectual_prefixes[aspect] += 1
        
        pos_dist = self.estimate_pos_distribution(tokens)
        nouns = pos_dist.get('noun', 0)
        adjectives = pos_dist.get('adjective', 0)
        verbs = pos_dist.get('verb', 0)
        
        noun_adj_ratio = nouns / adjectives if adjectives > 0 else float(nouns)
        verb_noun_ratio = verbs / nouns if nouns > 0 else float(verbs)
        
        return MorphologicalStats(
            case_counts=dict(case_counts),
            genitive_chains=genitive_chains,
            dative_patterns=dict(dative_patterns),
            participle_counts=dict(participle_counts),
            aspectual_prefixes=dict(aspectual_prefixes),
            noun_adjective_ratio=noun_adj_ratio,
            verb_noun_ratio=verb_noun_ratio
        )
    
    def process_corpus(self, corpus_dir: str, is_ai: bool = False) -> List[MorphologicalStats]:
        corpus_path = Path(corpus_dir)
        if not corpus_path.exists():
            print(f"Warning: Corpus directory {corpus_dir} does not exist")
            return []
        
        stats_list = []
        
        for file_path in corpus_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                stats = self.analyze_text(text)
                stats_list.append(stats)
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        if is_ai:
            self.ai_stats.extend(stats_list)
        else:
            self.human_stats.extend(stats_list)
        
        print(f"Processed {len(stats_list)} files from {corpus_dir}")
        return stats_list
    
    def aggregate_stats(self, stats_list: List[MorphologicalStats]) -> Dict:
        if not stats_list:
            return {}
        
        aggregated = {
            'case_totals': defaultdict(int),
            'genitive_chain_lengths': [],
            'genitive_chain_avg': 0.0,
            'genitive_chain_max': 0,
            'participle_totals': defaultdict(int),
            'aspectual_totals': defaultdict(int),
            'noun_adjective_ratio_avg': 0.0,
            'verb_noun_ratio_avg': 0.0
        }
        
        for stats in stats_list:
            for case, count in stats.case_counts.items():
                aggregated['case_totals'][case] += count
            
            aggregated['genitive_chain_lengths'].extend(stats.genitive_chains)
            
            for participle, count in stats.participle_counts.items():
                aggregated['participle_totals'][participle] += count
            
            for aspect, count in stats.aspectual_prefixes.items():
                aggregated['aspectual_totals'][aspect] += count
            
            aggregated['noun_adjective_ratio_avg'] += stats.noun_adjective_ratio
            aggregated['verb_noun_ratio_avg'] += stats.verb_noun_ratio
        
        n = len(stats_list)
        aggregated['noun_adjective_ratio_avg'] /= n
        aggregated['verb_noun_ratio_avg'] /= n
        
        if aggregated['genitive_chain_lengths']:
            aggregated['genitive_chain_avg'] = sum(aggregated['genitive_chain_lengths']) / len(aggregated['genitive_chain_lengths'])
            aggregated['genitive_chain_max'] = max(aggregated['genitive_chain_lengths'])
        
        aggregated['case_totals'] = dict(aggregated['case_totals'])
        aggregated['participle_totals'] = dict(aggregated['participle_totals'])
        aggregated['aspectual_totals'] = dict(aggregated['aspectual_totals'])
        
        return aggregated
    
    def calculate_case_complexity_score(self, aggregated: Dict) -> float:
        case_counts = aggregated.get('case_totals', {})
        total = sum(case_counts.values())
        
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in case_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * (p ** 0.5)
        
        return entropy
    
    def compare_corpora(self) -> Dict:
        human_agg = self.aggregate_stats(self.human_stats)
        ai_agg = self.aggregate_stats(self.ai_stats)
        
        comparison = {
            'human': {
                'case_distribution': human_agg.get('case_totals', {}),
                'genitive_chain_avg': human_agg.get('genitive_chain_avg', 0),
                'genitive_chain_max': human_agg.get('genitive_chain_max', 0),
                'participle_distribution': human_agg.get('participle_totals', {}),
                'aspectual_distribution': human_agg.get('aspectual_totals', {}),
                'noun_adjective_ratio': human_agg.get('noun_adjective_ratio_avg', 0),
                'verb_noun_ratio': human_agg.get('verb_noun_ratio_avg', 0),
                'morphological_complexity_score': self.calculate_case_complexity_score(human_agg)
            },
            'ai': {
                'case_distribution': ai_agg.get('case_totals', {}),
                'genitive_chain_avg': ai_agg.get('genitive_chain_avg', 0),
                'genitive_chain_max': ai_agg.get('genitive_chain_max', 0),
                'participle_distribution': ai_agg.get('participle_totals', {}),
                'aspectual_distribution': ai_agg.get('aspectual_totals', {}),
                'noun_adjective_ratio': ai_agg.get('noun_adjective_ratio_avg', 0),
                'verb_noun_ratio': ai_agg.get('verb_noun_ratio_avg', 0),
                'morphological_complexity_score': self.calculate_case_complexity_score(ai_agg)
            }
        }
        
        differences = {}
        
        if human_agg.get('genitive_chain_avg', 0) > 0 and ai_agg.get('genitive_chain_avg', 0) > 0:
            differences['genitive_chain_ratio'] = ai_agg['genitive_chain_avg'] / human_agg['genitive_chain_avg']
        
        if human_agg.get('noun_adjective_ratio_avg', 0) > 0 and ai_agg.get('noun_adjective_ratio_avg', 0) > 0:
            differences['noun_adj_ratio_diff'] = ai_agg['noun_adjective_ratio_avg'] - human_agg['noun_adjective_ratio_avg']
        
        comparison['differences'] = differences
        
        return comparison
    
    def generate_report(self, output_path: str = "reports/morphological_analysis.json") -> Dict:
        comparison = self.compare_corpora()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, ensure_ascii=False, indent=2)
        
        print(f"Morphological analysis report saved to {output_path}")
        return comparison


def main():
    analyzer = MorphologicalAnalyzer()
    
    analyzer.process_corpus("corpus/human", is_ai=False)
    analyzer.process_corpus("corpus/ai", is_ai=True)
    
    report = analyzer.generate_report()
    
    print("\n=== Morphological Comparison ===")
    print(f"Human genitive chain avg: {report['human']['genitive_chain_avg']:.2f}")
    print(f"AI genitive chain avg: {report['ai']['genitive_chain_avg']:.2f}")
    print(f"Human noun/adj ratio: {report['human']['noun_adjective_ratio']:.2f}")
    print(f"AI noun/adj ratio: {report['ai']['noun_adjective_ratio']:.2f}")


if __name__ == "__main__":
    main()
