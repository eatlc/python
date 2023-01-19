//Veri tabanındaki CSV leri ayrı bir yere kopyalama
import shutil
import sqlite3
pathdest='C:\\Users\\esra2\\Documents\\OTET\\ASDCSV\\'
vt = sqlite3.connect('C:/Users/esra2/Documents/SOBE/GeoSocEyeTrackingforTraining/FormAppInteraction-2022_07_19-a/WindowsFormsApp1/bin/x64/Debug/OTETDatabaseV1.squlite')
im = vt.cursor()
im.execute("""SELECT DynamicVideo FROM User""")
veriler = im.fetchall()

for i in range(len(veriler)):
    path=' '.join(map(str,veriler[i]))
    if(path=='None'):
        continue
    shutil.copy(path,pathdest)
