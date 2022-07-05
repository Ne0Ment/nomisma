import asyncio
from db import DBHandler


async def main():
    db = DBHandler()
    tempKey = '4a5377c7804ecbfb715d818789ae77409f66713cdad9bc30be0d6b2e9b8e7c5a7d94e6541ac2c5fef3b67726d0cf30d864e055f0ced525aee40064eb2c19835c09a6a21f47cc79c4fef1ecb6be73caa96d11e8ddf5776ef1100a638835fbf561c166506a5612dfa4ce03c59319b5f7a681a2b7cb6d1c0d6fd53166c6096dfb97'
    
    await db.GetAllBonds();


asyncio.run(main())