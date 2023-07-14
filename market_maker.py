import math
import pandas as pd
import numpy as np

from pykalman import KalmanFilter

# Define the market making model


class MarketMaker:
    def __init__(self):
        self.order_books = None
        self.trade_data = None
        self.fair_price = None
        self.ref_price = None
        self.target_position = 0

    def update_data(self, order_books, trade_data):
        self.order_books = order_books
        self.trade_data = trade_data

    def calculate_fair_price(self, method):
        if method == 'MidPrice':
            # Update fair value based on the market mid price
            return self.order_books.mid_price.values[-1]
        elif method == 'VWAP':
            # Calculate fair value based on trade data using VWAP
            trade_prices = self.trade_data['price'].values
            trade_volumes = self.trade_data['amount'].values
            vwap = np.sum(trade_prices * trade_volumes) / np.sum(trade_volumes)
            self.fair_price = vwap
        elif method == 'KalmanFilter':
            # Use a Kalman filter for fair value prediction
            kf = KalmanFilter(transition_matrices=[1],
                              observation_matrices=[1],
                              initial_state_mean=self.trade_data['price'].values[0],
                              initial_state_covariance=1,
                              observation_covariance=1,
                              transition_covariance=0.01)
            filtered_state_means, _ = kf.filter(
                self.trade_data['price'].values)
            self.fair_price = filtered_state_means[-1]
        elif method == 'RefOverride':
            # Override fair price using reference price. Reference price may come from other exchanges with better liquidity
            self.fair_price = self.ref_price
        else:
            raise ValueError(
                "Invalid fair value prediction method. Choose 'MidPrice', 'VWAP', 'KalmanFilter' or 'RefOverride'.")

    def generate_quotes_symmetric(self, spreads: list = None):
        '''        
            A simple symmetric quoting algo. The spreads can be provided manually or from another algo.
            If not provided, the spreads will be decide automatically according to price vol.
            More volatile prices will lead to wider spreads

        '''

        if spreads is None:
            # Calculate price vol to decide spread if spread is not given
            vol = self.trade_data.price.rolling(50).std().values[-1]
            # vol = self.order_books.mid_price.rolling(50).std()
            # Adjust quotes based on position and spread
            return {
                'asks': {
                    'Q1': self.fair_price + 0.5 * vol,  # p=0.6
                    'Q2': self.fair_price + 0.7 * vol,  # p=0.5
                    'Q3': self.fair_price + 1 * vol,  # p=0.3

                },
                'bids': {
                    'Q1': self.fair_price - 0.5 * vol,  # p=0.6
                    'Q2': self.fair_price - 0.7 * vol,  # p=0.5
                    'Q3': self.fair_price - 1 * vol,  # p=0.3
                }
            }
        else:
            # given spreads in percentage e.g. [0.05, 0.1, 0.2]
            return {'asks': {f'Q{i}': self.fair_price * (1 + spreads[i]) for i in len(spreads)},
                    'bids': {f'Q{i}': self.fair_price * (1 - spreads[i]) for i in len(spreads)}}

    def generate_quotes_avellaneda_stoikov(self, position, fair_price, gamma, vol, order_book_density, T, t):
        '''        
            Generate optimal quotes based on Avellaneda & Stoikov's strategy 
            position: existing position
            fair_price: fair price calcualted from self.update_fair_value()
            gamma: inventory risk aversion parameter
            T = closing time
            t = current time 
            q = quantity of assets in inventory of base asset (could be positive/negative for long/short positions)
            order_book_density: bigger if the order book is denser, 
                and the optimal spread will have to be smaller since there is more competition on the market;
                smaller if assuming the order book has low liquidity, thus use a more extensive spread.

        '''
        reservation_price = fair_price - \
            (position - self.target_position) * gamma * (T - t)/T * (vol ** 2)
        spread = gamma * (vol ** 2) * (T - t) + (2/gamma) * \
            math.log(1 + (gamma/order_book_density))
        bid = reservation_price - spread/2
        ask = reservation_price + spread/2

        return {'as_bid': bid, 'as_ask': ask}


### Example usage
# Data Extraction and Cleaning
order_books = ..
trade_data = ..

# Create a MarketMaker instance
market_maker = MarketMaker()

# Update order books and trade data
market_maker.update_data(order_books, trade_data)

# Update fair price
market_maker.calculate_fair_price('KalmanFilter')

# Generate quotes
quotes = market_maker.generate_quotes_symmetric()


# Set parameters
position = 0  # Assuming no existing position
position_factor = 0.1

# Generate quotes
quotes = market_maker.generate_quotes(position, position_factor)

