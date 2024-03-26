from contract_portfolio import ContractPortfolio
import matplotlib.pyplot as plt

contract_portfolio = ContractPortfolio()
portfolio_returns = contract_portfolio.get_returns()

# Graph box-plot of portfolio returns
plt.boxplot(portfolio_returns)
plt.title('Box-Plot of Portfolio Returns')
plt.show()

