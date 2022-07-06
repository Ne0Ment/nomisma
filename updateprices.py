import pymongo
from datetime import datetime, timedelta
client = pymongo.MongoClient("localhost",27017)
db = client['nomisma-db']

bonds = [i for i in db.bonds.find({})]

def CalcProfit(bond): # return fullprofit, then just coupon profit
    daysLeft = (bond['maturity_date']-datetime.now()).days
    marketDiff = bond['nominal']-bond['market_price']
    if 'coupons' not in bond.keys():
        return (marketDiff/daysLeft*365, 0)
    if bond['coupons']==[]:
        return (marketDiff/daysLeft*365, 0)
    if bond['market_price']==0:
        return (0,0)
    if bond['coupons'][-1]['coupon_type']=='COUPON_TYPE_CONSTANT':
        fp = (bond['coupon_quantity_per_year']*bond['coupons'][-1]['pay_one_bond']+marketDiff)/bond['market_price']
        cp = (bond['coupon_quantity_per_year']*bond['coupons'][-1]['pay_one_bond'])/bond['market_price']
        return (fp,cp)
    elif bond['coupons'][-1]['coupon_type']=='COUPON_TYPE_VARIABLE':
        fp = (marketDiff + bond['coupon_quantity_per_year']*bond['coupons'][-1]['pay_one_bond'] - bond['aci_value'])/bond['market_price']
        cp = (bond['coupon_quantity_per_year']*bond['coupons'][-1]['pay_one_bond'] - bond['aci_value'])/bond['market_price']
        return (fp, cp)
    else:
        couponSum = sum([i['pay_one_bond'] for i in bond['coupons']])
        fp = (couponSum+marketDiff)/bond['market_price']/daysLeft*365
        cp = couponSum/bond['market_price']/daysLeft*365
        return (cp, fp)

for bond in bonds:
    fp, cp = CalcProfit(bond)
    bond['profitability'] = fp
    bond['coupon_profitability'] = cp

for bond in bonds:
    db['bonds'].replace_one({"_id":bond["_id"]}, bond, upsert=True)