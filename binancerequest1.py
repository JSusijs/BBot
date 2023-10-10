import requests
import json

url = 'https://www.binance.com/bapi/capital/v1/public/future/common/strategy/landing-page/queryTopStrategy'
post = {"page":1,"rows":8,"direction":"","strategyType":2,"symbol":"","zone":"","runningTimeMin":172800,"runningTimeMax":604800,"sort":"roi"}

jsonResp = requests.post(url, json=post).json()
stringResp = json.dumps(jsonResp)
stringResp_edited = "[" + stringResp.split('[', 1)[1]
stringResp_edited_2 = stringResp_edited.split(']', 1)[0] + "]"
stringResp_edited_3 = stringResp_edited_2.replace("'", "\"")


print(stringResp_edited_3)

BinanceList = json.loads(stringResp_edited_3)


print(BinanceList)

for i in range(0, 8):
    print(BinanceList[i]['symbol'], ": ", BinanceList[i]['roi'])
