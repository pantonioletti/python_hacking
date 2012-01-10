from com.ziclix.python.sql import zxJDBC
import java.sql.Connection
import java.sql.Statement
import java.sql.ResultSet
import java.sql.SQLException

class JDBCConnection:
    def __init__(self, connURL, user, passwd, driver):
        self.connUrl = connURL
        self.db = zxJDBC.connect(self.connUrl, user, passwd, driver)
        
    def getConn(self):
        return self.db   
        
    def close(self):
        self.db.close()
        return