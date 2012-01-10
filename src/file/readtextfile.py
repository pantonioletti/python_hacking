def readfile(input):
    dcode = None
    dval = None
    try:
        fd = open(input, 'r')
        str = fd.readline()
        sequence = 1
        while(len(str) != 0):
            if (str.find("values (") != -1):
                nstr = str.replace("'#seq#'",sequence.__str__())
                print(nstr)
                sequence = sequence + 1
            else:
                print(str)
            str = fd.readline()
        fd.close()
    except IOError:
        print( "File ", input, " not found")
    
