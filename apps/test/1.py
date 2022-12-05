import random
import time
import httpx
import asyncio
import re


async def spider_email(session, url):
    res = await session.get(url)
    rec = re.compile("1[3456789]\d\s?\d{4}\s?\d{4}")
    results = rec.findall(res.text)
    for i in range(len(results)):
        print(f"{i},爬取的结果为----{results[i]}")


async def main(url):
    async with httpx.AsyncClient() as session:
        tasks = [spider_email(session, url) for _ in range(10)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.perf_counter()

    # stringGroup = "ABCDEFGHIJKLMNO"
    # randomStr = "".join([random.choice(stringGroup) for _ in range(10)])
    # print(5/10)
    # for i in range(1000):
    #     print("".join([random.choice(stringGroup) for _ in range(10)]))
    url = "https://www.zhaohaowang.com/"

    asyncio.run(main(url))

    print(time.perf_counter() - start_time)
