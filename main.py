import requests
from bs4 import BeautifulSoup


class Avito_Parser():
    url = ''

    def __init__(self, search_parametrs=None, url='https://www.avito.ru/'):
        self.url = url
        self.session = requests.Session()
        self.session.headers = {
            'Accept-Language': 'ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.931 YaBrowser/23.9.3.931 Yowser/2.5 Safari/537.36'
        }
        try:
            if url == 'https://www.avito.ru/':
                self.url += search_parametrs['city'] + "?q=" + search_parametrs['product'] + "&s=" + self.viborka[
                    search_parametrs['criterion']]
                print("URL сформировавшейся страницы : ",self.url)
        except KeyError:
            print("Вы ввели неправильные параметры для запроса")

    def parsing(self):
        params = {
            'radius': 0,
            'user': 1
        }
        call = self.session.get(self.url, params=params)
        if call.status_code == 200:
            print("Запрос отправлен на сервер")
            soup = BeautifulSoup(call.content, "html.parser")
            title = soup.find_all("h3")
            price = soup.find_all("meta", itemprop="price")
            date = soup.find_all("p", class_="styles-module-root-_KFFt", attrs={"data-marker": "item-date"})
            links = soup.find_all("a", attrs={"itemprop": "url", "data-marker": "item-title"})
            if len(title) > 0:
                with open("data.txt", "w", encoding='utf-8') as file:
                    for i in range(len(price)):
                        file.write(title[i].text + "\t" + price[i]['content'] + "р\t\t" + date[i].text + "\t\t" + "https://www.avito.ru/" + links[i]['href'] + "\n")
                print("Объявления успешно спарсились в файл data.txt")
            else:
                print("Объявлений на странице не найдено")

        else:
            print("Запрос не удался, проверьте входные данные")

    viborka = {
        'По умолчанию': '',
        'Дешевле': '1',
        'Дороже': '2',
        'По дате': '104'
    }


def main():
    print("Привет, помогу тебе спарсить объявления с сайта авито:")
    choise = input('У тебя есть ссылка страницы, откуда хочешь спарсить объявления?(да/нет) ').lower()
    if choise == 'нет':
        conditions = {}
        conditions['city'] = input(
            "В каком городе хотите искать?(Напишите на английском. Например: по всей России - rossiya) ").lower()
        conditions['product'] = input("Что вы хотите найти? ").replace(" ","+")
        conditions['criterion'] = input(
            "По какому критерию вам вывести объявления?(По умолчанию, Дешевле, Дороже, По дате) ").capitalize()

        response = Avito_Parser(conditions)
        response.parsing()

    elif choise == 'да':
        url = input("Ввдеите ссылку: ")
        response = Avito_Parser(url=url)
        response.parsing()

    else:
        print("Такого варианта нет")


if __name__ == "__main__":
    main()
