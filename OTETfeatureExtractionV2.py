import sqlite3
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time, timedelta
import os
from goto import goto, label

prj_path=("C:\\Users\\esra2\\Documents\\OTET\\pythonKodlar\\OTETFeatureExtractionV1")

#Verilerin kayıtlı olduğu veritabanları
#ASD Verileri
db_asd = sqlite3.connect('C:/Users/esra2/Documents/OTET/pythonKodlar/OTETFeatureExtractionV1/database/OTETDatabaseV1.squlite')
db_nonasd = sqlite3.connect('C:/Users/esra2/Documents/OTET/pythonKodlar/OTETFeatureExtractionV1/database/OTETDatabaseV2.squlite')

#Yeni verilerin kayıt edileceği yeni veri tabanı yolu


#Veri tabanlarının imleçleri
crsr_asd=db_asd.cursor()
crsr_nonasd=db_nonasd.cursor()

#Veritabanlarındaki DynamicVideo sütunundaki bilgileri seçmek için
crsr_asd.execute("""SELECT DynamicVideo FROM User""")
crsr_nonasd.execute("""SELECT DynamicVideo FROM User""")

#Fetchall ile birlikte seçilen verilerin tamamı getirilir
dynmcData_asd=crsr_asd.fetchall()
dynmcData_nonasd=crsr_nonasd.fetchall()

#Verileri IDlerini de aynı şekilde almak için
crsr_asd.execute("""SELECT ID FROM User""")
crsr_nonasd.execute("""SELECT ID FROM User""")
id_asd=crsr_asd.fetchall()
id_nonasd=crsr_nonasd.fetchall()


#Cinsiyet bilgileri
crsr_asd.execute("""SELECT Gender FROM User""")
crsr_nonasd.execute("""SELECT Gender FROM User""")
gender_asd=crsr_asd.fetchall()
gender_nonasd=crsr_nonasd.fetchall()

#Yaş bilgisi
crsr_asd.execute("""SELECT Birthday FROM User""")
crsr_nonasd.execute("""SELECT Birthday FROM User""")
birthday_asd=crsr_asd.fetchall()
birthday_nonasd=crsr_nonasd.fetchall()

#Izleme orani
crsr_asd.execute("""SELECT IzlemeOrani FROM User""")
crsr_nonasd.execute("""SELECT IzlemeOrani FROM User""")
viewrate_asd=crsr_asd.fetchall()
viewrate_nonasd=crsr_nonasd.fetchall()

#Ad-soyad gerekmezse sil
#ad
crsr_asd.execute("""SELECT FirstName FROM User""")
crsr_nonasd.execute("""SELECT FirstName FROM User""")
firstname_asd=crsr_asd.fetchall()
firstname_nonasd=crsr_nonasd.fetchall()
#soyad
crsr_asd.execute("""SELECT LastName FROM User""")
crsr_nonasd.execute("""SELECT LastName FROM User""")
lastname_asd=crsr_asd.fetchall()
lastname_nonasd=crsr_nonasd.fetchall()

#ASD için feature extraction
for i in range(len(id_asd)):
    path=' '.join(map(str, dynmcData_asd[i]))
    if path=='None':
        continue

    firstname=' '.join(map(str, firstname_asd[i]))
    lastname=' '.join(map(str, lastname_asd[i]))
    filename="asd_"+firstname+lastname
    gender=' '.join(map(str, gender_asd[i]))
    birthday=' '.join(map(str, birthday_asd[i]))
    bday=[]
    bday=birthday.split('.')
    bday=bday[2]
    viewrate=' '.join(map(str, viewrate_asd[i]))

    df=pd.read_csv(path)
    #satır sütun sayılarının değişkenelere atılması
    row_count, column_count=df.shape

    #Kullanılacak değişkenlerin başlangıç değerleri
    t1 = ""
    row = 0
    fix = 0
    sac = 0
    i = 0
    j = 0
    zerotime = time(00, 00, 00, 000000)
    totalsaccadetime = 0
    totalfixationtime = 0
    totaltime = 0
    totalsaccadetimee = 0
    totalCalcSaccadeTimeGeo = 0
    totalCalcFixationTimeGeo = 0
    totalCalcFixationTimeSocial = 0
    totalCalcSaccadeTimeSocial = 0
    countSacGeo = 0
    countSacSocial = 0
    countFixGeo = 0
    countFixSocial = 0
    status = "empty"
    default = time(00, 00, 00, 500000)
    # kullanılan zamanın formatı
    fmt = '%H:%M:%S.%f'


    # Zamanı saniye'ye dönüştürerek float cinsinden kaydeden fonksiyon
    def timeToFloat(timeF):
        # sanieye dönüştürme
        timee = timeF.microsecond * 0.000001 + timeF.second + timeF.minute * 60 + timeF.hour * 3600
        return timee

    # Zamanı string türünden time formatına döünştüren fonksiyon
    def dfToTime(t):
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        ms = int(t[9:15])
        # time formatına dönüştürme
        timeF = time(h, m, s, ms)
        return timeF

    # Üzerinde işlem yapılan CSV'nin tüm satırlarını gezerek inceleyen ve onu göre işlem yapan döngü
    for i in range(0, row_count - 1):
        if df.at[i, 'fixationStatus'] == "End":
            # zaman boş olduğu için ilk t1 in alındığı durum
            if t1 == "":
                t1 = df.at[i, 'fixationDuring']
                t1cntrl=[]
                t1cntrl=t1.split(':')
                if(len(t1cntrl[0])>2):
                    #print(df.shape)
                    df=df.drop([i])
                    #print(df.shape)
                    continue
                time1 = dfToTime(t1)
                #print(time1)

                # zaman alınmadan önce end olan satırlarda saccade etikitini bastırmak için
                if time1 < default:
                    # print("saccade")
                    df.at[i, 'status'] = "1"
                    status = "1"

                # zaman alınmadan önce end olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    # print("fixation")
                    df.at[i, 'status'] = "0"
                    status = "0"

            # zaman alındıktan sonraki end satırlarına  bastırmak için
            else:
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)

                # zaman alındıktan sonra end olan durumlarda saccade etiketini bastırmak için
                if time1 < default:
                    #print("saccade")
                    sac = sac + 1
                    row = 0
                    # Saccade ise status = 1
                    status = "1"

                # zaman alındıktan sonra end  olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    fix = fix + 1
                    row = 1
                    # fixation ise status = 0
                    status = "0"

            # Status değişkenine göre gerekli işlemler yapılıyor
            if status == "1":  # saccade
                # status değişkeni döngünün bir sonraki adımı için boşaltılıyor
                status = "empty"
                saccadetime = df.at[i, 'fixationDuring']
                df.at[i, 'saccadetime'] = saccadetime
                calcSaccadetimee = timeToFloat(dfToTime(saccadetime))
                totalsaccadetime = calcSaccadetimee + totalsaccadetime

                if df.at[i, 'side'] == 0:  # sol taraf geo
                    saccadeTimeGeo = df.at[i, 'fixationDuring']
                    calcSaccadeTimeGeo = timeToFloat(dfToTime(saccadeTimeGeo))
                    totalCalcSaccadeTimeGeo = calcSaccadeTimeGeo + totalCalcSaccadeTimeGeo
                    countSacGeo = countSacGeo + 1

                elif df.at[i, 'side'] == 1:  # sağ taraf    social
                    saccadeTimeSocial = df.at[i, 'fixationDuring']
                    calcSaccadeTimeSocial = timeToFloat(dfToTime(saccadeTimeSocial))
                    totalCalcSaccadeTimeSocial = calcSaccadeTimeSocial + totalCalcSaccadeTimeSocial
                    countSacSocial = countSacSocial + 1

            elif status == "0":  # fixation
                status = "empty"
                #print(status)
                fixationtime = df.at[i, 'fixationDuring']
                df.at[i, 'fixationtime'] = fixationtime
                calcFixationtimee = timeToFloat(dfToTime(fixationtime))
                totalfixationtime = calcFixationtimee + totalfixationtime

                if df.at[i, 'side'] == 0:  # sol taraf geo
                    fixationTimeGeo = df.at[i, 'fixationDuring']
                    calcFixationTimeGeo = timeToFloat(dfToTime(fixationTimeGeo))
                    totalCalcFixationTimeGeo = calcFixationTimeGeo + totalCalcFixationTimeGeo
                    countFixGeo = countFixGeo + 1

                elif df.at[i, 'side'] == 1:  # sağ taraf    social
                    fixationTimeSocial = df.at[i, 'fixationDuring']
                    calcFixationTimeSocial = timeToFloat(dfToTime(fixationTimeSocial))
                    totalCalcFixationTimeSocial = calcFixationTimeSocial + totalCalcFixationTimeSocial
                    countFixSocial = countFixSocial + 1

    # tekli satıra geçiş
    # totaltime=saccadetime+fixationtime
    totaltime = totalsaccadetime + totalfixationtime
    total = totalCalcSaccadeTimeGeo + totalCalcFixationTimeGeo + totalCalcSaccadeTimeSocial + totalCalcFixationTimeSocial
    totalFixationPercent = (totalfixationtime / (totalfixationtime + totalsaccadetime)) * 100
    totalSaccadePercent = (totalsaccadetime / (totalfixationtime + totalsaccadetime)) * 100

    if(totalfixationtime==0):
        totalFixGeoPercent=0
        totalFixSocPercent=0
    else:
        totalFixGeoPercent = (totalCalcFixationTimeGeo / totalfixationtime) * 100
        totalFixSocPercent = (totalCalcFixationTimeSocial / totalfixationtime) * 100

    if(totalsaccadetime==0):
        totalSacGeoPercent=0
        totalSacSocPercent=0
    else:
        totalSacGeoPercent = (totalCalcSaccadeTimeGeo / totalsaccadetime) * 100
        totalSacSocPercent = (totalCalcSaccadeTimeSocial / totalsaccadetime) * 100

    #Toplanan verilerin istatistiksel özellikleri
    df = df.dropna(subset=['fixationX'])
    #df = df.dropna(subset=['fixationY'])
    #mean
    meanfixX = statistics.mean(df['fixationX'])
    meanfixY = statistics.mean(df['fixationY'])
    meangzpX = statistics.mean(df['gazePointX'])
    meangzpY = statistics.mean(df['gazePointY'])
    meanhdrtX = statistics.mean(df['headRotationX'])
    meanhdrtY = statistics.mean(df['headRotationY'])
    meanhdrtZ = statistics.mean(df['headRotationZ'])
    meanhdpsX = statistics.mean(df['headPosX'])
    meanhdpsY = statistics.mean(df['headPosY'])
    meanhdpsZ = statistics.mean(df['headPosZ'])
    meanlfteyepsX = statistics.mean(df['leftEyePosX'])
    meanlfteyepsY = statistics.mean(df['leftEyePosY'])
    meanlfteyepsZ = statistics.mean(df['leftEyePosZ'])
    meanrgteyepsX = statistics.mean(df['rightEyePosX'])
    meanrgteyepsY = statistics.mean(df['rightEyePosY'])
    meanrgteyepsZ = statistics.mean(df['rightEyePosZ'])
    meanlftynrmX = statistics.mean(df['leftEyeNormalizedX'])
    meanlftynrmY = statistics.mean(df['leftEyeNormalizedY'])
    meanlftynrmZ = statistics.mean(df['leftEyeNormalizedZ'])
    meanrgtynrmX = statistics.mean(df['rightEyeNormalizedX'])
    meanrgtynrmY = statistics.mean(df['rightEyeNormalizedY'])
    meanrgtynrmZ = statistics.mean(df['rightEyeNormalizedZ'])
    #median
    medianfixX = statistics.median(df['fixationX'])
    medianfixY = statistics.median(df['fixationY'])
    mediangzpX = statistics.median(df['gazePointX'])
    mediangzpY = statistics.median(df['gazePointY'])
    medianhdrtX = statistics.median(df['headRotationX'])
    medianhdrtY = statistics.median(df['headRotationY'])
    medianhdrtZ = statistics.median(df['headRotationZ'])
    medianhdpsX = statistics.median(df['headPosX'])
    medianhdpsY = statistics.median(df['headPosY'])
    medianhdpsZ = statistics.median(df['headPosZ'])
    medianlfteyepsX = statistics.median(df['leftEyePosX'])
    medianlfteyepsY = statistics.median(df['leftEyePosY'])
    medianlfteyepsZ = statistics.median(df['leftEyePosZ'])
    medianrgteyepsX = statistics.median(df['rightEyePosX'])
    medianrgteyepsY = statistics.median(df['rightEyePosY'])
    medianrgteyepsZ = statistics.median(df['rightEyePosZ'])
    medianlftynrmX = statistics.median(df['leftEyeNormalizedX'])
    medianlftynrmY = statistics.median(df['leftEyeNormalizedY'])
    medianlftynrmZ = statistics.median(df['leftEyeNormalizedZ'])
    medianrgtynrmX = statistics.median(df['rightEyeNormalizedX'])
    medianrgtynrmY = statistics.median(df['rightEyeNormalizedY'])
    medianrgtynrmZ = statistics.median(df['rightEyeNormalizedZ'])
    #std
    stdfixX = statistics.stdev(df['fixationX'])
    stdfixY = statistics.stdev(df['fixationY'])
    stdgzpX = statistics.stdev(df['gazePointX'])
    stdgzpY = statistics.stdev(df['gazePointY'])
    stdhdrtX = statistics.stdev(df['headRotationX'])
    stdhdrtY = statistics.stdev(df['headRotationY'])
    stdhdrtZ = statistics.stdev(df['headRotationZ'])
    stdhdpsX = statistics.stdev(df['headPosX'])
    stdhdpsY = statistics.stdev(df['headPosY'])
    stdhdpsZ = statistics.stdev(df['headPosZ'])
    stdlfteyepsX = statistics.stdev(df['leftEyePosX'])
    stdlfteyepsY = statistics.stdev(df['leftEyePosY'])
    stdlfteyepsZ = statistics.stdev(df['leftEyePosZ'])
    stdrgteyepsX = statistics.stdev(df['rightEyePosX'])
    stdrgteyepsY = statistics.stdev(df['rightEyePosY'])
    stdrgteyepsZ = statistics.stdev(df['rightEyePosZ'])
    stdlftynrmX = statistics.stdev(df['leftEyeNormalizedX'])
    stdlftynrmY = statistics.stdev(df['leftEyeNormalizedY'])
    stdlftynrmZ = statistics.stdev(df['leftEyeNormalizedZ'])
    stdrgtynrmX = statistics.stdev(df['rightEyeNormalizedX'])
    stdrgtynrmY = statistics.stdev(df['rightEyeNormalizedY'])
    stdrgtynrmZ = statistics.stdev(df['rightEyeNormalizedZ'])
    #quantile %25
    q25fixX = np.percentile(df['fixationX'],25)
    q25fixY = np.percentile(df['fixationY'],25)
    q25gzpX = np.percentile(df['gazePointX'],25)
    q25gzpY = np.percentile(df['gazePointY'],25)
    q25hdrtX = np.percentile(df['headRotationX'],25)
    q25hdrtY = np.percentile(df['headRotationY'],25)
    q25hdrtZ = np.percentile(df['headRotationZ'],25)
    q25hdpsX = np.percentile(df['headPosX'],25)
    q25hdpsY = np.percentile(df['headPosY'],25)
    q25hdpsZ = np.percentile(df['headPosZ'],25)
    q25lfteyepsX = np.percentile(df['leftEyePosX'],25)
    q25lfteyepsY = np.percentile(df['leftEyePosY'],25)
    q25lfteyepsZ = np.percentile(df['leftEyePosZ'],25)
    q25rgteyepsX = np.percentile(df['rightEyePosX'],25)
    q25rgteyepsY = np.percentile(df['rightEyePosY'],25)
    q25rgteyepsZ = np.percentile(df['rightEyePosZ'],25)
    q25lftynrmX = np.percentile(df['leftEyeNormalizedX'],25)
    q25lftynrmY = np.percentile(df['leftEyeNormalizedY'],25)
    q25lftynrmZ = np.percentile(df['leftEyeNormalizedZ'],25)
    q25rgtynrmX = np.percentile(df['rightEyeNormalizedX'],25)
    q25rgtynrmY = np.percentile(df['rightEyeNormalizedY'],25)
    q25rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'],25)
    #quantiles %50
    q50fixX = np.percentile(df['fixationX'], 50)
    q50fixY = np.percentile(df['fixationY'], 50)
    q50gzpX = np.percentile(df['gazePointX'], 50)
    q50gzpY = np.percentile(df['gazePointY'], 50)
    q50hdrtX = np.percentile(df['headRotationX'], 50)
    q50hdrtY = np.percentile(df['headRotationY'], 50)
    q50hdrtZ = np.percentile(df['headRotationZ'], 50)
    q50hdpsX = np.percentile(df['headPosX'], 50)
    q50hdpsY = np.percentile(df['headPosY'], 50)
    q50hdpsZ = np.percentile(df['headPosZ'], 50)
    q50lfteyepsX = np.percentile(df['leftEyePosX'], 50)
    q50lfteyepsY = np.percentile(df['leftEyePosY'], 50)
    q50lfteyepsZ = np.percentile(df['leftEyePosZ'], 50)
    q50rgteyepsX = np.percentile(df['rightEyePosX'], 50)
    q50rgteyepsY = np.percentile(df['rightEyePosY'], 50)
    q50rgteyepsZ = np.percentile(df['rightEyePosZ'], 50)
    q50lftynrmX = np.percentile(df['leftEyeNormalizedX'], 50)
    q50lftynrmY = np.percentile(df['leftEyeNormalizedY'], 50)
    q50lftynrmZ = np.percentile(df['leftEyeNormalizedZ'], 50)
    q50rgtynrmX = np.percentile(df['rightEyeNormalizedX'], 50)
    q50rgtynrmY = np.percentile(df['rightEyeNormalizedY'], 50)
    q50rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'], 50)
    #quantile %75
    q75fixX = np.percentile(df['fixationX'], 75)
    q75fixY = np.percentile(df['fixationY'], 75)
    q75gzpX = np.percentile(df['gazePointX'], 75)
    q75gzpY = np.percentile(df['gazePointY'], 75)
    q75hdrtX = np.percentile(df['headRotationX'], 75)
    q75hdrtY = np.percentile(df['headRotationY'], 75)
    q75hdrtZ = np.percentile(df['headRotationZ'], 75)
    q75hdpsX = np.percentile(df['headPosX'], 75)
    q75hdpsY = np.percentile(df['headPosY'], 75)
    q75hdpsZ = np.percentile(df['headPosZ'], 75)
    q75lfteyepsX = np.percentile(df['leftEyePosX'], 75)
    q75lfteyepsY = np.percentile(df['leftEyePosY'], 75)
    q75lfteyepsZ = np.percentile(df['leftEyePosZ'], 75)
    q75rgteyepsX = np.percentile(df['rightEyePosX'], 75)
    q75rgteyepsY = np.percentile(df['rightEyePosY'], 75)
    q75rgteyepsZ = np.percentile(df['rightEyePosZ'], 75)
    q75lftynrmX = np.percentile(df['leftEyeNormalizedX'], 75)
    q75lftynrmY = np.percentile(df['leftEyeNormalizedY'], 75)
    q75lftynrmZ = np.percentile(df['leftEyeNormalizedZ'], 75)
    q75rgtynrmX = np.percentile(df['rightEyeNormalizedX'], 75)
    q75rgtynrmY = np.percentile(df['rightEyeNormalizedY'], 75)
    q75rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'], 75)
    #min
    minfixX = min(df['fixationX'])
    minfixY = min(df['fixationY'])
    mingzpX = min(df['gazePointX'])
    mingzpY = min(df['gazePointY'])
    minhdrtX = min(df['headRotationX'])
    minhdrtY = min(df['headRotationY'])
    minhdrtZ = min(df['headRotationZ'])
    minhdpsX = min(df['headPosX'])
    minhdpsY = min(df['headPosY'])
    minhdpsZ = min(df['headPosZ'])
    minlfteyepsX = min(df['leftEyePosX'])
    minlfteyepsY = min(df['leftEyePosY'])
    minlfteyepsZ = min(df['leftEyePosZ'])
    minrgteyepsX =min(df['rightEyePosX'])
    minrgteyepsY = min(df['rightEyePosY'])
    minrgteyepsZ =min(df['rightEyePosZ'])
    minlftynrmX = min(df['leftEyeNormalizedX'])
    minlftynrmY = min(df['leftEyeNormalizedY'])
    minlftynrmZ = min(df['leftEyeNormalizedZ'])
    minrgtynrmX = min(df['rightEyeNormalizedX'])
    minrgtynrmY = min(df['rightEyeNormalizedY'])
    minrgtynrmZ = min(df['rightEyeNormalizedZ'])
    #max
    maxfixX = max(df['fixationX'])
    maxfixY = max(df['fixationY'])
    maxgzpX = max(df['gazePointX'])
    maxgzpY = max(df['gazePointY'])
    maxhdrtX = max(df['headRotationX'])
    maxhdrtY = max(df['headRotationY'])
    maxhdrtZ = max(df['headRotationZ'])
    maxhdpsX =max(df['headPosX'])
    maxhdpsY = max(df['headPosY'])
    maxhdpsZ = max(df['headPosZ'])
    maxlfteyepsX = max(df['leftEyePosX'])
    maxlfteyepsY = max(df['leftEyePosY'])
    maxlfteyepsZ = max(df['leftEyePosZ'])
    maxrgteyepsX = max(df['rightEyePosX'])
    maxrgteyepsY = max(df['rightEyePosY'])
    maxrgteyepsZ =max(df['rightEyePosZ'])
    maxlftynrmX = max(df['leftEyeNormalizedX'])
    maxlftynrmY = max(df['leftEyeNormalizedY'])
    maxlftynrmZ = max(df['leftEyeNormalizedZ'])
    maxrgtynrmX = max(df['rightEyeNormalizedX'])
    maxrgtynrmY = max(df['rightEyeNormalizedY'])
    maxrgtynrmZ = max(df['rightEyeNormalizedZ'])

    # Tüm hesaplamalar için oluşturulacak tek satırlık DataFrame'in verileri
    datason = {'name': [firstname], 'lastname': [lastname], 'label': 1,
               'gender': [gender], 'birthday': [bday], 'viewrate': [viewrate],
               'ttlFixationTime': [round(totalfixationtime, 5)], 'ttlSaccadeTime': [round(totalsaccadetime, 5)],
               'ttlTime': [round(totaltime, 5)],
               'fixationCount': [fix], 'saccadeCount': [sac],
               'ttlFixPerc': [round(totalFixationPercent, 5)], 'ttlSacPerc': [round(totalSaccadePercent, 5)],
               'ttlFixGeoPerc': [round(totalFixGeoPercent, 5)], 'ttlFixSocPerc': [round(totalFixSocPercent, 5)],
               'ttlSacGeoPerc': [round(totalSacGeoPercent, 5)], 'ttlSacSocPerc': [round(totalSacSocPercent, 5)],
               'ttlFixTimeGeo': [round(totalCalcFixationTimeGeo, 5)],
               'ttlFixTimeSoc': [round(totalCalcFixationTimeSocial, 5)],
               'ttlSacTimeGeo': [round(totalCalcSaccadeTimeGeo, 5)],
               'ttlSacTimeSoc': [round(totalCalcSaccadeTimeSocial, 5)],
               'cntFixGeo': [round(countFixGeo, 5)], 'cntFixSoc': [round(countFixSocial, 5)],
               'cntSacGeo': [round(countSacGeo, 5)], 'cntSacSoc': [round(countSacSocial, 5)],
               'meanfixX': [round(meanfixX, 5)], 'meanfixY': [round(meanfixY, 5)], 'meangzpX': [round(meangzpX, 5)],
               'meangzpY': [round(meangzpY, 5)],
               'meanhdrtX': [round(meanhdrtX, 5)], 'meanhdrtY': [round(meanhdrtY, 5)],
               'meanhdrtZ': [round(meanhdrtZ, 5)],
               'meanhdpsX': [round(meanhdpsX, 5)], 'meanhdpsY': [round(meanhdpsY, 5)],
               'meanhdpsZ': [round(meanhdpsZ, 5)],
               'meanlfteyepsX': [round(meanlfteyepsX, 5)], 'meanlfteyepsY': [round(meanlfteyepsY, 5)],
               'meanlfteyepsZ': [round(meanlfteyepsZ, 5)],
               'meanrghteyepsX': [round(meanrgteyepsX, 5)], 'meanrghteyepsY': [round(meanrgteyepsY, 5)],
               'meanrghteyepsZ': [round(meanrgteyepsZ, 5)],
               'meanlftynrmX': [round(meanlftynrmX, 5)], 'meanlftynrmY': [round(meanlftynrmY, 5)],
               'meanlftynrmZ': [round(meanlftynrmZ, 5)],
               'meanrgtynrmX': [round(meanrgtynrmX, 5)], 'meanrgtynrmY': [round(meanrgtynrmY, 5)],
               'meanrgtynrmZ': [round(meanrgtynrmZ, 5)],
               'medianfixX': [round(medianfixX, 5)], 'medianfixY': [round(medianfixY, 5)],
               'mediangzpX': [round(mediangzpX, 5)], 'mediangzpY': [round(mediangzpY, 5)],
               'medianhdrtX': [round(medianhdrtX, 5)], 'medianhdrtY': [round(medianhdrtY, 5)],
               'medianhdrtZ': [round(medianhdrtZ, 5)],
               'medianhdpsX': [round(medianhdpsX, 5)], 'medianhdpsY': [round(medianhdpsY, 5)],
               'medianhdpsZ': [round(medianhdpsZ, 5)],
               'medianlfteyepsX': [round(medianlfteyepsX, 5)], 'medianlfteyepsY': [round(medianlfteyepsY, 5)],
               'medianlfteyepsZ': [round(medianlfteyepsZ, 5)],
               'medianrghteyepsX': [round(medianrgteyepsX, 5)], 'medianrghteyepsY': [round(medianrgteyepsY, 5)],
               'medianrghteyepsZ': [round(medianrgteyepsZ, 5)],
               'medianlftynrmX': [round(medianlftynrmX, 5)], 'medianlftynrmY': [round(medianlftynrmY, 5)],
               'medianlftynrmZ': [round(medianlftynrmZ, 5)],
               'medianrgtynrmX': [round(medianrgtynrmX, 5)], 'medianrgtynrmY': [round(medianrgtynrmY, 5)],
               'medianrgtynrmZ': [round(medianrgtynrmZ, 5)],
               'stdfixX': [round(stdfixX, 5)], 'stdfixY': [round(stdfixY, 5)], 'stdgzpX': [round(stdgzpX, 5)],
               'stdgzpY': [round(stdgzpY, 5)],
               'stdhdrtX': [round(stdhdrtX, 5)], 'stdhdrtY': [round(stdhdrtY, 5)], 'stdhdrtZ': [round(stdhdrtZ, 5)],
               'stdhdpsX': [round(stdhdpsX, 5)], 'stdhdpsY': [round(stdhdpsY, 5)], 'stdhdpsZ': [round(stdhdpsZ, 5)],
               'stdlfteyepsX': [round(stdlfteyepsX, 5)], 'stdlfteyepsY': [round(stdlfteyepsY, 5)],
               'stdlfteyepsZ': [round(stdlfteyepsZ, 5)],
               'stdrghteyepsX': [round(stdrgteyepsX, 5)], 'stdrghteyepsY': [round(stdrgteyepsY, 5)],
               'stdrghteyepsZ': [round(stdrgteyepsZ, 5)],
               'stdlftynrmX': [round(stdlftynrmX, 5)], 'stdlftynrmY': [round(stdlftynrmY, 5)],
               'stdlftynrmZ': [round(stdlftynrmZ, 5)],
               'stdrgtynrmX': [round(stdrgtynrmX, 5)], 'stdrgtynrmY': [round(stdrgtynrmY, 5)],
               'stdrgtynrmZ': [round(stdrgtynrmZ, 5)],
               'q25fixX': [round(q25fixX, 5)], 'q25fixY': [round(q25fixY, 5)], 'q25gzpX': [round(q25gzpX, 5)],
               'q25gzpY': [round(q25gzpY, 5)],
               'q25hdrtX': [round(q25hdrtX, 5)], 'q25hdrtY': [round(q25hdrtY, 5)], 'q25hdrtZ': [round(q25hdrtZ, 5)],
               'q25hdpsX': [round(q25hdpsX, 5)], 'q25hdpsY': [round(q25hdpsY, 5)], 'q25hdpsZ': [round(q25hdpsZ, 5)],
               'q25lfteyepsX': [round(q25lfteyepsX, 5)], 'q25lfteyepsY': [round(q25lfteyepsY, 5)],
               'q25lfteyepsZ': [round(q25lfteyepsZ, 5)],
               'q25rghteyepsX': [round(q25rgteyepsX, 5)], 'q25rghteyepsY': [round(q25rgteyepsY, 5)],
               'q25rghteyepsZ': [round(q25rgteyepsZ, 5)],
               'q25lftynrmX': [round(q25lftynrmX, 5)], 'q25lftynrmY': [round(q25lftynrmY, 5)],
               'q25lftynrmZ': [round(q25lftynrmZ, 5)],
               'q25rgtynrmX': [round(q25rgtynrmX, 5)], 'q25rgtynrmY': [round(q25rgtynrmY, 5)],
               'q25rgtynrmZ': [round(q25rgtynrmZ, 5)],
               'q50fixX': [round(q50fixX, 5)], 'q50fixY': [round(q50fixY, 5)], 'q50gzpX': [round(q50gzpX, 5)],
               'q50gzpY': [round(q50gzpY, 5)],
               'q50hdrtX': [round(q50hdrtX, 5)], 'q50hdrtY': [round(q50hdrtY, 5)], 'q50hdrtZ': [round(q50hdrtZ, 5)],
               'q50hdpsX': [round(q50hdpsX, 5)], 'q50hdpsY': [round(q50hdpsY, 5)], 'q50hdpsZ': [round(q50hdpsZ, 5)],
               'q50lfteyepsX': [round(q50lfteyepsX, 5)], 'q50lfteyepsY': [round(q50lfteyepsY, 5)],
               'q50lfteyepsZ': [round(q50lfteyepsZ, 5)],
               'q50rghteyepsX': [round(q50rgteyepsX, 5)], 'q50rghteyepsY': [round(q50rgteyepsY, 5)],
               'q50rghteyepsZ': [round(q50rgteyepsZ, 5)],
               'q50lftynrmX': [round(q50lftynrmX, 5)], 'q50lftynrmY': [round(q50lftynrmY, 5)],
               'q50lftynrmZ': [round(q50lftynrmZ, 5)],
               'q50rgtynrmX': [round(q50rgtynrmX, 5)], 'q50rgtynrmY': [round(q50rgtynrmY, 5)],
               'q50rgtynrmZ': [round(q50rgtynrmZ, 5)],
               'q75fixX': [round(q75fixX, 5)], 'q75fixY': [round(q75fixY, 5)], 'q75gzpX': [round(q75gzpX, 5)],
               'q75gzpY': [round(q75gzpY, 5)],
               'q75hdrtX': [round(q75hdrtX, 5)], 'q75hdrtY': [round(q75hdrtY, 5)], 'q75hdrtZ': [round(q75hdrtZ, 5)],
               'q75hdpsX': [round(q75hdpsX, 5)], 'q75hdpsY': [round(q75hdpsY, 5)], 'q75hdpsZ': [round(q75hdpsZ, 5)],
               'q75lfteyepsX': [round(q75lfteyepsX, 5)], 'q75lfteyepsY': [round(q75lfteyepsY, 5)],
               'q75lfteyepsZ': [round(q75lfteyepsZ, 5)],
               'q75rghteyepsX': [round(q75rgteyepsX, 5)], 'q75rghteyepsY': [round(q75rgteyepsY, 5)],
               'q75rghteyepsZ': [round(q75rgteyepsZ, 5)],
               'q75lftynrmX': [round(q75lftynrmX, 5)], 'q75lftynrmY': [round(q75lftynrmY, 5)],
               'q75lftynrmZ': [round(q75lftynrmZ, 5)],
               'q75rgtynrmX': [round(q75rgtynrmX, 5)], 'q75rgtynrmY': [round(q75rgtynrmY, 5)],
               'q75rgtynrmZ': [round(q75rgtynrmZ, 5)],
               'minfixX': [round(minfixX, 5)], 'minfixY': [round(minfixY, 5)], 'mingzpX': [round(mingzpX, 5)],
               'mingzpY': [round(mingzpY, 5)],
               'minhdrtX': [round(minhdrtX, 5)], 'minhdrtY': [round(minhdrtY, 5)], 'minhdrtZ': [round(minhdrtZ, 5)],
               'minhdpsX': [round(minhdpsX, 5)], 'minhdpsY': [round(minhdpsY, 5)], 'minhdpsZ': [round(minhdpsZ, 5)],
               'minlfteyepsX': [round(minlfteyepsX, 5)], 'minlfteyepsY': [round(minlfteyepsY, 5)],
               'minlfteyepsZ': [round(minlfteyepsZ, 5)],
               'minrghteyepsX': [round(minrgteyepsX, 5)], 'minrghteyepsY': [round(minrgteyepsY, 5)],
               'minrghteyepsZ': [round(minrgteyepsZ, 5)],
               'minlftynrmX': [round(minlftynrmX, 5)], 'minlftynrmY': [round(minlftynrmY, 5)],
               'minlftynrmZ': [round(minlftynrmZ, 5)],
               'minrgtynrmX': [round(minrgtynrmX, 5)], 'minrgtynrmY': [round(minrgtynrmY, 5)],
               'minrgtynrmZ': [round(minrgtynrmZ, 5)],
               'maxfixX': [round(maxfixX, 5)], 'maxfixY': [round(maxfixY, 5)], 'maxgzpX': [round(maxgzpX, 5)],
               'maxgzpY': [round(maxgzpY, 5)],
               'maxhdrtX': [round(maxhdrtX, 5)], 'maxhdrtY': [round(maxhdrtY, 5)], 'maxhdrtZ': [round(maxhdrtZ, 5)],
               'maxhdpsX': [round(maxhdpsX, 5)], 'maxhdpsY': [round(maxhdpsY, 5)], 'maxhdpsZ': [round(maxhdpsZ, 5)],
               'maxlfteyepsX': [round(maxlfteyepsX, 5)], 'maxlfteyepsY': [round(maxlfteyepsY, 5)],
               'maxlfteyepsZ': [round(maxlfteyepsZ, 5)],
               'maxrghteyepsX': [round(maxrgteyepsX, 5)], 'maxrghteyepsY': [round(maxrgteyepsY, 5)],
               'maxrghteyepsZ': [round(maxrgteyepsZ, 5)],
               'maxlftynrmX': [round(maxlftynrmX, 5)], 'maxlftynrmY': [round(maxlftynrmY, 5)],
               'maxlftynrmZ': [round(maxlftynrmZ, 5)],
               'maxrgtynrmX': [round(maxrgtynrmX, 5)], 'maxrgtynrmY': [round(maxrgtynrmY, 5)],
               'maxrgtynrmZ': [round(maxrgtynrmZ, 5)]}

    # Başlangıçta hamveri yukarıdaki hesaplamalar ile işlendi
    # 'datason' kullanılarak DataFrame'e dönüştürülecek
    dfson = pd.DataFrame.from_records(datason)
    # Dönüştürülen yani artık tek satır olan CSV'nin 'islenmis_veri' klasörüne kaydedilmesi
    dfson.to_csv(prj_path+"\\\islenmisVeriler\\" + filename+".csv")

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
    plt.savefig(prj_path+"\\plot\\" + filename + ".jpg")
    plt.close()

#Non-ASD için feature extraction
for i in range(len(id_nonasd)):
    path=' '.join(map(str, dynmcData_nonasd[i]))
    if path=='None':
        continue

    firstname=' '.join(map(str, firstname_nonasd[i]))
    lastname=' '.join(map(str, lastname_nonasd[i]))
    filename="nonasd_"+firstname+lastname
    gender=' '.join(map(str, gender_nonasd[i]))
    bday=' '.join(map(str, birthday_nonasd[i]))
    viewrate=' '.join(map(str, viewrate_nonasd[i]))

    df=pd.read_csv(path)
    #satır sütun sayılarının değişkenelere atılması
    row_count, column_count=df.shape

    #Kullanılacak değişkenlerin başlangıç değerleri
    t1 = ""
    row = 0
    fix = 0
    sac = 0
    i = 0
    j = 0
    zerotime = time(00, 00, 00, 000000)
    totalsaccadetime = 0
    totalfixationtime = 0
    totaltime = 0
    totalsaccadetimee = 0
    totalCalcSaccadeTimeGeo = 0
    totalCalcFixationTimeGeo = 0
    totalCalcFixationTimeSocial = 0
    totalCalcSaccadeTimeSocial = 0
    countSacGeo = 0
    countSacSocial = 0
    countFixGeo = 0
    countFixSocial = 0
    status = "empty"
    default = time(00, 00, 00, 500000)
    # kullanılan zamanın formatı
    fmt = '%H:%M:%S.%f'


    # Zamanı saniye'ye dönüştürerek float cinsinden kaydeden fonksiyon
    def timeToFloat(timeF):
        # sanieye dönüştürme
        timee = timeF.microsecond * 0.000001 + timeF.second + timeF.minute * 60 + timeF.hour * 3600
        return timee

    # Zamanı string türünden time formatına döünştüren fonksiyon
    def dfToTime(t):
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        ms = int(t[9:15])
        # time formatına dönüştürme
        timeF = time(h, m, s, ms)
        return timeF

    # Üzerinde işlem yapılan CSV'nin tüm satırlarını gezerek inceleyen ve onu göre işlem yapan döngü
    for i in range(0, row_count - 1):
        if df.at[i, 'fixationStatus'] == "End":
            # zaman boş olduğu için ilk t1 in alındığı durum
            if t1 == "":
                t1 = df.at[i, 'fixationDuring']
                t1cntrl=[]
                t1cntrl=t1.split(':')
                if(len(t1cntrl[0])>2):
                    #print(df.shape)
                    df=df.drop([i])
                    #print(df.shape)
                    continue
                time1 = dfToTime(t1)
                #print(time1)

                # zaman alınmadan önce end olan satırlarda saccade etikitini bastırmak için
                if time1 < default:
                    # print("saccade")
                    df.at[i, 'status'] = "1"
                    status = "1"

                # zaman alınmadan önce end olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    # print("fixation")
                    df.at[i, 'status'] = "0"
                    status = "0"

            # zaman alındıktan sonraki end satırlarına  bastırmak için
            else:
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)

                # zaman alındıktan sonra end olan durumlarda saccade etiketini bastırmak için
                if time1 < default:
                    #print("saccade")
                    sac = sac + 1
                    row = 0
                    # Saccade ise status = 1
                    status = "1"

                # zaman alındıktan sonra end  olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    fix = fix + 1
                    row = 1
                    # fixation ise status = 0
                    status = "0"

            # Status değişkenine göre gerekli işlemler yapılıyor
            if status == "1":  # saccade
                # status değişkeni döngünün bir sonraki adımı için boşaltılıyor
                status = "empty"
                saccadetime = df.at[i, 'fixationDuring']
                df.at[i, 'saccadetime'] = saccadetime
                calcSaccadetimee = timeToFloat(dfToTime(saccadetime))
                totalsaccadetime = calcSaccadetimee + totalsaccadetime

                if df.at[i, 'side'] == 0:  # sol taraf geo
                    saccadeTimeGeo = df.at[i, 'fixationDuring']
                    calcSaccadeTimeGeo = timeToFloat(dfToTime(saccadeTimeGeo))
                    totalCalcSaccadeTimeGeo = calcSaccadeTimeGeo + totalCalcSaccadeTimeGeo
                    countSacGeo = countSacGeo + 1

                elif df.at[i, 'side'] == 1:  # sağ taraf    social
                    saccadeTimeSocial = df.at[i, 'fixationDuring']
                    calcSaccadeTimeSocial = timeToFloat(dfToTime(saccadeTimeSocial))
                    totalCalcSaccadeTimeSocial = calcSaccadeTimeSocial + totalCalcSaccadeTimeSocial
                    countSacSocial = countSacSocial + 1

            elif status == "0":  # fixation
                status = "empty"
                #print(status)
                fixationtime = df.at[i, 'fixationDuring']
                df.at[i, 'fixationtime'] = fixationtime
                calcFixationtimee = timeToFloat(dfToTime(fixationtime))
                totalfixationtime = calcFixationtimee + totalfixationtime

                if df.at[i, 'side'] == 0:  # sol taraf geo
                    fixationTimeGeo = df.at[i, 'fixationDuring']
                    calcFixationTimeGeo = timeToFloat(dfToTime(fixationTimeGeo))
                    totalCalcFixationTimeGeo = calcFixationTimeGeo + totalCalcFixationTimeGeo
                    countFixGeo = countFixGeo + 1

                elif df.at[i, 'side'] == 1:  # sağ taraf    social
                    fixationTimeSocial = df.at[i, 'fixationDuring']
                    calcFixationTimeSocial = timeToFloat(dfToTime(fixationTimeSocial))
                    totalCalcFixationTimeSocial = calcFixationTimeSocial + totalCalcFixationTimeSocial
                    countFixSocial = countFixSocial + 1

    # tekli satıra geçiş
    # totaltime=saccadetime+fixationtime
    totaltime = totalsaccadetime + totalfixationtime
    total = totalCalcSaccadeTimeGeo + totalCalcFixationTimeGeo + totalCalcSaccadeTimeSocial + totalCalcFixationTimeSocial
    totalFixationPercent = (totalfixationtime / (totalfixationtime + totalsaccadetime)) * 100
    totalSaccadePercent = (totalsaccadetime / (totalfixationtime + totalsaccadetime)) * 100

    if(totalfixationtime==0):
        totalFixGeoPercent=0
        totalFixSocPercent=0
    else:
        totalFixGeoPercent = (totalCalcFixationTimeGeo / totalfixationtime) * 100
        totalFixSocPercent = (totalCalcFixationTimeSocial / totalfixationtime) * 100

    if(totalsaccadetime==0):
        totalSacGeoPercent=0
        totalSacSocPercent=0
    else:
        totalSacGeoPercent = (totalCalcSaccadeTimeGeo / totalsaccadetime) * 100
        totalSacSocPercent = (totalCalcSaccadeTimeSocial / totalsaccadetime) * 100

    #Toplanan verilerin istatistiksel özellikleri
    df = df.dropna(subset=['fixationX'])
    #df = df.dropna(subset=['fixationY'])
    #mean
    meanfixX = statistics.mean(df['fixationX'])
    meanfixY = statistics.mean(df['fixationY'])
    meangzpX = statistics.mean(df['gazePointX'])
    meangzpY = statistics.mean(df['gazePointY'])
    meanhdrtX = statistics.mean(df['headRotationX'])
    meanhdrtY = statistics.mean(df['headRotationY'])
    meanhdrtZ = statistics.mean(df['headRotationZ'])
    meanhdpsX = statistics.mean(df['headPosX'])
    meanhdpsY = statistics.mean(df['headPosY'])
    meanhdpsZ = statistics.mean(df['headPosZ'])
    meanlfteyepsX = statistics.mean(df['leftEyePosX'])
    meanlfteyepsY = statistics.mean(df['leftEyePosY'])
    meanlfteyepsZ = statistics.mean(df['leftEyePosZ'])
    meanrgteyepsX = statistics.mean(df['rightEyePosX'])
    meanrgteyepsY = statistics.mean(df['rightEyePosY'])
    meanrgteyepsZ = statistics.mean(df['rightEyePosZ'])
    meanlftynrmX = statistics.mean(df['leftEyeNormalizedX'])
    meanlftynrmY = statistics.mean(df['leftEyeNormalizedY'])
    meanlftynrmZ = statistics.mean(df['leftEyeNormalizedZ'])
    meanrgtynrmX = statistics.mean(df['rightEyeNormalizedX'])
    meanrgtynrmY = statistics.mean(df['rightEyeNormalizedY'])
    meanrgtynrmZ = statistics.mean(df['rightEyeNormalizedZ'])
    #median
    medianfixX = statistics.median(df['fixationX'])
    medianfixY = statistics.median(df['fixationY'])
    mediangzpX = statistics.median(df['gazePointX'])
    mediangzpY = statistics.median(df['gazePointY'])
    medianhdrtX = statistics.median(df['headRotationX'])
    medianhdrtY = statistics.median(df['headRotationY'])
    medianhdrtZ = statistics.median(df['headRotationZ'])
    medianhdpsX = statistics.median(df['headPosX'])
    medianhdpsY = statistics.median(df['headPosY'])
    medianhdpsZ = statistics.median(df['headPosZ'])
    medianlfteyepsX = statistics.median(df['leftEyePosX'])
    medianlfteyepsY = statistics.median(df['leftEyePosY'])
    medianlfteyepsZ = statistics.median(df['leftEyePosZ'])
    medianrgteyepsX = statistics.median(df['rightEyePosX'])
    medianrgteyepsY = statistics.median(df['rightEyePosY'])
    medianrgteyepsZ = statistics.median(df['rightEyePosZ'])
    medianlftynrmX = statistics.median(df['leftEyeNormalizedX'])
    medianlftynrmY = statistics.median(df['leftEyeNormalizedY'])
    medianlftynrmZ = statistics.median(df['leftEyeNormalizedZ'])
    medianrgtynrmX = statistics.median(df['rightEyeNormalizedX'])
    medianrgtynrmY = statistics.median(df['rightEyeNormalizedY'])
    medianrgtynrmZ = statistics.median(df['rightEyeNormalizedZ'])
    #std
    stdfixX = statistics.stdev(df['fixationX'])
    stdfixY = statistics.stdev(df['fixationY'])
    stdgzpX = statistics.stdev(df['gazePointX'])
    stdgzpY = statistics.stdev(df['gazePointY'])
    stdhdrtX = statistics.stdev(df['headRotationX'])
    stdhdrtY = statistics.stdev(df['headRotationY'])
    stdhdrtZ = statistics.stdev(df['headRotationZ'])
    stdhdpsX = statistics.stdev(df['headPosX'])
    stdhdpsY = statistics.stdev(df['headPosY'])
    stdhdpsZ = statistics.stdev(df['headPosZ'])
    stdlfteyepsX = statistics.stdev(df['leftEyePosX'])
    stdlfteyepsY = statistics.stdev(df['leftEyePosY'])
    stdlfteyepsZ = statistics.stdev(df['leftEyePosZ'])
    stdrgteyepsX = statistics.stdev(df['rightEyePosX'])
    stdrgteyepsY = statistics.stdev(df['rightEyePosY'])
    stdrgteyepsZ = statistics.stdev(df['rightEyePosZ'])
    stdlftynrmX = statistics.stdev(df['leftEyeNormalizedX'])
    stdlftynrmY = statistics.stdev(df['leftEyeNormalizedY'])
    stdlftynrmZ = statistics.stdev(df['leftEyeNormalizedZ'])
    stdrgtynrmX = statistics.stdev(df['rightEyeNormalizedX'])
    stdrgtynrmY = statistics.stdev(df['rightEyeNormalizedY'])
    stdrgtynrmZ = statistics.stdev(df['rightEyeNormalizedZ'])
    #quantile %25
    q25fixX = np.percentile(df['fixationX'],25)
    q25fixY = np.percentile(df['fixationY'],25)
    q25gzpX = np.percentile(df['gazePointX'],25)
    q25gzpY = np.percentile(df['gazePointY'],25)
    q25hdrtX = np.percentile(df['headRotationX'],25)
    q25hdrtY = np.percentile(df['headRotationY'],25)
    q25hdrtZ = np.percentile(df['headRotationZ'],25)
    q25hdpsX = np.percentile(df['headPosX'],25)
    q25hdpsY = np.percentile(df['headPosY'],25)
    q25hdpsZ = np.percentile(df['headPosZ'],25)
    q25lfteyepsX = np.percentile(df['leftEyePosX'],25)
    q25lfteyepsY = np.percentile(df['leftEyePosY'],25)
    q25lfteyepsZ = np.percentile(df['leftEyePosZ'],25)
    q25rgteyepsX = np.percentile(df['rightEyePosX'],25)
    q25rgteyepsY = np.percentile(df['rightEyePosY'],25)
    q25rgteyepsZ = np.percentile(df['rightEyePosZ'],25)
    q25lftynrmX = np.percentile(df['leftEyeNormalizedX'],25)
    q25lftynrmY = np.percentile(df['leftEyeNormalizedY'],25)
    q25lftynrmZ = np.percentile(df['leftEyeNormalizedZ'],25)
    q25rgtynrmX = np.percentile(df['rightEyeNormalizedX'],25)
    q25rgtynrmY = np.percentile(df['rightEyeNormalizedY'],25)
    q25rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'],25)
    #quantiles %50
    q50fixX = np.percentile(df['fixationX'], 50)
    q50fixY = np.percentile(df['fixationY'], 50)
    q50gzpX = np.percentile(df['gazePointX'], 50)
    q50gzpY = np.percentile(df['gazePointY'], 50)
    q50hdrtX = np.percentile(df['headRotationX'], 50)
    q50hdrtY = np.percentile(df['headRotationY'], 50)
    q50hdrtZ = np.percentile(df['headRotationZ'], 50)
    q50hdpsX = np.percentile(df['headPosX'], 50)
    q50hdpsY = np.percentile(df['headPosY'], 50)
    q50hdpsZ = np.percentile(df['headPosZ'], 50)
    q50lfteyepsX = np.percentile(df['leftEyePosX'], 50)
    q50lfteyepsY = np.percentile(df['leftEyePosY'], 50)
    q50lfteyepsZ = np.percentile(df['leftEyePosZ'], 50)
    q50rgteyepsX = np.percentile(df['rightEyePosX'], 50)
    q50rgteyepsY = np.percentile(df['rightEyePosY'], 50)
    q50rgteyepsZ = np.percentile(df['rightEyePosZ'], 50)
    q50lftynrmX = np.percentile(df['leftEyeNormalizedX'], 50)
    q50lftynrmY = np.percentile(df['leftEyeNormalizedY'], 50)
    q50lftynrmZ = np.percentile(df['leftEyeNormalizedZ'], 50)
    q50rgtynrmX = np.percentile(df['rightEyeNormalizedX'], 50)
    q50rgtynrmY = np.percentile(df['rightEyeNormalizedY'], 50)
    q50rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'], 50)
    #quantile %75
    q75fixX = np.percentile(df['fixationX'], 75)
    q75fixY = np.percentile(df['fixationY'], 75)
    q75gzpX = np.percentile(df['gazePointX'], 75)
    q75gzpY = np.percentile(df['gazePointY'], 75)
    q75hdrtX = np.percentile(df['headRotationX'], 75)
    q75hdrtY = np.percentile(df['headRotationY'], 75)
    q75hdrtZ = np.percentile(df['headRotationZ'], 75)
    q75hdpsX = np.percentile(df['headPosX'], 75)
    q75hdpsY = np.percentile(df['headPosY'], 75)
    q75hdpsZ = np.percentile(df['headPosZ'], 75)
    q75lfteyepsX = np.percentile(df['leftEyePosX'], 75)
    q75lfteyepsY = np.percentile(df['leftEyePosY'], 75)
    q75lfteyepsZ = np.percentile(df['leftEyePosZ'], 75)
    q75rgteyepsX = np.percentile(df['rightEyePosX'], 75)
    q75rgteyepsY = np.percentile(df['rightEyePosY'], 75)
    q75rgteyepsZ = np.percentile(df['rightEyePosZ'], 75)
    q75lftynrmX = np.percentile(df['leftEyeNormalizedX'], 75)
    q75lftynrmY = np.percentile(df['leftEyeNormalizedY'], 75)
    q75lftynrmZ = np.percentile(df['leftEyeNormalizedZ'], 75)
    q75rgtynrmX = np.percentile(df['rightEyeNormalizedX'], 75)
    q75rgtynrmY = np.percentile(df['rightEyeNormalizedY'], 75)
    q75rgtynrmZ = np.percentile(df['rightEyeNormalizedZ'], 75)
    #min
    minfixX = min(df['fixationX'])
    minfixY = min(df['fixationY'])
    mingzpX = min(df['gazePointX'])
    mingzpY = min(df['gazePointY'])
    minhdrtX = min(df['headRotationX'])
    minhdrtY = min(df['headRotationY'])
    minhdrtZ = min(df['headRotationZ'])
    minhdpsX = min(df['headPosX'])
    minhdpsY = min(df['headPosY'])
    minhdpsZ = min(df['headPosZ'])
    minlfteyepsX = min(df['leftEyePosX'])
    minlfteyepsY = min(df['leftEyePosY'])
    minlfteyepsZ = min(df['leftEyePosZ'])
    minrgteyepsX =min(df['rightEyePosX'])
    minrgteyepsY = min(df['rightEyePosY'])
    minrgteyepsZ =min(df['rightEyePosZ'])
    minlftynrmX = min(df['leftEyeNormalizedX'])
    minlftynrmY = min(df['leftEyeNormalizedY'])
    minlftynrmZ = min(df['leftEyeNormalizedZ'])
    minrgtynrmX = min(df['rightEyeNormalizedX'])
    minrgtynrmY = min(df['rightEyeNormalizedY'])
    minrgtynrmZ = min(df['rightEyeNormalizedZ'])
    #max
    maxfixX = max(df['fixationX'])
    maxfixY = max(df['fixationY'])
    maxgzpX = max(df['gazePointX'])
    maxgzpY = max(df['gazePointY'])
    maxhdrtX = max(df['headRotationX'])
    maxhdrtY = max(df['headRotationY'])
    maxhdrtZ = max(df['headRotationZ'])
    maxhdpsX =max(df['headPosX'])
    maxhdpsY = max(df['headPosY'])
    maxhdpsZ = max(df['headPosZ'])
    maxlfteyepsX = max(df['leftEyePosX'])
    maxlfteyepsY = max(df['leftEyePosY'])
    maxlfteyepsZ = max(df['leftEyePosZ'])
    maxrgteyepsX = max(df['rightEyePosX'])
    maxrgteyepsY = max(df['rightEyePosY'])
    maxrgteyepsZ =max(df['rightEyePosZ'])
    maxlftynrmX = max(df['leftEyeNormalizedX'])
    maxlftynrmY = max(df['leftEyeNormalizedY'])
    maxlftynrmZ = max(df['leftEyeNormalizedZ'])
    maxrgtynrmX = max(df['rightEyeNormalizedX'])
    maxrgtynrmY = max(df['rightEyeNormalizedY'])
    maxrgtynrmZ = max(df['rightEyeNormalizedZ'])

    # Tüm hesaplamalar için oluşturulacak tek satırlık DataFrame'in verileri
    datason = {'name': [firstname],'lastname': [lastname],'label': 0,
               'gender': [gender],'birthday':[bday],'viewrate':[viewrate],
                'ttlFixationTime': [round(totalfixationtime,5)], 'ttlSaccadeTime': [round(totalsaccadetime,5)], 'ttlTime': [round(totaltime,5)],
               'fixationCount': [fix], 'saccadeCount': [sac],
               'ttlFixPerc': [round(totalFixationPercent,5)], 'ttlSacPerc': [round(totalSaccadePercent,5)],
               'ttlFixGeoPerc': [round(totalFixGeoPercent,5)], 'ttlFixSocPerc': [round(totalFixSocPercent,5)],
               'ttlSacGeoPerc': [round(totalSacGeoPercent,5)], 'ttlSacSocPerc': [round(totalSacSocPercent,5)],
               'ttlFixTimeGeo': [round(totalCalcFixationTimeGeo,5)], 'ttlFixTimeSoc': [round(totalCalcFixationTimeSocial,5)],
               'ttlSacTimeGeo': [round(totalCalcSaccadeTimeGeo,5)], 'ttlSacTimeSoc': [round(totalCalcSaccadeTimeSocial,5)],
               'cntFixGeo': [round(countFixGeo,5)], 'cntFixSoc': [round(countFixSocial,5)],
               'cntSacGeo': [round(countSacGeo,5)], 'cntSacSoc': [round(countSacSocial,5)],
               'meanfixX': [round(meanfixX,5)], 'meanfixY': [round(meanfixY,5)],'meangzpX': [round(meangzpX,5)],'meangzpY': [round(meangzpY,5)],
               'meanhdrtX': [round(meanhdrtX,5)],'meanhdrtY': [round(meanhdrtY,5)],'meanhdrtZ': [round(meanhdrtZ,5)],
               'meanhdpsX': [round(meanhdpsX,5)],'meanhdpsY': [round(meanhdpsY,5)],'meanhdpsZ': [round(meanhdpsZ,5)],
               'meanlfteyepsX': [round(meanlfteyepsX,5)],'meanlfteyepsY': [round(meanlfteyepsY,5)],'meanlfteyepsZ': [round(meanlfteyepsZ,5)],
               'meanrghteyepsX': [round(meanrgteyepsX,5)],'meanrghteyepsY': [round(meanrgteyepsY,5)],'meanrghteyepsZ': [round(meanrgteyepsZ,5)],
               'meanlftynrmX': [round(meanlftynrmX,5)],'meanlftynrmY': [round(meanlftynrmY,5)],'meanlftynrmZ': [round(meanlftynrmZ,5)],
               'meanrgtynrmX': [round(meanrgtynrmX,5)],'meanrgtynrmY': [round(meanrgtynrmY,5)],'meanrgtynrmZ': [round(meanrgtynrmZ,5)],
               'medianfixX': [round(medianfixX,5)], 'medianfixY': [round(medianfixY,5)], 'mediangzpX': [round(mediangzpX,5)], 'mediangzpY': [round(mediangzpY,5)],
               'medianhdrtX': [round(medianhdrtX,5)], 'medianhdrtY': [round(medianhdrtY,5)], 'medianhdrtZ': [round(medianhdrtZ,5)],
               'medianhdpsX': [round(medianhdpsX,5)], 'medianhdpsY': [round(medianhdpsY,5)], 'medianhdpsZ': [round(medianhdpsZ,5)],
               'medianlfteyepsX': [round(medianlfteyepsX,5)], 'medianlfteyepsY': [round(medianlfteyepsY,5)], 'medianlfteyepsZ': [round(medianlfteyepsZ,5)],
               'medianrghteyepsX': [round(medianrgteyepsX,5)], 'medianrghteyepsY': [round(medianrgteyepsY,5)],
               'medianrghteyepsZ': [round(medianrgteyepsZ,5)],
               'medianlftynrmX': [round(medianlftynrmX,5)], 'medianlftynrmY': [round(medianlftynrmY,5)], 'medianlftynrmZ': [round(medianlftynrmZ,5)],
               'medianrgtynrmX': [round(medianrgtynrmX,5)], 'medianrgtynrmY': [round(medianrgtynrmY,5)], 'medianrgtynrmZ': [round(medianrgtynrmZ,5)],
               'stdfixX': [round(stdfixX,5)], 'stdfixY': [round(stdfixY,5)], 'stdgzpX': [round(stdgzpX,5)],
               'stdgzpY': [round(stdgzpY,5)],
               'stdhdrtX': [round(stdhdrtX,5)], 'stdhdrtY': [round(stdhdrtY,5)], 'stdhdrtZ': [round(stdhdrtZ,5)],
               'stdhdpsX': [round(stdhdpsX,5)], 'stdhdpsY': [round(stdhdpsY,5)], 'stdhdpsZ': [round(stdhdpsZ,5)],
               'stdlfteyepsX': [round(stdlfteyepsX,5)], 'stdlfteyepsY': [round(stdlfteyepsY,5)],
               'stdlfteyepsZ': [round(stdlfteyepsZ,5)],
               'stdrghteyepsX': [round(stdrgteyepsX,5)], 'stdrghteyepsY': [round(stdrgteyepsY,5)],
               'stdrghteyepsZ': [round(stdrgteyepsZ,5)],
               'stdlftynrmX': [round(stdlftynrmX,5)], 'stdlftynrmY': [round(stdlftynrmY,5)],
               'stdlftynrmZ': [round(stdlftynrmZ,5)],
               'stdrgtynrmX': [round(stdrgtynrmX,5)], 'stdrgtynrmY': [round(stdrgtynrmY,5)],
               'stdrgtynrmZ': [round(stdrgtynrmZ,5)],
               'q25fixX': [round(q25fixX,5)], 'q25fixY': [round(q25fixY,5)], 'q25gzpX': [round(q25gzpX,5)],
               'q25gzpY': [round(q25gzpY,5)],
               'q25hdrtX': [round(q25hdrtX,5)], 'q25hdrtY': [round(q25hdrtY,5)], 'q25hdrtZ': [round(q25hdrtZ,5)],
               'q25hdpsX': [round(q25hdpsX,5)], 'q25hdpsY': [round(q25hdpsY,5)], 'q25hdpsZ': [round(q25hdpsZ,5)],
               'q25lfteyepsX': [round(q25lfteyepsX,5)], 'q25lfteyepsY': [round(q25lfteyepsY,5)],
               'q25lfteyepsZ': [round(q25lfteyepsZ,5)],
               'q25rghteyepsX': [round(q25rgteyepsX,5)], 'q25rghteyepsY': [round(q25rgteyepsY,5)],
               'q25rghteyepsZ': [round(q25rgteyepsZ,5)],
               'q25lftynrmX': [round(q25lftynrmX,5)], 'q25lftynrmY': [round(q25lftynrmY,5)],
               'q25lftynrmZ': [round(q25lftynrmZ,5)],
               'q25rgtynrmX': [round(q25rgtynrmX,5)], 'q25rgtynrmY': [round(q25rgtynrmY,5)],
               'q25rgtynrmZ': [round(q25rgtynrmZ,5)],
               'q50fixX': [round(q50fixX,5)], 'q50fixY': [round(q50fixY,5)], 'q50gzpX': [round(q50gzpX,5)],
               'q50gzpY': [round(q50gzpY,5)],
               'q50hdrtX': [round(q50hdrtX,5)], 'q50hdrtY': [round(q50hdrtY,5)], 'q50hdrtZ': [round(q50hdrtZ,5)],
               'q50hdpsX': [round(q50hdpsX,5)], 'q50hdpsY': [round(q50hdpsY,5)], 'q50hdpsZ': [round(q50hdpsZ,5)],
               'q50lfteyepsX': [round(q50lfteyepsX,5)], 'q50lfteyepsY': [round(q50lfteyepsY,5)],
               'q50lfteyepsZ': [round(q50lfteyepsZ,5)],
               'q50rghteyepsX': [round(q50rgteyepsX,5)], 'q50rghteyepsY': [round(q50rgteyepsY,5)],
               'q50rghteyepsZ': [round(q50rgteyepsZ,5)],
               'q50lftynrmX': [round(q50lftynrmX,5)], 'q50lftynrmY': [round(q50lftynrmY,5)],
               'q50lftynrmZ': [round(q50lftynrmZ,5)],
               'q50rgtynrmX': [round(q50rgtynrmX,5)], 'q50rgtynrmY': [round(q50rgtynrmY,5)],
               'q50rgtynrmZ': [round(q50rgtynrmZ,5)],
               'q75fixX': [round(q75fixX,5)], 'q75fixY': [round(q75fixY,5)], 'q75gzpX': [round(q75gzpX,5)],
               'q75gzpY': [round(q75gzpY,5)],
               'q75hdrtX': [round(q75hdrtX,5)], 'q75hdrtY': [round(q75hdrtY,5)], 'q75hdrtZ': [round(q75hdrtZ,5)],
               'q75hdpsX': [round(q75hdpsX,5)], 'q75hdpsY': [round(q75hdpsY,5)], 'q75hdpsZ': [round(q75hdpsZ,5)],
               'q75lfteyepsX': [round(q75lfteyepsX,5)], 'q75lfteyepsY': [round(q75lfteyepsY,5)],
               'q75lfteyepsZ': [round(q75lfteyepsZ,5)],
               'q75rghteyepsX': [round(q75rgteyepsX,5)], 'q75rghteyepsY': [round(q75rgteyepsY,5)],
               'q75rghteyepsZ': [round(q75rgteyepsZ,5)],
               'q75lftynrmX': [round(q75lftynrmX,5)], 'q75lftynrmY': [round(q75lftynrmY,5)],
               'q75lftynrmZ': [round(q75lftynrmZ,5)],
               'q75rgtynrmX': [round(q75rgtynrmX,5)], 'q75rgtynrmY': [round(q75rgtynrmY,5)],
               'q75rgtynrmZ': [round(q75rgtynrmZ,5)],
               'minfixX': [round(minfixX,5)], 'minfixY': [round(minfixY,5)], 'mingzpX': [round(mingzpX,5)],
               'mingzpY': [round(mingzpY,5)],
               'minhdrtX': [round(minhdrtX,5)], 'minhdrtY': [round(minhdrtY,5)], 'minhdrtZ': [round(minhdrtZ,5)],
               'minhdpsX': [round(minhdpsX,5)], 'minhdpsY': [round(minhdpsY,5)], 'minhdpsZ': [round(minhdpsZ,5)],
               'minlfteyepsX': [round(minlfteyepsX,5)], 'minlfteyepsY': [round(minlfteyepsY,5)],
               'minlfteyepsZ': [round(minlfteyepsZ,5)],
               'minrghteyepsX': [round(minrgteyepsX,5)], 'minrghteyepsY': [round(minrgteyepsY,5)],
               'minrghteyepsZ': [round(minrgteyepsZ,5)],
               'minlftynrmX': [round(minlftynrmX,5)], 'minlftynrmY': [round(minlftynrmY,5)],
               'minlftynrmZ': [round(minlftynrmZ,5)],
               'minrgtynrmX': [round(minrgtynrmX,5)], 'minrgtynrmY': [round(minrgtynrmY,5)],
               'minrgtynrmZ': [round(minrgtynrmZ,5)],
               'maxfixX': [round(maxfixX,5)], 'maxfixY': [round(maxfixY,5)], 'maxgzpX': [round(maxgzpX,5)],
               'maxgzpY': [round(maxgzpY,5)],
               'maxhdrtX': [round(maxhdrtX,5)], 'maxhdrtY': [round(maxhdrtY,5)], 'maxhdrtZ': [round(maxhdrtZ,5)],
               'maxhdpsX': [round(maxhdpsX,5)], 'maxhdpsY': [round(maxhdpsY,5)], 'maxhdpsZ': [round(maxhdpsZ,5)],
               'maxlfteyepsX': [round(maxlfteyepsX,5)], 'maxlfteyepsY': [round(maxlfteyepsY,5)],
               'maxlfteyepsZ': [round(maxlfteyepsZ,5)],
               'maxrghteyepsX': [round(maxrgteyepsX,5)], 'maxrghteyepsY': [round(maxrgteyepsY,5)],
               'maxrghteyepsZ': [round(maxrgteyepsZ,5)],
               'maxlftynrmX': [round(maxlftynrmX,5)], 'maxlftynrmY': [round(maxlftynrmY,5)],
               'maxlftynrmZ': [round(maxlftynrmZ,5)],
               'maxrgtynrmX': [round(maxrgtynrmX,5)], 'maxrgtynrmY': [round(maxrgtynrmY,5)],
               'maxrgtynrmZ': [round(maxrgtynrmZ,5)]}

    # Başlangıçta hamveri yukarıdaki hesaplamalar ile işlendi
    # 'datason' kullanılarak DataFrame'e dönüştürülecek
    dfson = pd.DataFrame.from_records(datason)
    # Dönüştürülen yani artık tek satır olan CSV'nin 'islenmis_veri' klasörüne kaydedilmesi
    dfson.to_csv(prj_path+"\\\islenmisVeriler\\" + filename+".csv")

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
    plt.savefig(prj_path+"\\plot\\" + filename + ".jpg")
    plt.close()

#Tüm işlenmiş CSV'lerin tek bir CSV'de birleştirilmesi
#united CSV için önce boş bir CSV oluşturulur
united_csv=pd.DataFrame()

#İşlenmiş CSVlerin aldığı klasörün yolu
islenmisDirectory=os.fsencode(prj_path+"\\islenmisVeriler\\")

#İşlenmişveri klasöründeki dosya sayısı kadar çalışan bir döngü
for file in os.listdir(islenmisDirectory):
    filename=os.fsdecode(file)
    if united_csv.empty:
        united_csv=pd.read_csv(prj_path+"\\islenmisVeriler\\"+filename)
        #bu satır ile for döngüsünde oluşturulan boş 'Unnamed' sütunu siliniyor
        united_csv=united_csv.loc[:, ~united_csv.columns.str.contains('Unnamed')]
    else:
        new_df=pd.read_csv(prj_path+"\\islenmisVeriler\\"+filename)
        # bu satır ile for döngüsünde oluşturulan boş 'Unnamed' sütunu siliniyor
        new_df=new_df.loc[:, ~new_df.columns.str.contains('Unnamed')]
        #CSVlerin birleştirilmesi
        united_csv=pd.concat([united_csv,new_df],ignore_index=True)


#United CSV'nin kaydedilmesi
#indexsiz
united_csv.to_csv(prj_path+"\\united.csv",index=False)
##indexli
#united_csv.to_csv(path+"\\train_dataset\\united.csv")
