import pandas as pd
import numpy as np
import sqlite3

# reading data and transforming to appendable format
data = pd.read_csv('Data.csv')
info = pd.read_csv('indexInfo.csv')
processed = pd.read_csv('Processed.csv')

data_array = np.array(data)
info_array = np.array(info)
processed_array = np.array(processed)

data_tuple = []
for item in data_array:
    data_tuple.append(tuple(item))

info_tuple = []
for item in info_array:
    info_tuple.append(tuple(item))

processed_tuple = []
for item in processed_array:
    processed_tuple.append(tuple(item))

# Creating DataBase and inserting data
conn = sqlite3.connect('stockprice.db')
c = conn.cursor()

c.execute("""CREATE TABLE data ( 
    key INT, 
    Index_ TEXT,
    Date TEXT, 
    Open REAL,
    High REAL,
    Low REAL,
    Close REAL,
    Adj_Close REAL,
    Volume REAL 
    )""")

c.execute("""CREATE TABLE info (
    Region TEXT,
    Exchange TEXT,
    Index_ TEXT,
    Currency TEXT
    )""")

c.execute("""CREATE TABLE processed (
    key INT,
    Index_ TEXT,
    Date TEXT, 
    Open REAL,
    High REAL,
    Low REAL,
    Close REAL,
    Adj_Close REAL,
    Volume REAL,
    Close_USD REAL 
    )""")


c.executemany("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?)", data_tuple)
c.executemany("INSERT INTO info VALUES (?,?,?,?)", info_tuple)
c.executemany("INSERT INTO processed VALUES (?,?,?,?,?,?,?,?,?,?)", processed_tuple)

conn.commit()
conn.close()


