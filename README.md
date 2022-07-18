# 自动定时关机小程序，解决学生是电脑管理员忘记关电脑或关电脑烦的痛点

## 用前声明<br>
我是一个初中生,Python萌新,可能有较多处语法不规范的地方,我甚至连怎么将PySide2的UI文件转为py文件并导入项目都不会,请谅解,谢谢.

## 使用方法<br>
·下载Release解压运行"autoPowerOff.exe"或克隆后使用python 3.9.8 (包含PySide2 + PythonWx + pywin32 + pynput库) 运行main.py (上述方法首次运行均可能需要安装"MiSans-Semibold-首次运行需要安装此字体.ttf"字体)<br>
·设置界面可在托盘图标右键后,单击"设置"打开<br>
·托盘图标右键后"关机"选项用于到达关机时间但并未到达强制关机时间,关机提升为弹出时手动关机（为避免Windows自带关机被此程序拦截）<br>

## 设置项<br>
·鼠标键盘最大无操作时间（秒）：设置最大时间,单位秒<br>
·关机时间：到达此时间后开始检测鼠标和键盘,若在鼠标键盘无操作时间内无操作则弹出关机提示框并发出提示音,询问是否关机<br>
·强制关机时间：到达此时间后会强制关机(可将其设置为23:59:59以禁用)<br>

## 使用须知<br>
·为保证此程序每次启动计算机均有效,我们将写入自启动项 （位于注册表 "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",仅对当前用户有效）[(注册表是什么？)](https://docs.microsoft.com/zh-cn/windows/win32/sysinfo/registry)<br>
·为保证此程序不被关闭,我们将禁用任务管理器并禁用UAC (但我们没有禁用"taskkill.exe") [(UAC是什么?)](https://docs.microsoft.com/zh-cn/windows/security/identity-protection/user-account-control/how-user-account-control-works)<br>
·**警告：** _**我们注册了关机检测,若您在非关机时间关机我们将强制重启**_<br>

## 感谢您的支持<br>
### [个人B站主页](https://space.bilibili.com/687039517)
