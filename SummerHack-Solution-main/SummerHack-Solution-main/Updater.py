import sqlite3
from main import db, Products
import time
from olx_scrapper import olx_scrapper
from datetime import datetime

message = ''

conn = sqlite3.connect("products.db")
c = conn.cursor()
sql = """ SELECT * FROM products """
c.execute(sql)
rows = c.fetchall()
conn.commit()
conn.close()

for row in rows:
    try:
        info = olx_scrapper(row[5])
        products_update = Products.query.get_or_404(row[0])
        products_update.name = info[0]
        products_update.price = info[1]
        products_update.description = info[2]
        products_update.image = info[3]
        products_update.url = info[4]
        products_update.date_created = datetime.utcnow()
        db.session.commit()

    except:
        products_delete = Products.query.get_or_404(row[5])
        db.session.delete(products_delete)
        db.session.commit()

print('finish')

