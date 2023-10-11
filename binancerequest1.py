import requests
import json
from matplotlib import pyplot as plt
import math
import numpy as np

url = 'https://www.binance.com/bapi/capital/v1/public/future/common/strategy/landing-page/queryTopStrategy'
post = {"page":1,"rows":3,"direction":"","strategyType":2,"symbol":"","zone":"","runningTimeMin":172800,"runningTimeMax":604800,"sort":"roi"}

url_chart = 'https://www.binance.com/bapi/futures/v1/public/future/common/strategy/landing-page/queryRoiChart'

jsonResp = requests.post(url, json=post).json()

stringResp = json.dumps(jsonResp)

stringResp_edited = "[" + stringResp.split('[', 1)[1]
stringResp_edited_2 = stringResp_edited.split(']', 1)[0] + "]"
stringResp_edited_3 = stringResp_edited_2.replace("'", "\"")

BinanceChart = []

BinanceList = json.loads(stringResp_edited_3)

print(BinanceList)

for i in range(0, len(BinanceList)):
    post_chart = {"rootUserId":BinanceList[i]['userId'],"strategyId":BinanceList[i]['strategyId'],"streamerStrategyType":"UM_GRID"}
    jsonResp_chart = requests.post(url_chart, json=post_chart).json()
    stringResp_chart = json.dumps(jsonResp_chart)
    stringResp_edited_chart = "[" + stringResp_chart.split('[', 1)[1]
    stringResp_edited_chart_2 = stringResp_edited_chart.split(']', 1)[0] + "]"
    stringResp_edited_chart_3 = stringResp_edited_chart_2.replace("'", "\"")
    BinanceChart.insert(i, json.loads(stringResp_edited_chart_3))

for i in range(0, len(BinanceChart)):
    print(BinanceList[i]['strategyId'], ": ", BinanceList[i]['roi'])
    for j in range(0, len(BinanceChart[i])):
        print(BinanceChart[i][j]['time'], ": ", BinanceChart[i][j]['roi'])

g_roi_temp = []
g_time_temp = []
g_roi = []
g_time = []

for i in range(0, len(BinanceChart)):
    for j in range(0,len(BinanceChart[i])):
        g_time_temp.insert(j, math.floor((BinanceChart[i][j]['time']-BinanceChart[i][0]['time'])/3600000))
        g_roi_temp.insert(j, BinanceChart[i][j]['roi'])
    g_time.insert(i, g_time_temp)
    g_roi.insert(i, g_roi_temp)
    g_time_temp = []
    g_roi_temp = []

for i in range(0, len(BinanceChart)):
    plt.plot(g_time[i], g_roi[i])

plt.show()
