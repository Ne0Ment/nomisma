import tinkoff
from tinkoff.invest import AsyncClient
import asyncio 

def quotation2float(quot):
    return float(str(quot.units)+"."+str(quot.nano))

async def FetchPortfolios(tinkoffToken):
    async with AsyncClient(tinkoffToken) as tinkoff:
        accounts = await tinkoff.users.get_accounts()
        portfolios = []
        for account in accounts.accounts:
            portfolio = await tinkoff.operations.get_portfolio(account_id=account.id)
            bonds = {}
            for i in portfolio.positions:
                if i.instrument_type=='bond':
                    bonds[i.figi] = quotation2float(i.quantity_lots)
            portfolios.append({'name': account.name, 'bonds':bonds})
        return portfolios
async def FetchPrices(figis, tinkoffToken):
    async with AsyncClient(tinkoffToken) as tinkoff:
        return (await tinkoff.market_data.get_last_prices(figi=figis)).last_prices