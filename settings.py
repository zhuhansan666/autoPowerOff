from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
from workPath import reWorkPath
from os.path import join
from json import loads,dumps
# from threading import Thread
import time
import wx
import wx.adv

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

workPath = reWorkPath()

class Stats():
    def __init__(self):
        super(Stats,self).__init__()

        self.languagesList = [ #对应文件(./ui/*.json)
            "zh_cn",
            "en_us",
        ]
        self.languages = [ #显示内容(需一一对应)
            "简体中文",
            "English(US)",
        ]
        self.languagesDic = {}
        for i in range(len(self.languagesList)):
            self.languagesDic[self.languagesList[i]] = "{}".format(i)

        self.language = self.languagesList[0]
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        qfileTemp = QFile(join(workPath,'./qtui/main.ui'))
        qfileTemp.open(QFile.ReadOnly)
        qfileTemp.close

        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(join(workPath,'./qtui/main.ui'))
        self.ui.setWindowIcon(QIcon(join(workPath,'./images/icon.png')))
        # SysTray = QSystemTrayIcon(self.ui)
        # SysTray.setIcon(QIcon(join(workPath,'./images/icon.png')))
        self.ui.setWindowTitle('自动关机 - 设置')

        # SysTrayMenu = QMenu()
        # SysTrayMenu.addAction(QAction("设置",triggered = self.ui.show))
        # SysTray.setContextMenu(SysTrayMenu)
        # SysTrayMenu.show()
        # SysTray.showMessage("123",'Test',0)

    #     self.ui.Button.clicked.connect(self.handleCalc)
        self.ui.setFixedSize(500, 330) # 禁用最大化和拖拽改变大小

        with open(join(workPath,'./settings.json'),"r+",encoding='utf-8') as jsonF:
            jsonDic = loads(jsonF.read())
        self.ui.spinBoxH.setMaximum(23)
        self.ui.spinBoxH.setMinimum(0)
        self.ui.spinBoxH.setValue(int(str(jsonDic["time"]).split(':')[0]))
        self.ui.spinBoxM.setMaximum(60)
        self.ui.spinBoxM.setMinimum(0)
        self.ui.spinBoxM.setValue(int(str(jsonDic["time"]).split(':')[1]))
        self.ui.spinBoxS.setMaximum(60)
        self.ui.spinBoxS.setMinimum(0)
        self.ui.spinBoxS.setValue(int(str(jsonDic["time"]).split(':')[2]))
        self.ui.spinBoxH2.setMaximum(23)
        self.ui.spinBoxH2.setMinimum(0)
        self.ui.spinBoxH2.setValue(int(str(jsonDic["poTime"]).split(':')[0]))
        self.ui.spinBoxM2.setMaximum(60)
        self.ui.spinBoxM2.setMinimum(0)
        self.ui.spinBoxM2.setValue(int(str(jsonDic["poTime"]).split(':')[1]))
        self.ui.spinBoxS2.setMaximum(60)
        self.ui.spinBoxS2.setMinimum(0)
        self.ui.spinBoxS2.setValue(int(str(jsonDic["poTime"]).split(':')[2]))
        self.ui.waitTimeBox.setValue(jsonDic['waitTime'])
        self.ui.chooseBox.addItems(self.languages)
        self.ui.chooseBox.setCurrentIndex(int(self.languagesDic[jsonDic["language"]]))

        self.ui.chooseBox.currentIndexChanged.connect(self.changeLanguage)
        self.ui.OKButton.clicked.connect(lambda:self.okButtonDown(apply=False))
        self.ui.CloseButton.clicked.connect(self.CloseButtonDown)
        self.ui.ApplyButton.clicked.connect(lambda:self.okButtonDown(apply=True))

    def changeLanguage(self,num):
        self.language = self.languagesList[num]
    def getLanguage(self) -> str:
        return self.language

    def okButtonDown(self,apply=False):
        setTime = "{}:{}:{}".format(str(self.ui.spinBoxH.value()).zfill(2),str(self.ui.spinBoxM.value()).zfill(2),str(self.ui.spinBoxS.value()).zfill(2)) #.zfill(int) 补零，仅限字符串
        setPowerOffTime = "{}:{}:{}".format(str(self.ui.spinBoxH2.value()).zfill(2),str(self.ui.spinBoxM2.value()).zfill(2),str(self.ui.spinBoxS2.value()).zfill(2))
        try:
            # 语言设置
            with open(join(workPath,'./settings.json'),"r+",encoding='utf-8') as jsonF:
                jsonDic = loads(jsonF.read())
            with open(join(workPath,'./settings.json'),"w+",encoding='utf-8') as jsonF:
                jsonDic["language"] = self.getLanguage()
                # 时间设置
                if time_check(setTime) != "错误:时间格式问题":
                    jsonDic["time"] = setTime
                if time_check(setPowerOffTime) != "错误:时间格式问题":
                    jsonDic["poTime"] = setPowerOffTime
                jsonDic['waitTime'] = self.ui.waitTimeBox.value()
                # 写入
                jsonF.write(dumps(jsonDic))
            if not apply: #是否为应用更改模式
                QApplication.quit() #否,则退出
        except Exception:
            pass
        if not apply:
            self.ui.close()

    def CloseButtonDown(self):
        self.ui.close()


app = QApplication([])

def show():
    stats = Stats()
    stats.ui.show()
    app.exec_()

# test = Thread(target=show,kwargs={})
# test.start()

class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = join(workPath,"./images/icon.png")  # 图标地址
    ID_ABOUT = wx.NewId()  # 菜单选项“关于”的ID
    ID_EXIT = wx.NewId()  # 菜单选项“退出”的ID
    ID_SHOW_WEB = wx.NewId()  # 菜单选项“显示页面”的ID
    TITLE = "自动关机设置" #鼠标移动到图标上显示的文字

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        # self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
        # self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)  # 绑定“设置”选项的点击事件

    # “显示页面”选项的事件处理器
    def onShowWeb(self, event):
        show()

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    # 获取菜单的属性元组
    def getMenuAttrs(self):
        return [('设置', self.ID_SHOW_WEB)]


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()#显示系统托盘图标


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True

def main():
    app = MyApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
