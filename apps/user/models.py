import pymysql
from dbutils.pooled_db import PooledDB
import threading

lock = threading.Lock()


class MysqlPOOL:

    def __init__(self):
        self.POOL = PooledDB(
            creator=pymysql,
            maxconnections=50,
            mincached=20,
            maxcached=30,
            maxshared=20,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=1,
            database="hll",
            host='106.14.26.159',
            port=3306,
            user='hucheng',
            passwd='hu697693',
            charset='utf8mb4',
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            print("不存在")
            cls._instance = super().__new__(cls, *args, **kwargs)
        else:
            print("存在")
        return cls._instance

    def _connect(self):
        con = self.POOL.connection()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        return con, cursor

    def query_one(self, sql):
        con, cursor = self._connect()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(e)
        finally:
            self._connect_close(con, cursor)

    def _connect_close(self, con, cursor):
        cursor.close()
        con.close()


my_db = MysqlPOOL()
