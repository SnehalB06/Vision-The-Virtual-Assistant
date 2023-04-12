import json
from flask import Flask, render_template, request, jsonify, url_for,redirect,make_response
import os

from flask_cors import CORS
import requests
from datetime import datetime
#from googletrans import Translator, constants
import time
import openai
import gradio as gr
from load_key_from_config import getConfigKey
from ner_test import getNER
from weather import weather_keyword_list, getWeather, getWeatherASR
from stocks import stock_keyword_list, getStocks
from oc_transpo_bus import bus_keyword, processBusRequest
from news import news_keywords_list, processNewsRequest
from google_drive_load_file import summary_keywords, processSummaryRequest
import os
from io import BytesIO
from load_key_from_config import getConfigKey

import spacy
text = ""
#engine = pyttsx3.init()
nlp = spacy.load('en_core_web_sm')


app = Flask(__name__)
cors = CORS(app)

openai.api_key = getConfigKey("opanaiAPI")
messages = [{"role": "system", "content": "You are a virtual assistant chatbot. Your name is Vision. You will help users with general queries."}]

from pprint import pprint
#M7E7BMSVG2N5CJKNZ23E6Y8C8

@app.route('/news', methods=['POST','GET'])
def news():
    translator = Translator()
    news_dict = {}
    news =[]
    url = "https://newsapi.org/v2/everything?q=tesla&from=2023-03-09&sortBy=publishedAt&apiKey=45f7ab3c7b1241b88021bf121166b87f"
    r = requests.get(url).json()
    #print(url)
    print(r)
    #print(r['articles'])
    total = r['totalResults']
    for i in range(0,10):
        x = {}
        title = translator.translate(r['articles'][i]['title']).text
        x['title'] = title
        description = translator.translate(r['articles'][i]['description']).text
        x['description'] = description
        url = translator.translate(r['articles'][i]['url']).text
        x['url'] = url
        source_name = r['articles'][i]['source']['name']
        author = r['articles'][i]['author']
        x['author'] = author
        x['source'] = source_name
        news_dict[x['title']] = x
        if i <10:
            news.append(x)
    #print(news)
    return render_template('news.html', news_obj=news)

@app.route('/stocks',methods=['POST','GET'])
def getStocks1():
    stocks = {}
    stock = []
    url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2023-01-09?adjusted=true&apiKey=BEVh584XY8ypg7_ZwnmO1VuGGa4GKNyF"
    r = requests.get(url).json()
    c = r['count']
    print(c)
    print(r)
    for i in range(0,c):
        x={}
        x['Title']  = r['results'][i]['T']
        x['open']  = r['results'][i]['o']
        x['close']  = r['results'][i]['c']
        x['high']  = r['results'][i]['h']
        x['low']  = r['results'][i]['l']
        #x['transaction']  = r['results'][i]['n']
        #print(x)
        stocks[x['Title']] = x
        if i<10:
            stock.append(x)
    print(stocks)
    #specific stock
    filtered_dict = {k: v for k, v in stocks.items() if 'DXGE' in k}
    print(filtered_dict)
    return render_template('stocks.html',stocks=stock)



@app.route('/back',methods=['POST'])
def about():
    data = json.loads(request.data)
    doc = nlp(data)
    response_data = {}

    user_input = data
    print(user_input)
    messages.append({"role": "user", "content": user_input})

    tokens = getNER(user_input)
    print(tokens)

    if any(word in user_input for word in weather_keyword_list):
        gpe_entities = [ent.text for ent in tokens if ent.label_ == 'GPE']
        print(gpe_entities)
        if gpe_entities:
            chat_response = getWeatherASR(gpe_entities[0])
            print(chat_response)
            response_data = jsonify({'weather': chat_response, "weather_flag": 1})

    elif any(word in user_input for word in stock_keyword_list):
        org_entities = [ent.text for ent in tokens if ent.label_ == 'ORG']
        print(org_entities)
        if org_entities:
            chat_response = getStocks(org_entities[0])
            print(chat_response)
            response_data = jsonify({'stocks': chat_response, 'stock_flag': 1})


    elif any(word in user_input for word in bus_keyword):
        user_input = "what time does the route 97 bus leave Hurdman Station"
        chat_response = processBusRequest(user_input)
        print("c",chat_response)
        response_data = jsonify({'buses': chat_response, "bus_flag": 1})

    elif any(word in user_input for word in news_keywords_list):
        chat_response = processNewsRequest(user_input)
        print("chat",chat_response)
        response_data = jsonify({'news': [chat_response], "news_flag": 1})


    elif any(word in user_input for word in summary_keywords):
        chat_response = processSummaryRequest(user_input)

    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        chat_response = response["choices"][0]["message"]["content"]
        response_data = jsonify({'chat': [chat_response], "chat_flag": 1})

    messages.append({"role": "assistant", "content": chat_response})
    #return chat_response
    '''
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == 'GPE' and 'weather' in data:
            print('weather in ',ent.text)
            r = getWeatherData(ent.text)
            print(r)
    '''
    resp = make_response(response_data, 201)
    return resp

@app.route('/')
def start():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
