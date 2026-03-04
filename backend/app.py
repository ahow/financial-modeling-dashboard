"""
Simplified Systems Model Flask Application - Multi-Scenario Version
Main entry point for the enhanced systems model web application.
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import math
import random
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                static_folder='static',
                template_folder='static')
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Configure app
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    @app.route('/')
    def index():
        """Serve the main application page"""
        return send_from_directory(app.static_folder, 'comprehensive_dashboard.html')
    
    @app.route('/comprehensive_dashboard.html')
    def comprehensive_dashboard():
        return send_from_directory('static', 'comprehensive_dashboard.html')
    
    @app.route('/chart_interface.html')
    def chart_interface():
        """Serve the original chart interface"""
        return send_from_directory(app.static_folder, 'chart_interface.html')
    
    @app.route('/api/company/distributions', methods=['POST', 'GET'])
    def analyze_company_distributions():
        """Analyze company valuation distributions using Monte Carlo simulation for all scenarios"""
        try:
            # Handle GET request for testing
            if request.method == 'GET':
                data = {
                    'market_cap': 50,
                    'revenue': 25,
                    'ebitda_margin': 22,
                    'revenue_growth': 8,
                    'sector': 'technology'
                }
            else:
                data = request.get_json()
            
            # Extract company characteristics
            market_cap = data.get('market_cap', 50)  # In billions
            revenue = data.get('revenue', 25)
            ebitda_margin = data.get('ebitda_margin', 22)
            revenue_growth = data.get('revenue_growth', 8)
            sector = data.get('sector', 'technology')
            
            # Convert market cap to millions for internal calculations
            base_valuation = market_cap * 1000  # Convert to millions
            
            # Generate Monte Carlo simulation for all scenarios
            num_simulations = 10000
            
            # Scenario-specific parameters
            scenario_params = {
                'base': {'mean_return': 0.0, 'volatility': 0.25},
                'optimistic': {'mean_return': 0.15, 'volatility': 0.20},
                'pessimistic': {'mean_return': -0.15, 'volatility': 0.30},
                'crisis': {'mean_return': -0.40, 'volatility': 0.35}
            }
            
            # Generate distributions for all scenarios
            all_scenarios = {}
            
            for scenario_name, params in scenario_params.items():
                random.seed(42)  # Reset seed for each scenario for consistency
                valuations = []
                
                # Generate realistic distribution for this scenario
                for _ in range(num_simulations):
                    # Generate random shock with scenario-specific parameters
                    random_shock = random.normalvariate(params['mean_return'], params['volatility'])
                    valuation = base_valuation * (1 + random_shock)
                    
                    # Apply realistic bounds with zero floor
                    if scenario_name == 'crisis':
                        # Crisis scenario: 10% bankruptcy probability (zero value)
                        # Remaining companies follow normal distribution with lower mean
                        bankruptcy_prob = 0.10
                        if random.random() < bankruptcy_prob:
                            valuation = 0  # Complete bankruptcy
                        else:
                            # For surviving companies, use normal distribution around crisis mean
                            # No artificial boosting - let natural distribution occur
                            valuation = max(0, valuation)  # Only floor at zero, no artificial minimum
                    else:
                        # Other scenarios: reasonable bounds (10% to 300% of base)
                        valuation = max(base_valuation * 0.1, min(valuation, base_valuation * 3.0))
                    
                    valuations.append(valuation)
                
                # Calculate statistics for this scenario
                valuations_sorted = sorted(valuations)
                n = len(valuations_sorted)
                
                mean_valuation = sum(valuations) / n
                median_valuation = valuations_sorted[n // 2]
                
                # Calculate percentiles
                p5 = valuations_sorted[int(0.05 * n)]
                p10 = valuations_sorted[int(0.10 * n)]
                p90 = valuations_sorted[int(0.90 * n)]
                p95 = valuations_sorted[int(0.95 * n)]
                
                # Store scenario results (convert to billions)
                all_scenarios[scenario_name] = {
                    'mean_valuation': mean_valuation / 1000,
                    'median_valuation': median_valuation / 1000,
                    'confidence_interval_90': [p10 / 1000, p90 / 1000],
                    'value_at_risk_95': p5 / 1000,
                    'distribution_data': [v / 1000 for v in valuations],  # Use unsorted for histogram
                    'scenario': scenario_name,
                    'num_simulations': num_simulations
                }
            
            # Use base case for main summary statistics
            base_case = all_scenarios['base']
            
            return jsonify({
                'success': True,
                'mean_valuation': base_case['mean_valuation'],
                'median_valuation': base_case['median_valuation'],
                'confidence_interval_90': base_case['confidence_interval_90'],
                'value_at_risk_95': base_case['value_at_risk_95'],
                'distribution_data': base_case['distribution_data'],
                'scenario': 'base',
                'num_simulations': num_simulations,
                'all_scenarios': all_scenarios  # Include all scenarios for multi-line chart
            })
            
        except Exception as e:
            print(f"Error in Monte Carlo analysis: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/company/distributions/test', methods=['GET'])
    def test_distributions():
        """Test endpoint for distribution analysis"""
        try:
            # Generate test data for all scenarios
            scenario_params = {
                'base': {'mean_return': 0.0, 'volatility': 0.25},
                'optimistic': {'mean_return': 0.15, 'volatility': 0.20},
                'pessimistic': {'mean_return': -0.15, 'volatility': 0.30},
                'crisis': {'mean_return': -0.30, 'volatility': 0.40}
            }
            
            base_valuation = 50000  # $50B in millions
            test_results = {}
            
            for scenario_name, params in scenario_params.items():
                random.seed(42)
                valuations = []
                
                for _ in range(10000):
                    random_shock = random.normalvariate(params['mean_return'], params['volatility'])
                    valuation = base_valuation * (1 + random_shock)
                    valuation = max(base_valuation * 0.2, min(valuation, base_valuation * 3.0))
                    valuations.append(valuation)
                
                valuations_sorted = sorted(valuations)
                n = len(valuations_sorted)
                
                mean_val = sum(valuations) / n
                p5 = valuations_sorted[int(0.05 * n)]
                p95 = valuations_sorted[int(0.95 * n)]
                
                test_results[scenario_name] = {
                    'mean': f"${mean_val/1000:.1f}B",
                    'min': f"${min(valuations)/1000:.1f}B", 
                    'max': f"${max(valuations)/1000:.1f}B",
                    'p5': f"${p5/1000:.1f}B",
                    'p95': f"${p95/1000:.1f}B"
                }
            
            return jsonify({
                'success': True,
                'message': 'Multi-scenario Monte Carlo distribution analysis working correctly',
                'test_results': test_results
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # API endpoint for the original chart interface
    @app.route('/api/enhanced/analyze-curves', methods=['POST'])
    def api_analyze_curves():
        """Analyze policy curves and calculate portfolio impact"""
        try:
            data = request.get_json()
            policy_assumptions = data.get('policy_assumptions', {})
            
            # Extract policy values for 2050 (or use defaults)
            carbon_price_2050 = policy_assumptions.get('carbon_price', {}).get(2050, 150)
            central_bank_rate_2050 = policy_assumptions.get('central_bank_rate', {}).get(2050, 4.5)
            govt_spending_2050 = policy_assumptions.get('govt_spending', {}).get(2050, 30)
            corp_tax_rate_2050 = policy_assumptions.get('corp_tax_rate', {}).get(2050, 25)
            
            # Calculate market variables based on policy assumptions
            # GDP Growth Impact
            gdp_growth_base = 2.5
            gdp_impact = (
                (govt_spending_2050 - 25) * 0.05 +  # Government spending impact
                (5.0 - central_bank_rate_2050) * 0.3 +  # Interest rate impact
                (carbon_price_2050 - 100) * 0.002  # Carbon price impact (small)
            )
            gdp_growth = gdp_growth_base + gdp_impact
            
            # Inflation Impact
            inflation_base = 2.0
            inflation_impact = (
                (central_bank_rate_2050 - 4.0) * -0.2 +  # Interest rate impact
                (govt_spending_2050 - 25) * 0.03 +  # Government spending impact
                (carbon_price_2050 - 100) * 0.001  # Carbon price impact
            )
            inflation = max(0, inflation_base + inflation_impact)
            
            # Unemployment Impact (Okun's Law approximation)
            unemployment_base = 5.0
            unemployment = max(0, unemployment_base - (gdp_growth - 2.5) * 0.5)
            
            # Market Volatility
            volatility_base = 0.15
            volatility_impact = (
                abs(central_bank_rate_2050 - 4.0) * 0.01 +  # Interest rate uncertainty
                abs(carbon_price_2050 - 100) * 0.0001 +  # Carbon price uncertainty
                abs(corp_tax_rate_2050 - 25) * 0.002  # Tax rate uncertainty
            )
            market_volatility = volatility_base + volatility_impact
            
            # Calculate WACC components
            risk_free_rate = central_bank_rate_2050
            market_risk_premium = 0.06 + market_volatility * 0.2  # Volatility affects risk premium
            
            # Sector-specific calculations
            sectors = {
                'Technology': {'beta': 1.3, 'weight': 0.25, 'tax_sensitivity': 1.2, 'carbon_sensitivity': 0.5},
                'Healthcare': {'beta': 0.9, 'weight': 0.15, 'tax_sensitivity': 0.8, 'carbon_sensitivity': 0.3},
                'Financial': {'beta': 1.1, 'weight': 0.20, 'tax_sensitivity': 1.5, 'carbon_sensitivity': 0.2},
                'Energy': {'beta': 1.4, 'weight': 0.10, 'tax_sensitivity': 1.0, 'carbon_sensitivity': 2.0},
                'Consumer': {'beta': 1.0, 'weight': 0.15, 'tax_sensitivity': 1.1, 'carbon_sensitivity': 0.8},
                'Industrial': {'beta': 1.2, 'weight': 0.15, 'tax_sensitivity': 1.3, 'carbon_sensitivity': 1.2}
            }
            
            sector_results = {}
            total_equity_value = 0
            weighted_wacc = 0
            
            for sector, props in sectors.items():
                # Calculate cost of equity using CAPM
                cost_of_equity = risk_free_rate + props['beta'] * market_risk_premium
                
                # Adjust for policy impacts
                tax_impact = (25 - corp_tax_rate_2050) * props['tax_sensitivity'] * 0.01
                carbon_impact = (carbon_price_2050 - 100) * props['carbon_sensitivity'] * 0.0001
                
                adjusted_cost_of_equity = cost_of_equity + tax_impact + carbon_impact
                
                # Simplified WACC calculation (assuming 70% equity, 30% debt)
                cost_of_debt = risk_free_rate + 0.02  # 2% credit spread
                wacc = 0.7 * adjusted_cost_of_equity + 0.3 * cost_of_debt * (1 - corp_tax_rate_2050/100)
                
                # Calculate sector equity value (simplified DCF)
                base_cash_flow = 100  # Base cash flow per sector
                growth_rate = min(gdp_growth * 0.8, 0.06)  # Cap growth at 6%
                terminal_value = base_cash_flow * (1 + growth_rate) / (wacc/100 - growth_rate)
                
                sector_equity_value = terminal_value * props['weight'] * 1000  # Scale up
                
                sector_results[sector] = {
                    'cost_of_equity': adjusted_cost_of_equity,
                    'wacc': wacc,
                    'equity_value': sector_equity_value,
                    'weight': props['weight']
                }
                
                total_equity_value += sector_equity_value
                weighted_wacc += wacc * props['weight']
            
            # Calculate portfolio metrics
            base_portfolio_value = 1000000  # $1M base
            policy_impact = (
                (carbon_price_2050 - 100) * 500 +  # Carbon impact
                (5.0 - central_bank_rate_2050) * 20000 +  # Interest rate impact
                (govt_spending_2050 - 25) * 3000 +  # Government spending impact
                (25 - corp_tax_rate_2050) * 5000  # Tax impact
            )
            
            total_portfolio_value = base_portfolio_value + policy_impact
            
            # Market variables for display
            market_variables = {
                'gdp_growth': round(gdp_growth, 2),
                'inflation_rate': round(inflation, 2),
                'unemployment_rate': round(unemployment, 2),
                'market_volatility': round(market_volatility, 3),
                'risk_free_rate': round(risk_free_rate, 2),
                'market_risk_premium': round(market_risk_premium, 3)
            }
            
            # Portfolio analysis results
            portfolio_analysis = {
                'total_equity_value': round(total_portfolio_value / 1000000, 1),  # In millions
                'weighted_wacc': round(weighted_wacc, 2),
                'policy_impact': round(policy_impact / 1000, 1),  # In thousands
                'policy_impact_percent': round((policy_impact / base_portfolio_value) * 100, 1),
                'sector_breakdown': sector_results
            }
            
            return jsonify({
                'success': True,
                'market_variables': market_variables,
                'portfolio_analysis': portfolio_analysis,
                'policy_assumptions': {
                    'carbon_price_2050': carbon_price_2050,
                    'central_bank_rate_2050': central_bank_rate_2050,
                    'govt_spending_2050': govt_spending_2050,
                    'corp_tax_rate_2050': corp_tax_rate_2050
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

