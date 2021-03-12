from sqlalchemy import Table, Column, Integer, String
from aiomysql.sa.connection import SAConnection

from db import metadata

user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(15), index=True, unique=True),
    Column("password", String(128)),
    Column("image", String(45), nullable=True),
)


async def get_user_by_username(conn: SAConnection, username: str) -> dict:
    user_query = user_table.select().where(user_table.c.username == username)
    user_row = await conn.fetch_one(query=user_query)

    if user_row:
        user_dict = dict(user_row)
    else:
        return {}

    return user_dict
