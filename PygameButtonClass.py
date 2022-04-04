import pygame
pygame.init()
class button(object):
    '''buttonInfo若使用文字: [text,fout,foutType,size,color,背景色{颜色或False},透明度{False或0-255}] 或者 (text,fout,foutType,size,color,背景色{颜色或False},透明度{False或0-255})'''
    def __init__(self,buttonName:str,buttonPos:list or tuple,buttonInfo:list or tuple or pygame.Surface,screen:pygame.Surface,buttonTmd:int=255,screenUpdate=False,buttonSize:bool or list or tuple=False,选中阴影:bool=False,阴影颜色:list or tuple=None,阴影缩放:int or bool=False,阴影透明度:int=0,阴影圆角:bool or int=False,描边:int=0):
        '''buttonInfo若使用文字: [text,fout,foutType,size,color,背景色{颜色或False},透明度{False或0-255}] 或者 (text,fout,foutType,size,color,背景色{颜色或False},透明度{False或0-255})'''
        self.Version = 'Beat-1.2.114514'
        self.Name = buttonName
        self.buttonTmd = buttonTmd
        self.buttonPos = buttonPos
        self.buttonInfo = buttonInfo
        self.阴影 = 选中阴影
        self.阴影颜色 = 阴影颜色
        self.阴影透明度 = 阴影透明度
        self.阴影圆角 = 阴影圆角
        self.阴影缩放 = 阴影缩放
        self.描边 = 描边
        self.screen = screen
        self.screenUpdate = screenUpdate
        self.buttonSize = buttonSize
        self.button = False
        self.buttonType = -1
        self.buttonSurfaceSize = None
    def getEndX(self):
        return self.buttonPos[0]+self.buttonSurfaceSize[0]
    def getEndY(self):
        return self.buttonPos[1]+self.buttonSurfaceSize[1]
    def getSize(self):
        return self.buttonSurfaceSize
    def getPos(self):
        return (self.buttonPos[0],self.buttonPos[1])
    def setMainTmd(self,buttonTmd:int=255):
        self.buttonTmd = buttonTmd
    def setPos(self,buttonPos:list or tuple):
        self.buttonPos = buttonPos
    def setSurface(self,surface:list or tuple or pygame.Surface):
        self.buttonInfo = surface
    def setInfo(self,buttonInfo):
        self.buttonInfo = buttonInfo
    def checkPos(self,nowPos:list or tuple,checkPos:list or tuple):
        if (nowPos[0] >= checkPos[0] and nowPos[0] <= checkPos[2]) and (nowPos[1] >= checkPos[1] and nowPos[1] <= checkPos[3]):
            return True
        else:
            return False
    def returnClick(self):
        return (self.button,self.buttonType,self.Name)
    def set阴影缩放(self,阴影缩放):
        self.阴影缩放 = 阴影缩放
    def setYYtmd(self,tmd):
        self.阴影透明度 = tmd
    def draw(self,eventList):
        '''受pygame按键抓取限制,请将按键列表保存并传入本函数'''
        self.button = False
        if self.buttonSize != False: #设定对象大小
            buttonSurface = pygame.Surface(self.buttonSize) #应用大小
        # elif self.buttonSize == False:  #不使用设定对象大小(Size)(使用自动匹配)
        if type(self.buttonInfo) != pygame.Surface:
            if self.buttonInfo[2] == 'system':  #类型为 调用系统字体
                fout = pygame.font.SysFont(self.buttonInfo[1],self.buttonInfo[3])  #调用系统字体，获取list 的 字体位置,Size
            elif self.buttonInfo[2] == 'file':  #类型为 调用字体文件
                fout = pygame.font.Font(self.buttonInfo[1],self.buttonInfo[3])  #调用字体文件字体，获取list 的 字体位置,Size
            if self.buttonInfo[5] != False:  #判断背景色为启用状态
                s = fout.render(str(self.buttonInfo[0]),True,self.buttonInfo[4],self.buttonInfo[5])  #设置一系列参数(内容，是否抗锯齿，颜色，背景色)
            elif self.buttonInfo[5] == False:
                s = fout.render(str(self.buttonInfo[0]),True,self.buttonInfo[4])  #设置一系列参数(内容，是否抗锯齿，颜色)
            if self.buttonInfo[6] != False:  #若需要更改透明度
                s.set_alpha(self.buttonInfo[6])  #设置透明度
            buttonSurface = s #赋值对象
            # buttonSurface = pygame.Surface(s.get_size()) #设定为对象大小
            # buttonSurface.blit(s, (0,0)) #画对象
        else:
            buttonSurface = self.buttonInfo #赋值对象
            # buttonSurface = pygame.Surface(self.buttonInfo.get_size()) #设定为对象大小
            # buttonSurface.blit(self.buttonInfo, (0,0)) #画对象
        surfaceSize = buttonSurface.get_size() #获取对象大小

        tempSurface = buttonSurface
        tempSurface.set_alpha(self.buttonTmd) #设置透明度
        
        # eventList = pygame.event.get()
        if self.阴影:
            if len(eventList) == 0:
                mousePos = pygame.mouse.get_pos() #获取鼠标位置
                surfacePos = (self.buttonPos[0],self.buttonPos[1],surfaceSize[0],surfaceSize[1]) #获取对象位置
                surfacePos2 = (self.buttonPos[0]-self.阴影缩放//2,self.buttonPos[1]-self.阴影缩放//2,self.buttonPos[0]-self.阴影缩放//2+surfacePos[2]+self.阴影缩放,self.buttonPos[1]-self.阴影缩放//2+surfacePos[3]+self.阴影缩放) #获取阴影位置(真实位置)
            for e in eventList: #更新鼠标位置并获取操作
                mousePos = pygame.mouse.get_pos() #获取鼠标位置
                surfacePos = (self.buttonPos[0],self.buttonPos[1],surfaceSize[0],surfaceSize[1]) #获取对象位置
                surfacePos2 = (self.buttonPos[0]-self.阴影缩放//2,self.buttonPos[1]-self.阴影缩放//2,self.buttonPos[0]-self.阴影缩放//2+surfacePos[2]+self.阴影缩放,self.buttonPos[1]-self.阴影缩放//2+surfacePos[3]+self.阴影缩放) #获取阴影位置(真实位置)
                if e.type == pygame.MOUSEBUTTONUP: #检测是否鼠标左键是否弹起
                    if self.checkPos(e.pos,surfacePos2): #检测是否按下按钮
                        self.buttonType = e.button #left 1,moddle 2,right 3,侧键(left Down) 6,鼠标滚轮上 4,鼠标滚轮下 5,...
                        self.button = True
            if self.checkPos(mousePos,surfacePos2): #检测鼠标位置是否在对象(按钮)上
                阴影Surface = pygame.Surface(self.screen.get_size()) #设置对象大小
                if self.阴影圆角 != False: #圆角
                    阴影Surface = 阴影Surface.convert_alpha() #设置可更改颜色值
                    阴影Surface.fill((0,0,0,0)) #填充透明颜色
                    pygame.draw.rect(阴影Surface, self.阴影颜色, (self.buttonPos[0]-self.阴影缩放//2,self.buttonPos[1]-self.阴影缩放//2,surfacePos[2]+self.阴影缩放,surfacePos[3]+self.阴影缩放),self.描边,border_radius=self.阴影圆角) #画阴影(圆角)
                else:
                    阴影Surface.fill(self.阴影颜色) #设置阴影颜色
                阴影Surface.set_alpha(self.阴影透明度) #设置阴影透明度
                self.screen.blit(阴影Surface, (0,0)) #画选中阴影
        else:
            if len(eventList) == 0:
                mousePos = pygame.mouse.get_pos() #获取鼠标位置
                surfacePos = (self.buttonPos[0],self.buttonPos[1],self.buttonPos[0]+surfaceSize[0],self.buttonPos[1]+surfaceSize[1]) #获取对象位置
            for e in eventList: #更新鼠标位置并获取操作
                mousePos = pygame.mouse.get_pos() #获取鼠标位置
                surfacePos = (self.buttonPos[0],self.buttonPos[1],self.buttonPos[0]+surfaceSize[0],self.buttonPos[1]+surfaceSize[1]) #获取对象位置
                if e.type == pygame.MOUSEBUTTONUP: #检测是否鼠标左键是否弹起
                    if self.checkPos(e.pos,surfacePos): #检测是否按下按钮
                        self.buttonType = e.button #left 1,moddle 2,right 3,侧键(left Down) 6,鼠标滚轮上 4,鼠标滚轮下 5,...
                        self.button = True

        self.screen.blit(tempSurface,self.buttonPos) #画主对象
        if self.screenUpdate: #检测是否自动更新屏幕
            pygame.display.update() #跟新屏幕
        self.buttonSurfaceSize = (surfacePos[2]+self.阴影缩放,surfacePos[3]+self.阴影缩放) #赋值按钮大小
