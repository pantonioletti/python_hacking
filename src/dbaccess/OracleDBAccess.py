import cx_Oracle
from dbaccess.common import RowIterator

class OracleDBAccess:
    def __init__(self, user, passwd, service):
        #self.str = self.buildConnStr(user, passwd, service)
        self.user = user
        self.passwd = passwd
        self.servcice = service
        self.db = self.openConn()
    
    def buildConnStr(self,user, passwd, service):
        return user + "/" + passwd + "@" + service

    def openConn(self):
        db = cx_Oracle.connect(self.user, self.passwd, self.servcice)
        return db
    
    def getConn(self):
        return self.db
    
    def executeQuery(self, sql):
        cur = self.db.cursor()
        cur.execute(sql)
        return RowIterator(cur)
    
    def close(self):
        self.db.close()

    def begin(self):
        self.db.begin()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
        