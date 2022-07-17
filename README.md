# 自动定时关机小程序，解决学生pc管理员忘记关电脑的痛点

## 使用方法<br>
·下载Release解压运行"autoPowerOff.exe"或克隆后使用python 3.9.8 (包含PySide2 + PythonWx + pywin32 + pynput库) 运行Main.py (上述方法首次运行均可能需要安装"MiSans-Semibold-首次运行需要安装此字体.ttf"字体)


## 设置项<br>
·鼠标键盘最大无操作时间（秒）：设置最大时间,单位秒<br>
·关机时间：到达此时间后开始检测鼠标和键盘,若在鼠标键盘无操作时间内无操作则弹出关机提示框并发出提示音,询问是否关机<br>
·强制关机时间：到达此时间后会强制关机(可将其设置为23:59:59以禁用)<br>

## 使用须知<br>
·为保证此程序每次启动计算机均有效,我们将写入自启动项 （位于[注册表](https://docs.microsoft.com/zh-cn/windows/win32/sysinfo/registry) "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",仅对当前用户有效）<br>
·为保证此程序不被关闭,我们将禁用任务管理器并禁用UAC [(UAC是什么?)](https://docs.microsoft.com/zh-cn/windows/security/identity-protection/user-account-control/how-user-account-control-works)<br>

## 感谢您的支持 [个人B站主页](https://space.bilibili.com/687039517)
