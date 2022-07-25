# mpy-timelapse<br>
Esp32 CAM + Micro Python<br>
上传后开机自启, 每4秒拍一张, 参数可调. <br>
*** 已弃用boot.py, 请使用main.py ***
<br>
#### 关于调参:
+ 在main.py中修改对应文件名
+ 在SDCard根目录下创建对应的json文件
+ 例程: `{"saturation": 0, "brightness": 0, "contrast": 0, "quality": 10, "flip": 0, "mirror": 0, "framesize": 13, "speffect": 0, "whitebalance": 0, "sleeptime": 2, "maxpic": 3000}` 

<br>
#### 板载LED相关: 
+ 上电闪烁(0.5s) => 已开机, LED正常
+ 常亮 => 正在拍照
+ 一次闪烁(0.1s) => 计时中, 闪烁一次为1s
+ 两次闪烁(0.25s/次, 组间隔1s) => SD卡异常
+ 三次闪烁(0.15s/次, 组间隔1.1s) => 相机初始化异常
+ 四次闪烁(0.1s/次, 组间隔1.2s) => 拍照保存异常
