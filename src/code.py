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
        params = {'text': {self.keyword}, 'per_page': 5}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        result = response.json()
        return result

d = GetAPIhh('https://api.hh.ru/') # check code
#print(d.get_information_via_API("разработчик")) # check code

s = d.get_information_via_API("повар")




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
      elif self.salary_from == "не указано" or other.salary_from == "не указано" or self.salary_from == 0 or other.salary_from == 0:
         return f"Вакансии нельзя сравнить, зарплата не указана."
      elif self.salary_to == "не указано" or other.salary_to == "не указано" or self.salary_to == 0 or other.salary_to == 0:
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


class Abstract_file_handler(ABC):
    """создаем абстрактный класс для добавления в файл, удаления и получения информации о вакансиях"""

    @abstractmethod
    def add_vacancy(self, name):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary_from):
        self.salary_from = salary_from

    @abstractmethod
    def delete_vacancy(self, name):
        pass


class Vacancy_to_JSON(Abstract_file_handler):

    def __init__(self, file_name): #я так предполагаю, что мы будем инициализироваться по будущему имени вк
        self.file_name = file_name


    def add_vacancy(self, name):
        self.name = name # тут мы записываем все вакансии в файл, а не по одной
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.name, file, ensure_ascii=False, indent=4)


    def delete_vacancy(self, name):

        """тут мы хотим удалить вакансию по её названию"""
        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file) # открываем файл

        new_vac_list = []
        for del_vacancy in data['items']:
            if del_vacancy['name'] == name:
                pass
            else:
                new_vac_list.append(del_vacancy)

        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump({"items": new_vac_list}, file, ensure_ascii=False, indent=4) # типо мы тут удаляем вакансию и перезаписываем файл


    def get_vacancies_by_salary(self, salary_from):
        #self.salary_from = salary_from
        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file) # открываем файл

        my_vac_list = []
        for v in data['items']:
            if v['salary']['from'] == int(salary_from):
                my_vac_list.append(v)

        with open(self.file_name, 'w', encoding='utf-8') as file:
            fin_vac = json.dump({"items": my_vac_list}, file, ensure_ascii=False, indent=4) #опять перезаписываем

            self.fin_vac = fin_vac



#check code

#from src.code import GetAPIhh, s

#vac = Vacancy_to_JSON('filename.json')
#vac.add_vacancy(s) # add vacancy thanks god works, and it looks beautiful, amazing!

#vac.delete_vacancy("Повар Универсал")
#vac.delete_vacancy("Шеф-повар") # It works! Amazing!

#vac.get_vacancies_by_salary(30000) # It works! Amazing!


