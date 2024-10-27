from src.utils import PlatformsAPI
import requests


class HeadHunterAPI(PlatformsAPI):

    def get_vacancies(self, name_vacancy) -> list[dict]:
        """ Получение вакансии через API
        """
        url = "https://api.hh.ru/vacancies"
        params = {"text": f"{name_vacancy}", "page": 0, "per_page": 100, "only_with_salary": "true"}
        response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}).json()
        return response["items"]
