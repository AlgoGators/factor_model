Factor Model Explanation

1. Overview:
    This project contains a factor model implementation designed for financial data analysis, 
    specifically for constructing and analyzing portfolios based on various financial factors.

2. Files and Classes:
- main.py
     - This is the entry point of the application. It initializes the portfolios, performs data preparation and cleaning, 
     standardizes features, executes a grid search to find optimal parameters for Lasso and ElasticNet models, 
     and finally performs regression analyses using Linear, Lasso, Ridge, and ElasticNet models.

- portfolio.py
    - An abstract base class that defines the structure for portfolio classes. It requires the implementation of initialize_components() and aggregate_returns() methods.
    
- contract_portfolio.py
    - A subclass of Portfolio that is specialized for managing a portfolio of contracts. It implements methods to initialize contract components and aggregate their returns.
    
- factor_portfolio.py
    - Another subclass of Portfolio, tailored for factor portfolios. It initializes factor components and aggregates their returns, similar to ContractPortfolio.
    
- factor.py
    - Defines the Factor class, which is responsible for fetching and processing financial data for a given ticker. It includes methods to download historical data, calculate returns, and access the processed data.
    
- portfolio_utils.py
    - Contains utility functions for data preparation and regression analysis:

      - prepare_data(): Joins and cleans portfolio and factor returns data.
      - perform_grid_search(): Finds the optimal alpha parameters for Lasso and ElasticNet.
      - perform_different_regressions(): Fits Linear, Lasso, Ridge, and ElasticNet models.
      - plot_regression_results(): Plots the regression results on a given axes object.
      - calculate_adjusted_r_squared(): Calculates the R-squared and adjusted R-squared values.
3. Model Workflow
- The main.py script initiates the process by creating portfolios and retrieving their returns.
- The data is then cleaned and standardized.
- Optimal hyperparameters for certain regression models are determined via grid search.
- Different types of regressions are performed.
- The results, including regression plots, are displayed for analysis.