from pydantic import BaseModel, Field
import typing
import pymysql
from pymysql import DatabaseError


class DBConfig(BaseModel):
    host: str = Field(..., description="host")
    port: typing.Union[int, str] = Field(..., description="port")
    user: str = Field(..., description="user")
    password: str = Field(..., description="port")
    database: typing.Optional[str] = Field(None, description="database")
    read_timeout: int = Field(None, description="read_timeout")
    charset: str = Field("UTF8MB4", description="charset")


class DB:
    def __init__(self, config: DBConfig):
        self.config = config
        self.connect = self.db_connect()
        self.cursor = self.db_cursor()

    def db_connect(self):
        try:
            connect = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                read_timeout=self.config.read_timeout,
                charset=self.config.charset
            )
        except DatabaseError as err:
            raise Exception('数据库连接错误：', err)
        return connect

    def db_cursor(self):
        return self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def close(self):
        self.cursor.close()
        self.connect.close()

    def execute(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # self.close()
        return data

    def __del__(self):
        self.close()
