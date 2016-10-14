__author__ = 'pantonio'

import os

fd = open('C:\\Downloads\\fahorro\\products.dat')
str = fd.readline()
lines = 0
ins = "insert into stg_product (TRAN_TYPE,UPC,ID,Name,Width,Height,Depth,AbbrevName,\"SIZE\",UOM,Category,Supplier,Price,CaseWidth,CaseHeight,CaseDepth,CaseTotalNumber,UnitCost,Desc1,Desc2,Desc3,Desc4,Desc5,Desc6,Desc7,Desc8,Desc9,Desc10,Desc11,Desc12,Desc13,Desc14,Desc15,Desc16,Desc17,Desc18,Desc19,Desc20,Desc21,Desc22,Desc23,Desc24,Desc26,Value1,Value2,Brand,Subcategory,Weight,DateCreated) values ("
while len(str) > 0:
    str = fd.readline()
    str = str.replace('\n', '')
    cols = str.split('|')

    if len(cols) < 49:
        break

    #TRANS_TYPE
    ins2 = ins + "'"+cols[0] + "',"
    # UPC
    ins2 = ins2 + "'"+cols[1] + "',"
    # ID
    ins2 = ins2 + "'"+cols[2] + "',"
    # Name
    ins2 = ins2 + "'"+cols[3] + "',"
    # Width
    ins2 = ins2 + cols[4] + ","
    # Height
    ins2 = ins2 + cols[5] + ","
    # Depth
    ins2 = ins2 + cols[6] + ","
    # AbbrevName
    ins2 = ins2 + "'"+cols[7] + "',"
    # Size
    ins2 = ins2 + cols[8] + ","
    # UOM
    ins2 = ins2 + "'" +  (cols[9])[0:5] + "',"
    # Category
    ins2 = ins2 + "'"+cols[10] + "',"
    # Supplier
    ins2 = ins2 + "'"+cols[11] + "',"
    # Price
    ins2 = ins2 + cols[12] + ","
    # CaseWidth
    ins2 = ins2 + cols[13] + ","
    # CaseHeight
    ins2 = ins2 + cols[14] + ","
    # CaseDepth
    ins2 = ins2 + cols[15] + ","
    # CaseTotalNumber
    ins2 = ins2 + cols[16] + ","
    # UnitCost
    ins2 = ins2 + cols[17] + ","
    # Desc1
    ins2 = ins2 + "'"+cols[18] + "',"
    # Desc2
    ins2 = ins2 + "'"+cols[19] + "',"
    # Desc3
    ins2 = ins2 + "'"+cols[20] + "',"
    # Desc4
    ins2 = ins2 + "'"+cols[21] + "',"
    # Desc5
    ins2 = ins2 + "'"+cols[22] + "',"
    # Desc6
    ins2 = ins2 + "'"+cols[23] + "',"
    # Desc7
    ins2 = ins2 + "'"+cols[24] + "',"
    # Desc8
    ins2 = ins2 + "'"+cols[25] + "',"
    # Desc9
    ins2 = ins2 + "'"+cols[26] + "',"
    # Desc10
    ins2 = ins2 + "'"+cols[27] + "',"
    # Desc11
    ins2 = ins2 + "'"+cols[28] + "',"
    # Desc12
    ins2 = ins2 + "'"+cols[29] + "',"
    # Desc13
    ins2 = ins2 + "'"+cols[30] + "',"
    # Desc14
    ins2 = ins2 + "'"+cols[31] + "',"
    # Desc15
    ins2 = ins2 + "'"+cols[32] + "',"
    # Desc16
    ins2 = ins2 + "'"+cols[33] + "',"
    # Desc17
    ins2 = ins2 + "'"+cols[34] + "',"
    # Desc18
    ins2 = ins2 + "'"+cols[35] + "',"
    # Desc19
    ins2 = ins2 + "'"+cols[36] + "',"
    # Desc20
    ins2 = ins2 + "'"+cols[37] + "',"
    # Desc21
    ins2 = ins2 + "'"+cols[38] + "',"
    # Desc22
    ins2 = ins2 + "'"+cols[39] + "',"
    # Desc23
    ins2 = ins2 + "'"+cols[40] + "',"
    # Desc24
    ins2 = ins2 + "'"+cols[41] + "',"
    # Desc26
    ins2 = ins2 + "'"+cols[42] + "',"
    # Value1
    ins2 = ins2 + cols[43] + ","
    # Value2
    ins2 = ins2 + cols[44] + ","
    # Brand
    ins2 = ins2 + "'"+cols[45] + "',"
    # Subcategory
    ins2 = ins2 + "'"+cols[46] + "',"
    # Weight
    ins2 = ins2 + cols[47] + ","
    # DateCreated
    ins2 = ins2 + "to_date('" + cols[48] + "','dd/mm/yyyy'));"
    print(ins2)
    lines = lines +1
    if lines > 498:
        print("commit;")
        lines = 0

print("commit;\n")
lines = 0
fd.close()
#print(lines.__str__() + " lines read\n")