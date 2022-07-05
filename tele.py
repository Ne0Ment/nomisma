import telegram

class Telegramhandler():
    def __init__(self, telegramToken):
        self.token = telegramToken
        self.bot = telegram.Bot(token=self.token)
    async def SendConfCode(self, userId, confCode):
        async with self.bot:
            return await self.bot.send_message(chat_id=userId, text=f'Confirmation code: {confCode}')