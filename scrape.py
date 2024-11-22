import json
import requests
from bs4 import BeautifulSoup
import paymentCalc

event = {
    "url": "https://www.zillow.com/homedetails/20-Woodside-Ln-Flippin-AR-72634/109079719_zpid/"
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

    # get zpid from event
    zpid = event["url"].split("/")[-2].split("_")[0]

    soup = BeautifulSoup(page.content, "html.parser")

    price = getPrice(soup)

    paymentData = getPaymentData(zpid)

    body = {
        "price": price,
    } | paymentData

    print(body)

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def getPrice(soup):
    return soup.find('span', {"data-testid" : "price"}).findChild('span').text.replace("$", "").replace(",", "")

def getPaymentData(zpid):
    return paymentCalc.get_zillow_data(zpid)


if __name__ == "__main__":
    lambda_handler(event)