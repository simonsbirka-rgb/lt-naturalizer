#!/usr/bin/env python3
"""
Validation Framework for Lithuanian AI Detection
Tests detector accuracy against corpus data
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import random

@dataclass
class ValidationResult:
    true_positives: int = 0
    true_negatives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0

@dataclass
class ThresholdConfig:
    particle_threshold: float = 2.0
    copula_threshold: float = 8.0
    ngram_ai_threshold: int = 5
    genitive_chain_max: int = 3
    vocabulary_richness_min: float = 0.4

class ValidationFramework:
    def __init__(self, config_path: str = "config/analysis_config.json"):
        self.config = self._load_config(config_path)
        self.thresholds = ThresholdConfig()
        self.human_texts: List[Tuple[str, str]] = []
        self.ai_texts: List[Tuple[str, str]] = []
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_corpus(self, human_dir: str = "corpus/human", ai_dir: str = "corpus/ai"):
        human_path = Path(human_dir)
        if human_path.exists():
            for file_path in human_path.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.human_texts.append((file_path.name, f.read()))
        
        ai_path = Path(ai_dir)
        if ai_path.exists():
            for file_path in ai_path.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.ai_texts.append((file_path.name, f.read()))
        
        print(f"Loaded {len(self.human_texts)} human texts and {len(self.ai_texts)} AI texts")
    
    def calculate_particle_score(self, text: str) -> float:
        particles = self.config.get('particles', [])
        words = text.lower().split()
        word_count = len(words)
        
        if word_count == 0:
            return 0.0
        
        particle_count = sum(1 for word in words if word.strip('.,!?') in particles)
        return (particle_count / word_count) * 1000
    
    def calculate_copula_score(self, text: str) -> float:
        copula_forms = self.config.get('copula_forms', ['yra', 'buvo', 'bus', 'yra', 'esą'])
        words = text.lower().split()
        word_count = len(words)
        
        if word_count == 0:
            return 0.0
        
        copula_count = sum(1 for word in words if word.strip('.,!?') in copula_forms)
        return (copula_count / word_count) * 1000
    
    def calculate_vocabulary_richness(self, text: str) -> float:
        tokens = []
        for word in text.lower().split():
            tokens.append(word.strip('.,!?;:„"()[]'))
        
        if not tokens:
            return 0.0
        
        types = set(tokens)
        return len(types) / len(tokens)
    
    def calculate_sentence_length_variance(self, text: str) -> float:
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if len(lengths) < 2:
            return 0.0
        
        mean = sum(lengths) / len(lengths)
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        return variance ** 0.5
    
    def detect_ai_patterns(self, text: str) -> Dict[str, float]:
        scores = {
            'particle_score': self.calculate_particle_score(text),
            'copula_score': self.calculate_copula_score(text),
            'vocabulary_richness': self.calculate_vocabulary_richness(text),
            'sentence_variance': self.calculate_sentence_length_variance(text)
        }
        
        return scores
    
    def classify_text(self, text: str) -> Tuple[bool, Dict[str, float]]:
        scores = self.detect_ai_patterns(text)
        
        ai_indicators = 0
        
        if scores['particle_score'] < self.thresholds.particle_threshold:
            ai_indicators += 1
        
        if scores['copula_score'] > self.thresholds.copula_threshold:
            ai_indicators += 1
        
        if scores['vocabulary_richness'] < self.thresholds.vocabulary_richness_min:
            ai_indicators += 1
        
        is_ai = ai_indicators >= 2
        
        return is_ai, scores
    
    def validate(self) -> ValidationResult:
        result = ValidationResult()
        
        for name, text in self.human_texts:
            is_ai, scores = self.classify_text(text)
            if is_ai:
                result.false_positives += 1
            else:
                result.true_negatives += 1
        
        for name, text in self.ai_texts:
            is_ai, scores = self.classify_text(text)
            if is_ai:
                result.true_positives += 1
            else:
                result.false_negatives += 1
        
        total = result.true_positives + result.true_negatives + result.false_positives + result.false_negatives
        
        if total > 0:
            result.accuracy = (result.true_positives + result.true_negatives) / total
        
        if result.true_positives + result.false_positives > 0:
            result.precision = result.true_positives / (result.true_positives + result.false_positives)
        
        if result.true_positives + result.false_negatives > 0:
            result.recall = result.true_positives / (result.true_positives + result.false_negatives)
        
        if result.precision + result.recall > 0:
            result.f1_score = 2 * (result.precision * result.recall) / (result.precision + result.recall)
        
        return result
    
    def cross_validate(self, folds: int = 5) -> List[ValidationResult]:
        all_texts = [(text, False) for _, text in self.human_texts] + [(text, True) for _, text in self.ai_texts]
        random.shuffle(all_texts)
        
        fold_size = len(all_texts) // folds
        results = []
        
        for i in range(folds):
            test_start = i * fold_size
            test_end = test_start + fold_size
            
            test_set = all_texts[test_start:test_end]
            
            fold_result = ValidationResult()
            
            for text, is_ai in test_set:
                predicted_ai, scores = self.classify_text(text)
                
                if is_ai and predicted_ai:
                    fold_result.true_positives += 1
                elif not is_ai and not predicted_ai:
                    fold_result.true_negatives += 1
                elif not is_ai and predicted_ai:
                    fold_result.false_positives += 1
                else:
                    fold_result.false_negatives += 1
            
            total = fold_result.true_positives + fold_result.true_negatives + fold_result.false_positives + fold_result.false_negatives
            
            if total > 0:
                fold_result.accuracy = (fold_result.true_positives + fold_result.true_negatives) / total
            
            if fold_result.true_positives + fold_result.false_positives > 0:
                fold_result.precision = fold_result.true_positives / (fold_result.true_positives + fold_result.false_positives)
            
            if fold_result.true_positives + fold_result.false_negatives > 0:
                fold_result.recall = fold_result.true_positives / (fold_result.true_positives + fold_result.false_negatives)
            
            if fold_result.precision + fold_result.recall > 0:
                fold_result.f1_score = 2 * (fold_result.precision * fold_result.recall) / (fold_result.precision + fold_result.recall)
            
            results.append(fold_result)
        
        return results
    
    def optimize_thresholds(self) -> Dict[str, float]:
        particle_range = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        copula_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        richness_range = [0.3, 0.35, 0.4, 0.45, 0.5]
        
        best_f1 = 0
        best_thresholds = {}
        
        for p_thresh in particle_range:
            for c_thresh in copula_range:
                for r_thresh in richness_range:
                    self.thresholds.particle_threshold = p_thresh
                    self.thresholds.copula_threshold = c_thresh
                    self.thresholds.vocabulary_richness_min = r_thresh
                    
                    result = self.validate()
                    
                    if result.f1_score > best_f1:
                        best_f1 = result.f1_score
                        best_thresholds = {
                            'particle_threshold': p_thresh,
                            'copula_threshold': c_thresh,
                            'vocabulary_richness_min': r_thresh,
                            'f1_score': result.f1_score,
                            'accuracy': result.accuracy,
                            'precision': result.precision,
                            'recall': result.recall
                        }
        
        if best_thresholds:
            self.thresholds.particle_threshold = best_thresholds['particle_threshold']
            self.thresholds.copula_threshold = best_thresholds['copula_threshold']
            self.thresholds.vocabulary_richness_min = best_thresholds['vocabulary_richness_min']
        
        return best_thresholds
    
    def generate_report(self, output_path: str = "reports/validation_report.json") -> Dict:
        basic_result = self.validate()
        
        cross_val_results = self.cross_validate(folds=5)
        
        avg_accuracy = sum(r.accuracy for r in cross_val_results) / len(cross_val_results) if cross_val_results else 0
        avg_f1 = sum(r.f1_score for r in cross_val_results) / len(cross_val_results) if cross_val_results else 0
        
        report = {
            'basic_validation': {
                'true_positives': basic_result.true_positives,
                'true_negatives': basic_result.true_negatives,
                'false_positives': basic_result.false_positives,
                'false_negatives': basic_result.false_negatives,
                'accuracy': round(basic_result.accuracy, 4),
                'precision': round(basic_result.precision, 4),
                'recall': round(basic_result.recall, 4),
                'f1_score': round(basic_result.f1_score, 4)
            },
            'cross_validation': {
                'folds': [
                    {
                        'accuracy': round(r.accuracy, 4),
                        'precision': round(r.precision, 4),
                        'recall': round(r.recall, 4),
                        'f1_score': round(r.f1_score, 4)
                    }
                    for r in cross_val_results
                ],
                'average_accuracy': round(avg_accuracy, 4),
                'average_f1': round(avg_f1, 4)
            },
            'current_thresholds': {
                'particle_threshold': self.thresholds.particle_threshold,
                'copula_threshold': self.thresholds.copula_threshold,
                'vocabulary_richness_min': self.thresholds.vocabulary_richness_min
            },
            'corpus_stats': {
                'human_texts': len(self.human_texts),
                'ai_texts': len(self.ai_texts),
                'total_texts': len(self.human_texts) + len(self.ai_texts)
            }
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"Validation report saved to {output_path}")
        return report


def main():
    framework = ValidationFramework()
    
    framework.load_corpus()
    
    if framework.human_texts or framework.ai_texts:
        report = framework.generate_report()
        
        print("\n=== Validation Results ===")
        print(f"Accuracy: {report['basic_validation']['accuracy']:.2%}")
        print(f"Precision: {report['basic_validation']['precision']:.2%}")
        print(f"Recall: {report['basic_validation']['recall']:.2%}")
        print(f"F1 Score: {report['basic_validation']['f1_score']:.4f}")
        print(f"False Positives: {report['basic_validation']['false_positives']}")
        print(f"False Negatives: {report['basic_validation']['false_negatives']}")
    else:
        print("No corpus data found. Please add text files to corpus/human/ and corpus/ai/")


if __name__ == "__main__":
    main()
