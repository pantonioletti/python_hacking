import array
WORD=2
HEXB=16

ERR_LEN = 'Unexpected file length'
'''
Estructura de archivo *.lnk (acceso directo)

+--------------------------------------------------+
|             .LNK File Header                     |
+------+-----------+-------------------------------+
|Offset| Size/Type |          Contents             |
+------+-----------+-------------------------------+
|0h    | 1 dword   | Always 0000004Ch ‘L’          |
+------+-----------+-------------------------------+
|4h    |16 bytes   | GUID of shortcut files        |
+------+-----------+-------------------------------+
|14h   | 1 dword   | Flags                         |
+------+-----------+-------------------------------+
|18h   | 1 dword   | File attributes               |
+------+-----------+-------------------------------+
|1Ch   | 1 qword   | Time 1                        |
+------+-----------+-------------------------------+
|24h   | 1 qword   | Time 2                        |
+------+-----------+-------------------------------+
|2Ch   | 1 qword   | Time 3                        |
+------+-----------+-------------------------------+
|34h   | 1 dword   | File length                   |
+------+-----------+-------------------------------+
|38h   | 1 dword   | Icon number                   |
+------+-----------+-------------------------------+
|3Ch   | 1 dword   | ShowWnd value                 |
+------+-----------+-------------------------------+
|40h   | 1 dword   | Hot key                       |
+------+-----------+-------------------------------+
|44h   | 2 dwords  | Unknown, always zero          |
+------+-----------+-------------------------------+


+-----------------------------------------------------------------------------+
|                                The flags                                    |
+------+-----------------------------------+----------------------------------+
| Bit  |          Meaning when 1           |       when 0                     |
+------+-----------------------------------+----------------------------------+
| 0    | The shell item id list is present.| The shell item id list is absent.|
+------+-----------------------------------+----------------------------------+
| 1    | Points to a file or directory.    |  Points to something else.       |
+------+-----------------------------------+----------------------------------+
| 2    |Has a description string.          |  No description string.          |
+------+-----------------------------------+----------------------------------+
| 3    | Has a relative path string.       | No relative path.                |
+------+-----------------------------------+----------------------------------+
| 4    | Has a working directory.          |  No working directory.           |
+------+-----------------------------------+----------------------------------+
| 5    |  Has command line arguments.      | No command line arguments.       |
+------+-----------------------------------+----------------------------------+
| 6    | Has a custom icon.                |  Has the default icon.           |
+------+-----------------------------------+----------------------------------+

  
+-------------------------------------------------------------+
|                          File Attributes                                    |
+------+------------------------------------------------------+
| Bit  |                  Meaning when set                    |
+------+------------------------------------------------------+
| 0    | Target is read only.                                 |
+------+------------------------------------------------------+
| 1    | Target is hidden.                                    |
+------+------------------------------------------------------+
| 2    | Target is a system file.                             |
+------+------------------------------------------------------+
| 3    | Target is a volume label. (Not possible)             |
+------+------------------------------------------------------+
| 4    | Target is a directory.                               |
+------+------------------------------------------------------+
| 5    | Target has been modified since last backup. (archive)|
+------+------------------------------------------------------+
| 6    | Target is encrypted (NTFS EFS)                       |
+------+------------------------------------------------------+
| 7    | Target is Normal??                                   |
+------+------------------------------------------------------+
| 8    | Target is temporary.                                 |
+------+------------------------------------------------------+
| 9    | Target is a sparse file.                             |
+------+------------------------------------------------------+
| 10   | Target has reparse point data.                       |
+------+------------------------------------------------------+
| 11   | Target is compressed.                                |
+------+------------------------------------------------------+
| 12   | Target is offline.                                   |
+------+------------------------------------------------------+

+-----------------------------------------------------------------------------------+
|                           File Location Info                                      |
+------+---------+------------------------------------------------------------------+
|Offset|  Size   | Contents                                                         |
+------+---------+------------------------------------------------------------------+
|  0h  | 1 dword | This is the total length of this structure and all following data|
+------+---------+------------------------------------------------------------------+
|  4h  | 1 dword | This is a pointer to first offset after this structure. 1Ch      |
+------+---------+------------------------------------------------------------------+
|  8h  | 1 dword | Flags                                                            |
+------+---------+------------------------------------------------------------------+
|  Ch  | 1 dword | Offset of local volume info                                      |
+------+---------+------------------------------------------------------------------+
|  10h | 1 dword | Offset of base pathname on local system                          |
+------+---------+------------------------------------------------------------------+
|  14h | 1 dword | Offset of network volume info                                    |
+------+---------+------------------------------------------------------------------+
|  18h | 1 dword | Offset of remaining pathname                                     |
+------+---------+------------------------------------------------------------------+
| Notes: The first length value includes all the assorted pathnames and other data  |
| structures. All offsets are relative to the start of this structure.              |
+-----------------------------------------------------------------------------------+

'''
class LnkReadError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
def printarraycontent(arr, astype, startat, yn):
    if (yn):
        print 'size : ', len(arr)
    s ='%(v)02' + astype + ''
    for i in (len(arr)-1, startat):
        print s % {'v':arr[i]}
def readshortcut(filestr):
    try:
        fd = open(filestr, 'rb')
        
        buf = array.array('B')
        buf.fromfile(fd, 2*WORD)
        if (chr(buf[0]) != 'L'):
            raise LnkReadError, ('This is not windows shortcut file')
        buf.fromfile(fd, HEXB)



|0h    | 1 dword   | Always 0000004Ch ‘L’          |
+------+-----------+-------------------------------+
|4h    |16 bytes   | GUID of shortcut files        |
+------+-----------+-------------------------------+
|14h   | 1 dword   | Flags                         |
+------+-----------+-------------------------------+
|18h   | 1 dword   | File attributes               |
+------+-----------+-------------------------------+
|1Ch   | 1 qword   | Time 1                        |
+------+-----------+-------------------------------+
|24h   | 1 qword   | Time 2                        |
+------+-----------+-------------------------------+
|2Ch   | 1 qword   | Time 3                        |
+------+-----------+-------------------------------+
|34h   | 1 dword   | File length                   |
+------+-----------+-------------------------------+
|38h   | 1 dword   | Icon number                   |
+------+-----------+-------------------------------+
|3Ch   | 1 dword   | ShowWnd value                 |
+------+-----------+-------------------------------+
|40h   | 1 dword   | Hot key                       |
+------+-----------+-------------------------------+
|44h   | 2 dwords  | Unknown, always zero          |
+------+-----------+-------------------------------+
        #printarraycontent(buf, 'X', DWORD, True)
        
        
        #buf = fd.read()
        #print 'Length buf :', len(buf)
        #for i in (0, len(buf)-1):
        #    print '%(hex)02X ' %{'hex': ord(buf[i])}
        #print '\n'
        #print 'Everything is fine'
        fd.close()
    except IOError:
        print "File not found"
    except EOFError:
        print ERR_LEN
    except LnkReadError, e:
        print e.__str__()
    return