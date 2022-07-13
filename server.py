import quart
from dataclasses import dataclass
from quart_cors import cors
from quart_schema import validate_request

from db import DBHandler
from tele import Telegramhandler
from utility import CheckTelegramHash, HashToken, RandomConfCode

app = quart.Quart('main',
                static_folder="web/dist/assets")
app = cors(app, allow_origin="*")

@dataclass
class TempKeyData:
    temp_key: str

@dataclass
class SetNewTokenData:
    temp_key: str
    new_token: str
    conf_code: str

@app.route('/')
async def mainPage():
    return await quart.send_from_directory('web/dist','index.html')

@app.route('/Login', methods=['POST'])
async def CheckTelegramAuth():
    requestData = await quart.request.get_json()
    if "id" not in requestData or not isinstance(requestData["id"], int):
        return quart.abort(400)

    if CheckTelegramHash(requestData, telegramSecret):
        response = quart.jsonify(await db.LoginUser(requestData))
    else:
        response = quart.jsonify({'status': False})
    return response

@app.route('/GetConfCode', methods=['POST'])
@validate_request(TempKeyData)
async def GetConfCode(data: TempKeyData):
    confCode = RandomConfCode()
    response = await db.SetConfCode(data.temp_key, confCode)
    if response['status']==True:
        telegramId = (await db.FindUser(tempKey=data.temp_key))['telegram-id']
        await teleHandler.SendConfCode(telegramId, confCode)
    return quart.jsonify(response)

@app.route('/SetNewToken', methods=['POST'])
@validate_request(SetNewTokenData)
async def SetNewToken(data: SetNewTokenData):
    response = await db.UpdateToken(data.temp_key, data.conf_code, data.new_token)
    return quart.jsonify(response)

@app.route('/GetPortfolios', methods=['POST'])
@validate_request(TempKeyData)
async def GetPortfolios(data: TempKeyData):
    response = await db.GetPortfolios(data.temp_key)
    return quart.jsonify(response)

@app.route('/GetPortfolioSums', methods=['POST'])
@validate_request(TempKeyData)
async def GetPortfolioSums(data: TempKeyData):
    response = await db.GetPortfolioSums(data.temp_key)
    return quart.jsonify(response)
    
@app.route('/GetAllBonds', methods=['GET'])
async def GetAllBonds():
    return quart.jsonify(await db.GetAllBonds())

teleToken = '5437510552:AAF8_OLh1OmGgibhzn1w2Bc4BCDOd1pFaM4'
telegramSecret = HashToken(teleToken.encode('utf-8'))
db = DBHandler(connString='mongodb://localhost:27017/', dbName='nomisma-db')
#db = DBHandler()
teleHandler = Telegramhandler(teleToken)
#app.run(host='0.0.0.0', port=80)
#app.run(debug=True)