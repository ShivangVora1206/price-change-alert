import yfinance as yf
import smtplib
from email.message import EmailMessage
import os

# Load sensitive info from environment variables for security
EMAIL_ADDRESS = os.environ.get('ALERT_EMAIL')      # Your Gmail address
EMAIL_PASSWORD = os.environ.get('ALERT_EMAIL_PWD') # App password or Gmail password

def get_gold_etf_price():
    ticker = 'GOLDIETF.NS'
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    if data.empty:
        print("No price data found for", ticker)
        return None
    latest_price = data['Close'].iloc[-1]
    print(f"ICICI Prudential Gold ETF (ICICIGOLD.NS) latest closing price: ₹{latest_price:.2f}")
    return latest_price

def send_email_alert(price):
    msg = EmailMessage()
    msg['Subject'] = "Gold ETF Price Alert"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # You can set this to any recipient
    msg.set_content(f"Alert! ICICI Prudential Gold ETF price is ₹{price:.2f}, which is above your threshold of ₹85.73.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    threshold = float(os.environ.get('THRESHOLD'))  # Default threshold if not set
    price = get_gold_etf_price()
    if price and price > threshold:
        send_email_alert(price)