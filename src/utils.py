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


class Vacancy:
    """ Клас для работы с вакансиями
    """

    def __init__(self, name_vacancy=None, url=None, salary=None, requirements=None) -> None:
        self.verify_name(name_vacancy)
        self.verify_url(url)
        self.verify_salary(salary)
        self.verify_requirements(requirements)

        self.__name_vacancy = name_vacancy
        self.__url = url
        self.__salary = salary
        self.__requirements = requirements

    def __str__(self):
        return f'{self.__name_vacancy}, {self.__url}, {self.__salary} руб, {self.__requirements}'

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__name_vacancy}, {self.__url}, {self.__salary}, {self.__requirements}'

    def __lt__(self, other):
        """ Меньше или равно
        """
        return self.__salary < other.salary

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

    @classmethod
    def verify_name(cls, name_vacancy: str) -> None:
        if not isinstance(name_vacancy, str):
            raise TypeError(f'Значение должно быть {str}')

    @classmethod
    def verify_url(cls, url: str) -> None:
        if not isinstance(url, str):
            raise TypeError(f'Значение должно быть {str}')

    @classmethod
    def verify_salary(cls, salary: int) -> None:
        if not isinstance(salary, int):
            raise TypeError(f'Значение должно быть {int}')
        if salary == 0:
            print('Зарплата не указана')

    @classmethod
    def verify_requirements(cls, requirements: str) -> None:
        if not isinstance(requirements, str):
            raise TypeError(f'Значение должно быть {str}')

    @property
    def name(self) -> str:
        return self.__name_vacancy

    @name.setter
    def name(self, name_vacancy: str) -> None:
        self.verify_name(name_vacancy)
        self.__name_vacancy = name_vacancy

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url) -> None:
        self.verify_url(url)
        self.__url = url

    @property
    def salary(self) -> int:
        return self.__salary

    @salary.setter
    def salary(self, salary: int) -> None:
        self.verify_salary(salary)
        self.__salary = salary

    @property
    def requirements(self) -> str:
        return self.__requirements

    @requirements.setter
    def requirements(self, requirements: str) -> None:
        self.verify_requirements(requirements)
        self.__requirements = requirements
