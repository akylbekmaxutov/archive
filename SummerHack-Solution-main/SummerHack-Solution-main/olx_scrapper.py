from bs4 import BeautifulSoup
import requests


def olx_scrapper(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    product_name = soup.find_all('div', class_='css-sg1fy9')[1].h1.text
    price = soup.find('div', class_='css-dcwlyx').h3.text
    characteristics = soup.find('div', class_='css-g5mtbi-Text').text
    image = soup.find('img', alt=product_name).get('src')
    info = (product_name, price, characteristics, image, url)
    return info

