from __future__ import annotations
from typing import List, Any


class Vacancy:
    """Класс для вакансий."""
    list_vacancies: List = []

    def __init__(self, id_vacancy: int, town: str, name: str, url: str, salary: int, schedule: str, description: str):
        """
                Создание экземпляра класса Vacancy.
                :param id_vacancy: id вакансии на сайте.
                :param town: Город вакансии.
                :param name: Наименование вакансии.
                :param url: Ссылка на вакансию.
                :param salary: Зарплата.
                :param schedule: График работы.
                :param description: Описание вакансии.
                """
        self.__id_vacancy = id_vacancy
        self.name = name
        self.town = town
        self.url = url
        self.__salary = salary
        self.schedule = schedule
        self.description = description
        self.list_vacancies.append(self)

    @property
    def id_vacancy(self):
        return self.__id_vacancy

    @id_vacancy.setter
    def id_vacancy(self, id):
        if isinstance(id, int):
            self.__id_vacancy = id
        elif isinstance(id, str) and id.isdigit():
            self.__id_vacancy = int(id)
        else:
            raise ValueError('Неверно указан id')

    @property
    def salary(self) -> int:
        return self.__salary

    @salary.setter
    def salary(self, salary: str | int) -> None:
        if isinstance(salary, str) and '-' in salary:
            list_salary = salary.split('-')
            self.__salary = int(list_salary[1])
        elif isinstance(salary, str) and '-' not in salary:
            self.__salary = int(salary)
        else:
            self.__salary = int(salary)



    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.id_vacancy}, '{self.name}', {self.town}, {self.url}, {self.__salary})"
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.__salary}"

    @classmethod
    def instantiate_data(cls, list_vacancies: list) -> None:
        """Классовый метод
                Инициализирует экземпляры класса `Vacancy` данными из списка словарей list_vacancies
                :param list_vacancies - списка словарей с данными вакансий
                """
        for vacancy in list_vacancies:
            id_vacancy = vacancy['id_vacancy']
            town = vacancy['town']
            name = vacancy['name']
            url = vacancy['url']
            salary = vacancy['salary']
            schedule = vacancy['schedule']
            if not vacancy['description']:
                description = '-'
            else:
                description = vacancy['description']
            cls(id_vacancy, town, name, url, salary, schedule, description)

    def __lt__(self, other: object) -> Any:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.__salary < other.__salary

    def __le__(self, other: object) -> Any:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.__salary <= other.__salary

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.__salary == other.__salary
