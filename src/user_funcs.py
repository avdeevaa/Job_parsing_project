from src.code import GetAPIhh, GetAPIsuperjob, Vacancy, Vacancy_to_JSON
import json


def open_json(file_name):
    """Функция помощник для открытия файла json"""
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def user_interaction():
    print("Привет! Сегодня будем искать подходящие вакансии. У нас есть две платформы: HeadHunter и SuperJob. \nНа какой платформе ты хочешь искать?")
    platform = input().lower()

    if platform == "HeadHunter".lower():
        print("Отлично, будем искать на HeadHunter!")
        platform_url = 'https://api.hh.ru/'
        chosen_platform = GetAPIhh(platform_url)
        keyword_input = input("Введите ключевое слово, по которому будем искать подходящие вакансии: ")
        api = chosen_platform.get_information_via_API(keyword_input)  # here we first found API file!
        to_json = Vacancy_to_JSON("filename.json")
        all_vac = to_json.add_vacancy(api)  # finally we write all Vac to JSON

        data = open_json("filename.json")
        print("Вот вакансии подходящие для вас: \n")
        for vacancy in data['items']:
            name = vacancy['name']
            city = vacancy['area']['name']
            try:
                salary_from = vacancy['salary']['from']

                if salary_from is None:
                    salary_from = "не указано"
            except TypeError:
                continue

            try:
                salary_to = vacancy['salary']['to']
                if salary_to is None:
                    salary_to = "не указано"
            except TypeError:
                continue
            try:
                currency = vacancy['salary']['currency']
                if currency is None:
                    currency = "не указано"
            except TypeError:
                continue
            url = vacancy['url']
            responsibilities = vacancy['snippet']['responsibility']

            print(f"Название: {name}\nГород: {city}\nЗарплата от: {salary_from} до {salary_to} в валюте {currency}.")
            print(f"Ссылка: {url}\nОбязанности: {responsibilities}\n")

        print("Хотите сравнить вакансии? (да/нет) (yes/no)")
        yes_no = input().lower()
        if yes_no == "yes" or yes_no == "да":
            print("Отлично, будем сравнивать!")
            vacancy1 = input("Введите название первой вакансии: ")
            vacancy2 = input("Введите название второй вакансии: ")

            vacancy_found = False
            for vacancy in data['items']:
                if vacancy1 == vacancy['name']:
                    class_vacancy1 = Vacancy(vacancy1, vacancy['url'], vacancy['snippet']['responsibility'],
                                             vacancy['salary']['from'], vacancy['salary']['to'],
                                             vacancy['salary']['currency'])
                    vacancy_found = True
                elif vacancy2 == vacancy['name']:
                    class_vacancy2 = Vacancy(vacancy2, vacancy['url'], vacancy['snippet']['responsibility'],
                                             vacancy['salary']['from'], vacancy['salary']['to'],
                                             vacancy['salary']['currency'])
                    vacancy_found = True

            if not vacancy_found:
                print("Нет таких вакансий. Спасибо за интеракцию!")

            else:
                fin = class_vacancy1.comparision(class_vacancy2)
                print(fin)

        elif yes_no == "no" or yes_no == "нет":
            print("Сравнивать не будем, спасибо за интеракцию!")
        else:
            print("Ой, вы ввели что-то не то. Спасибо за интеракцию!")
            pass



    elif platform == "SuperJob".lower():
        print("Отлично, будем искать на SuperJob!")
        platform_url_sj = 'https://api.superjob.ru/2.0/vacancies/'
        chosen_platform = GetAPIsuperjob(platform_url_sj)

        keyword_input = input("Введите ключевое слово, по которому будем искать подходящие вакансии: ")
        api = chosen_platform.get_information_via_API(keyword_input)  # here we first found API file!
        to_json = Vacancy_to_JSON("filename2.json")
        all_vac = to_json.add_vacancy(api)  # finally we write all Vac to JSON

        data = open_json("filename2.json")
        print("Вот вакансии подходящие для вас: \n")

        for vacancy in data['objects']:
            name = vacancy['profession']
            city = vacancy['address']
            salary_from = vacancy['payment_from']

            if salary_from is None or salary_from == 0:
                salary_from = "не указано"
            salary_to = vacancy['payment_to']
            if salary_to is None or salary_to == 0:
                salary_to = "не указано"
            currency = vacancy['currency']
            if currency is None or currency == 0:
                currency = "не указано"
            url = vacancy['link']
            responsibilities = vacancy['candidat']

            print(f"Название: {name}\nГород: {city}\nЗарплата от: {salary_from} до {salary_to} в валюте {currency}.")
            print(f"Ссылка: {url}\n{responsibilities}\n")

        print("Хотите сравнить вакансии? (да/нет) (yes/no)")
        yes_no = input().lower()
        if yes_no == "yes" or yes_no == "да":
            print("Отлично, будем сравнивать!")
            vacancy1 = input("Введите название первой вакансии: ")
            vacancy2 = input("Введите название второй вакансии: ")


            vacancy_found = False
            for vacancy in data['objects']:
                if vacancy1 == vacancy['profession']:
                    class_vacancy1 = Vacancy(vacancy1, vacancy['link'], vacancy['candidat'],
                                             vacancy['payment_from'], vacancy['payment_to'],
                                             vacancy['currency'])
                    vacancy_found = True
                elif vacancy2 == vacancy['profession']:
                    class_vacancy2 = Vacancy(vacancy1, vacancy['link'], vacancy['candidat'],
                                             vacancy['payment_from'], vacancy['payment_to'],
                                             vacancy['currency'])
                    vacancy_found = True

            if not vacancy_found:
                print("Нет таких вакансий. Спасибо за интеракцию!")

            else:
                fin2 = class_vacancy1.comparision(class_vacancy2)
                print(fin2)

        elif yes_no == "no" or yes_no == "нет":
            print("Сравнивать не будем, спасибо за интеракцию!")
        else:
            print("Ой, вы ввели что-то не то. Спасибо за интеракцию!")
            pass


    else:
        print("Нет такой платформы. Кажется, вы не хотите искать вакансии")


user_interaction()

#headhunter
#superjob
#повар