# -- coding: utf-8 --
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import requests, json, re
import threading
import queue
import time
import main_part


class LoginPage(object):

    def __init__(self, root):
        self.root = root
        self.root.geometry("255x255+561+268")
        self.LoginPage()
        self.queue = queue.Queue()
        # self.names_list = []

    def LoginPage(self):
        font = "-family {Microsoft YaHei UI Light} -size 11 -weight " \
            "bold -slant roman -underline 0 -overstrike 0"
        self.loginPage = tk.Frame(master=self.root, height=261, width=255, bg='black')
        self.loginPage.pack()
        username = tk.StringVar()
        self.userNameEntry = ttk.Combobox(self.loginPage, textvariable=username)
        self.userNameEntry.place(relx=0.23, rely=0.23, height=25, relwidth=0.59)
        self.userNameEntry.configure(background="white",
                                     font=font,
                                     foreground="#000000",
                                     width=154,)
        self.get_users_thread()



        room = tk.StringVar()
        self.roomChooseEntry = ttk.Combobox(self.loginPage, textvariable=room)
        self.roomChooseEntry.place(relx=0.23, rely=0.58, height=25, relwidth=0.59)
        self.roomChooseEntry.configure(font=font,
                                       background="white",
                                       foreground="#000000",)
        self.roomChooseEntry.bind('<Return>', self.login)
        self.get_rooms_thread()

        self.LoginButton = tk.Button(self.loginPage, command=self.login)
        self.LoginButton.place(relx=0.402, rely=0.8, height=28, width=45)
        self.LoginButton.configure(activebackground="#ececec",
                                   activeforeground="#000000",
                                   background="#000000",
                                   disabledforeground="#a3a3a3",
                                   foreground="#ffffff",
                                   highlightbackground="#d9d9d9",
                                   highlightcolor="black",
                                   pady="0",
                                   relief='groove',
                                   text='''登陆''',
                                   width=45,)

        self.UserLabel = tk.Label(self.loginPage)
        self.UserLabel.place(relx=0.038, rely=0.23, height=23, width=42)
        self.UserLabel.configure(activebackground="#000000",
                                 activeforeground="white",
                                 background="#000000",
                                 disabledforeground="#a3a3a3",
                                 foreground="#ffffff",
                                 text='''用户名''',)

        self.RoomLabel = tk.Label(self.loginPage)
        self.RoomLabel.place(relx=0.038, rely=0.59, height=23, width=42)
        self.RoomLabel.configure(background="#000000",
                                 disabledforeground="#a3a3a3",
                                 foreground="#ffffff",
                                 text='''房间名''',)

        self.appLabel = tk.Label(self.loginPage)
        self.appLabel.place(relx=0.307, rely=0.044, height=33, width=97)
        self.appLabel.configure(background="#000000",
                                   disabledforeground="#a3a3a3",
                                   foreground="#ffffff",
                                   text='''DOLLARS''',
                                   font=font,
                                   width=97,)

    def login(self, event=None):
        self.userName = self.userNameEntry.get()
        self.roomName = self.roomChooseEntry.get()
        if self.userName == '' or self.roomName == '':
            tkinter.messagebox.showerror("错误", "用户名/房间名 信息不完整")
        else:
            self.roomName, self.roomId, self.session= main_part.login(self.userName, self.roomName, self.roomInfos)
            if self.roomName and self.roomId:
                self.loginPage.destroy()
                self.show_room(self.roomName)

    def show_room(self, roomName):
        threading.Thread(target=self.save_users).start()
        self.root.geometry('528x452+526+169')
        chatRoom = tk.Frame(master=self.root, height=453, width=528, bg='black')
        chatRoom.place(relx=0.0, rely=0.0, relheight=1.007, relwidth=1.013)
        chatRoom.pack()
        self.root.title(roomName)
        entry = tk.StringVar()
        self.Entry = tk.Entry(chatRoom, textvariable=entry)
        self.Entry.place(relx=0.019, rely=0.911, height=27, relwidth=0.568)
        self.Entry.configure(background="black",
                             disabledforeground="#a3a3a3",
                             font="TkFixedFont",
                             foreground="#ffffff",
                             highlightbackground="#d9d9d9",
                             highlightcolor="black",
                             insertbackground="white",
                             selectbackground="#c4c4c4",
                             selectforeground="black")
        self.Entry.bind('<Return>', self.button)

        self.postButton = tk.Button(chatRoom, command=self.button)
        self.postButton.place(relx=0.019, rely=0.824, height=28, width=299)
        self.postButton.configure(activebackground="#ececec",
                                  activeforeground="#000000",
                                  background="#ffffff",
                                  disabledforeground="#a3a3a3",
                                  foreground="#000000",
                                  highlightbackground="#d9d9d9",
                                  highlightcolor="black",
                                  pady="0",
                                  relief='groove',
                                  text='''发送''',)


        self.getMessageText = tk.Text(chatRoom)
        self.getMessageText.configure(background='#000000')
        self.getMessageText.place(relx=0.019, rely=0.022, relheight=0.777, relwidth=0.568)

        self.roomListLabel = tk.Label(chatRoom)
        self.roomListLabel.place(relx=0.606, rely=0.022, height=25, width=194)
        self.roomListLabel.configure(activebackground="#f9f9f9",
                                     activeforeground="black",
                                     background="#000000",
                                     disabledforeground="#a3a3a3",
                                     foreground="#ffffff",
                                     highlightbackground="#d9d9d9",
                                     highlightcolor="black",
                                     relief='groove',
                                     text='''房间列表''',)
        self.roomListLabel.bind('<Button-1>', self.create_room_thread)

        self.roomListbox = tk.Listbox(chatRoom)
        self.roomListbox.place(relx=0.606, rely=0.088, relheight=0.5, relwidth=0.367)
        self.roomListbox.configure(background="#000000",
                                   disabledforeground="#a3a3a3",
                                   font="TkFixedFont",
                                   foreground="#ffffff",
                                   highlightbackground="#d9d9d9",
                                   highlightcolor="black",
                                   relief='groove',
                                   selectbackground="#c4c4c4",
                                   selectforeground="black",
                                   width=194,)
        self.roomListbox.bind('<Double-Button-1>', self.join_new_room)

        self.memberLabel = tk.Label(chatRoom)
        self.memberLabel.place(relx=0.606, rely=0.597, height=25, width=194)
        self.memberLabel.configure(activebackground="#f9f9f9",
                                   activeforeground="black",
                                   background="#000000",
                                   disabledforeground="#a3a3a3",
                                   foreground="#ffffff",
                                   highlightbackground="#d9d9d9",
                                   highlightcolor="black",
                                   relief='groove',
                                   text='''成员列表''',)

        self.memberListbox = tk.Listbox(chatRoom)
        self.memberListbox.place(relx=0.606, rely=0.664, relheight=0.31, relwidth=0.367)
        self.memberListbox.configure(background="#000000",
                                     disabledforeground="#a3a3a3",
                                     font="TkFixedFont",
                                     foreground="#ffffff",
                                     highlightbackground="#d9d9d9",
                                     highlightcolor="black",
                                     selectbackground="#c4c4c4",
                                     selectforeground="black",
                                     width=194,)

        main_part.get_message_thread(self.userName, self.getMessageText, self.roomId, self.memberListbox, self.queue)
        main_part.get_room_thread(self.roomListbox)

    def button(self, event=None):
        message = self.Entry.get()
        main_part.post_message(self.roomId, message, self.Entry, self.root)

    def get_rooms_thread(self):
        room_thread = threading.Thread(target=self.get_rooms)
        room_thread.setDaemon(True)
        room_thread.start()

    def get_rooms(self):
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://drrr.com/lounge',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': '__cfduid=d0f2d37f03823a2fce2f58a60c43218c61547450103;drrr-session-1=q57dhbunjsjq5a0st60ulvmf17'
        }
        roomUrl = 'https://drrr.com/lounge?api=json'
        response = requests.get(url=roomUrl, headers=headers).text
        self.roomInfos = json.loads(response)['rooms']

        roomNames = [roomInfo['name'] for roomInfo in self.roomInfos
                     if roomInfo['language'] == 'zh-CN' and roomInfo['limit'] != roomInfo['total']]

        try:
            self.roomChooseEntry['values'] = roomNames
        except:
            pass

    def get_users_thread(self):
        user_thread = threading.Thread(target=self.get_users)
        user_thread.setDaemon(True)
        user_thread.start()

    def get_users(self):
        with open('./users.txt', 'a+') as f:
            f.seek(0)
            content = f.read()
            if content != '':
                self.names_list = json.loads(content)
                self.userNameEntry['values'] = self.names_list

    def save_users(self):
        if self.userName not in self.names_list:
            self.names_list.append(self.userName)
            with open('./users.txt', 'w+') as f:
                f.write(json.dumps(self.names_list))

    def join_new_room(self, event=None):
        value = self.roomListbox.get(self.roomListbox.curselection()[0])
        roomName = re.search('<(.*?)  (\d/\d)>', value).group(1)
        join_header = {
            'Host': 'drrr.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://drrr.com/lounge/',
        }
        room = self.session.get('https://drrr.com/lounge?api=json', headers=join_header)
        room_id = None
        rooms = json.loads(room.text)['rooms']
        for room in rooms:
            if room['name'] == roomName:
                room_id = room['roomId']

        if room_id:
            data = {
                'message': '/leave',
                'url': '',
                'to': '',
            }
            session_headers = {
                'authority': 'drrr.com',
                'method': 'POST',
                'path': '/room/?ajax=1',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://drrr.com',
                'referer': None,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            post_message_url = 'https://drrr.com/room/?ajax=1'
            while True:
                response = self.session.post(url=post_message_url, headers=session_headers, data=data)
                if response.status_code == 200:
                    break
                time.sleep(2)


            main_part.join(room_id)
            self.queue.put_nowait('stop')
            self.root.title(roomName)
            main_part.get_message_thread(self.userName, self.getMessageText, room_id, self.memberListbox, self.queue)
        else:
            tkinter.messagebox.showerror('错误',  '房间名不存在')

    def create_room_thread(self, event=None):
        threading.Thread(target=self.create_room).start()

    def create_room(self):
        create_root = tk.Tk()
        create_root.geometry("330x216+525+285")
        create_root.title("创建房间")
        create_root.iconbitmap('./drrr.ico')
        create_root.configure(background="#000000")

        roomName = tk.StringVar()
        roomNameEntry = tk.Entry(create_root, textvariable=roomName)
        roomNameEntry.place(relx=0.258, rely=0.278, height=23, relwidth=0.467)
        roomNameEntry.configure(background="white",
                                disabledforeground="#a3a3a3",
                                font="TkFixedFont",
                                foreground="#000000",
                                insertbackground="black",
                                width=154,)

        count = tk.StringVar()
        countCombobox = ttk.Combobox(create_root, textvariable=count)
        countCombobox.place(relx=0.258, rely=0.648, relheight=0.106, relwidth=0.467)
        countCombobox['values'] = [i for i in range(2,21)]

        music = tk.IntVar()
        musicCheckbutton = tk.Checkbutton(create_root, variable=music,)
        musicCheckbutton.place(relx=0.773, rely=0.255, relheight=0.125, relwidth=0.194)
        musicCheckbutton.configure(activebackground="#000000",
                                   activeforeground="#ffffff",
                                   background="#000000",
                                   disabledforeground="#000000",
                                   foreground="#ffffff",
                                   highlightbackground="#000000",
                                   highlightcolor="black",
                                   selectcolor='black',
                                   justify='left',
                                   text='''音乐房''', )

        adult = tk.IntVar()
        adultCheckbutton = tk.Checkbutton(create_root, variable=adult,)
        adultCheckbutton.place(relx=0.773, rely=0.463, relheight=0.125, relwidth=0.194)
        adultCheckbutton.configure(activebackground="#000000",
                                   activeforeground="#ffffff",
                                   background="#000000",
                                   disabledforeground="#000000",
                                   foreground="#ffffff",
                                   highlightbackground="#000000",
                                   highlightcolor="black",
                                   selectcolor='black',
                                   justify='left',
                                   text='''成人室''', )

        hidden = tk.IntVar()
        hiddenCheckbutton = tk.Checkbutton(create_root, variable=hidden)
        hiddenCheckbutton.place(relx=0.773, rely=0.648, relheight=0.125, relwidth=0.23)
        hiddenCheckbutton.configure(activebackground="#000000",
                                    activeforeground="#ffffff",
                                    background="#000000",
                                    disabledforeground="#000000",
                                    foreground="#ffffff",
                                    highlightbackground="#000000",
                                    highlightcolor="black",
                                    selectcolor='black',
                                    justify='left',
                                    text='''隐藏房间''', )


        roomNameLabel = tk.Label(create_root)
        roomNameLabel.place(relx=0.061, rely=0.255, height=23, width=54)
        roomNameLabel.configure(background="#000000",
                                disabledforeground="#a3a3a3",
                                foreground="#ffffff",
                                text='''房间名称''')

        descriptionLabel = tk.Label(create_root)
        descriptionLabel.place(relx=0.061, rely=0.486, height=23, width=54)
        descriptionLabel.configure(background="#000000",
                                   disabledforeground="#a3a3a3",
                                   foreground="#ffffff",
                                   text='''房间描述''',)

        countLabel = tk.Label(create_root)
        countLabel.place(relx=0.061, rely=0.648, height=23, width=54)
        countLabel.configure(background="#000000",
                             disabledforeground="#a3a3a3",
                             foreground="#ffffff",
                             text='''成员人数''',)

        createButton = tk.Button(create_root, command=lambda: self.create_room_(roomName=roomNameEntry.get(),
                                                                               description=descriptionEntry.get(),
                                                                               limit=countCombobox.get(),
                                                                               language='zh-CN',
                                                                               music=music.get(),
                                                                               root=create_root))
        createButton.place(relx=0.409, rely=0.833, height=28, width=49)
        createButton.configure(activebackground="#ececec",
                               activeforeground="#000000",
                               background="#000000",
                               disabledforeground="#a3a3a3",
                               foreground="#ffffff",
                               highlightbackground="#d9d9d9",
                               highlightcolor="black",
                               pady="0",
                               relief='groove',
                               text='''创建''',)


        descriptionEntry = tk.Entry(create_root)
        descriptionEntry.place(relx=0.258, rely=0.463, height=23, relwidth=0.467)
        descriptionEntry.configure(background="white",
                                   disabledforeground="#a3a3a3",
                                   font="TkFixedFont",
                                   foreground="#000000",
                                   highlightbackground="#d9d9d9",
                                   highlightcolor="black",
                                   insertbackground="black",
                                   selectbackground="#c4c4c4",
                                   selectforeground="black",)

        font9 = "-family {Microsoft YaHei UI} -size 11 -weight bold " \
                "-slant roman -underline 0 -overstrike 0"
        createLabel = tk.Label(create_root)
        createLabel.place(relx=0.379, rely=0.069, height=25, width=76)
        createLabel.configure(background="#000000",
                              disabledforeground="#a3a3a3",
                              font=font9,
                              foreground="#ffffff",
                              text='''DOLLARS''', )

        create_root.mainloop()


    def create_room_(self, roomName, description, limit, language, music, root):
        data = {
            'message': '/leave',
            'url': '',
            'to': '',
        }
        session_headers = {
            'authority': 'drrr.com',
            'method': 'POST',
            'path': '/room/?ajax=1',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://drrr.com',
            'referer': None,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        post_message_url = 'https://drrr.com/room/?ajax=1'
        while True:
            response = self.session.post(url=post_message_url, headers=session_headers, data=data)
            if response.status_code == 200:
                break
            time.sleep(2)

        main_part.create_room(name=roomName,
                              description=description,
                              limit=limit,
                              language=language,
                              music=music)

        data = {
            'name': roomName,
            'description': description,
            'limit': limit,
            'language': language,
            'submit': '创建房间'
        }
        if music == 1 :
            music = 'true'
            data.update({'music': music})
        create_headers = {
            'authority': 'drrr.com',
            'method': 'POST',
            'path': '/create_room/?',
            'scheme': 'https',
            'cache - control': 'max - age = 0',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://drrr.com',
            'referer': 'https://drrr.com/create_room/?',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        create_url = 'https://drrr.com/create_room/?'
        response = self.session.post(url=create_url, data=data, headers=create_headers, allow_redirects=False)
        if response.status_code == 302:
            url = 'https://drrr.com/room/'
            join_headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'https://drrr.com/lounge',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            response = self.session.get(url, headers=join_headers).text
            room_id = re.search('data-url=".*id=(.*?)"', response).group(1)
            self.queue.put_nowait('stop')
            self.root.title(roomName)
            root.destroy()
            main_part.get_message_thread(self.userName, self.getMessageText, room_id, self.memberListbox, self.queue)
        else:
            tk.messagebox.showerror('错误', '房间名已存在')