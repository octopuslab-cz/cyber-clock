# simple basic example - ESP32 + 7segment display
#  ver. 2.7.2020
print("--- octopusLAB: test_display7.py ---")


print("-> imports")
from time import sleep
from machine import Pin
from utils.pinout import set_pinout
from components.rgb import Rgb 
import colors_rgb as rgb

from ntptime import settime
from machine import RTC
import ds3231
from utils.octopus_lib import i2c_init
# from utils.octopus_lib import w, time_init, setlocal

INTENSITY = 200 # 50 -> 150 ...

#time_init()
print("--- i2c_init")
i2c = i2c_init()
#i2c.scan()
sleep(2)

print("time init")
ds = ds3231.DS3231(i2c)

def ds3231_init(ds3231, rtc):
    now = (2022, 6, 21, 6, 16, 20, 0, 0)
    rtc.datetime(now)
    ds3231.save_time()

rtc = RTC()
# ---------------------
#ds3231_init(ds, rtc)
# ---------------------


print("rtc.datetime-old", rtc.datetime())
print(ds.get_time(True))
print("rtc.datetime-now", rtc.datetime())

WSMAX = 250
ws = Rgb(27,WSMAX) #27 DEV3
"""    ROW
-----+ odd
  RX |
+----+ even
|RXX
"""
sleep(1)
# --- led strip --- row / space
RX=25
RXX=3

# import char3x5
# chx,chy = 3,5
chx,chy = 4,7
from assets.char4x7 import *
# import assets.char4x7


off = 0

def ws_clear():
    for i in range(WSMAX):
        ws.color((0,0,0),i)


def ws_char(char,pos=0, color=1):
 row = 0
 for rx in char:
    col = 0
    for cy in rx:
       if row%2==0:
           posx = row*(RX+RXX)+col+pos
       else:
           posx = row*(RX+RXX)+RX-col-1-pos
       # print(posx,rx,cy)
       if color== 1:
           if pos<WSMAX: ws.color((INTENSITY*cy,0,0),posx)
       if color== 2:
           if pos<WSMAX: ws.color((0,50*cy,0),posx)
       if color== 3:
           if pos<WSMAX: ws.color((0,0,INTENSITY*cy),posx)
       col += 1
    row += 1
    
def add0(sn):
    return "0"+str(sn) if int(sn)<10 else str(sn)

hh=add0(rtc.datetime()[4])
mm=add0(rtc.datetime()[5])
print("time:",hh,mm)
sleep(3)


print("-"*30)
posun = 1

for arr in range(7):
    print(arr)
    # ws_clear()
    ws_char(char[12],arr*3,3)
    sleep(0.3)
    ws_char(char[11],arr*3,3)

tick = 0
while True:
   tick += 1
   hh=add0(rtc.datetime()[4])
   mm=add0(rtc.datetime()[5])
   num1 = int(hh[0])
   num2 = int(hh[1])
   num3 = int(mm[0])
   num4 = int(mm[1])
   print("time:",hh,mm)
   print("nums:",num1,num2,num3,num4)
   
   if num1 == 0: num1=11
   
   try:     
        ws_char(char[num1],0+posun)
        ws_char(char[num2],6+posun)
            
        if tick%2==0:
            ws_char(char[10],6+4+posun,2)
        else:
            ws_char(char[11],6+4+posun)
                
        ws_char(char[num3],6+7+posun)
        ws_char(char[num4],6+7+6+posun)

        sleep(0.5)

   except:
       print("Err")

