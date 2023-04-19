# модель таблицы для бд
import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class OrmGoods(SqlAlchemyBase):
    __tablename__ = 'allgoods'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True,
                           autoincrement=True)  # просто номер строки в бд
    chat_id = sqlalchemy.Column(sqlalchemy.Integer)  # в каком чате добавляется товар
    articul_good = sqlalchemy.Column(sqlalchemy.Integer)  # артикул товара
    name_good = sqlalchemy.Column(sqlalchemy.Text)  # название товара
    price_good = sqlalchemy.Column(sqlalchemy.Integer)  # цена товара на данный момент
    price_to_look = sqlalchemy.Column(sqlalchemy.Integer)  # цена за которой надо следить

    def __repr__(self):
        return f'Товар номер {self.id}\n' \
               f'{self.name_good}. Артикул: {self.articul_good}.\n' \
               f'Цена: {self.price_good}\n' \
               f'Желаемая цена: {self.price_to_look}'
