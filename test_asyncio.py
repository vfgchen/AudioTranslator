import asyncio

async def task1():
    await asyncio.sleep(1)
    print("t1--------------")
    return 1

async def task2():
    await asyncio.sleep(2)
    print("t2--------------")
    return 2

async def task3():
    await asyncio.sleep(3)
    print("t3--------------")
    return 3

async def main():
    t1 = task1()
    t2 = task2()
    t3 = task3()
    result = await asyncio.gather(t1, t2, t3)
    for item in result:
        print(f"main: {item}")

if __name__ == "__main__":
    asyncio.run(main())
