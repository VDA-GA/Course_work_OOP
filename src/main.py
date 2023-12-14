from typing import Any

from src.API import HeadHunterAPI, SuperJobAPI
from src.utils import filter_vacancies_by_key_word
from src.vacancies import Vacancy
from src.vacancy_save import JSONSaver


def main() -> Any:
    """Основная функция программы"""

    print("Добрый день, Вам помочь найти работу?")
    while True:
        answer1 = input('да/нет? \n')
        if answer1.lower() not in ['да', 'нет']:
            print("Попробуйте ответить еще раз")
        elif answer1.lower() == "нет":
            return "До следующих встреч"
        elif answer1.lower() == "да":
            break

    key_word = input("Какая профессия Вас интересует?")
    print("""На каких сайтах будете искать вакансии? Введите номер варианта:
    1- HeadHunter
    2- SuperJob
    3- HeadHunter и SuperJob
          """)
    for i in range(1, 4):
        variant = input()
        if variant in ['1', '2', '3']:
            variant_int = int(variant)
            break
        else:
            print(f"Увы, такого варианта нет, попробуйте еще раз у Вас есть еще {3 - i} попыток")
    else:
        return
    if variant_int == 1:
        hh_api = HeadHunterAPI(key_word)
        list_vacancies = hh_api.get_vacancies()
    elif variant_int == 2:
        sj_api = SuperJobAPI(key_word)
        list_vacancies = sj_api.get_vacancies()
    else:
        hh_api = HeadHunterAPI(key_word)
        sj_api = SuperJobAPI(key_word)
        list_vacancies = hh_api.get_vacancies()
        list_vacancies.extend(sj_api.get_vacancies())

    json_saver_1 = JSONSaver('all_results.json')
    json_saver_1(list_vacancies)
    print(f'Найдено {len(list_vacancies)} вакансий. Они сохранены в файле all_results.json')
    print('Переходим к фильтрации вакансий')
    salary_range = input('Введите диапазон зарплат в формате №№№№-№№№№ \n')
    list_vacancies_by_salary = json_saver_1.get_vacancies_by_salary(salary_range)
    Vacancy.instantiate_data(list_vacancies_by_salary)
    print(f'В ходе фильтрации найдено {len(Vacancy.list_vacancies)} вакансий')
    json_saver_2 = JSONSaver('filtered_results.json')
    for vac in Vacancy.list_vacancies:
        json_saver_2.add_vacancy(vac)
    print('Данные записаны в новом файле filtered_results.json')
    town = input('Введите город, в котором должна быть вакансия \n')
    for vac in Vacancy.list_vacancies:
        if vac.town != town:
            json_saver_2.delete_vacancy(vac)
            Vacancy.list_vacancies.remove(vac)
    print('Данные в файле filtered_results.json отфильтрованы')
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    answer2 = input('Нужна ли фильтрация по ключевым словам? \n да/нет')
    if answer2.lower() == 'да':
        filter_words = input(
            "Введите ключевые слова в описании для фильтрации вакансий через пробел: \n").strip().split()
        new_list = filter_vacancies_by_key_word(filter_words, Vacancy.list_vacancies)
    else:
        new_list = Vacancy.list_vacancies
    sorted_new_list = sorted(new_list, reverse=True)
    if len(sorted_new_list) == 0:
        print('"Нет вакансий, соответствующих заданным критериям."')
    else:
        print(f'Топ вакансий: {sorted_new_list[0:top_n]}')
    return sorted_new_list


if __name__ == "__main__":
    main()
