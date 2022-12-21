from celery import shared_task
import pygsheets
from bs4 import BeautifulSoup
import time
import pygsheets
from bs4 import BeautifulSoup
import time
import aiohttp
import asyncio
import math


def get_orders():
    client = pygsheets.authorize(service_account_file="credentials.json")
    shs = client.open('demotable')
    data = shs.sheet1.get_all_records()
    return data


async def get_dollar_course(session, url):
    async with session.get(url) as response:
        data = await response.text()
        course = BeautifulSoup(data, 'lxml').find(id='R01235').value.text
        course = float(course.replace(',', '.'))
        return course


async def main():
    start = time.time()
    tasks = []
    orders = get_orders()
    async with aiohttp.ClientSession() as session:
        for order in orders:
            tasks.append(get_dollar_course(
                session, f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={order['DeliveryDate']}"))
        courses = await asyncio.gather(*tasks)
        for indx, order in enumerate(orders):
            order["RoubleCost"] = math.floor(
                courses[indx] * int(order["Cost"]))
            print(order)
    print(time.time()-start)


@shared_task
def task():
    asyncio.run(main())
