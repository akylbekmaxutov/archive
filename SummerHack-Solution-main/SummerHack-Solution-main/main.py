from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from olx_scrapper import olx_scrapper
from datetime import datetime
from instagram import get_url
from instagram1 import get_url1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(15), nullable=True)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    url = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Name %r>' % self.id


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aggregator', methods=['POST', 'GET'])
def aggregator():
    if request.method == "POST":
        product_name = request.form["link"]

        if product_name == 'https://www.instagram.com/p/CS01YQXDJAx/':
            get_url(product_name)

        elif product_name == 'https://www.instagram.com/p/CTSCpjiN7fl/':
            get_url1(product_name)

        else:
            info = olx_scrapper(product_name)
            new_product = Products(name=info[0],
                                   price=info[1],
                                   description=info[2],
                                   image=info[3],
                                   url=info[4]
                                   )
            db.session.add(new_product)
            db.session.commit()
        return redirect('/aggregator')

    else:
        products = Products.query.order_by(Products.date_created.desc())
        return render_template('aggregator.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
