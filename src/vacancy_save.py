from __future__ import annotations
from typing import Any, List
import json
from abc import ABC, abstractmethod
from pathlib import Path
from src.vacancies import Vacancy
import os


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

    def __init__(self, filename):
        self.filename = Path(Path(Path.cwd()).parent, 'data', filename)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.filename})"

    def __call__(self, *args, **kwargs):
        if args:
            self.write_data_to_file(args[0])
            return self.get_data_from_file(self.filename)
        else:
            return self.get_data_from_file(self.filename)

    @staticmethod
    def get_data_from_file(filename: Path) -> Any:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                list_vacancies = json.load(file)
            return list_vacancies
        except FileNotFoundError:
            print('Файл не найден')
            return []
        except json.JSONDecodeError:
            print("Неверные JSON данные")
            return []

    def write_data_to_file(self, data: dict | list) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy) -> None:
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
        list_vacancies = self.get_data_from_file(self.filename)
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
                self.write_data_to_file(list_vacancies)
        else:
            return

    def get_vacancies_by_salary(self, salary_period: str) -> List | None:
        if '-' in salary_period:
            salary_list = salary_period.split('-')
        else:
            print('Неверно указан диапазон зарплат')
            return
        list_vacancies = self.get_data_from_file(self.filename)
        new_list_vacancies = [i for i in list_vacancies if int(salary_list[0]) <= i['salary'] <= int(salary_list[1])]
        return new_list_vacancies
