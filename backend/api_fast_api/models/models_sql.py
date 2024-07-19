from typing import Dict, Union

from sqlalchemy.orm import sessionmaker, attributes, declarative_base
from sqlalchemy import create_engine

from api_fast_api.config import SQLALCHEMY_DATABASE_URL
from api_fast_api.models.asinc_models import UsersSql

# Создаем экземпляр класса Engine для соединения с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
# Создаем экземпляр базового класса
Base = declarative_base()


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
            print("Ошибка БД:", str(e))
            return {"error": str(e)}

