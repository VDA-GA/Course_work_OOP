from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List

from src.vacancies import Vacancy


class Saver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary: str) -> List:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONSaver(Saver):

    def __init__(self, filename: str) -> None:
        self.filename = Path(Path(Path.cwd()).parent, 'data', filename)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.filename})"

    def __call__(self, *args: list | dict) -> Any:
        if args:
            self.write_data_to_file(args[0])
            return self.get_data_from_file()
        else:
            return self.get_data_from_file()

    def get_data_from_file(self) -> Any:
        """Метод для получения данных из файла
        :return: возвращает список словарей с данными по вакансиям"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                list_vacancies = json.load(file)
            return list_vacancies
        except FileNotFoundError:
            print('Файл не найден')
            return []
        except json.JSONDecodeError:
            print("Неверные JSON данные")
            return []

    def write_data_to_file(self, data: dict | list) -> None:
        """Метод для записи данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод добавляющий вакансию в файл
        :param vacancy: экземпляр класса Vacancy"""

        new_vacancy_dict = dict(id_vacancy=vacancy.id_vacancy, town=vacancy.town, name=vacancy.name, url=vacancy.url,
                                salary=vacancy.salary, schedule=vacancy.schedule, description=vacancy.description)
        if os.path.exists(self.filename) and os.stat(self.filename).st_size != 0:
            list_vacancies = self()
            if isinstance(list_vacancies, dict):
                list_new_vac = [list_vacancies, new_vacancy_dict]
                self(list_new_vac)
            else:
                list_vacancies.append(new_vacancy_dict)
                self(list_vacancies)
        else:
            self(new_vacancy_dict)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Метод удаляющий вакансию из файла
                :param vacancy: экземпляр класса Vacancy"""

        list_vacancies = self()
        dict_vacancy = dict(id_vacancy=vacancy.id_vacancy, town=vacancy.town, name=vacancy.name, url=vacancy.url,
                            salary=vacancy.salary, schedule=vacancy.schedule, description=vacancy.description)
        if isinstance(list_vacancies, dict) and list_vacancies == dict_vacancy:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write('[]')
        elif isinstance(list_vacancies, dict) and list_vacancies != dict_vacancy:
            print('Указанная вакансия отсутствует')
        elif isinstance(list_vacancies, list):
            try:
                list_vacancies.remove(dict_vacancy)
            except ValueError:
                print('Указанная вакансия отсутствует')
            finally:
                self(list_vacancies)
        else:
            return

    def get_vacancies_by_salary(self, salary_period: str) -> List:
        """Метод осуществляющий фильтрацию данных по вакансиям из файла
                :param salary_period: диапазон значений зарплат"""
        if '-' in salary_period:
            salary_list: list = salary_period.split('-')
        else:
            print('Неверно указан диапазон зарплат')
        list_vacancies = self()
        new_list_vacancies = [i for i in list_vacancies if int(salary_list[0]) <= i['salary'] <= int(salary_list[1])]
        return new_list_vacancies
