import asyncio
import httpx



def outer():
    async def f():
        await asyncio.sleep(2)
        print('hello')
        return 1

    # asyncio.run(f())
    async def f2():
        async with httpx.AsyncClient() as client:
            r = await client.get('https://jsonplaceholder.typicode.com/posts/1')
            print(r.text)
            return 2

    async def runner():
        results = await asyncio.gather(f(), f2())
        print(type(results))

    asyncio.run(runner())


outer()