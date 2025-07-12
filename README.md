# Stock Data Explorer

A command-line tool/interface (CLI) to analyze historical stock data using Python, yfinance, and matplotlib.

## Features

- Analyze a stock by ticker and date range
- Calculate key summary statistics:
  - Opening and closing prices
  - Average, highest, and lowest closing prices
  - Daily and annualized volatility
  - Total return percentage
  - Average daily volume
- Save analysis results to CSV files
- View graphs of stock price and volume over time
- Simple menu-driven interface with input validation

## Requirements

- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [matplotlib](https://matplotlib.org/)
- pandas (installed automatically with yfinance)

## Installation

1. Clone the repository or download the source code.
2. Install dependencies using pip:
   ```bash
   pip install yfinance matplotlib