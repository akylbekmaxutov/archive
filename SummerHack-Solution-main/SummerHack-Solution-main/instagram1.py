from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from datetime import datetime

headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}


def get_url1(url_link):
	url2 = url_link

	#'https://www.instagram.com/p/CTSCpjiN7fl/'

	def inser_db(name, capas, price):
		with sqlite3.connect("products.db") as con:
			img = "https://eduken.kz/image/cache/catalog/%21%21Nataly/%D0%A7%D0%B5%D1%85%D0%BB%D1%8B%20%D0%B4%D0%BB%D1%8F%20Iphone/%24_57-1000x1000.jpg"
			info = (name, price, capas, img, url2, datetime.utcnow())
			sql = """ INSERT INTO  products(name, price, description, image, url, date_created) VALUES(?,?,?,?,?,?) """
			cur=con.cursor()
			cur.execute(sql, info)
			return cur.lastrowid

	def str_obr(str):
		name_prod = str[0][2:].split()
		price = name_prod[3]
		name = name_prod[0] +' '+ name_prod[1]
		for i in range(2):
			desc = str[i+1]
			inser_db(name, desc, price)

	def get_info_post(url):
		html = requests.get(url, headers=headers)
		soup = BeautifulSoup(html.text, 'lxml')
		bs = BeautifulSoup(html.text, "html.parser")
		if html.ok:
				h=html.text
				bs_html = BeautifulSoup(h, 'lxml')
				#ned = bs_html.select('script[type="application/ld+json"]')
				ned = bs_html.select('script[type="application/ld+json"]')

				insJ = json.loads(ned[0].string.strip())
				#print(json.dumps(insJ, indent=4, sort_keys=True))
				caption = insJ['caption']
				return caption
	#print(get_info_post(url).split()[22:])
	only_tovars = get_info_post(url2).splitlines()[:5]
	for only_tovar in only_tovars:
		if (len(only_tovar) <= 1):
			only_tovars.remove(only_tovar)
	str_obr(only_tovars)
