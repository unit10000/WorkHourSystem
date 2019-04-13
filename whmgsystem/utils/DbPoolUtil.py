# -*- coding:utf-8 -*-

from DBUtils.PooledDB import PooledDB
import importlib
from whmgsystem.syslog import systemlog
from whmgsystem.conf import setting
from whmgsystem.model.jindee import Jindee
import copy
class DbPoolUtil(object):
    def __init__(self,config):

        self.__db_type = "sqlserver"
        if self.__db_type == "mysql":
            db_creator = importlib.import_module("pymysql")
            self.__pool = PooledDB(db_creator, maxcached=50, maxconnections=1000, maxusage=1000, **config)

        elif self.__db_type == "sqlserver":
            config = config
            db_creator = importlib.import_module("pymssql")
            self.__pool = PooledDB(db_creator, maxcached=50, maxconnections=1000, maxusage=1000, **config)
        else:
            raise Exception("unsupported database type " + self.__db_type)
    def execute_query(self, sql, args=()):
        """
        执行查询语句，获取结果
        :param sql:sql语句，注意防注入
        :param args:传入参数
        :return:结果集
        """
        result = ()
        conn = self.__pool.connection()
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        try:
            cur.execute(sql, args)
            fields = [desc[0] for desc in cur.description]
            result = cur.fetchall()
            if result:
                result = [dict(zip(fields, row)) for row in result]
        except Exception as e:
            systemlog.log_error(e)
            print('异常信息:' + str(e))
        cur.close()
        conn.close()
        return result

    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    def execute_query_single(self, sql, args=()):
        """
        执行查询语句，获取单行结果
        :param sql:sql语句，注意防注入
        :param args:传入参数
        :return:结果集
        """
        result = ()
        conn = self.__pool.connection()
        conn.row_factory = self.dict_factory
        cur = conn.cursor()
        try:
            cur.execute(sql, args)
            result = cur.fetchone()
        except Exception as e:
            systemlog.log_error(e)
            print('异常信息:' + str(e))
        cur.close()
        conn.close()
        return result

    def execute_iud(self, sql, args=()):
        """
        执行增删改语句
        :param sql:sql语句，注意防注入
        :param args:传入参数
        :return:影响行数,mysql和sqlite有返回值
        """
        conn = self.__pool.connection()
        cur = conn.cursor()
        count = 0
        try:
            result = cur.execute(sql, args)
            conn.commit()
            if self.__db_type == "mysql":
                count = result
            if self.__db_type == "sqlite3":
                count = result.rowcount
        except Exception as e:
            systemlog.log_error(e)
            print('异常信息:' + str(e))
            conn.rollback()
        cur.close()
        conn.close()
        return count
    def execute_many_iud(self, sql, args):
        """
        批量执行增删改语句
        :param sql:sql语句，注意防注入
        :param args:参数,内部元组或列表大小与sql语句中参数数量一致
        :return:影响行数，mysql和sqlite有返回值
        """
        conn = self.__pool.connection()
        cur = conn.cursor()
        count = 0
        try:
            result = cur.executemany(sql, args)
            conn.commit()
            if self.__db_type == "mysql":
                count = result
            if self.__db_type == "sqlite3":
                count = result.rowcount
        except Exception as e:
            systemlog.log_error(e)
            print('异常信息:' + str(e))
            conn.rollback()
        cur.close()
        conn.close()
        return count
    def getConn(self):
        return self.__pool.connection()
# 获取实例，保持单例
def get_dbpool(jindee_id):
    try:
        db = setting.dbpool_jindee[jindee_id]
    except:
        print("未发金蝶数据库")
        jindee = Jindee.query.get(int(jindee_id))
        if jindee:
            print("初始化金蝶数据库")
            config = {
                'host': jindee.DBAddress,
                'database': jindee.DBName,
                'user': jindee.userName,
                'password': jindee.userPw,
                'charset': "utf8"
            }
            db = DbPoolUtil(config)
            setting.dbpool_jindee[jindee_id] = db
        else:
            print("未配置金蝶数据库")
            db = None
    return db
#dbpool_quanjie = DbPoolUtil(quanjie_config)
if __name__ == "__main__":
    # 使用demo，工作目录在项目目录的前提下,使用表为TEST2表
    # from util.DBUtil import dbpool_util
    sql1 = """SELECT * FROM t_ICItem WHERE FModel like '%CBM1%' """
    #result1 = dbpool_shibian.execute_query(sql1)
    #print(result1)