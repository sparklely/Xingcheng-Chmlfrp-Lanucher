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

# 主窗口左侧边栏按钮
class Left_sidebar_Button(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master,fg_color="#dcdcdc",width=173,height=350)
        # 添加隧道
        self.add_tun=ctk.CTkButton(self,text="添加隧道",text_color="black",font=("Arial",16.5),width=173,hover_color="#d2d2d2",corner_radius=0,fg_color="transparent")
        self.add_tun.place(x=0,y=0)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.winx=0
        self.winy=0
        self.overrideredirect(True)
        self.title("XingCheng Chmlfrp Lanucher - main")
        self.geometry("730x420")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        # 处理/下载背景图片
        if not (User.LoginData['background_img']=='' or User.LoginData['background_img']==None):
            self.bg=Image.open(BytesIO(reqt.get(User.LoginData['background_img']).content))
            self.bg=self.bg.resize((730,420))
            self.bg=ImageTk.PhotoImage(self.bg)
            self.bg_label=ctk.CTkLabel(self,text="",image=self.bg)
            self.bg_label.place(relx=0,rely=0)
        # 识别鼠标拖拽事件
        self.bind("<ButtonPress-1>",App.on_drag_start)
        self.bind("<B1-Motion>",App.on_drag)
        self.bind("<ButtonRelease-1>",App.on_drag_stop)
        # 左侧边栏背景
        self.Left_sidebar_bg=ctk.CTkLabel(self,text="",height=730,width=173)
        self.Left_sidebar_bg.place(relx=0,rely=0)
        # 用户头像
        self.userimg=Image.open(BytesIO(reqt.get(User.LoginData['userimg']).content))
        self.userimg=self.userimg.resize((47,47))
        self.userimg=ImageTk.PhotoImage(self.userimg)
        self.userimg_label=ctk.CTkLabel(self,text="",image=self.userimg)
        self.userimg_label.place(relx=0.02,rely=0.05)
        # 用户邮箱/名字
        self.useremail_label=ctk.CTkLabel(self,text=User.LoginData["email"],font=("Arial",11))
        self.useremail_label.place(x=68,y=40)
        self.username_label=ctk.CTkLabel(self,text=User.LoginData["username"],font=("Arial",16))
        self.username_label.place(x=71,rely=0.05)
        # 主窗口左侧边栏按钮
        self.Left_sidebar_Button=Left_sidebar_Button(master=self)
        self.Left_sidebar_Button.place(relx=0,rely=0.2)
        # start frp
        App.usertun_TidyUp()
        self.optionmenu = ctk.CTkOptionMenu(self,height=41,corner_radius=0,dynamic_resizing=False,command=self.optionmenu_callback,values=User.TunList)
        self.optionmenu.place(relx=0.77,rely=0.85)
        self.start_frp_button=ctk.CTkButton(self,text="Start Frp\n#0 你TM倒是选a",corner_radius=0,state="disabled",height=40,command=self.start_frp)
        self.start_frp_button.place(relx=0.72,rely=0.85)
    
    # 处理鼠标按下事件
    def on_drag_start(event):
        App.winx=event.x
        App.winy=event.y

    # 处理鼠标移动事件
    def on_drag(event):
        deltax=event.x-App.winx
        deltay=event.y-App.winy
        new_x=GUI.tkObj.winfo_x()+deltax
        new_y=GUI.tkObj.winfo_y()+deltay
        GUI.tkObj.geometry(f"+{new_x}+{new_y}")

    # 处理鼠标释放事件
    def on_drag_stop(event):
        App.winx=0
        App.winy=0

    # 处理隧道信息
    def usertun_TidyUp():
        usertun=ChmlfrpAPI.user_tun()
        if usertun[0]==False:
            if usertun[1]==None:
                return ["无数据"]
            return usertun[1]
        re_usertun_list=[]
        for usertun_e in usertun[1]:
            re_usertun_list.append("#"+usertun_e["id"]+" "+usertun_e["name"]+" - "+usertun_e["type"])
        User.TunList=re_usertun_list

    # 更新start frp按钮
    def optionmenu_callback(self,choice):
        if "#" not in choice:
            self.start_frp_button.configure(text=f"Start Frp\n{choice}")
        else:
            self.start_frp_button.configure(text=f"Start Frp\n{choice}",state="normal")

    # 启动frp
    def start_frp(self):
        # 获取启动tunID
        tunID=self.start_frp_button.cget("text")
        tunID=tunID.split("\n")[1]
        tunID=tunID.split(" ")[0][1:]
        # 启动
        StartFrp.start(tunID)
        # 弹窗
        info_window.info("正在拉起frp核心","协议: \n连接地址: ")

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
    GUI.tkObj=App()
    GUI.tkObj.mainloop()