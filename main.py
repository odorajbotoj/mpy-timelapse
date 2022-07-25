# mpy-timelapse
# main.py
# Ver. 4
# For: ESP 32 CAM
# By: odorajbotoj
# Update time: 2022-07-06
import machine, network, utime, uos, socket, camera, ujson
led=machine.Pin(33, machine.Pin.OUT) # LED init
try:
    led(0)
    camera.init(0, format=camera.JPEG) # 初始化
    utime.sleep(2) # 等待完全启动
    led(1)
except Exception:
    print("Camera Init ERROR")
    for i in range(25):
        for j in range(3):
            led(0)
            utime.sleep_ms(150)
            led(1)
            utime.sleep_ms(150)
        led(1)
        utime.sleep_ms(1100)
    raise Exception

try:
    led(0)
    uos.mount(machine.SDCard(slot=1, width=1),"/sd") # 挂载sd卡
    led(1)
except Exception:
    print("SD Card ERROR")
    for i in range(25):
        for j in range(2):
            led(0)
            utime.sleep_ms(250)
            led(1)
            utime.sleep_ms(250)
        led(1)
        utime.sleep_ms(1000)
    raise Exception
uos.chdir("sd") # 更改工作目录
gCtr = open("gCtr.txt", "r+") # group counter
gCtrNum = int(gCtr.read()) # 每次开机将组号+1
gCtrNum = str(gCtrNum + 1)
gCtr.seek(0)
gCtr.write(gCtrNum)
gCtr.close()
gCtrName = "sunny01"

if True:
# if continueRun:
    print("Running...")
    led(0) # on
    utime.sleep(0.5)
    led(1) #off

    with open(gCtrName+".json", "r") as cfg: # load config file
        cfgD = ujson.loads(cfg.read())
        cfg.close()

    # load camera config
    camera.saturation(cfgD["saturation"])
    camera.brightness(cfgD["brightness"])
    camera.contrast(cfgD["contrast"])
    camera.quality(cfgD["quality"])
    camera.flip(cfgD["flip"])
    camera.mirror(cfgD["mirror"])
    camera.framesize(cfgD["framesize"])
    camera.speffect(cfgD["speffect"])
    camera.whitebalance(cfgD["whitebalance"])

    pCtrNum = 0 # picture counter number
    pCtrNumMax = cfgD["maxpic"]
    SLEEP_TIME = cfgD["sleeptime"]

    def countPic(): # 返回文件名
        global gCtrNum, pCtrNum
        pCtrNum = pCtrNum + 1
        return str(gCtrNum + "_" + str(pCtrNum) + ".jpg")

    # 第1~3张照片可能会出问题
    while pCtrNum <= pCtrNumMax:
        try:
            led(0)
            picBuf = camera.capture()
            img=open(countPic(),"wb")
            img.write(picBuf)
            img.close()
            led(1)
        except Exception:
            print("Take photos and save ERROR")
            for i in range(25):
                for j in range(4):
                    led(0)
                    utime.sleep_ms(100)
                    led(1)
                    utime.sleep_ms(100)
                led(1)
                utime.sleep_ms(1200)
            raise Exception

        print("Success")

        for i in range(SLEEP_TIME):
            led(0)
            utime.sleep_ms(100)
            led(1)
            utime.sleep_ms(900)

        print("Slept "+str(SLEEP_TIME)+"s")
