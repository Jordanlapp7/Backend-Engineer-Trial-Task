import joblib
import pandas as pd
from datetime import timedelta

# Load the pre-trained model
def load_pretrained_model():
    model = joblib.load('myapp/models/linear_regression_model.pkl')  # Adjust path if necessary
    return model

# Predict stock prices using the loaded model
def predict_stock_prices(model, historical_data, num_days=30):
    # Use last 50 days as features
    features = historical_data[['close_price']].tail(50)

    # Generate predictions for the next `num_days`
    predictions = model.predict(features.values.reshape(-1, 1))  # Reshape data if needed

    # Create future dates
    last_date = historical_data.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, num_days + 1)]

    # Return predictions as a DataFrame
    return pd.DataFrame({'date': future_dates, 'predicted_price': predictions})