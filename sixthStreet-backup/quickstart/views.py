from django.shortcuts import render
from django.http import JsonResponse
import json
import time
from alpha_vantage.timeseries import TimeSeries
from LazyLoader import LazyValues
from functools import lru_cache

API_KEY = 'XSNTT1Z9MAEUCVYX'
ts = TimeSeries(API_KEY, output_format='json')

@lru_cache(maxsize=128)
def lookup(request):
    symbol = ''
    date = ''
    if request.is_json:
        jsonRequest = request.get_json()
        symbol = jsonRequest['symbol']
        date = jsonRequest['date']
    prices,meta = ts.get_daily(symbol, outputsize='full')
    prices = prices.get(date)
    lazyValues = LazyValues(some_slow_value = lambda: slow_function(json.dumps(prices, indent = 1) , sleep_time=3),)
    return JsonResponse(prices, lazyValues)

@lru_cache(maxsize=128)
def min(request):
    symbol = ''
    range = 0
    if request.is_json:
        jsonRequest = request.get_json()
        symbol = jsonRequest['symbol']
        range = jsonRequest['range']
    data = ts.get_daily(symbol, outputsize = 'full')
    jsonData = data[0]
    jsonList = list(jsonData.values())[1:range]
    minimum = float(jsonList[0]['3. low'])
    for key in jsonList:
        comp = float(key['3. low'])
        if(comp < minimum):
            minimum = comp
    return JsonResponse(str(minimum))

@lru_cache(maxsize=128)    
def max(request):
    symbol = ''
    range = 0
    if request.is_json:
        jsonRequest = request.get_json()
        symbol = jsonRequest['symbol']
        range = jsonRequest['range']
    data = ts.get_daily('AAPL', outputsize = 'full')
    jaon = data[0]
    jsonList = list(jaon.values())[1:range]
    maximum = float(jsonList[0]['4. high'])
    for key in jsonList:
        comp = float(key['4. high'])
        if(comp > maximum):
            maximum = comp
    return JsonResponse(str(maximum))

def slow_function(v, sleep_time=2):
  time.sleep(sleep_time)
  return v




