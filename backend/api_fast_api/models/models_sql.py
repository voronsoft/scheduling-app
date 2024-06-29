import calendar
import uuid
from datetime import datetime
from typing import Dict, List, Union

from fastapi import HTTPException
from sqlalchemy_utils import database_exists
from sqlalchemy.orm import sessionmaker, attributes, declarative_base
from sqlalchemy import Column, Integer, Date, Boolean, String, create_engine, extract, or_, and_, inspect, func, UUID

from api_fast_api.config import SQLALCHEMY_DATABASE_URL

# Создаем экземпляр класса Engine для соединения с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
# Создаем экземпляр базового класса
Base = declarative_base()


# ===================================================

# Модель зарегистрированных пользователей
class UsersSql(Base):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    last_name = Column(String(50), default=None)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    disabled = Column(Boolean, default=False)


# Модель зарезервированных пользователем уроков
class LessonsDaysSql(Base):
    __tablename__: str = 'lessons_days'

    id = Column(Integer, primary_key=True)  # Будет назначено автоматически в БД (уникальное)
    username = Column(String(50), nullable=False)  # Обязательно
    last_name = Column(String(50), nullable=False)  # Обязательно
    phone = Column(String(50), nullable=False)  # Обязательно
    email = Column(String(100), nullable=False)  # Обязательно (уникальное)
    selected_date = Column(Date)  # Обязательно 2020-4-30 Column(Date)
    time = Column(String(20), nullable=False, default='00:00')  # Если нет, то по умолчанию будет default='00:00'
    confirmed = Column(Boolean, default=False)  # По умолчанию всегда будет default='false'


# ======================== Функция создание БД
def create_database():
    """Функция создание БД"""
    if not database_exists(engine.url):
        # Если базы данных не существует, создаем ее и все таблицы
        Base.metadata.create_all(bind=engine)
        print("База данных успешно создана.")
        return True
    else:
        # Если база данных существует, проверяем наличие всех таблиц
        with engine.connect() as connection:
            inspector = inspect(connection)
            existing_tables = inspector.get_table_names()

            # Получаем все классы, определенные в models.py
            model_classes = Base.__subclasses__()

            # Проверяем наличие всех таблиц, и если каких-то не хватает, создаем их
            for cls in model_classes:
                table_name = cls.__tablename__
                if table_name not in existing_tables:
                    cls.__table__.create(bind=engine)
                    print(f"Таблица {table_name} успешно создана.")

        print("База данных уже существует.")
        return False


# ======================== Функция добавления урока в БД из календаря
def add_lesson_data_to_db(username: str, last_name: str, phone: str, email: str, selected_date: str, time: str):
    """Функция добавления урока из календаря в БД"""
    with Session() as session:
        try:
            # Проверяем есть ли уже такой урок с такими же username, selected_date, email и time
            lesson_exists = session.query(LessonsDaysSql).filter(
                    and_(
                            # Имя пользователя
                            LessonsDaysSql.username == username,
                            # Дата занятия
                            LessonsDaysSql.selected_date == datetime.strptime(selected_date,
                                                                              "%Y-%m-%d"
                                                                              ).date(),
                            # Почта
                            LessonsDaysSql.email == email,
                            # Время урока
                            LessonsDaysSql.time == time
                    )
            ).first()

            # Если нет такого урока в БД, то создаем запись!
            if not lesson_exists:
                new_lesson = LessonsDaysSql(username=username,
                                            last_name=last_name,
                                            phone=phone,
                                            email=email,
                                            selected_date=datetime.strptime(selected_date,
                                                                            "%Y-%m-%d"
                                                                            ).date(),
                                            time=time,
                                            confirmed=False
                                            )

                session.add(new_lesson)
                # Добавляем в БД
                session.commit()
                print("Урок успешно добавлен в базу данных.")
                return True  # Добавлено в БД
            else:
                print("Урок на эту дату уже занят.")
                return False  # Такой урок уже существует
        except Exception as e:
            session.rollback()
            print("Ошибка при добавлении урока в базу данных:",
                  e
                  )
            return {
                    "error": str(e)
            }  # Все типы ошибок (возврат)


# ======================== Функция выбора уроков по заданному месяцу (ПРОСТО ДАТА)
def lesson_dates_for_the_month_db_backend(date: str):
    """Функция выбора уроков по заданному месяцу (ПРОСТО ДАТА И СТАТУС УРОКА)"""
    try:
        # Преобразуем строку в объект даты и получаем год и месяц
        date_obj = datetime.strptime(date,
                                     "%Y-%m-%d"
                                     ).date()
        year = date_obj.year
        month = str('0' + str(date_obj.month) if len(str(date_obj.month)) == 1 else date_obj.month)
    except Exception as e:
        return 422, {
                "error": str(e)
        }  # Все типы ошибок (возврат)

    # Создаем словарь для хранения результатов
    results_dict = dict()

    # Выполняем запрос к базе данных
    with Session() as session:
        # Используем фильтр, чтобы выбрать только записи с нужным месяцем и годом
        try:
            lessons = session.query(LessonsDaysSql).filter(
                    extract('year',
                            LessonsDaysSql.selected_date
                            ) == year,
                    extract('month',
                            LessonsDaysSql.selected_date
                            ) == month
            ).all()

            # Заполняем словарь результатами запроса
            for lesson in lessons:
                results_dict[str(lesson.selected_date)] = bool(lesson.confirmed)

            # Сортируем по возрастанию
            results_dict_sorted = dict(sorted(results_dict.items()))

            if len(results_dict_sorted) >= 1:
                return 200, results_dict_sorted
            else:
                return 404, "Not found"

        except Exception as e:
            return 500, {
                    "error": str(e)
            }  # Все типы ошибок (возврат)


def lesson_dates_for_the_month_db_frontend(date_month: str):
    try:
        # Преобразуем строку в объект даты и получаем год и месяц
        date_obj = datetime.strptime(date_month,
                                     "%Y-%m-%d"
                                     ).date()
        year = date_obj.year
        month = str('0' + str(date_obj.month) if len(str(date_obj.month)) == 1 else date_obj.month)
    except Exception as e:
        return 422, {
                "error": str(e)
        }  # Все типы ошибок

    # Создаем словарь для хранения результатов
    result_dict = {}

    # Выполняем запрос к базе данных
    with Session() as session:
        try:
            # Выполняем запрос для выборки данных за указанный месяц
            lessons = session.query(
                    LessonsDaysSql.selected_date,
                    LessonsDaysSql.time
            ).filter(
                    extract('year',
                            LessonsDaysSql.selected_date
                            ) == year,
                    extract('month',
                            LessonsDaysSql.selected_date
                            ) == month
            ).all()

            # Заполняем словарь
            for lesson in lessons:
                date_str = lesson.selected_date.strftime('%Y-%m-%d')
                time_slot = int(lesson.time)  # Считываем время записи урока

                if date_str not in result_dict:
                    result_dict[date_str] = []
                result_dict[date_str].append(time_slot)

            # Сортируем временные слоты внутри каждого дня
            for time_slots in result_dict.values():
                time_slots.sort()

            # Преобразуем словарь в отсортированный список по датам
            result_list = []
            for date_str in sorted(result_dict.keys()):
                result_list.append({
                        "date": date_str,
                        "lessons": result_dict[date_str]
                }
                )

            if len(result_list) >= 1:
                return 200, result_list
            else:
                return 404, "Not found"

        except Exception as e:
            return 500, {
                    "error": str(e)
            }


# ======================== Функция получение занятий на определенный месяц (ПОЛНЫЕ ДАННЫЕ ЗАПИСИ)
def get_lessons_for_month(date_in: str):
    """
    Получение уроков из БД на определенный месяц (полные данные записи)

    :param date_in: str Example: '2024-04-20' yyyy-dd-mm
    :returns tuple: (status_cod:int, month_name:[{},{},{{},{}}])
    """
    # Проверка даты
    try:
        year, month, _ = map(int,
                             date_in.split('-')
                             )  # Вытягиваем год и месяц
    except Exception as e:
        return 422, str(e)

    try:
        with Session() as session:
            # Парсим строку с датой
            search_date = datetime.strptime(date_in,
                                            '%Y-%m-%d'
                                            )
            # Формируем запрос, выбирая записи, у которых год и месяц совпадают с заданной датой
            query = session.query(LessonsDaysSql).filter(
                    extract('year',
                            LessonsDaysSql.selected_date
                            ) == search_date.year,
                    extract('month',
                            LessonsDaysSql.selected_date
                            ) == search_date.month
            ).order_by(LessonsDaysSql.selected_date)

            search_data_month = []
            lessons_dict = {}
            id_counter = 1  # Установим начальное значение для переменной id_counter

            # Обходим результаты запроса
            for lesson in query:
                lesson_date = lesson.selected_date.strftime('%Y-%m-%d')
                # Если дата уже встречалась, добавляем запись в список уроков
                if lesson_date in lessons_dict:
                    lessons_dict[lesson_date]['lessons'].append({
                            'id': lesson.id,
                            'email': lesson.email,
                            'firstName': lesson.username,
                            'lastName': lesson.last_name,
                            'phone': lesson.phone,
                            'selectedDate': lesson_date,
                            'selectedTime': lesson.time,
                            'confirmed': lesson.confirmed
                    }
                    )
                else:
                    # Создаем новую запись для данной даты
                    lessons_dict[lesson_date] = {
                            'id': id_counter,
                            'date': lesson_date,
                            'lessons': [{
                                    'id': lesson.id,
                                    'email': lesson.email,
                                    'firstName': lesson.username,
                                    'lastName': lesson.last_name,
                                    'phone': lesson.phone,
                                    'selectedDate': lesson_date,
                                    'selectedTime': lesson.time,
                                    'confirmed': lesson.confirmed
                            }]
                    }
                    # Увеличиваем значение переменной id_counter перед следующей итерацией
                    id_counter += 1

            # Преобразуем словарь в список для вывода
            search_data_month = list(lessons_dict.values())
            # Получаем название месяца на английском языке
            month_name = calendar.month_name[search_date.month]

        if len(search_data_month) == 0:
            print(len(search_data_month))
            return 404, str("Not found")
        elif len(search_data_month) > 0:
            print(len(search_data_month))
            return 200, search_data_month

    except Exception as e:
        return 500, str(e)


# ======================== Функция получение уроков из БД на определенный месяц
# ======================== (ПОЛНЫЕ ДАННЫЕ ЗАПИСИ) одномерный список
def get_lessons_for_month_one_dimensional_list(date_in: str):
    """Получение уроков из БД на определенный месяц

    :param date_in: str Example: '2024-04-20' yyyy-dd-mm
    :returns tuple: (status_cod:int, dict)
    """

    try:
        year, month, _ = map(int,
                             date_in.split('-')
                             )  # Вытягиваем год и месяц
    except Exception as e:
        return 422, str(e)

    try:
        with Session() as session:
            # Выполнение запроса к базе данных
            lessons = session.query(LessonsDaysSql).filter(
                    extract('year',
                            LessonsDaysSql.selected_date
                            ) == year,
                    extract('month',
                            LessonsDaysSql.selected_date
                            ) == month
            ).all()

            # Формируем список уроков в требуемом формате
            lessons_list = []
            for lesson in lessons:
                lesson_data = {
                        "id": lesson.id,
                        "username": lesson.username,
                        "last_name": lesson.last_name,
                        "email": lesson.email,
                        "phone": lesson.phone,
                        "selected_date": lesson.selected_date.strftime("%Y-%m-%d"),
                        "time": lesson.time,
                        "confirmed": lesson.confirmed
                }
                lessons_list.append(lesson_data)

            lessons_list_sorted = sorted(lessons_list,
                                         key=lambda x: x["selected_date"]
                                         )

        if len(lessons_list) == 0:
            return 404, False
        elif len(lessons_list) > 0:
            return 200, lessons_list_sorted
    except Exception as e:
        return 500, str(e)


# ======================== Функция сохранение данных пользователя в базе данных. (Регистрация)
def save_user_registration(username: str, email: str, hashed_password: str) -> tuple:
    """Сохранение данных нового пользователя в базе данных."""
    # Подключаемся к базе данных и открываем сессию
    with Session() as session:
        try:
            # Проверяем, сколько пользователей уже зарегистрировано
            user_count = session.query(func.count(UsersSql.id)).scalar()

            # Если количество пользователей превышает 2, возвращаем отказ в доступе
            if user_count >= 2:
                return 409, False

            # Проверяем, существует ли уже пользователь с таким email
            existing_user = session.query(UsersSql).filter(UsersSql.email == email).first()
            if existing_user:
                # Если пользователь с таким email уже существует, возвращаем код конфликта
                # Если количество пользователей огрпниченодля реистрациии и превышает лимит пользователей
                return 409, False

            # Создаем новую запись пользователя
            new_user = UsersSql(username=username,
                                email=email,
                                hashed_password=hashed_password
                                )
            # Добавляем пользователя в сессию
            session.add(new_user)
            # Сохраняем изменения в базу данных
            session.commit()

            # Возвращаем код успеха, True и JWT токен
            return 201, True

        except Exception as e:
            # Откатываем изменения в случае возникновения другой ошибки
            session.rollback()
            # Возвращаем код ошибки и False в случае других исключений
            return 500, str(e)


# ======================== Функция преобразования объекта SQLAlchemy в словарь.
def sqlalchemy_obj_to_dict(obj) -> Dict:
    """
    Преобразование объекта SQLAlchemy в словарь.

    - Принимает объект SQLAlchemy
    - Возвращает словарь с данными полей из модели таблицы
    """
    obj_dict = attributes.instance_dict(obj)
    # Удаляем ключ '_sa_instance_state' из словаря
    obj_dict.pop('_sa_instance_state')
    return obj_dict


# ======================== Функция поиска пользователя в БД
def search_user_database(username: str) -> Union[UsersSql, None] | dict:
    """
    Функция поиска пользователя в БД

    - Принимает имя пользователя тип str
    - Возвращает объект SQLAlchemy или None
    """
    with Session() as session:
        try:
            user = session.query(UsersSql).filter(UsersSql.username == username).first()
            if user:
                return user
            else:
                return None
        except Exception as e:
            print("Ошибка БД:",
                  e
                  )
            return {
                    "error": str(e)
            }


# ======================== Функция получение списка всех уроков из БД на конкретный день определенного месяца
# ======================== (полные данные записи)
def get_lessons_for_day(date: str):
    """Получение уроков из БД на конкретный день определенного месяца
    :param date: str (2024-01-20)
    """
    # Проверка даты
    try:
        year, month, day = map(int,
                               date.split('-')
                               )  # Вытягиваем год и месяц
        # print(f"{year}/{month}/{day}")
    except Exception as e:
        return 422, str(e)

    try:
        with Session() as session:
            # Выполнение запроса к базе данных
            lessons = session.query(LessonsDaysSql).filter(extract('year',
                                                                   LessonsDaysSql.selected_date
                                                                   ) == year,
                                                           extract('month',
                                                                   LessonsDaysSql.selected_date
                                                                   ) == month,
                                                           extract('day',
                                                                   LessonsDaysSql.selected_date
                                                                   ) == day
                                                           ).all()

            # Формируем список уроков в требуемом формате
            lessons_list = []
            for lesson in lessons:
                lesson_data = {
                        "id": lesson.id,
                        "firstName": lesson.username,
                        "lastName": lesson.last_name,
                        "phone": lesson.phone,
                        "email": lesson.email,
                        "selected_date": lesson.selected_date.strftime("%Y-%m-%d"),
                        "selectedTime": lesson.time,
                        "confirmed": lesson.confirmed
                }
                lessons_list.append(lesson_data)

            lessons_list_sorted = sorted(lessons_list,
                                         key=lambda x: x["id"]
                                         )

        if len(lessons_list) == 0:  # Если нет записей возвращаем
            return 404, str("Not found")
        elif len(lessons_list) > 0:
            return 200, lessons_list_sorted
    except Exception as e:  # Обработка ошибок
        return 500, str(e)


# ======================== Функция подтверждения урока пользователю,
# ======================== меняет метку статуса урока на True (одобрено) в БД
def change_lesson_status_db(lesson_id: int) -> tuple:
    """Функция подтверждения урока пользователю.
    Изменяет метку статуса урока на True (одобрено) В БД

    :param lesson_id: Идентификатор урока, который требуется подтвердить
    :return: True, если операция выполнена успешно, False в противном случае
    """
    print("change_lesson_status_db", lesson_id)
    try:
        with Session() as session:
            # Получаем урок по его идентификатору
            lesson = session.query(LessonsDaysSql).filter(LessonsDaysSql.id == lesson_id).first()

            # Если урок не найден, возвращаем False
            if not lesson:
                return 404, False

            # Изменяем метку статуса урока на True (одобрено)
            lesson.confirmed = True

            # Сохраняем изменения в базе данных
            session.commit()

            # Возвращаем True, чтобы указать успешное выполнение операции
            return 200, True

    except Exception as e:  # Обработка ошибок
        # Откатываем изменения в случае возникновения другой ошибки
        session.rollback()
        return 500, str(e)


# ======================== Функция удаления записи об уроке конкретного пользователя
def delete_lesson_db(lesson_id: int) -> tuple:
    """Функция удаления записи об уроке конкретного пользователя.

    :param lesson_id: Словарь с данными пользователя, содержащий user_id и lesson_id
    :return: Кортеж (статусный код, сообщение об успешности операции)
    """
    print("(delete_lesson_db)Пришел запрос на удаление записи",
          lesson_id
          )
    try:
        with Session() as session:
            # Получаем запись урока по идентификатору
            lesson = session.query(LessonsDaysSql).filter(LessonsDaysSql.id == lesson_id).first()
            print("lesson--------", lesson)
            # Если запись не найдена, возвращаем ошибку
            if not lesson:
                return 404, False

            # Удаляем найденную запись
            session.delete(lesson)

            # Сохраняем изменения в базе данных
            session.commit()

            # Возвращаем успешный статус и сообщение
            return 200, True

    except Exception as e:
        # Откатываем изменения в случае возникновения ошибки
        session.rollback()
        return 500, str(e)


# ======================== Функция изменения данных записи урока
def change_lesson_data_db(lesson_id: int, data: dict) -> tuple:
    """Функция изменения данных записи урока
    :param lesson_id: Идентификатор урока, который требуется изменить
    :param data: Словарь с данными
    :return: True, если операция выполнена успешно, False в противном случае
    """
    try:
        with Session() as session:
            # Получаем урок по его идентификатору
            lesson_change = session.query(LessonsDaysSql).filter(LessonsDaysSql.id == lesson_id).first()

            # Если урок не найден
            if not lesson_change:
                return 404, False

            # Изменяем данные
            for key, value in data.items():
                if value is not None:
                    if key == 'selected_date':  # Проверка, если ключ - дата
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").date()
                        except ValueError:
                            return 400, f"Invalid date format for '{key}': {value}"
                    setattr(lesson_change, key, value)

                # Сохраняем изменения в базе данных
                session.commit()

            # Возвращаем True, чтобы указать успешное выполнение операции
            return 200, True

    except Exception as e:  # Обработка ошибок
        # Откатываем изменения в случае возникновения другой ошибки
        session.rollback()
        return 500, str(e)

