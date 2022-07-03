# This file is executed on every boot (including wake-boot from deepsleep)
# mpy-timelapse
# Ver. 2
# For: ESP 32 CAM
# By: odorajbotoj
# Update time: 2022-07-03
import camera, uos, utime
from machine import SDCard, Pin

########
# 休眠时长
# 注意拍照和保存会耗掉大约1s
SLEEP_TIME = 4 # (s)
########

led = Pin(33, Pin.OUT) # 状态指示灯 板载LED
led(0) # on
utime.sleep(0.5)
led(1) # off
try:
    camera.init(0, format=camera.JPEG) # 初始化
    camera.framesize(camera.FRAME_UXGA) # 1600*1200
    camera.quality(10) # 高品质
    utime.sleep(2) # 等待完全启动
except:
    print("Camera Init ERROR")
    for i in range(25):
        for j in range(3):
            led(0)
            utime.sleep_ms(150)
            led(1)
            utime.sleep_ms(150)
        led(1)
        utime.sleep_ms(1100)
        
try:
    uos.mount(SDCard(slot=1, width=1),"/sd") # 挂载sd卡
except:
    print("SD Card ERROR")
    for i in range(25):
        for j in range(2):
            led(0)
            utime.sleep_ms(250)
            led(1)
            utime.sleep_ms(250)
        led(1)
        utime.sleep_ms(1000)
uos.chdir("sd") # 更改工作目录
gCtr = open("gCtr.txt", "r+") # group counter 每次开机将组号+1
gCtrNum = int(gCtr.read())
gCtrNum = gCtrNum + 1
gCtr.seek(0)
gCtr.write(str(gCtrNum))
gCtr.close()
pCtrNum = 0 # picture counter number
def countPic(): # 返回文件名
    global gCtrNum, pCtrNum
    pCtrNum = pCtrNum + 1
    return str(str(gCtrNum) + "_" + str(pCtrNum) + ".jpg")
# for i in range(241): # 256MB限制, 第一张照片可能会出问题
while 1:
    try:
        led(0)
        picBuf = camera.capture()
        img=open(countPic(),"wb")
        img.write(picBuf)
        img.close()
        led(1)
    except:
        print("Take photos and save ERROR")
        for i in range(25):
            for j in range(4):
                led(0)
                utime.sleep_ms(100)
                led(1)
                utime.sleep_ms(100)
            led(1)
            utime.sleep_ms(1200)
    print("Success")
    for i in range(SLEEP_TIME):
        led(0)
        utime.sleep_ms(100)
        led(1)
        utime.sleep_ms(900)
    print("Slept "+str(SLEEP_TIME)+"s")
