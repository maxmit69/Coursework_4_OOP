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
