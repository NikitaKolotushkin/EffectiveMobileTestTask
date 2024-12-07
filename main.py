#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


class Book(object):
    def __init__(self, title: str, author: str, year: int) -> None:
        """
        Initializes a Book object with title, author, year, and default status.

        :param title: The title of the book.
        :type title: str
        :param author: The author of the book.
        :type author: str
        :param year: The year the book was published.
        :type year: int
        """
        self.id = 0
        self.title = title
        self.author = author
        self.year = year
        self.status = 'В наличии'

    def __eq__(self, other: object) -> bool:
        """
        Checks if two books are equal.

        This function is used to compare two :class:`Book` objects.

        :param other: The other book to compare.
        :type other: object
        :return: Whether the two books are equal.
        :rtype: bool
        """
        if not isinstance(other, Book):
            return False
        return (self.title == other.title) and (self.author == other.author) and (self.year == other.year)

    def __str__(self) -> str:    
        """
        Returns a string representation of the book.

        This method provides a human-readable representation of the book,
        including its ID, title, author, year, and status.

        :return: A string representation of the book.
        :rtype: str
        """
        return f'{self.id}: {self.title} ({self.author}, {self.year}) - {self.status}'


class Library(object):
    def __init__(self, filename: str = 'library.json') -> None:
        """
        Initializes a :class:`Library` object.

        This function is used to initialize a :class:`Library` object. It takes
        an optional parameter, `filename`, which is the name of the file to use
        for storing the library data. If no filename is given, the default
        filename is 'library.json'.

        The function first tries to open the file for reading. If the file does
        not exist, it is created with an empty list of books.

        :param filename: The name of the file to use for storing the library data.
        :type filename: str
        """
        self.filename = filename
        try:
            self._open_file()
        except FileNotFoundError:
            self._save_file({'books': []})

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the library.

        This function is used to add a book to the library. It takes a
        :class:`Book` object as a parameter and adds it to the library.

        If a book with the same title, author, and year already exists
        in the library, a message is printed to the console indicating
        that the book already exists and the function does nothing else.

        The id of the book is set to the id of the last book in the
        library plus one, or one if the library is empty.

        The book is then added to the library and the library data is
        written to the file.

        :param book: The book to add to the library.
        :type book: Book
        :return: None
        """
        data = self._open_file()
        
        if any(book == Book(b['title'], b['author'], b['year']) for b in data['books']):
            print('Ошибка: Книга уже есть в библиотеке!')
            return
    
        book.id = data['books'][-1]['id'] + 1 if data['books'] else 1
        
        data['books'].append(book.__dict__)
        
        self._save_file(data)

    def remove_book(self, book_id: int) -> None:
        """
        Removes a book from the library.

        This function is used to remove a book from the library. It takes
        a book id as a parameter and removes the book with the given id
        from the library.

        If a book with the given id does not exist in the library, a
        message is printed to the console indicating that the book does
        not exist and the function does nothing else.

        The book is then removed from the library and the library data is
        written to the file.

        :param book_id: The id of the book to remove.
        :type book_id: int
        :return: None
        """
        data = self._open_file()

        book = next((book for book in data['books'] if book['id'] == book_id), None)

        if book is None:
            print(f'Ошибка: Книги с id = {book_id} не существует!')
            return

        data['books'] = [book for book in data['books'] if book['id'] != book_id]

        self._save_file(data)

    def find_book(self, search_mode: int, search_query: str) -> None:
        
        """
        Finds a book in the library and prints it to the console.

        This function is used to find a book in the library and print it
        to the console. It takes two parameters: a search mode and a
        search query. The search mode must be an integer between 1 and
        3, inclusive, which determines how the search query is used to
        search for the book. The search modes are:

        1. Search by title: The search query is used to search the
           title of the books in the library.

        2. Search by author: The search query is used to search the
           author of the books in the library.

        3. Search by year: The search query is used to search the year
           the books in the library were published.

        If a book with the given search query is not found in the
        library, a message is printed to the console indicating that
        the book was not found.

        :param search_mode: The search mode to use.
        :type search_mode: int
        :param search_query: The search query to use.
        :type search_query: str
        :return: None
        """
        data = self._open_file()

        search_modes = ['title', 'author', 'year']

        if search_mode not in range(1, len(search_modes) + 1):
            print('Ошибка: Неверный режим поиска!')
            return

        matching_books = [book for book in data if str(book[search_modes[search_mode - 1]]) == search_query]

        if not matching_books:
            print('Книги не найдены!')
            return

        self.show_books(matching_books)

    def show_books(self, book_list: list = None) -> None:
        """
        Displays a list of books in a formatted table.

        This function prints out the details of books in a tabular format.
        It can display either all books in the library or a specific list
        of books if provided. The table includes columns for book ID, title,
        author, year, and status. If no books are found, a message is printed
        to the console.

        :param book_list: A list of books to display. If None, all books in
                        the library are displayed.
        :type book_list: list, optional
        :return: None
        """
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

    def change_book_status(self, book_id: int) -> None:
        """
        Changes the status of a book.

        This function is used to change the status of a book in the library.
        It takes the id of the book as a parameter and changes its status to
        the next one in the list of statuses. If the book does not exist, a
        message is printed to the console.

        :param book_id: The id of the book to change the status of.
        :type book_id: int
        :return: None
        """
        data = self._open_file()
        
        book = next((book for book in data['books'] if book['id'] == book_id), None)

        if book is None:
            print(f'Ошибка: Книги с id = {book_id} не существует!')
            return

        statuses = ['В наличии', 'Выдана']
        book['status'] = statuses[(statuses.index(book['status']) + 1) % 2]

        self._save_file(data)

    def print_header(self, id_w: int, title_w: int, author_w: int, year_w: int, status_w: int) -> None:
        """
        Prints a header line for the table.

        This function is used to print the header line of the table when
        displaying the books in the library. It takes the widths of the
        columns as parameters and prints the header line with the column
        names centered in the columns.

        :param id_w: The width of the "ID" column.
        :type id_w: int
        :param title_w: The width of the "Название" column.
        :type title_w: int
        :param author_w: The width of the "Автор" column.
        :type author_w: int
        :param year_w: The width of the "Год" column.
        :type year_w: int
        :param status_w: The width of the "Статус" column.
        :type status_w: int
        :return: None
        """
        self.print_separator(id_w, title_w, author_w, year_w, status_w)
        print(f'| {"ID":^{id_w}} | {"Название":^{title_w}} | {"Автор":^{author_w}} | {"Год":^{year_w}} | {"Статус":^{status_w}} |')
        self.print_separator(id_w, title_w, author_w, year_w, status_w)

    def print_separator(self, id_w: int, title_w: int, author_w: int, year_w: int, status_w: int) -> None:
        """
        Prints a separator line for the table.

        This function is used to print a separator line for a table of books.
        It takes the widths of the columns as parameters and prints a separator
        line with the same length as the header line.

        :param id_w: The width of the ID column.
        :type id_w: int
        :param title_w: The width of the title column.
        :type title_w: int
        :param author_w: The width of the author column.
        :type author_w: int
        :param year_w: The width of the year column.
        :type year_w: int
        :param status_w: The width of the status column.
        :type status_w: int
        :return: None
        """
        print('+' + '-' * (id_w + 2), '-' * (title_w + 2), '-' * (author_w + 2), '-' * (year_w + 2), '-' * (status_w + 2), sep='+', end='+\n')

    def _open_file(self) -> dict:
        with open(self.filename, mode='r', encoding='utf-8') as file:
            return json.load(file)
        
    def _save_file(self, data: dict) -> None:
        with open(self.filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def __call__(self):
        """
        Runs the library management system.

        This function is called when the library object is invoked as a
        function. It runs the library management system, showing the user a
        menu of options and performing the action chosen by the user.

        :return: None
        """
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


if __name__ == '__main__':
    library = Library()
    library()