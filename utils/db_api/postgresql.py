from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config
import json


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def _init_connection(self, conn):
        await conn.set_client_encoding('UTF8')  # Bu qator qo'shilgan

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
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

    async def create_table_postbot_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS postbot_users (
        id SERIAL PRIMARY KEY,
        users_language varchar(5) NOT NULL,
        fullname varchar(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_postbot_users(self, users_language, fullname, telegram_id):
        sql = "INSERT INTO postbot_users (users_language, fullname, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, users_language, fullname, telegram_id,
                                  fetchrow=True)

    async def select_all_postbot_users(self):
        sql = "SELECT * FROM postbot_users"
        return await self.execute(sql, fetch=True)

    async def select_postbot_users(self, **kwargs):
        sql = "SELECT * FROM postbot_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_postbot_users(self):
        sql = "SELECT COUNT(*) FROM postbot_users"
        return await self.execute(sql, fetchval=True)

    async def update_user_language_postbot_users(self, new_lang, telegram_id):
        sql = "UPDATE postbot_users SET users_language=$1 WHERE telegram_id=$2"
        return await self.execute(sql, new_lang, telegram_id, execute=True)

    async def delete_postbot_users(self):
        await self.execute("DELETE FROM postbot_users WHERE TRUE", execute=True)

    async def drop_postbot_users(self):
        await self.execute("DROP TABLE postbot_users", execute=True)

    async def see_postbot_users(self, tg_id):
        sql = "SELECT * FROM postbot_users WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetchrow=True)

    #lang tekshirish
    async def check_lang_postbot_users(self, telegram_id):
        sql = "SELECT users_language FROM postbot_users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)

    ##posts
    async def create_table_postbot_posts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS postbot_posts (
        id SERIAL PRIMARY KEY,
        post_type varchar(50) NOT NULL,
        post_content TEXT NOT NULL,
        post_caption TEXT,
        buttons JSONB,
        telegram_id BIGINT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, execute=True)


    async def add_postbot_post(self, post_type, post_content, post_caption, buttons, telegram_id):
        buttons_json = json.dumps(buttons)

        sql = """
        INSERT INTO postbot_posts (post_type, post_content, post_caption, buttons, telegram_id)
        VALUES ($1, $2, $3, $4, $5) 
        RETURNING id
        """
        return await self.execute(sql, post_type, post_content, post_caption, buttons_json, telegram_id, fetchval=True)

    async def get_count_posts_bot(self):
        sql = "SELECT COUNT(*) FROM postbot_posts"
        return await self.execute(sql, fetchval=True)

    async def get_postbot_post_by_id(self, post_id):
        sql = "SELECT * FROM postbot_posts WHERE id = $1"
        return await self.execute(sql, post_id, fetchrow=True)

    async def select_all_postbot_posts(self):
        sql = "SELECT * FROM postbot_posts"
        return await self.execute(sql, fetch=True)

    async def delete_postbot_post(self, post_id):
        sql = "DELETE FROM postbot_posts WHERE post_id = $1"
        return await self.execute(sql, post_id, execute=True)


    async def drop_table_postbot_post(self):
        await self.execute("DROP TABLE postbot_posts", execute=True)

    async def get_post_by_id(self, post_id):
        sql = "SELECT * FROM postbot_posts WHERE id = $1"
        return await self.execute(sql, post_id, fetchrow=True)

    async def get_post_by_idtg_id(self, post_id, tg_id):
        sql = "SELECT * FROM postbot_posts WHERE id=$1 AND telegram_id=$2"
        return await self.execute(sql, post_id, tg_id, fetchrow=True)

    #saqlangan post

    async def create_table_postbot_posts_saves(self):
        sql = """
              CREATE TABLE IF NOT EXISTS postbot_posts_saves (
              id SERIAL PRIMARY KEY,
              post_name VARCHAR(50) NOT NULL,
              post_id BIGINT NOT NULL,
              telegram_id BIGINT NOT NULL
              );
              """
        await self.execute(sql, execute=True)

    async def add_postbot_post_saves(self, post_name, post_id, telegram_id):
        sql = """
              INSERT INTO postbot_posts_saves (post_name, post_id, telegram_id)
              VALUES ($1, $2, $3) 
              RETURNING id
              """
        return await self.execute(sql, post_name, post_id, telegram_id, fetchval=True)

    async def get_postbot_post_by_id_saves(self, post_id):
        sql = "SELECT * FROM postbot_posts_saves WHERE post_id = $1"
        return await self.execute(sql, post_id, fetchrow=True)

    async def select_all_postbot_posts_saves(self):
        sql = "SELECT * FROM postbot_posts_saves"
        return await self.execute(sql, fetch=True)

    async def delete_postbot_post_saves(self, post_id):
        sql = "DELETE FROM postbot_posts_saves WHERE post_id = $1"
        return await self.execute(sql, post_id, execute=True)

    async def drop_table_postbot_post_saves(self):
        await self.execute("DROP TABLE postbot_posts_saves", execute=True)

    async def get_post_by_id_saves(self, post_id):
        sql = "SELECT * FROM postbot_posts_saves WHERE post_id = $1"
        return await self.execute(sql, post_id, fetch=True)

    async def get_posts_tg_id(self, tg_id):
        sql = "SELECT * FROM postbot_posts_saves WHERE telegram_id = $1"
        return await self.execute(sql, tg_id, fetch=True)

    async def delete_post_by_id(self, post_id, tg_id):
        sql = "DELETE FROM postbot_posts_saves WHERE post_id = $1 AND telegram_id = $2"
        return await self.execute(sql, post_id, tg_id, execute=True)