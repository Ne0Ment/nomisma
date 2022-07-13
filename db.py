from functools import wraps
import motor.motor_asyncio
import secrets
import bcrypt
from tinkof import FetchPortfolios
from utility import Random128Hex, CalculateNominalPortfolio, CalculateMarketPortfolio
import os

class DBHandler():
    def __init__(self, connString=None, dbName=None):
        if (connString==None):
            connString = os.getenv('MONGODB_CONNSTRING')
        if (dbName==None):
            dbName = os.getenv('MONGODB_DATABASE')
        self.db = motor.motor_asyncio.AsyncIOMotorClient(connString, serverSelectionTimeoutMS=5000)[dbName]

    def WrongTempCode(self):
        return {'status': False, 'error': 'wrong_temp_code'}
    def WrongPassword(self):
        return {'status': False, 'error': 'wrong_password'}
    def WrongTempKey(self):
        return {'status': False, 'error': 'wrong_temp_key'}
    def StatusTrue(self):
        return {'status': True}
    def CheckPassword(self, p1, p2):
        return bcrypt.checkpw(bytes(p1, encoding='utf8'), p2)
    def HashPassword(self, password):
        return bcrypt.hashpw(bytes(password, encoding='utf8'), bcrypt.gensalt(10))

    async def FindUser(self, tempKey=None, telegramId=None):
        if tempKey:
            return await self.db.users.find_one({'temp-key': tempKey})
        else:
            return await self.db.users.find_one({'telegram-id': telegramId})
        
    async def GetByFigis(self, figis):
        return await self.db.bonds.find({
            'figi': {
                '$in': figis
            }
            }).to_list(5000)

    async def CreateTempKey(self, userId):
        tempKey = Random128Hex()
        await self.db.users.update_one(
            {
                "_id":userId
            }, 
            {
                "$set": {
                    "temp-key": tempKey
                }
            })
        return tempKey

    async def CreateUser(self, user):
        tempKey = Random128Hex();
        userObj = {
            'telegram-id': user['id'],
            'tinkoff-token': '',
            'temp-key': tempKey,
            'confirmation-code': Random128Hex(),
            'portfolios': []
        }
        inserted = await self.db.users.insert_one(userObj)
        return {'status': True, 'temp_key': await self.CreateTempKey(inserted.inserted_id)}

    async def LoginUser(self, user):
        foundUser = await self.FindUser(telegramId=user['id'])
        if foundUser:
            return {'status': True, 'temp_key': await self.CreateTempKey(foundUser['_id'])}
        else:
            return await self.CreateUser(user)

    def authorized(func):
        @wraps(func)
        async def wrapper(self, tempKey, *args, **kwargs):
            if foundUser := await self.FindUser(tempKey=tempKey):
                return await func(self, tempKey, foundUser, *args, **kwargs)
            else:
                return self.WrongTempKey()
        return wrapper

    @authorized
    async def SetConfCode(self, tempKey, foundUser, confCode):
        await self.db.users.update_one(
            {
                "temp-key": tempKey   
            },
            {
                '$set': {
                    "confirmation-code": confCode
                }
            })
        return self.StatusTrue()

    @authorized
    async def UpdateToken(self, tempKey, foundUser, confCode, newToken):
        if foundUser['confirmation-code']==confCode:
            await self.db.users.update_one(
                {
                    "temp-key": tempKey   
                },
                {
                    '$set': {
                        'confirmation-code': secrets.token_hex(128),
                        'tinkoff-token': newToken
                    }
                })
            await self.UpdatePortfolios(tempKey)
            return self.StatusTrue()
        else:
            return self.WrongTempCode()
    @authorized
    async def GetPortfolios(self, tempKey, foundUser):
        portfolios = foundUser['portfolios']
        for portfolio in portfolios:
            bonds = await self.GetByFigis(list(portfolio['bonds'].keys()))
            for bond in bonds:
                bond['count'] = portfolio['bonds'][bond['figi']]
            portfolio['bonds'] = bonds
        return {'status': True, 'portfolios': portfolios}

    @authorized
    async def UpdatePortfolios(self, tempKey, foundUser):
        if tinkoffToken := foundUser['tinkoff-token']:
            portfolios = await FetchPortfolios(tinkoffToken)
            await self.db.users.update_one(
                {
                    "temp-key": tempKey   
                },
                {
                    '$set': {
                        'portfolios': portfolios
                    }
                })
            return self.StatusTrue()
        else:
            return {'status': False, 'error':'token_not_initialized'}

    @authorized
    async def GetPortfolioSums(self, tempKey, foundUser):
        portfolios = (await self.GetPortfolios(tempKey))['portfolios']
        return {'status': True, 'market_sum': CalculateMarketPortfolio(portfolios), 'nominal_sum': CalculateNominalPortfolio(portfolios)}
    
    async def GetAllBonds(self):
        allBonds = await self.db.bonds.find().to_list(length=5000)
        return {'status': True, 'bonds': allBonds}
    

    """
    async def create_user(self, username, password):
        user_dict = {
            "t_username": username,
            "telegram_id": '',
            "tinkoff_token": "",
            "pass_hash": bcrypt.hashpw(bytes(password, encoding='utf8'), bcrypt.gensalt(10)),
            "temp_key": ''
        } 
        inserted = await self.db.users.insert_one(user_dict);
        return {'status': True, 'temp_key': self.create_temp_key(inserted.inserted_id)}

    async def login_user(self, username, password):
        found_user = await self.find_user(username=username)
        if found_user:
            if self.check_password(password, found_user['pass_hash']):
                return {'status': True, 'temp_key': await self.create_temp_key(found_user['_id'])}
            else: 
                return self.wrong_password()
                
        else:
            return self.create_user(username, password)

        
    async def update_token(self, temp_key, password, new_token):
        found_user = await self.find_user(temp_key=temp_key)
        if found_user:
            if self.check_password(password, found_user['pass_hash']):
                await self.db.users.update_one(
                {
                    "_id": found_user['_id']   
                },
                {
                    '$set': {
                        "tinkoff_token": new_token
                    }
                })
                return self.status_true()
            else:
                return self.wrong_password()
        else:
            return self.wrong_temp_key()
        
    async def update_password(self, temp_key, old_password, new_password):
        found_user = await self.find_user(temp_key=temp_key)
        if found_user:
            if self.check_password(old_password, found_user['pass_hash']):
                await self.db.users.update_one(
                {
                    "_id": found_user['_id']
                },
                {
                    '$set': {
                        'pass_hash': self.hash_password(new_password)
                    }
                })
                return self.status_true()
        else:
            return self.wrong_temp_key()
    """