from abc import ABC, abstractmethod
import json
import requests

### PART 1

class GetAPI(ABC):
    """Создаем абстрактный класс
    для работы с API сайтов с вакансиями"""

    @abstractmethod
    def __init__(self, web_url):
        self.web_url = web_url

    @abstractmethod
    def get_information_via_API(self, keyword):
        pass



class GetAPIhh(GetAPI):
    """Получаем вакансии из сайта HeadHunter, инициализируем по ссылке"""

    def __init__(self, web_url):
        super().__init__(web_url)

    def get_information_via_API(self, keyword):
        self.keyword = keyword
        #url = 'https://api.hh.ru/'
        endpoint = 'vacancies'
        params = {'text': {self.keyword}, 'per_page': 1}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        result = response.json()
        return result

d = GetAPIhh('https://api.hh.ru/') # check code
#print(d.get_information_via_API("разработчик")) # check code

s = d.get_information_via_API("программист")




class GetAPIsuperjob(GetAPI):
    """Получаем вакансии из сайта SuperJob, инициализируем по ссылке"""
    def __init__(self, web_url):
        super().__init__(web_url)

    def get_information_via_API(self, keyword):
        self.keyword = keyword
        #sj_url = "https://api.superjob.ru/2.0/vacancies/"
        superJob_API = "v3.r.137862906.018bdb5da03fa2b6be6c9543c3fcd4a21fce604c.6efbc6ead56ea0e4936505097cc50dbea2ce3457"

        headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": superJob_API,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        params = {'keyword': {self.keyword}, 'per_page': 1}
        response = requests.request("GET", self.web_url, headers=headers, params=params)
        result = response.json()
        return result


b = GetAPIsuperjob("https://api.superjob.ru/2.0/vacancies/") # check code
#print(b.get_information_via_API("разработчик")) # check code

k = b.get_information_via_API("разработчик")


#### PART 2


class Vacancy:

   def __init__(self, name, url, requirements, salary_from="не указано", salary_to="не указано", salary_currency="не указано"):
      self.name = name
      self.url = url
      self.salary_from = salary_from
      self.salary_to = salary_to
      self.salary_currency = salary_currency
      self.requirements = requirements

   def __str__(self):
      return f"""Вакансия {self.name} доступна по ссылке {self.url}.
Предлагаемая зарплата в размере от {self.salary_from} до {self.salary_to} в валюте {self.salary_currency}.
Требования: {self.requirements}"""


   # def __it__(self, other):
   #    """метод для операции сравнения меньше"""
   #    if (self.salary_currency == other.salary_currency and
   #            int(self.salary_from) > int(other.salary_from) or int(self.salary_to) > int(other.salary_to)):
   #       return f'Вакансия {other.name} имеет большую зарплату чем вакансия {self.name}.\n Вакансия {other.name} предлагает зарплату от {other.salary_from} до {other.salary_to} в валюте {other.salary_currency}'
   #

   def comparision(self, other):
      """метод для операции по зарплате"""
      if self.salary_currency != other.salary_currency:
         return f"Вакансии нельзя сравнить, разная валюта."
      elif self.salary_from == "не указано" or other.salary_from == "не указано":
         return f"Вакансии нельзя сравнить, зарплата не указана."
      elif self.salary_to == "не указано" or other.salary_to == "не указано":
         return f"Вакансии нельзя сравнить, зарплата не указана."


      if int(self.salary_from) > int(other.salary_from) or int(self.salary_to) > int(other.salary_to):
         return f'Вакансия {self.name} имеет большую зарплату чем вакансия {other.name}.\nВакансия {self.name} предлагает зарплату от {self.salary_from} до {self.salary_to} в валюте {self.salary_currency}'

      elif int(self.salary_from) < int(other.salary_from) or int(self.salary_to) < int(other.salary_to):
         return f'Вакансия {other.name} имеет зарплату больше чем вакансия {self.name}.\nВакансия {other.name} предлагает зарплату от {other.salary_from} до {other.salary_to} в валюте {other.salary_currency}'


# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "не указано", "15000", "RUB")
# vacancy1 = Vacancy("Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "70000", "80000", "RUB")
#
# b = vacancy.comparision(vacancy1) # for check
# print(b) # also for check
#

