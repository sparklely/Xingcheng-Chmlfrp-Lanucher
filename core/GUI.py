from core.network import ChmlfrpAPI
from core.module import StartFrp
from core.g_var import User
from PIL import Image,ImageTk,ImageDraw
from io import BytesIO
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

    # login
    def login(self):
        logining=ChmlfrpAPI.login(self.Login_name.get(),self.Login_password.get())
        if logining[0]:
            self.destroy()
            main()
        else:
            info_window.info("登录失败"," 未知错误 ")
    
    # login error
    def login_error(self,error_info):
        # 创建对话窗口
        self.login_error_windows=ctk.CTkInputDialog(text=f"{error_info}", title="登录失败")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #self.overrideredirect(True)
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
        # 左侧边栏
        self.Left_sidebar_bg=ctk.CTkLabel(self,text="",height=730,width=173)
        self.Left_sidebar_bg.place(relx=0,rely=0)
        self.userimg=Image.open(BytesIO(reqt.get(User.LoginData['userimg']).content))
        self.userimg=self.userimg.resize((47,47))
        self.userimg=ImageTk.PhotoImage(self.userimg)
        self.userimg_label=ctk.CTkLabel(self,text="",image=self.userimg)
        self.userimg_label.place(relx=0.02,rely=0.05)
        self.useremail_label=ctk.CTkLabel(self,text=User.LoginData["email"],font=("Arial",11))
        self.useremail_label.place(x=68,y=40)
        self.username_label=ctk.CTkLabel(self,text=User.LoginData["username"],font=("Arial",16))
        self.username_label.place(x=71,rely=0.05)
        # start frp
        App.usertun_TidyUp()
        self.optionmenu = ctk.CTkOptionMenu(self,height=41,corner_radius=0,dynamic_resizing=False,command=self.optionmenu_callback,values=User.TunList)
        self.optionmenu.place(relx=0.77,rely=0.85)
        self.start_frp_button=ctk.CTkButton(self,text="Start Frp\n#0 你TM倒是选a",corner_radius=0,state="disabled",height=40,command=self.start_frp)
        self.start_frp_button.place(relx=0.72,rely=0.85)
    
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
    login.mainloop()

def main():
    app=App()
    app.mainloop()