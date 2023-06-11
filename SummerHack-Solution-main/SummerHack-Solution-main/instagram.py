from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from datetime import datetime

def get_url(url_link):
	url = url_link

	headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

	#'https://www.instagram.com/p/CS01YQXDJAx/'

	def inser_db(name, capas, price):
		with sqlite3.connect("products.db") as con:
			mod = "iPhone" + name
			img = "https://s.taplink.ru/a/3/0/3/6/2bc6c4.jpg?1"
			info = (mod, price, capas,img, url, datetime.utcnow())
			sql = """ INSERT INTO  products(name, price, description, image, url, date_created) VALUES(?,?,?,?,?,?) """
			cur=con.cursor()
			cur.execute(sql, info)
			return cur.lastrowid

	def str_obr(str):
		s = str.split()
		if(s[-1] == 'GB'):
			price = '0'
		else:
			price = s[-1]
		capasity=''
		for i in range(len(s)):
			if s[i] == 'GB':
				capasity = s[i-1]
		name=''
		for i in s:
			if (i == capasity):
				break
			name += i + ' '

		price = price.replace(".",'')
		inser_db(name, capasity, price)

	def get_info_post(usr):
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
	only_tovars = get_info_post(url).splitlines()[5:]
	for only_tovar in only_tovars:
		if (len(only_tovar) <= 1):
			only_tovars.remove(only_tovar)
	#print (only_tovars)
	for ind in range(19):
		str_obr(only_tovars[ind][1:])
