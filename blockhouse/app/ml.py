import joblib
import numpy as np
import pandas as pd
from datetime import timedelta

# Load the pre-trained model
def load_pretrained_model():
    model = joblib.load('app/models/linear_regression_model.pkl')  # Adjust path if necessary
    return model

def predict_stock_prices(model, historical_data, num_days=30):
    # Ensure historical data has enough points for prediction (e.g., last 50 days)
    if len(historical_data) < 50:
        raise ValueError("Not enough historical data for prediction. Need at least 50 days of data.")
    
    # Use the last 50 days of 'close_price' as features for initial prediction
    features = historical_data[['close_price']].tail(50).values.reshape(-1, 1)

    # Create future dates (next 30 days)
    last_date = historical_data.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, num_days + 1)]

    # List to store the predictions
    predictions = []

    # Predict stock prices for the next 30 days
    for _ in range(num_days):
        # Predict the next day's price based on the current 50-day window
        next_prediction = model.predict(features)[-1]  # Get the prediction for the next day
        predictions.append(next_prediction)

        # Update features: Drop the oldest day and add the predicted value
        features = np.roll(features, -1)  # Shift the features to the left
        features[-1] = next_prediction  # Add the new prediction to the feature set

    # Return predictions as a DataFrame with future dates
    return pd.DataFrame({
        'date': future_dates,
        'predicted_price': predictions
    })