#!/usr/bin/env python3
"""
Statistical Analysis Module
Performs statistical analysis on processed Lithuanian corpus data.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from collections import Counter, defaultdict
import pickle
import matplotlib.pyplot as plt
import seaborn as sns



class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        import numpy as np
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

class StatisticalAnalyzer:
    def __init__(self):
        self.corpus_dir = Path("corpus")
        self.processed_dir = self.corpus_dir / "processed"
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Load processed data
        self.human_corpus = self.load_processed_data("human_corpus_processed.pkl")
        self.ai_corpus = self.load_processed_data("ai_corpus_processed.pkl")
    
    def load_processed_data(self, filename):
        """Load processed data from file"""
        try:
            with open(self.processed_dir / filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Run text_processor.py first.")
            return []
    
    def perform_full_analysis(self):
        """Perform complete statistical analysis"""
        print("Performing statistical analysis...")
        
        # 1. Particle frequency analysis
        particle_results = self.analyze_particles()
        
        # 2. Copula density analysis
        copula_results = self.analyze_copula()
        
        # 3. Vocabulary richness analysis
        vocabulary_results = self.analyze_vocabulary()
        
        # 4. Morphological complexity analysis
        morphology_results = self.analyze_morphology()
        
        # 5. Generate comprehensive report
        self.generate_report(particle_results, copula_results, 
                           vocabulary_results, morphology_results)
        
        print("Statistical analysis complete!")
    
    def analyze_particles(self):
        """Analyze particle frequency differences"""
        print("Analyzing particle frequencies...")
        
        human_particles = []
        ai_particles = []
        
        for doc in self.human_corpus:
            human_particles.append(doc["analysis"]["particle_frequency"]["particles_per_1000"])
        
        for doc in self.ai_corpus:
            ai_particles.append(doc["analysis"]["particle_frequency"]["particles_per_1000"])
        
        # Statistical test
        if len(human_particles) > 0 and len(ai_particles) > 0:
            t_stat, p_value = stats.ttest_ind(human_particles, ai_particles)
            
            results = {
                "human_mean": np.mean(human_particles),
                "human_std": np.std(human_particles),
                "ai_mean": np.mean(ai_particles),
                "ai_std": np.std(ai_particles),
                "t_statistic": t_stat,
                "p_value": p_value,
                "significant": p_value < 0.05
            }
        else:
            results = {
                "human_mean": 0,
                "human_std": 0,
                "ai_mean": 0,
                "ai_std": 0,
                "t_statistic": 0,
                "p_value": 1.0,
                "significant": False
            }
        
        return results
    
    def analyze_copula(self):
        """Analyze copula density differences"""
        print("Analyzing copula density...")
        
        human_copula = []
        ai_copula = []
        
        for doc in self.human_corpus:
            human_copula.append(doc["analysis"]["copula_density"]["copula_per_1000"])
        
        for doc in self.ai_corpus:
            ai_copula.append(doc["analysis"]["copula_density"]["copula_per_1000"])
        
        # Statistical test
        if len(human_copula) > 0 and len(ai_copula) > 0:
            t_stat, p_value = stats.ttest_ind(human_copula, ai_copula)
            
            results = {
                "human_mean": np.mean(human_copula),
                "human_std": np.std(human_copula),
                "ai_mean": np.mean(ai_copula),
                "ai_std": np.std(ai_copula),
                "t_statistic": t_stat,
                "p_value": p_value,
                "significant": p_value < 0.05
            }
        else:
            results = {
                "human_mean": 0,
                "human_std": 0,
                "ai_mean": 0,
                "ai_std": 0,
                "t_statistic": 0,
                "p_value": 1.0,
                "significant": False
            }
        
        return results
    
    def analyze_vocabulary(self):
        """Analyze vocabulary richness differences"""
        print("Analyzing vocabulary richness...")
        
        human_ttr = []
        ai_ttr = []
        human_hapax = []
        ai_hapax = []
        
        for doc in self.human_corpus:
            human_ttr.append(doc["analysis"]["vocabulary_richness"]["ttr"])
            human_hapax.append(doc["analysis"]["vocabulary_richness"]["hapax_legomena"])
        
        for doc in self.ai_corpus:
            ai_ttr.append(doc["analysis"]["vocabulary_richness"]["ttr"])
            ai_hapax.append(doc["analysis"]["vocabulary_richness"]["hapax_legomena"])
        
        # Statistical tests
        if len(human_ttr) > 0 and len(ai_ttr) > 0:
            ttr_t_stat, ttr_p_value = stats.ttest_ind(human_ttr, ai_ttr)
            hapax_t_stat, hapax_p_value = stats.ttest_ind(human_hapax, ai_hapax)
            
            results = {
                "ttr": {
                    "human_mean": np.mean(human_ttr),
                    "ai_mean": np.mean(ai_ttr),
                    "t_statistic": ttr_t_stat,
                    "p_value": ttr_p_value,
                    "significant": ttr_p_value < 0.05
                },
                "hapax_legomena": {
                    "human_mean": np.mean(human_hapax),
                    "ai_mean": np.mean(ai_hapax),
                    "t_statistic": hapax_t_stat,
                    "p_value": hapax_p_value,
                    "significant": hapax_p_value < 0.05
                }
            }
        else:
            results = {
                "ttr": {
                    "human_mean": 0,
                    "ai_mean": 0,
                    "t_statistic": 0,
                    "p_value": 1.0,
                    "significant": False
                },
                "hapax_legomena": {
                    "human_mean": 0,
                    "ai_mean": 0,
                    "t_statistic": 0,
                    "p_value": 1.0,
                    "significant": False
                }
            }
        
        return results
    
    def analyze_morphology(self):
        """Analyze morphological complexity differences"""
        print("Analyzing morphological complexity...")
        
        human_genitive = []
        ai_genitive = []
        
        for doc in self.human_corpus:
            human_genitive.append(doc["analysis"]["morphological_complexity"]["genitive_chains"])
        
        for doc in self.ai_corpus:
            ai_genitive.append(doc["analysis"]["morphological_complexity"]["genitive_chains"])
        
        # Statistical test
        if len(human_genitive) > 0 and len(ai_genitive) > 0:
            t_stat, p_value = stats.ttest_ind(human_genitive, ai_genitive)
            
            results = {
                "genitive_chains": {
                    "human_mean": np.mean(human_genitive),
                    "ai_mean": np.mean(ai_genitive),
                    "t_statistic": t_stat,
                    "p_value": p_value,
                    "significant": p_value < 0.05
                }
            }
        else:
            results = {
                "genitive_chains": {
                    "human_mean": 0,
                    "ai_mean": 0,
                    "t_statistic": 0,
                    "p_value": 1.0,
                    "significant": False
                }
            }
        
        return results
    
    def generate_report(self, particle_results, copula_results, 
                       vocabulary_results, morphology_results):
        """Generate comprehensive analysis report"""
        print("Generating analysis report...")
        
        report = {
            "summary": {
                "human_corpus_size": len(self.human_corpus),
                "ai_corpus_size": len(self.ai_corpus),
                "total_samples": len(self.human_corpus) + len(self.ai_corpus)
            },
            "particle_analysis": particle_results,
            "copula_analysis": copula_results,
            "vocabulary_analysis": vocabulary_results,
            "morphology_analysis": morphology_results,
            "conclusions": self.draw_conclusions(particle_results, copula_results,
                                                 vocabulary_results, morphology_results)
        }
        
        # Save report
        with open(self.reports_dir / "statistical_analysis_report.json", 'w') as f:
            json.dump(report, f, indent=2, cls=NumpyEncoder)
        
        # Generate visualizations
        self.generate_visualizations(particle_results, copula_results, 
                                    vocabulary_results, morphology_results)
        
        print(f"Report saved to {self.reports_dir / 'statistical_analysis_report.json'}")
    
    def draw_conclusions(self, particle_results, copula_results, 
                        vocabulary_results, morphology_results):
        """Draw conclusions from statistical analysis"""
        conclusions = []
        
        if particle_results["significant"]:
            diff = particle_results["human_mean"] - particle_results["ai_mean"]
            if diff > 0:
                conclusions.append(f"Human text uses significantly more particles "
                                 f"({particle_results['human_mean']:.2f} vs "
                                 f"{particle_results['ai_mean']:.2f} per 1000 words)")
            else:
                conclusions.append(f"AI text uses significantly more particles "
                                 f"({particle_results['ai_mean']:.2f} vs "
                                 f"{particle_results['human_mean']:.2f} per 1000 words)")
        
        if copula_results["significant"]:
            diff = copula_results["human_mean"] - copula_results["ai_mean"]
            if diff > 0:
                conclusions.append(f"Human text uses significantly more copula "
                                 f"({copula_results['human_mean']:.2f} vs "
                                 f"{copula_results['ai_mean']:.2f} per 1000 words)")
            else:
                conclusions.append(f"AI text uses significantly more copula "
                                 f"({copula_results['ai_mean']:.2f} vs "
                                 f"{copula_results['human_mean']:.2f} per 1000 words)")
        
        if vocabulary_results["ttr"]["significant"]:
            conclusions.append(f"Significant difference in Type-Token Ratio detected")
        
        return conclusions
    
    def generate_visualizations(self, particle_results, copula_results,
                               vocabulary_results, morphology_results):
        """Generate visualization plots"""
        print("Generating visualizations...")
        
        # Create comparison plots
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Particle frequency comparison
        self.plot_comparison(axes[0, 0], "Particle Frequency (per 1000 words)",
                           particle_results, "particles")
        
        # Copula density comparison
        self.plot_comparison(axes[0, 1], "Copula Density (per 1000 words)",
                           copula_results, "copula")
        
        # TTR comparison
        self.plot_comparison(axes[1, 0], "Type-Token Ratio",
                           vocabulary_results["ttr"], "ttr")
        
        # Hapax legomena comparison
        self.plot_comparison(axes[1, 1], "Hapax Legomena Rate",
                           vocabulary_results["hapax_legomena"], "hapax")
        
        plt.tight_layout()
        plt.savefig(self.reports_dir / "statistical_comparison.png", dpi=300)
        print(f"Visualization saved to {self.reports_dir / 'statistical_comparison.png'}")
    
    def plot_comparison(self, ax, title, results, metric):
        """Plot comparison bar chart"""
        categories = ['Human', 'AI']
        means = [results.get('human_mean', 0), results.get('ai_mean', 0)]
        stds = [results.get('human_std', 0), results.get('ai_std', 0)]
        
        x = np.arange(len(categories))
        bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, 
                     color=['blue', 'orange'])
        
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        # Add significance marker
        if results.get('significant', False):
            ax.text(0.5, 0.95, '*', transform=ax.transAxes, 
                   fontsize=20, ha='center', va='top')

if __name__ == "__main__":
    analyzer = StatisticalAnalyzer()
    analyzer.perform_full_analysis()
