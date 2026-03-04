# Variable Evolution Tab Design

## Overview
Create a comprehensive time series visualization showing the expected evolution of both exogenous (policy) and endogenous (economic/financial) variables over time, with interactive variable selection.

## Tab Structure

### Tab Name: "📈 Variable Evolution"

## Interface Design

### 1. Variable Selection Panel (Left Side)
```
┌─ Variable Categories ─────────────────┐
│ □ Select All / Deselect All          │
│                                       │
│ 🏛️ Exogenous (Policy) Variables      │
│ ☑ Carbon Price ($/tCO2)              │
│ ☑ Central Bank Rate (%)              │
│ ☑ Government Spending (% GDP)        │
│ ☑ Corporate Tax Rate (%)             │
│                                       │
│ 📊 Endogenous (Economic) Variables   │
│ ☑ GDP Growth Rate (%)                │
│ ☑ Inflation Rate (%)                 │
│ ☑ Unemployment Rate (%)              │
│ ☑ Stock Market Index                 │
│ ☑ Corporate Earnings Growth (%)      │
│ ☑ Interest Rate Spread (%)           │
│                                       │
│ 🏢 Company-Level Variables           │
│ ☑ Revenue Growth (%)                 │
│ ☑ Profit Margin (%)                  │
│ ☑ ROE (%)                            │
│ ☑ Debt-to-Equity Ratio              │
│ ☑ ESG Score                          │
│                                       │
│ 🌡️ Climate Variables                │
│ ☑ Global Temperature Anomaly (°C)    │
│ ☑ Carbon Emissions (GtCO2)           │
│ ☑ Renewable Energy Share (%)         │
└───────────────────────────────────────┘
```

### 2. Time Series Chart (Right Side)
```
┌─ Variable Evolution Over Time ────────────────────────────────────┐
│                                                                   │
│  Variable Evolution (2017-2050)                                  │
│                                                                   │
│  [Large Chart.js time series with multiple y-axes]               │
│  - Left Y-axis: Percentage values (%, rates)                     │
│  - Right Y-axis: Absolute values (prices, indices)               │
│  - X-axis: Years (2017-2050)                                     │
│  - Different colors for each variable                            │
│  - Legend showing selected variables                             │
│                                                                   │
│  Time Range: [2017-2030] [2017-2040] [2017-2050]                │
│  Scenario: [Base Case ▼] [Show Confidence Bands ☑]              │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Data Structure

### Variable Categories
1. **Exogenous Variables** (User-controlled policy inputs)
   - Carbon Price: Historical + projections from interactive charts
   - Central Bank Rate: Historical + projections from interactive charts
   - Government Spending: Historical + projections from interactive charts
   - Corporate Tax Rate: Historical + projections from interactive charts

2. **Endogenous Variables** (Model-calculated economic outcomes)
   - GDP Growth Rate: Calculated from economic model
   - Inflation Rate: Derived from monetary policy and economic conditions
   - Unemployment Rate: Function of GDP growth and economic cycle
   - Stock Market Index: Based on economic fundamentals and sentiment
   - Corporate Earnings Growth: Function of GDP, tax rates, and sector dynamics
   - Interest Rate Spread: Credit risk premium based on economic conditions

3. **Company-Level Variables** (Firm-specific outcomes)
   - Revenue Growth: Function of sector growth and company positioning
   - Profit Margin: Impact of costs, competition, and efficiency
   - ROE: Return on equity based on profitability and leverage
   - Debt-to-Equity: Capital structure evolution
   - ESG Score: Environmental and governance improvements over time

4. **Climate Variables** (Environmental indicators)
   - Global Temperature Anomaly: Climate science projections
   - Carbon Emissions: Function of carbon pricing and policy
   - Renewable Energy Share: Energy transition modeling

## Technical Implementation

### Frontend Components
1. **Variable Selection Checkboxes**
   - Grouped by category with expand/collapse
   - Select All / Deselect All functionality
   - Color coding for each variable

2. **Time Series Chart**
   - Chart.js with multiple datasets
   - Dual Y-axes for different scales
   - Interactive legend
   - Zoom and pan functionality
   - Confidence bands for projections

3. **Controls**
   - Time range selector (2030/2040/2050)
   - Scenario selector (Base/Optimistic/Pessimistic/Crisis)
   - Confidence band toggle

### Backend Data Generation
1. **Historical Data (2017-2023)**
   - Real economic data for calibration
   - Actual policy variables
   - Historical company performance

2. **Projection Data (2024-2050)**
   - Economic model calculations
   - Policy scenario impacts
   - Climate pathway effects
   - Company evolution modeling

### API Endpoints
- `/api/variables/evolution` - Get all variable time series data
- `/api/variables/categories` - Get variable categories and metadata
- `/api/variables/scenarios` - Get scenario-specific projections

## User Experience Flow
1. User opens "Variable Evolution" tab
2. Default view shows key variables selected (GDP, Inflation, Carbon Price)
3. User can check/uncheck variables to customize view
4. Chart updates in real-time as selections change
5. User can adjust time range and scenario
6. Hover tooltips show exact values and dates
7. Export functionality for data and charts

## Benefits
- **Comprehensive View**: See all variables in one place
- **Relationship Analysis**: Understand how variables interact over time
- **Scenario Comparison**: Compare different economic pathways
- **Policy Impact**: See how exogenous changes affect endogenous outcomes
- **Long-term Planning**: Visualize 30-year evolution trajectories

