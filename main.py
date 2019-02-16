# -- coding: utf-8 --
from tkinter import *
from LoginPage import *


root = Tk()
root.title('drrr')
root.resizable(0, 0)
root.geometry("255x255+561+268")
root.configure(background='#000000')
root.iconbitmap('./drrr.ico')
LoginPage(root)
root.mainloop()