from tkinter import Toplevel, Label, Button, StringVar, Entry, W
from tkinter import messagebox, ttk, PhotoImage, Radiobutton, IntVar
from tool import public4all
from tool import sig2pbsig, msg2pbmsg, diagreqmsgcfg, dtccfg, msgnode, diagmsgcfg, checkerror

class BoxWindow(object):
	'''工具窗口'''
	def __init__(self, main_window, config):
		'''初始化'''
		self.box_window = Toplevel()
		self.main_window = main_window
		self.config = config

	def boxwin_setup(self):
		self.box_window.title("百宝袋")
		if self.config.user_type == "Customer":
			self.box_window.geometry('550x210')                 #是x 不是*
		elif self.config.user_type == "Developer":
			self.box_window.geometry('550x350')
		self.box_window.iconbitmap("image/icon1.ico")
		self.box_window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 报文显示
		# Label(self.box_window, text="Current File:", font=("Times", 10), width=10, height=2).place(x=10, y=20)
		Label(self.box_window, text="路由表", font=("楷体", 10), width=10, height=2).place(x=10, y=20)
		self.routetable_pathname_display = Label(self.box_window, text="请选择 <xxx_路由表提取>", bg="white", font=("楷体", 9), width=60, height=2)
		self.routetable_pathname_display.place(x=90, y=22)

		self.openfileimg = PhotoImage(file='image/open.png')
		self.routetable_select_buntton = Button(self.box_window,image=self.openfileimg, command=self.select_route_table_callback)
		# self.routetable_select_buntton = Button(self.box_window, text="选择路由表", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.select_route_table_callback)
		self.routetable_select_buntton.place(x=480, y=22)

		# # PostBuild报文表
		# self.msgtable_buntton = Button(self.box_window, text="PostBuild报文表", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.postbuild_msg_table_callback)
		# self.msgtable_buntton.place(x=100, y=80)

		# # PostBuild信号表
		# self.signal_buntton = Button(self.box_window, text="PostBuild报文表", bg="lightgreen", activebackground="gold", \
		# 										fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.postbuild_sig_table_callback)
		# self.signal_buntton.place(x=300, y=80)

		# if self.config.user_type == "Developer":
		# 	# DTC配置表
		# 	self.dtc_config_buntton = Button(self.box_window, text="DTC配置表", bg="lightgreen", activebackground="gold", \
		# 											fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.dtc_cfg_table_callback)
		# 	self.dtc_config_buntton.place(x=100, y=140)

		# 	# 节点使能配置表
		# 	self.node_enable_buntton = Button(self.box_window, text="节点使能配置表", bg="lightgreen", activebackground="gold", \
		# 											fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.node_en_cfg_table_callback)
		# 	self.node_enable_buntton.place(x=300, y=140)

		# 	# 诊断请求
		# 	self.diag_req_buntton = Button(self.box_window, text="诊断请求表", bg="lightgreen", activebackground="gold", \
		# 											fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.diag_req_table_callback)
		# 	self.diag_req_buntton.place(x=100, y=200)

		# 	# 诊断响应
		# 	self.diag_res_buntton = Button(self.box_window, text="诊断响应表", bg="lightgreen", activebackground="gold", \
		# 											fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.diag_res_table_callback)
		# 	self.diag_res_buntton.place(x=300, y=200)

		self.radio_var = IntVar()
		self.radio_var.set(1)
		self.msgtable_radio = Radiobutton(self.box_window,text='PostBuild报文表', font=("楷体", 9), variable=self.radio_var, value=1, command=self.radio_callback)
		self.msgtable_radio.place(x=100, y=80)
		self.signaltable_radio = Radiobutton(self.box_window,text='PostBuild信号表', font=("楷体", 9), variable=self.radio_var, value=2, command=self.radio_callback)
		self.signaltable_radio.place(x=300, y=80)
		if self.config.user_type == "Developer":
			self.dtc_config_radio = Radiobutton(self.box_window,text='DTC配置表', font=("楷体", 9), variable=self.radio_var, value=3, command=self.radio_callback)
			self.dtc_config_radio.place(x=100, y=140)
			self.node_enable_radio = Radiobutton(self.box_window,text='节点使能配置表', font=("楷体", 9), variable=self.radio_var, value=4, command=self.radio_callback)
			self.node_enable_radio.place(x=300, y=140)
			self.diag_req_radio = Radiobutton(self.box_window,text='诊断请求表', font=("楷体", 9), variable=self.radio_var, value=5, command=self.radio_callback)
			self.diag_req_radio.place(x=100, y=200)
			self.diag_res_radio = Radiobutton(self.box_window,text='诊断响应表', font=("楷体", 9), variable=self.radio_var, value=6, command=self.radio_callback)
			self.diag_res_radio.place(x=300, y=200)


		# # 帮助
		# self.helpimg = PhotoImage(file='image/help.png')
		# self.help_button = Button(self.box_window,image=self.helpimg, command=self.help_callback)
		# # self.help_button = Button(self.box_window, text="帮助", bg="lightgreen", activebackground="gold", \
		# # 					fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.help_callback)
		# if self.config.user_type == "Customer":
		# 	self.help_button.place(x=130, y=140)
		# elif self.config.user_type == "Developer":
		# 	self.help_button.place(x=130, y=280)
		# # 绑定鼠标移入事件
		# self.help_button.bind("<Enter>", self.enter_help_area)
		# # 绑定鼠标移出事件
		# self.help_button.bind("<Leave> ", self.leave_help_area)

		# 运行
		self.runimg = PhotoImage(file='image/run.png')
		self.run_button = Button(self.box_window, image=self.runimg, command=self.run)
		# self.run_button = Button(self.box_window, text="运行", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=10, height=2, command=self.run)
		if self.config.user_type == "Customer":
			self.run_button.place(x=130, y=140)
		elif self.config.user_type == "Developer":
			self.run_button.place(x=130, y=280)
		# 绑定鼠标移入事件
		self.run_button.bind("<Enter>", self.enter_run_area)
		# 绑定鼠标移出事件
		self.run_button.bind("<Leave> ", self.leave_run_area)

		# 返回
		self.backimg = PhotoImage(file='image/exit.png')
		self.back_button = Button(self.box_window,image=self.backimg, command=self.back_callback)
		# self.back_button = Button(self.box_window, text="返回", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.back_callback)
		if self.config.user_type == "Customer":
			self.back_button.place(x=340, y=140)
		elif self.config.user_type == "Developer":
			self.back_button.place(x=340, y=280)
		# 绑定鼠标移入事件
		self.back_button.bind("<Enter>", self.enter_back_area)
		# 绑定鼠标移出事件
		self.back_button.bind("<Leave> ", self.leave_back_area)

		# 鼠标悬浮提示
		self.pre_click_hint_val = StringVar()#窗体自带的文本，新建一个值
		self.pre_click_hint = Label(self.box_window, textvariable=self.pre_click_hint_val, font=("楷体", 8), width=8, height=1)
		self.pre_click_hint.place_forget()

	def close_win_callback(self):
		'''点击X关闭窗口回调函数'''
		self.box_window.destroy()
		del(self.main_window.tool_if)

	def select_route_table_callback(self):
		'''选择路由表回调函数'''
		self.public_for_all = public4all.Public4All()
		self.public_for_all.get_file_pathname()
		# 如选择文件不为空字符串，修改Label显示内容；否则回至初始化显示状态
		if self.public_for_all.pathname != "":
			self.routetable_pathname_display["text"] = self.public_for_all.pathname
			self.routetable_pathname_display["anchor"] = W
		else:
			self.routetable_pathname_display["text"] = "请选择 <xxx_路由表提取>"
			self.routetable_pathname_display["anchor"] = "center"
			del self.public_for_all

	def postbuild_msg_table_callback(self):
		'''生成postbuil工具所用报文表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				msg = msg2pbmsg.MsgTableConvert()
				msg.pathname = self.public_for_all.pathname
				try:
					msg.main_pandas()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息或查看报文表是否关闭')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def postbuild_sig_table_callback(self):
		'''生成postbuil工具所用信号表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				sig = sig2pbsig.SignalTableConvert(self.config)
				sig.pathname = self.public_for_all.pathname
				try:
					sig.main_pandas()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息或查看报文表是否关闭')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')


	def dtc_cfg_table_callback(self):
		'''生成代码DTC配置表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				dtc_cfg = dtccfg.DtcConfig()
				dtc_cfg.pathname = self.public_for_all.pathname
				try:
					dtc_cfg.main()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def node_en_cfg_table_callback(self):
		'''生成代码节点配置表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				msg_node_en = msgnode.MsgNodeEnable()
				msg_node_en.pathname = self.public_for_all.pathname
				try:
					msg_node_en.main()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def diag_req_table_callback(self):
		'''生成诊断请求表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				diag_req = diagreqmsgcfg.DiagReqTable()
				diag_req.pathname = self.public_for_all.pathname
				diag_msg = diagmsgcfg.DiagResTable()
				diag_msg.pathname = self.public_for_all.pathname
				try:
					diag_req.main()
					diag_msg.main_req()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def diag_res_table_callback(self):
		'''生成诊断响应表（硬件转发）'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				diag_msg = diagmsgcfg.DiagResTable()
				diag_msg.pathname = self.public_for_all.pathname
				try:
					diag_msg.main_res()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def radio_callback(self):
		'''单选按钮回调函数'''
		print(self.radio_var.get())

	def run(self):
		'''运行按钮回调函数'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				val = self.radio_var.get()
				if val == 1 or val == 4 or val == 5 or val ==6:
					'''报文表转换，节点使能，诊断请求，诊断响应'''
					msg_checkerror = checkerror.MsgCheckError()
					msg_checkerror.pathName = self.public_for_all.pathname
					ret = msg_checkerror.main()
					if ret != False:
						messagebox.showinfo(title='提示', message='{} 第 {} 行，第 {} 列出错：{}'.format(ret[0], ret[1], ret[2], ret[3]))
						return
				elif val == 2:
					'''信号表转换'''
					sig_checkerror = checkerror.SignalCheckError()
					sig_checkerror.pathName = self.public_for_all.pathname
					ret = sig_checkerror.main()
					if ret != False:
						messagebox.showinfo(title='提示', message='{} 第 {} 行，第 {} 列出错：{}'.format(ret[0], ret[1], ret[2], ret[3]))
						return
				elif val == 3:
					'''DTC配置'''
					pass
				
				if val == 1:
					msg = msg2pbmsg.MsgTableConvert()
					msg.pathname = self.public_for_all.pathname
					try:
						msg.main_pandas()
						messagebox.showinfo(title='提示', message='PostBuild报文表生成成功')
					except:
						messagebox.showinfo(title='提示', message='转换出错，请检查表格信息或查看报文表是否关闭')
				elif val == 2:
					sig = sig2pbsig.SignalTableConvert(self.config)
					sig.pathname = self.public_for_all.pathname
					try:
						sig.main_pandas()
						messagebox.showinfo(title='提示', message='PostBuild信号表生成成功')
					except:
						messagebox.showinfo(title='提示', message='转换出错，请检查表格信息或查看报文表是否关闭')
				elif val == 3:
					dtc_cfg = dtccfg.DtcConfig()
					dtc_cfg.pathname = self.public_for_all.pathname
					try:
						dtc_cfg.main()
						messagebox.showinfo(title='提示', message='DTC配置表生成成功')
					except:
						messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
				elif val == 4:
					msg_node_en = msgnode.MsgNodeEnable()
					msg_node_en.pathname = self.public_for_all.pathname
					try:
						msg_node_en.main()
						messagebox.showinfo(title='提示', message='节点使能配置表生成成功')
					except:
						messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
				elif val == 5:
					if self.config.platInfo == "GAW1.2_NewPlatform":
						diag_req = diagreqmsgcfg.DiagReqTable()
						diag_req.pathname = self.public_for_all.pathname
						try:
							diag_req.main()
							messagebox.showinfo(title='提示', message='诊断请求表生成成功')
						except:
							messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
					elif self.config.platInfo == "GAW1.2_OldPlatform" or self.config.platInfo == "Qoros_C6M0" or self.config.platInfo == "CHJ":
						diag_msg = diagmsgcfg.DiagResTable()
						diag_msg.pathname = self.public_for_all.pathname
						try:
							diag_msg.main_req()
							messagebox.showinfo(title='提示', message='诊断请求表生成成功')
						except:
							messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')

				elif val == 6:
					if self.config.platInfo == "GAW1.2_NewPlatform":
						messagebox.showinfo(title='提示', message='新平台诊断响应报文不需要配置')
					elif self.config.platInfo == "GAW1.2_OldPlatform" or self.config.platInfo == "Qoros_C6M0" or self.config.platInfo == "CHJ":	
						diag_msg = diagmsgcfg.DiagResTable()
						diag_msg.pathname = self.public_for_all.pathname
						try:
							diag_msg.main_res()
							messagebox.showinfo(title='提示', message='诊断响应表生成成功')
						except:
							messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')
		else:
			messagebox.showinfo(title='提示', message='请选择路由表')

	def enter_run_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("运行")
		if self.config.user_type == "Customer":
			self.pre_click_hint.place(x=130, y=120)
		elif self.config.user_type == "Developer":
			self.pre_click_hint.place(x=130, y=260)

	def leave_run_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

	def help_callback(self):
		'''帮助'''
		ret = messagebox.askquestion(title='Help', message='这么简单还需要帮助？！！！')
		if ret == "yes":
			messagebox.showinfo(title='Help', message='哈哈哈 逗你呢 并没有什么帮助')

	def enter_help_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("帮助")
		if self.config.user_type == "Customer":
			self.pre_click_hint.place(x=130, y=120)
		elif self.config.user_type == "Developer":
			self.pre_click_hint.place(x=130, y=260)

	def leave_help_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()


	def back_callback(self):
		'''返回'''
		self.box_window.destroy()
		del(self.main_window.tool_if)

	def enter_back_area(self, *args):
		'''鼠标悬浮'''
		self.pre_click_hint_val.set("返回")
		if self.config.user_type == "Customer":
			self.pre_click_hint.place(x=340, y=120)
		elif self.config.user_type == "Developer":
			self.pre_click_hint.place(x=340, y=260)

	def leave_back_area(self, *args):
		'''鼠标离开'''
		self.pre_click_hint.place_forget()

