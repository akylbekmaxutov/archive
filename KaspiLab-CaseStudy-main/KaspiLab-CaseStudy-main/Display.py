import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

df1 = pd.read_csv('Data.csv')
df2 = pd.read_csv('indexInfo.csv')
df3 = pd.read_csv('Processed.csv')

df3.drop_duplicates(subset='key', inplace=True)
df1 = df1.dropna()


def v_processed(region, date, df2, df3):
    month = date.split('/')[0]
    year = date.split('/')[1]
    index = list(df2[df2['Region'] == region]['Index'].values)
    frames = []
    for item in index:
        frames.append(df3[(df3['Index'] == item) & (df3['Date'].apply(lambda x: x.split('/')[0]) == month ) &
                          (df3['Date'].apply(lambda x: x.split('/')[2]) == year)])
    dataFrame = pd.concat(frames)
    max_open = max(dataFrame['Open'])
    max_index = dataFrame[dataFrame['Open'] == max_open]['Index'].values[0]
    min_close = min(dataFrame['Low'])
    min_index = dataFrame[dataFrame['Low'] == min_close]['Index'].values[0]
    currency = df2[df2['Region'] == region]['Currency'].values[0]
    max_open_exchange = df2[(df2['Region'] == region) & (df2['Index'] == max_index)]['Exchange'].values[0]
    min_close_exchange = df2[(df2['Region'] == region) & (df2['Index'] == min_index)]['Exchange'].values[0]
    return dataFrame, max_open, min_close, currency, max_open_exchange, min_close_exchange


def visualization(dataFrame, currency, region, date):
    fig, ax = plt.subplots()
    for item in list(dataFrame['Index'].unique()):
        ax.plot(dataFrame[dataFrame['Index'] == item]['Date'].apply(lambda x: x.split('/')[1]),
                dataFrame[dataFrame['Index'] == item]['Open'],
                label=item, markersize=8)
    ax.legend()
    ax.set_xlabel('Days')
    ax.set_ylabel(currency)
    ax.set_title('{}. максимальная цена в момент даты открытия на {}'.format(region, date))
    fig.savefig('static/my_visual1.png')

    fig, ax = plt.subplots()
    for item in list(dataFrame['Index'].unique()):
        ax.plot(dataFrame[dataFrame['Index'] == item]['Date'].apply(lambda x: x.split('/')[1]),
                dataFrame[dataFrame['Index'] == item]['Low'],
                label=item, markersize=8)
    ax.legend()
    ax.set_xlabel('Days')
    ax.set_ylabel(currency)
    ax.set_title('{}. минимальная цена во время торговли на {}'.format(region, date))
    fig.savefig('static/my_visual2.png')


app = Flask(__name__)


@app.route('/')
def display():
    return render_template('Display.html')


@app.route('/display2')
def display2():
    return render_template('Display2.html')


@app.route('/form', methods=['POST'])
def form():
    country = request.form.get('country')
    month = request.form.get('month')
    date = '{}/{}'.format(str(int(month.split('-')[1])),month.split('-')[0])
    dataFrame, max_open, min_close, currency, max_open_exchange, min_close_exchange = v_processed(country,date,df2,df3)
    visualization(dataFrame,currency,country,date)
    return render_template('form.html', country=country, month=month)


if __name__ == '__main__':
    app.run()
