# sample-market-making-agent

Given order book and trade data, the sample market maker is able to update fair prices and generate quotes. Below are some highlights. Check the notebook for the details. This is a toy example and should not be used in production.

## Update fair price (Users can choose from 4 methods):
1. MidPrice: Update fair value based on the market mid price
2. VWAP: Calculate fair value based on trade data using VWAP
3. KalmanFilter: Use a Kalman filter for fair value prediction
4. RefOverride: Override fair price using reference price. Reference prices may come from other exchanges with better liquidity

## Generate quotes
Using Avellaneda & Stoikov’s strategy to find the optimal bid/ask spreads and taking inventory risk into consideration.

