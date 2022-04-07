from subprocess import run
from ctypes import windll
from sys import executable,argv
from os import startfile,_exit,popen
from os.path import join
from threading import Thread
from ctypes import windll,byref,sizeof
from ctypes.wintypes import HWND,DWORD,RECT
# from multiprocessing import Process
import winreg
from time import time as getTime
import pywintypes #防止显示无法找到pywin32
import win32api,win32con,win32gui,win32print
from workPath import reWorkPath
from datetime import datetime
import time
from ui import mainWindow
import pynput
from json import loads
from json.decoder import JSONDecodeError

url = """https://github.com/zhuhansan666/autoPowerOff"""
startUpArgv = ''

def time_check(_time_:str,精确匹配:bool=False,addSec:int=0):
    '''时间格式:%Y-%m-%d/%H:%M:%S 或 %H:%M:%S'''
    if '/' not in _time_:
        _time_ = "{}{}".format(time.strftime('%Y-%m-%d/',time.localtime(time.time())),_time_)
    try:
        timeStamp = float(time.mktime(time.strptime(_time_, "%Y-%m-%d/%H:%M:%S")))+addSec
    except:
        return "错误:时间格式问题"
    cache = timeStamp-time.time()
    if 精确匹配:
        if round(cache,3) <= 0.0:
            return (00,00,00,00,000,True)
        else:
            d = int(cache // 86400)
            H = int((cache - d*86400) // 3600)
            M = int((cache - d*86400 - H*3600) // 60)
            S = int((cache - d*86400 - H*3600 - M*60))
            MS = (cache % 1) * 1000
            return ('%02d'%d,'%02d'%H,'%02d'%M,'%02d'%S,'%03d'%MS,False)
    elif not 精确匹配:
        if cache <= 0.0:
            return (00,00,00,00,000,True)
        else:
            d = int(cache // 86400)
            H = int((cache - d*86400) // 3600)
            M = int((cache - d*86400 - H*3600) // 60)
            S = int((cache - d*86400 - H*3600 - M*60))
            MS = (cache % 1) * 1000
            return ('%02d'%d,'%02d'%H,'%02d'%M,'%02d'%S,'%03d'%MS,False)

def checkSize(_checkSize1:(list or tuple),_checkSize2:(list or tuple)):
    """if _checkSize1 >= _checkSize2 Return True else Return False"""
    size1X = _checkSize1[3]-_checkSize1[0]
    size1Y = _checkSize1[2]-_checkSize1[1]
    size2X = _checkSize2[3]-_checkSize2[0]
    size2Y = _checkSize2[2]-_checkSize2[1]
    Size1 = size1X*size1Y
    Size2 = size2X*size2Y
    if Size1 >= Size2:
        return True
    return False

def GetRealScreenSize():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return 0,0,w, h

def GetWindowSize(hwnd):
    """获取窗口真实大小"""
    try:
        f = windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        return False
    rect = RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(HWND(hwnd),
        DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        byref(rect),
        sizeof(rect)
        )
    return (rect.left, rect.top, rect.right, rect.bottom)

def checkFullScreen():
    return checkSize(GetWindowSize(win32gui.GetForegroundWindow()),GetRealScreenSize())

def settings():
    global debug,maxJ,setTime
    try:
        jsonFile = open(join(workPath,'./settings.json'))
        jsonInFo = loads(jsonFile.read())
        if 'time' in jsonInFo:
            setTimeTemp = jsonInFo['time']
            if time_check(setTimeTemp) != "错误:时间格式问题":
                setTime = setTimeTemp
        if 'waitTime' in jsonInFo:
            maxJTemp = jsonInFo['waitTime']
            if type(maxJTemp):
                maxJ = maxJTemp
            elif maxJTemp.isdigit():
                maxJ = int(maxJTemp)
        if 'debug' in jsonInFo:
            debug = bool(jsonInFo['debug'])

    except FileNotFoundError:
        pass
    except JSONDecodeError:
        pass


workPath = reWorkPath()

maxJ = 60
j = -1 #主操作检测变量
setTime = "16:15:00"
setPowerOffTime = "17:27:00"
debug = False
exit = False

#文件初始化（避免删除

file1 = open(join(workPath,'./images/icon.png'))
file2 = open(join(workPath,'./Font/MiSans-Bold.ttf'))
file3 = open(join(workPath,'./sounds/定时关机提示音.wav'))
settings()

#结束文件初始化（避免删除



def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False



if is_admin():
    pass
else:
    windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
    _exit(-1)



class Daemon:
    def __init__(self) -> None:
        pass
    def tsk(self,whileTrue:bool=True,type:int=1):
        """禁用tsk"""
        if whileTrue:
            while True:
                tskReg = """HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\system"""
                run("reg add {} /v DisableTaskMgr /t REG_SZ /d {} /f".format(tskReg,type),shell=True)
                rec = popen("taskkill /im Taskmgr.exe /f").read()
                if len(rec) == 0:
                    time.sleep(1)
        else:
            tskReg = """HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\system"""
            run("reg add {} /v DisableTaskMgr /t REG_SZ /d {} /f".format(tskReg,type),shell=True)
            rec = popen("taskkill /im Taskmgr.exe /f").read()
            if len(rec) == 0:
                time.sleep(1)
    def uac(self,whileTrue:bool=True,type:int=0):
        """禁用UAC"""
        if whileTrue:
            while True:
                uacReg = """HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"""
                run("reg add {} /v EnableLUA /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                run("reg add {} /v PromptOnSecureDesktop /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                run("reg add {} /v ConsentPromptBehaviorAdmin /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                rec = popen("taskkill /im dllhost.exe /f").read()
                print(rec)
                if len(rec) == 0:
                    time.sleep(1)
        else:
            uacReg = """HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"""
            run("reg add {} /v EnableLUA /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            run("reg add {} /v PromptOnSecureDesktop /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            run("reg add {} /v ConsentPromptBehaviorAdmin /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            rec = popen("taskkill /im dllhost.exe /f").read()
            if len(rec) == 0:
                time.sleep(1)
    def startUp(self,whileTrue:bool=True,waitTime:float=10,setFile=False):
        """设置当前用户自启动"""
        global startUpArgv
        run = 0
        while whileTrue or run == 0:
            run += 1
            reg = """SOFTWARE\Microsoft\Windows\CurrentVersion\Run""" # HKEY_CURRENT_USER\
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg,access=winreg.KEY_ALL_ACCESS)
            if not setFile:
                winreg.SetValueEx(key,'systemPowerOff',0,winreg.REG_SZ,'"{}"{}'.format(argv[0],startUpArgv))
            else:
                winreg.SetValueEx(key,'systemPowerOff',0,winreg.REG_SZ,'"{}"{}'.format(setFile,startUpArgv))
            winreg.CloseKey(key)
            time.sleep(waitTime)


class checkEvents():
    def __init__(self) -> None:
        pass
    def Ctrl(self,*event):
        global j
        j = -1
    def main(self):
        pynput.mouse.Listener(on_move=self.Ctrl, on_click=self.Ctrl, on_scroll=self.Ctrl,daemon=True).start()
        pynput.keyboard.Listener(on_press=self.Ctrl,on_release=self.Ctrl,daemon=True).start()


_checkEvents = checkEvents()

_checkEvents.main()

main = Daemon()
mainList = [main.tsk,main.uac,main.startUp]

threadList = []
# processList = []

for f in mainList:
    t = Thread(target=f,args=(),daemon=True)
    t.start()
    threadList.append(t)

#实测多线程的运行速度比多进程快

# if __name__ == "__main__":
#     for f in mainList:
#         p = Process(target=f,args=())
#         p.start()
#         processList.append(p)


if '-powerOffInWorkDay' in argv:
    tips = Thread(target=win32gui.MessageBox,args=(None, "请不要在工作日关机,若误报请联系开发者.\n按下确定键以关闭提示窗口...", '提示',(win32con.MB_OK | win32con.MB_ICONERROR)),daemon=True)


def wndproc(hwnd, msg, wparam, lparam): #关机事件后执行的函数
    global startUpArgv
    main.startUp(whileTrue=False,waitTime=0)
    if datetime.today().isoweekday() < 6 and not time_check(setTime)[-1]:
        startUpArgv = ' -powerOffInWorkDay'
        run('shutdown /r /f /t 3',shell=True)
        win32gui.MessageBox(None, "非法的操作：工作日关机(将自动重启,若误报请联系开发者.)", '非法的操作：工作日关机(将自动重启,若误报请联系开发者.)',(win32con.MB_OK | win32con.MB_ICONERROR))
        return 0
    else:
        _exit(0)


#初始化捕捉关机事件

hinst = win32api.GetModuleHandle(None)
wndclass = win32gui.WNDCLASS()
wndclass.hInstance = hinst
wndclass.lpszClassName = "testWindowClass"
messageMap = {
                win32con.WM_QUERYENDSESSION: wndproc,    
                win32con.WM_ENDSESSION: wndproc,
                }

wndclass.lpfnWndProc = messageMap

try:
    myWindowClass = win32gui.RegisterClass(wndclass)    # 注册窗口类
    hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,      # 实例化对象
                                    myWindowClass,
                                    "",
                                    0,
                                    0,
                                    0,
                                    win32con.CW_USEDEFAULT,
                                    win32con.CW_USEDEFAULT,
                                    0,
                                    0,
                                    hinst,
                                    None)
except Exception as e:
    startfile(argv[0])
    _exit(-1)

#捕捉关机初始化结束

lowTime = getTime()
lowTime2 = getTime()
powerOffTime = None
fullScreenApplicationRuning = 0

while True:
    if getTime() - lowTime2 >= 1 or debug:
        print(fullScreenApplicationRuning)
        j += 1
        lowTime2 = getTime()
        settings()
        if time_check(setTime)[-1] or debug:
            checkFullScreen_ = checkFullScreen()
            if checkFullScreen_:
                j = maxJ - 1
                fullScreenApplicationRuning = 1
            elif checkFullScreen_ == False and fullScreenApplicationRuning == 1:
                fullScreenApplicationRuning = 2
    if (getTime() - lowTime >= 0.1 and not exit) or debug:
        lowTime = getTime()
        win32gui.PumpWaitingMessages() #捕捉关机主程序
        if time_check(setPowerOffTime,addSec=-60)[-1]:
            main.startUp(whileTrue=False,waitTime=0)
            run('shutdown /s /f /t 60',shell=True)
            exit = True
            powerOffTime = getTime()
        elif time_check(setTime)[-1] or debug:
            if  fullScreenApplicationRuning == 2 or j >= maxJ or debug:
                fullScreenApplicationRuning = 0
                rec = mainWindow()
                if rec == 1:
                    main.startUp(whileTrue=False,waitTime=0)
                    run('shutdown /s /f /t 0',shell=True)
                    _exit(0)
                elif rec == 2:
                    j = -1
                elif rec == 3:
                    exit = True
                elif rec == 4:
                    j = -1
                    run("explorer {}".format(url),shell=True)
    if powerOffTime is not None and getTime() - powerOffTime > 60:
        powerOffTime = None
        exit = False
        main.startUp(whileTrue=False,waitTime=0)
        run('shutdown /s /f /t 0',shell=True)
