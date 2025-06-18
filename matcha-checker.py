import requests
import smtplib
import ssl
from bs4 import BeautifulSoup
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()


url = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1?currency=USD'
# url = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1g28200c6?currency=USD'

EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
TO_EMAIL = os.environ['TO_EMAIL']
matchas = {
    'Isuzu': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1?currency=USD',
    'Wako': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1?currency=USD',
    'Yugen': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1171020c1?currency=USD',
    'Aoarashi': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1?currency=USD',
    # 'Hojicha': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1g28200c6?currency=USD'

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
    for name, url in matchas.items():
        try:
            if is_in_stock(url):
                print(f"In stock: {name}")
                send_email(name, url)
            else:
                print(f"Sold out: {name}")
        except Exception as e:
            print(f"Error checking {name}: {e}")