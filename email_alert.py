import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Magic! This loads all our secret email stuff from the .env file
# It's like a secret treasure chest for passwords and things
load_dotenv()

# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
# Email settings - these are like the instructions for our email delivery person
# We need to tell them where to go and how to log in
DEFAULT_SENDER = "price-alerts@company.com"
DEFAULT_RECIPIENT = "your-email@example.com"
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

def send_price_alert(alert_products, recipient_email=DEFAULT_RECIPIENT):
    """
    Send an email alert for products where competitors have lower prices
    """
    # If we don't have login info, we can't send emails :(
    # That's like trying to mail a letter without stamps!
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        error_msg = (
            "Email not sent: SMTP credentials not configured. Please set up your email credentials by either:\n"
            "1. Setting environment variables SMTP_USERNAME and SMTP_PASSWORD\n"
            "2. Directly editing the email_alert.py file\n\n"
            "For Gmail users: You'll need to create an App Password. See README.md for instructions."
        )
        log_alert_instead(alert_products)
        return False, error_msg
    
    # If there's nothing to tell people about, don't bother them!
    if alert_products.empty:
        return False, "No price alerts to send"
    
    # Let's create a nice-looking email to send
    msg = MIMEMultipart()
    msg['From'] = DEFAULT_SENDER
    msg['To'] = recipient_email
    msg['Subject'] = f"PRICE ALERT: {len(alert_products)} products with competitor price drops"
    
    # build the email body with HTML
    body = f"""
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .alert {{
                color: #721c24;
                background-color: #f8d7da;
            }}
        </style>
    </head>
    <body>
        <h2>Price Alert Report - {datetime.now().strftime('%Y-%m-%d')}</h2>
        <p>The following {len(alert_products)} products have competitors with lower prices:</p>
        <table>
            <tr>
                <th>Product</th>
                <th>Our Price</th>
                <th>Competitor</th>
                <th>Their Price</th>
                <th>Difference</th>
            </tr>
    """
    
    # add each product to the table
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    for _, row in alert_products.iterrows():
        price_diff = row['our_price'] - row['competitor_price']
        percentage = (price_diff / row['our_price']) * 100
        body += f"""
            <tr class="alert">
                <td>{row['product_name']}</td>
                <td>${row['our_price']:.2f}</td>
                <td>{row['competitor_name']}</td>
                <td>${row['competitor_price']:.2f}</td>
                <td>${price_diff:.2f} ({percentage:.1f}%)</td>
            </tr>
        """
    
    body += """
        </table>
        <p>Please review these prices and consider adjusting your pricing strategy.</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # try to send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, f"Price alert sent to {recipient_email}"
    except Exception as e:
        # if it fails, log the alert instead
        log_alert_instead(alert_products)
        return False, f"Failed to send email: {str(e)}"

def log_alert_instead(alert_products):
    """
    Log the alert to a file if email sending fails
    """
    # make sure we have a logs directory
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # create a log file with current date
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