import asyncio
from db import DBHandler


async def main():
    db = DBHandler()
    tempKey = '5ec9658b7acb091c24331b3bcc5d7e6483e6bd990c4cd3b639460c6137336a6a25ce6489def78b503187163f220243aa42ad7a77549f4b93159c8b438210b423adc053d545366b29c7f3b6d8ee3002b93e743a3dd00c4151152dd2d1d8a335407a5e7f1931e9fd0ccf9b07be2d245907d466d0b4c623bf3557484915a9ab640c'
    
    print(await db.GetPortfolioSums(tempKey))


asyncio.run(main())