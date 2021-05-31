import json, hmac, hashlib, time, requests, base64, os
from requests.auth import AuthBase

CurrencyList = [
    "USDT",
    "ETH",
    "ANKR",
    "ADA",
    "ALGO",
    "CTSI"
    ]

comparer = {}

looping = True
boolrecord = False

API_KEY  = ""
API_SECRET  = ""

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or "")
        hmac_key = base64.b64decode(self.secret_key)
        bitearray = bytearray(self.secret_key, 'utf-8')
        signature = hmac.new(bitearray, message.encode(), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        })
        return request

#check all currencies and wallets
def checker(boolrecord):
    checkertext=""
    tot = 0
    for i in CurrencyList:
        lookfor = "accounts/"+i
        r = requests.get(api_url +lookfor, auth=auth)
        Crypto = str(json.dumps(r.json()["data"]["balance"]["currency"]))
        Quantity = str(json.dumps(r.json()["data"]["balance"]["amount"]))
        value = rjson.json()["data"]["rates"][i]
        conversion = str(round(float(Quantity.strip('"'))/float(value),2))
        tot = tot + float(conversion)
        if boolrecord == True:
            arrowatend = ""
            if float(comparer[i]) < float(conversion):
                arrowatend = "\t\u2191"
            elif float(comparer[i]) > float(conversion):
                arrowatend = "\t\u2193"
            else:
                arrowatend = "\t\u25A0"

            checkertext = checkertext + Crypto +"\t" + " Quantity: " +"\t"+ str(round(float(Quantity.strip('"')),2)) +"\t" + " EUR: " +"\t" + conversion + arrowatend + "\t" + comparer[i] + "\n"



            
        
        if boolrecord == False:
            comparer[i] = conversion

    os.system('cls')
    return checkertext, tot 
    

api_url = 'https://api.coinbase.com/v2/'

while looping is True:
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
    #Check all conversions
    lookfor = "exchange-rates?currency=EUR"
    rjson = requests.get(api_url +lookfor, auth=auth)
    container = checker(boolrecord)
    print(container[0])
    print("Totale: " + str(round(container[1],2)))
    boolrecord = True
    time.sleep(5)
    




# {u'data': {u'username': None, u'resource': u'user', u'name': u'User'...

