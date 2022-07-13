import pymongo
from datetime import datetime, timedelta
from db import DBHandler
from tinkof import FetchPrices, quotation2float
import asyncio
import os

connString = os.getenv('MONGODB_CONNSTRING')
dbName = os.getenv('MONGODB_DATABASE')

client = pymongo.MongoClient(connString)
db2 = client[dbName]


def CalcProfit(bond):
    daysLeft = (bond['maturity_date']-datetime.now()).days
    marketDiff = bond['nominal']-bond['market_price']-bond['aci_value']
    if bond['market_price'] == 0:
        return (0, 0)

    if 'coupons' not in bond.keys():
        return (marketDiff/bond['market_price']/daysLeft*365, 0)

    if bond['coupons'] == []:
        return (marketDiff/bond['market_price']/daysLeft*365, 0)

    if bond['coupons'][-1]['coupon_type'] == 'COUPON_TYPE_CONSTANT':
        c = sum([i['pay_one_bond'] for i in bond['coupons']])/bond['market_price']/daysLeft*365
        m = marketDiff/bond['market_price']/daysLeft*365
        return (c+m, c)

    elif bond['coupons'][-1]['coupon_type'] == 'COUPON_TYPE_VARIABLE':
        c = bond['coupons'][-1]['pay_one_bond']*len(bond['coupons'])/bond['market_price']/daysLeft*365
        m = marketDiff/bond['market_price']/daysLeft*365
        return (c+m, c)

    else:
        couponSum = sum([i['pay_one_bond'] for i in bond['coupons']])
        fp = (couponSum+marketDiff)/bond['market_price']/daysLeft*365
        cp = couponSum/bond['market_price']/daysLeft*365
        return (cp, fp)


async def main():
    db = DBHandler()
    bonds = [i for i in (await db.GetAllBonds())['bonds']]
    bond_figis = [i['figi'] for i in bonds]
    prices = await FetchPrices(bond_figis, 't.CbJu2z3-n0MfU9Dbtbk9kxlGvnml00A7upkA6WvXDjQcpwmtqQyyJ4z00oS17cMfVFO_twNOZ5OcdHvMLyHbwg')
    price_dict = {}
    for i in prices:
        price_dict[i.figi] = i.price
    for bond in bonds:
        bond['market_price'] = quotation2float(
            price_dict[bond['figi']])*bond['nominal']/100
        fp, cp = CalcProfit(bond)
        bond['profitability'] = fp
        bond['coupon_profitability'] = cp
    for bond in bonds:
        db2['bonds'].replace_one({"_id": bond["_id"]}, bond, upsert=True)

asyncio.run(main())
