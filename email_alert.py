import pandas as pd
import os
from datetime import datetime

# Email alert is in process
# This module will be implemented in a future update

# Default configuration - placeholder values only
DEFAULT_SENDER = "price-alerts@company.com"
DEFAULT_RECIPIENT = "your-email@example.com"

def send_price_alert(alert_products, recipient_email=DEFAULT_RECIPIENT):
    """
    Send an email alert for products where competitors have lower prices
    CURRENTLY NOT IMPLEMENTED - EMAIL ALERT IS IN PROCESS
    """
    # placeholder implementation that just logs instead of sending emails
    log_alert_instead(alert_products)
    return False, "Email alerts are currently in development. Alert data has been logged."

def log_alert_instead(alert_products):
    """
    Log the alert to a file for demonstration purposes
    """
    # gotta make sure we got a logs folder ya know
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # create a log file with current date so we can find it later
    filename = f"logs/price_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"PRICE ALERT: {len(alert_products)} products with competitor price drops\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for _, row in alert_products.iterrows():
            price_diff = row['our_price'] - row['competitor_price']
            percentage = (price_diff / row['our_price']) * 100
            f.write(f"Product: {row['product_name']}\n")
            f.write(f"Our Price: ${row['our_price']:.2f}\n")
            f.write(f"Competitor: {row['competitor_name']}\n")
            f.write(f"Their Price: ${row['competitor_price']:.2f}\n")
            f.write(f"Difference: ${price_diff:.2f} ({percentage:.1f}%)\n\n")
    
    print(f"Alert logged to {filename}")
    return True