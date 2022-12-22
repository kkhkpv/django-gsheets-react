import pygsheets
from bs4 import BeautifulSoup
import requests
import time
from celery import shared_task
from .models import Order


def get_orders():
    client = pygsheets.authorize(service_account_file="credentials.json")
    shs = client.open('demotable')
    data = shs.sheet1.get_all_records()
    return data


def get_dollar_course(date):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    course = soup.find(id='R01235').value.text
    course = float(course.replace(",", "."))
    return course


@shared_task
def get_parsed_data():
    start = time.time()
    orders = get_orders()
    Order.objects.all().delete()
    for order in orders:
        order_number = order.get("OrderNumber")
        cost = int(order.get("Cost"))
        delivery_date = order.get("DeliveryDate")
        dollar_course = get_dollar_course(delivery_date)
        rouble_cost = int(cost * dollar_course)
        print(f"order {order['Id']} add")
        order_to_save = Order(order_number=order_number, cost=cost,
                              delivery_date="-".join(reversed(delivery_date.split("."))), rouble_cost=rouble_cost,)
        order_to_save.save()

    print(time.time()-start)


# import pygsheets
# from bs4 import BeautifulSoup
# import time
# import aiohttp
# import asyncio


# def get_orders():
#     client = pygsheets.authorize(service_account_file="credentials.json")
#     shs = client.open('demotable')
#     data = shs.sheet1.get_all_records()
#     return data


# async def get_dollar_course(session, url):
#     async with session.get(url) as response:
#         data = await response.text()
#         course = BeautifulSoup(data, 'lxml').find(id='R01235').value.text
#         course = float(course.replace(',', '.'))
#         return course


# async def main():
#     start = time.time()
#     tasks = []
#     orders = get_orders()
#     async with aiohttp.ClientSession() as session:
#         for order in orders:
#             tasks.append(get_dollar_course(
#                 session, f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={order['DeliveryDate']}"))
#         courses = await asyncio.gather(*tasks)
#         for indx, order in enumerate(orders):
#             order["RoubleCost"] = courses[indx] * int(order["Cost"])
#             print(order)
#     print(time.time()-start)


# if __name__ == "__main__":
#     asyncio.run(main())
