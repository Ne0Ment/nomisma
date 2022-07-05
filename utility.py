import hashlib
import hmac
import random
import string
import secrets

def HashToken(token):
    return hashlib.sha256(token)

def CheckTelegramHash(dataObj, secret):
    data = [(k, dataObj[k]) for k in sorted(list(dataObj.keys()))]
    dataCheckString = '\n'.join([f'{i[0]}={i[1]}' for i in data if i[0]!='hash'])
    hmacHex = hmac.new(key=secret.digest(),
                       msg=bytes(dataCheckString,encoding='utf-8'),
                       digestmod=hashlib.sha256).hexdigest()
    return hmacHex==dataObj['hash']

def Random128Hex():
    return secrets.token_hex(128)

def RandomConfCode(k=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))

def CalculateNominalPortfolio(portfolios):
    nominalSum = 0
    for portfolio in portfolios:
        for bond in portfolio['bonds']:
            nominalSum += bond['nominal']*bond['count']
    return nominalSum

def CalculateMarketPortfolio(portfolios):
    marketSum = 0
    for portfolio in portfolios:
        for bond in portfolio['bonds']:
            marketSum += bond['market_price']*bond['count']
    return marketSum

