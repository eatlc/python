import pandas as pd
import numpy as np
import os
import statistics

YeksOrt=[]
txt_path=("C:\\Users\\esra2\\Documents\\OTET\\OTETHamcsv\\nonASDortalamalar_Xekseni.txt")
csv_path=("C:\\Users\\esra2\\Documents\\OTET\\OTETHamcsv\\nonASD")
directory= os.fsencode("C:\\Users\\esra2\\Documents\\OTET\\OTETHamcsv\\nonASD")

for file in os.listdir(directory):
    filename=os.fsdecode(file)
    #print(filename)
    df=pd.read_csv(csv_path+"\\"+filename)
    childname=filename.split('_')
    #print(childname[0])
    df = df.dropna(axis=0)
    YeksOrt.append(statistics.mean(df['fixationX']))
    YeksOrt1=statistics.mean(df['fixationX'])
    print(childname[0],YeksOrt1)

    with open(txt_path, "a+") as f:
        f.write(childname[0]+" "+str(YeksOrt1)+ "\n")
        f.close()

print("-"*20)
print("max:",max(YeksOrt))
print("min:",min(YeksOrt))
print("ort:", statistics.mean(YeksOrt))

with open(txt_path, "a+") as f:
    f.write("-"*20 + "\n")
    f.write("max:"+str(max(YeksOrt))+ "\n")
    f.write("min:"+str(min(YeksOrt)) + "\n")
    f.write("ort:"+ str(statistics.mean(YeksOrt)) + "\n")
    f.close()
