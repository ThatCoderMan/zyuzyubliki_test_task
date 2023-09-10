import re

from lxml import html
from sqlalchemy import func, select

from app.core.client_session import ClientSession
from app.core.db import AsyncSessionLocal
from app.models import ParsingData


async def parse_products():
    price_sum = 0
    product_count = 0

    async with AsyncSessionLocal() as db_session:
        parsing_data_list = await db_session.scalars(select(ParsingData))
        total_count = await db_session.execute(func.count(ParsingData.id))
        total_count = total_count.scalars().first()

    for parsing_data in parsing_data_list:
        url = parsing_data.url
        xpath = parsing_data.xpath

        async with ClientSession() as session:
            response = await session.get_data(url)
            if response:
                tree = html.fromstring(str(response))
                html_price = tree.xpath(xpath)
                if html_price:
                    if isinstance(html_price[0], html.HtmlElement):
                        html_price = html_price[0].text_content()
                    numbers_text = re.sub(r"\\x.{2}", "", str(html_price))
                    numbers = re.findall(r"(\d+)", numbers_text)
                    if numbers:
                        price_sum += int("".join(numbers))
                        product_count += 1
    price_avg = price_sum / product_count if product_count else 0
    return {
        "count": product_count,
        "price_avg": price_avg,
        "total": total_count,
    }
