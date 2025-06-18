import requests
import smtplib
import ssl
from bs4 import BeautifulSoup
from email.message import EmailMessage
import os
from datetime import datetime
import json

# from dotenv import load_dotenv
# load_dotenv()

import pytz

pacific = pytz.timezone("America/Los_Angeles")
now = datetime.now(pacific)

url = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1?currency=USD'
# url = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1g28200c6?currency=USD'
print("EMAIL_ADDRESS:", os.environ.get("EMAIL_ADDRESS"))
print("EMAIL_PASSWORD:", os.environ.get("EMAIL_PASSWORD"))
print("TO_EMAIL:", os.environ.get("TO_EMAIL"))
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
TO_EMAIL = os.environ['TO_EMAIL']

matchas = {
    'Isuzu': {
        'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1?currency=USD',
        'in_stock': None
    },
    'Wako': {
        'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1?currency=USD',
        'in_stock': None
    },
    'Yugen': {
        'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1171020c1?currency=USD',
        'in_stock': None
    },
    'Aoarashi': {
        'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1?currency=USD',
        'in_stock': None
    },
    'Hojicha':{
        'url' :'https://www.marukyu-koyamaen.co.jp/english/shop/products/1g28200c6?currency=USD',
        'in_stock': None
    }
    # Add more if needed
}
def is_in_stock(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    sold_out = soup.find('p', class_='out-of-stock')
    return sold_out is None

def send_email(name, url):
    msg = EmailMessage()
    msg["Subject"] = f'🎉 {name} MATCHA is in stock!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(f'{name} is available!\n\n👉 {url}')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    

if __name__ == '__main__':
    for name, info in matchas.items():
        try:
            url = info['url']
            in_stock = is_in_stock(url)
            matchas[name]['in_stock'] = in_stock

            if in_stock:
                print(f"✅ In stock: {name}")
                if EMAIL_ADDRESS and EMAIL_PASSWORD and TO_EMAIL:
                    send_email(name, url)
            else:
                print(f"❌ Sold out: {name}")

        except Exception as e:
            print(f"⚠️ Error checking {name}: {e}")

    new_data = {
        "last_updated": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "matchas": matchas
    }
    try:
        with open("status.json", "r") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {}
    if old_data.get("matchas") != new_data["matchas"]:
        print("🆕 Matcha stock changed — updating file.")
        with open("status.json", "w") as f:
            json.dump(new_data, f, indent=2)
    else:
        print("✅ Matcha stock is the same — skipping update.")




