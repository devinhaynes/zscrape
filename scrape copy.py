import requests
from bs4 import BeautifulSoup


def getPrice(url):
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    page = requests.get(url, headers=req_headers)

    soup = BeautifulSoup(page.content, "html.parser")

    price = soup.find('span', {"data-testid" : "price"}).findChild('span').text.replace("$", "").replace(",", "")
    return price

if __name__ == '__main__':
    getPrice("https://www.zillow.com/homedetails/316-Ottawa-Ln-Flippin-AR-72634/109080314_zpid/")