from subprocess import run
from ctypes import windll
from sys import executable,argv
from os import startfile,_exit
from os.path import join
from threading import Thread
import winreg
from time import time as getTime
import pywintypes #防止显示无法找到pywin32
import win32api,win32con,win32gui
from workPath import reWorkPath
from datetime import datetime
import time
from ui import mainWindow
import pynput
from json import loads
from json.decoder import JSONDecodeError

url = """https://github.com/zhuhansan666/autoPowerOff"""

def time_check(_time_:str,精确匹配:bool=False):
    '''时间格式:%Y-%m-%d/%H:%M:%S 或 %H:%M:%S'''
    if '/' not in _time_:
        _time_ = "{}{}".format(time.strftime('%Y-%m-%d/',time.localtime(time.time())),_time_)
    try:
        timeStamp = float(time.mktime(time.strptime(_time_, "%Y-%m-%d/%H:%M:%S")))
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

workPath = reWorkPath()

maxJ = 60
j = -1 #主操作检测变量
setTime = "16:15:00"
debug = False
exit = False

#文件初始化（避免删除

file1 = open(join(workPath,'./images/icon.png'))
file2 = open(join(workPath,'./Font/MiSans-Bold.ttf'))
file3 = open(join(workPath,'./sounds/定时关机提示音.wav'))
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
                run("taskkill /im Taskmgr.exe /f",shell=True)
        else:
            tskReg = """HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\system"""
            run("reg add {} /v DisableTaskMgr /t REG_SZ /d {} /f".format(tskReg,type),shell=True)
            run("taskkill /im Taskmgr.exe /f",shell=True)
    def uac(self,whileTrue:bool=True,type:int=0):
        """禁用UAC"""
        if whileTrue:
            while True:
                uacReg = """HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"""
                run("reg add {} /v EnableLUA /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                run("reg add {} /v PromptOnSecureDesktop /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                run("reg add {} /v ConsentPromptBehaviorAdmin /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
                run("taskkill /im dllhost.exe /f",shell=True)
        else:
            uacReg = """HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"""
            run("reg add {} /v EnableLUA /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            run("reg add {} /v PromptOnSecureDesktop /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            run("reg add {} /v ConsentPromptBehaviorAdmin /t REG_DWORD /d {} /f".format(uacReg,type),shell=True)
            run("taskkill /im dllhost.exe /f",shell=True)
    def startUp(self,whileTrue:bool=True,setFile=False):
        """设置当前用户自启动"""
        run = 0
        while whileTrue or run == 0:
            run += 1
            reg = """SOFTWARE\Microsoft\Windows\CurrentVersion\Run""" # HKEY_CURRENT_USER\
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg,access=winreg.KEY_ALL_ACCESS)
            if not setFile:
                winreg.SetValueEx(key,'systemPowerOff',0,winreg.REG_SZ,'"{}"'.format(argv[0]))
            else:
                winreg.SetValueEx(key,'systemPowerOff',0,winreg.REG_SZ,'"{}"'.format(setFile))
            winreg.CloseKey(key)


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

for f in mainList:
    t = Thread(target=f,args=(),daemon=True)
    t.start()
    threadList.append(t)

def wndproc(hwnd, msg, wparam, lparam): #关机事件后执行的函数
    if datetime.today().isoweekday() < 6 and not time_check(setTime)[-1]:
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

while True:
    if getTime() - lowTime2 >= 1 or debug:
        j += 1
        lowTime2 = getTime()
    if (getTime() - lowTime >= 0.1 and not exit) or debug:
        lowTime = getTime()
        win32gui.PumpWaitingMessages() #捕捉关机主程序
        if time_check(setTime)[-1] or debug:
            if j >= maxJ or debug:
                rec = mainWindow()
                if rec == 1:
                    run('shutdown /s /f /t 0',shell=True)
                    _exit(0)
                elif rec == 2:
                    j = -1
                elif rec == 3:
                    exit = True
                elif rec == 4:
                    j = -1
                    run("explorer {}".format(url),shell=True)
