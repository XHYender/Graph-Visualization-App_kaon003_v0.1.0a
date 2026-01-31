#coding=utf-8
"""
Idea Visualization
author:曾久丁   20251021183
version:0.1a
Codes Manners:
。注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；注释说人话；
。变量名用蛇形命名法(frame_per_second);
。函数名用驼峰命名法(saveDataAsFormatJSON);
。类名用帕斯卡命名法(Mode);
。全局变量、常量全大写;
。非局部变量请用带有完整意义的英文词组或拼音(english_var_name,pinyintailowlegaodexiangxiaoxueshen);
。变量列表请在确保可读性的同时适当换行;
。在进行状态机行为时一定不要用反判断，防止后续添加新状态时报错;
。记号[优化]代表我在用我显得有点可笑的知识在做优化;
"""

#from logging import info
import tkinter as tk
import time as t
import json as j


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
    def __init__(self,p:Vector=Vector(),text:str='Text',r=15,id:int=0,light=None,title:str=None):
        super().__init__()
        self.position = p
        self.r=r
        self.id=id
        self.text=text
        self.light=Mode()
        if title is None:self.title='Node:'+str(id)
        else:self.title=title

        if light is not None:
            self.light.mode=light

class Line(TriStates):
    def __init__(self,source:Node,target:Node,heading:bool=True,weight=1,width=3,id:int=0):
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
        self.id=id
        self.width=width
        self.vector=source.position-target.position     #TS

    def flip(self):
        """起点终点翻转"""
        self.source,self.target = self.target,self.source

    def updateVector(self):
        self.vector=self.source.position-self.target.position
        
class Textblank(TriStates):
    def __init__(self,text:str='Default Text',anchor:Vector=Vector(),hide:bool=False,node_id:int=-1,rod=0,bbox=None,color:str='white',font=('黑体',16)):
        super().__init__()
        self.text=text
        self.anchor=anchor
        self.font=font
        self.color=color
        self.hide=hide
        self.node_id=node_id    #node_id==-1说明该文本框不依赖某node
        self.rod=rod            #杆长
        self.bbox=bbox     #包围盒坐标：左上，右下

class Limb:
    """Forward And Back Reaching Inverse Kinematics"""
    def __init__(self,S=None,N=2,fixed=True,joints_size_ratio=10,limbs_lenth_ratio=None,delta = 1,lenths:list=None,joints:list=None,iterate_num:int=5):
        
        self.N = N
        self.fixed = fixed    #根节点是否固定
        self.delta = delta      #末端可接受误差
        self.iterate_num=iterate_num

        if S is not None:
            self.S = S  #根节点
        if limbs_lenth_ratio is not None:
            self.limbs_lenth_ratio = limbs_lenth_ratio
        if joints_size_ratio is not None:
            self.joints_size_ratio = joints_size_ratio
        #渲染相关

        if lenths is None and limbs_lenth_ratio is not None:
            self.lenths = [self.limbs_lenth_ratio*(1+2**(-1-i)) for i in range(N)]
            self.lenths.reverse()
        else:
            self.lenths=lenths

        if joints is None and self.lenths is not None:
            self.joints = [S+Vector(s,0) for s in [ sum(self.lenths[0:i:]) for i in range(N+1) ] ]
        else:
            self.joints=joints

    def fabrik(self,S:Vector,T:Vector):
        self.joints[-1] = T
        for i in range(self.N-1,-1,-1):
            v = self.joints[i+1]-self.joints[i]
            l=abs(v)
            if l!=0: self.joints[i] += v*(1-self.lenths[i]/l)
            else:self.joints[i]+=Vector(self.lenths[i],0)
        #forward reaching

        if self.fixed:
            self.joints[0] = S
            for i in range(self.N):
                v = self.joints[i]-self.joints[i+1]
                l=abs(v)
                if l!=0:self.joints[i+1] += v*(1-self.lenths[i]/l)
                else:self.joints[i+1]+=Vector(self.lenths[i],0)
        #back inverse

    def iterate(self,S:Vector,T:Vector):
        for _ in range(self.iterate_num):  #5次迭代上限防止找不到解决方案（目标点在可触范围之外导致的无限迭代）
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

class Interpolater:
    '''插值器  记得在外部调用iterXXX之前通过检测属性end来控制插值动画的启闭'''
    def __init__(self,timelimit):
        self.source=Vector()
        self.target=Vector()
        self.timelimit=timelimit    #插值时长
        self.time_integral=0        #累计时长
        self.theta=0                #插值系数
        self.end=False

    def timeIntegral(self,dt):
        self.time_integral+=dt
        return (self.time_integral/self.timelimit)

    def start(self,sor:Vector,tar:Vector,timelimit=None):
        self.source=sor
        self.target=tar
        self.time_integral=0
        self.end=False
        if timelimit is not None: self.timelimit=timelimit

    def iterOneDirection(self):
        if self.time_integral>=self.timelimit:
            self.end=True
            return self.target
        else:
            return self.source+(self.target-self.source)*self.theta

    def iterLinear(self,dt):
        '''线性插值:  y=x '''
        self.theta=self.timeIntegral(dt)
        return self.iterOneDirection()

    def iterSquare(self,dt):
        '''平方插值:  y=2 x^(2)(0≤x<0.5) +(1-2(x-1)^(2))(0.5≤x≤1)'''
        temp=self.timeIntegral(dt)

        if temp<0.5:    self.theta=2*(temp**2)
        else:           self.theta=1-2*((temp-1)**2)

        return self.iterOneDirection()

    def iterCubic(self,dt):
        '''立方插值:  y=4 x^(3)(0≤x<0.5) +(1+4(x-1)^(3))(0.5≤x≤1)'''
        temp=self.timeIntegral(dt)

        if temp<0.5:    self.theta=4*(temp**3)
        else:           self.theta =1+4*((temp-1)**3)

        return self.iterOneDirection()

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
        self.createSubTextWindow()
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
    
    def createSubTextWindow(self):
        self.sub_window_for_text=tk.Toplevel(self.root)
        self.sub_window_for_text.withdraw()

        self.sub_window_for_text.minsize(200,160)
        self.sub_window_for_text.title('Text Edit')
        self.sub_window_for_text.iconbitmap('assets\ebook_writable.ico')
        self.sub_window_for_text.attributes('-topmost', True)   #置顶

        self.sub_window_for_text.config(bg="#262643")   #1a1a2e  背景色

        self.sub_window_text_title=tk.Entry(self.sub_window_for_text,
                                 bg="#272728",fg="#FFFFFF",
                                 insertbackground="#FFFFFF",
                                 selectbackground="#93B9CA",
                                 selectforeground="#2E3030",
                                 font=('黑体',20)
                                 )

        self.sub_window_text_blank=tk.Text(self.sub_window_for_text, wrap=tk.WORD, 
                                  bg="#272728",fg="#ffffff",        #5EC8E3
                                  insertbackground="#FFFFFF",
                                  selectbackground="#93B9CA",
                                  selectforeground="#2E3030",
                                  font=('黑体',12),undo=True)
        
        self.sub_window_text_title.pack(fill=tk.BOTH,expand=True,padx=15,pady=10)
        self.sub_window_text_blank.pack(fill=tk.BOTH,expand=True,padx=15)

    def bindEvents(self):
        """输入绑定事件(抽象方法)"""
        #self.canva.bind('<input_event>',triggerFunction)
        pass

    def calculateFPS(self,current_time):
        """计算帧率"""
        self.frame_count += 1
        if current_time - self.fps_timer >= 1:     #每秒更新FPS
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

        if self.delta_time >= self.frame_time:      #帧内刷新
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

class Aplication(Framework):

    def initModes(self):
        """初始化mode们"""
        self.test_limb_mode = Mode(['Fixed','Instant','SOS'])
        self.info_mode = Mode()
        self.adjoin_graph_mode=Mode(['Off','ids','weights'])
        self.scene_mode = Mode(['for limbs','for nodes'],1)
        self.focus_player_mode=Mode()
        self.text_mode=Mode()
        self.nodes_mode=Mode(['Fixed','Physics'])

    def __init__(self,title:str='附魔台',width:int =1080,height:int=720,save_id:int=0):
        """:param save_id:要进行读写的存档编号。默认值0通常情况下是演示存档"""
        super().__init__(title,width,height)

        self.initModes()

        self.pointer_position = Vector()
        self.pointer_radius=5
        self.pointer_focus=[Mode(['None','Node','Line','Canva','Textblank']),None]      #[类，id]
        self.pointer_selected=[Mode(['None','Node','Line','Canva','Textblank']),None]   #[类，id]
        #初始化指针

        self.S=Vector(300,300)                      #test limb的末节点生成点
        self.test_limb = Limb(S=self.S,N=5,fixed=False,joints_size_ratio=8,limbs_lenth_ratio=20)
        #初始化test_limb

        self.sos = SOS(self.S,1,0.9,0.8)    
        #初始化二阶系统(test limb)
    
        self.limbs=[]
        #初始化limb实体模拟的实体槽 TODO

        self.temp_delta_for_move=Vector()   #用于相对固定的移动的临时量
        self.temp_positions_for_drag={}     #用于中键拖拽所有节点
        self.temp_positions_for_text_drag={}#用于中键拖拽所有文本框
        self.temp_focus_target=Vector()
        self.temp_position_for_textblank_drag=None
        self.temp_node_id_for_text_or_focus=None       #打开的text的Node的id
        self.temp_timer_for_ignite=None                 #用于长按点亮节点的计时器
        #初始化临时量

        self.focus_center=Vector()         #[bug]目前是在makeCameraFocusOn方法中提前实现。
        self.focus_mover=Interpolater(0.6)
        #初始化focus动画

        self.nodes={}
        self.node_counts=0                  #节点id计数用数据
        self.node_high_pic=(5,10)           #节点高姿态绘制用数据（距离，长度）
        #初始化节点集

        self.lines={}
        self.line_counts=0
        self.line_temp_sor_id=None          #新线起点，用于创建线（可视为非None时是创建线模式）
        #初始化线集

        self.textblanks={}                  #id对应node的id
        self.textblank_rods={}              #fabrik实现rod
        self.rod_lenth=30
        #初始化文本框

        self.adjoin_graph={}
        #初始化邻接表(无权重){起点:{终点:线id}}

        self.adjoin_graph_with_weights={}
        #初始化邻接表(带正权重){起点:{终点:权重}}

        self.save_id=save_id
        #初始化存档选择id

    def bindEvents(self):
        """绑定事件处理"""

        self.root.bind('<Configure>', self.onResize)    #窗口大小改变事件

        self.root.bind('<KeyPress>', self.onKeyPress)   #键盘按键

        self.root.bind('<KeyPress-Escape>', self.onKeyPressEsc) 
        self.root.bind('<KeyPress-space>', self.onKeyPressSpace)
        self.root.bind('<KeyPress-F3>', self.onKeyPressF3)
        self.root.bind('<KeyPress-F2>', self.onKeyPressF2)

        self.root.bind('<KeyPress-s>', self.onKeyPressS)
        self.root.bind('<KeyPress-S>', self.onKeyPressS)
        self.root.bind('<KeyPress-c>', self.onKeyPressC)
        self.root.bind('<KeyPress-C>', self.onKeyPressC)
        self.root.bind('<KeyPress-d>', self.onKeyPressD)
        self.root.bind('<KeyPress-D>', self.onKeyPressD)
        self.root.bind('<KeyPress-m>', self.onKeyPressM)
        self.root.bind('<KeyPress-M>', self.onKeyPressM)
        self.root.bind('<KeyPress-t>', self.onKeyPressT)
        self.root.bind('<KeyPress-T>', self.onKeyPressT)
        self.root.bind('<KeyPress-w>', self.onKeyPressW)
        self.root.bind('<KeyPress-W>', self.onKeyPressW)

        self.root.bind('<Control-KeyPress-r>', self.onKeyPressCtrlR)
        self.root.bind('<Control-KeyPress-R>', self.onKeyPressCtrlR)
        self.root.bind('<Control-KeyPress-s>', self.onKeyPressCtrlS)
        self.root.bind('<Control-KeyPress-S>', self.onKeyPressCtrlS)

        self.canva.bind('<Motion>',self.onMouseMove)    #鼠标移动

        self.canva.bind('<Button-1>', self.onMouseLClick)               #左键按下
        self.canva.bind('<B1-Motion>', self.onMouseLDrag)               #左键拖动
        self.canva.bind('<ButtonRelease-1>', self.onMouseLRelease)      #左键释放
        self.canva.bind("<Double-Button-1>", self.onMouseLDoubleClick)  #左键双击

        self.canva.bind('<Button-3>',self.onMouseRClick)                #右键
        self.canva.bind('<B3-Motion>', self.onMouseRDrag)
        self.canva.bind('<ButtonRelease-3>', self.onMouseRRelease)

        self.canva.bind('<Button-2>',self.onMouseMClick)                #中键
        self.canva.bind('<B2-Motion>', self.onMouseMDrag)
        self.canva.bind('<ButtonRelease-2>', self.onMouseMRelease)



        #子窗口：sub window for text
        self.sub_window_for_text.protocol("WM_DELETE_WINDOW", self.onSubWindowForTextClose)#修改关闭协议
        self.sub_window_for_text.bind('<Control-KeyPress-t>', self.onKeyPressT)
        self.sub_window_for_text.bind('<Control-KeyPress-T>', self.onKeyPressT)             #以主窗口为主所以还是onKeyPressT
        self.sub_window_for_text.bind('<KeyPress-Escape>',self.onSubWindowForTextClose)

    if 1:   #{EventsFunctions}

        def onMouseMove(self,event):
            """鼠标移动事件"""
            self.pointer_position = Vector(event.x,event.y) #event.x,event.y

        def onResize(self,event):
            """窗口大小改变时的改动"""
            if event.widget == self.root:
                self.window_width = self.canva.winfo_width() 
                self.window_height = self.canva.winfo_height() 
                self.focus_center=Vector(self.window_width//2,self.window_height//2)
                #获取当前画布大小
                self.render()
                
        def onKeyPress(self,event):
            print(f"Key: {event.keycode}, Sym: {event.keysym}, Char: {event.char}")

        def onKeyPressF3(self,event):
            self.info_mode.switch()

        def onKeyPressF2(self,event):
            self.onKeyPressT()
                
        def onKeyPressEsc(self,event):
            self.close()

        def onKeyPressSpace(self,event):
            if self.scene_mode == 0:
                self.test_limb_mode.switch()

                if self.test_limb_mode ==2:     #让sos继承上个mode结束时的位置
                    self.sos.prp =self.sos.p=self.sos.pp= self.pointer_position
                    self.sos.prs = Vector()
                    
            if self.scene_mode == 1:
                self.nodes_mode.switch()
                self.inheritTextblankRod()

        def onKeyPressS(self,event):
            if self.text_mode==1:                    #关闭子窗口
                self.swicthTextWindow()
            self.scene_mode.switch()

        def onKeyPressC(self,event):
            if self.scene_mode == 1:
                self.makeNewNode(self.pointer_position)

        def onKeyPressD(self,event):
            if self.scene_mode == 1:
                if self.pointer_focus[0] in (1,2,4):
                    selected_id=self.pointer_focus[1]
                    if self.pointer_focus[0] == 1:      #Node
                        self.delNode(selected_id)
                    if self.pointer_focus[0] == 2:      #Line
                        self.delLine(selected_id)
                    if self.pointer_focus[0]==4:        #文本框
                        self.textblanks[self.pointer_focus[1]].hide=True

        def onKeyPressW(self,event):
            if self.scene_mode == 1:
                self.renewAdjoinGraphWithWeight()

        def onKeyPressM(self,event):
            if self.scene_mode == 1:
                self.adjoin_graph_mode.switch()

        def onKeyPressT(self,event=None):
            if self.scene_mode == 1:
                if self.focus_player_mode == 1:    #聚焦过程中禁用编写行为
                    return 0

                if self.pointer_focus[0] in (1,4):
                    self.swicthTextWindow(self.pointer_focus[1])
                else:
                    self.swicthTextWindow()

        def onKeyPressCtrlR(self,event):
            if self.scene_mode == 1:
                self.readDatas(self.save_id)

        def onKeyPressCtrlS(self,event):
            if self.scene_mode == 1:
                self.saveDatas(self.save_id)

        def onMouseLClick(self,event):
            if self.scene_mode == 1:
                if self.focus_player_mode == 1:    #聚焦过程中禁用鼠标行为
                    return 0
                
                if self.pointer_focus[0]==1:            #Node
                    self.nodes[self.pointer_focus[1]].high()
                    self.pointer_selected[0].mode=1
                    self.pointer_selected[1]=self.pointer_focus[1]
                    self.makeRelativeMove(self.nodes[self.pointer_selected[1]].position,self.pointer_position)

                    self.temp_timer_for_ignite=-t.time()#开始计时判断是否需要点亮

                if self.pointer_focus[0]==2:            #line
                    self.lines[self.pointer_focus[1]].high()
                    self.pointer_selected[0].mode=2
                    self.pointer_selected[1]=self.pointer_focus[1]
                    self.makeRelativeMove(self.lines[self.pointer_selected[1]].target.position,self.pointer_position)

                if self.pointer_focus[0]==4:            #textblank
                    self.textblanks[self.pointer_focus[1]].high()
                    self.pointer_selected[0].mode=4
                    self.pointer_selected[1]=self.pointer_focus[1]
                    self.textblank_rods[self.pointer_selected[1]].joints=self.textblank_rods[self.pointer_selected[1]].joints[::-1]
                    self.textblank_rods[self.pointer_selected[1]].fixed=True
                    self.temp_position_for_textblank_drag=self.textblanks[self.pointer_selected[1]].anchor
                    self.makeRelativeMove(self.temp_position_for_textblank_drag,self.pointer_position)
                    
        def onMouseLDrag(self,event):
            self.onMouseMove(event)
            if self.scene_mode == 1:
                if self.pointer_selected[0]!=0:
                    if self.pointer_selected[0]==1:     #Node
                        self.temp_timer_for_ignite=None     #取消点亮节点
                        d=self.pointer_position+self.temp_delta_for_move
                        if self.textblanks.get(self.pointer_selected[1],False) and (self.nodes_mode==0 or self.textblanks[self.pointer_selected[1]].hide):    #文本框移动
                            self.textblanks[self.pointer_selected[1]].anchor-=self.nodes[self.pointer_selected[1]].position-d
                        self.nodes[self.pointer_selected[1]].position= d   #节点移动
                        
                    if self.pointer_selected[0]==2:     #Line
                        tt,ts=self.lines[self.pointer_selected[1]].target.position,self.lines[self.pointer_selected[1]].source.position
                        idt,ids=self.lines[self.pointer_selected[1]].target.id,self.lines[self.pointer_selected[1]].source.id

                        self.lines[self.pointer_selected[1]].target.position=self.pointer_position+self.temp_delta_for_move     #target移动
                        self.lines[self.pointer_selected[1]].source.position=self.lines[self.pointer_selected[1]].target.position+self.lines[self.pointer_selected[1]].vector      #source移动

                        if self.textblanks.get(idt,False):      #textblank 移动
                            if self.nodes_mode==0 or self.textblanks[idt].hide:
                                self.textblanks[idt].anchor+=self.lines[self.pointer_selected[1]].target.position-tt
                        if self.textblanks.get(ids,False):
                            if self.nodes_mode==0 or self.textblanks[ids].hide:
                                self.textblanks[ids].anchor+=self.lines[self.pointer_selected[1]].source.position-ts

                    if self.pointer_selected[0]==4:     #textblank
                        self.temp_position_for_textblank_drag=self.pointer_position+self.temp_delta_for_move        #文本框移动

        def onMouseLRelease(self,event):
            if self.scene_mode == 1:
                if self.pointer_selected[0]==1:         #Node
                    self.nodes[self.pointer_selected[1]].low()

                    if self.temp_timer_for_ignite is not None:  #长按点亮node部分
                        self.temp_timer_for_ignite+=t.time()
                        if self.temp_timer_for_ignite >=0.5:    #0.5s
                            self.nodes[self.pointer_selected[1]].light.switch()
                            self.temp_timer_for_ignite=None
                            self.makePointerSelectedNone()   #释放pointer selected
                            return

                    for id,line in self.lines.items():          #更新相关线信息
                        if self.nodes[self.pointer_selected[1]] in (line.source,line.target):
                            self.lines[id].updateVector()

                if self.pointer_selected[0]==2:         #Line
                    self.lines[self.pointer_selected[1]].low()
                    for id,line in self.lines.items():          #更新相关线信息
                        if self.lines[self.pointer_selected[1]].source in (line.source,line.target) or \
                        self.lines[self.pointer_selected[1]].target in (line.source,line.target):
                            self.lines[id].updateVector()

                if self.pointer_selected[0]==4:         #textblanks
                    self.textblanks[self.pointer_selected[1]].low()
                    self.textblank_rods[self.pointer_selected[1]].joints=self.textblank_rods[self.pointer_selected[1]].joints[::-1]
                    self.textblank_rods[self.pointer_selected[1]].fixed=False
                    self.temp_position_for_textblank_drag=None
                    
                self.makePointerSelectedNone()   #释放pointer selected

        def onMouseLDoubleClick(self,event):
            if self.scene_mode == 1:
                id=self.pointer_focus[1]
                if self.pointer_focus[0]==1:        #node:打开/关闭文本框(only for title)
                    if self.textblanks.get(id,None) is None:    #初始化
                        self.textblanks[id]=Textblank(node_id=id,rod=self.rod_lenth)
                        self.inheritTextblanksText(id)
                        self.textblanks[id].anchor=Vector(self.textblanks[id].rod+self.nodes[id].r,0)+self.nodes[id].position            #初始化锚杆
                        self.textblank_rods[id]=Limb(joints=[self.textblanks[id].anchor,self.nodes[id].position],N=1,fixed=False,iterate_num=1,lenths=[self.textblanks[id].rod+self.nodes[id].r])
                    elif self.textblanks[id].hide:              #已存在
                        self.textblanks[id].hide=False
                        self.inheritTextblanksText(id)
                        self.textblank_rods[id].joints[0]=self.textblanks[id].anchor
                    else:                                       #隐藏
                        self.textblanks[id].hide=True

                if self.pointer_focus[0]==4:        #文本框
                    self.textblanks[id].hide=True

                if self.pointer_focus[0]==2 and self.lines[id].heading:        #翻转Line
                    sor_id=self.lines[id].source.id  
                    tar_id=self.lines[id].target.id
                    self.adjoinGraphDel(sor_id,tar_id)
                    self.adjoinGraphAdd(tar_id,sor_id,id)#维护邻接表

                    self.lines[id].flip()
                    self.lines[id].updateVector()

        def onMouseRClick(self,event):
            if self.scene_mode == 1:
                if self.focus_player_mode == 1:        #聚焦过程中禁用鼠标行为
                    return 0
                
                if self.pointer_focus[0]==3:    #在Canva上（非Node、Line）创建Node
                    self.makeNewNode(self.pointer_position)

                elif self.pointer_focus[0]==1:  #在Node上创建Line
                    self.line_temp_sor_id=self.pointer_focus[1]
                    self.makeNewLine(Node(p=self.nodes[self.line_temp_sor_id].position,
                        r=self.nodes[self.line_temp_sor_id].r),Node(p=self.pointer_position,r=self.pointer_radius))     #创建preview line
                    self.pointer_selected[0].mode=2
                    self.pointer_selected[1]=self.line_counts
                    if self.adjoin_graph.get(self.line_temp_sor_id,None) is None:   #在邻接表中添加节点
                        self.adjoin_graph[self.line_temp_sor_id] = {}

                elif self.pointer_focus[0]==2:  #切换线的有向无向
                    line_id=self.pointer_focus[1]
                    sor_id,tar_id=self.lines[line_id].source.id,self.lines[line_id].target.id
                    
                    if self.lines[line_id].heading:
                        self.lines[line_id].heading=False
                        #self.adjoinGraphDel(sor_id,tar_id)
                    else:
                        self.lines[line_id].heading=True
                        #self.adjoinGraphAdd(sor_id,tar_id,line_id)

        def onMouseRDrag(self,event):
            self.onMouseMove(event)
            if self.scene_mode == 1:
                if self.line_temp_sor_id is not None:       #创建线过程中箭头指向pointer
                    self.lines[self.line_counts].target.position=self.pointer_position

        def onMouseRRelease(self,event):
            if self.scene_mode == 1:
                if self.line_temp_sor_id is not None:       #进入线创建模式
                    if self.pointer_focus[0] ==1 and self.pointer_focus[1] != self.line_temp_sor_id and \
                    self.adjoin_graph[self.line_temp_sor_id].get(self.pointer_focus[1],None) is None:       #当pointer focus是新节点时确定创建线
                        self.lines[self.pointer_selected[1]].source = self.nodes[self.line_temp_sor_id]
                        self.lines[self.pointer_selected[1]].target = self.nodes[self.pointer_focus[1]]
                        self.adjoin_graph[self.line_temp_sor_id][self.pointer_focus[1]]=self.lines[self.line_counts].id
                        self.lines[self.pointer_selected[1]].updateVector()
                    else:              #创建失败，取消preview line
                        del self.lines[self.line_counts]
                        self.line_counts-=1
                        if self.adjoin_graph[self.line_temp_sor_id] == {}:      
                            del self.adjoin_graph[self.line_temp_sor_id]
                    self.makePointerSelectedNone()
                    self.line_temp_sor_id=None      #退出线创建模式

        def onMouseMClick(self,event):
            if self.scene_mode == 1:
                if self.focus_player_mode == 1 or self.text_mode==1:        #聚焦、编辑过程中禁用行为
                    return 0
                
                if self.pointer_focus[0]==3 and self.focus_player_mode == 0:          #Canva
                    self.pointer_selected[0].mode=3
                    self.pointer_selected[1]=self.pointer_position

                    for id,node in self.nodes.items():
                        self.temp_positions_for_drag[id]=node.position
                    for id,textblank in self.textblanks.items():
                        self.temp_positions_for_text_drag[id]=textblank.anchor

                elif self.pointer_focus[0]==2:        #Line
                    if self.lines[self.pointer_focus[1]].heading:
                        self.makeCameraFocusOn(self.lines[self.pointer_focus[1]].target.position,self.lines[self.pointer_focus[1]].target.id)

                elif self.pointer_focus[0]==1:        #Node
                    self.makeCameraFocusOn(self.nodes[self.pointer_focus[1]].position,self.nodes[self.pointer_focus[1]].id)

        def onMouseMDrag(self,event):
            self.onMouseMove(event)
            if self.scene_mode == 1:
                if self.pointer_selected[0]==3:   #Canva
                    self.makeAllThingsMove(self.pointer_selected[1],self.pointer_position)

        def onMouseMRelease(self,event):
            if self.scene_mode == 1:
                self.makePointerSelectedNone()   #释放pointer selected

        def onSubWindowForTextClose(self,event=None):
            self.swicthTextWindow()

    def update(self):
        """
        运行逻辑
        """
        if self.scene_mode.mode==0:             #'for limbs'
            if self.test_limb_mode.mode == 1:
                #self.makeTestLimbMoveTo(self.pointer_position)         #[优化]：不走函数栈
                self.test_limb.iterate(self.S,self.pointer_position)
                
            elif self.test_limb_mode.mode == 2:
                #self.makeTestLimbMoveInSOSTo(self.pointer_position)    #[优化]:同上
                self.sos.iterate(self.pointer_position,self.delta_time)
                self.test_limb.iterate(self.S,self.sos.prp)

        if self.scene_mode.mode==1:             #'for nodes
            self.detectPointerFocus()

            self.makeTextblankRodMove()

            if self.focus_player_mode == 1:    #聚焦动画
                #interpolater
                if not self.focus_mover.end:
                    self.makeAllThingsMove(self.temp_focus_target,self.focus_mover.iterCubic(self.delta_time))
                else:
                    self.focus_player_mode.mode =0
                    self.temp_node_id_for_text_or_focus=None

    if 1:   #{updatesFunctions}

        def makeTestLimbMoveTo(self,destination):
            self.test_limb.iterate(self.S,destination)

        def makeTestLimbMoveInSOSTo(self,destination):
            self.sos.iterate(destination,self.delta_time)
            self.test_limb.iterate(self.S,self.sos.prp)

        def makeNewNode(self,p:Vector):
            self.node_counts += 1
            self.nodes[self.node_counts]= Node(p=p,r=10,id=self.node_counts)

        def makeNewLine(self,sor:Node,tar:Node,heading:bool=True):
            self.line_counts +=1
            self.lines[self.line_counts]= Line(sor,tar,heading,id=self.line_counts)

        def makePointerSelectedNone(self):
            self.pointer_selected[0].mode=0
            self.pointer_selected[1]=None

        def makeRelativeMove(self,object:Vector,pointer:Vector):
            dx=object.x-pointer.x
            dy=object.y-pointer.y
            self.temp_delta_for_move=Vector(dx,dy)

        def makeAllThingsMove(self,source:Vector,target:Vector):
            shift=target-source
            if self.nodes:
                for id in self.nodes.keys():
                    self.nodes[id].position = self.temp_positions_for_drag[id]+shift
                for id in self.textblanks.keys():
                    self.textblanks[id].anchor=self.temp_positions_for_text_drag[id]+shift
                    self.textblank_rods[id].joints[0]=self.textblanks[id].anchor
                    self.textblank_rods[id].joints[1]=self.nodes[id].position
            
        def makeTextblankRodMove(self):
            if self.focus_player_mode == 0 and self.textblank_rods:
                if self.pointer_selected[0]==4:
                    self.textblank_rods[self.pointer_selected[1]].iterate(self.nodes[self.pointer_selected[1]].position,self.temp_position_for_textblank_drag)
                    self.textblanks[self.pointer_selected[1]].anchor=self.textblank_rods[self.pointer_selected[1]].joints[1]

                elif self.pointer_selected[0] != 3 and self.nodes_mode==1:
                    for id,rod in self.textblank_rods.items():
                        if self.textblanks[id].hide:
                            continue
                        rod.iterate(Vector(),self.nodes[id].position)
                        self.textblanks[id].anchor=rod.joints[0]
                
        def makeCameraFocusOn(self,target:Vector,node_id:int):
            self.setFocusCenter()
            self.temp_focus_target=target
            for id,node in self.nodes.items():
                self.temp_positions_for_drag[id]=node.position
            for id,textblank in self.textblanks.items():
                self.temp_positions_for_text_drag[id]=textblank.anchor

            self.focus_mover.start(sor=target,tar=self.focus_center)

            self.focus_player_mode.switch()
            self.temp_node_id_for_text_or_focus=node_id

        def swicthTextWindow(self,node_id:int=None):
            if self.text_mode==0 and node_id is not None:   #打开子窗口
                self.text_mode.switch()
                try:
                    width,height=500,300
                    x=self.root.winfo_x()+(self.root.winfo_width()-width)//2
                    y=self.root.winfo_y()+(self.root.winfo_height()-height)//2
                    self.sub_window_for_text.geometry(f'{width}x{height}+{x}+{y}')  #初始化窗口信息

                    self.temp_node_id_for_text_or_focus=node_id
                    self.sub_window_text_title.insert(0,self.nodes[self.temp_node_id_for_text_or_focus].title)
                    self.sub_window_text_blank.insert('1.0',self.nodes[self.temp_node_id_for_text_or_focus].text)

                    self.sub_window_for_text.deiconify()
                except:self.text_mode.switch()
            elif self.text_mode==1:                         #关闭子窗口
                self.text_mode.switch()
                try:
                    self.nodes[self.temp_node_id_for_text_or_focus].title=self.sub_window_text_title.get()
                    self.nodes[self.temp_node_id_for_text_or_focus].text=self.sub_window_text_blank.get('1.0','end')
                    if self.textblanks.get(self.temp_node_id_for_text_or_focus,False):
                        self.inheritTextblanksText(self.temp_node_id_for_text_or_focus)

                    self.sub_window_text_blank.delete('1.0','end')
                    self.sub_window_text_title.delete(0,tk.END)
                    self.temp_node_id_for_text_or_focus=None        #释放临时量
                    self.sub_window_for_text.withdraw()
                except:self.text_mode.switch()
                
        def delNode(self,del_node_id:int):
            if del_node_id == self.node_counts:     #维护node counts
                self.node_counts-=1
            del self.nodes[del_node_id]
            if self.textblanks.get(del_node_id,None) is not None:       #删除相联文本框
                del self.textblanks[del_node_id]
                del self.textblank_rods[del_node_id]

            if self.lines:                          #删除相关线，同时维护邻接表
                if self.adjoin_graph.get(del_node_id,False):
                    temp_ids_wait_for_del=[line_id for line_id in self.adjoin_graph[del_node_id].values()]
                    for line_id in temp_ids_wait_for_del:
                        self.delLine(line_id)

                temp_nodes_id_wait_for_check=[lined_node_id for lined_node_id in self.adjoin_graph.keys()]
                for lined_node_id in temp_nodes_id_wait_for_check:
                    if self.adjoin_graph[lined_node_id].get(del_node_id,False):
                        self.delLine(self.adjoin_graph[lined_node_id][del_node_id])

        def delLine(self,del_line_id:int):
            if del_line_id==self.line_counts:       #维护line counts
                self.line_counts-=1
            sor,tar=self.lines[del_line_id].source.id,self.lines[del_line_id].target.id
            del self.lines[del_line_id]

            if self.adjoin_graph[sor].get(tar,False):        #维护adjoin graph
                del self.adjoin_graph[sor][tar]
                if not self.adjoin_graph[sor] :
                    del self.adjoin_graph[sor]

        def detectPointerFocus(self):
            self.pointer_focus[0].mode=0
            self.pointer_focus[1]=None
            if self.nodes:                              #节点
                for id,node in self.nodes.items():
                    if node.state==2:                   #跳过被选中的节点
                        continue
                    node.low()   
                    dx=self.pointer_position.x-node.position.x
                    dy=self.pointer_position.y-node.position.y
                    r=1.5*node.r                        #敏感范围：1.5倍半径
                    if abs(dx+dy)<= r and abs(dx-dy)<= r:      #[优化]曼哈顿距离-粗选
                        rsensitive=node.r+self.pointer_radius
                        if dx*dx+dy*dy<rsensitive*rsensitive:   #[优化]不开根
                            self.pointer_focus[0].mode=1
                            self.pointer_focus[1]=id
                            break

                if self.lines and self.pointer_selected[0]==0:            #line
                    p=self.pointer_position
                    for id,line in self.lines.items():
                        if line.state == 2:
                            continue
                        line.low()

                        b=line.width*2       #敏感范围：2倍线宽
                        s,t,vb=line.source.position,line.target.position,Vector(b,b)
                        if s-vb<p<t+vb or s+vb>p>t-vb:  #边界框-粗选
                            sp=s-p
                            lst=abs(line.vector)
                            if abs((sp)*line.vector.verticle())<=lst*b:  
                                if line.source.r*lst<sp*line.vector<(lst-line.source.r)*lst:
                                    self.pointer_focus[0].mode=2
                                    self.pointer_focus[1]=id
                                    break

            if self.textblanks:                         #textblank
                for node_id,textblank in self.textblanks.items():
                    if textblank.state==2 or textblank.bbox is None:
                        continue
                    textblank.low()
                    x,y,u,v=textblank.bbox
                    if Vector(x,y)<=self.pointer_position<=Vector(u,v):
                        self.pointer_focus[0].mode=4
                        self.pointer_focus[1]=node_id
                        break


            if self.pointer_focus[0].mode == 1:             #node
                self.nodes[self.pointer_focus[1]].wait()
            elif self.pointer_focus[0].mode == 2:           #line
                self.lines[self.pointer_focus[1]].wait()
            elif self.pointer_focus[0].mode == 4:           #textblank
                self.textblanks[self.pointer_focus[1]].wait()
            else:                                           #canva
                self.pointer_focus[0].mode=3

        def adjoinGraphAdd(self,sor_id:int,tar_id:int,line_id:int):
            if self.adjoin_graph.get(sor_id,None) is None:
                self.adjoin_graph[sor_id]={}
            self.adjoin_graph[sor_id][tar_id]=line_id

        def adjoinGraphDel(self,sor_id:int,tar_id:int):
            del self.adjoin_graph[sor_id][tar_id]
            if not self.adjoin_graph[sor_id] :
                del self.adjoin_graph[sor_id]

        def inheritTextblanksText(self,node_id:int=-1):
            self.textblanks[node_id].text=self.nodes[node_id].title
            
        def setFocusCenter(self):
            self.focus_center=Vector(self.canva.winfo_width()//2,self.canva.winfo_height()//2)

        def inheritTextblankRod(self):
            for id in self.textblank_rods.keys():
                self.textblank_rods[id].joints[0]=self.textblanks[id].anchor

        def renewAdjoinGraphWithWeight(self):
            self.adjoin_graph_with_weights={ sor:{tar:self.lines[id].weight for tar,id in tars.items() if self.lines[id].heading} for sor,tars in self.adjoin_graph.items() }
            ids_wait_for_del=[]
            for id in self.adjoin_graph_with_weights.keys():
                if not self.adjoin_graph_with_weights[id]:
                    ids_wait_for_del.append(id)
            for id in ids_wait_for_del:
                del self.adjoin_graph_with_weights[id]
            
        def saveDatas(self,file_id:int=0):
            """保存存档for nodes"""
            if self.scene_mode != 1 or self.focus_player_mode !=0: #只能在安全状态下保存读取
                print('save failed!')
                return 0
            save={
                'graph':[[sor,[(tar,id) for tar,id in t.items()]] for sor,t in self.adjoin_graph.items()],        #json的字典的键只能是string，遂做如此处理。如有属性变更请做备份后谨慎改动
                'node_counts':self.node_counts,
                'line_counts':self.line_counts,
                'nodes':[[node.position.x,node.position.y,node.text,node.r,node.light.mode,id,node.title] for id,node in self.nodes.items()],
                'lines':[[line.source.id,line.target.id,line.heading,line.weight,line.width,id] for id,line in self.lines.items()],
                'textblanks':[[tb.text,tb.anchor.x,tb.anchor.y,tb.hide,tb.bbox,tb.rod,tb.color,tb.font,id] for id,tb in self.textblanks.items()]
                }
            with open(f'saves/save{file_id}.json','w') as save_file:
                j.dump(save,save_file)
                print(f'save as ./saves/save{file_id}.json , succeeded!')

        def readDatas(self,file_id:int=0):
            """读取存档for nodes"""
            try:
                with open(f'saves/save{file_id}.json','r') as read_file:
                    if self.scene_mode != 1 or self.focus_player_mode !=0:
                        print('read failed!')
                        return 0
                    reads = j.load(read_file)
                    self.adjoin_graph = {s[0]:{t[0]:t[1] for t in s[1]} for s in reads['graph']}
                    self.node_counts=reads['node_counts']
                    self.line_counts=reads['line_counts']
                    self.nodes = {n[5]:Node(p=Vector(n[0],n[1]),text=n[2],r=n[3],id=n[5],light=n[4],title=n[6]) for n in reads['nodes']}
                    self.lines = {l[5]:Line(source=self.nodes[l[0]],target=self.nodes[l[1]],heading=l[2],weight=l[3],width=l[4],id=l[5]) for l in reads['lines']}
                    for id in self.lines.keys():
                        self.lines[id].updateVector()

                    self.textblanks={ tb[8]:Textblank(text=tb[0],anchor=Vector(tb[1],tb[2]),hide=tb[3],bbox=tb[4],rod=tb[5],color=tb[6],font=tb[7],node_id=tb[8]) for tb in reads['textblanks']  if tb[4] is None }
                    self.textblanks|={tb[8]:Textblank(text=tb[0],anchor=Vector(tb[1],tb[2]),hide=tb[3],bbox=tuple(tb[4]),rod=tb[5],color=tb[6],font=tb[7],node_id=tb[8]) for tb in reads['textblanks'] if tb[4] is not None}

                    for id in self.textblanks.keys():
                        self.textblank_rods[id]=Limb(joints=[self.textblanks[id].anchor,self.nodes[id].position],N=1,fixed=False,iterate_num=1,lenths=[self.textblanks[id].rod+self.nodes[id].r])

                    print(f'read at ./saves/save{file_id}.json , succeeded!')
            except FileNotFoundError:
                print('save not found!')

    def render(self):
        """
        画面渲染
        """
        width = self.canva.winfo_width() 
        height = self.canva.winfo_height() 
        #获取当前画布大小
        self.canva.delete('all')

        if self.scene_mode.mode==0:
            self.showTestLimb()
        elif self.scene_mode.mode==1:
            self.showAcrossLine(width,height)       #不知道为什么好像先画这个可以防止撕裂

            self.showLines()
            self.showNodes()
            self.showTextblanks()
            self.showFocusSign()

            if self.text_mode ==1:
                self.showSubWindowForTextLocation()

        if self.info_mode.mode == 1:
            self.showInfo()

        self.showMouse()

    if 1:   #{rendersFunctions}

        def showInfo(self):
            """绘制F3菜单"""
            if self.scene_mode==0:  #test limb info
                mode=str(self.test_limb_mode)
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
                mode=str(self.nodes_mode)

                self.canva.create_text(
                    10,60,
                    text=f'pointer focus:{self.pointer_focus[0]},{self.pointer_focus[1]}\npointer selected:{self.pointer_selected[0]},{self.pointer_selected[1]}',
                    fill='white',font=('Arial',12),anchor=tk.NW
                    )
                
                if self.adjoin_graph_mode==1:   #show adjoin graph with ids
                    adjoin_graph_str='{'
                    for sor,tars in self.adjoin_graph.items():              #join the graph
                        adjoin_graph_str+='\n    '+str(sor)+':'+str(tars)

                    self.canva.create_text(
                    10,100,
                    text=f'adjoin graph:    (sor:  tar:  line.id)\n {adjoin_graph_str}'+'\n }',
                    fill='white',font=('Arial',12),anchor=tk.NW
                    )

                elif self.adjoin_graph_mode==2:     #show adjoin graph with weights
                    adjoin_graph_str='{'
                    for sor,tars in self.adjoin_graph_with_weights.items():              #join the graph
                        adjoin_graph_str+='\n    '+str(sor)+':'+str(tars)

                    self.canva.create_text(
                    10,100,
                    text=f'adjoin graph:    (sor:  tar:  line.weight)\n {adjoin_graph_str}'+'\n }',
                    fill='white',font=('Arial',12),anchor=tk.NW
                    )
            
            self.canva.create_text(
                10,10,
                text=f'FPS={self.fps}  Mode:'+mode,
                fill='white',font=('Arial',12),anchor=tk.NW
                )
            #显示帧率,模式

            self.canva.create_text(
                10,35,
                text=f'鼠标位置={self.pointer_position}',
                fill='yellow',font=('Arial',12),anchor=tk.NW
                )
            #显示指针位置

        def showAcrossLine(self,width,height):
            """绘制中心十字线（调试用）"""
            if self.info_mode.mode == 1 :
                color='#fbfbfb'
            else:
                color='#1a1a2e'

            self.canva.create_line(
                width//2,0,
                width//2,height,
                fill=color,
                dash=(4,4)          #dash虚线
            )
            self.canva.create_line(
                0,height//2,
                width,height//2,
                fill=color,
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
                    x,y,r=node.position.x,node.position.y,node.r
                    scolor='#5f5f69'
                    if node.state == 1:        #等待姿态
                        self.canva.create_oval(
                        x-r,y-r,
                        x+r,y+r,
                        fill="",outline=scolor,width=8
                        )
                    elif node.state == 2:      #高姿态
                        self.canva.create_oval(
                        x-r,y-r,
                        x+r,y+r,
                        fill="",outline=scolor,width=8
                        )
                        temp=r+self.node_high_pic[1]
                        self.canva.create_line(
                            x+temp,y,
                            x+r,y,
                            fill=scolor,width=3
                        )
                        self.canva.create_line(
                            x-r,y,
                            x-temp,y,
                            fill=scolor,width=3
                        )
                        self.canva.create_line(
                            x,y+temp,
                            x,y+r,
                            fill=scolor,width=3
                        )
                        self.canva.create_line(
                            x,y-r,
                            x,y-temp,
                            fill=scolor,width=3
                        )
                    
                    if node.light==1:       #点亮
                        rr=r-2
                        self.canva.create_oval(
                            x-rr,y-rr,
                            x+rr,y+rr,
                            fill="#B7CEFF",outline="#84A9FF",width=2
                        )

                    #默认：低姿态
                    self.canva.create_oval(
                        x-r,y-r,
                        x+r,y+r,
                        fill='',outline='white',width=3
                    )
                
        def showFocusSign(self):
            if self.temp_node_id_for_text_or_focus is not None:     #聚焦/编辑
                    d=self.node_high_pic[1]
                    x=self.nodes[self.temp_node_id_for_text_or_focus].position.x
                    y=self.nodes[self.temp_node_id_for_text_or_focus].position.y
                    temp=self.node_high_pic[0]+self.nodes[self.temp_node_id_for_text_or_focus].r

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

        def showLines(self):
            if self.lines:
                for line in self.lines.values():        #从节点边缘开始画线
                    d=line.target.position-line.source.position
                    t=abs(d)
                    if line.heading:
                        arrow=tk.LAST
                    else:
                        arrow=tk.NONE

                    if t:
                        S=line.source.position+d*(line.source.r/t)
                        T=line.target.position-d*(line.target.r/t)
                        if line.state == 1:     #等待姿态
                            self.canva.create_line(
                                S.x,S.y,
                                T.x,T.y,
                                fill="#5f5f69",width=line.width*3,arrow=arrow,dash=6
                                )
                            
                        elif line.state==2:     #高姿态
                            self.canva.create_line(
                                S.x,S.y,
                                T.x,T.y,
                                fill="#5f5f69",width=line.width*3,arrow=arrow
                                )
                            
                        self.canva.create_line(
                            S.x,S.y,
                            T.x,T.y,
                            fill='white',width=line.width,arrow=arrow
                            )

        def showTextblanks(self):
            if self.textblanks:
                h,w=2,3
                for id,textblank in self.textblanks.items():
                    if textblank.hide:                  #不显示关闭的文本框
                        self.textblanks[id].bbox=None
                        continue

                    nw=textblank.anchor
                    title=' '+' \n '.join(textblank.text.split('\n'))+' '

                    text=self.canva.create_text(    #用于获取包围盒
                        nw.x,nw.y,
                        text=title,
                        font=textblank.font,
                        anchor=tk.NW
                    )
                    bbox=self.canva.bbox(text)      #获取包围框

                    if self.textblanks[id].bbox !=bbox:  #更新size
                        self.textblanks[id].bbox=bbox

                    if textblank.state==1:      #等待
                        bcolor='#525253'
                        icolor="#333334"
                    elif textblank.state==2:    #高姿态
                        bcolor="#d3e1ff"
                        icolor="#333334"
                    else:                       #低姿态
                        bcolor='#525253'
                        icolor='#272728'

                    v=self.textblanks[id].anchor-self.nodes[id].position
                    if v !=Vector():
                        S=self.nodes[id].position+((self.nodes[id].r+3)/abs(v))*v
                        self.canva.create_line(
                            S.x,S.y,bbox[0],bbox[1],
                            fill=bcolor,width=2
                        )

                    

                    self.canva.create_rectangle(
                        bbox,
                        fill=icolor,
                        outline=bcolor,width=2
                    )
                    self.canva.create_text(         #重绘text
                        nw.x,nw.y,
                        text=title,
                        font=textblank.font,fill=textblank.color,
                        anchor=tk.NW
                    )

                    
                    self.canva.create_rectangle(
                        bbox[0]-w,bbox[1]-h,bbox[0]+w,bbox[1]+h,
                        fill='#B7CEFF',
                        outline="#d3e1ff",width=1
                    )

        def showSubWindowForTextLocation(self):
            id=self.temp_node_id_for_text_or_focus
            if id is not None:
                wx,wy=self.sub_window_for_text.winfo_x()-self.root.winfo_x(),self.sub_window_for_text.winfo_y()-self.root.winfo_y()
                ww,wh=self.sub_window_for_text.winfo_width(),self.sub_window_for_text.winfo_height()
                x,y=self.nodes[id].position.x,self.nodes[id].position.y
                r=self.nodes[id].r

                self.showLineOnlyForLocation(x,y,wx,wy,r)
                self.showLineOnlyForLocation(x,y,wx+ww,wy,r)
                self.showLineOnlyForLocation(x,y,wx,wy+wh,r)
                self.showLineOnlyForLocation(x,y,wx+ww,wy+wh,r)

        def showLineOnlyForLocation(self,sx,sy,tx,ty,r):
            if sx!=tx or sy!=ty:
                ratio=(r+3)/(((sx-tx)**2+(sy-ty)**2)**0.5)
                x=sx+ratio*(tx-sx)
                y=sy+ratio*(ty-sy)

                self.canva.create_line(
                    x,y,tx,ty,
                    fill="#353561",width=2
                )



#main
if __name__ == "__main__":
    a=Aplication(save_id=0)
    a.run()

    