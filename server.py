from grpc import stream_stream_rpc_method_handler
import quart
from quart import request
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
    if CheckTelegramHash(requestData, telegramSecret):
        response = quart.jsonify(await db.LoginUser(requestData))
    else:
        response = quart.jsonify({'status': False})
    return response

@validate_request(TempKeyData)
@app.route('/GetConfCode', methods=['POST'])
async def GetConfCode():
    requestData = await quart.request.get_json()
    confCode = RandomConfCode()
    response = await db.SetConfCode(requestData['temp_key'], confCode)
    if response['status']==True:
        telegramId = (await db.FindUser(tempKey=requestData['temp_key']))['telegram-id']
        await teleHandler.SendConfCode(telegramId, confCode)
    return quart.jsonify(response)

@validate_request(SetNewTokenData)
@app.route('/SetNewToken', methods=['POST'])
async def SetNewToken():
    requestData = await quart.request.get_json()
    tempKey, newToken, confCode = requestData['temp_key'],requestData['new_token'],requestData['conf_code']
    response = await db.UpdateToken(tempKey, confCode, newToken)
    return quart.jsonify(response)

@validate_request(TempKeyData)
@app.route('/GetPortfolios', methods=['POST'])
async def GetPortfolios():
    requestData = await quart.request.get_json()
    tempKey = requestData['temp_key']
    response = await db.GetPortfolios(tempKey)
    return quart.jsonify(response)

@validate_request(TempKeyData)
@app.route('/GetPortfolioSums', methods=['POST'])
async def GetPortfolioSums():
    requestData = await quart.request.get_json()
    tempKey = requestData['temp_key']
    response = await db.GetPortfolioSums(tempKey)
    return quart.jsonify(response)
    
@app.route('/GetAllBonds', methods=['GET'])
async def GetAllBonds():
    return quart.jsonify(await db.GetAllBonds())

teleToken = '5437510552:AAF8_OLh1OmGgibhzn1w2Bc4BCDOd1pFaM4'
telegramSecret = HashToken(teleToken.encode('utf-8'))
db = DBHandler()
teleHandler = Telegramhandler(teleToken)
#app.run(host='0.0.0.0', port=80)
#app.run(debug=True)