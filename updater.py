from tinkoff.invest import Client
import pymongo
import tinkoff.invest.schemas
from datetime import datetime, timedelta
import pytz
import time


def quotation2float(quot):
    return float(str(quot.units)+"."+str(quot.nano))

def CouponProfitability(bond):
    coupons = sum([i['pay_one_bond'] for i in bond.coupons])
    return coupons/bond.nominal/(bond.maturity_date-pytz.UTC.localize(datetime.now())).days*365

def Profitability(bond):
    coupons = sum([i['pay_one_bond'] for i in bond.coupons]) + (bond.nominal-bond.market_price)
    return coupons/bond.market_price/(bond.maturity_date-pytz.UTC.localize(datetime.now())).days*365


client = pymongo.MongoClient("localhost", 27017)
db = client['nomisma-db']
tinkoffToken = 't.CbJu2z3-n0MfU9Dbtbk9kxlGvnml00A7upkA6WvXDjQcpwmtqQyyJ4z00oS17cMfVFO_twNOZ5OcdHvMLyHbwg'

with Client(tinkoffToken) as tinkoff:
    all_bonds = [i for i in tinkoff.instruments.bonds().instruments if i.currency=='rub']
    prices = tinkoff.market_data.get_last_prices(
        figi=[i.figi for i in all_bonds]).last_prices
    price_dict = {}
    for i in prices:
        price_dict[i.figi] = i.price
    for bond in all_bonds:
        bond.klong = quotation2float(bond.klong)
        bond.kshort = quotation2float(bond.kshort)
        bond.dlong = quotation2float(bond.dlong)
        bond.dshort = quotation2float(bond.dshort)
        bond.dlong_min = quotation2float(bond.dlong_min)
        bond.dshort_min = quotation2float(bond.dshort_min)
        bond.min_price_increment = quotation2float(bond.min_price_increment)

        bond.nominal_currency = bond.nominal.currency
        bond.nominal = quotation2float(bond.nominal)
        bond.placement_price_currency = bond.placement_price.currency
        bond.placement_price = quotation2float(bond.placement_price)
        bond.aci_value_currency = bond.aci_value.currency
        bond.aci_value = quotation2float(bond.aci_value)
        bond.trading_status = bond.trading_status._value_

        bond.market_price = bond.nominal/100*quotation2float(price_dict[bond.figi])

        bond._id = bond.figi
        try:
            coupons_response = tinkoff.instruments.get_bond_coupons(
                figi=bond.figi, to=bond.maturity_date+timedelta(days=5), from_=datetime.now()).events
            coupons = []
            for coupon in coupons_response:
                coupon = vars(coupon)
                coupon['pay_one_bond_currency'] = coupon['pay_one_bond'].currency
                coupon['pay_one_bond'] = quotation2float(
                    coupon['pay_one_bond'])
                coupon['coupon_type'] = coupon['coupon_type']._name_
                coupons.append(coupon)
            bond.coupons = coupons
            bond.coupon_profitability = CouponProfitability(bond)
            bond.profitability = Profitability(bond)
        except Exception as e:
            pass
        time.sleep(0.25)

bonds_dicts = [vars(i) for i in all_bonds]
for bond in bonds_dicts:
    db['bonds'].replace_one({"_id": bond["_id"]}, bond, upsert=True)
