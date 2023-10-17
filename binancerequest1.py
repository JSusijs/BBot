import requests
import json
from matplotlib import pyplot as plt
import math
import numpy as np
from scipy.stats import linregress


url = 'https://www.binance.com/bapi/capital/v1/public/future/common/strategy/landing-page/queryTopStrategy'
post = {"page":1,"rows":10,"direction":"","strategyType":2,"symbol":"","zone":"","runningTimeMin":0,"runningTimeMax":604800,"sort":"roi"}

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
    print(BinanceList[i]['symbol'], ": ", BinanceList[i]['strategyId'], ": ", BinanceList[i]['roi'])
#    for j in range(0, len(BinanceChart[i])):
#        print(BinanceChart[i][j]['time'], ": ", BinanceChart[i][j]['roi'])

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
    linear_analysis = linregress(g_time[i], g_roi[i])
    print(linear_analysis.rvalue)

    x = np.linspace(0, len(g_time[i]), len(g_time[i]))
    y = linregress(g_time[i], g_roi[i]).slope * x + linregress(g_time[i], g_roi[i]).intercept

    plt.plot(x, y, ':')

    print(linregress(g_time[i], g_roi[i], alternative='two-sided'))

plt.show()

InTrade = []
NotInTrade_amount = []

for i in range(0, len(BinanceChart)):
    TimeTotal_temp = 0
    TimeInTrade_temp = 0
    NotInTrade_temp = 0
    for j in range(1, len(g_time[i])):
        if (g_roi[i][j-1] - g_roi[i][j]) != 0:
            TimeTotal_temp += 1
            TimeInTrade_temp += 1
        else:
            TimeTotal_temp += 1
    for j in range(1, len(g_time[i])-1):
        if (g_roi[i][j-1] - g_roi[i][j]) != 0:
            if (g_roi[i][j] - g_roi[i][j+1]) == 0:
                NotInTrade_temp += 1
    if (g_roi[i][0] - g_roi[i][1]) == 0:
        NotInTrade_temp += 1
    InTrade.insert(i, (TimeInTrade_temp/TimeTotal_temp))
    NotInTrade_amount.insert(i, NotInTrade_temp)
    print(InTrade[i], " : ", NotInTrade_amount[i])

url_volatility = 'https://www.binance.com/bapi/futures/v1/public/future/common/strategy/landing-page/queryTopVolatility'
post_volatility = {"strategyType":2,"rows":1000,"page":1}
jsonResp_volatility = requests.post(url_volatility, json=post_volatility).json()
stringRespV = json.dumps(jsonResp_volatility)
stringRespV_edited = "[" + stringRespV.split('[', 1)[1]
stringRespV_edited_2 = stringRespV_edited.split(']', 1)[0] + "]"
stringRespV_edited_3 = stringRespV_edited_2.replace("'", "\"")
VolatilityList = json.loads(stringRespV_edited_3)
print(VolatilityList)

Coef = []
for i in range(0, len(BinanceList)):
    for j in range(0, len(VolatilityList)):
        if VolatilityList[j]['symbol'] == BinanceList[i]['symbol']:
            symbol_volatility = VolatilityList[j]['volatility']
            break
        else:
            symbol_volatility = "null"

    url_24hr = 'https://www.binance.com/fapi/v1/ticker/24hr?symbol=' + BinanceList[i]['symbol']
    getResp = requests.get(url_24hr).json()

# Coefficient attempt 1
#    Coef.insert(i, (InTrade[i] * linregress(g_time[i], g_roi[i], alternative='two-sided').slope * (pow(linregress(g_time[i], g_roi[i], alternative='two-sided').rvalue, 2)) * (((float(BinanceList[i]['strategyParams']['upperLimit']) - float(BinanceList[i]['strategyParams']['lowerLimit']))/float(BinanceList[i]['strategyParams']['gridCount']))/float(getResp['weightedAvgPrice']))))

# Coefficient attempt 2
    Coef.insert(i, (InTrade[i] * linregress(g_time[i], g_roi[i], alternative='two-sided').slope * (pow(linregress(g_time[i], g_roi[i], alternative='two-sided').rvalue, 2)) * (((float(BinanceList[i]['strategyParams']['upperLimit']) - float(BinanceList[i]['strategyParams']['lowerLimit']))/float(BinanceList[i]['strategyParams']['gridCount']))/linregress(g_time[i], g_roi[i], alternative='two-sided').stderr)))

    if Coef[i] > 0:
        print(BinanceList[i]['symbol'], " : ", round(BinanceList[i]['runningTime']/3600, 1), "h : ", symbol_volatility, " : ", BinanceList[i]['roi'], "% : ", round(Coef[i], 8))


