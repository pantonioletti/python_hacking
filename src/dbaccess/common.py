#coding=ISO_8859-1
#UTF-8
import cx_Oracle

class RowIterator:
    def __init__(self, cursor):
        self.cur = cursor
        
    def next(self):
        row = self.cur.fetchone()
        if row is None:
            self.cur.close()
        return row
        
    def retrieveAll(self):
        all = self.cur.fetchall()
        self.cur.close()
        return all

class Cursor:
    def __init__(self, cur):
        self.__cursor = cur
        self.__iterator = None 
    def execute(self, sql):
        self.__cursor.execute(sql)
        self.__iterator = RowIterator(self.__cursor)
        return self.__iterator 
    def fecthone(self):
        if (self.__iterator is not None):
            return self.__iterator.next()
    def fetchall(self):
        ret = None
        if (self.__iterator is not None):
            ret = self.__iterator.retrieveAll()
        return ret
    def close(self):
        self.__cursor.close()

class Connection:
    def __init__(self, user, passwd, service):
        self.user = user
        self.passwd = passwd
        self.service = service
        self.conn = None
        
    def __buildConnStr(self):
        return self.user + "/" + self.passwd + "@" + self.service

    def openConn(self):
        self.conn = self.__openConn(self.__buildConnStr())

    def __openConn(self,connStr):
        db = cx_Oracle.connect(connStr)
        return db
    
    def getCursor(self):
        cursor = self.conn.cursor()
        return cursor

    def close(self):
        self.conn.close()
    
    def execute(self, sql):
        cur=self.getCursor()
        return cur.execute(sql)


def getConnection(connType, target):
    if connType=='JAVA':
        from com.ziclix.python.sql import zxJDBC
        conn = zxJDBC.connect("jdbc:oracle:thin:@//cl1csgdev01:1521/wfmfala", "ewmuser", "ewmuser", "oracle.jdbc.driver.OracleDriver")
    elif connType=='CPYTHON':
        user = ""
        passwd = ""
        conn_str=""
        if target == "WFMFALA_PROD":
            user="uewmuser"
            passwd="orauewmuser"
            conn_str="wfmfala_prod"
        elif target == "WFMFALA_TEST":
            user="ewmuser"
            passwd="ewmuser"
            conn_str="wfmfala_test"
        elif target == "WFMFALA":
            user="ewmuser"
            passwd="ewmuser"
            conn_str="wfmfala"
        elif target == "WFMFALAPE":
            user="ewmuser"
            passwd="ewmuser"
            conn_str="wfmfalape"
        else:
            print("DB connection target should be one of: ")
            print("    WFMFALAPE    | ")
            print("    WFMFALA_PROD | ")
            print("    WFMFALA_TEST | ")
            print("    WFMFALA")
        import cx_Oracle
        conn = cx_Oracle.connect(user,passwd,conn_str)
    else:
        print("ERROR the second parameter should be JAVA or CPYTHON")
        exit()
    return conn
