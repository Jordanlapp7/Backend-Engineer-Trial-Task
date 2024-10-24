import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample function to generate stock data for training (replace with your actual data)
def generate_sample_stock_data():
    # Example: Generate dummy stock data (in a real scenario, replace this with real stock data)
    dates = pd.date_range('2020-01-01', periods=100)
    close_prices = pd.Series([100 + i * 0.5 for i in range(100)], index=dates)
    return pd.DataFrame({'close_price': close_prices})

# Train a simple linear regression model using stock price data
def train_linear_regression_model():
    # Get historical stock data (replace this with your actual stock data fetching logic)
    data = generate_sample_stock_data()

    # Use the last 50 days as features
    X = list(range(len(data)))  # Example: Use time as a feature (you may replace this with better features)
    y = data['close_price'].values  # Target is the stock's close price

    # Reshape X for scikit-learn (it expects a 2D array for features)
    X = pd.DataFrame(X).values.reshape(-1, 1)

    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Save the trained model to a .pkl file
    joblib.dump(model, 'app/models/linear_regression_model.pkl')  # Ensure path matches your Django app
    print("Model trained and saved as linear_regression_model.pkl")

# Execute model training when the script is run
if __name__ == '__main__':
    train_linear_regression_model()