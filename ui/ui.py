from tkinter import Tk, Toplevel, Label, Button, StringVar, Entry, W
from tkinter import messagebox, ttk, PhotoImage
from ui import tool_interface

class MainWindow(object):
	"""UI类"""
	def __init__(self):
		'''初始化'''
		self.window = Tk()

	def setup(self):
		"""主界面参数配置"""
		if self.config.user_type == "Customer":
			self.window.title("PostBuildTool(客户版)  Kanwairen")
		elif self.config.user_type == "Developer":
			self.window.title("PostBuildTool(开发版)  Kanwairen")
		self.window.geometry('580x340')                 #是x 不是*
		self.window.iconbitmap("image/icon.ico")
		self.window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		if self.config.user_type == "Developer":
			# 创建一个适用平台下拉列表
			self.apply_platform_val = StringVar()#窗体自带的文本，新建一个值
			self.apply_platform = ttk.Combobox(self.window, textvariable=self.apply_platform_val, width=54, state='readonly')
			self.apply_platform["values"]=("选择平台","GAW1.2_NewPlatform","GAW1.2_OldPlatform","Qoros_C6M0")  
			self.apply_platform.current(0)  #选择第一个  
			self.apply_platform.bind("<<ComboboxSelected>>", self.select_apply_platform)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
			self.apply_platform.place(x=91, y=15)
			# print(self.apply_platform.get())

		# 报文显示
		Label(self.window, text="报文表", font=("楷体", 10), width=8, height=2).place(x=20, y=50)
		self.msgtable_pathname_display = Label(self.window, text="如无报文可不选", bg="white", font=("楷体", 9), width=66, height=2)
		self.msgtable_pathname_display.place(x=90, y=52)
		self.openfileimg = PhotoImage(file='image/open.png')
		self.msgtable_select_buntton = Button(self.window,image=self.openfileimg, command=self.select_msgtable)
		# self.msgtable_select_buntton = Button(self.window, text="选择", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=8, height=2, command=self.select_msgtable)
		self.msgtable_select_buntton.place(x=510, y=51)

		# 信号显示
		Label(self.window, text="信号表", font=("楷体", 10), width=8, height=2).place(x=20, y=120)
		self.signaltable_pathname_display = Label(self.window, text="如无信号可不选", bg="white", font=("楷体", 9), width=66, height=2)
		self.signaltable_pathname_display.place(x=90, y=122)

		self.signaltable_select_buntton = Button(self.window,image=self.openfileimg, command=self.select_signaltable)
		# self.signaltable_select_buntton = Button(self.window, text="选择", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=8, height=2, command=self.select_signaltable)
		self.signaltable_select_buntton.place(x=510, y=121)

		# hex显示
		Label(self.window, text="源hex", font=("楷体", 10), width=8, height=2).place(x=20, y=190)
		if self.config.user_type == "Customer":
			self.hex_pathname_display = Label(self.window, text="请选择源hex文件", bg="white", font=("楷体", 9), width=66, height=2)
		elif self.config.user_type == "Developer":
			self.hex_pathname_display = Label(self.window, text="如不操作hex可不选", bg="white", font=("楷体", 9), width=66, height=2)
		self.hex_pathname_display.place(x=90, y=192)

		self.hex_select_buntton = Button(self.window,image=self.openfileimg, command=self.select_hex)
		# self.hex_select_buntton = Button(self.window, text="选择", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=8, height=2, command=self.select_hex)
		self.hex_select_buntton.place(x=510, y=191)

		# 运行
		self.runimg = PhotoImage(file='image/run.png')
		self.run_button = Button(self.window, image=self.runimg, command=self.run)
		# self.run_button = Button(self.window, text="运行", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=10, height=2, command=self.run)
		self.run_button.place(x=90, y=260)
		# 绑定鼠标移入事件
		self.run_button.bind("<Enter>", self.enter_run_area)
		# 绑定鼠标移出事件
		self.run_button.bind("<Leave> ", self.leave_run_area)

		# 退出
		self.exitimg = PhotoImage(file='image/exit.png')
		self.exit_button = Button(self.window,image=self.exitimg, command=self.exit)
		# self.exit_button = Button(self.window, text="退出", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=10, height=2, command=self.exit)
		self.exit_button.place(x=210, y=260)
		# 绑定鼠标移入事件
		self.exit_button.bind("<Enter>", self.enter_exit_area)
		# 绑定鼠标移出事件
		self.exit_button.bind("<Leave> ", self.leave_exit_area)

		# 帮助
		self.helpimg = PhotoImage(file='image/help.png')
		self.help_button = Button(self.window,image=self.helpimg, command=self.help)
		# self.help_button = Button(self.window, text="帮助", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=10, height=2, command=self.help)
		self.help_button.place(x=330, y=260)
		# 绑定鼠标移入事件
		self.help_button.bind("<Enter>", self.enter_help_area)
		# 绑定鼠标移出事件
		self.help_button.bind("<Leave> ", self.leave_help_area)
		
		# 百宝箱
		self.toolimg = PhotoImage(file='image/tool.png')
		self.Doraemon_button = Button(self.window,image=self.toolimg, command=self.box)
		# self.Doraemon = Button(self.window, text="哆啦A梦", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 8), width=8, height=2, command=self.box)
		self.Doraemon_button.place(x=450, y=260)
		# 绑定鼠标移入事件
		self.Doraemon_button.bind("<Enter>", self.enter_doraemon_area)
		# 绑定鼠标移出事件
		self.Doraemon_button.bind("<Leave> ", self.leave_doraemon_area)

		# 鼠标悬浮提示
		self.pre_click_hint_val = StringVar()#窗体自带的文本，新建一个值
		self.pre_click_hint = Label(self.window, textvariable=self.pre_click_hint_val, font=("楷体", 8), width=8, height=1)
		self.pre_click_hint.place_forget()
		

	def show(self):
		'''主界面显示'''
		self.window.mainloop()


class RegWindow(object):
	'''注册窗口'''
	def regwin_setup(self):
		self.reg_window = Toplevel()
		self.reg_window.title('注册')
		self.reg_window.geometry('450x200')
		self.reg_window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 注册码输入
		Label(self.reg_window, text="注册码:", font=("楷体", 10), width=13, height=3).place(x=10, y=100)
		self.reg_code = StringVar()
		self.regist_code_input = Entry(self.reg_window, textvariable=self.reg_code, bg="white", font=("Times", 10), width=50)
		# self.reg_code.set("haha")
		self.regist_code_input.place(x=100, y=113)

		Label(self.reg_window, text="（请将机器码发送至 wangcq714@163.com 获取注册码）", font=("楷体", 10), width=58, height=2).place(x=10, y=60)

		# 机器码显示
		Label(self.reg_window, text="机器码:", font=("楷体", 10), width=13, height=3).place(x=10, y=20)
		self.mac_code = StringVar()
		self.machine_code_display = Entry(self.reg_window, textvariable=self.mac_code, state="readonly", bg="white", font=("Times", 10), width=50)
		# self.mac_code.set("jiqima")
		self.mac_code_display()
		self.machine_code_display.place(x=100, y=33)
		
		# 确定
		self.confirm = Button(self.reg_window, text="注册", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=8, height=1, command=self.regwin_regit)
		self.confirm.place(x=150, y=155)
		# 返回
		self.back = Button(self.reg_window, text="返回", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=8, height=1, command=self.regwin_back)
		self.back.place(x=270, y=155)

	def close_win_callback(self):
		'''点击X关闭窗口回调函数'''
		self.reg_window.destroy()
		del(self.reg_window)


class MyWindow(MainWindow, RegWindow):
	"""UI"""
	def __init__(self, config, msgRoute, signalRoute, readHex, reg, run):
		super().__init__()
		self.paltform = "选择平台"
		self.config = config
		self.msgRoute = msgRoute
		self.signalRoute = signalRoute
		self.readHex = readHex
		self.reg = reg
		self.ui_run = run
		# self.user_type = user_type
		# self.user_type = config.user_type

	def select_apply_platform(self, *args):
		'''选择适用对象'''
		self.paltform = self.apply_platform.get()
		# print(self.paltform)

	def run(self):
		'''主界面运行按钮回调函数'''
		try:
			# 当用户为客户时，必须选择源hex文件（客户版）
			if self.config.user_type == "Customer" and self.readHex.pathName == "":
				messagebox.showinfo(title='提示', message='请选择源hex文件！')
			else:
				if self.config.user_type == "Developer":
					if self.paltform != "选择平台":
						self.config.platInfo = self.paltform
					else:
						messagebox.showinfo(title='提示', message='请选择应用平台')
						return

				ret = self.ui_run(self.config, self.msgRoute, self.signalRoute, self.readHex)
				if ret == "Success":
					messagebox.showinfo(title='提示', message='运行结束')
				elif ret == "DecryptionError":
					messagebox.showinfo(title='提示', message='Hex解密错误，请选择正确的加密Hex文件')
				else:
					messagebox.showinfo(title='提示', message='{} 第 {} 行，第 {} 列出错：{}'.format(ret[0], ret[1], ret[2], ret[3]))
		except:
			messagebox.showinfo(title='提示', message='运行出错，请检查需求表！！！')

	def enter_run_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("运行")
		self.pre_click_hint.place(x=90, y=240)

	def leave_run_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

	def exit(self):
		'''主界面退出按钮回调函数'''
		self.window.quit()

	def enter_exit_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("退出")
		self.pre_click_hint.place(x=210, y=240)

	def leave_exit_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

	def help(self):
		'''主界面帮助按钮回调函数'''
		ret = messagebox.askquestion(title='Help', message='这么简单还需要帮助？！！！')
		if ret == "yes":
			messagebox.showinfo(title='Help', message='哈哈哈 逗你呢 并没有什么帮助')

	def enter_help_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("帮助")
		self.pre_click_hint.place(x=330, y=240)

	def leave_help_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

	def box(self):
		'''主界面百宝箱按钮回调函数'''
		if not hasattr(self, "tool_if"):
			if self.config.user_type == "Developer":
					if self.paltform != "选择平台":
						self.config.platInfo = self.paltform
					else:
						messagebox.showinfo(title='提示', message='请选择应用平台')
						return
			self.tool_if = tool_interface.BoxWindow(self, self.config)
			self.tool_if.boxwin_setup()
			self.tool_if.box_window.protocol("WM_DELETE_WINDOW", self.tool_if.close_win_callback)
		else:
			messagebox.showinfo(title='Help', message='百宝袋已打开！')

	def enter_doraemon_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("哆啦A梦")
		self.pre_click_hint.place(x=450, y=240)

	def leave_doraemon_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

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
				if self.user_type == "Customer":
					self.hex_pathname_display["text"] = "请选择源hex文件"
				elif self.user_type == "Developer":
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
						self.reg_window.protocol("WM_DELETE_WINDOW", self.close_win_callback)
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



