import json

import pytest

from src.utils import filter_vacancies_by_key_word
from src.vacancies import Vacancy


@pytest.fixture
def list_vac():
    with open('test_vac.json', encoding='utf-8') as file:
        list_vacancies = json.load(file)
    Vacancy.instantiate_data(list_vacancies)
    return Vacancy.list_vacancies


def test_filter_vacancies_by_key_word(list_vac):
    new_list = filter_vacancies_by_key_word(['Flask', 'API'], list_vac)
    assert len(new_list) == 1
