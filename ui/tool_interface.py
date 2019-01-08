from tkinter import Toplevel, Label, Button, StringVar, Entry, W
from tkinter import messagebox

class BoxWindow(object):
	'''工具窗口'''
	def __init__(self):
		'''初始化'''
		self.box_window = Toplevel()

	def boxwin_setup(self):
		self.box_window.title("Tool")
		self.box_window.geometry('550x350')                 #是x 不是*
		self.box_window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 报文显示
		Label(self.box_window, text="Current File:", font=("Times", 10), width=10, height=2).place(x=10, y=20)
		self.msgtable_pathname_display = Label(self.box_window, text="请选择 <xxx_路由表提取>", bg="white", font=("楷体", 9), width=56, height=2)
		self.msgtable_pathname_display.place(x=90, y=22)

		self.msgtable_select_buntton = Button(self.box_window, text="选择路由表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2)
		self.msgtable_select_buntton.place(x=450, y=20)

		# PostBuild报文表
		self.signaltable_select_buntton = Button(self.box_window, text="PostBuild报文表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.signaltable_select_buntton.place(x=100, y=80)

		# PostBuild信号表
		self.hex_select_buntton = Button(self.box_window, text="PostBuild信号表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.hex_select_buntton.place(x=300, y=80)

		# DTC配置表
		self.signaltable_select_buntton = Button(self.box_window, text="DTC配置表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.signaltable_select_buntton.place(x=100, y=140)

		# 节点使能配置表
		self.hex_select_buntton = Button(self.box_window, text="节点使能配置表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.hex_select_buntton.place(x=300, y=140)

		# DTC配置表
		self.signaltable_select_buntton = Button(self.box_window, text="诊断请求表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.signaltable_select_buntton.place(x=100, y=200)

		# 节点使能配置表
		self.hex_select_buntton = Button(self.box_window, text="诊断响应表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2)
		self.hex_select_buntton.place(x=300, y=200)

		# 帮助
		self.help = Button(self.box_window, text="帮助", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2)
		self.help.place(x=120, y=280)
		# 退出
		self.exit = Button(self.box_window, text="退出", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2)
		self.exit.place(x=325, y=280)
		# 
		# self.help = Button(self.box_window, text="帮助", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2)
		# self.help.place(x=350, y=260)
