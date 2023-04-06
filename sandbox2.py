import aiofiles
import asyncio

async def main():
    async with aiofiles.open('ditto_moves.txt', mode='w') as f:
        await f.write('transform')

asyncio.run(main())