import requests
from bs4 import BeautifulSoup, Comment
from colorama import Fore, Style, init
import re

init(autoreset=True)  # Инициализация colorama для вывода цветных сообщений об ошибках

class PageParser:
    """
    Класс для парсинга веб-страниц. Позволяет легко искать элементы и извлекать данные.
    """

    def __init__(self, url):
        """
        Инициализирует PageParser с указанным URL.

        :param url: Строка, содержащая URL веб-страницы для парсинга.
        :raises: requests.exceptions.RequestException в случае ошибки загрузки страницы.
        """
        try:
            response = requests.get(url)
            response.raise_for_status() 
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"{Fore.RED}Ошибка при загрузке страницы: {e}{Style.RESET_ALL}")
            self.soup = None

    def find_el(self, tag, class_name=None):
        """
        Ищет первый элемент с заданным тегом и классом на странице.

        :param tag: Строка с именем HTML тега.
        :param class_name: Строка с именем класса для более точного поиска. Необязательный параметр.
        :return: BeautifulSoup Tag объект или None, если элемент не найден.
        """
        if not self.soup:
            return None
        return self.soup.find(tag, class_=class_name) if class_name else self.soup.find(tag)

    def find_els(self, tag, class_name=None):
        """
        Ищет все элементы с заданным тегом и классом.

        :param tag: Строка с именем HTML тега.
        :param class_name: Строка с именем класса. Необязательный параметр.
        :return: Список BeautifulSoup Tag объектов или пустой список.
        """
        if not self.soup:
            return []
        return self.soup.find_all(tag, class_=class_name) if class_name else self.soup.find_all(tag)

    def emails(self):
        """
        Извлекает все найденные email-адреса на веб-странице.

        :return: Set уникальных email-адресов, найденных на странице.
        """
        if not self.soup:
            return set()
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        texts = self.soup.find_all(text=True)
        visible_texts = filter(self._visible, texts)
        return set(re.findall(email_regex, ' '.join(visible_texts)))
    
    @staticmethod
    def _visible(element):
        """
        Определяет, является ли элемент видимым на странице.

        :param element: Элемент BeautifulSoup для проверки.
        :return: Булево значение, True если элемент видим, иначе False.
        """
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    @staticmethod
    def extract_text(element):
        """
        Извлекает очищенный текст из переданного элемента.

        :param element: Элемент BeautifulSoup.
        :return: Строка текста элемента или пустая строка, если элемент None или не содержит текста.
        """
        return element.get_text(strip=True) if element else ""

# Обертки для удобства
def parse(url):
    """
    Создает экземпляр PageParser для указанного URL.

    :param url: URL веб-страницы для парсинга.
    :return: Экземпляр PageParser.
    """
    return PageParser(url)

def find_el(page, tag_name, class_name=None):
    """
    Удобный интерфейс для поиска первого элемента по тегу и классу через PageParser.

    :param page: Экземпляр PageParser.
    :param tag_name: Имя тега.
    :param class_name: Имя класса. Необязательно.
    :return: Tag или None.
    """
    return page.find_el(tag_name, class_name)

def find_els(page, tag_name, class_name=None):
    """
    Удобный интерфейс для поиска всех элементов по тегу и классу.

    :param page: Экземпляр PageParser.
    :param tag_name: Имя тега.
    :param class_name: Имя класса. Необязательно.
    :return: Список Tag объектов.
    """
    return page.find_els(tag_name, class_name)

def extract_text(element):
    """
    Обертка для извлечения текста из элемента.

    :param element: Элемент BeautifulSoup.
    :return: Строка с текстом.
    """
    return PageParser.extract_text(element)

# Создание динамических функций для часто используемых тегов
for tag in ['h1', 'a', 'div', 'span', 'p', 'ul', 'li', 'table', 'tr', 'td']:
    exec(f"""
def find_{tag}(page, class_name=None):
    return find_el(page, '{tag}', class_name)

def find_{tag}s(page, class_name=None):
    return find_els(page, '{tag}', class_name)
""")