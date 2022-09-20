import asyncio
import aiohttp


async def main(url, path):
    async with aiohttp.ClientSession() as session:
        for i in range(4000):
            async with session.post(url, data={'file': open(path.format(i), 'rb')}):
                pass

def call(*args):
    asyncio.run(main(*args))


if __name__ == "__main__":
    call()