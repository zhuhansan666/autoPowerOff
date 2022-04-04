from workPath import reWorkPath
from os.path import join
from os import _exit
from PygameButtonClass import button
from time import time
import pygame,win32gui,win32con,win32com.client
pygame.init()

def 活动窗口(hwnd):
    win32com.client.Dispatch("WScript.Shell").SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)

def head(hwnd): #置顶
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

def mainWindow():
    workPath = reWorkPath()


    colors = {
        "w":(255,255,255),
        "b":(0,0,0),
    }

    sound = pygame.mixer.Sound(join(workPath,'./sounds/定时关机提示音.wav'))
    sound.set_volume(1)
    sound.play()

    clock = pygame.time.Clock()
    icon = pygame.image.load(join(workPath,"./images/icon.png"))
    pygame.display.set_icon(icon)

    pygame.display.set_caption("自动关机提醒 2.0")

    screen = pygame.display.set_mode((687,150),pygame.NOFRAME)
    screen.fill(colors.get("w"))

    hwnd = pygame.display.get_wm_info()['window']
    head(hwnd)

    pygame.display.flip()

    fontFile = join(workPath,"./Font/MiSans-Bold.ttf")
    fontSize = 29
    阴影圆角 = 12
    阴影缩放 = 10
    mainY = 70
    titleY = 15
    waitS = 3
    font =  pygame.font.Font(fontFile,fontSize)
    fontbig =  pygame.font.Font(fontFile,fontSize+10)


    b1 = button("确定,我现在关机",(5,mainY),('  确定  ',fontFile,"file",fontSize,colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    b2 = button("稍等,程序后台检测",(30,mainY),(' 稍等,程序后台检测 ',fontFile,"file",fontSize,colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    b3 = button("取消,我现在退出程序",(300,mainY),(' 取消,我现在退出程序 ',fontFile,"file",fontSize,colors["b"],False,False,False),screen,选中阴影=True,阴影颜色=(127,127,127),阴影透明度=200,阴影圆角=阴影圆角,阴影缩放=阴影缩放)
    surface = fontbig.render("已达预定时间,将在10秒后自动关机~",True,colors["b"])
    showS = (round(screen.get_width()/2-surface.get_width()/2),titleY)

    lowTime = time()
    lowTime2 = time()
    outTimeS = 10


    while (True):
        if time() - lowTime2 >= 1:
            lowTime2 = time()
            活动窗口(hwnd)
        surface = fontbig.render("已达预定时间,将在{}秒后自动关机~".format(outTimeS-round(time()-lowTime)),True,colors["b"])
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
                surface = font.render("程序已退出,将在{}秒后自动关闭本窗口...".format(waitS-i//60),True,colors["b"])
                show = (round(screen.get_width()/2-surface.get_width()/2),round(screen.get_height()/2-surface.get_height()/2))
                screen.blit(surface,show)
                pygame.display.update()
            pygame.quit()
            return 3
        pygame.display.update()
        screen.fill(colors.get("w"))
        if time() - lowTime >= outTimeS:
            pygame.quit()
            return 1

if __name__ == "__main__":
    mainWindow()
