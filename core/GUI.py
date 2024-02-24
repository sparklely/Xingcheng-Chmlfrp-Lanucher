from core.network import ChmlfrpAPI
from core.module import StartFrp
from core.g_var import User,GUI
from PIL import Image,ImageTk,ImageDraw
from io import BytesIO
from os import path
import yaml
import requests as reqt
import customtkinter as ctk
import tkinter.messagebox

class info_window:
    def info(title:str,text:str):
        tkinter.messagebox.showinfo(title=title,message=text)
    def yesno(title:str,text:str):
        return tkinter.messagebox.askyesno(title=title,message=text)

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("XingCheng Chmlfrp Lanucher - login")
        self.geometry(f"320x200")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        self.Login_title=ctk.CTkLabel(self,text="Chmlfrp Login",font=("Arial",16))
        self.Login_title.place(relx=0.03,rely=0.01)
        # login name
        self.Login_name_title=ctk.CTkLabel(self,text="用户名/邮箱/QQ号",font=("微软雅黑",12.5))
        self.Login_name_title.place(relx=0.14,rely=0.17)
        self.Login_name=ctk.CTkEntry(self,height=15,width=195)
        self.Login_name.place(relx=0.13,rely=0.3)
        # login Password
        self.Login_password_title=ctk.CTkLabel(self,text="密码",font=("微软雅黑",12.5))
        self.Login_password_title.place(relx=0.14,rely=0.45)
        self.Login_password=ctk.CTkEntry(self,height=15,width=195,show="*")
        self.Login_password.place(relx=0.13,rely=0.58)
        # login button
        self.Login_button=ctk.CTkButton(self,text="登录",width=125,command=self.login)
        self.Login_button.place(relx=0.56,rely=0.78)
        # 自动登录
        self.AutmLogin=ctk.CTkCheckBox(self,checkbox_width=16,checkbox_height=16,text="自动登录",font=("微软雅黑",12))
        self.AutmLogin.place(relx=0.07,rely=0.75)

    # login
    def login(self):
        logining=ChmlfrpAPI.login(self.Login_name.get(),self.Login_password.get())
        if logining[0]:
            # AutmLogin处理
            if self.AutmLogin.get()==1:
                al=open("./temp/AutmLogin.yml","w")
                data={"enable":True,"name":self.Login_name.get(),"password":self.Login_password.get()}
                al.write(yaml.safe_dump(data))
                al.close()
            self.destroy()
            main()
        else:
            info_window.info("登录失败","请检查账号密码是否正确")
    
    # login error
    def login_error(self,error_info):
        # 创建对话窗口
        self.login_error_windows=ctk.CTkInputDialog(text=f"{error_info}", title="登录失败")

# 隧道信息卡
class Tun_Info_Card(ctk.CTkFrame):
    def __init__(self,master,tundata):
        super().__init__(master,fg_color="#e5e5e5",width=245,height=183,corner_radius=12)
        # 隧道id
        self.tun_id=ctk.CTkLabel(self,text="#"+tundata["id"],font=("微软雅黑",15.5))
        self.tun_id.place(x=13,y=7)
        # 隧道名称
        ctk.CTkLabel(self,text=tundata["name"],font=("微软雅黑",15.5,"bold")).place(x=(len(tundata["id"])+2)*9+13,y=7)
        # 内网地址
        ctk.CTkLabel(self,text="内网地址: "+tundata["localip"]+":"+tundata["nport"]+" - "+tundata["type"],font=("微软雅黑",13)).place(x=13,y=37)
        # 节点信息
        ctk.CTkLabel(self,text="节点信息: "+tundata["node"],font=("微软雅黑",13)).place(x=13,y=57)
        # 连接地址
        try:
            ctk.CTkLabel(self,text="连接地址: "+tundata["ip"],font=("微软雅黑",13)).place(x=13,y=77)
        except:
            ctk.CTkLabel(self,text="连接地址: ",font=("微软雅黑",13)).place(x=13,y=77)
        # 启动隧道按钮
        ctk.CTkButton(self,text="启动隧道",command=self.start_frp,fg_color="#e5e5ec",width=219,hover_color="#e2e2e9",border_width=1,border_color="#409eff",text_color="#409eff").place(x=13,y=108)
        # 删除隧道按钮
        ctk.CTkButton(self,text="删除隧道",command=self.del_tun,fg_color="#ece5e5",width=219,hover_color="#e9e2e2",border_width=1,border_color="#f56c6c",text_color="#f56c6c").place(x=13,y=143)
    
    # 启动frp
    def start_frp(self):
        # 启动
        StartFrp.start(self.tun_id.cget("text")[1:])
        # 弹窗
        info_window.info("正在拉起frp核心","协议: "+User.TunDict[self.tun_id.cget("text")[1:]]["type"]+"\n连接地址: "+User.TunDict[self.tun_id.cget("text")[1:]]["ip"])

    # 删除隧道
    def del_tun(self):
        tunid=self.tun_id.cget("text")[1:]
        if info_window.yesno("删除隧道",f"您现在正在删除隧道 #{tunid} ,请确认是否删除"):
            if not ChmlfrpAPI.del_tun(self.tun_id.cget("text")[1:])[0]:
                info_window.info("删除隧道","无法删除,隧道不属于你或不存在")
            else:
                # 刷新隧道
                GUI.tkObj.main_tab_view.refresh_tun()

# 隧道滑动条窗口
class Tun_Info_win(ctk.CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master,border_width=0,corner_radius=0,width=768,height=420)
        self.figure=0
        self.list_tun_info_card=[]
        if User.TunData!=None:
            # 遍历创建隧道信息卡
            for tundata in User.TunData:
                self.list_tun_info_card.append(Tun_Info_Card(master=self,tundata=tundata))
                self.list_tun_info_card[self.figure].grid(row=int(self.figure/3),column=int(self.figure%3),pady=7,padx=6)
                self.figure+=1
                
# 左侧边栏用户信息
class Left_Sidebar_Frame(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master,width=158,fg_color="#e1e1e1",border_color="#e1e1e1")
        self.user_id=ctk.CTkLabel(self,font=("微软雅黑",12.5),text="用户ID:  "+str(User.LoginData["userid"]))
        self.user_id.place(x=13,y=3)
        self.user_group=ctk.CTkLabel(self,font=("微软雅黑",12.5),text="权限组:  "+str(User.LoginData["usergroup"]))
        self.user_group.place(x=13,y=28)
        self.user_tun=ctk.CTkLabel(self,font=("微软雅黑",12.5),text="隧道数:  "+str(User.LoginData["tunnelstate"])+"/"+str(User.LoginData["tunnel"])+"条")
        self.user_tun.place(x=13,y=53)
        self.user_bandwidth=ctk.CTkLabel(self,font=("微软雅黑",12.5),text="限带宽:  "+str(User.LoginData["bandwidth"])+"m | "+str(User.LoginData["bandwidth"]*4)+"m")
        self.user_bandwidth.place(x=13,y=78)
        self.user_realname=ctk.CTkLabel(self,font=("微软雅黑",12.5),text="实名状态:  "+User.LoginData["realname"])
        self.user_realname.place(x=13,y=103)

# 主窗口切换界面
class MainTabView(ctk.CTkTabview):
    def __init__(self,master):
        super().__init__(master,height=480,width=810,corner_radius=13,fg_color="#ebebeb",segmented_button_fg_color="#ebebeb",segmented_button_selected_color="#d7d7d7",segmented_button_unselected_hover_color="#d7d7d7",segmented_button_selected_hover_color="#d7d7d7",segmented_button_unselected_color="#ebebeb",text_color="#969696")
        # 页面
        self.add("启动")
        self.add("隧道管理")
        self.add("设置")
        # 处理/下载背景图片
        if not (User.LoginData['background_img']=='' or User.LoginData['background_img']==None):
            self.bg=Image.open(BytesIO(reqt.get(User.LoginData['background_img']).content))
            self.bg=self.bg.resize((810,450))
            self.bg=ImageTk.PhotoImage(self.bg)
            self.bg_label_qd=ctk.CTkLabel(self.tab("启动"),text="",image=self.bg)
            self.bg_label_qd.place(x=0,y=0)
            self.bg_label_tun=ctk.CTkLabel(self.tab("隧道管理"),text="",image=self.bg)
            self.bg_label_tun.place(x=0,y=0)
            self.bg_label_sz=ctk.CTkLabel(self.tab("设置"),text="",image=self.bg)
            self.bg_label_sz.place(x=0,y=0)
        '''启动'''
        # 左侧边栏背景
        self.qd_Left_sidebar_bg=ctk.CTkLabel(self.tab("启动"),text="",height=730,width=173,bg_color="#d7d7d7")
        self.qd_Left_sidebar_bg.place(relx=0,rely=0)
        # 用户头像
        self.qd_userimg=Image.open(BytesIO(reqt.get(User.LoginData['userimg']).content))
        self.qd_userimg=self.qd_userimg.resize((47,47))
        self.qd_userimg=ImageTk.PhotoImage(self.qd_userimg)
        self.qd_userimg_label=ctk.CTkLabel(self.tab("启动"),text="",image=self.qd_userimg)
        self.qd_userimg_label.place(relx=0.02,rely=0.05)
        # 用户邮箱/名字
        self.qd_useremail_label=ctk.CTkLabel(self.tab("启动"),text=User.LoginData["email"],font=("Arial",11),bg_color="#d7d7d7")
        self.qd_useremail_label.place(x=68,y=40)
        self.qd_username_label=ctk.CTkLabel(self.tab("启动"),text=User.LoginData["username"],font=("Arial",16),bg_color="#d7d7d7")
        self.qd_username_label.place(x=71,rely=0.05)
        # 用户信息
        self.qd_userinfo=Left_Sidebar_Frame(master=self.tab("启动"))
        self.qd_userinfo.place(x=8,rely=0.23)
        # start frp
        MainTabView.usertun_TidyUp()
        self.qd_optionmenu=ctk.CTkOptionMenu(self.tab("启动"),height=41,corner_radius=0,dynamic_resizing=False,command=self.optionmenu_callback,values=User.TunList)
        self.qd_optionmenu.place(relx=0.77,rely=0.85)
        self.qd_start_frp_button=ctk.CTkButton(self.tab("启动"),text="Start Frp\n#0 你TM倒是选a",corner_radius=0,state="disabled",height=40,command=self.start_frp)
        self.qd_start_frp_button.place(relx=0.72,rely=0.85)
        '''隧道管理'''
        # 隧道滑动条窗口覆盖
        self.tun_win=Tun_Info_win(master=self.tab("隧道管理"))
        self.tun_win.place(x=0,y=0)

    # 刷新隧道
    def refresh_tun(self):
        MainTabView.usertun_TidyUp()
        # 主页面start frp
        self.qd_optionmenu.configure(values=User.TunList)
        # 隧道滑动条窗口覆盖
        self.tun_win.destroy()
        self.tun_win=Tun_Info_win(master=self.tab("隧道管理"))
        self.tun_win.place(x=0,y=0)

    # 处理隧道信息
    def usertun_TidyUp():
        usertun=ChmlfrpAPI.user_tun()
        # 初始化
        User.TunList=[]
        User.TunDict={}
        if usertun[0]:
            User.TunData=usertun[1]
            for tuninfo in usertun[1]:
                User.TunList.append("#"+tuninfo["id"]+" "+tuninfo["name"])
                User.TunDict[tuninfo["id"]]=tuninfo
        else:
            User.TunList.append("请先创建隧道")

    # 更新start frp按钮
    def optionmenu_callback(self,choice):
        if "#" not in choice:
            self.qd_start_frp_button.configure(text=f"Start Frp\n{choice}")
        else:
            self.qd_start_frp_button.configure(text=f"Start Frp\n{choice}",state="normal")

    # 启动frp
    def start_frp(self):
        # 获取启动tunID
        tunID=self.qd_start_frp_button.cget("text")
        tunID=tunID.split("\n")[1]
        tunID=tunID.split(" ")[0][1:]
        # 启动
        StartFrp.start(tunID)
        # 弹窗
        info_window.info("正在拉起frp核心","协议: "+User.TunDict[tunID]["type"]+"\n连接地址: "+User.TunDict[tunID]["ip"])

# 主窗口
class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.winx=0
        self.winy=0
        self.overrideredirect(True)
        self.attributes('-topmost','true')
        self.title("XingCheng Chmlfrp Lanucher - main")
        self.configure(fg_color="#ebebeb")
        self.geometry("810x480")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        # 透明化背景
        self.wm_attributes('-transparentcolor','#0000ff')
        # 页面覆盖
        self.main_tab_view=MainTabView(master=self)
        self.main_tab_view.place(x=0,y=0)
        # 关闭窗口按钮
        self.close_win_button=ctk.CTkButton(self,text="x",width=27,height=27,font=("Arial",23,"bold"),corner_radius=24,command=self.close_win,fg_color="#ebebeb",hover_color="#e1e1e1",text_color="#bebebe")
        self.close_win_button.place(relx=0.92,y=5)
        # 遮盖背景
        self.shelter_down=ctk.CTkLabel(self,text="",width=810,height=13,bg_color="#0000FF")
        self.shelter_down.place(x=0,y=467)
        self.shelter_left=ctk.CTkLabel(self,text="",width=13,height=480,bg_color="#0000FF")
        self.shelter_left.place(x=0,y=0)
        self.shelter_right=ctk.CTkLabel(self,text="",width=13,height=480,bg_color="#0000FF")
        self.shelter_right.place(x=797,y=0)
        # 识别鼠标拖拽事件
        self.bind("<ButtonPress-1>",Main.on_drag_start)
        self.bind("<B1-Motion>",Main.on_drag)
        self.bind("<ButtonRelease-1>",Main.on_drag_stop)
        # 取消一直顶置
        self.attributes('-topmost','false')

    # 关闭窗口
    def close_win(self):
        self.destroy()

    # 处理鼠标按下事件
    def on_drag_start(event):
        # 识别按下位置
        if str(event.widget)==".!maintabview" or str(event.widget)==".!maintabview.!ctkcanvas":
            GUI.tkObj.winx=event.x
            GUI.tkObj.winy=event.y

    # 处理鼠标移动事件
    def on_drag(event):
        if GUI.tkObj.winy!=0:
            deltax=event.x-GUI.tkObj.winx
            deltay=event.y-GUI.tkObj.winy
            new_x=GUI.tkObj.winfo_x()+deltax
            new_y=GUI.tkObj.winfo_y()+deltay
            GUI.tkObj.geometry(f"+{new_x}+{new_y}")

    # 处理鼠标释放事件
    def on_drag_stop(event):
        GUI.tkObj.winx=0
        GUI.tkObj.winy=0

def run():
    login=Login()
    if path.isfile("./temp/AutmLogin.yml"):
        # 自动登录处理
        al=yaml.safe_load(open("./temp/AutmLogin.yml","r").read())
        if al['enable']==True:
            logining=ChmlfrpAPI.login(al["name"],al['password'])
            if logining[0]:
                login.destroy()
                main()
            else:
                info_window.info("自动登录失败","自动登录失败,点击确认以拉起登录界面")
                login.mainloop()
    else:
        login.mainloop()

def main():
    GUI.tkObj=Main()
    GUI.tkObj.mainloop()