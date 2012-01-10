import sys
import re

print ("Good choice fellow")
__all__=["ActivateUnitOrg", "EmployeesWORotation","PWMRepCommon","RepLauncher", "UnbalancedRotations", "DupSalesLM"]
platform = sys.platform
if (re.match("java", platform) is not None):
    # Crear conexion con jdbc
    print ("Esto es Jython")
else:
    # Crear conexion con cx_Oracle
    print ("This is python")
