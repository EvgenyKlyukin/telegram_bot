import sqlite3


class Table:
    """Класс представляющий собой таблицу из БД,
    при создании объекта класса создается таблица."""
    def __init__(self, table) -> None:
        self.create_table()

    def create_table(self):  # Нужно редактировать
        connection = sqlite3.connect(r'telegram_bot\database')
        cursor = connection.cursor()

        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    date_of_birt TEXT NOT NULL,
                    phone_number INTEGER NOT NULL)
                    ''')
            connection.commit()
        except sqlite3.Error as e:
            print(f"Произошла ошибка при создании таблицы {e}")
        finally:
            connection.close()
