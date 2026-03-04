# Technical Documentation: Comprehensive Financial Modeling Dashboard

**Author**: Manus AI  
**Version**: 1.0  
**Date**: March 2026  
**Live Demo**: https://mzhyi8cn7gy0.manus.space/comprehensive_dashboard.html  
**GitHub Repository**: https://github.com/ahow/financial-modeling-dashboard

---

## 1. Executive Summary

This document provides a comprehensive technical description of the Comprehensive Financial Modeling Dashboard — a professional web application designed for economic modeling, company valuation analysis, and investment scenario planning. The application integrates macroeconomic variables with company-specific financial drivers, enabling users to explore how global policy decisions, economic cycles, and climate pathways affect company valuations over a 30-year horizon.

The platform was built to address a specific analytical need: the ability to move beyond single-point valuation estimates and instead understand the full probability distribution of outcomes under different economic regimes. By combining a Monte Carlo simulation engine with interactive scenario modeling and rich time-series visualizations, the dashboard provides a level of analytical depth typically found only in institutional-grade financial tools.

---

## 2. Project Objectives

The application was designed to achieve the following core objectives:

**Objective 1 — Probabilistic Valuation**: Replace static, single-point valuation models with a Monte Carlo simulation engine that generates full probability distributions of company valuations, providing a statistically rigorous basis for investment decisions.

**Objective 2 — Multi-Scenario Analysis**: Enable simultaneous comparison of four distinct economic scenarios — Base Case, Optimistic, Pessimistic, and Crisis — to understand the range of potential outcomes and their relative likelihoods.

**Objective 3 — Policy Impact Modeling**: Allow users to interactively adjust key macroeconomic policy variables (carbon price, central bank rates, government spending, corporate tax rates) and observe their downstream effects on company valuations and economic indicators.

**Objective 4 — Long-Horizon Visualization**: Provide a comprehensive view of how all key variables — from macroeconomic indicators to company-level metrics and climate variables — are expected to evolve from 2017 to 2050.

**Objective 5 — Accessibility**: Deliver these capabilities through an intuitive, browser-based interface that requires no specialized software installation, making sophisticated financial modeling accessible to a broader audience.

---

## 3. Technical Architecture

The application follows a classic client-server architecture, with a clear separation between the presentation layer (frontend) and the business logic layer (backend).

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML5, CSS3, JavaScript (ES6+) | User interface and interactive visualizations |
| Visualization | Chart.js (CDN) | All charts, graphs, and interactive plots |
| Backend | Python 3.11, Flask 2.3+ | REST API, Monte Carlo engine, financial calculations |
| CORS Handling | Flask-CORS | Cross-Origin Resource Sharing for API access |
| Production Server | Gunicorn | WSGI server for production deployment |
| Deployment Platform | Manus.space | Permanent public hosting |

### 3.1 Data Flow

The data flow within the application follows a straightforward request-response cycle. When a user interacts with the dashboard — for example, by clicking "Generate Valuation Distributions" — the frontend JavaScript collects the relevant input values from the form fields and constructs a JSON payload. This payload is sent to the Flask backend via a `POST` request to the `/api/company/distributions` endpoint. The backend processes the request, runs the Monte Carlo simulation, and returns a JSON response containing the full statistical analysis and raw distribution data. The frontend then parses this response and uses Chart.js to render the visualization.

For the "Variable Evolution" and "Global Scenario" tabs, all data generation and chart rendering is handled entirely on the frontend using pre-defined datasets embedded in the JavaScript code. This design choice eliminates unnecessary API calls for data that does not change based on user input, resulting in a faster and more responsive user experience.

---

## 4. Backend: Flask Application (`backend/app.py`)

The backend is a single-file Flask application that serves both the static frontend and the analytical API endpoints.

### 4.1 Application Factory

The application uses the Flask application factory pattern, where a `create_app()` function is responsible for creating and configuring the Flask application instance. This pattern is a best practice for Flask applications as it makes the application more modular and easier to test. CORS is enabled globally for all routes using the `flask-cors` library to allow the frontend to make API calls without browser security restrictions.

### 4.2 API Endpoints

The application exposes the following RESTful API endpoints:

**`GET /` and `GET /comprehensive_dashboard.html`**

These routes serve the main `comprehensive_dashboard.html` file from the `static` directory. The Flask `send_from_directory` function is used to serve the file securely.

**`POST /api/company/distributions`**

This is the primary analytical endpoint. It accepts a JSON payload with the following fields:

| Field | Type | Description | Default |
|---|---|---|---|
| `market_cap` | `float` | Company market capitalization in billions ($B) | 50 |
| `revenue` | `float` | Annual revenue in billions ($B) | 25 |
| `ebitda_margin` | `float` | EBITDA margin as a percentage | 22 |
| `revenue_growth` | `float` | Annual revenue growth rate as a percentage | 8 |
| `sector` | `string` | Industry sector (e.g., "technology", "healthcare") | "technology" |

The endpoint returns a JSON object with the following key fields:

- `success`: Boolean indicating whether the analysis succeeded.
- `mean_valuation`: The mean valuation from the base case simulation (in $B).
- `median_valuation`: The median valuation from the base case simulation (in $B).
- `confidence_interval_90`: A two-element array representing the 10th and 90th percentile valuations (in $B).
- `value_at_risk_95`: The 5th percentile valuation, representing the 95% Value at Risk (in $B).
- `distribution_data`: An array of 10,000 raw valuation outcomes from the base case simulation (in $B).
- `all_scenarios`: A dictionary containing the full statistical analysis and distribution data for all four scenarios (base, optimistic, pessimistic, crisis).

**`GET /api/company/distributions/test`**

A lightweight test endpoint that runs the Monte Carlo simulation with default parameters and returns a summary of the results. This is useful for verifying that the backend is functioning correctly.

**`POST /api/enhanced/analyze-curves`**

This endpoint analyzes the impact of user-defined policy curves on a range of market and portfolio metrics. It accepts a JSON payload containing the user's policy assumptions (carbon price, central bank rate, government spending, and corporate tax rate for 2050) and returns calculated values for GDP growth, inflation, unemployment, market volatility, WACC, and sector-level equity values.

### 4.3 Monte Carlo Simulation Engine

The Monte Carlo engine is the core of the application's analytical capability. The simulation process is described below.

**Step 1 — Scenario Parameterization**: For each of the four economic scenarios, a set of parameters is defined: a mean return and a volatility. These parameters reflect the expected economic conditions under each scenario.

| Scenario | Mean Return | Volatility | Description |
|---|---|---|---|
| Base Case | 0.0% | 25% | Steady-state economic conditions |
| Optimistic | +15% | 20% | Strong growth, lower uncertainty |
| Pessimistic | -15% | 30% | Economic slowdown, higher uncertainty |
| Crisis | -40% | 35% | Severe downturn with bankruptcy risk |

**Step 2 — Simulation Loop**: For each scenario, the engine runs 10,000 independent simulations. In each simulation, a random shock is drawn from a normal distribution with the scenario's mean return and volatility. This shock is then applied multiplicatively to the company's base valuation (derived from its market cap).

**Step 3 — Boundary Conditions**: To ensure realistic outcomes, the simulated valuations are bounded. For the Base, Optimistic, and Pessimistic scenarios, the valuation is capped between 10% and 300% of the base valuation. For the Crisis scenario, an additional 10% probability of complete bankruptcy (zero valuation) is applied before the standard bounds are enforced.

**Step 4 — Statistical Aggregation**: After the simulation loop, the engine calculates a comprehensive set of statistics from the 10,000 outcomes, including the mean, median, the 5th, 10th, 90th, and 95th percentiles, and the 90% confidence interval.

### 4.4 Policy Impact Model

The `/api/enhanced/analyze-curves` endpoint implements a simplified systems model that translates policy variable assumptions into economic outcomes. The key relationships modeled are:

- **GDP Growth** is positively influenced by government spending and negatively influenced by high interest rates.
- **Inflation** is negatively influenced by higher interest rates (monetary tightening) and positively influenced by higher government spending.
- **Unemployment** is inversely related to GDP growth, following an approximation of Okun's Law.
- **WACC** for each sector is calculated using the Capital Asset Pricing Model (CAPM), with the risk-free rate set equal to the central bank rate and the market risk premium adjusted for market volatility.

---

## 5. Frontend: Dashboard Interface (`frontend/comprehensive_dashboard.html`)

The frontend is a single-page application built with vanilla HTML, CSS, and JavaScript. It is designed to be self-contained and requires no build tools or package managers to run.

### 5.1 User Interface Structure

The interface is organized into four main tabs, each serving a distinct analytical purpose.

**Tab 1: Global Scenario**

This tab is the starting point for the analysis. It allows users to configure the global macroeconomic environment. The key feature of this tab is the set of four interactive policy charts, which display the historical trajectory and projected future values of Carbon Price, Central Bank Rate, Government Spending, and Corporate Tax Rate. Users can drag the red data points on each chart to adjust the 2030, 2040, and 2050 projections, creating a custom economic forecast. The tab also includes a Climate Scenario section for selecting a climate pathway (1.5°C, 2°C, or 3°C+) and a transition speed.

**Tab 2: Company Analysis**

This tab is the primary interface for company-specific analysis. Users input the company's fundamental financial data (market cap, revenue, EBITDA margin, revenue growth, sector), ESG metrics (carbon intensity, renewable energy usage, employee turnover, gender pay gap, board independence), and additional financial metrics (debt-to-equity ratio, ROE, FCF margin, R&D investment). Two action buttons are available: "Analyze Company" for a quick qualitative assessment, and "Generate Valuation Distributions" to trigger the Monte Carlo simulation and display the full probability distribution chart.

**Tab 3: Variable Evolution**

This tab provides a comprehensive time-series view of all key variables in the system. A variable selection panel on the left allows users to choose which variables to display by checking or unchecking boxes. Variables are organized into four categories: Exogenous (Policy), Endogenous (Economic), Company-Level, and Climate. The main chart area on the right displays the selected variables over the chosen time range (2017–2030, 2017–2040, or 2017–2050), with historical data shown as solid lines and projections shown as dashed lines. A scenario selector allows users to switch between the four economic scenarios to see how the projected trajectories change.

**Tab 4: Methodology**

This tab provides a narrative explanation of the underlying models, assumptions, and data sources used in the application.

### 5.2 Key JavaScript Components

**Tab Management (`showTab`, `showGlobalScenario`, `showVariableEvolution`)**

The `showTab()` function is the core of the tab-switching mechanism. It iterates over all tab content elements and removes the `active` class, then adds it back to the selected tab. Specialized wrapper functions (`showGlobalScenario`, `showVariableEvolution`) are used for tabs that require chart initialization upon first display. These functions check whether the charts have already been initialized and, if not, call the appropriate initialization function after a short delay to allow the DOM to render.

**Interactive Policy Charts (`InteractivePolicyCharts` class)**

This is the most complex JavaScript component in the application. It is implemented as a class with the following key methods:

- `init()`: Iterates over the four policy variables and calls `createInteractiveChart()` for each one.
- `createInteractiveChart(variable)`: Creates a Chart.js line chart for a given policy variable. The chart displays both historical data (2017–2023) and three projection points (2030, 2040, 2050). The projection points are rendered as larger red dots to visually distinguish them from the historical data. The chart uses the `segment` configuration option to render the projection portion of the line as a dashed line.
- `setupDragInteraction(chart, variable)`: Attaches mouse event listeners to the chart canvas to enable the drag-and-drop functionality for the projection points. When a user clicks and drags one of the red projection dots, the underlying data value is updated in real time, and the chart is re-rendered.
- `updateGlobalProjections()`: Reads the current projection values from all four policy charts and updates the summary metrics displayed at the bottom of the "Global Scenario" tab.

**Monte Carlo Visualization (`generateValuationDistributions`, `createCombinedDistributionChart`)**

The `generateValuationDistributions()` function is the event handler for the "Generate Valuation Distributions" button. It collects the company's financial data from the input fields, sends a POST request to the `/api/company/distributions` endpoint, and then calls `createCombinedDistributionChart()` with the response data. The `createCombinedDistributionChart()` function processes the raw simulation data for each scenario, bins it into a histogram with 20 bins, converts the bin counts to percentages, and renders a multi-line Chart.js chart with a separate line for each scenario.

**Variable Evolution Chart (`variableDefinitions`, `initializeVariableEvolutionChart`, `updateVariableChart`)**

The `variableDefinitions` object is a dictionary that serves as the data store for the Variable Evolution tab. It contains an entry for each of the 13 variables, with the following properties: `name`, `color`, `yAxisID`, `historical` (an array of 7 historical values for 2017–2023), and `projections` (an object containing four arrays of projected values — one for each economic scenario — covering the period from 2024 to 2050 in 4-year intervals).

The `initializeVariableEvolutionChart()` function creates the Chart.js instance for the Variable Evolution tab. It initializes the chart with empty data and a dual-axis configuration (a left Y-axis for percentage values and a right Y-axis for absolute values like stock indices and carbon prices). After initialization, it immediately calls `updateVariableChart()` to populate the chart with the default selections.

The `updateVariableChart()` function is called whenever the user changes a checkbox, the time range, or the scenario. It reads the current state of all checkboxes and the dropdown selectors, generates the appropriate year labels and data arrays, and updates the Chart.js instance. For each selected variable, it creates two datasets: one for the historical data (solid line) and one for the projection data (dashed line). The two datasets are connected by sharing the last historical data point as the first point of the projection dataset, creating a seamless visual transition.

### 5.3 Data Model for Variable Evolution

The historical data embedded in the `variableDefinitions` object is based on real-world economic data for the period 2017–2023. The projection data for each scenario is based on the following economic assumptions:

| Variable | Base Case Trend | Optimistic Trend | Pessimistic Trend | Crisis Trend |
|---|---|---|---|---|
| Carbon Price | Gradual increase to $200/tCO2 by 2050 | Rapid increase to $240/tCO2 | Slow increase to $160/tCO2 | Stagnation at $120/tCO2 |
| Central Bank Rate | Gradual decline to 3.5% | Moderate decline to 3.5% | Aggressive cuts to 2.5% | Emergency cuts to near-zero |
| GDP Growth | Stable at ~2.5–3.0% | Strong at ~3.0–4.5% | Weakening to ~0.5–2.0% | Deep recession then recovery |
| Inflation | Convergence to 2.0% target | Below-target at ~1.5% | Persistent above-target at ~5.0% | Stagflation spike then normalization |
| Unemployment | Gradual improvement to ~3.3% | Full employment at ~1.5% | Rising to ~8.0% | Spike to ~12% then recovery |
| Temperature Anomaly | +2.1°C by 2050 | +1.58°C (Paris-aligned) | +2.58°C | +3.50°C (high-emission) |
| Renewable Energy | 70% share by 2050 | 85% share (rapid transition) | 55% share (slow transition) | 42% share (delayed transition) |

---

## 6. Deployment

The application is deployed on the **Manus.space** platform and is publicly accessible at the following URL:

**https://mzhyi8cn7gy0.manus.space/comprehensive_dashboard.html**

The deployment consists of the Flask backend running as a persistent web service, serving both the static frontend file and the analytical API endpoints. The `static` folder in the Flask application's configuration points to the directory containing the `comprehensive_dashboard.html` file, allowing Flask to serve it directly.

### 6.1 Local Development Setup

To run the application locally, follow these steps:

```bash
# 1. Clone the repository
git clone https://github.com/ahow/financial-modeling-dashboard.git
cd financial-modeling-dashboard

# 2. Install Python dependencies
cd backend
pip install -r requirements.txt

# 3. Run the Flask development server
python app.py

# 4. Open the dashboard in your browser
# Navigate to http://127.0.0.1:5000 in your browser
```

### 6.2 Production Deployment with Gunicorn

For a production environment, use Gunicorn as the WSGI server:

```bash
cd backend
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## 7. Known Issues and Limitations

The following known issues and limitations are present in the current version of the application:

**Variable Evolution Chart Initialization**: The Variable Evolution chart requires the tab to be clicked before it initializes. This is by design, as Chart.js cannot render a chart in a hidden `div`. The `showVariableEvolution()` function handles this initialization on first click.

**Projection Data Granularity**: The projection data in the `variableDefinitions` object is defined at 4-year intervals (2024, 2028, 2032, etc.) but is interpolated linearly by the `updateVariableChart()` function when the full year-by-year timeline is requested. This linear interpolation may not accurately represent the expected non-linear dynamics of some variables.

**Monte Carlo Seed**: The Monte Carlo simulation uses a fixed random seed (`random.seed(42)`) for reproducibility. This means that the simulation results will be identical on every run, which is useful for testing but may not reflect the true stochasticity of the model. This seed is reset for each scenario, which means the scenarios are not independent draws from the same random process.

**Simplified Policy Impact Model**: The policy impact model in the `/api/enhanced/analyze-curves` endpoint uses simplified linear relationships between policy variables and economic outcomes. A more realistic model would incorporate non-linear dynamics, feedback loops, and time lags.

---

## 8. Developer Guide: Recreating the Application

A developer wishing to recreate this application from scratch should follow these steps:

**Step 1 — Set Up the Project Structure**: Create the directory structure as described in the "Application Structure" section of the README.

**Step 2 — Build the Flask Backend**: Create the `backend/app.py` file. Start with the application factory pattern, enabling CORS. Implement the `/api/company/distributions` endpoint with the Monte Carlo simulation logic as described in Section 4.3. Implement the `/api/enhanced/analyze-curves` endpoint with the policy impact model as described in Section 4.4.

**Step 3 — Build the Frontend HTML Structure**: Create the `frontend/comprehensive_dashboard.html` file. Build the four-tab structure using `div` elements with `class="tab-content"` and `id` attributes corresponding to each tab name. Create the form inputs for the Company Analysis tab and the variable selection checkboxes for the Variable Evolution tab.

**Step 4 — Add CSS Styling**: Add the CSS styles within a `<style>` block in the `<head>`. Key styles to implement include the gradient background, the card-based layout for sections, the tab button active state, and the responsive grid layouts.

**Step 5 — Implement Tab Switching**: Implement the `showTab()` function in JavaScript. This function should remove the `active` class from all tab content elements and tab buttons, then add it to the selected ones.

**Step 6 — Implement the Interactive Policy Charts**: Implement the `InteractivePolicyCharts` class. Define the historical data and default projection values for each of the four policy variables. Use Chart.js to create the charts, using the `segment` configuration to render the projection portion as a dashed line. Implement the drag interaction using `mousedown`, `mousemove`, and `mouseup` event listeners on the canvas.

**Step 7 — Implement the Monte Carlo Visualization**: Implement the `generateValuationDistributions()` function to call the backend API and the `createCombinedDistributionChart()` function to render the results.

**Step 8 — Implement the Variable Evolution Chart**: Define the `variableDefinitions` object with historical and projection data for all 13 variables. Implement `initializeVariableEvolutionChart()` to create the Chart.js instance with a dual-axis configuration. Implement `updateVariableChart()` to dynamically generate datasets based on the user's checkbox selections and scenario choice.

**Step 9 — Connect the Frontend and Backend**: Ensure that the API calls in the frontend JavaScript are pointing to the correct backend URL. For local development, this will be `http://127.0.0.1:5000`. For production, update the URL to the deployed backend's address.

**Step 10 — Test and Deploy**: Test the application thoroughly, verifying that all charts render correctly, all API calls succeed, and all interactive elements function as expected. Deploy the application to a production server using Gunicorn.
