import pymongo
from tinkof import FetchPortfolios
import asyncio

client = pymongo.MongoClient("localhost", 27017)
db = client['nomisma-db']
allUsers = [i for i in db.users.find()]


async def main():
    for user in allUsers:
        portfolios = await FetchPortfolios(user['tinkoff-token'])
        db.users.update_one(
            {
                "_id": user['_id']
            },
            {
                '$set': {
                    'portfolios': portfolios
                }
            })

asyncio.run(main())