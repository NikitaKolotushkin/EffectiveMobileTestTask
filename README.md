# Описание функционала

## Основные классы:

```python
# Класс 'Книга'
class Book(object): ...

# Класс 'Библиотека'
class Library(object): ...
```

## Класс Book:

```python
def __init__(self, title: str, author: str, year: int) -> None:
    self.id = 0
    self.title = title
    self.author = author
    self.year = year
    self.status = 'В наличии'
```

Конструктор класса. <br />
Принимает следующие аргументы:
* `title` – Название книги
* `author` – Автор книги
* `year` – Год издания

Помимо этого, он автоматически инициализирует следующие поля: <br/>

* `id` – идентификатор книги в таблице библиотеки
* `status` – статус наличия книги в библиотеке: 'В наличии' | 'Выдана'

#

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Book):
        return False
    return (self.title == other.title) and (self.author == other.author) and (self.year == other.year)
```
**Магический метод** `__eq__`. <br />
Принимает следующие аргументы:
* `other` – Объект сравниваемого класса.

Позволяет сравнивать с помощью операции `==` два объекта класса Book. <br />
Будет использоваться далее для исключения добавления в библиотеку книги, которая уже существует.

#

```python
def __str__(self) -> str:
    return f'{self.id}: {self.title} ({self.author}, {self.year}) - {self.status}'
```
**Магический метод** `__str__`. <br />
Предоставляет красивый, читабельный текстовый образ объекта класса Book. <br />
**Пример:** `1: Мастер и Маргарита (Булгаков М. А., 1967) – В наличии`

## Класс Library:

```python
def __init__(self, filename: str = 'library.json') -> None:
    self.filename = filename
    try:
        self._open_file()
    except FileNotFoundError:
        self._save_file({'books': []})
```
Конструктор класса. <br />
Принимает следующие аргументы:
* `filename` – название файла библиотеки в формате .json [Опционально].

В конструкторе класса осуществляется проверка на существование JSON файла библиотеки с помощью конструкции `try/except`. <br />
Если файла с заданным именем не существует, создаётся новый файл со следующим наполнением:
```json
{
    "books": [

    ]
}
```

#

```python
def add_book(self, book: Book) -> None:
    data = self._open_file()
    
    if any(book == Book(b['title'], b['author'], b['year']) for b in data['books']):
        print('Ошибка: Книга уже есть в библиотеке!')
        return

    book.id = data['books'][-1]['id'] + 1 if data['books'] else 1
    
    data['books'].append(book.__dict__)
    
    self._save_file(data)
```
Метод добавления книги в библиотеку. <br />
Принимает следующие аргументы:
* `book` – Экземпляр класса `Book`.

Для начала осуществляется проверка на наличие добавляемой книги в библиотеке за счёт прохода по JSON файлу. <br />
При попытке добавления существующей книги пользователь видит ошибку. <br />
В случае отсутствия книги в библиотеке книге присваивается `id`, равный `id` последней книги в библиотеке `+ 1`. <br />
После этого в JSON файл заносятся данные о новой книге.

#

```python
def remove_book(self, book_id: int) -> None:
    data = self._open_file()

    book = next((book for book in data['books'] if book['id'] == book_id), None)

    if book is None:
        print(f'Ошибка: Книги с id = {book_id} не существует!')
        return

    data['books'] = [book for book in data['books'] if book['id'] != book_id]

    self._save_file(data)
```
Метод удаления книги из библиотеки. <br />
Принимает следующие аргументы:
* `book_id` – id книги, которую надо удалить.

Для начала осуществляется проверка на наличие удаляемой книги в библиотеке с помощью функции `next` <br />
При попытке удаления несуществующей книги пользователь видит ошибку. <br />
В противном случае формируется список книг, **не** содержащий заданную книгу, и добавляется в JSON файл.

#

```python
def find_book(self, search_mode: int, search_query: str) -> None:
    data = self._open_file()

    search_modes = ['title', 'author', 'year']

    if search_mode not in range(1, len(search_modes) + 1):
        print('Ошибка: Неверный режим поиска!')
        return

    matching_books = [book for book in data['books'] if str(book[search_modes[search_mode - 1]]) == search_query]

    if not matching_books:
        print('Книги не найдены!')
        return

    self.show_books(matching_books)
```
Метод поиска книги в библиотеке. <br />
Принимает следующие аргументы:
* `search_mode` – режим поиска.
* `search_query` – поисковой запрос.

`search_modes` – список режимов поиска: по названию, автору и году соответственно. <br />

Далее производится проверка: если режим поиска находится не относится к [1; 3], то пользователь получает ошибку. <br />
После этого формируется список подходящих книг. Если список пуст, пользователь получает соответствующее сообщение. <br />
Если же получившийся список не является пустым, выводится список найденных книг.

#

```python
def show_books(self, book_list: list = None) -> None:
    data = self._open_file()['books'] if book_list is None else book_list

    if not data:
        print('Книги не найдены!')
        return

    lengths = {
        'id_w': max(len('ID'), max(len(str(book['id'])) for book in data)),
        'title_w': max(len('Название'), max(len(book['title']) for book in data)),
        'author_w': max(len('Автор'), max(len(book['author']) for book in data)),
        'year_w': max(len('Год'), max(len(str(book['year'])) for book in data)),
        'status_w': max(len('Статус'), max(len(book['status']) for book in data))
    }

    self.print_header(**lengths)

    for book in data:
        print(f'| {book["id"]:<{lengths["id_w"]}} | {book["title"]:<{lengths["title_w"]}} | {book["author"]:<{lengths["author_w"]}} | {book["year"]:<{lengths["year_w"]}} | {book["status"]:<{lengths["status_w"]}} |')
        self.print_separator(**lengths)
```
Метод вывода книг на экран. <br />
Принимает следующие аргументы:
* `book_list` – список книг для вывода на экран [Опционально].

Если `book_list` равен `None`, выводятся все книги в библиотеке. <br />
В случае, если книги в библиотеке отсутствуют, пользователь видит соответствующее сообщение. <br />

Далее формируется словарь `lengths`, содержащий в себе размеры ячеек выводимой таблицы. <br />
Длина ячейки таблицы равна максимальному значению из длины надписи в шапке таблицы и максимальной длины соответствующего поля в списке книг.<br />
После этого вызывается метод `print_header`, печатающий шапку таблицы, а также печатаются книги с соответствующим форматированием.<br />

### Пример: 
| ID | Название | Автор | Год | Статус |
|----|----------|-------|-----|--------|
| 1 | Белая гвардия | Булгаков М. А. | 1925 | В наличии |
| 2 | Мастер и Маргарита| Булгаков М. А. | 1967 | В наличии |
| 3 | Судьба человека | Шолохов М. А. | 1957 | Выдана |
| 4 | Тихий Дон | Шолохов М. А. | 1928 | В наличии|

#

```python
def change_book_status(self, book_id: int) -> None:
    data = self._open_file()
    
    book = next((book for book in data['books'] if book['id'] == book_id), None)

    if book is None:
        print(f'Ошибка: Книги с id = {book_id} не существует!')
        return

    statuses = ['В наличии', 'Выдана']
    book['status'] = statuses[(statuses.index(book['status']) + 1) % 2]

    self._save_file(data)
```
Метод изменения статуса книги. <br />
Принимает следующие аргументы:
* `book_id` – идентификатор книги.

Для начала осуществляется проверка на наличие изменяемой книги в библиотеке с помощью функции `next` <br />
При попытке изменения статуса несуществующей книги пользователь видит ошибку. <br />
Далее объявляется список возможных статусов книг `statuses`, содержащий два значения: **В наличии** и **выдана**. <br />
После этого осуществляется смена статуса выбранной книги.

#

```python
def print_header(self, id_w: int, title_w: int, author_w: int, year_w: int, status_w: int) -> None:
    self.print_separator(id_w, title_w, author_w, year_w, status_w)
    print(f'| {"ID":^{id_w}} | {"Название":^{title_w}} | {"Автор":^{author_w}} | {"Год":^{year_w}} | {"Статус":^{status_w}} |')
```
Метод печати шапки таблицы. <br />
Приниммет следующие аргументы:
* `id_w` – Ширина поля идентификаторов книг.
* `title_w` – Ширина поля названий книг.
* `author_w` – Ширина поля авторов книг.
* `year_w` – Ширина поля годов изданий книг.
* `status_w` – Ширина поля статусов книг.

Выводит разделительную черту, а затем печатает названия полей таблицы, выровненные по центру и разделённые символом `|`.

#

```python
def print_separator(self, id_w: int, title_w: int, author_w: int, year_w: int, status_w: int) -> None:
    print('+' + '-' * (id_w + 2), '-' * (title_w + 2), '-' * (author_w + 2), '-' * (year_w + 2), '-' * (status_w + 2), sep='+', end='+\n')
```
Метод печати разделительной черты таблицы. <br />
Приниммет следующие аргументы:
* `id_w` – Ширина поля идентификаторов книг.
* `title_w` – Ширина поля названий книг.
* `author_w` – Ширина поля авторов книг.
* `year_w` – Ширина поля годов изданий книг.
* `status_w` – Ширина поля статусов книг.

Выводит разделительную черту, по ширине соответствующую заданным аргументам.

# 

```python
def _open_file(self) -> dict:    
    with open(self.filename, mode='r', encoding='utf-8') as file:
        return json.load(file)
```
Метод загрузки данных о книгах из JSON файла. <br />
Загружает информацию о библиотеке из .json файла и преобразует её в словарь.

#

```python
def _save_file(self, data: dict) -> None:
    with open(self.filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
```
Метод сохранения данных о книгах в JSON файл. <br />
Принимает следующие аргументы:
* `data` – словарь, который необходимо преобразовать в JSON формат и загрузить в соотв. файл.

Загружает информацию о библиотеке в виде словаря в .json файл.

#

```python
def __call__(self):
    while True:
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книгу')
        print('4. Показать все книги')
        print('5. Изменить статус книги')
        print('0. Выход')
        choice = int(input('Выберите действие: '))

        if choice == 1:
            self.add_book(Book(input('Введите название книги: '), input('Введите автора: '), int(input('Введите год издания: '))))
        elif choice == 2:
            self.remove_book(int(input('Введите ID книги: ')))
        elif choice == 3:
            search_mode = int(input('Введите режим поиска (1 - по названию, 2 - по автору, 3 - по году издания): '))
            search_query = input('Введите поисковый запрос: ')
            self.find_book(search_mode, search_query)
        elif choice == 4:
            self.show_books()
        elif choice == 5:
            self.change_book_status(int(input('Введите ID книги: ')))
        elif choice == 0:
            break
        else:
            print('Ошибка: Неверный выбор!')
```
**Магический метод** `__call__`. <br />
Позволяет вызывать экземпляры класса `Library`.<br />
Выводит меню взаимодействия с библиотекой и вызывает соотв. методы класса с задаваемыми аргументами.

## Конструкция `if __name__ == '__main__'`
```python
if __name__ == '__main__':
    library = Library()
    library()
```
Конструкция, позволяющая определить, как именно был запущен скрипт – напрямую или с использованием `import`. <br />
В случае, если скрипт был запущен напрямую, создаётся и вызывается экземпляр класса `Library`.