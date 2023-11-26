import requests
import json
import math
import numpy as np
from scipy.stats import linregress, tstd
from scipy import stats


def analysis():
    url = 'https://www.binance.com/bapi/capital/v1/public/future/common/strategy/landing-page/queryTopStrategy'
    post = {"page":1,"rows":10,"direction":"","strategyType":2,"symbol":"","zone":"","runningTimeMin":0,"runningTimeMax":172800,"sort":"roi"}

    url_chart = 'https://www.binance.com/bapi/futures/v1/public/future/common/strategy/landing-page/queryRoiChart'

    jsonResp = requests.post(url, json=post).json()

    stringResp = json.dumps(jsonResp)

    stringResp_edited = "[" + stringResp.split('[', 1)[1]
    stringResp_edited_2 = stringResp_edited.split(']', 1)[0] + "]"
    stringResp_edited_3 = stringResp_edited_2.replace("'", "\"")

    BinanceChart = []
    Roi_Av = []

    BinanceList = json.loads(stringResp_edited_3)

    for i in range(0, len(BinanceList)):
        post_chart = {"rootUserId":BinanceList[i]['userId'],"strategyId":BinanceList[i]['strategyId'],"streamerStrategyType":"UM_GRID"}
        jsonResp_chart = requests.post(url_chart, json=post_chart).json()
        stringResp_chart = json.dumps(jsonResp_chart)
        stringResp_edited_chart = "[" + stringResp_chart.split('[', 1)[1]
        stringResp_edited_chart_2 = stringResp_edited_chart.split(']', 1)[0] + "]"
        stringResp_edited_chart_3 = stringResp_edited_chart_2.replace("'", "\"")
        BinanceChart.insert(i, json.loads(stringResp_edited_chart_3))
        Roi_Av.insert(i, float(BinanceList[i]['roi'])/(BinanceList[i]['runningTime']/3600))

    g_roi_temp = []
    g_time_temp = []
    g_roi = []
    g_time = []
    g_roi_hourly = []
    g_roi_hourly_temp = []
    g_sd_hourly = []
    g_sd_hourly_temp = []

    for i in range(0, len(BinanceChart)):
        for j in range(0,len(BinanceChart[i])):
            g_time_temp.insert(j, math.floor((BinanceChart[i][j]['time']-BinanceChart[i][0]['time'])/3600000))
            g_roi_temp.insert(j, BinanceChart[i][j]['roi'])
            if j != 0:
                g_roi_hourly_temp.insert(j, BinanceChart[i][j]['roi']-BinanceChart[i][j-1]['roi'])
        g_time.insert(i, g_time_temp)
        g_roi.insert(i, g_roi_temp)
        g_roi_hourly.insert(i, g_roi_hourly_temp)
        g_sd_hourly_temp = np.nanstd(g_roi_hourly_temp)
        g_sd_hourly.insert(i, g_sd_hourly_temp)
        g_time_temp = []
        g_roi_temp = []
        g_roi_hourly_temp = []

    for i in range(0, len(g_sd_hourly)):
        if g_sd_hourly[i] == 'nan' or g_sd_hourly[i] == 0:
            del BinanceChart[i]
            del BinanceList[i]
            del Roi_Av[i]
            del g_sd_hourly[i]
            del g_roi_hourly[i]
            del g_roi[i]
            del g_time[i]
            #i = i-1

    sharpe = []
    t_value = []
    #Sharpe
    for i in range(0, len(BinanceList)):
        sharpe.insert(i, Roi_Av[i]/g_sd_hourly[i])
        t_value.insert(i, Roi_Av[i]/g_sd_hourly[i] * math.sqrt((BinanceList[i]['runningTime']/86400)))

    P_value = []
    P_value_log = []

    Coef = []
    for i in range(0, len(BinanceList)):

        url_24hr = 'https://www.binance.com/fapi/v1/ticker/24hr?symbol=' + BinanceList[i]['symbol']
        getResp = requests.get(url_24hr).json()

        # P-Value
        P_value.insert(i, stats.ttest_1samp(g_roi_hourly[i], 0).pvalue)
        P_value_log.insert(i, np.log10(P_value[i]))

        Coef.insert(i, t_value[i] * (pow(linregress(g_time[i], g_roi[i], alternative='two-sided').rvalue, 2)))

    # P-Value analysis

    P_mean_log = np.mean(P_value_log)
    P_std_log = tstd(P_value_log)
    P_hurdle = pow(10, (P_mean_log+P_std_log))/(len(BinanceList))
    Coef_mean = np.mean(Coef)
    Coef_std = tstd(Coef)
    Coef_hurdle = Coef_mean - Coef_std
    passed_temp = []
    passed = []

    for i in range(0, len(BinanceList)):
        if Coef[i] > Coef_mean:
            if P_value[i] < pow(10, P_mean_log):
                passed_temp = {"position": i, "symbol": BinanceList[i]['symbol'], "strategyId": BinanceList[i]['strategyId'], "runningTime": round(BinanceList[i]['runningTime']/3600, 1), "roi": BinanceList[i]['roi'], "coef": round(Coef[i], 8), "p_value": P_value[i]}
                passed.append(passed_temp)

    def sort_second(val):
        return val['coef']

    passed.sort(key=sort_second, reverse=True)

    return passed
