import asyncio


async def task1():
    a = 5
    while a:
        print("Task 1 is running...")
        a -= 1
        await asyncio.sleep(1)


async def task2():
    while True:
        print("Task 2 is running...")
        await asyncio.sleep(1)


async def main():
    asyncio.create_task(task1())
    asyncio.create_task(task2())
    await asyncio.gather()

if __name__ == '__main__':
    asyncio.run(main())
