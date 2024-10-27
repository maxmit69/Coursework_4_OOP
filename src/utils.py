from abc import ABC, abstractmethod
import re


class PlatformsAPI(ABC):
    """ Абстрактный класс
    """

    @abstractmethod
    def get_vacancies(self, vacancy):
        """ Получение вакансии через API
        """
        pass


class WorkingWithFiles(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        """ Добавление вакансии в файл
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, unformatted_vacancy):
        """ Получение данных из файла по указанным критериям
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """ Удаление информации о вакансиях
        """
        pass


class Descriptors:
    """ Класс для работы с дескрипторами
    """
    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value




class Vacancy:
    """ Клас для работы с вакансиями
    """

    name_vacancy = Descriptors()
    url = Descriptors()
    salary = Descriptors()
    requirements = Descriptors()

    def __init__(self, name_vacancy=None, url=None, salary=None, requirements=None):
        self.name_vacancy = name_vacancy
        self.url = url
        self.salary = salary
        self.requirements = requirements

    def __str__(self):
        return f'{self.name_vacancy}, {self.url}, {self.salary} руб, {self.requirements}'

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name_vacancy}, {self.url}, {self.salary}, {self.requirements}'

    def __lt__(self, other):
        """ Меньше или равно
        """
        return self.salary < other.salary

    @classmethod
    def cast_to_object_list(cls, vacancy_data):
        """ Преобразование списка словарей в список объектов
        """
        for item in vacancy_data:
            name_vacancy = item["name_vacancy"]
            url = item["url"]
            salary = item["salary"]
            requirements = item["requirements"]
            return cls(name_vacancy, url, salary, requirements)

    @classmethod
    def get_format_vacancy_hh(cls, vacancy_data: list[dict]) -> list:
        """ Возвращает список вакансий с нужными параметрами
        """
        list_vacancies_hh = []
        for item in vacancy_data:
            list_vacancies_hh.append(item["name"])
            list_vacancies_hh.append(item["alternate_url"])
            if item["salary"] and item["salary"]["from"]:
                list_vacancies_hh.append(f"От {item['salary']['from']} {item['salary']['currency']}")
            elif item["salary"] and item["salary"]["to"]:
                list_vacancies_hh.append(f"До {item['salary']['to']} {item['salary']['currency']}")
            else:
                list_vacancies_hh.append("Зарплата не указана")
            list_vacancies_hh.append(item["experience"]["name"])
        return list_vacancies_hh

    @classmethod
    def convert_dict_vacancy(cls, list_name: list) -> list[dict]:
        """ Преобразует список в список словарей с заданными ключами
        """
        lest_vacancies = ['name_vacancy', 'url', 'salary', 'requirements']
        res = []
        for item in range(0, len(list_name), 4):
            res_dict = dict(zip(lest_vacancies, list_name[item:item + 4]))
            res.append(res_dict)
        return res

    @classmethod
    def sorting_salary(cls, list_convert: list[dict]) -> list[dict]:
        """ Сортирует зарплату по рублю
        """
        new_list = []
        for item in list_convert:
            if item['salary'][-3:] == 'RUR'[-3:] or item['salary'][-3:] == 'rub'[-3:]:
                item['salary'] = int(re.sub(r'\D', '', item['salary']))
                new_list.append(item)
        return new_list

def get_yes_no_input(prompt):
    """Функция для запроса ответа 'да' или 'нет'."""
    while True:
        response = input(prompt).strip().lower()
        if response in ("да", "нет"):
            return response
        print("Некорректное значение. Введите 'да' или 'нет'.")

def get_salary_input(prompt):
    """Функция для запроса ввода зарплаты в виде целого числа."""
    while True:
        try:
            salary = int(input(prompt))
            return salary
        except ValueError:
            print("Некорректное значение. Введите целое число для зарплаты.")
