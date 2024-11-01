from src.HeadHunterAPI import HeadHunterAPI
from src.JSONSaver import JSONSaver
from src.utils import Vacancy, get_yes_no_input, get_salary_input


def user_interaction():
    """ Функция для взаимодействия с пользователем
    """
    while True:
        user_input = input("Введите поисковый запрос: ")
        # Создание экземпляра класса для работы с API сайтов с вакансиями
        hh_api = HeadHunterAPI()

        # Получение вакансий с hh.ru в формате JSON
        hh_vacancies = hh_api.get_vacancies(user_input)

        # Форматирование списка вакансий с необходимыми параметрами
        vacancies_list = Vacancy.get_format_vacancy_hh(hh_vacancies)

        # Преобразование списка в словарь с необходимыми ключами
        vacancies_dict = Vacancy.convert_dict_vacancy(vacancies_list)

        # Сортировка вакансий по рублю
        hh_vacancies_sorted = Vacancy.sorting_salary(vacancies_dict)

        # Инициализация вакансий
        Vacancy.cast_to_object_list(hh_vacancies_sorted)

        # Сохранение информации о вакансиях в файл
        json_saver = JSONSaver()
        json_saver.add_vacancy(vacancy=hh_vacancies_sorted)

        count_vacancies = int(input("Введите количество вакансий для вывода в топ N: по зарплате: "))

        # Сортировка вакансий по зарплате в рублях
        hh_vacancies_sorted = sorted(hh_vacancies_sorted, key=lambda x: x['salary'], reverse=True)
        for item in hh_vacancies_sorted[:count_vacancies]:
            print(Vacancy.cast_to_object_list([item]))

        # Поиск вакансий по критериям
        while True:
            try:
                search_vacancy = get_yes_no_input("Поиск вакансий по зарплате? (да/нет): ")

                if search_vacancy == "да":
                    salary = get_salary_input("Введите зарплату: ")
                    vacancies_criteria = json_saver.get_vacancies_by_salary(unformatted_salary=salary)
                    for item in vacancies_criteria:
                        print(Vacancy.cast_to_object_list([item]))

                # Удаление информации о вакансиях
                delete_vacancy = get_yes_no_input("Удалить информацию о вакансиях? (да/нет): ")
                if delete_vacancy == "да":
                    json_saver.delete_vacancy(vacancy=hh_vacancies_sorted)

                # Повторить поиск
                user_input = get_yes_no_input("Продолжить поиск? (да/нет): ")
                if user_input == "да":
                    break  # Завершает внутренний цикл для повторного поиска
                else:
                    print("Завершение поиска. Спасибо за использование!")
                    exit()

            except Exception as e:
                print(f"Произошла ошибка: {e}")


def main():
    """ Главная функция
    """
    user_interaction()


if __name__ == "__main__":
    main()
