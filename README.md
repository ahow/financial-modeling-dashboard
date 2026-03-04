# Comprehensive Financial Modeling Dashboard

This repository contains the source code for a sophisticated financial modeling and valuation dashboard. The application is designed to provide a professional platform for economic modeling, integrating macroeconomic variables with company-specific valuation drivers for comprehensive investment analysis. It features Monte Carlo simulations, multi-scenario analysis, and interactive visualizations to empower users with deep financial insights.

## Table of Contents

- [Project Objective](#project-objective)
- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Application Structure](#application-structure)
- [Backend Development (Flask)](#backend-development-flask)
- [Frontend Development (HTML-JS)](#frontend-development-html-js)
- [Setup and Local Execution](#setup-and-local-execution)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)

## Project Objective

The primary objective of this application is to provide a comprehensive and interactive tool for financial analysis and company valuation. It aims to bridge the gap between high-level macroeconomic trends and their direct impact on company performance and valuation. By offering a multi-scenario framework and advanced visualization capabilities, the dashboard enables users to explore complex financial systems, test various economic assumptions, and make more informed investment decisions.

## Key Features

The dashboard is equipped with a wide range of features designed for in-depth financial analysis:

- **Multi-Tab Interface**: A clean, organized interface with dedicated tabs for different analysis modules:
  - **Global Scenario**: Analyze and configure global macroeconomic scenarios.
  - **Company Analysis**: Input company-specific data and run valuation models.
  - **Variable Evolution**: Visualize the time-series evolution of all system variables.
  - **Methodology**: A section explaining the underlying models and assumptions.

- **Interactive Scenario Modeling**: Users can select from four pre-defined economic scenarios (Base Case, Optimistic, Pessimistic, Crisis) or customize their own by adjusting key policy variables.

- **Interactive Policy Charts**: The "Global Scenario" tab features draggable charts for key policy variables, allowing users to create custom forecasts for:
  - Carbon Price
  - Central Bank Rate
  - Government Spending
  - Corporate Tax Rate

- **Monte Carlo Valuation Engine**: The backend is powered by a robust Monte Carlo simulation engine that generates 10,000 valuation outcomes for a given company. This provides a full probability distribution of potential valuations rather than a single point estimate.

- **Multi-Scenario Distribution Analysis**: The application can generate and display valuation distributions for all four economic scenarios simultaneously, allowing for a clear comparison of potential outcomes under different macroeconomic conditions.

- **Comprehensive Variable Evolution**: The "Variable Evolution" tab provides a powerful tool for visualizing the historical and projected evolution of over a dozen key variables, including:
  - **Exogenous (Policy) Variables**: Carbon Price, Central Bank Rate, etc.
  - **Endogenous (Economic) Variables**: GDP Growth, Inflation, Unemployment, etc.
  - **Company-Level Variables**: Revenue Growth, Profit Margin, ROE.
  - **Climate Variables**: Temperature Anomaly, Renewable Energy Share.

- **Advanced Visualizations**: All data is presented through professionally designed charts using Chart.js, including line charts, histograms, and multi-axis time-series visualizations.

- **ESG Integration**: The model allows for the input of Environmental, Social, and Governance (ESG) metrics, which can be used to adjust valuation models and assess non-financial risks and opportunities.

## Technical Architecture

The application is built on a modern web stack, with a clear separation between the frontend and backend. This architecture ensures modularity, scalability, and ease of maintenance.

- **Frontend**: A single-page application (SPA) built with vanilla **HTML**, **CSS**, and **JavaScript**. It uses the **Chart.js** library for all data visualizations.
- **Backend**: A lightweight and powerful backend server built with **Python** and the **Flask** web framework. It exposes a set of RESTful APIs for the frontend to consume.
- **Data Analysis**: The backend leverages popular Python libraries like **NumPy** and **Pandas** for numerical operations and data manipulation, although for this specific application, the core logic is implemented in standard Python.
- **Deployment**: The application is designed to be deployed easily using a production-ready web server like **Gunicorn** and can be hosted on any platform that supports Python applications.

## Application Structure

The project is organized into a clean and logical directory structure to facilitate development and collaboration.

```
/financial-modeling-dashboard
├── .gitignore
├── README.md
├── backend/
│   ├── app.py
│   └── requirements.txt
├── docs/
│   └── variable_evolution_design.md
├── frontend/
│   └── comprehensive_dashboard.html
└── models/
    └── monte_carlo_valuation.py
```

- **`backend/`**: Contains the Flask application (`app.py`) and its Python dependencies (`requirements.txt`).
- **`docs/`**: Includes all project documentation, such as design documents and technical specifications.
- **`frontend/`**: Holds the main HTML file for the dashboard, which includes all the CSS and JavaScript code.
- **`models/`**: Contains the core financial modeling logic, including the Monte Carlo simulation engine.

## Backend Development (Flask)

The backend is a Flask application responsible for handling the core business logic and data processing. It exposes several API endpoints that the frontend consumes to populate the dashboard with data.

### Key File: `backend/app.py`

This file contains the entire Flask application. It defines the API endpoints, handles incoming requests, and orchestrates the financial calculations.

### API Endpoints

The application exposes the following key endpoints:

- **`/` and `/comprehensive_dashboard.html`**: These routes serve the main `comprehensive_dashboard.html` file to the user's browser.

- **`/api/company/distributions` (POST, GET)**: This is the primary endpoint for running the Monte Carlo valuation analysis. It accepts company-specific financial data as a JSON payload in a POST request and returns a comprehensive analysis, including valuation distributions for all four economic scenarios. A GET request to this endpoint will run the analysis with default data for testing purposes.

- **`/api/company/distributions/test` (GET)**: A dedicated test endpoint to quickly verify that the multi-scenario Monte Carlo engine is functioning correctly. It returns a summary of the distribution statistics for each scenario.

- **`/api/enhanced/analyze-curves` (POST)**: This endpoint is part of the original, more complex version of the model and is used to analyze the impact of the interactive policy curves on various market and portfolio metrics. It takes the user-defined policy assumptions and calculates their impact on GDP growth, inflation, unemployment, and other key variables.

### Monte Carlo Simulation Logic

The core of the backend is the Monte Carlo simulation engine, which is implemented within the `/api/company/distributions` endpoint. The process is as follows:

1.  **Input Data**: The endpoint receives the company's market cap, revenue, EBITDA margin, revenue growth, and sector.
2.  **Scenario Parameters**: The application defines a set of parameters for each of the four economic scenarios (Base, Optimistic, Pessimistic, Crisis). These parameters include the mean return and volatility for the valuation simulations.
3.  **Simulation Loop**: For each scenario, the application runs 10,000 simulations. In each simulation, a random shock is generated based on the scenario's mean return and volatility. This shock is then applied to the company's base valuation.
4.  **Realistic Bounds and Crisis Modeling**: The model incorporates realistic constraints. For the "Crisis" scenario, there is a 10% probability of complete bankruptcy (valuation goes to zero). For other scenarios, the valuation is bounded to a reasonable range (e.g., 10% to 300% of the base valuation) to prevent unrealistic outcomes.
5.  **Statistical Analysis**: After running all simulations for a scenario, the application calculates a range of statistics, including the mean, median, confidence intervals, and Value at Risk (VaR).
6.  **API Response**: The final API response includes the detailed statistical analysis and the raw distribution data for all four scenarios, which the frontend then uses to generate the valuation charts.

## Frontend Development (HTML/JS)

The frontend is a self-contained HTML file that includes all the necessary CSS for styling and JavaScript for interactivity. It provides a rich user interface for interacting with the financial models and visualizing the results.

### Key File: `frontend/comprehensive_dashboard.html`

This single file contains the entire user interface. It is structured as follows:

- **HTML Structure**: The file is organized into a series of tabs, with each tab containing different modules for analysis. The main tabs are "Global Scenario," "Company Analysis," and "Variable Evolution."
- **CSS Styling**: All the styling is included within a `<style>` block in the `<head>` of the document. It provides a modern and professional look and feel for the dashboard, with a responsive design that adapts to different screen sizes.
- **JavaScript Logic**: The core of the frontend interactivity is handled by a large block of JavaScript code at the end of the file. This code is responsible for:
    - **Tab Switching**: The `showTab()` function manages the display of different tabs.
    - **API Communication**: The `generateValuationDistributions()` function makes an API call to the backend to fetch the Monte Carlo simulation results.
    - **Chart Rendering**: The application uses the **Chart.js** library to create all the visualizations. Key functions like `createCombinedDistributionChart()` and `initializeVariableEvolutionChart()` are responsible for creating and updating the charts.
    - **Interactive Elements**: The frontend includes several interactive elements, such as sliders, dropdowns, and draggable charts. The JavaScript code handles the events from these elements and updates the application state accordingly.

### Key JavaScript Functions

- **`showTab(tabName)`**: Manages the visibility of the different tabs in the dashboard.
- **`generateValuationDistributions()`**: Fetches the company's financial data from the input fields, sends it to the backend's `/api/company/distributions` endpoint, and then uses the response to populate the valuation metrics and render the distribution chart.
- **`createCombinedDistributionChart(data)`**: Takes the multi-scenario distribution data from the API and creates the valuation distribution line chart, with a separate line for each economic scenario.
- **`InteractivePolicyCharts` class**: A dedicated class for managing the four interactive policy charts in the "Global Scenario" tab. It handles the dragging functionality and updates the underlying policy data.
- **`initializeVariableEvolutionChart()` and `updateVariableChart()`**: These functions are responsible for creating and updating the main time-series chart in the "Variable Evolution" tab. They gather the user's selections, generate the appropriate data, and update the Chart.js instance.

## Setup and Local Execution

To run the application on your local machine, you will need to have Python and pip installed. Follow these steps to get the application running:

1.  **Clone the Repository**: Clone this GitHub repository to your local machine.

2.  **Install Dependencies**: Navigate to the `backend` directory and install the required Python packages using pip:

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Run the Backend Server**: Once the dependencies are installed, you can start the Flask development server:

    ```bash
    python app.py
    ```

    The backend server will start on `http://127.0.0.1:5000`.

4.  **Open the Frontend**: Open the `frontend/comprehensive_dashboard.html` file in your web browser. The application will load, and you can start interacting with the dashboard.

## Deployment

For a production deployment, it is recommended to use a production-ready web server like **Gunicorn** or **uWSGI** to serve the Flask application. Here is a basic example of how to run the application with Gunicorn:

```bash
cd backend
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

This command will start Gunicorn with four worker processes, making the application accessible on port 5000 of the server. You would then typically use a reverse proxy like **Nginx** or **Apache** to manage incoming traffic and serve the application to the public.

## Future Enhancements

This application provides a solid foundation for a comprehensive financial modeling platform. There are several potential enhancements that could be added in the future:

-   **User Authentication**: Implement user accounts to allow users to save their analyses and custom scenarios.
-   **Database Integration**: Connect the application to a database to store historical data, user settings, and saved scenarios.
-   **More Advanced Models**: Incorporate more sophisticated financial models, such as discounted cash flow (DCF) analysis, real options modeling, and advanced time-series forecasting.
-   **Expanded ESG Factors**: Integrate a wider range of ESG data and develop more nuanced models for assessing their impact on valuation.
-   **Real-Time Data Feeds**: Connect the application to real-time data feeds for stock prices, economic data, and news.
-   **Customizable Dashboards**: Allow users to create and customize their own dashboards with the charts and metrics that are most important to them.
