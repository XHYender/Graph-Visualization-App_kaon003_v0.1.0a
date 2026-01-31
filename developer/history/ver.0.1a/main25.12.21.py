#coding=utf-8

"""
Idea Visualization

Codes Rule:
注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；
变量名用蛇形命名法(frame_per_second);
函数名用驼峰命名法(saveDataAsFormatJSON);
类名用帕斯卡命名法(Mode);
全局变量、常量全大写;
非局部变量请用带有完整意义的英文词组或拼音(english_var_name,pinyintailowlegaodexiangxiaoxueshen);
变量列表请在确保可读性的同时适当换行;
记号[优化]代表我在用我显得有点可笑的知识在做优化;
"""
#from logging import info
import tkinter as tk
import time as t


class Vector:
    """
    2d vector
    """
    def __init__(self,x=0,y=0):
        self.x,self.y = x,y

    def distanceTo(self,other):
        if isinstance(other,Vector):return ((self.x-other.x)**2+(self.y-other.y)**2)**0.5
        else:raise TypeError

    def verticle(self,reverse=False):
        if reverse:return Vector(self.y,-self.x)    #顺时针90
        else:return Vector(-self.y,self.x)          #逆时针90[默认]

    def det(self,other):
        if isinstance(other,Vector):return self.x*other.y-self.y*other.x
        else:raise TypeError

    def cos(self,other):
        if isinstance(other,Vector):return (self*other)/(abs(self)*abs(other))
        else:raise TypeError

    def sin(self,other):
        if isinstance(other,Vector):return self.det(other)/(abs(self)*abs(other))
        else:raise TypeError

    def __repr__(self):
        return f'({self.x},{self.y})'

    def __str__(self):
        return f'({self.x},{self.y})'

    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)

    def __iadd__(self,other):
        return self+other

    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)

    def __isub__(self,other):
        return self-other

    def __mul__(self,other):
        if isinstance(other,(int,float)):return Vector(self.x*other,self.y*other)       #数乘
        elif isinstance(other,Vector):return self.x*other.x+self.y*other.y              #点乘
        else:raise TypeError

    def __imul__(self,other):
        return self*other

    def __rmul__(self,other):
        return self*other

    def __truediv__(self,other):
        if isinstance(other,(int,float)):return Vector(self.x/other,self.y/other)       #数除
        else:raise TypeError

    def __floordiv__(self,other):
        if isinstance(other,int):return Vector(self.x//other,self.y//other)
        elif isinstance(other,Vector):return Vector(self.x//other.x,self.y//other.y)
        else:raise TypeError

    def __mod__(self,other):
        if isinstance(other,int):return Vector(self.x%other,self.y%other)
        elif isinstance(other,Vector):return Vector(self.x%other.x,self.y%other.y)
        else:raise TypeError

    def __abs__(self):
        return ( self.x**2 + self.y**2 )**0.5   #取模
    
    def __eq__(self,other):         #逐个分量比较，等效于self - other ~ (0,0)
        if isinstance(other,Vector):return self.x==other.x and self.y==other.y
        else:raise ValueError

    def __lt__(self,other):
        if isinstance(other,Vector):return self.x<other.x and self.y<other.y
        else:raise ValueError
        
    def __ne__(self,other):
        return not self==other
    
    def __le__(self,other):
        return self == other or self <other
    
    def __ge__(self,other):
        return not self<other
    
    def __gt__(self,other):
        return not self <= other

    

class Mode:
    """
    模式列表modes_list
    以modes_list的索引作为各个mode的id
    """
    def __init__(self,modes_list:list=['Off','On'],default_mode:int=0):
        self.modes=modes_list
        self.mode=default_mode%len(modes_list)

    def switch(self,step:int=1):
        """
        切换mode，默认步长step=1;
        若想逆序切换，请设置step=-1
        """
        self.mode=(self.mode+step)%len(self.modes)
        return self

    def __str__(self):
        return self.modes[self.mode]
    
    def __format__(self,spec):
        if spec=='id':return f'{str(self)}:{self.mode}'
        elif spec=='idonly':return str(self.mode)
        else:return str(self)
    
    def __len__(self):
        return len(self.modes)
    
    def __getitem__(self,index):
        return self.modes[index]
    
    def __setitem__(self,index,value):
        self.modes[index]=value

    def __delitem__(self,index):
        del self.modes[index]

    def __iter__(self):
        return iter(self.modes)

    def __eq__(self,other):
        if isinstance(other,int):return self.mode==other
        elif isinstance(other,str):return str(self)==other
        else:raise ValueError

    def __lt__(self,other):
        if isinstance(other,(int,float)):return self.mode<other
        elif isinstance(other,str)and other in self.modes:return self.mode<self.modes.index(other)#NeverUseItIfYoureIdiot
        else:raise ValueError
        
    def __ne__(self,other):
        return not self==other
    
    def __le__(self,other):
        return self == other or self <other
    
    def __ge__(self,other):
        return not self<other
    
    def __gt__(self,other):
        return not self <= other
    
    def __iadd__(self,other):
        if isinstance(other,int):return self.switch(step=other)
        else:raise ValueError
    
    def __isub__(self,other):
        if isinstance(other,int):return self.__iadd__(other*-1)
        else:raise ValueError

class TriStates:
    """三态"""
    def __init__(self):
        self.state=Mode(['low','wait','high'])

    def low(self):
        self.state.mode=0
    def wait(self):
        self.state.mode=1
    def high(self):
        if self.state.mode==1:
            self.state.mode=2

class Node(TriStates):
    def __init__(self,p:Vector=Vector(),text:str='None',r=15):
        super().__init__()
        self.position = p
        self.text=text
        self.r=r
        self.light=Mode()

class Line(TriStates):
    def __init__(self,source:Node,target:Node,heading:bool=True,weight=1,width=3):
        """
        一条线

        :param source: 起点
        :type source: Vector
        :param target: 终点
        :type target: Vector
        :param heading: 是否有向(T/F)
        :type heading: bool
        :param weight: 权重(默认1)
        """
        super().__init__()
        self.source=source
        self.target=target
        self.heading=heading
        self.weight=weight
        self.width=width
        self.vector=source.position-target.position

    def flip(self):
        """起点终点翻转"""
        self.source,self.target = self.target,self.source

    def updateVector(self):
        self.vector=self.source.position-self.target.position
        
class Limb:
    """Forward And Back Reaching Inverse Kinematics"""
    def __init__(self,S=Vector(),N=2,fixed=True,joints_size_ratio=10,limbs_lenth_ratio=50,delta = 1):
        self.S = S  #根节点
        self.N = N
        self.isfixed = fixed    #根节点是否固定

        self.limbs_lenth_ratio = limbs_lenth_ratio
        self.joints_size_ratio = joints_size_ratio
        #渲染相关

        self.delta = delta
        #末端可接受误差

        self.lenths = [self.limbs_lenth_ratio*(1+2**(-1-i)) for i in range(N)]
        self.lenths.reverse()
        self.joints = [S+Vector(s,0) for s in [ sum(self.lenths[0:i:]) for i in range(N+1) ] ]

    def fabrik(self,S:Vector,T:Vector):
        self.joints[-1] = T
        for i in range(self.N-1,-1,-1):
            v = self.joints[i+1]-self.joints[i]
            self.joints[i] += v*(1-self.lenths[i]/abs(v))
        #forward reaching

        if self.isfixed:
            self.joints[0] = S
            for i in range(self.N):
                v = self.joints[i]-self.joints[i+1]
                self.joints[i+1] += v*(1-self.lenths[i]/abs(v))
        #back inverse

    def iterate(self,S:Vector,T:Vector):
        for _ in range(5):  #5次迭代上限防止找不到解决方案（目标点在可触范围之外导致的无限迭代）
            if T.distanceTo(self.joints[-1]) <= self.delta:
                break
            self.fabrik(S,T)
  
class SOS:
    """Second-Order System"""
    def __init__(self,init_position:Vector=Vector(),f=1,s=1,r=0):
        """
        
        :param f: 固有频率：系统对变化的响应速度、震动时的大致频率
        :param s: 阻尼系数：0:无阻尼；0<_<1:小阻尼；>1:过阻尼
        :param r: 初始响应：0:缓释反应：0<_<1:即时反应；>1:过反应；<0:预反应 
        """
        self.f = f
        self.s = s
        self.r = r

        pi = 3
        #近似圆周率
        self.a = self.s/(pi*self.f)
        self.b = (self.f*self.f)/(4*pi*pi)
        self.c = (self.r*self.a)/2
        #物理参数

        self.p = self.pp = self.prp = init_position        
        self.prs = Vector(0,0)
        #位置初始化
        
    def react(self,dt,p:Vector,pp:Vector,prp:Vector,prs:Vector):
        """
        p:position
        pp:previous position
        prp:previous reacted position
        prs:previous reacted speed
        rp:reacted position
        rs:reacted speed
        """
        rp = prp + prs*dt
        #rp:reacted position
        rs = prs + (p+(p-pp)*(self.c/dt)-self.a*prs-rp)*(dt/self.b)
        #rs:reacted speed

        return rp,rs

    def iterate(self,T:Vector,dt):
        self.pp = self.p
        self.p = T
        self.prp,self.prs = self.react(dt,self.p,self.pp,self.prp,self.prs)






class Framework:
    """
    基于time_process的帧处理渲染窗口框架
    待重写方法有：update()、render()、bindEvent()
    """
    def __init__(self,title:str,width:int,height:int):
        self.root=tk.Tk()
        self.window_title =title
        self.window_height = height
        self.window_width = width
        #程序窗口属性

        self.createWindow()
        self.createCanva()
        self.bindEvents()

        self.running = True
        self.target_fps = 60
        self.frame_time = 1/self.target_fps
        self.delta_time = 0             #delta_time
        self.last_time = t.time()
        #初始化game_loop锁时间帧数据

        self.fps_timer = t.time()
        self.fps , self.frame_count = 0,0
        #初始化fps计数器数据

    def createWindow(self):
        """配置窗口属性"""

        self.root.update_idletasks()
        y = (self.root.winfo_screenheight()-self.window_height)//2
        x = (self.root.winfo_screenwidth()-self.window_width)//2
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        #窗口大小、位置居中(1X2+3+4)

        self.root.resizable(True,True)
        #窗口大小是否可拉伸(宽,高)
        self.root.minsize(300,300)
        #窗口最小宽高
        #self.root.overrideredirect(True)
        #移除窗口边框
        self.root.iconbitmap('assets\enchantingtable0.ico')
        #窗口图标 (同目录.ico文件)
        self.root.title(self.window_title)
        #窗口标题

        self.root.attributes(
            '-topmost',False,                  #窗口始终在最前面;
            '-transparentcolor','',            #窗口指定色‘’为透明;
            '-toolwindow', False,              #窗口无任务栏图标;
            '-fullscreen', False               #全屏模式;
        )
    
    def createCanva(self):
        self.canva = tk.Canvas(
            self.root,
            width = self.window_width,
            height = self.window_height,
            bg='#1a1a2e'
        )
        self.canva.pack(fill=tk.BOTH, expand=1)     #画布填充窗口
    
    def bindEvents(self):
        """输入绑定事件(抽象方法)"""
        #self.canva.bind('<input_event>',triggerFunction)
        pass

    def calculateFPS(self,current_time):
        """计算帧率"""
        self.frame_count += 1
        if current_time - self.fps_timer >= 1:
           self.fps = self.frame_count
           self.frame_count = 0
           self.fps_timer = current_time

    def update(self):
        """实际运算逻辑(抽象方法)"""
        pass

    def render(self):
        """帧渲染逻辑(抽象方法)"""
        pass

    def gameLoop(self):
        """游戏循环"""
        if not self.running:
            return

        current_time = t.time()
        self.delta_time = current_time - self.last_time

        if self.delta_time >= self.frame_time:
            self.last_time = current_time

            self.calculateFPS(current_time)

            self.update()

            self.render()

        self.root.after(1,self.gameLoop)

    def run(self):
        """启动游戏主循环"""
        print("Waiting for open...")
        self.root.after(10,self.render)
        print("OPEN!")
        self.gameLoop()
        self.root.mainloop()
        
        # 创建主窗口

    def close(self):
        """窗口关闭时的清理工作"""
        self.running = False
        print('Waiting for close...')
        self.root.quit()
        print("CLOSE!")


class DisciplineAPP(Framework):

    def initModes(self):
        """初始化mode们"""
        self.test_limb_mode = Mode(['Fixed','Instant','SOS'])
        self.info_mode = Mode()
        self.adjoin_graph_mode=Mode()
        self.scene_mode = Mode(['for limbs','for nodes'],1)

    def __init__(self,title:str='附魔台[Debug]',width:int =1080,height:int=720):
        super().__init__(title,width,height)

        self.initModes()

        self.pointer_position = Vector()
        self.pointer_radius=5
        self.pointer_focus=[Mode(['None','Node','Line','Canva']),None]      #[类，id]
        self.pointer_selected=[Mode(['None','Node','Line','Canva']),None]   #[类，id]
        #初始化指针

        self.S=Vector(300,300)                      #test limb的末节点生成点
        self.test_limb = Limb(self.S,5,False,8,20)
        #初始化test_limb

        self.sos = SOS(self.S,1,0.9,0.8)
        #初始化二阶系统
    
        self.limbs=[]
        #初始化limb实体模拟的实体槽 TODO

        self.temp_delta_for_move=Vector()
        #用于相对固定的移动的临时量

        self.nodes={}
        self.node_counts=0                  #节点id计数用数据
        self.node_high_pic=(5,10)           #节点高姿态绘制用数据（距离，长度）
        #初始化节点集

        self.lines={}
        self.line_counts=0
        self.line_temp_sor_id=None          #新线起点，用于创建线（可视为非None时是创建线模式）
        #初始化线集

        self.adjoin_graph={}
        #初始化邻接表


    def bindEvents(self):
        """绑定事件处理"""

        self.root.bind('<Configure>', self.onResize)    #窗口大小改变事件

        self.root.bind('<KeyPress>', self.onKeyPress)   #键盘按键

        self.root.bind('<KeyPress-Escape>', self.onKeyPressEsc) 
        self.root.bind('<KeyPress-space>', self.onKeyPressSpace)
        self.root.bind('<KeyPress-F3>', self.onKeyPressF3) 
        self.root.bind('<KeyPress-s>', self.onKeyPressS)
        self.root.bind('<KeyPress-S>', self.onKeyPressS)
        self.root.bind('<KeyPress-c>', self.onKeyPressC)
        self.root.bind('<KeyPress-C>', self.onKeyPressC)
        self.root.bind('<KeyPress-d>', self.onKeyPressD)
        self.root.bind('<KeyPress-D>', self.onKeyPressD)
        self.root.bind('<KeyPress-m>', self.onKeyPressM)
        self.root.bind('<KeyPress-M>', self.onKeyPressM)


        self.canva.bind('<Motion>',self.onMouseMove)    #鼠标移动

        self.canva.bind('<Button-1>', self.onMouseLClick)               #左键按下
        self.canva.bind('<B1-Motion>', self.onMouseLDrag)               #左键拖动
        self.canva.bind('<ButtonRelease-1>', self.onMouseLRelease)      #左键释放
        self.canva.bind("<Double-Button-1>", self.onMouseLDoubleClick)  #左键双击

        self.canva.bind('<Button-3>',self.onMouseRClick)                #右键
        self.canva.bind('<B3-Motion>', self.onMouseRDrag)
        self.canva.bind('<ButtonRelease-3>', self.onMouseRRelease)
        '''
        self.canva.bind('<Button-2>',self.onMouseRClick)                #中键
        self.canva.bind('<B2-Motion>', self.onMouseRDrag)
        self.canva.bind('<ButtonRelease-2>', self.onMouseRRelease)
        '''
    #begin{Events}

    def onMouseMove(self,event):
        """鼠标移动事件"""
        self.pointer_position = Vector(event.x,event.y) #event.x,event.y

    def onResize(self,event):
        """窗口大小改变时的改动"""
        if event.widget == self.root:
            self.window_width = self.canva.winfo_width() 
            self.window_height = self.canva.winfo_height() 
            #获取当前画布大小
            self.render()
            
    def onKeyPress(self,event):
        print(f"Key: {event.keycode}, Sym: {event.keysym}, Char: {event.char}")

    def onKeyPressF3(self,event):
        self.info_mode.switch()

    def onKeyPressEsc(self,event):
        self.close()

    def onKeyPressSpace(self,event):
        self.test_limb_mode.switch()

        if self.test_limb_mode ==2:
            self.sos.prp =self.sos.p=self.pp= self.pointer_position
            self.sos.prs = Vector()
            #让sos继承上个mode结束时的位置

    def onKeyPressS(self,event):
        self.scene_mode.switch()

    def onKeyPressC(self,event):
        if self.scene_mode == 1:
            self.makeNewNode(self.pointer_position)

    def onKeyPressD(self,event):
        if self.pointer_focus[0] != 0 or 3:
            if self.pointer_focus[0] == 1:
                del self.nodes[self.pointer_focus[1]]

    def onKeyPressM(self,event):
        self.adjoin_graph_mode.switch()

    def onMouseLClick(self,event):
        if self.pointer_focus[0]==1:            #Node
            self.nodes[self.pointer_focus[1]].high()
            self.pointer_selected[0].mode=1
            self.pointer_selected[1]=self.pointer_focus[1]
            self.makeRelativeMove(self.nodes[self.pointer_focus[1]].position,self.pointer_position)

        elif self.pointer_focus[0]==3:          #Canva
            self.pointer_selected[0].mode=3
            self.pointer_selected[1]=self.pointer_position

    def onMouseLDrag(self,event):
        self.onMouseMove(event)
        if self.pointer_selected[0]!=0:
            if self.pointer_selected[0]==1:     #Node
                self.nodes[self.pointer_selected[1]].position=self.pointer_position+self.temp_delta_for_move    #节点移动
                for id,line in self.lines.items():
                    if self.nodes[self.pointer_selected[1]] in (line.source,line.target):
                        self.lines[id].updateVector()


            elif self.pointer_selected[0]==3:   #Canva
                pass
             
    def onMouseLRelease(self,event):
        if self.pointer_selected[0]==1:         #Node
            self.nodes[self.pointer_selected[1]].low()
        self.makePointerSelectedNone()   #释放pointer selected

    def onMouseLDoubleClick(self,event):
        if self.pointer_focus[0]==1:        #Node
            self.nodes[self.pointer_focus[1]].light.switch()

    def onMouseRClick(self,event):
        if self.pointer_focus[0]==3:    #在Canva上（非Node、Line）创建Node
            self.makeNewNode(self.pointer_position)

        elif self.pointer_focus[0]==1:  #在Node上创建Line
            self.line_temp_sor_id=self.pointer_focus[1]
            self.makeNewLine(Node(p=self.nodes[self.pointer_focus[1]].position,
                r=self.nodes[self.pointer_focus[1]].r),Node(p=self.pointer_position,r=self.pointer_radius))     #创建preview line
            self.pointer_selected[0].mode=2
            self.pointer_selected[1]=self.line_counts
            if self.adjoin_graph.get(self.line_temp_sor_id,None) is None:   #在邻接表中添加节点
                self.adjoin_graph[self.line_temp_sor_id] = {}
            
    def onMouseRDrag(self,event):
        self.onMouseMove(event)
        if self.line_temp_sor_id is not None:       #创建线过程中箭头指向pointer
            self.lines[self.line_counts].target.position=self.pointer_position

    def onMouseRRelease(self,event):
        if self.line_temp_sor_id is not None:
            if self.pointer_focus[0] ==1 and self.pointer_focus[1] != self.line_temp_sor_id and \
            self.adjoin_graph[self.line_temp_sor_id].get(self.pointer_focus[1],None) is None:       #当pointer focus是新节点时确定创建线
                self.lines[self.pointer_selected[1]].source = self.nodes[self.line_temp_sor_id]
                self.lines[self.pointer_selected[1]].target = self.nodes[self.pointer_focus[1]]
                self.adjoin_graph[self.line_temp_sor_id][self.pointer_focus[1]]=self.lines[self.line_counts].weight
                self.lines[self.pointer_selected[1]].updateVector()
            else:              #创建失败，取消preview line
                del self.lines[self.line_counts]
                self.line_counts-=1
                if self.adjoin_graph[self.line_temp_sor_id] == {}:      
                    del self.adjoin_graph[self.line_temp_sor_id]
            self.makePointerSelectedNone()
            self.line_temp_sor_id=None      #退出线创建模式

            

            


    #end{Events}

    def update(self):
        """
        运行逻辑
        """
        if self.scene_mode=='for limbs':
            if self.test_limb_mode.mode == 1:
                #self.makeTestLimbMoveTo(self.pointer_position)         #[优化]：不走函数栈
                self.test_limb.iterate(self.S,self.pointer_position)

            elif self.test_limb_mode.mode == 2:
                #self.makeTestLimbMoveInSOSTo(self.pointer_position)    #[优化]:同上
                self.sos.iterate(self.pointer_position,self.delta_time)
                self.test_limb.iterate(self.S,self.sos.prp)

        if self.scene_mode.mode==1:
            self.detectPointerFocus()


    #begin{updates}

    def makeTestLimbMoveTo(self,destination):
        self.test_limb.iterate(self.S,destination)

    def makeTestLimbMoveInSOSTo(self,destination):
        self.sos.iterate(destination,self.delta_time)
        self.test_limb.iterate(self.S,self.sos.prp)

    def makeNewNode(self,p:Vector):
        self.node_counts += 1
        self.nodes[self.node_counts]= Node(p=p,r=10)

    def makeNewLine(self,sor:Node,tar:Node,heading:bool=True):
        self.line_counts +=1
        self.lines[self.line_counts]= Line(sor,tar,heading)

    def makePointerSelectedNone(self):
        self.pointer_selected[0].mode=0
        self.pointer_selected[1]=None

    def makeRelativeMove(self,object:Vector,pointer:Vector):
        dx=object.x-pointer.x
        dy=object.y-pointer.y
        self.temp_delta_for_move=Vector(dx,dy)

    def detectPointerFocus(self):
        self.pointer_focus[0].mode=3
        self.pointer_focus[1]=None
        if self.nodes:                              #节点
            for id,node in self.nodes.items():
                if node.state==2:                   #跳过被选中的节点
                    continue
                node.low()   
                dx=self.pointer_position.x-node.position.x
                dy=self.pointer_position.y-node.position.y
                r=1.5*node.r
                if abs(dx+dy)<= r and abs(dx-dy)<= r:      #[优化]曼哈顿距离
                    rsensitive=node.r+self.pointer_radius
                    if dx*dx+dy*dy<rsensitive*rsensitive:   #[优化]不开根
                        node.wait()
                        self.pointer_focus[0].mode=1
                        self.pointer_focus[1]=id
                        break

            if self.pointer_focus[0].mode != 1 and self.lines:            #line
                for id,line in self.lines.items():
                    if line.state == 2:
                        continue
                    line.low()
                    if line.source.position<self.pointer_position<line.target.position or line.source.position>self.pointer_position>line.target.position:
                        sp=line.source.position-self.pointer_position
                        lst=abs(line.vector)
                        if abs((sp)*line.vector.verticle())<=lst*line.width*2:
                            if line.source.r*lst<sp*line.vector<(lst-line.source.r)*lst:
                                line.wait()
                                self.pointer_focus[0].mode=2
                                self.pointer_focus[1]=id
                                break



    #end{updates}

    def render(self):
        """
        画面渲染
        """
        width = self.canva.winfo_width() 
        height = self.canva.winfo_height() 
        #获取当前画布大小
        self.canva.delete('all')
        

        if self.info_mode.mode == 1:
            self.showAcrossLine(width,height)
            self.showInfo()

        if self.scene_mode.mode==0:
            self.showTestLimb()
        elif self.scene_mode.mode==1:
            self.showLines()
            self.showNodes()

        self.showMouse()

    #begin{renders}

    def showInfo(self):
        """绘制F3菜单"""
        info=''

        self.canva.create_text(
            10,10,
            text=f'FPS={self.fps}, Mode={self.test_limb_mode}',
            fill='white',font=('Arial',12),anchor=tk.NW
            )
        #显示帧率,模式

        self.canva.create_text(
            10,35,
            text=f'鼠标位置={self.pointer_position}',
            fill='yellow',font=('Arial',12),anchor=tk.NW
            )
        #显示指针位置
        

        if self.scene_mode==0:  #test limb info
            self.canva.create_text(
                10,60,
                text=f'{self.test_limb_mode}',
                fill='gray',font=('Arial',12),anchor=tk.NW
                )
            if self.test_limb_mode==2:
                self.canva.create_text(
                    20,78,
                    text=f'coefficients:\nN={self.test_limb.N};\nf={self.sos.f},\nζ={self.sos.s},\nr={self.sos.r}',
                    fill='white',font=('Arial',12),anchor=tk.NW
                    )
                #config info

        elif self.scene_mode==1:    #nodes scene info
            self.canva.create_text(
                10,60,
                text=f'pointer focus:{self.pointer_focus[0]},{self.pointer_focus[1]}\npointer selected:{self.pointer_selected[0]},{self.pointer_selected[1]}',
                fill='white',font=('Arial',12),anchor=tk.NW
                )
            if self.adjoin_graph_mode==1:   #show adjoin graph with weights
                adjoin_graph_str='{'
                for sor,tars in self.adjoin_graph.items():
                    adjoin_graph_str+='\n    '+str(sor)+':'+str(tars)
                self.canva.create_text(
                10,100,
                text=f'adjoin graph:\n {adjoin_graph_str}'+'\n }',
                fill='white',font=('Arial',12),anchor=tk.NW
                )
            
    def showAcrossLine(self,width,height):
        """绘制中心十字线（调试用）"""
        self.canva.create_line(
            width//2,0,
            width//2,height,
            fill='#fbfbfb',
            dash=(4,4)          #dash虚线
        )
        self.canva.create_line(
            0,height//2,
            width,height//2,
            fill='#fbfbfb',
            dash=(4,4)
        )
        
    def showMouse(self):
        """绘制鼠标"""
        self.canva.create_oval(
            self.pointer_position.x-self.pointer_radius,self.pointer_position.y-self.pointer_radius,
            self.pointer_position.x+self.pointer_radius,self.pointer_position.y+self.pointer_radius,
            outline='lightblue',width=2
            )
        
    def showTestLimb(self):
        """渲染test_limb"""
        for i in range(self.test_limb.N):       #绘制test_limb的连接线
            self.canva.create_line(
                self.test_limb.joints[i].x,self.test_limb.joints[i].y,
                self.test_limb.joints[i+1].x,self.test_limb.joints[i+1].y,
                fill='white',width=2
                )
        for i in range(self.test_limb.N+1):     #绘制test_limb的节点
            r = self.test_limb.joints_size_ratio*(1.5**(i-self.test_limb.N-1)+0.4)
            self.canva.create_oval(
                self.test_limb.joints[i].x-r,self.test_limb.joints[i].y-r,
                self.test_limb.joints[i].x+r,self.test_limb.joints[i].y+r,
                fill='',outline='white',width=3
                )
    
    def showNodes(self):
        if self.nodes:
            for node in self.nodes.values():
                x,y,r,d=node.position.x,node.position.y,node.r,self.node_high_pic[1]
                if node.state == 1:        #等待姿态
                    self.canva.create_oval(
                    x-r,y-r,
                    x+r,y+r,
                    fill="",outline="#5f5f69",width=8
                    )
                elif node.state == 2:      #高姿态
                    temp=self.node_high_pic[0]+r
                    self.canva.create_line(
                        x+temp,y,
                        x+temp+d,y,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x-temp,y,
                        x-temp-d,y,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x,y+temp,
                        x,y+temp+d,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x,y-temp,
                        x,y-temp-d,
                        fill='white',width=3
                    )

                #默认：低姿态
                self.canva.create_oval(
                    x-r,y-r,
                    x+r,y+r,
                    fill='',outline='white',width=3
                )
                if node.light==1:       #点亮
                    '''
                    tr=r*0.6
                    self.canva.create_oval(
                        x-tr,y-tr,
                        x+tr,y+tr,
                        fill="#3392FF"
                    )
                    '''
                    temp=d//2
                    self.canva.create_line(
                        x+r+temp,y,
                        x+r-temp,y,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x-r+temp,y,
                        x-r-temp,y,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x,y+r+temp,
                        x,y+r-temp,
                        fill='white',width=3
                    )
                    self.canva.create_line(
                        x,y-r+temp,
                        x,y-r-temp,
                        fill='white',width=3
                    )
                    
    def showLines(self):
        if self.lines:
            for line in self.lines.values():        #从节点边缘开始画线
                d=line.target.position-line.source.position
                t=abs(d)
                if t:
                    S=line.source.position+d*(line.source.r/t)
                    T=line.target.position-d*(line.target.r/t)
                    if line.state == 1:     #等待姿态
                        self.canva.create_line(
                            S.x,S.y,
                            T.x,T.y,
                            fill="#5f5f69",width=line.width*3,arrow=tk.LAST,dash=6
                            )

                self.canva.create_line(
                    S.x,S.y,
                    T.x,T.y,
                    fill='white',width=line.width,arrow=tk.LAST
                    )

    #end{renders}



#main
if __name__ == "__main__":
    a=DisciplineAPP()
    a.run()

    




