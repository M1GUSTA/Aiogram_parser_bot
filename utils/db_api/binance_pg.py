from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config



class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def insert_transaction(self, symbol, type, price, sum, id_bill):
        try:
            sql = 'INSERT INTO transactions ("Symbol", type, price, sum, "ID_schet") ' \
              'VALUES($1, $2, $3, $4, $5) returning *'
            return await self.execute(sql, symbol, type, price, sum, id_bill, fetchrow=True)
        except Exception as ex:
            print(ex)