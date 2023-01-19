import pandas as pd
from datetime import datetime,date
from datetime import time, timedelta
import statistics
import numpy as np
import matplotlib.pyplot as plt
import os
import sklearn
import pickle


path="C:\\Users\\esra2\\Documents\\OTET\\OTETHamcsv"
#hamverilerin yani C# üzerinden alınan verilerin bulunduğu dosya yolu
hamveridirectory1=os.fsencode(path+"\\ASD\\")

hamveridirectory2=os.fsencode(path+"\\nonASD\\")


#ASD için
#Hamverilerin sayısınca çalışacak bir döngü oluşturuldu
#amaç kaydedilen tüm CSV'lerin işlenmesi ve 'islanmis_veri' klasörüne ayrı ayrı kaydedilmesi
for file in os.listdir(hamveridirectory1):
    filename=os.fsdecode(file)
    print(filename)
    #dosyadan CSV okur
    df=pd.read_csv(path+"\\ASD\\"+filename)

    #DataFrame C#dan ilk hgeldiğinde naşlangıçta 05.55.3343 gibi bir süre gönderiyor onu burada siliyorum.
    #başka çözüm bulunursa bu satır silinebilir
    df=df.drop([0]).reset_index(drop=True)
    # satır sayısını bulup değişkene atıyor
    row_count, coulmn_count = df.shape

    #Kullanılan değişkenleri başlangıç değerleri
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
    status="empty"
    default = time(00, 00, 00, 500000)
    #kullanılan zamanın formatı
    fmt = '%H:%M:%S.%f'

    #Zamanı saniye'ye dönüştürerek float cinsinden kaydeden fonksiyon
    def timeToFloat(timeF):
        # sanieye dönüştürme
        timee = timeF.microsecond * 0.000001 + timeF.second + timeF.minute * 60 + timeF.hour * 3600
        return timee

    #Zamanı string türünden time formatına döünştüren fonksiyon
    def dfToTime(t):
        print(t)
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        ms = int(t[9:15])
        # time formatına dönüştürme
        timeF = time(h, m, s, ms)
        return timeF

    #Üzerinde işlem yapılan CSV'nin tüm satırlarını gezerek inceleyen ve onu göre işlem yapan döngü
    for i in range(0, row_count - 1):

        if df.at[i, 'fixationStatus'] == "End":
            # zaman boş olduğu için ilk t1 in alındığı durum
            if t1 == "":
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)
                # zaman alınmadan önce end olan satırlarda saccade etikitini bastırmak için
                if time1 < default:
                    #print("saccade")
                    df.at[i, 'status'] = "1"
                    status="1"

                # zaman alınmadan önce end olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    df.at[i, 'status'] = "0"
                    status="0"

            # zaman alındıktan sonraki end satırlarına  bastırmak için
            else:
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)

                # zaman alındıktan sonra end olan durumlarda saccade etiketini bastırmak için
                if time1 < default:
                    #print("saccade")
                    sac = sac + 1
                    row = 0
                    #Saccade ise status = 1
                    status="1"

                # zaman alındıktan sonra end  olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    fix = fix + 1
                    row = 1
                    #fixation ise status = 0
                    status="0"

            #Status değişkenine göre gerekli işlemler yapılıyor
            if status == "1":  # saccade
                #status değişkeni döngünün bir sonraki adımı için boşaltılıyor
                status="empty"
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
                status="empty"
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

    totalFixGeoPercent = (totalCalcFixationTimeGeo / totalfixationtime) * 100
    totalFixSocPercent = (totalCalcFixationTimeSocial / totalfixationtime) * 100
    totalSacGeoPercent = (totalCalcSaccadeTimeGeo / totalsaccadetime) * 100
    totalSacSocPercent = (totalCalcSaccadeTimeSocial / totalsaccadetime) * 100

    #FixatinX ve fixationY değerlerinin İstatistiksel Özellikleri
    df = df.dropna(subset=['fixationX'])
    # mean
    mean_x = statistics.mean(df['fixationX'])
    mean_y = statistics.mean(df['fixationY'])
    # median
    median_x = statistics.median(df['fixationX'])
    median_y = statistics.median(df['fixationY'])
    # std
    std_x = statistics.stdev(df['fixationX'])
    std_y = statistics.stdev(df['fixationY'])
    # quantile %25
    q25_x = np.percentile(df['fixationX'], 25)
    q25_y = np.percentile(df['fixationY'], 25)
    # quantiles %50
    q50_x = np.percentile(df['fixationX'], 50)
    q50_y = np.percentile(df['fixationY'], 50)
    # quantiles %75
    q75_x = np.percentile(df['fixationX'], 75)
    q75_y = np.percentile(df['fixationY'], 75)
    # min
    min_x = min(df['fixationX'])
    min_y = min(df['fixationY'])
    # max
    max_x = max(df['fixationX'])
    max_y = max(df['fixationY'])

    #Tüm hesaplamalar için oluşturulacak tek satırlık DataFrame'in verileri
    datason = {'ttlFixationTime': [totalfixationtime], 'ttlSaccadeTime': [totalsaccadetime], 'ttlTime': [totaltime],
               'fixationCount': [fix], 'saccadeCount': [sac],
               'ttlFixPerc': [totalFixationPercent], 'ttlSacPerc': [totalSaccadePercent],
               'ttlFixGeoPerc': [totalFixGeoPercent], 'ttlFixSocPerc': [totalFixSocPercent],
               'ttlSacGeoPerc': [totalSacGeoPercent], 'ttlSacSocPerc': [totalSacSocPercent],
               'ttlFixTimeGeo': [totalCalcFixationTimeGeo], 'ttlFixTimeSoc': [totalCalcFixationTimeSocial],
               'ttlSacTimeGeo': [totalCalcSaccadeTimeGeo], 'ttlSacTimeSoc': [totalCalcSaccadeTimeSocial],
               'cntFixGeo': [countFixGeo], 'cntFixSoc': [countFixSocial],
               'cntSacGeo': [countSacGeo], 'cntSacSoc': [countSacSocial], 'meanX': [mean_x], 'meanY': [mean_y],
               'medianX': [median_x], 'medianY': [median_y],
               'stdX': [std_x], 'stdY': [std_y], 'qntls25X': [q25_x], 'qntls25Y': [q25_y], 'qntls50X': [q50_x],
               'qntls50Y': [q50_y], 'qntls75X': [q75_x],
               'qntls75Y': [q75_y], 'minX': [min_x], 'minY': [min_y], 'maxX': [max_x], 'maxY': [max_y],'label':1}

    #Başlangıçta hamveri yukarıdaki hesaplamalar ile işlendi
    #'datason' kullanılarak DataFrame'e dönüştürülecek
    dfson = pd.DataFrame.from_records(datason)
    #Dönüştürülen yani artık tek satır olan CSV'nin 'islenmis_veri' klasörüne kaydedilmesi
    dfson.to_csv(path +"\\islenmisVeri\\"+"ASD"+filename)

    #GRAFİK
    """x1, y1 = [965, 965],[0,1200]
    plt.plot(x1,y1)
    plt.plot(df['fixationX'], df['fixationY'],linestyle='',color='r',marker='*',label='Sizin Takibiniz',alpha=0.3)
    plt.plot(df['fixationX'], df['fixationY'],linestyle='-',alpha=0.2)
    plt.axvspan(0,965,facecolor='b',alpha=0.2)
    plt.axvspan(965,1800,facecolor='r',alpha=0.2)
    #
    plt.xlim(170, 1800)
    plt.ylim(1200,0)
    plt.xlabel('X')
    plt.ylabel('Y')
    #Grafiğin kaydedilmesi
    plt.savefig(path+"\\plot\\"+filename+".jpg")
    plt.close()"""
    #print("ASD filename: ", filename)
#for döngüsünün bitişi, yukarıdaki satırlar 'hamveri' klasöründeki tüm dosyalar için ayrı ayrı çalıştı

#non-ASD için
for file in os.listdir(hamveridirectory2):
    filename=os.fsdecode(file)

    #dosyadan CSV okur
    df=pd.read_csv(path+"\\nonASD\\"+filename)

    #DataFrame C#dan ilk hgeldiğinde naşlangıçta 05.55.3343 gibi bir süre gönderiyor onu burada siliyorum.
    #başka çözüm bulunursa bu satır silinebilir
    df=df.drop([0]).reset_index(drop=True)
    # satır sayısını bulup değişkene atıyor
    row_count, coulmn_count = df.shape

    #Kullanılan değişkenleri başlangıç değerleri
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
    status="empty"
    default = time(00, 00, 00, 500000)
    #kullanılan zamanın formatı
    fmt = '%H:%M:%S.%f'

    #Zamanı saniye'ye dönüştürerek float cinsinden kaydeden fonksiyon
    def timeToFloat(timeF):
        # sanieye dönüştürme
        timee = timeF.microsecond * 0.000001 + timeF.second + timeF.minute * 60 + timeF.hour * 3600
        return timee

    #Zamanı string türünden time formatına döünştüren fonksiyon
    def dfToTime(t):
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        ms = int(t[9:15])
        # time formatına dönüştürme
        timeF = time(h, m, s, ms)
        return timeF

    #Üzerinde işlem yapılan CSV'nin tüm satırlarını gezerek inceleyen ve onu göre işlem yapan döngü
    for i in range(0, row_count - 1):

        if df.at[i, 'fixationStatus'] == "End":
            # zaman boş olduğu için ilk t1 in alındığı durum
            if t1 == "":
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)
                # zaman alınmadan önce end olan satırlarda saccade etikitini bastırmak için
                if time1 < default:
                    #print("saccade")
                    df.at[i, 'status'] = "1"
                    status="1"

                # zaman alınmadan önce end olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    df.at[i, 'status'] = "0"
                    status="0"

            # zaman alındıktan sonraki end satırlarına  bastırmak için
            else:
                t1 = df.at[i, 'fixationDuring']
                time1 = dfToTime(t1)

                # zaman alındıktan sonra end olan durumlarda saccade etiketini bastırmak için
                if time1 < default:
                    #print("saccade")
                    sac = sac + 1
                    row = 0
                    #Saccade ise status = 1
                    status="1"

                # zaman alındıktan sonra end  olan durumlarda fixation etiketini bastırmak için
                elif time1 >= default:
                    #print("fixation")
                    fix = fix + 1
                    row = 1
                    #fixation ise status = 0
                    status="0"

            #Status değişkenine göre gerekli işlemler yapılıyor
            if status == "1":  # saccade
                #status değişkeni döngünün bir sonraki adımı için boşaltılıyor
                status="empty"
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
                status="empty"
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

    totalFixGeoPercent = (totalCalcFixationTimeGeo / totalfixationtime) * 100
    totalFixSocPercent = (totalCalcFixationTimeSocial / totalfixationtime) * 100
    totalSacGeoPercent = (totalCalcSaccadeTimeGeo / totalsaccadetime) * 100
    totalSacSocPercent = (totalCalcSaccadeTimeSocial / totalsaccadetime) * 100

    #FixatinX ve fixationY değerlerinin İstatistiksel Özellikleri
    df = df.dropna(subset=['fixationX'])
    # mean
    mean_x = statistics.mean(df['fixationX'])
    mean_y = statistics.mean(df['fixationY'])
    # median
    median_x = statistics.median(df['fixationX'])
    median_y = statistics.median(df['fixationY'])
    # std
    std_x = statistics.stdev(df['fixationX'])
    std_y = statistics.stdev(df['fixationY'])
    # quantile %25
    q25_x = np.percentile(df['fixationX'], 25)
    q25_y = np.percentile(df['fixationY'], 25)
    # quantiles %50
    q50_x = np.percentile(df['fixationX'], 50)
    q50_y = np.percentile(df['fixationY'], 50)
    # quantiles %75
    q75_x = np.percentile(df['fixationX'], 75)
    q75_y = np.percentile(df['fixationY'], 75)
    # min
    min_x = min(df['fixationX'])
    min_y = min(df['fixationY'])
    # max
    max_x = max(df['fixationX'])
    max_y = max(df['fixationY'])

    #Tüm hesaplamalar için oluşturulacak tek satırlık DataFrame'in verileri
    datason = {'ttlFixationTime': [totalfixationtime], 'ttlSaccadeTime': [totalsaccadetime], 'ttlTime': [totaltime],
               'fixationCount': [fix], 'saccadeCount': [sac],
               'ttlFixPerc': [totalFixationPercent], 'ttlSacPerc': [totalSaccadePercent],
               'ttlFixGeoPerc': [totalFixGeoPercent], 'ttlFixSocPerc': [totalFixSocPercent],
               'ttlSacGeoPerc': [totalSacGeoPercent], 'ttlSacSocPerc': [totalSacSocPercent],
               'ttlFixTimeGeo': [totalCalcFixationTimeGeo], 'ttlFixTimeSoc': [totalCalcFixationTimeSocial],
               'ttlSacTimeGeo': [totalCalcSaccadeTimeGeo], 'ttlSacTimeSoc': [totalCalcSaccadeTimeSocial],
               'cntFixGeo': [countFixGeo], 'cntFixSoc': [countFixSocial],
               'cntSacGeo': [countSacGeo], 'cntSacSoc': [countSacSocial], 'meanX': [mean_x], 'meanY': [mean_y],
               'medianX': [median_x], 'medianY': [median_y],
               'stdX': [std_x], 'stdY': [std_y], 'qntls25X': [q25_x], 'qntls25Y': [q25_y], 'qntls50X': [q50_x],
               'qntls50Y': [q50_y], 'qntls75X': [q75_x],
               'qntls75Y': [q75_y], 'minX': [min_x], 'minY': [min_y], 'maxX': [max_x], 'maxY': [max_y],'label':0}

    #Başlangıçta hamveri yukarıdaki hesaplamalar ile işlendi
    #'datason' kullanılarak DataFrame'e dönüştürülecek
    dfson = pd.DataFrame.from_records(datason)
    #Dönüştürülen yani artık tek satır olan CSV'nin 'islenmis_veri' klasörüne kaydedilmesi
    dfson.to_csv(path +"\\islenmisVeri\\"+"nonASD"+filename)

    #GRAFİK
    """x1, y1 = [965, 965],[0,1200]
    plt.plot(x1,y1)
    plt.plot(df['fixationX'], df['fixationY'],linestyle='',color='m',marker='*',label='Sizin Takibiniz',alpha=0.3)
    plt.plot(df['fixationX'], df['fixationY'],linestyle='-',alpha=0.2)
    plt.axvspan(0,965,facecolor='y',alpha=0.2)
    plt.axvspan(965,2000,facecolor='g',alpha=0.2)
    #
    plt.xlim(50, 2000)
    plt.ylim(1200,0)
    plt.xlabel('X')
    plt.ylabel('Y')
    #Grafiğin kaydedilmesi
    ###plt.savefig(path+"\\plot\\"+filename+".jpg")
    plt.close()"""
    #print("nonASD filename: ", filename)

#for döngüsünün bitişi, yukarıdaki satırlar 'hamveri' klasöründeki tüm dosyalar için ayrı ayrı çalıştı

#Tüm işlenmiş CSV'lerin tek bir CSV'de birleştirilmesi
#united CSV için önce boş bir CSV oluşturulur
united_csv=pd.DataFrame()

#İşlenmiş CSVlerin aldığı klasörün yolu
islenmisDirectory=os.fsencode(path+"\\islenmisVeri\\")

#İşlenmişveri klasöründeki dosya sayısı kadar çalışan bir döngü
for file in os.listdir(islenmisDirectory):
    filename=os.fsdecode(file)
    if united_csv.empty:
        united_csv=pd.read_csv(path+"\\islenmisVeri\\"+filename)
        #bu satır ile for döngüsünde oluşturulan boş 'Unnamed' sütunu siliniyor
        united_csv=united_csv.loc[:, ~united_csv.columns.str.contains('Unnamed')]
    else:
        new_df=pd.read_csv(path+"\\islenmisVeri\\"+filename)
        # bu satır ile for döngüsünde oluşturulan boş 'Unnamed' sütunu siliniyor
        new_df=new_df.loc[:, ~new_df.columns.str.contains('Unnamed')]
        #CSVlerin birleştirilmesi
        united_csv=pd.concat([united_csv,new_df],ignore_index=True)

#United CSV'nin kaydedilmesi
#indexsiz
united_csv.to_csv(path+"\\united.csv",index=False)
##indexli
#united_csv.to_csv(path+"\\train_dataset\\united.csv")

