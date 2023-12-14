import pytest
from src.vacancy_save import JSONSaver
import json
import os
from pathlib import Path
from src.vacancies import Vacancy



@pytest.fixture
def js_1():
    return JSONSaver('test_json.json')


@pytest.fixture
def js_2():
    return JSONSaver('test_json_dict.json')

@pytest.fixture
def data():
    with open('test_vac.json', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    return list_vacancies


@pytest.fixture
def vacancy_1():
    return Vacancy(12345, 'Москва', 'Разработчик', 'www.sites.ru', 1000000, '25 часов в сутки', 'Прекрасная работа')


@pytest.fixture
def path_1():
    return Path(Path(Path.cwd()).parent, 'data', 'test_json.json')


@pytest.fixture
def path_2():
    return Path(Path(Path.cwd()).parent, 'data', 'test_json_dict.json')
def test_repr(js_1, path_1):
    assert repr(js_1) == f"JSONSaver({path_1})"


def test_call_1(js_1, data):
    res = js_1(data)
    assert len(res) == 10

def test_call_2(js_1, data, path_1):
    js_1(data)
    assert os.path.exists(path_1)


def test_get_data(js_1):
    res = js_1.get_data_from_file('ghvhgvhgv.json')
    assert res == []

def test_add_vacancy_1(js_1, vacancy_1, path_1):
    js_1.add_vacancy(vacancy_1)
    with open(path_1, 'r', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    assert len(list_vacancies) == 11

def test_delete_vacancy_1(js_1, vacancy_1, path_1):
    js_1.delete_vacancy(vacancy_1)
    with open(path_1, 'r', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    assert len(list_vacancies) == 10


def test_add_vacancy_2(js_2, vacancy_1, path_2):
    js_2.add_vacancy(vacancy_1)
    with open(path_2, 'r', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    assert len(list_vacancies) == 1

def test_delete_vacancy_2(js_2, vacancy_1, path_2):
    js_2.delete_vacancy(vacancy_1)
    with open(path_2, 'r', encoding='utf-8') as file:
        list_vacancies = file.read()
    assert list_vacancies == '[]'


def test_get_vacancies_by_salary_1(js_1):
    res = js_1.get_vacancies_by_salary('50000-500000')
    assert len(res) == 5

def test_get_vacancies_by_salary_2(js_1):
    res = js_1.get_vacancies_by_salary('50000')
    assert res is None

