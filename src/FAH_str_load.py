__author__ = 'pantonio'

import os

fd = open('C:\\Downloads\\fahorro\\stores.dat')
str = fd.readline()
lines = 0
ins = "insert into stg_store (tran_type,StoreNumber,Name,Address1,AddressCity,AddressCountry,Email,Phone,Region,Company,Desc1,Desc2,Desc3,Desc4,Desc5,Desc6,Desc7,Desc8,Desc9,Desc10,Desc11,Desc12,Desc13,Desc14,Desc15,Desc16,Desc17,Desc18,Desc19,Desc20,Desc21,DBDateEffectiveFrom,DBDateEffectiveTo) values ("
while len(str) > 0:
    str = fd.readline()
    str = str.replace('\n', '')
    cols = str.split('|')

    if len(cols) < 33:
        break

    #TRANS_TYPE
    ins2 = ins + "'" + cols[0] + "',"
    # StoreNumber
    ins2 = ins2 + cols[1] + ","
    # Name
    ins2 = ins2 + "'" + cols[2] + "',"
    # Address1
    ins2 = ins2 + "'" + cols[3][0:49] + "',"
    # AddressCity
    ins2 = ins2 + "'" + cols[4] + "',"
    # AddressCountry
    ins2 = ins2 + "'" + cols[5] + "',"
    # Email
    ins2 = ins2 + "'" + cols[6] + "',"
    # Phone
    ins2 = ins2 + "'" + cols[7] + "',"
    # Region
    ins2 = ins2 + "'" + cols[8] + "',"
    # Company
    ins2 = ins2 + "'" + cols[9] + "',"
    # Desc1
    ins2 = ins2 + "'" + cols[10] + "',"
    # Desc2
    ins2 = ins2 + "'" + cols[11] + "',"
    # Desc3
    ins2 = ins2 + "'" + cols[12] + "',"
    # Desc4
    ins2 = ins2 + "'" + cols[13] + "',"
    # Desc5
    ins2 = ins2 + "'" + cols[14] + "',"
    # Desc6
    ins2 = ins2 + "'" + cols[15] + "',"
    # Desc7
    ins2 = ins2 + "'" + cols[16] + "',"
    # Desc8
    ins2 = ins2 + "'" + cols[17] + "',"
    # Desc9
    ins2 = ins2 + "'"+cols[18] + "',"
    # Desc10
    ins2 = ins2 + "'"+cols[19] + "',"
    # Desc11
    ins2 = ins2 + "'"+cols[20] + "',"
    # Desc12
    ins2 = ins2 + "'"+cols[21] + "',"
    # Desc13
    ins2 = ins2 + "'"+cols[22] + "',"
    # Desc14
    ins2 = ins2 + "'"+cols[23] + "',"
    # Desc15
    ins2 = ins2 + "'"+cols[24] + "',"
    # Desc16
    ins2 = ins2 + "'"+cols[25] + "',"
    # Desc17
    ins2 = ins2 + "'"+cols[26] + "',"
    # Desc18
    ins2 = ins2 + "'"+cols[27] + "',"
    # Desc19
    ins2 = ins2 + "'"+cols[28] + "',"
    # Desc20
    ins2 = ins2 + "'"+cols[29] + "',"
    #Desc21
    ins2 = ins2 + "'"+cols[30] + "',"
    # DBDateEffectiveFrom
    ins2 = ins2 + "to_date('" + cols[31] + "','dd/mm/yyyy'),"
    # DBDateEffectiveTo
    ins2 = ins2 + "to_date('" + cols[32] + "','dd/mm/yyyy'));"

    print(ins2)
    lines = lines +1
    if lines > 998:
        print("commit;")
        lines = 0

print("commit;\n")
lines = 0
fd.close()
#print(lines.__str__() + " lines read\n")