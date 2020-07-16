from sqlalchemy import Column, Integer, BigInteger, String, Sequence, Boolean
from sqlalchemy import sql
from gino import Gino
from gino.schema import GinoSchemaVisitor
from aiogram import types
from gino.dialects.asyncpg import NullPool
from data.config import DB_NAME, DB_HOST

db = Gino()


class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(50))
    is_active = Column(Boolean, default=False)


class OrderList(db.Model):
    __tablename__ = 'order_list'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(50))
    quantity = Column(Integer)


class DBCommands:
    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username

        await new_user.create()
        return new_user

    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def get_all_users(self):
        users = await User.query.gino.all()
        return users

    async def get_quantity_order(self):
        order_list = await OrderList.query.gino.all()
        quantity = 0
        for order in order_list:
            quantity += order.quantity
        return quantity

    async def add_new_order(self, quantity):
        user = types.User.get_current()
        new_order = OrderList()
        new_order.user_id = user.id
        new_order.username = user.username
        new_order.quantity = quantity
        await new_order.create()
        return new_order

    async def clean_order_list(self):
        await OrderList.delete.gino.all()


async def create_db():
    await db.set_bind(f'postgresql://{DB_HOST}/{DB_NAME}', pool_class=NullPool)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
