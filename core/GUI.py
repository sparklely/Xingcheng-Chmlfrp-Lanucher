from core.network import ChmlfrpAPI

import customtkinter as ctk

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("XingCheng Chmlfrp Lanucher - login")
        self.geometry("320x200")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        self.Login_title=ctk.CTkLabel(self,text="Chmlfrp Login",font=("微软雅黑",16))
        self.Login_title.place(relx=0.03,rely=0.01)
        # login name
        self.Login_name_title=ctk.CTkLabel(self,text="用户名/邮箱/QQ号",font=("微软雅黑",12.5))
        self.Login_name_title.place(relx=0.14,rely=0.15)
        self.Login_name=ctk.CTkEntry(self,height=15,width=185)
        self.Login_name.place(relx=0.13,rely=0.3)
        # login Password
        self.Login_password_title=ctk.CTkLabel(self,text="密码",font=("微软雅黑",12.5))
        self.Login_password_title.place(relx=0.14,rely=0.43)
        self.Login_password=ctk.CTkEntry(self,height=15,width=185)
        self.Login_password.place(relx=0.13,rely=0.58)
        # login button
        self.Login_button=ctk.CTkButton(self,text="登录",width=125,command=self.login)
        self.Login_button.place(relx=0.57,rely=0.78)

    # login
    def login(self):
        if ChmlfrpAPI.login(self.Login_name.get(),self.Login_password.get())[0]:
            self.destroy()
            main()
        else:
            pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("XingCheng Chmlfrp Lanucher - main")
        self.geometry("730x420")
        self.iconbitmap("./chmlfrp.ico")
        self.resizable(0, 0)
        # start frp
        self.start_frp_button=ctk.CTkButton(self,text="Start Frp",height=40,command=self.button_callback)
        self.start_frp_button.place(relx=0.73,rely=0.83)
        self.optionmenu = ctk.CTkOptionMenu(self,command=self.optionmenu_callback,values=["1","2"])
        self.optionmenu.place(relx=0.1,rely=0.1)

    # 更新start frp按钮的信息
    def optionmenu_callback(self,choice):
        self.start_frp_button.configure(text=f"Start Frp\n{choice}")

    def button_callback(self):
        print("button pressed")

def run():
    login=Login()
    login.mainloop()

def main():
    app=App()
    app.mainloop()