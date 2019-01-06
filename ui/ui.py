from tkinter import *
from tkinter import messagebox

class MainWindow(object):
	"""UI类"""
	def __init__(self):
		'''初始化'''
		self.window = Tk()

	def setup(self):
		"""主界面参数配置"""
		self.window.title("PostBuild(开发版) kanwairen")
		self.window.geometry('500x200')                 #是x 不是*
		self.window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 报文显示
		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=19)
		self.msgtable_pathname_display = Label(self.window, text="如无报文可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.msgtable_pathname_display.place(x=80, y=19)

		self.msgtable_select_buntton = Button(self.window, text="选择报文表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_msgtable)
		self.msgtable_select_buntton.place(x=400, y=20)

		# 信号显示
		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=59)
		self.signaltable_pathname_display = Label(self.window, text="如无信号可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.signaltable_pathname_display.place(x=80, y=59)

		self.signaltable_select_buntton = Button(self.window, text="选择信号表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_signaltable)
		self.signaltable_select_buntton.place(x=400, y=60)

		# hex显示
		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=99)
		self.hex_pathname_display = Label(self.window, text="如不操作hex可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.hex_pathname_display.place(x=80, y=99)

		self.hex_select_buntton = Button(self.window, text="选择源HEX", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_hex)
		self.hex_select_buntton.place(x=400, y=100)

		# 运行
		self.run = Button(self.window, text="运行", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.run)
		self.run.place(x=100, y=150)
		# 退出
		self.exit = Button(self.window, text="退出", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.exit)
		self.exit.place(x=200, y=150)
		# 帮助
		self.help = Button(self.window, text="帮助", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.help)
		self.help.place(x=300, y=150)


	def show(self):
		'''主界面显示'''
		self.window.mainloop()

class RegWindow(object):
	'''注册窗口'''
	def regwin_setup(self):
		self.reg_window = Toplevel()
		self.reg_window.title('注册')
		self.reg_window.geometry('500x200')
		self.reg_window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 注册码输入
		Label(self.reg_window, text="输入注册码:", font=("Arial", 10), width=13, height=3).place(x=10, y=20)
		self.reg_code = StringVar()
		self.regist_code_input = Entry(self.reg_window, textvariable=self.reg_code, bg="white", font=("Arial", 10), width=50)
		# self.reg_code.set("haha")
		self.regist_code_input.place(x=100, y=33)

		Label(self.reg_window, text="（请将下方显示的机器码发送至 wangcq714@163.com 获取注册码）", font=("Arial", 10), width=58, height=2).place(x=10, y=60)

		# 机器码显示
		Label(self.reg_window, text="机器码显示:", font=("Arial", 10), width=13, height=3).place(x=10, y=100)
		self.mac_code = StringVar()
		self.machine_code_display = Entry(self.reg_window, textvariable=self.mac_code, state="readonly", bg="white", font=("Arial", 10), width=50)
		# self.mac_code.set("jiqima")
		self.mac_code_display()
		self.machine_code_display.place(x=100, y=113)
		
		# 确定
		self.confirm = Button(self.reg_window, text="注册", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.regwin_regit)
		self.confirm.place(x=150, y=150)
		# 返回
		self.back = Button(self.reg_window, text="返回", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.regwin_back)
		self.back.place(x=300, y=150)




class MyWindow(MainWindow, RegWindow):
	"""UI"""
	def __init__(self, msgRoute, signalRoute, readHex, reg, run):
		super().__init__()
		self.msgRoute = msgRoute
		self.signalRoute = signalRoute
		self.readHex = readHex
		self.reg = reg
		self.ui_run = run

	def run(self):
		'''主界面运行按钮回调函数'''
		self.ui_run(self.msgRoute, self.signalRoute, self.readHex)
		messagebox.showinfo(title='提示', message='运行结束')

	def exit(self):
		'''主界面退出按钮回调函数'''
		self.window.quit()

	def help(self):
		'''主界面帮助按钮回调函数'''
		ret = messagebox.askquestion(title='Help', message='这么简单还需要帮助？！！！')
		if ret == "yes":
			messagebox.showinfo(title='Help', message='哈哈哈 逗你呢 并没有什么帮助')

	def select_msgtable(self):
		'''主界面选择报文表按钮回调函数'''
		self.msgRoute.get_file_pathname()
		# 如选择文件不为空字符串，修改Label显示内容；否则回至初始化显示状态
		if self.msgRoute.pathName != "":
			self.msgtable_pathname_display["text"] = self.msgRoute.pathName
			self.msgtable_pathname_display["anchor"] = W
		else:
			self.msgtable_pathname_display["text"] = "如无报文可不选"
			self.msgtable_pathname_display["anchor"] = "center"

	def select_signaltable(self):
		'''主界面选择信号表按钮回调函数'''
		self.signalRoute.get_file_pathname()
		# 如选择文件不为空字符串，修改Label显示内容；否则回至初始化显示状态
		if self.signalRoute.pathName != "":
			self.signaltable_pathname_display["text"] = self.signalRoute.pathName
			self.signaltable_pathname_display["anchor"] = W
		else:
			self.signaltable_pathname_display["text"] = "如无信号可不选"
			self.signaltable_pathname_display["anchor"] = "center"

	def select_hex(self):
		'''主界面选择源hex按钮回调函数'''
		ret = self.reg.checkAuthored()
		if ret == 0:
			self.readHex.get_file_pathname()
			# 如选择文件不为空字符串，修改Label显示内容；否则回至初始化显示状态
			if self.readHex.pathName != "":
				self.hex_pathname_display["text"] = self.readHex.pathName
				self.hex_pathname_display["anchor"] = W
			else:
				self.hex_pathname_display["text"] = "如不操作hex可不选"
				self.hex_pathname_display["anchor"] = "center"
		else:
			ret = messagebox.askquestion(title='提示', message='您没有注册，需注册后才可使用！！！\n是否注册？')
			if ret == "yes":
				try:
					if hasattr(self, "reg_window"):
						messagebox.showinfo(title='提示', message='注册窗口已打开，请勿重复操作！')
					else:
						self.regwin_setup()
				except AttributeError:
					pass

	def mac_code_display(self):
		mac_info = self.reg.getmachinecode()
		self.mac_code.set(mac_info)

	def regwin_regit(self):
		'''注册界面注册按钮回调函数'''
		reg_code = self.regist_code_input.get()
		if self.reg.checkAuthored() != 0:
			ret = self.reg.regist(reg_code)
			if ret == 0:
				messagebox.showinfo(title='提示', message='恭喜，注册成功！')
			elif ret == 1:
				messagebox.showinfo(title='提示', message='注册码错误，请输入正确的注册码！')
			elif ret == 2:
				messagebox.showinfo(title='提示', message='获取机器码错误！')
			elif ret == 3:
				messagebox.showinfo(title='提示', message='请输入注册码！')
		else:
			messagebox.showinfo(title='提示', message='您已注册！！！')

	def regwin_back(self):
		'''注册界面返回按钮回调函数'''
		self.reg_window.destroy()
		del(self.reg_window)


if __name__ == '__main__':
	pass



