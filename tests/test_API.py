import json

import pytest

from src.API import HeadHunterAPI, SuperJobAPI


@pytest.fixture
def hh():
    return HeadHunterAPI('Python')


@pytest.fixture
def sj():
    return SuperJobAPI('Python')


@pytest.fixture
def hh_data():
    with open('test_1.json', encoding='utf-8') as file:
        data = json.load(file)
    return data


@pytest.fixture
def sj_data():
    with open('test_2.json', encoding='utf-8') as file:
        data = json.load(file)
    return data


def test_repr_hh(hh):
    assert repr(hh) == "HeadHunterAPI(Python)"


def test_repr_sj(sj):
    assert repr(sj) == "SuperJobAPI(Python)"


def test_api_date_sj(sj):
    with pytest.raises(AttributeError):
        print(sj.HEADERS)


def test_make_list_vacancies_hh_1(hh, hh_data):
    assert hh.make_list_vacancies(hh_data)[0]["salary"] == 50000


def test_make_list_vacancies_hh_2(hh, hh_data):
    assert len(hh.make_list_vacancies(hh_data)) == 5


def test_make_list_vacancies_sj_1(sj, sj_data):
    assert sj.make_list_vacancies(sj_data)[0]['id_vacancy'] == 46759846


def test_make_list_vacancies_sj_2(sj, sj_data):
    assert len(sj.make_list_vacancies(sj_data)) == 5
