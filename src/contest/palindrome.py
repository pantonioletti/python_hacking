import StirngIO

class parser:
    def init(self):
        pass
        
    def parseFile(self,  filename):
        try:
            text = StringIO.StringIO()
            
            fd = open(filename, 'r')
            str = fd.readline()
            while(len(str) != 0):
                for i in range(0, len(str)):
                    chr =   str[i]
                    chr.capwords()
                str = fd.readline()
            fd.close()
        except IOError:
            print( "File ", input, " not found")
    #def parse(self):
    #    for i in range()
        
