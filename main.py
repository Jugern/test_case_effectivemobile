import csv
from typing import Dict, List, Type


class ZapisKontakta:
    _fields: List[str] = ['last_name', 'first_name', 'otchestvo', 'organization', 'work_phone', 'personal_phone']

    def __init__(self, **kwargs: str) -> None:
        """
        Инициализирует экземпляр класса ZapisKontakta.

        Args:
            **kwargs (str): аргументы для инициализации полей класса.
        """
        for field in self._fields:
            setattr(self, field, kwargs.get(field, ''))

    def __str__(self) -> str:
        """
        Возвращает строковое представление экземпляра класса ZapisKontakta.

        Returns:
            str: Строковое представление экземпляра класса.
        """
        return f"{self.last_name}, {self.first_name}, {self.otchestvo}, {self.organization}, {self.work_phone}, {self.personal_phone}"


class Phonebook:
    """
    Класс Phonebook представляет собой телефонную книгу и содержит следующие методы:
        - __init__(self, record_class: Type, filename: str) -> None: Конструктор класса.
            Инициализирует экземпляр класса Phonebook с указанными аргументами.
        - add_record(self, **kwargs: str) -> None: Добавляет новую запись в телефонную книгу на основе
            переданных аргументов.
        - redactirovat(self, page_size: int = 10) -> None: Позволяет просматривать и редактировать записи в
            телефонной книге. Реализует постраницного вывода записей.
        - save_to_csv(self): Сохраняет данные из телефонной книги в CSV-файл.
        - load_from_csv(self): Загружает данные из CSV-файла в телефонную книгу.
        - search_records(self, poiskovoe_slovo: str) -> List[ZapisKontakta]: Ищет записи в телефонной книге по заданному
            поисковому запросу.

    Класс Phonebook имеет следующие атрибуты:
        - records: список, хранящий записи контактов в телефонной книге.
        - record_class: класс записи контакта из ZapisKontakta.
        - filename: имя файла для работы с телефонной книгой.
    """

    def __init__(self, record_class: Type, filename: str) -> None:
        """
        Инициализирует экземпляр класса Phonebook.

        Args:
            record_class (Type): Класс записи контакта.
            filename (str): Имя файла для работы с телефонной книгой.
        """
        self.records: list = []
        self.record_class: Type = record_class
        self.filename: str = filename

    def add_record(self, **kwargs: str) -> None:
        """
        Добавляет запись в телефонную книгу.

        Args:
            **kwargs (str): аргументы для создания новой записи.
        """
        record: Type = self.record_class(**kwargs)
        self.records.append(record)

    def redactirovat(self, page_size: int = 10) -> None:
        """
        Редактирует записи в телефонной книге.

        Args:
            page_size (int): Размер страницы при пагинации.

        Returns:
            None

        Raises:
            ValueError: Если введено некорректное значение номера страницы или строки для редактирования.
        """
        if not self.records:
            print("Нет данных в базе данных.")
            return

        total_records: int = len(self.records)  # количество записей в б.д.
        total_pages: int = (total_records + page_size - 1) // page_size  # количество страниц

        while True:
            try:
                page_number: int = int(input(f"Введите номер страницы (1-{total_pages}) или '0' для выхода: "))
                # номер страницы
                if page_number == 0:
                    return

                slovar_records: Dict[int, ZapisKontakta] = {
                    key: value for key, value in enumerate(self.records)
                    if (page_number - 1) * page_size <= key < page_number * page_size
                }  # Создание списка контактов на основе выбора страницы

                for i, record in slovar_records.items():  # Вывод списка
                    print(f"{i + 1}. {record}")

                try:
                    choice: int = int(input(f"Введите номер строки для редактирования или '0' что-бы выйти: "))
                    if 0 < choice <= len(self.records):
                        selected_record = self.records[choice - 1]
                        print("Введите новые значения в запись:")
                        new_data = {}
                        for field in self.record_class._fields:
                            znachenie = input(
                                f"{field.replace('_', ' ').title()} - сейчас: {getattr(selected_record, field)} ")
                            if znachenie:
                                new_data[field] = znachenie
                        for field, value in new_data.items():
                            setattr(selected_record, field, value)
                        print("Запись была сохранена.")
                    if choice == 0:
                        continue

                except ValueError:
                    raise ValueError("Введено некорректное значение номера строки для редактирования.")

                except Exception as e:
                    print(f'Ошибка: {e}')
                    continue

            except ValueError:
                continue

    def save_to_csv(self):
        """
        Сохраняет данные из телефонной книги в CSV-файл.

        В файл записываются только поля, определенные в классе записи (self.record_class).

        Raises:
            OSError: Если возникла ошибка при сохранении данных в файл.
        """
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.record_class._fields)
                for record in self.records:
                    row = [getattr(record, field, '') for field in self.record_class._fields]
                    writer.writerow(row)
            print("Данные сохранены в файл.")

        except Exception as e:
            print(f"Произошла ошибка при сохранении данных: {e}")

    def load_from_csv(self):
        """
        Загружает данные из CSV-файла в телефонную книгу.

        Если файл не найден, создает файл phonebook.csv со стандартными полями.

        Raises:
            FileNotFoundError: Если файл не найден.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                try:
                    fields = next(reader)  # Читаем заголовок столбцов
                    for row in reader:
                        data: Dict[str, str] = dict(zip(fields, row))
                        self.add_record(**data)
                    print("Данные загружены.")
                except StopIteration:
                    print("Пустой файл.")

        except FileNotFoundError:
            print("Файл не найден. Создание нового файла...")
            initial_fields = ['last_name', 'first_name', 'otchestvo', 'organization', 'work_phone', 'personal_phone']
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(initial_fields)
            print("Файл phonebook.csv создан с начальными полями.")

        except Exception as e:
            print(f"Ошибка программы: {e}")

    def search_records(self, poiskovoe_slovo: str) -> List[ZapisKontakta]:
        """
        Ищет записи в телефонной книге по заданному поисковому запросу.

        Args:
            poiskovoe_slovo (str): Поисковый запрос для поиска в записях телефонной книги.

        Returns:
            list: Список записей, соответствующих поисковому запросу.
        """
        results: list[ZapisKontakta] = []
        for record in self.records:
            check: bool = False  # Счетчик поиска по всем полям. Если нашел, то break
            for field in record.__dict__.values():
                if isinstance(field, str) and poiskovoe_slovo.lower() in field.lower():
                    check = True
                    break
            if check:
                results.append(record)
        return results


phonebook = Phonebook(ZapisKontakta, 'phonebook.csv')  # загружаем б.д.
phonebook.load_from_csv()
# Цикл обработки пользовательского ввода
while True:
    # Запрос выбора пользователя
    choice: int = int(input("Введите 1, чтобы добавить запись в телефонную книгу\n"
                            "Введите 2 для вывода списка из телефонной книжки\n"
                            "Введите 3 для поиска в телефонной книжке\n"
                            "Нажмите 4, чтобы выйти из программы\n"))

    if choice == 1:
        # Добавление записи в телефонную книгу
        last_name: str = input("Введите фамилию: ").replace(',', '-')
        first_name: str = input("Введите имя: ").replace(',', '-')
        otchestvo: str = input("Введите отчество: ").replace(',', '-')
        organization: str = input("Введите организацию: ").replace(',', '-')
        work_phone: str = input("Введите рабочий телефон: ").replace(',', '-')
        personal_phone: str = input("Введите персональный телефон: ").replace(',', '-')
        phonebook.add_record(last_name=last_name, first_name=first_name, otchestvo=otchestvo,
                             organization=organization, work_phone=work_phone, personal_phone=personal_phone)
        phonebook.save_to_csv()

    elif choice == 2:
        # Вывод списка из телефонной книги
        phonebook.redactirovat()
        phonebook.save_to_csv()

    elif choice == 3:
        # Поиск в телефонной книге
        search_criteria = {}
        value = input("Кого искать: ")
        results = phonebook.search_records(value)
        if results:
            print("Результаты поиска:")
            for record in results:
                print(record)
            print("-" * 30)
            print(input('Нажмите Enter для продолжения'))
        else:
            print("Запись не найдена")

    elif choice == 4:
        # Выход из программы
        break
    else:
        print("Неверный выбор. Ожидается число от 1 до 4")
