import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import numpy as np
from datetime import timedelta

# Calculate key backtest metrics
def calculate_backtest_metrics(backtest_results):
    total_return = (backtest_results['final_portfolio_value'] - backtest_results['initial_investment']) / backtest_results['initial_investment'] * 100
    max_drawdown = backtest_results['max_drawdown']
    trades = backtest_results['trades_executed']
    
    metrics = {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'trades_executed': trades
    }
    
    return metrics

# Generate stock price comparison plot
def generate_stock_price_plot(actual_data, predicted_data):
    plt.figure(figsize=(10, 6))
    
    # Plot actual stock prices
    plt.plot(actual_data['timestamp'], actual_data['close_price'], label="Actual Prices", color='blue')
    
    # Plot predicted stock prices
    plt.plot(predicted_data['date'], predicted_data['predicted_price'], label="Predicted Prices", color='red')
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Prediction vs. Actual')
    plt.legend()
    
    # Save the plot as an image
    plot_filename = 'stock_price_comparison.png'
    plt.savefig(plot_filename)

    return plot_filename

# Generate a PDF report
def generate_pdf_report(metrics, plot_filename):
    pdf_filename = "report.pdf"
    
    # Create a PDF object
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Add Title
    c.setFont("Helvetica", 20)
    c.drawString(100, 750, "Stock Performance Report")
    
    # Add metrics
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Total Return: {metrics['total_return']:.2f}%")
    c.drawString(100, 700, f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
    c.drawString(100, 680, f"Trades Executed: {metrics['trades_executed']}")
    
    # Insert the plot image
    c.drawImage(plot_filename, 100, 450, width=400, height=200)
    
    # Save the PDF
    c.showPage()
    c.save()
    
    return pdf_filename