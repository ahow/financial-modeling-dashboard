"""
Monte Carlo Valuation Distribution Framework - FIXED VERSION
Generates proper symmetric probability distributions of company valuations
"""

import math
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValuationDistribution:
    """Container for valuation distribution results"""
    mean: float
    median: float
    std_dev: float
    percentiles: Dict[int, float]  # 5th, 10th, 25th, 75th, 90th, 95th
    confidence_intervals: Dict[int, Tuple[float, float]]  # 68%, 90%, 95%
    var_95: float  # Value at Risk (95th percentile loss)
    expected_shortfall: float  # Expected loss beyond VaR
    scenario_probabilities: Dict[str, float]
    distribution_data: List[float]  # Raw simulation results

class MonteCarloValuationEngine:
    """Monte Carlo engine for generating symmetric valuation distributions"""
    
    def __init__(self, num_simulations: int = 10000):
        self.num_simulations = num_simulations
        
    def generate_valuation_distribution(
        self,
        base_valuation: float,
        company_metrics: Dict,
        scenario: str
    ) -> ValuationDistribution:
        """Generate symmetric probability distribution of valuations"""
        
        # Set random seed for reproducibility
        random.seed(42)
        valuations = []
        
        # Scenario-specific base adjustments
        scenario_multipliers = {
            'base_case': 1.0,
            'optimistic': 1.15,    # 15% higher base
            'pessimistic': 0.85,   # 15% lower base  
            'crisis': 0.70         # 30% lower base
        }
        
        scenario_base = base_valuation * scenario_multipliers.get(scenario, 1.0)
        
        # Scenario-specific volatility
        volatility_multipliers = {
            'base_case': 1.0,
            'optimistic': 0.8,     # Lower volatility in good times
            'pessimistic': 1.3,    # Higher volatility in bad times
            'crisis': 1.8          # Much higher volatility in crisis
        }
        
        base_volatility = 0.20  # 20% base volatility
        scenario_volatility = base_volatility * volatility_multipliers.get(scenario, 1.0)
        
        # Company-specific volatility adjustments
        sector = company_metrics.get('sector', 'Technology')
        sector_vol_adj = {
            'Technology': 1.4,
            'Healthcare': 1.2,
            'Financial Services': 1.3,
            'Energy': 1.5,
            'Manufacturing': 1.0,
            'Consumer Services': 1.1,
            'Real Estate': 1.2,
            'Utilities': 0.7
        }.get(sector, 1.0)
        
        beta = company_metrics.get('beta', 1.0)
        company_volatility = scenario_volatility * sector_vol_adj * beta
        
        # Generate proper symmetric normal distribution around scenario base
        for i in range(self.num_simulations):
            # Generate random shock from normal distribution (mean=0, std=volatility)
            # This creates symmetric distribution around the scenario base
            random_shock = random.normalvariate(0, company_volatility)
            
            # Apply additive shock to scenario base for symmetric distribution
            # This ensures the distribution is centered around the scenario base
            valuation = scenario_base * (1 + random_shock)
            
            # Ensure reasonable bounds (20% to 300% of base for more realistic range)
            valuation = max(scenario_base * 0.2, min(scenario_base * 3.0, valuation))
            
            valuations.append(valuation)
        
        return self._calculate_distribution_statistics(valuations, scenario)
    
    def _calculate_distribution_statistics(
        self, 
        valuations: List[float], 
        scenario: str
    ) -> ValuationDistribution:
        """Calculate comprehensive distribution statistics"""
        
        # Keep unsorted sample for visualization BEFORE sorting
        unsorted_sample = valuations[::10]  # Every 10th value for visualization
        
        valuations.sort()
        n = len(valuations)
        
        # Basic statistics
        mean_val = sum(valuations) / n
        median_val = valuations[n // 2]
        
        # Standard deviation
        variance = sum((x - mean_val) ** 2 for x in valuations) / n
        std_dev = math.sqrt(variance)
        
        # Percentiles
        percentiles = {
            5: valuations[int(0.05 * n)],
            10: valuations[int(0.10 * n)],
            25: valuations[int(0.25 * n)],
            75: valuations[int(0.75 * n)],
            90: valuations[int(0.90 * n)],
            95: valuations[int(0.95 * n)]
        }
        
        # Confidence intervals
        confidence_intervals = {
            68: (valuations[int(0.16 * n)], valuations[int(0.84 * n)]),
            90: (percentiles[5], percentiles[95]),
            95: (valuations[int(0.025 * n)], valuations[int(0.975 * n)])
        }
        
        # Risk metrics
        var_95 = mean_val - percentiles[5]  # 95% VaR
        tail_losses = [x for x in valuations if x < percentiles[5]]
        expected_shortfall = mean_val - (sum(tail_losses) / len(tail_losses) if tail_losses else percentiles[5])
        
        # Scenario probabilities
        scenario_probs = {
            'upside': len([x for x in valuations if x > mean_val * 1.15]) / n,
            'base_case': len([x for x in valuations if mean_val * 0.9 <= x <= mean_val * 1.1]) / n,
            'downside': len([x for x in valuations if x < mean_val * 0.85]) / n
        }
        
        return ValuationDistribution(
            mean=mean_val,
            median=median_val,
            std_dev=std_dev,
            percentiles=percentiles,
            confidence_intervals=confidence_intervals,
            var_95=var_95,
            expected_shortfall=expected_shortfall,
            scenario_probabilities=scenario_probs,
            distribution_data=list(unsorted_sample)  # Unsorted sample for proper histogram
        )

def create_company_valuation_distributions(
    company_data: Dict,
    base_valuation: float,
    scenarios: List[str] = None
) -> Dict[str, ValuationDistribution]:
    """Create symmetric valuation distributions for multiple scenarios"""
    
    if scenarios is None:
        scenarios = ['base_case', 'optimistic', 'pessimistic', 'crisis']
    
    engine = MonteCarloValuationEngine(num_simulations=10000)
    
    distributions = {}
    for scenario in scenarios:
        distributions[scenario] = engine.generate_valuation_distribution(
            base_valuation=base_valuation,
            company_metrics=company_data,
            scenario=scenario
        )
    
    return distributions

# Test the fixed Monte Carlo engine
if __name__ == "__main__":
    sample_company = {
        'sector': 'Technology',
        'market_cap': 50000,
        'beta': 1.2
    }
    
    base_valuation = 52500  # $52.5B
    
    distributions = create_company_valuation_distributions(
        company_data=sample_company,
        base_valuation=base_valuation
    )
    
    print("FIXED Monte Carlo Valuation Distributions:")
    for scenario, dist in distributions.items():
        print(f"\n{scenario.upper()}:")
        print(f"  Mean: ${dist.mean/1000:.1f}B")
        print(f"  Median: ${dist.median/1000:.1f}B")
        print(f"  Std Dev: ${dist.std_dev/1000:.1f}B")
        print(f"  90% CI: ${dist.confidence_intervals[90][0]/1000:.1f}B - ${dist.confidence_intervals[90][1]/1000:.1f}B")
        print(f"  VaR (95%): ${dist.var_95/1000:.1f}B")

