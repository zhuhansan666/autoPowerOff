# 自动定时关机小程序，解决学生pc管理员忘记关电脑的痛点

使用方法
·下载Release解压运行"autoPowerOff.exe"或克隆后使用python 3.9.8 (包含PySide2 + PythonWx + pywin32 + pynput库) 运行Main.py (上述方法首次运行均可能需要安装"MiSans-Semibold-首次运行需要安装此字体.ttf"字体)

设置项
·鼠标键盘最大无操作时间（秒）：设置最大时间,单位秒
·关机时间：到达此时间后开始检测鼠标和键盘,若在鼠标键盘无操作时间内无操作则弹出关机提示框并发出提示音,询问是否关机
·强制关机时间：到达此时间后会强制关机(可将其设置为23:59:59将其禁用)
