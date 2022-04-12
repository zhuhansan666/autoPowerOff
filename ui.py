from workPath import reWorkPath
from os.path import join,exists
from os import _exit
from PygameButtonClass import button
from time import time
import pygame,win32gui,win32con,win32com.client
from json import loads,dumps
from json.decoder import JSONDecodeError


def 活动窗口(hwnd):
    try:
        win32com.client.Dispatch("WScript.Shell").SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pass

def head(hwnd): #置顶
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

def mainWindow():
    pygame.init()
    workPath = reWorkPath()

    configJson = open(join(workPath,'./settings.json'),encoding='utf-8')
    try:
        language = str(loads(configJson.read())["language"]).lower()
    except:
        language = 'zh_cn'.lower()
    

    colors = {
        "w":(255,255,255),
        "b":(0,0,0),
        "blue":(43, 16, 195),
    }

    fontFile = join(workPath,"./Font/MiSans-Bold.ttf")
    fontSize = 29
    fontbigSize = 39
    阴影圆角 = 12
    阴影缩放 = 10
    mainY = 70
    titleY = 15
    waitS = 3
    githubButtonPos = (27,67)
    githubButtonSize = 20

    textDic = {
        "button1":"  确定  ",
        "button2":" 稍等,程序后台检测 ",
        "button3":" 取消,我现在退出程序 ",
        "githubButton":"github项目页面",
        "mainText":"已达预定时间,将在{}秒后自动关机~",
        "exitText":"程序已退出,将在{}秒后自动关闭本窗口...",
        "buttonSize":fontSize,
        "githubButtonSize":githubButtonSize,
        "fontbigSize":fontbigSize,
        "soundFile":str(join(workPath,'./sounds/定时关机提示音.wav')),
        "title":str("自动关机提醒 V2.0")
    }

    try:
        with open(join(workPath,'./ui/{}.json'.format(language)),encoding="utf-8") as f:
            try:
                textDic = loads(f.read())
            except JSONDecodeError:
                pass
    except FileNotFoundError:
        pass

    if "buttonSize" not in textDic:
        textDic["buttonSize"] = fontSize
    if "soundFile" not in textDic or not exists(join(workPath,textDic["soundFile"])) or len(str(textDic["soundFile"]).replace(' ','')) <= 0:
        textDic["soundFile"] = str(join(workPath,'./sounds/zh_cn.wav'))
    if "githubButtonSize" not in textDic:
        textDic["githubButtonSize"] = githubButtonSize
    if "fontbigSize" not in textDic:
        textDic["fontbigSize"] = fontbigSize
    if "title" not in textDic:
        textDic["title"] = "自动关机提醒 V2.0"

    font =  pygame.font.Font(fontFile,textDic["buttonSize"])
    fontbig =  pygame.font.Font(fontFile,textDic["fontbigSize"])

    sound = pygame.mixer.Sound(join(workPath,textDic["soundFile"]))
    sound.set_volume(1)
    sound.play()

    clock = pygame.time.Clock()
    icon = pygame.image.load(join(workPath,"./images/icon.png"))
    pygame.display.set_icon(icon)

    pygame.display.set_caption(textDic["title"])

    screen = pygame.display.set_mode((687,150),pygame.NOFRAME)
    screen.fill(colors.get("w"))

    hwnd = pygame.display.get_wm_info()['window']
    head(hwnd)

    pygame.display.flip()


    b1 = button("b1",(5,mainY),(textDic["button1"],fontFile,"file",textDic["buttonSize"],colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    b2 = button("b2",(30,mainY),(textDic["button2"],fontFile,"file",textDic["buttonSize"],colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    b3 = button("b3",(300,mainY),(textDic["button3"],fontFile,"file",textDic["buttonSize"],colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    b4 = button("github",githubButtonPos,(textDic["githubButton"],fontFile,"file",githubButtonSize,colors["blue"],False,False,False),screen)#,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    surface = fontbig.render(textDic["mainText"].format(10),True,colors["b"])
    showS = (round(screen.get_width()/2-surface.get_width()/2),titleY)

    lowTime = time()
    lowTime2 = time()
    outTimeS = 10


    while (True):
        if time() - lowTime2 >= 1:
            lowTime2 = time()
            活动窗口(hwnd)
        surface = fontbig.render(textDic["mainText"].format(outTimeS-round(time()-lowTime)),True,colors["b"])
        showS = (round(screen.get_width()/2-surface.get_width()/2),titleY)
        clock.tick(60)
        evensList = pygame.event.get()
        for e in evensList:
            if e.type == pygame.QUIT:
                pygame.quit()
                return 1
        screen.blit(surface,showS)
        b1.setPos((5,mainY))
        b1.draw(evensList)
        mainY = screen.get_height()-b1.getSize()[1]
        b2.setPos((b1.getEndX()+3,mainY))
        b2.draw(evensList)
        b3.setPos((b2.getEndX()+3,mainY))
        b3.draw(evensList)
        b4.draw(evensList)
        if b1.returnClick()[0]:
            pygame.quit()
            return 1
        if b2.returnClick()[0]:
            pygame.quit()
            return 2
        if b3.returnClick()[0]:
            for i in range(waitS*60+30):
                evensList = pygame.event.get()
                for e in evensList:
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        _exit(0)
                clock.tick(60)
                screen.fill(colors.get("w"))
                surface = font.render(textDic["exitText"].format(waitS-i//60),True,colors["b"])
                show = (round(screen.get_width()/2-surface.get_width()/2),round(screen.get_height()/2-surface.get_height()/2))
                screen.blit(surface,show)
                pygame.display.update()
            pygame.quit()
            return 3
        if b4.returnClick()[0]:
            pygame.quit()
            return 4
        pygame.display.update()
        screen.fill(colors.get("w"))
        if time() - lowTime >= outTimeS:
            pygame.quit()
            return 1

if __name__ == "__main__":
    print(mainWindow())
