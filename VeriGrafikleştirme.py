//Veri tabanına kaydettiğim verilerin grafikleştirilmesini sağlayan kodlar


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
vt = sqlite3.connect('C:/Users/esra2/Documents/SOBE/GeoSocEyeTrackingforTraining/FormAppInteraction-2022_07_19-a/WindowsFormsApp1/bin/x64/Debug/OTETDatabaseV1.squlite') #Windows
im = vt.cursor()
im.execute("""SELECT DynamicVideo FROM User""")
veriler = im.fetchall()
im.execute("""SELECT ID FROM User""")
idler=im.fetchall()
print(len(veriler))
print(type(veriler[2]))
a=' '.join(map(str, veriler[2]))
df=pd.read_csv(a)
#print(df)

for i in range(len(veriler)):
    path=' '.join(map(str, veriler[i]))
    id=' '.join(map(str, idler[i]))
    if path=='None':
        continue
    if id=='None':
        continue
    #print(type(path))
    name=path.split("\\")
    name=name[7]
    name1=name.split("_")
    name1=name1[0]
    #print(name)

    df = pd.read_csv(path)
    size1=df.shape[0]
    #print(size1)
    oran=(size1*100)/1600
    if oran>100:
        oran=100
    oran=int(oran)
    #print(oran)
    #print(id)
    #sqlite_insert_query = """INSERT INTO User(IzlemeOrani) VALUES (oran)"""
    im.execute(f"UPDATE User set IzlemeOrani={oran} where ID ={id}")
    vt.commit()
    #im.close()

    # GRAFİK
    ###-> küçük ekran için
    x1, y1 = [965, 965], [0, 1200]
    plt.plot(x1, y1)
    plt.plot(df['fixationX'], df['fixationY'], linestyle='', color='red', marker='.', alpha=0.9, label="Fixation")
    plt.plot(df['fixationX'], df['fixationY'], linestyle='-', color='red', alpha=0.5, label="Saccade")
    plt.legend(loc="upper right")
    plt.axvspan(0, 965, facecolor='grey', alpha=0.2)
    plt.axvspan(965, 2000, facecolor='grey', alpha=0.6)
    plt.text(250, 1100, 'Geometric', fontsize=13, alpha=0.6)
    plt.text(1360, 1100, 'Social', fontsize=13, alpha=0.6)

    #
    plt.xlim(0, 2000)
    plt.ylim(1200, 0)
    plt.xlabel('X')
    plt.ylabel('Y')
    # Grafiğin kaydedilmesi
    plt.savefig("C:\\Users\\esra2\\Downloads\\graf\\"+name+".jpg")
    plt.close()
    # plt.show()


