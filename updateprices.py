import pymongo
from datetime import datetime, timedelta
from db import DBHandler
from tinkof import FetchPrices, quotation2float
import asyncio

client = pymongo.MongoClient("localhost",27017)
db2 = client['nomisma-db']


def CalcProfit(bond):
    daysLeft = (bond['maturity_date']-datetime.now()).days
    marketDiff = bond['nominal']-bond['market_price']
    if bond['market_price'] == 0:
        return (0, 0)
    if 'coupons' not in bond.keys():
        return (marketDiff/bond['market_price']/daysLeft*365, 0)
    if bond['coupons'] == []:
        return (marketDiff/bond['market_price']/daysLeft*365, 0)
    if bond['coupons'][-1]['coupon_type'] == 'COUPON_TYPE_CONSTANT':
        fp = (bond['coupon_quantity_per_year']*bond['coupons'][-1]
              ['pay_one_bond']+marketDiff)/bond['market_price']
        cp = (bond['coupon_quantity_per_year']*bond['coupons']
              [-1]['pay_one_bond'])/bond['market_price']
        return (fp, cp)
    elif bond['coupons'][-1]['coupon_type'] == 'COUPON_TYPE_VARIABLE':
        fp = (marketDiff + bond['coupon_quantity_per_year']*bond['coupons']
              [-1]['pay_one_bond'] - bond['aci_value'])/bond['market_price']
        cp = (bond['coupon_quantity_per_year']*bond['coupons'][-1]
              ['pay_one_bond'] - bond['aci_value'])/bond['market_price']
        return (fp, cp)
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
        bond['market_price'] = quotation2float(price_dict[bond['figi']])*bond['nominal']/100
        fp, cp = CalcProfit(bond)
        bond['profitability'] = fp
        bond['coupon_profitability'] = cp
    for bond in bonds:
        db2['bonds'].replace_one({"_id": bond["_id"]}, bond, upsert=True)

asyncio.run(main())