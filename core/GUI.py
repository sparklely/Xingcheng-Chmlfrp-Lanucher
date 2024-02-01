from core.network import ChmlfrpAPI

import customtkinter as ctk
import tkinter.messagebox

class info_window:
    def info(title:str,text:str):
        tkinter.messagebox.showinfo(title=title,message=text)

class Login(ctk.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
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
        self.Login_password=ctk.CTkEntry(self,height=15,width=195)
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
        self.title("XingCheng Chmlfrp Lanucher - main")
        self.geometry("730x420")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        # start frp
        self.optionmenu = ctk.CTkOptionMenu(self,height=36,command=self.optionmenu_callback,values=["1","2","3","4"])
        self.optionmenu.place(relx=0.77,rely=0.85)
        self.start_frp_button=ctk.CTkButton(self,text="Start Frp\nNone",height=35,command=self.button_callback)
        self.start_frp_button.place(relx=0.72,rely=0.85)

    # 更新start frp按钮的信息
    def optionmenu_callback(self,choice):
        self.start_frp_button.configure(text=f"Start Frp\n{choice}")

    def button_callback(self):
        print("button pressed")

def run():
    login=Login()
    login.mainloop()

def main():
    ctk.set_appearance_mode('Dark')
    app=App()
    app.mainloop()