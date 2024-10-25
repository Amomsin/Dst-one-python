import asyncio
from adddata import update_database
from demo_group_reply_text import nmain


async def task1():
    while True:
        await update_database()
        await asyncio.sleep(300)


async def task2():
    await nmain()


async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())
