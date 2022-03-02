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

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id, full_name, username):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username = $1 WHERE telegram_id = $2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    async def create_table_vkposts(self):
        sql = """
           CREATE TABLE IF NOT EXISTS VK_posts (
           id SERIAL PRIMARY KEY, 
           group_id VARCHAR(255) NOT NULL,
           group_name VARCHAR(255) NOT NULL,
           last_known_id VARCHAR(255) NULL
           );
           """
        await self.execute(sql, execute=True)

    async def update_last_known_id(self, last_known_id, group_id):
        sql = "UPDATE VK_posts SET last_known_id = $1 WHERE group_id = $2"
        return await self.execute(sql, last_known_id, group_id, execute=True)

    async def drop_vk_posts(self):
        await self.execute("DROP TABLE VK_posts", execute=True)

    async def get_last_known_id(self):
        sql = "SELECT last_known_id, group_id FROM vk_posts"
        return await self.execute(sql, fetch=True)


    async def get_group_ids(self):
        sql = "SELECT group_id FROM vk_posts"
        return await self.execute(sql, fetch=True)

    async def create_table_sources(self):
        sql = """
           CREATE TABLE IF NOT EXISTS Available_sources (
           id SERIAL PRIMARY KEY, 
           domain VARCHAR(255) NOT NULL,
           name VARCHAR(255) NOT NULL
           );
           """
        await self.execute(sql, execute=True)

    async def add_source(self, domain, name):
        sql = "INSERT INTO Available_sources (domain, name) VALUES($1, $2) returning *"
        return await self.execute(sql, domain, name, fetchrow=True)

    async def drop_table_sources(self):
        await self.execute("DROP TABLE Available_sources", execute=True)

    async def select_all_domains(self):
        sql = "SELECT domain FROM Available_sources"
        return await self.execute(sql, fetch=True)