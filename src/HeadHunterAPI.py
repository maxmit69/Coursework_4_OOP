from string import ascii_letters
from src.utils import PlatformsAPI
import requests


class HeadHunterAPI(PlatformsAPI):
    """ Класс для работы с API hh.ru
    """
    S_RUS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()

    @classmethod
    def verify_name(cls, name_vacancy):
        """ Проверка на корректность названия вакансии
        """
        letters = cls.S_RUS + cls.S_RUS_UPPER + ascii_letters
        for name in name_vacancy:
            if len(name) < 1:
                raise TypeError("Название вакансии не может быть пустой строкой")
            if len(name.strip(letters)) != 0:
                raise TypeError("Название вакансии должно содержать только буквенные символы и дефис")

    def get_vacancies(self, vacancies) -> list[dict]:
        """ Получение вакансии через API
        """
        self.verify_name(vacancies)
        url = "https://api.hh.ru/vacancies"
        params = {"text": f"{vacancies}", "page": 0, "per_page": 100, "only_with_salary": "true"}

        try:
            response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            vacancies_data = response.json()

            if "items" not in vacancies_data or not vacancies_data["items"]:
                raise ValueError("Вакансии по запросу не найдены")

            return vacancies_data["items"]

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при запросе вакансий: {e}")
            return []
