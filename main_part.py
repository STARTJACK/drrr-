# -- coding: utf-8 --
import requests
import time
import re
import json
import copy
import threading
import tkinter
import tkinter.messagebox

login_header = {
        'Host': 'drrr.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
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
login_url = 'https://drrr.com/'
post_message_url = 'https://drrr.com/room/?ajax=1'
get_message_url = 'https://drrr.com/json.php?fast=1'
update_message_url = 'https://drrr.com/json.php?update=%s'
create_url = 'https://drrr.com/create_room/?'
session = requests.Session()

# 登陆
def login(user_name, room_name, roomInfos):
    id = user_name  # input("输入昵称: ")
    session.get(login_url, headers=login_header)
    response = session.get(login_url, headers=login_header, allow_redirects=False)
    token = re.search('name="token" data-value="(.*?)"', response.text).group(1)
    data = {
        'name': '%s' % id,
        'login': 'ENTER',
        'token': token,
        'direct-join': '',
        'language': 'zh-CN',
        'icon': 'zaika-2x',
    }
    session.post(login_url, headers=login_header, data=data)
    room_id = None
    for room in roomInfos:
        if room['name'] == room_name:
            room_id = room['roomId']
    # room_id = lounge(room_name)
    if not room_id:
        room_id = create_room(room_name)
        # room_id = lounge(room_name)
    else:
        room_name, room_id = join(room_id)
    return room_name, room_id, session

# 大厅
def lounge(name):
    lounge_url = 'https://drrr.com/lounge/'
    login_header.update({'Referer': 'https://drrr.com/'})
    session.get(lounge_url, headers=login_header)
    login_header.update({'Referer': 'https://drrr.com/lounge/'})
    room = session.get('https://drrr.com/lounge?api=json', headers=login_header)
    try:
        rooms = json.loads(room.text)['rooms']
        for room in rooms:
            if room['name'] == name:
                room_id = room['roomId']
                return room_id
    except Exception as e:
        print(str(e))

# 创建房间
def create_room(name, description='', limit=10, language='zh-CN', music='true'):
    data = {
        'name': name,
        'description': description,
        'limit': limit,
        'language': language,
        'submit': '创建房间'
    }
    if music == 1 or music == 'true':
        music = 'true'
        data.update({'music': music})
    create_headers = copy.deepcopy(session_headers)
    create_headers.update({'referer': 'https://drrr.com/create_room/?',
                           'path': '/create_room/?',
                           'cache - control': 'max - age = 0',
                           'accept-encoding':   None})
    session.post(url=create_url, data=data, headers=create_headers)
    url = 'https://drrr.com/room/'
    join_headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://drrr.com/lounge',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    session.get(url, headers=join_headers)
    return True

# 加入房间
def join(room_id):
    join_headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://drrr.com/lounge',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    join_room_url = 'https://drrr.com/room/?id=%s' % room_id
    response = session.get(url=join_room_url, headers=join_headers, allow_redirects=True)
    if 'zh-CN' in response.text:
        room_name = re.search('data-title="I\'m in “(.*?)”', response.text).group(1)
        room_id = re.search('data-url=".*id=(.*?)"', response.text).group(1)
        return room_name, room_id
    else:
        tkinter.messagebox.showerror(title="warning", message='已有相同用户名存在，请使用其他名称')
        session.cookies = requests.utils.cookiejar_from_dict({'cookies': None}, cookiejar=None, overwrite=True)
        return None, None

# 发送信息
def post_message(room_id, message, Entry, root, event=None):
    session_headers.update({'referer': 'https://drrr.com/room/?id=%s' % room_id,
                            'method': 'POST'})
    if message == '/leave':
        leave()
        root.destroy()
    else:
        while True:
            global users
            mslist = message.split("  ")
            to = ''
            if '/to' in mslist[0]:
                message = mslist[2]
                to_name = mslist[1]
                for user in users:
                    if to_name == user['name']:
                        to = user['id']
            data = {
                'message': message,
                'url': '',
                'to': to,
            }
            if '/host' in mslist[0]:
                host_name = mslist[1]
                for user in users:
                    if host_name == user['name']:
                        data = {'new_host': user['id']}
            elif '/kick' in mslist[0]:
                try:
                    kick_name = mslist[1]
                    for user in users:
                        if kick_name == user['name']:
                            data = {'kick': user['id']}
                except: pass
            elif '/music' in mslist[0]:
                try:
                    music_name = mslist[1]
                    music_url = mslist[2]
                    data = {
                        'music': 'music',
                        'name': music_name,
                        'url': music_url
                    }
                except: pass
            response = session.post(url=post_message_url, headers=session_headers, data=data)
            if response.status_code == 200 or response.status_code == 500:
                break
    try:
        Entry.delete(0, tkinter.END)
    except: pass

# 离开
def leave():
    while True:
        data = {
            'message': '/leave',
            'url': '',
            'to': '',
        }
        response = session.post(url=post_message_url, headers=session_headers, data=data)
        if response.status_code == 200:
            break
        time.sleep(1)

first = 1
# 解析消息
def parse_message(messages, myname, Text, room_id, lb):
    messages = json.loads(messages.text)
    bold_font = "-family {Microsoft YaHei UI Light} -size 10 -weight " \
        "bold -slant roman -underline 0 -overstrike 0"
    font = "-family {Microsoft YaHei UI Light} -size 9 -weight "  \
        "normal -slant roman -underline 0 -overstrike 0"
    global first, users
    host = messages.get('host')
    if messages.get('talks'):
        for message in messages['talks']:
            try:
                name = message['user']['name']
            except:
                try:
                    name = message['from']['name']
                    id = message['from']['id']
                except:pass

            type = message['type']

            Text.configure(foreground='#ffffff')
            Text.configure(font=font)
            if type == 'message':
                if message.get('to'):
                    Text.tag_config('private', font=bold_font, foreground='blue')
                    Text.insert(tkinter.END, name, 'private')
                    #threading.Thread(target=lambda :tkinter.messagebox.showinfo(title='来自%s的私信' % name, message=message['message'])).start()
                    # tkinter.messagebox.showinfo(title='来自%s的私信' % name, message=message['message'])
                    if myname != name and first == 0:
                        threading.Thread(target=private_show, args=(message, name, room_id, id)).start()
                elif myname != name:
                    Text.tag_config('name', font=bold_font, foreground='red')
                    Text.insert(tkinter.END, name, 'name')

                else:
                    Text.tag_config('me', font=bold_font, foreground='yellow')
                    Text.insert(tkinter.END, name, 'me')
                Text.configure(font=font)
                content = ': ' + message['message'] + '\n\n'
                Text.insert(tkinter.END, content)

            elif type == 'me':
                content = '                      ✦' + name + ' ' + message['content'] + '\n\n'
                Text.insert(tkinter.END, content)
            elif type == 'roll':
                content = '                      ✦' + name + ' 摇到了 ' +message['to']['name'] + '\n\n'
                Text.insert(tkinter.END, content)
            elif type == 'join':
                content = '                      ✦' + name+' logged in.' + '\n\n'
                Text.insert(tkinter.END, content)
                if not first:
                    users = messages['users']
                    updatelst(lb, host=host)

            elif type == 'leave':
                content = '                      ✦' + name + ' ' + message['message'][4:] + '\n\n'
                Text.insert(tkinter.END, content)
                if not first:
                    users = messages['users']
                    updatelst(lb, host=None)
            elif type == 'new-host':
                content = '                      ✦' + name + ' is a new host' + '\n\n'
                Text.insert(tkinter.END, content)
                if not first:
                    users = messages['users']
                    updatelst(lb, host=host)
            elif type == 'music':
                content = '                      ✦' + name +' shared music「%s」'% message['music']['name'] + '\n\n'
                music_url = message['music']['url']
                Text.insert(tkinter.END, content)
                threading.Thread(target=play_music, args=(music_url,message['music']['name'])).start()

            elif type == 'kick':
                name = message['to']['name']
                content = '                      ✦' + name + ' lost the connection' + '\n\n'
                Text.insert(tkinter.END, content)
                if not first:
                    users = messages['users']
                    updatelst(lb, host=host)

            Text.see(tkinter.END)
        first = 0



def private_show(message, name, room_id, id):

    top = tkinter.Tk()
    top.geometry("322x271+526+349")
    top.title("来自%s的私信" % name)

    privateFrame = tkinter.Frame(top)
    privateFrame.place(relx=-0.031, rely=-0.037, relheight=1.089, relwidth=1.071)
    privateFrame.configure(relief='groove',
                           borderwidth="2",
                           background="#000000",
                           width=345,)

    privateText = tkinter.Text(privateFrame)
    privateText.place(relx=0.043, rely=0.068, relheight=0.685, relwidth=0.887)
    privateText.configure(background="#000000",
                          foreground="#ffffff",
                          highlightbackground="#d9d9d9",
                          highlightcolor="black",
                          insertbackground="black",
                          selectbackground="#c4c4c4",
                          selectforeground="black",
                          width=304,
                          wrap='word',)

    entry = tkinter.StringVar()
    privateEntry = tkinter.Entry(privateFrame, textvariable=entry)
    privateEntry.place(relx=0.043, rely=0.814, height=27, relwidth=0.742)
    privateEntry.configure(background="#000000",
                           disabledforeground="#a3a3a3",
                           font="TkFixedFont",
                           foreground="#ffffff",
                           insertbackground="#ffffff",
                           relief='groove',
                           width=314,)
    privateEntry.bind('<Return>', handleradaptor(private_post, message=privateEntry, id=id, room_id=room_id, root=top))

    privateButton = tkinter.Button(privateFrame, command=lambda: private_post(event=None, message=privateEntry, id=id, room_id=room_id, root=top))
    privateButton.place(relx=0.783, rely=0.814, height=28, width=55)
    privateButton.configure(activebackground="#ececec",
                            activeforeground="#000000",
                            background="#000000",
                            disabledforeground="#a3a3a3",
                            foreground="#ffffff",
                            highlightbackground="#d9d9d9",
                            highlightcolor="black",
                            pady="0",
                            text='''发送''',
                            width=59,)


    privateText.insert(tkinter.END, name + ":  " + message['message'] + '\n')
    top.mainloop()



def handleradaptor(fun, **kwds):
    '''事件处理函数的适配器，相当于中介'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def private_post(event, message, id, room_id, root, ):
    message = message.get()
    while True:
        data = {
            'message': message,
            'url': '',
            'to': id,
        }
        session_headers.update({'method': 'POST',
                                'referer': 'https://drrr.com/room/?id=%s' % room_id})
        response = session.post(url=post_message_url, headers=session_headers, data=data)
        if response.status_code == 200:
            break
    root.destroy()

flag = 0
# 获取信息

def get_message(id, Text, room_id, memberlb, queue):
    global message, flag, users
    headers = copy.deepcopy(session_headers)
    headers.update({'method': 'GET', 'path': '/json.php?fast=1', 'accept-encoding': None})
    while True:
        if not flag:
            try:
                message = session.get(get_message_url, headers=headers)
                parse_message(message, id, Text=Text, room_id=room_id, lb=memberlb)
                info = json.loads(message.text)
                users = info['users']
                host = info['host']
                updatelst(memberlb, host)
                flag = 1
            except: pass
        else:
            try:
                update = json.loads(message.text)['update']
                url = update_message_url % update
                message = session.get(url, headers=headers)
                parse_message(message, id, Text=Text, room_id=room_id, lb=memberlb)
            except: pass
        if not queue.empty():
            if queue.get_nowait() == 'stop':
                queue.task_done()
                Text.delete(0.0, tkinter.END)
                flag = 0
                break





def get_message_thread(id, Text, room_id, memberlb, queue):
    thread = threading.Thread(target=get_message, args=(id, Text, room_id, memberlb, queue))
    thread.setDaemon(True)
    thread.start()

users = []
message = ''
def updatelst(memberlb, host):
    memberlb.delete(0, len(users) + 1)
    for user in users:
        if user['id'] == host:
            memberlb.insert(tkinter.END, ('--host--<', user['name'], '>------------------'))
        else:
            memberlb.insert(tkinter.END, ('--------<', user['name'], '>------------------'))


def update_rooms(roomlb):
    roomlb.delete(0, len(rooms)+1)
    for room in rooms:
        try:
            if room['language'] == 'zh-CN':
                roomlb.insert(tkinter.END, ('<' + room['name']+'  %s/%s' % (room['total'], room['limit']) + '>------------------'))
        except:
            pass


# def get_room_thread(roomlb):
#
#     def get_rooms(roomlb):
#         global rooms
#         login_header.update({'Referer': 'https://drrr.com/lounge/'})
#         room = session.get('https://drrr.com/lounge?api=json', headers=login_header)
#         rooms = json.loads(room.text)['rooms']
#         update_rooms(roomlb)
#         timer = threading.Timer(5, get_rooms, args=(roomlb, ))
#         timer.setDaemon(True)
#         timer.start()
#
#     timer = threading.Timer(5, get_rooms, args=(roomlb,))
#     timer.setDaemon(True)
#     timer.start()



rooms = []
def get_room_thread(roomlb):
    def get_room(roomlb):
        global rooms
        login_header.update({'Referer': 'https://drrr.com/lounge/'})
        while True:
            room = session.get('https://drrr.com/lounge?api=json', headers=login_header)
            rooms = json.loads(room.text)['rooms']
            update_rooms(roomlb)
            time.sleep(5)
    room_thread = threading.Thread(target=get_room, args=(roomlb, ))
    room_thread.setDaemon(True)
    room_thread.start()

volume = 0
def play_music(music_url, music_name):
    answer = tkinter.messagebox.askquestion("播放音乐", "是否播放<%s>" % music_name )
    if answer == 'yes':
        global volume
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
        response = requests.get(url=music_url, headers=headers)
        with open('./mp3/%s.mp3' % music_name, 'wb+') as f:
            f.write(response.content)
        import minimu
        song = minimu.load('./mp3/%s.mp3' % music_name)
        volume = 20
        song.volume(volume)
        song.play()
        music_root = tkinter.Tk()
        music_root.geometry("322x47+162+348")
        music_root.title(music_name)
        music_root.resizable(0, 0)
        try:
            music_root.iconbitmap("./drrr.ico")
        except: pass
        music_root.configure(relief="groove")
        music_root.configure(background="#000000")
        playButton = tkinter.Button(music_root, command=lambda: resume(song))
        playButton.place(relx=0.031, rely=0.213, height=28, width=49)
        playButton.configure(activebackground="#ececec",
                             activeforeground="#000000",
                             background="#000000",
                             disabledforeground="#a3a3a3",
                             foreground="#ffffff",
                             highlightbackground="#d9d9d9",
                             highlightcolor="black",
                             pady="0",
                             relief='groove',
                             text='''恢复''',)
        pauseButton = tkinter.Button(music_root, command=lambda: pause(song))
        pauseButton.place(relx=0.248, rely=0.213, height=28, width=49)
        pauseButton.configure(activebackground="#ececec",
                              activeforeground="#000000",
                              background="#000000",
                              disabledforeground="#a3a3a3",
                              foreground="#ffffff",
                              highlightbackground="#d9d9d9",
                              highlightcolor="black",
                              pady="0",
                              relief='groove',
                              text='''暂停''',)
        stopButton = tkinter.Button(music_root, command=lambda: stop(song, music_root))
        stopButton.place(relx=0.466, rely=0.213, height=28, width=49)
        stopButton.configure(activebackground="#ececec",
                             activeforeground="#000000",
                             background="#000000",
                             disabledforeground="#a3a3a3",
                             foreground="#ffffff",
                             highlightbackground="#d9d9d9",
                             highlightcolor="black",
                             pady="0",
                             relief='groove',
                             text='''停止''',)
        renewButton = tkinter.Button(music_root, command=lambda: renew(song))
        renewButton.place(relx=0.683, rely=0.213, height=28, width=49)
        renewButton.configure(activebackground="#ececec",
                              activeforeground="#000000",
                              background="#000000",
                              disabledforeground="#a3a3a3",
                              foreground="#ffffff",
                              highlightbackground="#d9d9d9",
                              highlightcolor="black",
                              pady="0",
                              relief='groove',
                              text='''重放''',)
        upButton = tkinter.Button(music_root, command=lambda: volume_up(song, volume))
        upButton.place(relx=0.885, rely=0.213, height=15, width=25)
        upButton.configure(activebackground="#ececec",
                           activeforeground="#000000",
                           background="#000000",
                           disabledforeground="#a3a3a3",
                           foreground="#ffffff",
                           highlightbackground="#d9d9d9",
                           highlightcolor="black",
                           pady="0",
                           relief='groove',
                           width=39,
                           text='''+''',)
        downButton = tkinter.Button(music_root, command=lambda: volume_down(song, volume))
        downButton.place(relx=0.885, rely=0.5, height=15, width=25)
        downButton.configure(activebackground="#ececec",
                             activeforeground="#000000",
                             background="#000000",
                             disabledforeground="#a3a3a3",
                             foreground="#ffffff",
                             highlightbackground="#d9d9d9",
                             highlightcolor="black",
                             pady="0",
                             relief='groove',
                             width=20,
                             text='''-''',)
        music_root.mainloop()

def resume(song):
    song.resume()

def pause(song):
    song.pause()

def stop(song, music_root):
    song.stop()
    music_root.destroy()

def renew(song):
    song.stop()
    song.play()

def volume_up(song, vol):
    global volume
    if volume < 100:
        vol += 5
        volume = vol
        song.volume(volume)

def volume_down(song, vol):
    global volume
    if vol > 0:
        vol -= 5
        volume = vol
        song.volume(volume)
