import mysql.connector

from infra.log import Log
from settings import DB_SETTINGS


class DataBase():
    def __init__(self, table, env='development'):
        self.__table = table
        self.__env = env
        self.mydb = None
        self.mycursor = None
        # if env == "development":
        #     print("[INFO] DEVELOPMENT DB!")
        self.connect()
        

    def __del__(self):
        self.commit()

    def reconnect(self):
        try:
            self.__conf = DB_SETTINGS[self.__env]
        except:
            raise (Exception("Configurações não encontradas!"))
        # Log(f"DB Connect for host => {self.__conf.get('host')}")
        self.mydb = mysql.connector.connect(
            host=self.__conf.get('host'),
            port=self.__conf.get('port'),
            user=self.__conf.get('user'),
            passwd=self.__conf.get('passwd'),
            database=self.__conf.get('database'))
        self.mycursor = self.mydb.cursor()
        # Log("Success connect!")

    def connect(self):
        try:
            if (not self.mydb or not self.mycursor
                    or not self.mydb.is_connected()):
                self.reconnect()
        except Exception as e:
            raise (e)

    def close(self):
        try:
            print("DB Closed...")
            self.mydb.close()
        except Exception as e:
            raise (e)

    def commit(self):
        try:
            self.mydb.commit()
        except Exception as e:
            raise (e)

    def rollback(self):
        try:
            self.mydb.rollback()
        except Exception as e:
            raise (e)

    def lock_table(self, read_op=False, write_op=True):
        try:
            if (read_op):
                self.mycursor.execute(f"LOCK TABLES {self.__table} READ")
            if (write_op):
                self.mycursor.execute(f"LOCK TABLES {self.__table} WRITE")
        except Exception as e:
            raise (e)

    def unlock_table(self):
        try:
            self.mycursor.execute(f"UNLOCK TABLES")
        except Exception as e:
            raise (e)

    def asDic(self, cursor, first=False):
        """Retorna o resultado do cursor como um dicionário"""
        try:
            descriptions = [x[0] for x in cursor.description]
            result = cursor.fetchone()
            data = []
            while result != None:
                dic = {}
                for i in range(len(descriptions)):
                    dic[descriptions[i]] = str(
                        result[i] if result[i] != None else "")
                data.append(dic)
                result = cursor.fetchone()
            self.mydb.commit()
            if (first):
                return data[0]
            else:
                return data
        except Exception as e:
            return {}

    def select(self,
               staments="*",
               where=None,
               groupby=None,
               first=False,
               orderby=None,
               dic=True,
               limit=None,
               offset=None,
               table_as=None):
        """Executa select no banco de dados (table=tabela, staments=colunas, where=dados)"""

        try:
            self.connect()
            tb = self.__table
            if (table_as):
                tb += f" as {table_as}"

            sql = "SELECT %s FROM %s " % (staments, tb)
            if where:
                sql += '''WHERE %s''' % (where)
            if groupby != None:
                sql += " GROUP BY %s" % (groupby)
            if orderby != None:
                sql += " ORDER BY %s" % (orderby)
            if limit != None:
                sql += " LIMIT %s" % (limit)
            if offset != None:
                sql += f" OFFSET {offset}"
            # print(sql)
            cur = self.mydb.cursor()
            cur.reset()
            cur.execute(sql)
            if dic:
                return self.asDic(cur, first)
            else:
                return cur.fetchall()
        except Exception as e:
            print(e)
            return []

    def count(self, where=None):
        try:
            self.connect()
            sql = f"SELECT COUNT(*) AS total FROM {self.__table}"
            if where:
                sql += f" WHERE {where}"
            # print(sql)
            cur = self.mydb.cursor()
            cur.reset()
            cur.execute(sql)
            return self.asDic(cur, True)['total']
        except Exception as e:
            raise (e)

    def insert(self, obj):
        """Insere dados em uma tabela (table=tabela, obj=dicionario de itens para inserir (key=column,value=value))"""
        try:
            self.connect()
            sql = '''INSERT INTO %s (%s) VALUES("%s")''' % (
                self.__table, ",".join(
                    [x for x in obj.keys() if obj[x]]), '''","'''.join(
                        str(x).replace("'", "").replace("\"", "")
                        for x in obj.values() if x))
            sql = sql.replace("''", "NULL").replace("'None'", "NULL")
            # print(sql)
            self.mycursor.execute(sql)
            # self.mydb.commit()
            # self.commit()
            if self.mycursor.rowcount > 0:
                return self.mycursor.lastrowid
            else:
                return None
        except Exception as e:
            self.rollback()
            print(e)
            raise (e)

    def update(self, obj, conditions, specialset=None):
        """Atualiza os dados em uma tabela (table=tabela, obj=dicionario de itens para inserir (key=column,value=value))"""
        try:
            self.connect()
            sql = "UPDATE %s " % (self.__table)
            staments = []
            if len(obj.keys()) > 0:
                sql += "SET "
            for i in obj.keys():
                if (obj[i]):
                    staments.append(i + "='" + str(obj[i]) + "'")
            if (specialset):
                staments.append(f"{specialset}")

            sql += ",".join(staments)
            sql += " where %s" % (conditions)
            # print(sql)
            self.mycursor.execute(sql)
            # self.commit()
            return self.mycursor.rowcount > 0
        
        except Exception as e:
            self.rollback()
            raise (e)
        
    def sendSql(self, sql):
        """Atualiza os dados em uma tabela (table=tabela, obj=dicionario de itens para inserir (key=column,value=value))"""
        try:
            self.connect()
            # print(sql)
            self.mycursor.execute(sql)
            # self.commit()
            return self.mycursor.rowcount > 0
        
        except Exception as e:
            self.rollback()
            raise (e)

    def delete(self, where):
        sql = "delete from %s where %s" % (self.__table, where)
        # print(sql)
        try:
            self.connect()
            self.mycursor.execute(sql)
            # self.mydb.commit()
            self.commit()
            return self.mycursor.rowcount > 0
        except Exception as e:
            raise (e)

    def clear(self):
        sql = "delete from %s" % (self.__table)
        # print(sql)
        try:
            self.connect()
            self.mycursor.execute(sql)
            # self.mydb.commit()
            self.commit()
            return self.mycursor.rowcount > 0
        except Exception as e:
            raise (e)

    @property
    def columns(self):
        try:
            sql = f"describe {self.__table}"
            cur = self.mydb.cursor()
            cur.reset()
            cur.execute(sql)
            res = self.asDic(cur, False)
            return [r['Field'] for r in res]
        except Exception as e:
            print(f'[ERROR] => {e}')
            return []
    
    @property
    def index(self):
        try:
            sql = f"show index from {self.__table} where Key_name = 'PRIMARY' ;"
            cur = self.mydb.cursor()
            cur.reset()
            cur.execute(sql)
            res = self.asDic(cur, False)
            # print([r['Column_name'] for r in res])
            return [r['Column_name'] for r in res]
        except Exception as e:
            print(f'[ERROR] => {e}')
            return []

    @property
    def tables(self):
        try:
            sql = f"SHOW TABLES"
            cur = self.mydb.cursor()
            cur.reset()
            cur.execute(sql)
            res = self.asDic(cur, False)
            return [list(r.values())[0] for r in res]
        except Exception as e:
            print(f'[ERROR] => {e}')
            return []

    def executeMigration(self, initial_fila="./migrations/migrations.sql"):
        try:
            self.connect()
            Log(f"Execute migrate...")
            db_sql = []
            with open(initial_fila, 'r') as f:
                txt = f.read()
                db_sql = txt.split(";")
            for sql in db_sql:
                if sql.strip():
                    try:
                        self.mycursor.execute(sql)
                    except Exception as e:
                        Log(f"Error => {str(e)}\nSQL => {sql}", "ERROR")
            self.commit()
            Log(f"Migrate executed!")
        except Exception as e:
            self.rollback()
            print(f"Error => {str(e)}")
