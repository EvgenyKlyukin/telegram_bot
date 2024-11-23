import psycopg2

import logging

from settings import host, user, password, db_name, port

from datetime import date, timedelta


def user_exists(user_id):
    """Проверяет существование пользователя в БД."""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT number FROM telegram_users WHERE user_id = %s""",
                (user_id,)
                )
            result = cursor.fetchone()
            if result is not None:
                return True
            return False
    except Exception as e:
        logging.error(f'[user_exists] - {e}')
    finally:
        if connection:
            connection.close()


def add_user(user_id, phone_number):
    """Добавляет пользователя в БД (telegram_users)."""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO telegram_users(user_id, number)
                VALUES (%s, %s);""", (user_id, phone_number)
                )
            connection.commit()
    except Exception as e:
        logging.error(f'[add_user] - {e}')
    finally:
        if connection:
            connection.close()


def checklist():
    """Возвращает записи на прием на следующий день в виде списка кортежей"""
    date_today = date.today() + timedelta(days=1)
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT start_date, duration, client_data, worker_id
                FROM event
                WHERE start_date = %s""",
                (date_today,)
                )
            result = cursor.fetchall()
            return result
    except Exception as e:
        logging.error(f'[checklist] - {e}')
    finally:
        if connection:
            connection.close()


def worker_speciality(id_worker):
    """Возвращает id специальности врача."""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, speciality_id
                FROM worker
                WHERE id = %s""",
                (id_worker,)
                )
            result = cursor.fetchone()
            return name_speciality(result[-1])
    except Exception as e:
        logging.error(f'[worker_speciality] - {e}')
    finally:
        if connection:
            connection.close()


def name_speciality(speciality_id):
    """Возвращает название специальности врача."""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, name
                FROM speciality
                WHERE id = %s""",
                (speciality_id,)
                )
            result = cursor.fetchone()
            return result[-1]
    except Exception as e:
        logging.error(f'[name_speciality] - {e}')
    finally:
        if connection:
            connection.close()


def id_telegram_users(number):
    """Возвращает id пользователя."""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT user_id, number
                FROM telegram_users
                WHERE number = %s""",
                (number,)
                )
            result = cursor.fetchone()
            return result[0]
    except Exception as e:
        logging.error(f'[id_telegram_users] - {e}')
    finally:
        if connection:
            connection.close()
