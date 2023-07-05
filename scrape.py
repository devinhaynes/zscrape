import json
import requests
from bs4 import BeautifulSoup

event = {
    "url": "https://www.zillow.com/homedetails/111-W-Johnson-Dr-Flippin-AR-72634/2057361817_zpid/"
}

def lambda_handler(event):
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    page = requests.get(event["url"], headers=req_headers)

    soup = BeautifulSoup(page.content, "html.parser")

    price = soup.find('span', {"data-testid" : "price"}).findChild('span').text.replace("$", "").replace(",", "")

    return {
        'statusCode': 200,
        'body': json.dumps(price)
    }


lambda_handler(event)