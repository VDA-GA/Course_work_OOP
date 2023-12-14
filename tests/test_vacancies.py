from src.vacancies import Vacancy
import pytest
import json


@pytest.fixture
def data():
    with open('test_vac.json', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    return list_vacancies


def test_instantiate_data(data):
    Vacancy.instantiate_data(data)
    assert len(Vacancy.list_vacancies) == 20


@pytest.fixture()
def vacancy_1():
    return Vacancy(12345, 'Москва', 'Разработчик', 'www.sites.ru', 1000000, '25 часов в сутки', 'Прекрасная работа')


@pytest.fixture()
def vacancy_2():
    return Vacancy(12456, 'Москва', 'Разработчик', 'www.sites.ru', 1000, '30 часов в сутки', 'Работа')


@pytest.fixture()
def vacancy_3():
    return Vacancy(1, 'Санкт-Петербург', 'Дворник', 'www.spb-work.ru', 1000000, 'удаленная работа', 'Уборка во дворе')


def test_compare_vac_1(vacancy_1, vacancy_2):
    assert vacancy_2 < vacancy_1


def test_compare_vac_2(vacancy_1, vacancy_3):
    assert vacancy_1 == vacancy_3


def test_compare_vac_3(vacancy_1):
    with pytest.raises(TypeError):
        vacancy_1 > 100000


def test_repr(vacancy_1):
    assert repr(vacancy_1) == "Vacancy(12345, 'Разработчик', Москва, www.sites.ru, 1000000)"


def test_str(vacancy_1):
    assert str(vacancy_1) == 'Разработчик, 1000000'


def test_salary(vacancy_1):
    vacancy_1.salary = '1000-2000'
    assert vacancy_1.salary == 2000


def test_id_1(vacancy_1):
    vacancy_1.id_vacancy = '1223'
    assert vacancy_1.id_vacancy == 1223


def test_id_2(vacancy_1):
    vacancy_1.id_vacancy = 1223
    assert vacancy_1.id_vacancy == 1223


def test_id_3(vacancy_1):
    with pytest.raises(ValueError):
        vacancy_1.id_vacancy = 'НЕТ ДАННЫХ'
