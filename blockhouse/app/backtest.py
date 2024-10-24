import pandas as pd
from .models import StockData

def get_stock_data(symbol):
    stock_data = StockData.objects.filter(symbol=symbol).order_by('timestamp')
    data = pd.DataFrame(list(stock_data.values('timestamp', 'close_price')))
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)
    return data

def calculate_moving_averages(data):
    data['50_day_ma'] = data['close_price'].rolling(window=50).mean()
    data['200_day_ma'] = data['close_price'].rolling(window=200).mean()
    return data

def backtest_strategy(data, initial_investment):
    cash = initial_investment
    stocks_held = 0
    max_value = initial_investment
    trades = 0
    portfolio_value = initial_investment
    portfolio_history = []

    for i in range(len(data)):
        row = data.iloc[i]
        if row['close_price'] < row['50_day_ma'] and stocks_held == 0:
            stocks_held = cash / row['close_price']
            cash = 0
            trades += 1
        elif row['close_price'] > row['200_day_ma'] and stocks_held > 0:
            cash = stocks_held * row['close_price']
            stocks_held = 0
            trades += 1

        portfolio_value = cash + (stocks_held * row['close_price'])
        portfolio_history.append(portfolio_value)

        if portfolio_value > max_value:
            max_value = portfolio_value

    total_return = (portfolio_value - initial_investment) / initial_investment * 100
    max_drawdown = max([max_value - value for value in portfolio_history]) / max_value * 100

    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'trades': trades
    }

def generate_performance_summary(symbol, initial_investment):
    data = get_stock_data(symbol)
    data = calculate_moving_averages(data)
    results = backtest_strategy(data, initial_investment)

    return {
        'total_return': f"{results['total_return']:.2f}%",
        'max_drawdown': f"{results['max_drawdown']:.2f}%",
        'trades_executed': results['trades']
    }