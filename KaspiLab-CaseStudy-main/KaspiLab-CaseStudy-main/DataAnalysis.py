import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv('Data.csv')
df2 = pd.read_csv('indexInfo.csv')
df3 = pd.read_csv('Processed.csv')

df3.drop_duplicates(subset='key', inplace=True)
df1 = df1.dropna()


def v_not_processed(df1, df2, df3):
    df1 = df1.dropna()
    for item in df1['Index'].unique():
        if (df1[df1['Index'] == item].shape[0]) != (df3[df3['Index'] == item].shape[0]):
            return df1[df1['Index'] == item], df2[df2['Index'] == item]['Region'].values[0]


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


region = 'China'
date = '5/2021'
dataFrame, max_open, min_close, currency, max_open_exchange, min_close_exchange = v_processed(region,date,df2,df3)


fig, ax = plt.subplots()
plt.style.use('seaborn')
for item in list(dataFrame['Index'].unique()):
    ax.plot(dataFrame[dataFrame['Index'] == item]['Date'].apply(lambda x: x.split('/')[1]),
            dataFrame[dataFrame['Index'] == item]['Open'],
            label=item, markersize=8)
ax.legend()
ax.set_xlabel('Days')
ax.set_ylabel(currency)
ax.set_title('{}. максимальная цена в момент даты открытия на {}'.format(region, date))
fig.savefig('my_plot1.png')


fig, ax = plt.subplots()
plt.style.use('seaborn')
for item in list(dataFrame['Index'].unique()):
    ax.plot(dataFrame[dataFrame['Index'] == item]['Date'].apply(lambda x: x.split('/')[1]),
            dataFrame[dataFrame['Index'] == item]['Low'],
            label=item, markersize=8)
ax.legend()
ax.set_xlabel('Days')
ax.set_ylabel(currency)
ax.set_title('{}. минимальная цена во время торговли на {}'.format(region, date))
fig.savefig('my_plot2.png')

