# sample-market-making-agent

Given order book and trade data, the sample market maker is able to update fair prices and generate quotes. The main algorithms are implemented in market_maker.py/MarketMaker. The demonstration and presentation are available on notebook.py. Below are some highlighted features. 

## Update fair price (4 methods):
1. MidPrice: Update fair value based on the market mid price
2. KalmanFilter: The observed mid-prices are dynamic and noisy. So we can apply a Kalman filter for better fair value estimation.
3. VWAP: Calculate fair value based on trade data using VWAP
4. RefOverride: Override fair price using reference price. Reference prices may come from other exchanges with better liquidity

## Generate quotes (2 methods)
1. A simple symmetric quoting algo
2. Using Avellaneda & Stoikov’s strategy to find the optimal bid/ask spreads and taking inventory risk into consideration.

## This is a toy example and should not be used in production.
