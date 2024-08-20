from random import choice
import threading
from colorama import Fore
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import kivy
import socket
import time
import kivymd
from kivymd.uix.label import MDLabel
from  kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout 
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.relativelayout import MDRelativeLayout

servers = 0
clients = 0
send_msg = ""
recv_msg = ""
global done1,done2
done1 = False
done2 = False

admins = {
    "a"      : "a",
    "Rohith" : "Perceptron",
    "Akash"  : "GaajiRaaj",
    "Praveen" : "GaajiKumar",
    "Sid"     : "Gaajeshwar"
}



def receive(conn):
    global send_msg,recv_msg,done1
    ports = [5555,6666,7777,8888,9999,6754,5493,9654,8546]
    while not done1:
        try:
            recv_msg = conn.recv(1024).decode()

        except:
            time.sleep(1)

Window.size = (350,675)
global c
global done3
done3 = False


global t,t1,t2
c = None
t = None
t1 = None
t2 = None

def create_socket():
    global c
    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Socket created")

class Screen1(Screen):
    pass
class Screen2(Screen):
    pass
class Screen3(Screen):
    pass
class Screen4(Screen):
    pass

class Screen5(Screen):
    pass

class Screen6(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MessageCard(MDCard):
    text = StringProperty()

class Clickable(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ChatRoom(MDApp):

    def build(self):
        global send_msg,recv_msg
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "A400"
        self.username = ''
        self.password = ''
        self.nickname = ''
        self.first = True
        self.conn = None
        self.server = False
        self.clients = []
        self.host = ''
        self.port = 8888
        self.noc = 0
        self.roomadmin = True
        self.sent = False
        self.recv = False
        Clock.schedule_once(self.changescreen,7)
        return WindowManager()
    
    def changescreen(self,dt):
        self.root.current = 'login'
    
    def back(self,screen):
        if screen == 'newscreen':
            self.root.current = "chatt"
        elif screen == 'room':
            self.root.current = 'login'
        elif screen == 'login':
            self.root.current = 'login'
        elif screen == 'chat room':
            self.root.current = 'chatroom'
        elif screen == 'mainpage':
            self.root.current = 'login'

    def send_message(self):
        home = self.root.get_screen('newscreen')

        message_input = home.ids.message_input
        messages = home.ids.message_list
        message = message_input.text
        scroll = home.ids.scroll
        try:
            if message:
                color_text = "\n"+"[color=#0000ff] You :[/color] "
                new_message = color_text + message
                messages.text += new_message
                message_input.text = ""
                scroll.scroll_y = 1
                color_text1 = f"[color=#ff0000]{self.nickname} : [/color]" 
                message = color_text1 + message 
                self.conn.send(message.encode())
        except:
            if not self.conn:
                self.exceptclose()



    def exceptclose(self):
        global c,done1,done2
        if self.server:
            if self.conn != None:
                self.conn.send(f'{self.nickname} is disconnected'.encode())
                self.conn.close()
                c.close()
                print("Socket destroyed 1")
            else:
                c.close()
                print("Socket destroyed 2")
        else:
            self.conn.send(f'{self.nickname} is disconnected'.encode())
            c.close()
            print("Socket destroyed 3")
        done1 = True
        done2 = True
        home = self.root.get_screen('newscreen')
        message_label = home.ids.message_list
        message_label.text = ""
        self.dialogbox.dismiss()
        self.root.current = "chatt"
    
    def on_start(self):
        menu_items = [
            {"viewclass":"OneLineListItem","text":"delete","on_release" : lambda x="delete":self.delete(x)}
        ]
        self.menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=2
        )

    def open_menu(self,button):
        self.menu.caller = button
        self.menu.open()

    def delete(self,text):
        home = self.root.get_screen('newscreen')
        message_input = home.ids.message_list
        message_input.text = ""
        self.menu.dismiss()
    
    def print_msg(self,msg):
        home = self.root.get_screen('newscreen')
        message_label = home.ids.message_list
        message_input = home.ids.message_input
        scroll = home.ids.scroll
        if msg:
            new_message = "\n"+msg
            message_label.text += new_message
            message_input.text = ""
            scroll.scroll_y = 1
   
    def start(self):
        alert = False
        self.sent = False
        try:
            global c
            global t
            create_socket()
            self.first = False
            nick =self.root.get_screen('chatt')
            nickname = nick.ids.nickname.text
            nick.ids.nickname.text = ""
            self.nickname = nickname
            self.conn = c
            self.conn.connect(('localhost',8888))
            print('socket connected')
            self.root.current = 'newscreen'
            t = threading.Thread(target=self.startover,args=("",))
            t.start()
        except:
            alert = True
            self.alert = MDDialog(title="Connection error",text="Connection cannot be made because of no active host server",buttons=[MDFillRoundFlatButton(text="Ok",on_release=self.conn_clo)])
            self.alert.open()


    def conn_clo(self,obj):
        self.alert.dismiss()
    
    def startserver(self):
        self.sent = False
        create_socket()
        global c
        global t
        nick =self.root.get_screen('chatt')
        nickname = nick.ids.nickname.text
        nick.ids.nickname.text = ""
        host = nick.ids.ipaddr.text
        port = nick.ids.port.text
        
        if not host or not port:
            self.arise = MDDialog(
                title="Error ",
                text="Please fill in all the details to connect or start the chat",
                buttons=[MDFillRoundFlatButton(text="OK",on_release=self.close_arise)]
            )
            self.arise.open()
        else:
            self.port = port
            self.host = host
            self.port = int(self.port)
            nick.ids.ipaddr.text = ""
            nick.ids.port.text = ""
            self.nickname = nickname
            c.bind((self.host,self.port))
            self.server = True
            print("Socket binded")
            self.root.current = 'newscreen'
            t = threading.Thread(target=self.startover,args=('server',))
            t.start()

    def close_arise(self,obj):
        self.arise.dismiss()



        

    def startover(self,ser):
        global c,done1,done2
        if ser == 'server':
            global done1
            c.listen(1)
            self.conn , port = c.accept()
            print("Connection made")
            done1 = False
            t1 = threading.Thread(target=receive,args=(self.conn,))
            t1.start()
        else:
            
            done1 = False
            t1 = threading.Thread(target=receive,args=(self.conn,))
            t1.start()
        done2 = False
        t2 = threading.Thread(target=self.receiv_msg)
        t2.start()
    
    def receiv_msg(self):
        global recv_msg,done2
        while not done2:
            if recv_msg != "":
                listmsg = recv_msg.split(' ')[-1]
                if listmsg == "disconnected":
                    self.sent = True
                self.print_msg(recv_msg)
                recv_msg = ""
            else:
                continue

    def login(self):
        global user
        login = self.root.get_screen('login')
        chat = self.root.get_screen('chatt')
        username = login.ids.user.text
        passwrod = login.ids.password.ids.text_field.text

        if username in admins and admins[username] == passwrod:
            self.username = username
            user = username
            self.password = passwrod
            login.ids.user.text = ''
            login.ids.password.ids.text_field.text = ""
            chat.ids.userna.text = username
            chat.ids.pwd.text = passwrod
            self.root.current = "chatt"
        else:
            login.ids.user.text = ''
            login.ids.password.ids.text_field.text = ""
            self.dialog = MDDialog(
                title="Try Again",
                text="Wrong Username or Password",
                buttons=[MDFillRoundFlatButton(text="OK",on_release=self.close_dialog),MDFillRoundFlatButton(text="Cancel",on_release=self.close_dialog)]
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
    

    def backdialog(self):
        self.dialogbox = MDDialog(title="Alert",
                                  text="If you try to go back your session will be closed",
                                  buttons=[MDFillRoundFlatButton(text="OK",on_release=self.close_conn),MDFillRoundFlatButton(text="Cancel",on_release=self.close_dialog_screen)]
        )
        self.dialogbox.open()

    def close_conn(self,obj):
        global c,done1,done2
        if self.server:
            if self.conn != None :
                if not self.sent:
                    self.sent = True
                    self.conn.send(f'{self.nickname} is disconnected'.encode())
                    self.conn.close()
                else:
                    self.conn.close()
                c.close()
                print("Socket destroyed 1")
            else:
                c.close()
                print("Socket destroyed 2")
        else:
            if not self.sent:
                self.sent = True
                self.conn.send(f'{self.nickname} is disconnected'.encode())
                c.close()
            print("Socket destroyed 3")
        done1 = True
        done2 = True
        home = self.root.get_screen('newscreen')
        message_label = home.ids.message_list
        message_label.text = ""
        self.dialogbox.dismiss()
        self.root.current = "chatt"

    def close_dialog_screen(self,obj):
        self.dialogbox.dismiss()

    def send_over(self):
        global c,done1,done2,done3
        create_socket()
        chatroom = self.root.get_screen('chatt')
        nickname = chatroom.ids.nicks.text
        chatroom.ids.nicks.text = ""
        self.nickname = nickname
        c.bind(('localhost',8888))
        self.server = True
        print("Socket binded")
        self.root.current = "chatroom"
        done3 = False
        t = threading.Thread(target=self.roomrecv)
        t.start()

    def roomrecv(self):
        global c,done1,done2,done3
        
        while self.noc <= 10 and not done3:
            global c
            done3 = False
            c.listen(10)
            conn,port = c.accept()
            self.clients.append(conn)
            print(f"Connection made from {conn} in {port}")
            t1 = threading.Thread(target=self.handleclient,args=(conn,port))
            t1.start()
            self.noc += 1
        
    def handleclient(self,conn,port):
        msg = ""
        while msg != "exit":
            msg = conn.recv(1024).decode()
            self.add_msg(msg)
            for connections in self.clients:
                if connections != conn:
                    try:
                        connections.send(msg.encode()) 
                    except:
                        continue
        conn.send("exit".encode())
        conn.close()

    def add_msg(self,msg):
        toprint = self.root.get_screen('chatroom')
        msglabel = toprint.ids.message_list
        msglabel.text += msg

    def send_room(self):
        sending = self.root.get_screen('chatroom')
        minput = sending.ids.message_input
        List = sending.ids.message_list
        msg = minput.text
        colors = ["[color=#00ff00]","[color=#ff0000]","[color=#0000ff]","[color=#ff00ff]","[color=#ffff00]"]
        if self.roomadmin:
            if msg:
                col = " "
                newmsg = "\n"+f"{col} You :[/color]"
                newmsg = newmsg + msg
                List.text += newmsg
                minput.text = ""
                sendmsg = msg
                for connections in self.clients:
                    try:
                        connections.send(sendmsg.encode())
                    except:
                        continue
        else:
            if msg:
                newmsg = "\n" + "[color=#0000ff] You : [/color]" + msg
                List.text += newmsg
                minput.text = ""
                sendmsg = msg
                self.conn.send(sendmsg.encode())


    def join_over(self):
        global done1,done2,done3,c
        self.roomadmin = False
        try:
            create_socket()
            self.conn = c
            self.conn.connect(('localhost',8888))
            done1 = False
            done2 = False
            t1 = threading.Thread(target=receive,args=(self.conn,))
            t1.start()
            t = threading.Thread(target=self.receiv_room)
            t.start()
            self.root.current = 'chatroom'
        except:
            time.sleep(1)


    def receiv_room(self):
        global recv_msg,done2
        while not done2:
            if recv_msg != "":
                self.add_msg(recv_msg)
                recv_msg = ""
            else:
                continue

    def close_room(self,obj):
        global done1,done2,done3,c
        if self.roomadmin:
            if not self.recv:
                self.recv = True
                for connections in self.clients:
                    connections.send("The server device has been shut down".encode())
                c.close()
            else:
                c.close()
            c.close()
            done3 = True
        else:
            if not self.recv:
                self.recv = True
                self.conn.send(f"{self.nickname} is disconnected")
                self.conn.close()
        done1 = True
        done2 = True
        self.roomdialog.dismiss()
        self.root.current = 'chatt'

    def menu_room(self):
        menu_item = [
            {"viewclass":"OneLineListItem","text":"delete","on_release" : lambda x="delete":self.deleteroom(x)}
        ]
        self.newmenu = MDDropdownMenu(
            caller=None,
            items=menu_item,
            width_mult=2
        )

    def open_menur(self,button):
        self.menu_room()
        self.newmenu.caller = button
        self.newmenu.open()

    def deleteroom(self,obj):
        get = self.root.get_screen('chatroom')
        todelete = get.ids.message_list
        todelete.text = ""
        self.newmenu.dismiss()

    def room_dialog(self):
        self.roomdialog = MDDialog(title="Alert",
                                  text="If you try to go back your session will be closed",
                                  buttons=[MDFillRoundFlatButton(text="OK",on_release=self.close_room),MDFillRoundFlatButton(text="Cancel",on_release=self.close_room_dialog)]
        )
        self.roomdialog.open()

    def close_room_dialog(self,obj):
        self.roomdialog.dismiss()


if __name__ == "__main__":
    chat = ChatRoom()
    chat.run()