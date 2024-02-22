import pandas as pd
from datetime import datetime as dt
import datetime
import pytz
import tkinter as tk
from tkinter import filedialog
import calendar
import math

now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

today=f'{now.year}/{now.month}/{now.day} {now.hour}'

def small():
    root.geometry("450x255")
def mid():
    root.geometry("1100x255")
def large():
    root.geometry("1100x960")

def repeat():
    calcButton()
    #print("test")
    root.after(60000,repeat)


def referenceButton():
    filename = filedialog.askopenfilename(initialdir="C:\\")
    fileBox.delete(0, tk.END)
    fileBox.insert(tk.END,filename)
    print(filename)
    with open(textfile,"w") as f:
        f.write(filename)

def calcButton():
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    filename=fileBox.get()
    df=pd.read_csv(filename,encoding='shift_jis')

    nowtext=f"最終更新：{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

    finalupdate.configure(state="normal")#以下入力
    finalupdate.delete(0, tk.END)
    finalupdate.insert(tk.END,nowtext)
    finalupdate.configure(state="readonly")    

    i=0
    while (dt.strptime(df.iat[len(df)-1-i,0],'%Y/%m/%d %H:%M:%S')-datetime.datetime(now.year,now.month,now.day,now.hour,0,0)).total_seconds()>0:
        i=i+1
    print(i)
    if i==0:
        i=1
    nowhourdf=df[df['日時'].str.contains(df.iat[len(df)-i,0])]
    print(nowhourdf)
    i=0
    if (now.hour-1)%24==23:
        nowday=now.day-1
    else:
        nowday=now.day
    while (dt.strptime(df.iat[len(df)-1-i,0],'%Y/%m/%d %H:%M:%S')-datetime.datetime(now.year,now.month,nowday,(now.hour-1)%24,0,0)).total_seconds()>0:
        i=i+1
    if i==0:
        i=1
    onehourdf=df[df['日時'].str.contains(df.iat[len(df)-i,0])]
    dexp=nowhourdf.iat[0,10]-onehourdf.iat[0,10]
    dtime =(dt.strptime(nowhourdf.iat[0,0],'%Y/%m/%d %H:%M:%S')-dt.strptime(onehourdf.iat[0,0],'%Y/%m/%d %H:%M:%S')).total_seconds()
    sph=round(dexp/dtime*3600*7/10000,3)
    sph_time=f"・戦果時速：{(dt.strptime(onehourdf.iat[0,0],'%Y/%m/%d %H:%M:%S')).hour}:00~{(dt.strptime(nowhourdf.iat[0,0],'%Y/%m/%d %H:%M:%S')).hour}:00の時速は",sph
    sphBox.configure(state="normal")#以下入力
    sphBox.delete(0, tk.END)
    sphBox.insert(tk.END,sph_time)
    sphBox.configure(state="readonly")

    with open(sph_setfile,"w") as f:
        f.write(sph_set.get())

    if val_sphset.get() == True:
        sph=float(sph_set.get())

    intnowhour=now.hour
    i=0
    while (dt.strptime(df.iat[len(df)-1-i,0],'%Y/%m/%d %H:%M:%S')-am_time(intnowhour)).total_seconds()>0:
        i=i+1
    a=df[df['日時'].str.contains(df.iat[len(df)-i,0])]
    dexp_day=df.iat[len(df)-1,10]-a.iat[0,10]
    senka_day=round(dexp_day*7/10000,2)
    senka_daydisp=f"・今日： +{dexp_day}exp/ 戦果 {senka_day}"
    dayBox.configure(state="normal")#以下入力
    dayBox.delete(0, tk.END)
    dayBox.insert(tk.END,senka_daydisp)
    dayBox.configure(state="readonly")

    i=0
    if 2<intnowhour and intnowhour<14:
        senka_now=senka_day
        dexp_now=dexp_day
    else:
        while (dt.strptime(df.iat[len(df)-1-i,0],'%Y/%m/%d %H:%M:%S')-pm_time(intnowhour)).total_seconds()>0:
           i=i+1
        b=df[df['日時'].str.contains(df.iat[len(df)-i,0])]
        dexp_now=df.iat[len(df)-1,10]-b.iat[0,10]
        senka_now=dexp_now*7/10000
    senka_now=f"・今回： +{dexp_now}exp/ 戦果 {senka_now}"
    nowBox.configure(state="normal")#以下入力
    nowBox.delete(0, tk.END)
    nowBox.insert(tk.END,senka_now)
    nowBox.configure(state="readonly")

    month_stand=datetime.datetime(now.year,now.month-1,calendar.monthrange(now.year,now.month-1)[1],22,0,0)
    i=0
    while (dt.strptime(df.iat[len(df)-1-i,0],'%Y/%m/%d %H:%M:%S')-month_stand).total_seconds()>0:
        i=i+1
    c=df[df['日時'].str.contains(df.iat[len(df)-i,0])]
    dexp_month=df.iat[len(df)-1,10]-c.iat[0,10]
    senka_month=round(dexp_month*7/10000,2)
    senka_m=senka_month
    senka_month=f"・今月： +{dexp_month}exp/ 戦果 {senka_month}"
    monthBox.configure(state="normal")#以下入力
    monthBox.delete(0, tk.END)
    monthBox.insert(tk.END,senka_month)
    monthBox.configure(state="readonly")

    global val11,val12,val13,val14,val15,val16,val17,val18,val19,val110
    global val31,val32,val33,val34,val35,val36,val37,val38,val39,val310

    totalnow=total=ex=0
    if val11.get() == True:
        totalnow += 80
        with open(val11file,"w") as f:
            f.write("True")
    else:
        with open(val11file,"w") as f:
            f.write("False")
    if val12.get() == True:
        totalnow += 330
        with open(val12file,"w") as f:
            f.write("True")
    else:
        with open(val12file,"w") as f:
            f.write("False")
    if val13.get() == True:
        totalnow += 200
        with open(val13file,"w") as f:
            f.write("True")
    else:
        with open(val13file,"w") as f:
            f.write("False")
    if val14.get() == True:
        totalnow += 300
        with open(val14file,"w") as f:
            f.write("True")
    else:
        with open(val14file,"w") as f:
            f.write("False")
    if val15.get() == True:
        totalnow += 350
        with open(val15file,"w") as f:
            f.write("True")
    else:
        with open(val15file,"w") as f:
            f.write("False")
    if val16.get() == True:
        totalnow += 400
        with open(val16file,"w") as f:
            f.write("True")
    else:
        with open(val16file,"w") as f:
            f.write("False")
    if val17.get() == True:
        totalnow += 390
        with open(val17file,"w") as f:
            f.write("True")
    else:
        with open(val17file,"w") as f:
            f.write("False")
    if val18.get() == True:
        totalnow += 480
        with open(val18file,"w") as f:
            f.write("True")
    else:
        with open(val18file,"w") as f:
            f.write("False")
    if val19.get() == True:
        totalnow += 600
        with open(val19file,"w") as f:
            f.write("True")
    else:
        with open(val19file,"w") as f:
            f.write("False")
    if val110.get() == True:
        totalnow += 800
        with open(val110file,"w") as f:
            f.write("True")
    else:
        with open(val110file,"w") as f:
            f.write("False")
    totalnow += int(ex_planBox.get())
    totalnow1=totalnow
    totalnow=f"計特別戦果 {totalnow}"
    totalnowBox.configure(state="normal")#以下入力
    totalnowBox.delete(0, tk.END)
    totalnowBox.insert(tk.END,totalnow)
    totalnowBox.configure(state="readonly")

    if val31.get() == True:
        total += 80
        with open(val31file,"w") as f:
            f.write("True")
    else:
        with open(val31file,"w") as f:
            f.write("False")
    if val32.get() == True:
        total += 330
        with open(val32file,"w") as f:
            f.write("True")
    else:
        with open(val32file,"w") as f:
            f.write("False")
    if val33.get() == True:
        total += 200
        with open(val33file,"w") as f:
            f.write("True")
    else:
        with open(val33file,"w") as f:
            f.write("False")
    if val34.get() == True:
        total += 300
        with open(val34file,"w") as f:
            f.write("True")
    else:
        with open(val34file,"w") as f:
            f.write("False")
    if val35.get() == True:
        total += 350
        with open(val35file,"w") as f:
            f.write("True")
    else:
        with open(val35file,"w") as f:
            f.write("False")
    if val36.get() == True:
        total += 400
        with open(val36file,"w") as f:
            f.write("True")
    else:
        with open(val36file,"w") as f:
            f.write("False")
    if val37.get() == True:
        total += 390
        with open(val37file,"w") as f:
            f.write("True")
    else:
        with open(val37file,"w") as f:
            f.write("False")
    if val38.get() == True:
        total += 480
        with open(val38file,"w") as f:
            f.write("True")
    else:
        with open(val38file,"w") as f:
            f.write("False")
    if val39.get() == True:
        total += 600
        with open(val39file,"w") as f:
            f.write("True")
    else:
        with open(val39file,"w") as f:
            f.write("False")
    if val310.get() == True:
        total += 800
        with open(val310file,"w") as f:
            f.write("True")
    else:
        with open(val310file,"w") as f:
            f.write("False")
    total += int(ex_Box.get())
    totalval=total
    total=f"計特別戦果 {total}"
    totalBox.configure(state="normal")#以下入力
    totalBox.delete(0, tk.END)
    totalBox.insert(tk.END,total)
    totalBox.configure(state="readonly")

    if val1.get() == True:
        ex += 75
    if val1_2.get() == True:
        ex += 75
    if val2.get() == True:
        ex += 100
    if val3.get() == True:
        ex += 150
    if val7.get() == True:
        ex += 170
    if val4.get() == True:
        ex += 180
    if val5.get() == True:
        ex += 200
    if val6.get() == True:
        ex += 250
    ex1=1200-ex
    ex=f"計EO {ex}/残EO {ex1}"
    exBox.configure(state="normal")#以下入力
    exBox.delete(0, tk.END)
    exBox.insert(tk.END,ex)
    exBox.configure(state="readonly")

    ex=0
    if val1was.get() == True:
        ex += 75
    if val1_2was.get() == True:
        ex += 75
    if val2was.get() == True:
        ex += 100
    if val3was.get() == True:
        ex += 150
    if val7was.get() == True:
        ex += 170
    if val4was.get() == True:
        ex += 180
    if val5was.get() == True:
        ex += 200
    if val6was.get() == True:
        ex += 250
    ex1=1200-ex
    extxt=f"計EO {ex}/残EO {ex1}"
    exwasBox.configure(state="normal")#以下入力
    exwasBox.delete(0, tk.END)
    exwasBox.insert(tk.END,extxt)
    exwasBox.configure(state="readonly")

    #引継ぎ戦果計算
    d=df[df['日時'].str.contains(str(now.year))]
    dexp_year=c.iat[0,10]-d.iat[0,10]
    senka_year=round(dexp_year/50000+(int(ex_Box.get())+ex+totalval)/35,2)
    inhertext=f"引継ぎ戦果 {senka_year}"
    inherBox.configure(state="normal")#以下入力
    inherBox.delete(0, tk.END)
    inherBox.insert(tk.END,inhertext)
    inherBox.configure(state="readonly")

    #実質総戦果計算
    realtotal=round(totalnow1+senka_m+senka_year+ex,2)
    realtotaltext=f"実質総戦果 {realtotal}"
    realtotalBox.configure(state="normal")#以下入力
    realtotalBox.delete(0, tk.END)
    realtotalBox.insert(tk.END,realtotaltext)
    realtotalBox.configure(state="readonly")

    #着地時間1
    land1time=(int(day1.get())-senka_day)/(sph) #+.iat[29,0]
    land1_minute,land1_hour=math.modf(land1time)
    land1_second,land1_minute=math.modf(land1_minute*60)
    land1text=datetime.timedelta(0,int(round(land1_second*60)),0,0,int(land1_minute),int(land1_hour),0) + dt.strptime(df.iat[len(df)-1,0],'%Y/%m/%d %H:%M:%S')
    land1.configure(state="normal")#以下入力
    land1.delete(0, tk.END)
    if int(day1.get())-senka_day<0:
        land1.insert(tk.END,"fin")
    else:
        land1.insert(tk.END,f"{land1text.hour}:{str(land1text.minute).zfill(2)}:{str(land1text.second).zfill(2)}")
    land1.configure(state="readonly")

    #着地時間2
    land2time=(int(day2.get())-senka_day)/(sph) #+.iat[29,0]
    land2_minute,land2_hour=math.modf(land2time)
    land2_second,land2_minute=math.modf(land2_minute*60)
    land2text=datetime.timedelta(0,int(round(land2_second*60)),0,0,int(land2_minute),int(land2_hour),0) + dt.strptime(df.iat[len(df)-1,0],'%Y/%m/%d %H:%M:%S')
    land2.configure(state="normal")#以下入力
    land2.delete(0, tk.END)
    if int(day2.get())-senka_day<0:
        land2.insert(tk.END,"fin")
    else:
        land2.insert(tk.END,f"{land2text.hour}:{str(land2text.minute).zfill(2)}:{str(land2text.second).zfill(2)}")
    land2.configure(state="readonly")

    #着地時間3
    land3time=(int(day3.get())-senka_day)/(sph) #+.iat[29,0]
    land3_minute,land3_hour=math.modf(land3time)
    land3_second,land3_minute=math.modf(land3_minute*60)
    land3text=datetime.timedelta(0,int(round(land3_second*60)),0,0,int(land3_minute),int(land3_hour),0) + dt.strptime(df.iat[len(df)-1,0],'%Y/%m/%d %H:%M:%S')
    land3.configure(state="normal")#以下入力
    land3.delete(0, tk.END)
    if int(day3.get())-senka_day<0:
        land3.insert(tk.END,"fin")
    else:
        land3.insert(tk.END,f"{land3text.hour}:{str(land3text.minute).zfill(2)}:{str(land3text.second).zfill(2)}")
    land3.configure(state="readonly")

    #着地時間4
    land4time=(int(day4.get())-senka_day)/(sph) #+.iat[29,0]
    land4_minute,land4_hour=math.modf(land4time)
    land4_second,land4_minute=math.modf(land4_minute*60)
    land4text=datetime.timedelta(0,int(round(land4_second*60)),0,0,int(land4_minute),int(land4_hour),0) + dt.strptime(df.iat[len(df)-1,0],'%Y/%m/%d %H:%M:%S')
    land4.configure(state="normal")#以下入力
    land4.delete(0, tk.END)
    if int(day4.get())-senka_day<0:
        land4.insert(tk.END,"fin")
    else:
        land4.insert(tk.END,f"{land4text.hour}:{str(land4text.minute).zfill(2)}:{str(land4text.second).zfill(2)}")
    land4.configure(state="readonly")

    #着地時間5
    land5time=(int(day5.get())-senka_day)/(sph) #+.iat[29,0]
    land5_minute,land5_hour=math.modf(land5time)
    land5_second,land5_minute=math.modf(land5_minute*60)
    land5text=datetime.timedelta(0,int(round(land5_second*60)),0,0,int(land5_minute),int(land5_hour),0) + dt.strptime(df.iat[len(df)-1,0],'%Y/%m/%d %H:%M:%S')
    land5.configure(state="normal")#以下入力
    land5.delete(0, tk.END)
    if int(day5.get())-senka_day<0:
        land5.insert(tk.END,"fin")
    else:
        land5.insert(tk.END,f"{land5text.hour}:{str(land5text.minute).zfill(2)}:{str(land5text.second).zfill(2)}")
    land5.configure(state="readonly")

    #着地予定1
    if now.hour<2:
        land_total1=round((totalnow1+senka_m+senka_year+ex)+int(day1.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-2+0.75),2)
    else:
        land_total1=round((totalnow1+senka_m+senka_year+ex)+int(day1.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-1+0.75),2)
    landtotal1.configure(state="normal")#以下入力
    landtotal1.delete(0, tk.END)
    landtotal1.insert(tk.END,land_total1)
    landtotal1.configure(state="readonly")

    #着地予定2
    if now.hour<2:
        land_total2=round((totalnow1+senka_m+senka_year+ex)+int(day2.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-2+0.75),2)
    else:
        land_total2=round((totalnow1+senka_m+senka_year+ex)+int(day2.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-1+0.75),2)
    landtotal2.configure(state="normal")#以下入力
    landtotal2.delete(0, tk.END)
    landtotal2.insert(tk.END,land_total2)
    landtotal2.configure(state="readonly")        
    
    #着地予定3
    if now.hour<2:
        land_total3=round((totalnow1+senka_m+senka_year+ex)+int(day3.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-2+0.75),2)
    else:
        land_total3=round((totalnow1+senka_m+senka_year+ex)+int(day3.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-1+0.75),2)
    landtotal3.configure(state="normal")#以下入力
    landtotal3.delete(0, tk.END)
    landtotal3.insert(tk.END,land_total3)
    landtotal3.configure(state="readonly")    
    
    #着地予定4
    if now.hour<2:
        land_total4=round((totalnow1+senka_m+senka_year+ex)+int(day4.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-2+0.75),2)
    else:
        land_total4=round((totalnow1+senka_m+senka_year+ex)+int(day4.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-1+0.75),2)
    landtotal4.configure(state="normal")#以下入力
    landtotal4.delete(0, tk.END)
    landtotal4.insert(tk.END,land_total4)
    landtotal4.configure(state="readonly")    
    
    #着地予定5
    if now.hour<2:
        land_total5=round((totalnow1+senka_m+senka_year+ex)+int(day5.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-2+0.75),2)
    else:
        land_total5=round((totalnow1+senka_m+senka_year+ex)+int(day5.get())*(calendar.monthrange(now.year,now.month-1)[1]-now.day-1+0.75),2)
    landtotal5.configure(state="normal")#以下入力
    landtotal5.delete(0, tk.END)
    landtotal5.insert(tk.END,land_total5)
    landtotal5.configure(state="readonly")    

    with open(day1file,"w") as f:
        f.write(day1.get())
    with open(day2file,"w") as f:
        f.write(day2.get())
    with open(day3file,"w") as f:
        f.write(day3.get())
    with open(day4file,"w") as f:
        f.write(day4.get())
    with open(day5file,"w") as f:
        f.write(day5.get())
    
    with open(explanfile,"w") as f:
        f.write(ex_planBox.get())
    with open(exfile,"w") as f:
        f.write(ex_Box.get())

def am_time(nowhour):
    if nowhour>2:
        return datetime.datetime(now.year,now.month,now.day,2,0,0)
    else:
        return datetime.datetime(now.year,now.month,now.day-1,2,0,0)

def pm_time(nowhour):
    if nowhour>2:
        return datetime.datetime(now.year,now.month,now.day,14,0,0)
    else:
        return datetime.datetime(now.year,now.month,now.day-1,14,0,0)

root = tk.Tk()
root.title(u"艦これ 戦果整理")
root.geometry("1100x960")
root.minsize(450,255)
root.maxsize(1100,960)
root.resizable(False,False)

df=""
i=0

val11=tk.BooleanVar()
val12=tk.BooleanVar()
val13=tk.BooleanVar()
val14=tk.BooleanVar()
val15=tk.BooleanVar()
val16=tk.BooleanVar()
val17=tk.BooleanVar()
val18=tk.BooleanVar()
val19=tk.BooleanVar()
val110=tk.BooleanVar()

val31=tk.BooleanVar()
val32=tk.BooleanVar()
val33=tk.BooleanVar()
val34=tk.BooleanVar()
val35=tk.BooleanVar()
val36=tk.BooleanVar()
val37=tk.BooleanVar()
val38=tk.BooleanVar()
val39=tk.BooleanVar()
val310=tk.BooleanVar()

val1=tk.BooleanVar()
val1_2=tk.BooleanVar()
val2=tk.BooleanVar()
val3=tk.BooleanVar()
val4=tk.BooleanVar()
val5=tk.BooleanVar()
val6=tk.BooleanVar()
val7=tk.BooleanVar()

val1was=tk.BooleanVar()
val1_2was=tk.BooleanVar()
val2was=tk.BooleanVar()
val3was=tk.BooleanVar()
val4was=tk.BooleanVar()
val5was=tk.BooleanVar()
val6was=tk.BooleanVar()
val7was=tk.BooleanVar()

def set():
    val1.set(True)
    val1_2.set(True)
    val2.set(True)
    val3.set(True)
    val4.set(True)
    val5.set(True)
    val6.set(True)
    val7.set(True)
    val1was.set(True)
    val1_2was.set(True)
    val2was.set(True)
    val3was.set(True)
    val4was.set(True)
    val5was.set(True)
    val6was.set(True)
    val7was.set(True)
set()



enfile_label=tk.Label(text="・74式ENのRecordSource.csvを参照",font=("游ゴシック", "10","bold"))
enfile_label.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=tk.W)

fileBox = tk.Entry(width=50,font=("游ゴシック", "10","bold"))
fileBox.grid(row=1,column=0,columnspan=3,padx=5,pady=0,sticky=tk.NW)

reference_Button=tk.Button(text=u"参照",font=("游ゴシック", "8","bold"),command=referenceButton)
reference_Button.place(x=365,y=32)

sphBox=tk.Entry(width=35,state="readonly",font=("游ゴシック", "14","bold"))
sphBox.grid(row=2,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
sphBox.configure(state="normal")
sphBox.insert(tk.END,"・戦果時速：")
sphBox.configure(state="readonly")

nowBox=tk.Entry(width=35,state="readonly",font=("游ゴシック", "14","bold"))
nowBox.grid(row=3,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
nowBox.configure(state="normal")
nowBox.insert(tk.END,"・今回：")
nowBox.configure(state="readonly")

dayBox=tk.Entry(width=35,state="readonly",font=("游ゴシック", "14","bold"))
dayBox.grid(row=4,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
dayBox.configure(state="normal")
dayBox.insert(tk.END,"・今日：")
dayBox.configure(state="readonly")

monthBox=tk.Entry(width=35,state="readonly",font=("游ゴシック", "14","bold"))
monthBox.grid(row=5,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
monthBox.configure(state="normal")
monthBox.insert(tk.END,"・今月：")
monthBox.configure(state="readonly")

hourex_label=tk.Label(text="※今回、今日、今月の更新は約1時間ごと\n(母港帰投により変動)",font=("游ゴシック", "11","bold"))
hourex_label.grid(row=5,column=1,columnspan=1,padx=50,sticky=tk.W)

plan_label=tk.Label(text="今月撃つ予定の砲",font=("游ゴシック", "13","bold"))
plan_label.grid(row=7,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)

was2_label=tk.Label(text="先月撃った砲",font=("游ゴシック", "13","bold"))
was2_label.grid(row=7,column=1,columnspan=1,padx=5,pady=5,sticky=tk.W)

kaijo_plan=tk.Checkbutton(text="南西諸島方面「海上警備行動」発令！",font=("游ゴシック", "11","bold"),variable=val11)
kaijo_plan.grid(row=8,column=0,columnspan=1,padx=5,sticky=tk.W)
seiho_plan=tk.Checkbutton(text="発令！「西方海域作戦」",font=("游ゴシック", "11","bold"),variable=val12)
seiho_plan.grid(row=9,column=0,columnspan=1,padx=5,sticky=tk.W)
mikawa_plan=tk.Checkbutton(text="新編成「三川艦隊」、鉄底海峡に突入せよ！",font=("游ゴシック", "11","bold"),variable=val13)
mikawa_plan.grid(row=10,column=0,columnspan=1,padx=5,sticky=tk.W)
hakuchi_plan=tk.Checkbutton(text="泊地周辺海域の安全確保を徹底せよ！",font=("游ゴシック", "11","bold"),variable=val14)
hakuchi_plan.grid(row=11,column=0,columnspan=1,padx=5,sticky=tk.W)
zfirst_plan=tk.Checkbutton(text="戦果拡張任務！「Z作戦」前段作戦",font=("游ゴシック", "11","bold"),variable=val15)
zfirst_plan.grid(row=12,column=0,columnspan=1,padx=5,sticky=tk.W)
zsecond_plan=tk.Checkbutton(text="戦果拡張任務！「Z作戦」後段作戦",font=("游ゴシック", "11","bold"),variable=val16)
zsecond_plan.grid(row=13,column=0,columnspan=1,padx=5,sticky=tk.W)
rokusuisen_plan=tk.Checkbutton(text="拡張「六水戦」、最前線へ！",font=("游ゴシック", "11","bold"),variable=val17)
rokusuisen_plan.grid(row=14,column=0,columnspan=1,padx=5,sticky=tk.W)
al_plan=tk.Checkbutton(text="AL作戦",font=("游ゴシック", "11","bold"),variable=val18)
al_plan.grid(row=15,column=0,columnspan=1,padx=5,pady=5,sticky=tk.W)
kidou_plan=tk.Checkbutton(text="機動部隊決戦",font=("游ゴシック", "11","bold"),variable=val19)
kidou_plan.grid(row=16,column=0,columnspan=1,padx=5,sticky=tk.W)
fb_plan=tk.Checkbutton(text="改装特務空母「Gambier Bay Mk.II」抜錨！",font=("游ゴシック", "11","bold"),variable=val110)
fb_plan.grid(row=17,column=0,columnspan=1,padx=5,sticky=tk.W)
ex_planBox=tk.Entry(width=10,font=("游ゴシック", "10","bold"))
ex_planBox.insert(tk.END,"0")
ex_planBox.grid(row=18,column=0,columnspan=1,padx=5,sticky=tk.W)
ex_planlabel=tk.Label(text="期間限定特別戦果",font=("游ゴシック", "11","bold"))
ex_planlabel.place(x=87,y=597)

kaijo=tk.Checkbutton(text="南西諸島方面「海上警備行動」発令！",font=("游ゴシック", "11","bold"),variable=val31)
kaijo.grid(row=8,column=1,columnspan=1,padx=5,sticky=tk.W)
seiho=tk.Checkbutton(text="発令！「西方海域作戦」",font=("游ゴシック", "11","bold"),variable=val32)
seiho.grid(row=9,column=1,columnspan=1,padx=5,sticky=tk.W)
mikawa=tk.Checkbutton(text="新編成「三川艦隊」、鉄底海峡に突入せよ！",font=("游ゴシック", "11","bold"),variable=val33)
mikawa.grid(row=10,column=1,columnspan=1,padx=5,sticky=tk.W)
hakuchi=tk.Checkbutton(text="泊地周辺海域の安全確保を徹底せよ！",font=("游ゴシック", "11","bold"),variable=val34)
hakuchi.grid(row=11,column=1,columnspan=1,padx=5,sticky=tk.W)
zfirst=tk.Checkbutton(text="戦果拡張任務！「Z作戦」前段作戦",font=("游ゴシック", "11","bold"),variable=val35)
zfirst.grid(row=12,column=1,columnspan=1,padx=5,sticky=tk.W)
zsecond=tk.Checkbutton(text="戦果拡張任務！「Z作戦」後段作戦",font=("游ゴシック", "11","bold"),variable=val36)
zsecond.grid(row=13,column=1,columnspan=1,padx=5,sticky=tk.W)
rokusuisen=tk.Checkbutton(text="拡張「六水戦」、最前線へ！",font=("游ゴシック", "11","bold"),variable=val37)
rokusuisen.grid(row=14,column=1,columnspan=1,padx=5,sticky=tk.W)
al=tk.Checkbutton(text="AL作戦",font=("游ゴシック", "11","bold"),variable=val38)
al.grid(row=15,column=1,columnspan=1,padx=5,pady=5,sticky=tk.W)
kidou=tk.Checkbutton(text="機動部隊決戦",font=("游ゴシック", "11","bold"),variable=val39)
kidou.grid(row=16,column=1,columnspan=1,padx=5,sticky=tk.W)
fb=tk.Checkbutton(text="改装特務空母「Gambier Bay Mk.II」抜錨！",font=("游ゴシック", "11","bold"),variable=val310)
fb.grid(row=17,column=1,columnspan=1,padx=5,sticky=tk.W)
ex_Box=tk.Entry(width=10,font=("游ゴシック", "10","bold"))
ex_Box.insert(tk.END,"0")
ex_Box.grid(row=18,column=1,columnspan=1,padx=5,sticky=tk.W)
ex_label=tk.Label(text="期間限定特別戦果",font=("游ゴシック", "11","bold"))
ex_label.place(x=490,y=597)

totalnowBox = tk.Entry(width=30,font=("游ゴシック", "12","bold"),state="readonly")
totalnowBox.grid(row=19,column=0,columnspan=1,padx=5,pady=7,sticky=tk.W)
totalnowBox.configure(state="normal")
totalnowBox.insert(tk.END,"計特別戦果")
totalnowBox.configure(state="readonly")
totalBox = tk.Entry(width=30,font=("游ゴシック", "12","bold"),state="readonly")
totalBox.grid(row=19,column=1,columnspan=1,padx=5,pady=7,sticky=tk.W)
totalBox.configure(state="normal")
totalBox.insert(tk.END,"計特別戦果")
totalBox.configure(state="readonly")

inherBox = tk.Entry(width=20,font=("游ゴシック", "12","bold"),state="readonly")
inherBox.grid(row=6,column=0,columnspan=1,padx=5,pady=7,sticky=tk.W)
inherBox.configure(state="normal")
inherBox.insert(tk.END,"引継ぎ戦果")
inherBox.configure(state="readonly")

realtotalBox=tk.Entry(width=20,font=("游ゴシック", "12","bold"),state="readonly")
realtotalBox.place(x=200,y=222)
realtotalBox.configure(state="normal")
realtotalBox.insert(tk.END,"実質総戦果")
realtotalBox.configure(state="readonly")

def exvalue():

    exvalue_kaijo=tk.Label(text="…80",font=("游ゴシック", "12","bold"))
    exvalue_kaijo.grid(row=8,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_seiho=tk.Label(text="…330",font=("游ゴシック", "12","bold"))
    exvalue_seiho.grid(row=9,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_mikawa=tk.Label(text="…200",font=("游ゴシック", "12","bold"))
    exvalue_mikawa.grid(row=10,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_hakuchi=tk.Label(text="…300",font=("游ゴシック", "12","bold"))
    exvalue_hakuchi.grid(row=11,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_zfirst=tk.Label(text="…350",font=("游ゴシック", "12","bold"))
    exvalue_zfirst.grid(row=12,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_zsecond=tk.Label(text="…400",font=("游ゴシック", "12","bold"))
    exvalue_zsecond.grid(row=13,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_rokusuisen=tk.Label(text="…390",font=("游ゴシック", "12","bold"))
    exvalue_rokusuisen.grid(row=14,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_al=tk.Label(text="…480",font=("游ゴシック", "12","bold"))
    exvalue_al.grid(row=15,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_kidou=tk.Label(text="…600",font=("游ゴシック", "12","bold"))
    exvalue_kidou.grid(row=16,column=2,columnspan=1,padx=5,sticky=tk.W)
    exvalue_fb=tk.Label(text="…800",font=("游ゴシック", "12","bold"))
    exvalue_fb.grid(row=17,column=2,columnspan=1,padx=5,sticky=tk.W)
exvalue()

ex1=tk.Checkbutton(text="1-5 …75",font=("游ゴシック", "11","bold"),variable=val1)
ex1.grid(row=20,column=0,columnspan=1,padx=5,sticky=tk.W)
ex1_2=tk.Checkbutton(text="1-6 …75",font=("游ゴシック", "11","bold"),variable=val1_2)
ex1_2.grid(row=21,column=0,columnspan=1,padx=5,sticky=tk.W)
ex2=tk.Checkbutton(text="2-5 …100",font=("游ゴシック", "11","bold"),variable=val2)
ex2.grid(row=22,column=0,columnspan=1,padx=5,sticky=tk.W)
ex3=tk.Checkbutton(text="3-5 …150",font=("游ゴシック", "11","bold"),variable=val3)
ex3.grid(row=23,column=0,columnspan=1,padx=5,sticky=tk.W)
ex7=tk.Checkbutton(text="7-5 …170",font=("游ゴシック", "11","bold"),variable=val7)
ex7.grid(row=24,column=0,columnspan=1,padx=5,sticky=tk.W)
ex4=tk.Checkbutton(text="4-5 …180",font=("游ゴシック", "11","bold"),variable=val4)
ex4.grid(row=25,column=0,columnspan=1,padx=5,sticky=tk.W)
ex5=tk.Checkbutton(text="5-5 …200",font=("游ゴシック", "11","bold"),variable=val5)
ex5.grid(row=26,column=0,columnspan=1,padx=5,sticky=tk.W)
ex6=tk.Checkbutton(text="6-5 …250",font=("游ゴシック", "11","bold"),variable=val6)
ex6.grid(row=27,column=0,columnspan=1,padx=5,sticky=tk.W)
exBox=tk.Entry(width=30,font=("游ゴシック", "12","bold"),state="readonly")
exBox.grid(row=28,column=0,columnspan=1,padx=5,sticky=tk.W)
exBox.configure(state="normal")
exBox.insert(tk.END,"計EO 1200/残EO 0")
exBox.configure(state="readonly")

ex1was=tk.Checkbutton(text="1-5 …75",font=("游ゴシック", "11","bold"),variable=val1was)
ex1was.grid(row=20,column=1,columnspan=1,padx=5,sticky=tk.W)
ex1_2was=tk.Checkbutton(text="1-6 …75",font=("游ゴシック", "11","bold"),variable=val1_2was)
ex1_2was.grid(row=21,column=1,columnspan=1,padx=5,sticky=tk.W)
ex2was=tk.Checkbutton(text="2-5 …100",font=("游ゴシック", "11","bold"),variable=val2was)
ex2was.grid(row=22,column=1,columnspan=1,padx=5,sticky=tk.W)
ex3was=tk.Checkbutton(text="3-5 …150",font=("游ゴシック", "11","bold"),variable=val3was)
ex3was.grid(row=23,column=1,columnspan=1,padx=5,sticky=tk.W)
ex7was=tk.Checkbutton(text="7-5 …170",font=("游ゴシック", "11","bold"),variable=val7was)
ex7was.grid(row=24,column=1,columnspan=1,padx=5,sticky=tk.W)
ex4was=tk.Checkbutton(text="4-5 …180",font=("游ゴシック", "11","bold"),variable=val4was)
ex4was.grid(row=25,column=1,columnspan=1,padx=5,sticky=tk.W)
ex5was=tk.Checkbutton(text="5-5 …200",font=("游ゴシック", "11","bold"),variable=val5was)
ex5was.grid(row=26,column=1,columnspan=1,padx=5,sticky=tk.W)
ex6was=tk.Checkbutton(text="6-5 …250",font=("游ゴシック", "11","bold"),variable=val6was)
ex6was.grid(row=27,column=1,columnspan=1,padx=5,sticky=tk.W)
exwasBox=tk.Entry(width=30,font=("游ゴシック", "12","bold"),state="readonly")
exwasBox.grid(row=28,column=1,columnspan=1,padx=5,sticky=tk.W)
exwasBox.configure(state="normal")
exwasBox.insert(tk.END,"計EO 1200/残EO 0")
exwasBox.configure(state="readonly")

day=tk.Label(text="/day",font=("游ゴシック", "13","bold"))
day.place(x=460,y=60)
day1=tk.Entry(width=9,font=("游ゴシック", "13","bold"),justify=tk.RIGHT)
day1.place(x=550,y=60)
day2=tk.Entry(width=9,font=("游ゴシック", "13","bold"),justify=tk.RIGHT)
day2.place(x=650,y=60)
day3=tk.Entry(width=9,font=("游ゴシック", "13","bold"),justify=tk.RIGHT)
day3.place(x=750,y=60)
day4=tk.Entry(width=9,font=("游ゴシック", "13","bold"),justify=tk.RIGHT)
day4.place(x=850,y=60)
day5=tk.Entry(width=9,font=("游ゴシック", "13","bold"),justify=tk.RIGHT)
day5.place(x=950,y=60)

land=tk.Label(text="着地時間",font=("游ゴシック", "13","bold"))
land.place(x=460,y=90)
land1=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
land1.place(x=550,y=90)
land2=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
land2.place(x=650,y=90)
land3=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
land3.place(x=750,y=90)
land4=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
land4.place(x=850,y=90)
land5=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
land5.place(x=950,y=90)

landtotal=tk.Label(text="着地予定",font=("游ゴシック", "13","bold"))
landtotal.place(x=460,y=120)
landtotal1=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
landtotal1.place(x=550,y=120)
landtotal2=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
landtotal2.place(x=650,y=120)
landtotal3=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
landtotal3.place(x=750,y=120)
landtotal4=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
landtotal4.place(x=850,y=120)
landtotal5=tk.Entry(width=9,font=("游ゴシック", "13","bold"),state="readonly",justify=tk.RIGHT)
landtotal5.place(x=950,y=120)

winsmall=tk.Button(text=u"小",font=("游ゴシック", "8","bold"),command=small)
winmid=tk.Button(text=u"中",font=("游ゴシック", "10","bold"),command=mid)
winlarge=tk.Button(text=u"大",font=("游ゴシック", "12","bold"),command=large)
winsmall.place(x=405,y=60)
winmid.place(x=403,y=90)
winlarge.place(x=400,y=125)

textfile=r"Data\filename.txt"

with open(textfile) as f:
   fileBox.insert(tk.END,f.read())

day1file=r"Data\day1.txt"
day2file=r"Data\day2.txt"
day3file=r"Data\day3.txt"
day4file=r"Data\day4.txt"
day5file=r"Data\day5.txt"

val11file=r"Data\val11.txt"
val12file=r"Data\val12.txt"
val13file=r"Data\val13.txt"
val14file=r"Data\val14.txt"
val15file=r"Data\val15.txt"
val16file=r"Data\val16.txt"
val17file=r"Data\val17.txt"
val18file=r"Data\val18.txt"
val19file=r"Data\val19.txt"
val110file=r"Data\val110.txt"

val31file=r"Data\val31.txt"
val32file=r"Data\val32.txt"
val33file=r"Data\val33.txt"
val34file=r"Data\val34.txt"
val35file=r"Data\val35.txt"
val36file=r"Data\val36.txt"
val37file=r"Data\val37.txt"
val38file=r"Data\val38.txt"
val39file=r"Data\val39.txt"
val310file=r"Data\val310.txt"

explanfile=r"Data\explan.txt"
exfile=r"Data\ex.txt"

sph_setfile=r"Data\sph_set.txt"

with open(day1file) as f:
    day1.insert(tk.END,f.read())
with open(day2file) as f:
    day2.insert(tk.END,f.read())
with open(day3file) as f:
    day3.insert(tk.END,f.read())
with open(day4file) as f:
    day4.insert(tk.END,f.read())
with open(day5file) as f:
    day5.insert(tk.END,f.read())

with open(val11file) as f:
    val11.set(f.read())
with open(val12file) as f:
    val12.set(f.read())
with open(val13file) as f:
    val13.set(f.read())
with open(val14file) as f:
    val14.set(f.read())
with open(val15file) as f:
    val15.set(f.read())
with open(val16file) as f:
   val16.set(f.read())
with open(val17file) as f:
    val17.set(f.read())
with open(val18file) as f:
    val18.set(f.read())
with open(val19file) as f:
    val19.set(f.read())
with open(val110file) as f:
    val110.set(f.read())

with open(val31file) as f:
    val31.set(f.read())
with open(val32file) as f:
    val32.set(f.read())
with open(val33file) as f:
    val33.set(f.read())
with open(val34file) as f:
    val34.set(f.read())
with open(val35file) as f:
    val35.set(f.read())
with open(val36file) as f:
    val36.set(f.read())
with open(val37file) as f:
    val37.set(f.read())
with open(val38file) as f:
    val38.set(f.read())
with open(val39file) as f:
    val39.set(f.read())
with open(val310file) as f:
    val310.set(f.read())

with open(explanfile) as f:
    ex_planBox.delete(0, tk.END)
    ex_planBox.insert(tk.END,f.read())
with open(exfile) as f:
    ex_Box.delete(0, tk.END)
    ex_Box.insert(tk.END,f.read())

calc=tk.Button(text=u"計算",font=("游ゴシック", "13","bold"),command=calcButton)
calc.place(x=500,y=215)

finalupdate=tk.Entry(width=30,font=("游ゴシック", "13","bold"),state="readonly")
finalupdate.place(x=560,y=222)
finalupdate.configure(state="normal")
finalupdate.insert(tk.END,"最終更新：")
finalupdate.configure(state="readonly")

val_sphset=tk.BooleanVar()
sph_set_Button=tk.Checkbutton(text="時速設定値",font=("游ゴシック", "11","bold"),variable=val_sphset)
sph_set_Button.place(x=460,y=28)
sph_set=tk.Entry(width=10,font=("游ゴシック", "12","bold"))
sph_set.place(x=575,y=30)

with open(sph_setfile) as f:
    sph_set.delete(0, tk.END)
    sph_set.insert(tk.END,f.read())

root.after(60000,repeat)
root.mainloop()