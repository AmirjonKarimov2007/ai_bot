from datetime import datetime, timedelta
from datetime import timedelta

import asyncpg
from asyncpg import Connection, Record
from asyncpg.pool import Pool
from typing import Union
from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT,
        )

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


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${index + 1}" for index, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def stat(self):
        return await self.execute(f"SELECT COUNT(*) FROM users_user;", fetchval=True)

    async def add_admin(self, user_id: str, full_name: str):
        sql = """
            INSERT INTO Admins( user_id, full_name ) VALUES($1, $2)
            """
        await self.execute(sql, user_id, full_name, execute=True)
        
    async def is_user(self, **kwargs):
        sql = "SELECT * FROM users_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        # Convert user_id to integer
        parameters = tuple(int(param) if param == 'user_id' else param for param in parameters)

        return await self.execute(sql, *parameters, fetch=True)
    async def add_user(self, name, username, user_id, balance=0, number=None, ref_father=None, register=False):
        if username:
            if not (username[-3:] == "bot" or username[-3:] == "Bot"):
                sql = """
                    INSERT INTO users_user (name, username, user_id, balance, number, ref_father, register)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    RETURNING *
                """
                return await self.execute(sql, name, username, user_id, balance, number, ref_father, register, fetchrow=True)
            else:
                pass
        else:
            sql = """
                INSERT INTO users_user (name, username, user_id, balance, number, ref_father, register)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
            """
            return await self.execute(sql, name, username, user_id, balance, number, ref_father, register, fetchrow=True)



    async def count_referred_users(self, ref_father):
        sql = """
            SELECT COUNT(*) FROM users_user WHERE ref_father = $1
        """
        return await self.execute(sql, ref_father, fetchval=True)
    async def get_top_users(self):
        sql = """
            SELECT name, username, balance
            FROM users_user
            ORDER BY balance DESC
            LIMIT 10
        """
        return await self.execute(sql, fetch=True)


    async def is_admin(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        # Convert user_id to string
        parameters = tuple(str(param) for param in parameters)

        return await self.execute(sql, *parameters, fetch=True)
        
    async def update_user_number(self, number, user_id, register=True):
        sql = "UPDATE users_user SET number=$1, register=$2 WHERE user_id=$3"
        return await self.execute(sql, number, register, user_id, execute=True)
    async def update_balance(self, user_id, sum):
        sql = "UPDATE users_user SET balance = balance + $1 WHERE user_id = $2"
        return await self.execute(sql, sum, user_id, execute=True)
    
    async def update_balances(self, user_id, sum):
        sql = "UPDATE users_user SET balance=$1 WHERE user_id = $2"
        return await self.execute(sql, sum, user_id, execute=True)
    

    async def select_all_users(self):
        sql = """
        SELECT * FROM users_user
        """
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return await self.execute(sql, *parameters, fetch=True)
    async def select_user_balance(self, **kwargs):
        sql = "SELECT balance FROM users_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        
        return await self.execute(sql, *parameters, fetch=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM users_user;", fetchval=True)
    
    async def delete_users(self):
        await self.execute("DELETE FROM users_user", execute=True)

    async def create_table_files(self):
        sql = """
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            type TEXT,
            file_id TEXT,
            caption TEXT,
            user_id INTEGER
            );
        """
        await self.execute(sql, execute=True)

    async def add_files(self, type: str=None, file_id: str=None, caption: str = None, user_id: str =None):
        sql = """
        INSERT INTO files(type, file_id, caption, user_id) VALUES($1, $2, $3, $4)
        """
        await self.execute(sql, type, file_id, caption, user_id, execute=True)

    async def select_files(self, **kwargs):
        sql = " SELECT * FROM files WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return await self.execute(sql, *parameters, fetch=True)

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL UNIQUE ,
            full_name TEXT
            );
        """
        await self.execute(sql, execute=True)

    async def add_admin(self, user_id: int, full_name: str):
        sql = """
            INSERT INTO Admins( user_id, full_name ) VALUES($1, $2)
            """
        await self.execute(sql, user_id, full_name, execute=True)

    async def select_all_admins(self):
            sql = """
            SELECT * FROM Admins
            """
            return await self.execute(sql, fetch=True)



        
    async def is_admin(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_admin(self, **kwargs):
            sql = "SELECT * FROM Admins WHERE "
            sql, parameters = self.format_args(sql, kwargs)

            return await self.execute(sql, *parameters, fetch=True)
        
    async def stat_admins(self):
        return await self.execute(f"SELECT COUNT(*) FROM Admins;", fetchval=True)

    async def delete_admin(self, admin_id):
        await self.execute("DELETE FROM Admins WHERE user_id=$1", admin_id, execute=True)

    async def select_admins(self):
        sql = "SELECT * FROM Admins WHERE TRUE"
        return await self.execute(sql, fetch=True)

        return await self.execute(sql, *parameters, fetch=True)

    async def create_table_channel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
            id SERIAL PRIMARY KEY,
            channel TEXT
            );
        """
        await self.execute(sql, execute=True)

    async def add_channel(self, channel: str):
        sql = """
            INSERT INTO Channels(channel) VALUES($1)
            """
        await self.execute(sql, channel, execute=True)

    async def check_channel(self, channel):
        return await self.execute("SELECT channel FROM Channels WHERE channel=$1", channel, fetchval=True)
    async def channel_stat(self):
        return await self.execute(f"SELECT COUNT(*) FROM Channels;", fetchval=True)

    async def select_channels(self):
        return await self.execute("SELECT * FROM Channels", fetch=True)

    async def select_all_channels(self):
        return await self.execute("SELECT * FROM Channels", fetch=True)

    async def delete_channel(self, channel):
        return await self.execute("DELETE FROM Channels WHERE channel=$1", channel, execute=True)



# Promokodlar

    async def add_promocode(self, user_id, promo_code, package, status, created_at):
        if isinstance(created_at, datetime):
            end_date = created_at + timedelta(days=15)  # Amal qilish muddati 15 kun
        else:
            raise ValueError("created_at must be a datetime object")
        
        sql = """
            INSERT INTO users_promocode (user_id, promo_code, package, status, created_at, end_date) 
            VALUES($1, $2, $3, $4, $5, $6)
        """
        await self.execute(sql, user_id, promo_code, package, status, created_at, end_date, execute=True)

    async def select_promocode(self, **kwargs):
        sql = "SELECT * FROM users_promocode WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        
        parameters = tuple(int(param) if param == 'promo_code' else param for param in parameters)

        return await self.execute(sql, *parameters, fetch=True)
    
    async def delete_promo_code(self, promo_code):
        return await self.execute("DELETE FROM users_promocode WHERE promo_code=$1", promo_code, execute=True)