import calendar
import uuid
from datetime import datetime
from typing import Dict, Union

from sqlalchemy import Column, Integer, String, UUID, Boolean, Date, inspect, and_, select, extract, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, attributes
from sqlalchemy_utils import database_exists

from api_fast_api.config import ASYNC_SQLALCHEMY_DATABASE_URL
from api_fast_api.logger_project.logger__app import logger_debug

# Создаем асинхронный движок для асинхронных операций
engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=False)
# Создаем асинхронную сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
# Создаем экземпляр базового класса
Base = declarative_base()


# ===================================================

# Модель зарегистрированных пользователей
class UsersSql(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    last_name = Column(String(50), default=None)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    disabled = Column(Boolean, default=False)


# Модель зарезервированных пользователем уроков
class LessonsDaysSql(Base):
    __tablename__ = 'lessons_days'

    id = Column(Integer, primary_key=True)  # Будет назначено автоматически в БД (уникальное)
    username = Column(String(50), nullable=False)  # Обязательно
    last_name = Column(String(50), nullable=False)  # Обязательно
    phone = Column(String(50), nullable=False)  # Обязательно
    email = Column(String(100), nullable=False)  # Обязательно (уникальное)
    selected_date = Column(Date)  # Обязательно 2020-04-30 Column(Date)
    time = Column(String(20), nullable=False, default='00:00')  # Если нет, то по умолчанию будет default='00:00'
    confirmed = Column(Boolean, default=False)  # По умолчанию всегда будет default='false'


# ======================== Функция создание БД
async def async_create_database():
    """Функция создания БД"""
    async with Session() as session:
        async with session.begin():
            # Проверяем существование базы данных асинхронно
            if not database_exists(engine.url):
                # Создаем базу данных
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                logger_debug.debug("as_База данных и таблицы успешно созданы.")
                return True
            else:
                logger_debug.debug("База данных уже существует.")
                # Проверяем существующие таблицы
                async with engine.connect() as conn:
                    # Получаем все таблицы которые есть в БД
                    existing_tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

                # Получаем все таблицы из метаданных которые должны присутствовать в БД
                expected_tables = set(Base.metadata.tables.keys())

                # Сравниваем наличие таблиц существующих и запланированных
                # При необходимости создаем те что отсутствуют в БД
                if set(existing_tables) == expected_tables:
                    logger_debug.debug("as_Все необходимые таблицы уже существуют.")
                else:
                    missing_tables = expected_tables - set(existing_tables)
                    print(f"Некоторые таблицы отсутствуют в базе данных: {missing_tables}")
                    logger_debug.error(f"Некоторые таблицы отсутствуют в базе данных: {missing_tables}")

                    # Создаем отсутствующие таблицы
                    async with engine.begin() as conn:
                        for table_name in missing_tables:
                            table = Base.metadata.tables[table_name]
                            await conn.run_sync(table.create)
                            print(f"Таблица {table_name} создана успешно.")
                            logger_debug.debug(f"Таблица {table_name} создана успешно.")
                    print("Таблицы которые отсутствуют добавлены.")
                    logger_debug.debug("Таблицы которые отсутствуют добавлены.")
                    return True


# ======================== Функция добавления урока в БД из календаря
async def async_add_lesson_data_to_db(username: str,
                                      last_name: str,
                                      phone: str,
                                      email: str,
                                      selected_date: str,
                                      time: str
                                      ):
    """Функция добавления урока из календаря в БД"""
    async with Session() as session:
        async with session.begin():
            try:
                # Проверяем есть ли уже такой урок с такими же параметрами
                statement = select(LessonsDaysSql).where(
                        and_(LessonsDaysSql.username == username,
                             LessonsDaysSql.selected_date == datetime.strptime(selected_date, "%Y-%m-%d").date(),
                             LessonsDaysSql.email == email,
                             LessonsDaysSql.time == time
                             )
                )

                result = await session.execute(statement)
                lesson_exists = result.scalar()

                # Если нет такого урока в БД, то создаем запись
                if not lesson_exists:
                    new_lesson = LessonsDaysSql(
                            username=username,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            selected_date=datetime.strptime(selected_date, "%Y-%m-%d").date(),
                            time=time,
                            confirmed=False
                    )

                    session.add(new_lesson)
                    await session.commit()
                    print("Урок успешно добавлен в базу данных.")
                    logger_debug.debug("Урок успешно добавлен в базу данных.")
                    return True  # Добавлено в БД
                else:
                    print("Урок на эту дату уже занят.")
                    logger_debug.debug("Урок на эту дату уже занят.")
                    return False  # Такой урок уже существует
            except Exception as e:
                await session.rollback()
                print("Ошибка при добавлении урока в базу данных:", str(e))
                logger_debug.exception(f"Ошибка при добавлении урока в базу данных: {str(e)}")
                return {"error": str(e)}  # Возврат ошибки


# ======================== Функция выбора уроков по заданному месяцу (ПРОСТО ДАТА)
async def async_lesson_dates_for_the_month_db_backend(date: str):
    """Функция выбора уроков по заданному месяцу (ПРОСТО ДАТА И СТАТУС УРОКА) для бекенд админчасти"""
    try:
        # Преобразуем строку в объект даты и получаем год и месяц
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        year = date_obj.year
        month = date_obj.month
    except Exception as e:
        logger_debug.exception(f"error: {str(e)}")
        return 422, {"error": str(e)}  # Все типы ошибок (возврат)

    # Создаем словарь для хранения результатов
    results_dict = dict()

    # Выполняем запрос к базе данных
    async with Session() as session:
        async with session.begin():
            try:
                statement = select(LessonsDaysSql).where(
                        extract('year', LessonsDaysSql.selected_date) == year,  # type: ignore
                        extract('month', LessonsDaysSql.selected_date) == month  # type: ignore
                )
                result = await session.execute(statement)
                lessons = result.scalars().all()

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
                logger_debug.exception(f"error: {str(e)}")
                return 500, {"error": str(e)}  # Все типы ошибок


async def async_lesson_dates_for_the_month_db_frontend(date_month: str):
    """Функция выбора уроков по заданному месяцу (ПРОСТО ДАТА И СТАТУС УРОКА) для фронтенд админчасти"""
    try:
        # Преобразуем строку в объект даты и получаем год и месяц
        date_obj = datetime.strptime(date_month, "%Y-%m-%d").date()
        year = date_obj.year
        month = date_obj.month
    except Exception as e:
        logger_debug.error(f"error - Incorrect date format: {str(e)}")
        return 422, {"error": "Incorrect date format"}  # Все типы ошибок

    # Создаем словарь для хранения результатов
    result_dict = {}

    # Счетчик для генерации id
    counter = 1

    # Выполняем запрос к базе данных
    async with Session() as session:
        async with session.begin():
            try:
                # Выполняем запрос для выборки данных за указанный месяц
                statement = select(LessonsDaysSql.selected_date, LessonsDaysSql.time).where(
                        extract('year', LessonsDaysSql.selected_date) == year,  # type: ignore
                        extract('month', LessonsDaysSql.selected_date) == month  # type: ignore
                )
                result = await session.execute(statement)
                lessons = result.fetchall()

                # Заполняем словарь
                for lesson in lessons:
                    date_str = lesson.selected_date.strftime('%Y-%m-%d')
                    time_slot = int(lesson.time)  # Считываем время записи урока

                    if date_str not in result_dict:
                        result_dict[date_str] = []
                    result_dict[date_str].append({"time_slot": time_slot})

                # Преобразуем словарь в отсортированный список по датам
                result_list = []

                for date_str in sorted(result_dict.keys()):
                    sorted_lessons = sorted(result_dict[date_str], key=lambda x: x["time_slot"])
                    lessons_data = {
                            "id": counter,  # Используем счетчик для id
                            "date": date_str,
                            "lessons": [lesson["time_slot"] for lesson in sorted_lessons],
                    }
                    result_list.append(lessons_data)
                    counter += 1  # Увеличиваем счетчик для следующего объекта

                if len(result_list) >= 1:
                    return 200, result_list
                else:
                    return 404, "Not found"

            except Exception as e:
                logger_debug.exception(f"error: {str(e)}")
                return 500, {"error": str(e)}


# ======================== Функция получение занятий на определенный месяц (ПОЛНЫЕ ДАННЫЕ ЗАПИСИ)
async def async_get_lessons_for_month(date_in: str):
    """
    Получение уроков из БД на определенный месяц (полные данные записи)

    :param date_in: str Example: '2024-04-20' yyyy-dd-mm
    :returns tuple: (status_cod:int, month_name:[{},{},{{},{}}])
    """
    # Проверка даты
    try:
        year, month, _ = map(int, date_in.split('-'))  # Вытягиваем год и месяц
    except Exception as e:
        logger_debug.exception(f"error - Incorrect date format: {str(e)}")
        return 422, str(e)

    async with Session() as session:
        async with session.begin():
            try:
                # Парсим строку с датой
                search_date = datetime.strptime(date_in, '%Y-%m-%d')
                # Формируем запрос, выбирая записи, у которых год и месяц совпадают с заданной датой
                statement = select(LessonsDaysSql).where(
                        extract('year', LessonsDaysSql.selected_date) == search_date.year,  # type: ignore
                        extract('month', LessonsDaysSql.selected_date) == search_date.month  # type: ignore
                ).order_by(LessonsDaysSql.selected_date)

                result = await session.execute(statement)
                lessons = result.scalars().all()

                lessons_dict = {}
                id_counter = 1  # Установим начальное значение для переменной id_counter

                # Обходим результаты запроса
                for lesson in lessons:
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
                    return 404, False
                elif len(search_data_month) > 0:
                    return 200, search_data_month

            except Exception as e:
                logger_debug.exception(f"error: {str(e)}")
                return 500, str(e)


# ======================== Функция получение уроков из БД на определенный месяц
# ======================== (ПОЛНЫЕ ДАННЫЕ ЗАПИСИ) одномерный список
async def async_get_lessons_for_month_one_dimensional_list(date_in: str):
    """Получение уроков из БД на определенный месяц

    :param date_in: str Example: '2024-04-20' yyyy-dd-mm
    :returns tuple: (status_cod:int, dict)
    """

    try:
        year, month, _ = map(int, date_in.split('-'))  # Вытягиваем год и месяц
    except Exception as e:
        logger_debug.exception(f"error - Incorrect date format: {str(e)}")
        return 422, str(e)

    try:
        async with Session() as session:
            # Выполнение запроса к базе данных
            result = await session.execute(
                    select(LessonsDaysSql).filter(
                            extract('year', LessonsDaysSql.selected_date) == year,
                            extract('month', LessonsDaysSql.selected_date) == month
                    )
            )
            lessons = result.scalars().all()

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

            lessons_list_sorted = sorted(lessons_list, key=lambda x: x["selected_date"])

        if len(lessons_list) == 0:
            return 404, False
        elif len(lessons_list) > 0:
            return 200, lessons_list_sorted
    except Exception as e:
        logger_debug.exception(f"error: {str(e)}")
        return 500, str(e)


# ======================== Функция сохранение данных пользователя в базе данных. (Регистрация)
async def async_save_user_registration(username: str, email: str, hashed_password: str) -> tuple:
    """Сохранение данных нового пользователя в базе данных."""
    # Подключаемся к базе данных и открываем сессию
    async with Session() as session:
        try:
            # Проверяем, сколько пользователей уже зарегистрировано
            user_count_result = await session.execute(select(func.count(UsersSql.id)))
            user_count = user_count_result.scalar()

            # Если количество пользователей превышает 2, возвращаем отказ в доступе
            if user_count >= 2:
                return 409, False

            # Проверяем, существует ли уже пользователь с таким email
            statement = select(UsersSql).where(UsersSql.email == email)  # type: ignore
            result = await session.execute(statement)
            existing_user = result.scalars().first()

            if existing_user:
                # Если пользователь с таким email уже существует, возвращаем код конфликта
                # Если количество пользователей ограничено для регистрации и превышает лимит пользователей
                return 409, False

            # Создаем новую запись пользователя
            new_user = UsersSql(username=username, email=email, hashed_password=hashed_password)
            # Добавляем пользователя в сессию
            session.add(new_user)
            # Сохраняем изменения в базу данных
            await session.commit()

            # Возвращаем код успеха, True и JWT токен
            return 201, True

        except Exception as e:
            logger_debug.exception(f"error: {str(e)}")
            # Откатываем изменения в случае возникновения другой ошибки
            await session.rollback()
            # Возвращаем код ошибки и False в случае других исключений
            return 500, str(e)


# ======================== Функция получение списка всех уроков из БД на конкретный день определенного месяца
# ======================== (полные данные записи)
async def async_get_lessons_for_day(date: str):
    """Получение уроков из БД на конкретный день определенного месяца
    :param date: str (2024-01-20)
    """
    # Проверка даты
    try:
        year, month, day = map(int, date.split('-'))  # Вытягиваем год и месяц
    except Exception as e:
        logger_debug.exception(f"error: {str(e)}")
        return 422, str(e)

    # Выполняем запрос к базе данных
    async with Session() as session:
        async with session.begin():
            try:
                # Выполнение запроса к базе данных
                statement = select(LessonsDaysSql).where(
                        extract('year', LessonsDaysSql.selected_date) == year,
                        extract('month', LessonsDaysSql.selected_date) == month,
                        extract('day', LessonsDaysSql.selected_date) == day
                )
                result = await session.execute(statement)
                lessons = result.scalars().all()

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

                lessons_list_sorted = sorted(lessons_list, key=lambda x: x["id"])

                if len(lessons_list) == 0:  # Если нет записей возвращаем
                    return 404, str("Not found")
                elif len(lessons_list) > 0:
                    return 200, lessons_list_sorted
            except Exception as e:  # Обработка ошибок
                logger_debug.exception(f"error: {str(e)}")
                return 500, str(e)


# ======================== Функция подтверждения урока пользователю,
# ======================== меняет метку статуса урока на True (одобрено) в БД
async def async_change_lesson_status_db(lesson_id: int) -> tuple:
    """Функция подтверждения урока пользователю.
    Изменяет метку статуса урока на True (одобрено) В БД

    :param lesson_id: Идентификатор урока, который требуется подтвердить
    :return: True, если операция выполнена успешно, False в противном случае
    """
    async with Session() as session:
        try:
            # Получаем урок по его идентификатору
            statement = select(LessonsDaysSql).where(LessonsDaysSql.id == lesson_id)  # type: ignore
            result = await session.execute(statement)
            lesson = result.scalars().first()

            # Если урок не найден, возвращаем False
            if not lesson:
                return 404, False

            # Изменяем метку статуса урока на True (одобрено)
            lesson.confirmed = True
            # Сохраняем изменения в базе данных
            await session.commit()
            # Возвращаем True, чтобы указать успешное выполнение операции
            return 200, True

        except Exception as e:
            logger_debug.exception(f"error: {str(e)}")
            await session.rollback()  # Откатываем изменения в случае возникновения ошибки
            return 500, str(e)


# ======================== Функция удаления записи об уроке конкретного пользователя
async def async_delete_lesson_db(lesson_id: int) -> tuple:
    """Функция удаления записи об уроке конкретного пользователя.

    :param lesson_id: Словарь с данными пользователя, содержащий user_id и lesson_id
    :return: Кортеж (статусный код, сообщение об успешности операции)
    """
    print("Пришел запрос на удаление записи", lesson_id)
    logger_debug.debug(f"Пришел запрос на удаление записи {lesson_id}")
    async with Session() as session:
        try:
            # Получаем запись урока по идентификатору
            statement = select(LessonsDaysSql).where(LessonsDaysSql.id == lesson_id)  # type: ignore
            result = await session.execute(statement)
            lesson = result.scalars().first()
            # Если запись не найдена, возвращаем ошибку
            if not lesson:
                return 404, False

            # Удаляем найденную запись
            await session.delete(lesson)
            # Сохраняем изменения в базе данных
            await session.commit()

            # Возвращаем успешный статус и сообщение
            return 200, True

        except Exception as e:
            logger_debug.exception(f"error: {str(e)}")
            await session.rollback()  # Откатываем изменения в случае возникновения ошибки
            return 500, str(e)


# ======================== Функция изменения данных записи урока
async def async_change_lesson_data_db(lesson_id: int, data: dict) -> tuple:
    """Функция изменения данных записи урока

    :param lesson_id: Идентификатор урока, который требуется изменить
    :param data: Словарь с данными
    :return: True, если операция выполнена успешно, False в противном случае
    """
    async with Session() as session:
        try:
            # Получаем урок по его идентификатору
            statement = select(LessonsDaysSql).where(LessonsDaysSql.id == lesson_id)  # type: ignore
            result = await session.execute(statement)
            lesson_change = result.scalars().first()

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
                            logger_debug.exception(f"error: {f"Invalid date format for '{key}': {value}"}")
                            return 400, f"Invalid date format for '{key}': {value}"
                    setattr(lesson_change, key, value)

                # Сохраняем изменения в базе данных
                await session.commit()

            # Возвращаем True, чтобы указать успешное выполнение операции
            logger_debug.debug(f"Данные урока {lesson_id} изменены")
            return 200, True

        except Exception as e:  # Обработка ошибок
            logger_debug.exception(f"error: {str(e)}")
            # Откатываем изменения в случае возникновения другой ошибки
            await session.rollback()
            return 500, str(e)


# ======================== Функция получения данных записи урока по id
async def async_get_lesson_data_db(lesson_id: int) -> tuple:
    """
    Функция получения данных записи урока по id

    :param lesson_id: int (Идентификатор урока для получения)
    :return dict: Данные урока
    """
    async with Session() as session:
        try:
            # Получаем урок по его идентификатору
            statement = select(LessonsDaysSql).where(LessonsDaysSql.id == lesson_id)  # type: ignore
            result = await session.execute(statement)
            lesson_data = result.scalars().first()

            # Если урок не найден
            if not lesson_data:
                return 404, False

            return 200, lesson_data

        except Exception as e:  # Обработка ошибок
            logger_debug.exception(f"error: {str(e)}")
            return 500, str(e)


# ======================== Функция преобразования объекта SQLAlchemy в словарь.
async def sqlalchemy_obj_to_dict(obj) -> Dict:
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
async def search_user_database(username: str) -> Union[UsersSql, None] | dict:
    """
    Функция поиска пользователя в БД

    - Принимает имя пользователя тип str
    - Возвращает объект SQLAlchemy или None
    """
    async with Session() as session:
        try:
            statement = select(UsersSql).where(UsersSql.username == username)  # type: ignore
            result = await session.execute(statement)
            user = result.scalars().first()

            if user:
                return user
            else:
                return None
        except Exception as e:
            print("Ошибка БД:", str(e))
            logger_debug.exception(f"error: {str(e)}")

            return {"error": str(e)}
