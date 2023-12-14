import json
import os
from abc import ABC, abstractmethod
from typing import Mapping

import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_COUNT = 5


class APIGetVacancies(ABC):
    """Абстрактный класс задающий работу с API"""

    @abstractmethod
    def get_vacancies(self) -> list:
        pass


class HeadHunterAPI(APIGetVacancies):
    """Класс для работы с API сайта HeadHunter"""

    def __init__(self, key_word: str):
        """Создание экземпляра класса HeadHunterAPI.
        :param key_word: ключевое слово для поиска вакансии"""

        self.key_word = key_word
        self.__page = 0
        self.__params = {"text": key_word, "area": 113, "page": self.__page,
                         "per_page": 100}  # "area": 113 = поиск по России

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.key_word})'

    def get_vacancies(self) -> list:
        """Метод получения вакансий по заданным параметрам"""
        list_data = []
        for i in range(0, PAGE_COUNT):
            req = requests.get("https://api.hh.ru/vacancies", self.__params)
            data = req.content.decode()
            req.close()
            list_data.extend(json.loads(data)["items"])
            self.__page += 1
        return self.make_list_vacancies(list_data)

    @staticmethod
    def make_list_vacancies(data_from_hh: list) -> list:
        """Метод обработки полученной с API информации по вакансиям
        :param data_from_hh: полученная с сайта HeadHunter информация в виде списка
        :return list_vacancies: новый список в виде списка словарей: {'id_vacancy': id вакансии, 'town': город,
                                                                     'name': название вакансии,
                                                                     'url': ссылка, 'salary': зарплата,
                                                                    'schedule': график работы,
                                                                        'description': описание}"""
        list_vacancies = []
        for i in data_from_hh:
            if i["salary"]:
                if i["salary"]["from"] and i["salary"]["to"]:
                    salary = i["salary"]["to"]
                elif i["salary"]["from"] and not i["salary"]["to"]:
                    salary = i["salary"]["from"]
                elif i["salary"]["to"] and not i["salary"]["from"]:
                    salary = i["salary"]["to"]
                else:
                    salary = 0
            else:
                salary = 0
            vacancy_data = {
                "id_vacancy": int(i["id"]),
                "town": i["area"]["name"],
                "name": i["name"],
                "url": i["alternate_url"],
                "salary": salary,
                "schedule": i["schedule"]["name"],
                "description": i["snippet"]["responsibility"],
            }
            list_vacancies.append(vacancy_data)
        return list_vacancies


class SuperJobAPI(APIGetVacancies):
    """Класс для работы с API сайта SuperJob"""

    __HEADERS: Mapping = {
        "Host": "api.superjob.ru",
        "X-Api-App-Id": os.getenv("Secret_key_SuperJob"),
        "Authorization": f'Bearer {os.getenv("SuperJob_Token")}.token',
    }

    def __init__(self, key_word: str):
        """Создание экземпляра класса SuperJobAPI.
        :param key_word: ключевое слово для поиска вакансии"""
        self.key_word = key_word
        self.__page = 0
        self.params = {"keyword": key_word, "country": 1, "page": self.__page, "count": 100}

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.key_word})'

    def get_vacancies(self) -> list:
        """Метод получения вакансий по заданным параметрам"""
        list_data = []
        for i in range(0, PAGE_COUNT):
            req = requests.get("https://api.superjob.ru/2.0/vacancies/", params=self.params, headers=self.__HEADERS)
            data = req.content.decode()
            req.close()
            list_data.extend(json.loads(data)["objects"])
            self.__page += 1
        return self.make_list_vacancies(list_data)

    @staticmethod
    def make_list_vacancies(data_from_sj: list) -> list:
        """Метод обработки полученной с API информации по вакансиям
        :param data_from_sj: полученная с сайта HeadHunter информация в виде списка
        :return list_vacancies: новый список в виде списка словарей: {'id_vacancy': id вакансии, 'town': город,
                                                                     'name': название вакансии,
                                                                     'url': ссылка, 'salary': зарплата,
                                                                    'schedule': график работы,
                                                                        'description': описание}"""
        list_vacancies = []
        for i in data_from_sj:
            if i["payment_from"] != 0 and i["payment_to"] != 0:
                salary = i["payment_to"]
            elif i["payment_from"] == 0 and i["payment_to"] != 0:
                salary = i["payment_to"]
            elif i["payment_from"] != 0 and i["payment_to"] == 0:
                salary = i["payment_from"]
            else:
                salary = 0
            vacancy_data = {
                "id_vacancy": i["id"],
                "town": i["town"]['title'],
                "name": i["profession"],
                "url": i["link"],
                "salary": salary,
                "schedule": i["type_of_work"]["title"],
                "description": i["candidat"],
            }
            list_vacancies.append(vacancy_data)
        return list_vacancies
