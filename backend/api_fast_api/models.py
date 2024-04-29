from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .config import SQLALCHEMY_DATABASE_URL
from sqlalchemy_utils import database_exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine, extract

# Создаем экземпляр класса Engine для соединения с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
# Создаем экземпляр базового класса
Base = declarative_base()


# Модель зарегестрированных пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    token = Column(String, unique=True, nullable=True, default=None)


# Модель зарезервированных пользователем уроков
class LessonsDays(Base):
    __tablename__ = 'lessons_days'

    id = Column(Integer, primary_key=True)  # Будет назначено автоматически в БД (уникальное)
    first_name = Column(String(50), nullable=False)  # Обязательно
    last_name = Column(String(50), nullable=False)  # Обязательно
    email = Column(String(100), unique=True, nullable=False)  # Обязательно (уникальное)
    phone = Column(String(50), nullable=False)  # Обязательно
    selected_date = Column(Date)  # Обязательно 2020-4-30 Column(Date)
    selected_time = Column(String(20), nullable=False, default='00:00')  # Если нет, то по умолчанию будет default='00:00'
    confirmed_state = Column(String(30), nullable=True, default='false')  # По умолчанию всегда будет default='false'


# ------------- DB functions -------------
# Создание БД
def create_database():
    if not database_exists(engine.url):
        # Если базы данных не существует, создаем ее и все таблицы
        Base.metadata.create_all(bind=engine)
        print("База данных успешно создана.")
        return True
    else:
        print("База данных уже существует.")
        return False


# Добавления урока в БД
def add_user_to_db(first_name: str, last_name: str, email: str, phone: str, selected_date: str, selected_time: str):
    with Session() as session:
        try:
            # Проверяем, существует ли пользователь с таким email
            user_exists = session.query(LessonsDays).filter(LessonsDays.email == email).first()
            # Если пользователь не существует, добавляем его в базу данных
            if not user_exists:
                new_lesson = LessonsDays(first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         phone=phone,
                                         selected_date=datetime.strptime(selected_date, "%Y-%m-%d").date(),
                                         selected_time=selected_time,
                                         confirmed_state="false")
                session.add(new_lesson)
                session.commit()
                print("Урок успешно добавлен в базу данных.")
            else:
                print("Урок с таким email уже существует в базе данных.")
                return False, 404
        except Exception as e:
            session.rollback()
            print("Ошибка при добавлении урока в базу данных:", e)
            return 'Error', 500
    return True, 200


# Функция выбора уроков по заданному месяцу
def select_lessons_by_month(date: str):
    # Преобразуем строку в объект даты и получаем год и месяц
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    year = date_obj.year
    month = str('0' + str(date_obj.month) if len(str(date_obj.month)) == 1 else date_obj.month)

    # Создаем словарь для хранения результатов
    results_dict = dict()

    # Выполняем запрос к базе данных
    with Session() as session:

        # Используем фильтр, чтобы выбрать только записи с нужным месяцем и годом
        try:
            lessons = session.query(LessonsDays).filter(
                extract('year', LessonsDays.selected_date) == year,
                extract('month', LessonsDays.selected_date) == month).all()

            # Заполняем словарь результатами запроса
            for lesson in lessons:
                results_dict[str(lesson.selected_date)] = str(lesson.confirmed_state)

            # Сортируем по возрастанию
            results_dict_sorted = dict(sorted(results_dict.items()))

            return 200, results_dict_sorted
        except Exception as e:
            return 500, e
