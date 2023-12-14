from src.API import HeadHunterAPI, SuperJobAPI
from src.vacancies import Vacancy
from src.vacancy_save import JSONSaver
from typing import List
from pprint import pprint

def filter_vacancies_by_key_word(key_words: list, list_vacancies: List) -> List:
    for word in key_words:
        list_vacancies = [i for i in list_vacancies if word in i.description]
    return list_vacancies
