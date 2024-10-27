import json
from config import PATH_FORMAT
from src.utils import WorkingWithFiles
import os


class JSONSaver(WorkingWithFiles):
    """ Класс для работы с JSON файлом
    """

    def add_vacancy(self, vacancy):
        """ Запись вакансии в файл
        """
        with open(PATH_FORMAT, "w", encoding="utf-8") as file:
            file.write(json.dumps(vacancy, indent=2, ensure_ascii=False))

    def get_vacancies_by_salary(self, unformatted_salary):
        """ Получение данных из файла по зарплате
        """
        with open(PATH_FORMAT, "r", encoding="utf-8") as file:
            data = json.load(file)
            filtered_data = []
            for vacancy in data:
                if vacancy['salary'] >= unformatted_salary:
                    filtered_data.append(vacancy)
            return filtered_data

    def delete_vacancy(self, vacancy):
        """ Удаление информации о вакансиях
        """
        # Проверяем, существует ли файл
        if os.path.exists(PATH_FORMAT):
            os.remove(PATH_FORMAT)  # Удаляем файл
            print(f"Файл '{PATH_FORMAT}' успешно удален.")
