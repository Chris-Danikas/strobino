import asyncio

async def main():
    beat = True
    print(beat)
    await asyncio.sleep(1)
    beat = False
    print(beat)

asyncio.run(main())
print('lol')