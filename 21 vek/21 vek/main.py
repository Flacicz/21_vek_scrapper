import datetime
import json

import requests
from bs4 import BeautifulSoup
import time

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
}


def get_data():
    curr_time = datetime.datetime.now().strftime('%d_%m_%Y')
    url = 'https://www.21vek.by/notebooks/region:ostrovets/'
    response = requests.get(url=url, headers=headers)

    # with open("index.html", "w", encoding='utf-8') as file:
    #     file.write(response.text)

    soup = BeautifulSoup(response.text, "lxml")

    pagination_count = int(
        soup.find("div", id="j-paginator").find_all('a')[-2].text
    )
    data = []
    for page in range(1, pagination_count + 1):
        url = f'https://www.21vek.by/notebooks/page:{page}/region:ostrovets/'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        notebooks = soup.find("ul", id=f'j-result-page-{page}') \
            .find_all("li", class_="result__item")

        for item in notebooks:
            notebooks_name = item.find('dl').find('div', class_='catalog-result__item_data') \
                .find('dt', class_='result__root') \
                .find('a', class_='result__link') \
                .find('span', class_='result__name').text.strip()

            in_stock = item.find('dl').find('div', class_='catalog-result__item_data') \
                .find('dt', class_='result__root') \
                .find('div', class_='catalog-result__item_meta') \
                .find('span', class_='g-catalog-status').text.strip()

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[0].find_all('td')[0].text.strip() == 'Диагональ экрана':
                    screen_diagonal = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[0].find_all('td')[-1].text.strip(' "').strip(" '")
                else:
                    screen_diagonal = '-'
            except Exception:
                screen_diagonal = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[1].find_all('td')[0].text.strip() == 'Разрешение экрана':
                    screen_resolution = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[1].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[0].find_all('td')[0].text.strip() == 'Разрешение экрана':
                    screen_resolution = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[0].find_all('td')[-1].text.strip()
                else:
                    screen_resolution = '-'
            except Exception:
                screen_resolution = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[2].find_all('td')[0].text.strip() == 'Частота обновления экрана':
                    screen_refresh_rate = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[2].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[1].find_all('td')[0].text.strip() == 'Частота обновления экрана':
                    screen_refresh_rate = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[1].find_all('td')[-1].text.strip()
                else:
                    screen_refresh_rate = '-'
            except Exception:
                screen_refresh_rate = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[3].find_all('td')[0].text.strip() == 'Модель процессора':
                    processor_model = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[3].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[2].find_all('td')[0].text.strip() == 'Модель процессора':
                    processor_model = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[2].find_all('td')[-1].text.strip()
                else:
                    processor_model = '-'
            except Exception:
                processor_model = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[4].find_all('td')[0].text.strip() == 'Объём оперативной памяти':
                    amount_of_RAM = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[4].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[3].find_all('td')[0].text.strip() == 'Объём оперативной памяти':
                    amount_of_RAM = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[3].find_all('td')[-1].text.strip()
                else:
                    amount_of_RAM = '-'
            except Exception:
                amount_of_RAM = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[5].find_all('td')[0].text.strip() == 'Емкость SSD':
                    SSD_capacity = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[5].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[4].find_all('td')[0].text.strip() == 'Емкость SSD':
                    SSD_capacity = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[4].find_all('td')[-1].text.strip()
                else:
                    SSD_capacity = '-'
            except Exception:
                SSD_capacity = '-'

            try:
                if item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[7].find_all('td')[0].text.strip() == 'Модель видеокарты':
                    video_card_model = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[7].find_all('td')[-1].text.strip()
                elif item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[6].find_all('td')[0].text.strip() == 'Модель видеокарты':
                    video_card_model = item.find('dl').find('div', class_='catalog-result__item_data') \
                        .find('dd', class_='result__desc') \
                        .find('div', class_='result__attrs').find('table') \
                        .find_all('tr')[6].find_all('td')[-1].text.strip()
                else:
                    video_card_model = '-'
            except Exception:
                video_card_model = '-'

            try:
                price = item.find('dl').find('div', class_='catalog-result__item_tools result__tools') \
                    .find('span', class_='g-price result__price cr-price__in') \
                    .find('span', class_='g-item-data').get('data-price')
            except Exception:
                price = '-'

            try:
                for_discount = item.find('dl').find('div', class_='catalog-result__item_tools') \
                    .find('span', class_='g-price result__price cr-price__in') \
                    .find('span', class_='g-price g-oldprice result__oldprice').text.strip()
            except Exception:
                for_discount = 'Нету скидки'

            # print(
            #     f'{screen_diagonal}---{screen_resolution}---{screen_refresh_rate}---{processor_model}---{amount_of_RAM}---{SSD_capacity}---{video_card_model}---{price}---{for_discount}'
            # )

            data.append(
                {
                    'Название': notebooks_name,
                    'Наличие': in_stock,
                    'Цена': price,
                    'Цена со скидкой': for_discount,
                    'Диагональ экрана': screen_diagonal,
                    'Разрешение экрана': screen_resolution,
                    'Частота обновления экрана': screen_refresh_rate,
                    'Модель процессора': processor_model,
                    'Объём оперативной памяти': amount_of_RAM,
                    'Емкость SSD': SSD_capacity,
                    'Модель видеокарты': video_card_model,
                }
            )

        with open(f'data_{curr_time}.json', 'a', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
