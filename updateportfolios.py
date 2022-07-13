import pymongo
from tinkof import FetchPortfolios
import asyncio
import os

connString = os.getenv('MONGODB_CONNSTRING')
dbName = os.getenv('MONGODB_DATABASE')

client = pymongo.MongoClient(connString)
db = client[dbName]
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