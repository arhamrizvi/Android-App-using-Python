from kivy.app import App
from kivy.lang import Builder # this is how you connect to the python file
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        print("Sign up buttom pressed")
    
    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong username or password"

    def forgot_password(self):
        print("\n forgot password \n")
        
        self.manager.current = "sign_up_screen"
        


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
            users[uname] = {'username':uname, 'password':pword,
            'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json","w") as file:
            json.dump(users,file)
        
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_Screen"
        
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_Screen"


    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            temp_var = "quotes//"+feel+".txt"
            with open(temp_var,encoding='utf8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "try another feeling"


class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass


class ForgetPassword(Screen):
    def enter_uname_pword(self,uname,pword):
        with open('users.json') as file:
            users = json.load(file)
            if uname in users:
                print(users)


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__=='__main__':
    MainApp().run()
