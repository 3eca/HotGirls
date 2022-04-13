#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import Session

__author__ = '3eca'
__github__ = 'https://github.com/3eca'


class BaseParser:
    def __init__(self):
        self.base_url = r'https://ero-top.info/ero/'
        self.upload_url = r'https://ero-top.info/'
        self.base_page = None
        self.all_urls_content = []
        self.user_agent = UserAgent()
        self.session = Session()
        self.session.headers = {'User-Agent': self.user_agent.random}

        self.pages = self.__generate_pages()
        self.__get_all_urls_content()

    def __check_availability(self, url: str) -> str:
        """
        Проверка доступности url
        :param url: ссылка на сайт
        :return: содержимое сайта
        """
        response = self.session.get(url=url)
        if response.status_code != 200:
            response.raise_for_status()
        else:
            return response.text

    def __get_last_page(self) -> int:
        """
        Формирование шаблона всех страниц с контентом
        :return: последняя страница с контентом
        """
        page = BeautifulSoup(
            self.__check_availability(self.base_url), 'html.parser'
        )
        pages = page.find('span', class_='navigat').find_all('a')[-1].get(
            'href')
        pages = re.split(self.base_url, pages)
        pages = re.findall(r'^\w+.?', pages[-1])
        self.base_page = self.base_url + pages[0]
        return int(
            page.find('span', class_='navigat').find_all('a')[-1].text
        )

    def __generate_pages(self) -> tuple:
        """
        :return: кортеж сгенирированых url с контентом
        """
        return tuple(
            [self.base_page + str(page) for page in
             range(1, self.__get_last_page() + 1)]
        )

    def __get_all_urls_content(self) -> None:
        for page in self.pages:
            current_url = self.__check_availability(url=page)
            content = BeautifulSoup(current_url, 'html.parser')
            content = content.find_all('div', id='short-stori')
            extract_urls_story = [url.find('a').get('href') for url in content]
            [self.all_urls_content.append(url) for url in
             extract_urls_story if url]
            # break

    # def __get_url_from_page(self, url: str) -> list:
    #     page = BeautifulSoup(self.__check_availability(url), 'html.parser')
    #     url_image = page.find('div', style='text-align:center;').find_all('a')
    #     url_image = [link.get('href') for link in url_image]
    #     return url_image
    #
    # def upload_image(self, url: str) -> None:
    #     for url in self.__get_url_from_page(url):
    #         image_name = re.split('/', url)[-1]
    #         image_path = bot_config.DIR_PATH + '/' + image_name
    #         with open(image_path, 'wb') as f:
    #             f.write(requests.get(url).content)

    def upload_image_2(self, url: str) -> list:
        page = BeautifulSoup(self.__check_availability(url), 'html.parser')
        url_image = page.find('div', style='text-align:center;').find_all('a')
        url_image = [link.get('href') for link in url_image]
        return url_image


if __name__ == '__main__':
    pass
