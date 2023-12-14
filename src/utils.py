from typing import List


def filter_vacancies_by_key_word(key_words: list, list_vacancies: List) -> List:
    """Функция для фильтрации списка экзепляров класса Vacancy по списку ключевых слов
    :param key_words: Список ключевых слов
    :param list_vacancies: исходный список экземпляров класса Vacancy
    :return: отфильтрованный список экземпляров класса Vacancy"""

    for word in key_words:
        list_vacancies = [i for i in list_vacancies if word in i.description]
    return list_vacancies
