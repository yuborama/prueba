import flask
from flask import request
import pandas as pd
from datetime import datetime



data = pd.read_csv('data.csv', names=['s', 'e', 'm']).set_index('m')

series = pd.Series(index=range(data.s.min(), datetime.now().year + 1))
for m in data.index:
    series.loc[data.loc[m].s:data.loc[m].e] = m

app = flask.Flask(__name__)

def convertStrToDate(date):
    if(type(date)==datetime):
        return date
    else:
        if(len(date)>=21):
            return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
        return datetime.strptime(date, '%m/%d/%Y')

def date(str):
    list = []
    x = 0
    for fecha in str:
        list.append(convertStrToDate(fecha))
    return pd.Series(list)

def calculateminutes(list):
    l = []
    for date in list:
        l.append(int(date.seconds / 60))
    return pd.Series(l)


@app.route('/', methods=['GET'])
def home():
    year = int(request.args['year'])
    try:
        return series.loc[year]
    except KeyError:
        return f'Invalid input ({series.index.min()} - {series.index.max()})'

@app.route('/ping', methods=['GET'])
def ping():
    return {"message":"pong"}