#!/usr/bin/env python3
"""
Experimental Analysis Toolkit for Condensed Quantum Operads
Statistical validation, visualization, and reporting tools for minimal viable experiments
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import bootstrap
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import warnings

@dataclass
class ExperimentResult:
    """Data structure for experimental results"""
    experiment_id: str
    timestamp: datetime
    hardware_backend: str
    circuit_type: str
    raw_counts: Dict[str, int]
    total_shots: int
    calibration_data: Dict[str, Any]
    metadata: Dict[str, Any]

class StatisticalAnalyzer:
    """Statistical analysis tools for quantum experiment validation"""
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha  # Significance level
        self.confidence_level = 1 - alpha
        
    def calculate_fidelity(self, measured_counts: Dict[str, int], 
                          theoretical_probs: Dict[str, float]) -> float:
        """Calculate fidelity between measured and theoretical distributions"""
        total_shots = sum(measured_counts.values())
        measured_probs = {state: count/total_shots 
                         for state, count in measured_counts.items()}
        
        # Ensure all theoretical states are present
        for state in theoretical_probs:
            if state not in measured_probs:
                measured_probs[state] = 0.0
                
        # Calculate fidelity (overlap between distributions)
        fidelity = 0.0
        for state in theoretical_probs:
            fidelity += np.sqrt(measured_probs.get(state, 0) * theoretical_probs[state])
            
        return fidelity
    
    def bell_state_fidelity(self, counts: Dict[str, int]) -> Tuple[float, float]:
        """Calculate Bell state fidelity with error estimation"""
        total_shots = sum(counts.values())
        
        # Perfect Bell state probabilities
        perfect_bell = {'00': 0.5, '11': 0.5, '01': 0.0, '10': 0.0}
        
        fidelity = self.calculate_fidelity(counts, perfect_bell)
        
        # Error estimation using shot noise
        # Standard error for binomial proportion
        p_00 = counts.get('00', 0) / total_shots
        p_11 = counts.get('11', 0) / total_shots
        error = np.sqrt((p_00 * (1 - p_00) + p_11 * (1 - p_11)) / total_shots)
        
        return fidelity, error
    
    def two_sample_comparison(self, group1: List[float], group2: List[float]) -> Dict[str, Any]:
        """Compare two groups of measurements with comprehensive statistics"""
        
        # Basic statistics
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        n1, n2 = len(group1), len(group2)
        
        # Two-sample t-test
        t_stat, t_pvalue = stats.ttest_ind(group1, group2)
        
        # Mann-Whitney U test (non-parametric)
        u_stat, u_pvalue = stats.mannwhitneyu(group1, group2, alternative='two-sided')
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
        
        # Bootstrap confidence intervals
        def bootstrap_diff(x, y):
            return np.mean(x) - np.mean(y)
        
        combined_data = (group1, group2)
        bootstrap_result = bootstrap(combined_data, bootstrap_diff, n_resamples=1000, 
                                   random_state=42, vectorized=False)
        ci_lower, ci_upper = bootstrap_result.confidence_interval
        
        return {
            'group1_mean': mean1,
            'group2_mean': mean2,
            'difference': mean1 - mean2,
            'group1_std': std1,
            'group2_std': std2,
            'group1_n': n1,
            'group2_n': n2,
            't_statistic': t_stat,
            't_pvalue': t_pvalue,
            'u_statistic': u_stat,
            'u_pvalue': u_pvalue,
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_effect_size(cohens_d),
            'bootstrap_ci_lower': ci_lower,
            'bootstrap_ci_upper': ci_upper,
            'significant_at_alpha': t_pvalue < self.alpha
        }
    
    def _interpret_effect_size(self, cohens_d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
    
    def power_analysis(self, effect_size: float, alpha: float = None, 
                      power: float = 0.8) -> int:
        """Calculate required sample size for given effect size and power"""
        if alpha is None:
            alpha = self.alpha
            
        # Approximate sample size calculation for two-sample t-test
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        # Cohen's formula for two-group comparison
        n_per_group = 2 * ((z_alpha + z_beta) / effect_size)**2
        
        return int(np.ceil(n_per_group))

class ExperimentVisualizer:
    """Visualization tools for experimental results"""
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        plt.style.use('default')  # Fallback to default style
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
    def plot_fidelity_comparison(self, standard_fidelities: List[float], 
                               liquid_fidelities: List[float],
                               title: str = "Bell State Fidelity Comparison") -> plt.Figure:
        """Plot fidelity comparison between standard and liquid preparations"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Box plot comparison
        data = [standard_fidelities, liquid_fidelities]
        labels = ['Standard', 'Liquid']
        bp = ax1.boxplot(data, labels=labels, patch_artist=True)
        bp['boxes'][0].set_facecolor(self.colors[0])
        bp['boxes'][1].set_facecolor(self.colors[1])
        
        ax1.set_ylabel('Fidelity')
        ax1.set_title('Fidelity Distribution')
        ax1.grid(True, alpha=0.3)
        
        # Scatter plot with error bars
        x_std = np.random.normal(1, 0.05, len(standard_fidelities))
        x_liq = np.random.normal(2, 0.05, len(liquid_fidelities))
        
        ax2.scatter(x_std, standard_fidelities, alpha=0.6, c=self.colors[0], 
                   label='Standard', s=50)
        ax2.scatter(x_liq, liquid_fidelities, alpha=0.6, c=self.colors[1], 
                   label='Liquid', s=50)
        
        # Add mean lines
        ax2.axhline(np.mean(standard_fidelities), color=self.colors[0], 
                   linestyle='--', alpha=0.8)
        ax2.axhline(np.mean(liquid_fidelities), color=self.colors[1], 
                   linestyle='--', alpha=0.8)
        
        ax2.set_xlim(0.5, 2.5)
        ax2.set_xticks([1, 2])
        ax2.set_xticklabels(['Standard', 'Liquid'])
        ax2.set_ylabel('Fidelity')
        ax2.set_title('Individual Measurements')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def plot_circuit_optimization(self, standard_depths: List[int], 
                                perfectoid_depths: List[int]) -> plt.Figure:
        """Plot circuit depth optimization results"""
        
        improvements = [(s - p) / s * 100 for s, p in zip(standard_depths, perfectoid_depths)]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Depth comparison
        x = np.arange(len(standard_depths))
        width = 0.35
        
        ax1.bar(x - width/2, standard_depths, width, label='Standard', 
               color=self.colors[0], alpha=0.7)
        ax1.bar(x + width/2, perfectoid_depths, width, label='Perfectoid', 
               color=self.colors[1], alpha=0.7)
        
        ax1.set_xlabel('Circuit Instance')
        ax1.set_ylabel('Circuit Depth')
        ax1.set_title('Circuit Depth Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Improvement histogram
        ax2.hist(improvements, bins=10, color=self.colors[2], alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(improvements), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(improvements):.1f}%')
        ax2.set_xlabel('Depth Reduction (%)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Optimization Effectiveness')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_error_detection_accuracy(self, classical_accuracy: List[float], 
                                    sheaf_accuracy: List[float]) -> plt.Figure:
        """Plot error detection accuracy comparison"""
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        # Create paired comparison plot
        x = np.arange(len(classical_accuracy))
        
        ax.plot(x, classical_accuracy, 'o-', color=self.colors[0], 
               label='Classical', linewidth=2, markersize=6)
        ax.plot(x, sheaf_accuracy, 's-', color=self.colors[1], 
               label='Sheaf Cohomology', linewidth=2, markersize=6)
        
        ax.set_xlabel('Test Instance')
        ax.set_ylabel('Detection Accuracy')
        ax.set_title('Error Syndrome Detection Accuracy')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add improvement annotations
        for i, (c, s) in enumerate(zip(classical_accuracy, sheaf_accuracy)):
            if s > c:
                improvement = (s - c) / c * 100
                ax.annotate(f'+{improvement:.1f}%', 
                           xy=(i, s), xytext=(i, s + 0.01),
                           ha='center', fontsize=8, color='green')
        
        plt.tight_layout()
        return fig

class ExperimentReporter:
    """Generate comprehensive reports from experimental results"""
    
    def __init__(self, analyzer: StatisticalAnalyzer, visualizer: ExperimentVisualizer):
        self.analyzer = analyzer
        self.visualizer = visualizer
        
    def generate_bell_state_report(self, standard_results: List[ExperimentResult],
                                 liquid_results: List[ExperimentResult]) -> Dict[str, Any]:
        """Generate comprehensive report for Bell state fidelity experiment"""
        
        # Extract fidelities
        standard_fidelities = []
        liquid_fidelities = []
        
        for result in standard_results:
            fidelity, _ = self.analyzer.bell_state_fidelity(result.raw_counts)
            standard_fidelities.append(fidelity)
            
        for result in liquid_results:
            fidelity, _ = self.analyzer.bell_state_fidelity(result.raw_counts)
            liquid_fidelities.append(fidelity)
        
        # Statistical comparison
        comparison = self.analyzer.two_sample_comparison(liquid_fidelities, standard_fidelities)
        
        # Generate visualization
        fig = self.visualizer.plot_fidelity_comparison(standard_fidelities, liquid_fidelities)
        
        # Compile report
        report = {
            'experiment_type': 'bell_state_fidelity',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'standard_mean_fidelity': np.mean(standard_fidelities),
                'liquid_mean_fidelity': np.mean(liquid_fidelities),
                'improvement': comparison['difference'],
                'improvement_percent': comparison['difference'] / np.mean(standard_fidelities) * 100,
                'statistical_significance': comparison['significant_at_alpha'],
                'p_value': comparison['t_pvalue'],
                'effect_size': comparison['cohens_d'],
                'effect_interpretation': comparison['effect_size_interpretation']
            },
            'detailed_statistics': comparison,
            'raw_data': {
                'standard_fidelities': standard_fidelities,
                'liquid_fidelities': liquid_fidelities
            },
            'interpretation': self._interpret_bell_results(comparison),
            'recommendations': self._recommend_next_steps(comparison)
        }
        
        return report, fig
    
    def _interpret_bell_results(self, comparison: Dict[str, Any]) -> str:
        """Interpret Bell state experimental results"""
        
        improvement = comparison['difference']
        p_value = comparison['t_pvalue']
        effect_size = comparison['cohens_d']
        
        if p_value < 0.001:
            significance = "highly significant (p < 0.001)"
        elif p_value < 0.01:
            significance = "significant (p < 0.01)"
        elif p_value < 0.05:
            significance = "marginally significant (p < 0.05)"
        else:
            significance = "not statistically significant"
        
        interpretation = f"""
        Liquid Bell state preparation showed a {improvement:.4f} improvement in fidelity 
        compared to standard preparation. This difference is {significance}.
        
        Effect size: {effect_size:.3f} ({comparison['effect_size_interpretation']})
        
        """
        
        if improvement > 0.01 and p_value < 0.05:
            interpretation += "RESULT: Supports theoretical predictions of condensed quantum operads."
        elif improvement > 0 and p_value < 0.05:
            interpretation += "RESULT: Small but significant improvement detected. Theoretical framework partially validated."
        else:
            interpretation += "RESULT: No significant improvement detected. Theoretical predictions not supported by this experiment."
            
        return interpretation
    
    def _recommend_next_steps(self, comparison: Dict[str, Any]) -> List[str]:
        """Recommend next experimental steps based on results"""
        
        recommendations = []
        
        if comparison['significant_at_alpha']:
            recommendations.extend([
                "Scale up to larger qubit systems to test scalability",
                "Investigate which theoretical aspects drive the improvement",
                "Conduct replication study with independent research group"
            ])
        else:
            recommendations.extend([
                "Increase sample size to improve statistical power",
                "Review theoretical assumptions and predictions",
                "Consider alternative experimental protocols",
                "Investigate sources of experimental noise"
            ])
            
        # Always recommend
        recommendations.extend([
            "Document all results in peer-reviewed publication",
            "Share data and analysis code for reproducibility"
        ])
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], filename: str):
        """Save report to JSON file"""
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Recursively convert numpy types
        def recursive_convert(data):
            if isinstance(data, dict):
                return {k: recursive_convert(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [recursive_convert(item) for item in data]
            else:
                return convert_numpy(data)
        
        clean_report = recursive_convert(report)
        
        with open(filename, 'w') as f:
            json.dump(clean_report, f, indent=2)

# Example usage and testing
def generate_synthetic_data() -> Tuple[List[ExperimentResult], List[ExperimentResult]]:
    """Generate synthetic experimental data for testing"""
    
    np.random.seed(42)  # For reproducible results
    
    standard_results = []
    liquid_results = []
    
    # Simulate 20 standard Bell state experiments
    for i in range(20):
        # Standard prep: ~90% fidelity with noise
        fidelity = np.random.normal(0.90, 0.03)
        fidelity = np.clip(fidelity, 0, 1)
        
        # Convert to counts (simulate 1024 shots)
        p_00_11 = fidelity * 0.5
        p_01_10 = (1 - fidelity) * 0.5
        
        counts = {
            '00': np.random.binomial(1024, p_00_11),
            '11': np.random.binomial(1024, p_00_11),
            '01': np.random.binomial(1024, p_01_10),
            '10': np.random.binomial(1024, p_01_10)
        }
        
        # Normalize to exactly 1024 shots
        total = sum(counts.values())
        if total != 1024:
            counts['00'] += 1024 - total
        
        result = ExperimentResult(
            experiment_id=f"standard_{i}",
            timestamp=datetime.now(),
            hardware_backend="ibmq_montreal",
            circuit_type="standard_bell",
            raw_counts=counts,
            total_shots=1024,
            calibration_data={},
            metadata={}
        )
        standard_results.append(result)
    
    # Simulate 20 liquid Bell state experiments (slight improvement)
    for i in range(20):
        # Liquid prep: ~92% fidelity (2% improvement)
        fidelity = np.random.normal(0.92, 0.03)
        fidelity = np.clip(fidelity, 0, 1)
        
        # Convert to counts
        p_00_11 = fidelity * 0.5
        p_01_10 = (1 - fidelity) * 0.5
        
        counts = {
            '00': np.random.binomial(1024, p_00_11),
            '11': np.random.binomial(1024, p_00_11),
            '01': np.random.binomial(1024, p_01_10),
            '10': np.random.binomial(1024, p_01_10)
        }
        
        total = sum(counts.values())
        if total != 1024:
            counts['00'] += 1024 - total
        
        result = ExperimentResult(
            experiment_id=f"liquid_{i}",
            timestamp=datetime.now(),
            hardware_backend="ibmq_montreal",
            circuit_type="liquid_bell",
            raw_counts=counts,
            total_shots=1024,
            calibration_data={},
            metadata={}
        )
        liquid_results.append(result)
    
    return standard_results, liquid_results

if __name__ == "__main__":
    # Demonstration of the analysis toolkit
    print("Experimental Analysis Toolkit for Condensed Quantum Operads")
    print("=" * 60)
    
    # Initialize tools
    analyzer = StatisticalAnalyzer(alpha=0.05)
    visualizer = ExperimentVisualizer()
    reporter = ExperimentReporter(analyzer, visualizer)
    
    # Generate synthetic data
    print("Generating synthetic experimental data...")
    standard_results, liquid_results = generate_synthetic_data()
    
    # Analyze results
    print("Performing statistical analysis...")
    report, fig = reporter.generate_bell_state_report(standard_results, liquid_results)
    
    # Display summary
    print("\nExperimental Results Summary:")
    print("-" * 40)
    summary = report['summary']
    print(f"Standard Bell fidelity: {summary['standard_mean_fidelity']:.4f}")
    print(f"Liquid Bell fidelity: {summary['liquid_mean_fidelity']:.4f}")
    print(f"Improvement: {summary['improvement']:.4f} ({summary['improvement_percent']:.2f}%)")
    print(f"Statistical significance: {summary['statistical_significance']}")
    print(f"P-value: {summary['p_value']:.6f}")
    print(f"Effect size: {summary['effect_size']:.3f} ({summary['effect_interpretation']})")
    
    print("\nInterpretation:")
    print(report['interpretation'])
    
    print("\nRecommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Save results
    print(f"\nSaving report and visualization...")
    reporter.save_report(report, f"bell_state_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    fig.savefig(f"bell_state_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 
                dpi=300, bbox_inches='tight')
    
    print("Analysis complete!")