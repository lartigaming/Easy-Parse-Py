# Easy Parse

`easy_parse.py` — это удобный и простой в использовании модуль для парсинга веб-страниц на Python.

## Возможности

- **Легкий парсинг веб-страниц:** быстрое создание экземпляра `PageParser` для работы с любой веб-страницей.
- **Поиск элементов:** поиск как одного, так и всех элементов по тегу и классу.
- **Извлечение текста:** извлечение очищенного текста из элементов HTML.
- **Извлечение email-адресов:** автоматический поиск и извлечение всех email-адресов на странице.

## Использование

### Создание парсера и загрузка страницы

```python
from easy_parse import parse

url = "https://example.com"
page = parse(url)
```

### Поиск элементов

#### Первый элемент с заданным тегом и классом:

```python
from easy_parse import find_el

element = find_el(page, 'div', 'content')
```

#### Все элементы с заданным тегом и классом:

```python
from easy_parse import find_els

elements = find_els(page, 'p', 'description')
```

### Извлечение текста

```python
from easy_parse import extract_text

text = extract_text(element)
```

### Извлечение email-адресов

```python
emails = page.emails()
print(emails)
```

### Поиск элементов по часто используемым тегам

Для удобства, библиотека предоставляет динамически созданные функции для поиска элементов по часто используемым тегам, например:

```python
from easy_parse import find_h1, find_as, find_divs

header = find_h1(page)
links = find_as(page)
divs = find_divs(page, 'main-content')
```

## Установка

```bash
pip install -r requirements.txt
```

Затем файл easy_parse.py, помещаете в директорию вашего проекта.

## Лицензия

Этот проект распространяется под лицензией GNU General Public License v3.0.

© 2024 Larti
