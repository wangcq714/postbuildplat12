from tkinter import Toplevel, Label, Button, StringVar, Entry, W
from tkinter import messagebox
from tool import public4all
from tool import sig2pbsig, msg2pbmsg, diagreqmsgcfg

class BoxWindow(object):
	'''工具窗口'''
	def __init__(self, main_window, user_type):
		'''初始化'''
		self.box_window = Toplevel()
		self.main_window = main_window
		self.user_type = user_type

	def boxwin_setup(self):
		self.box_window.title("百宝箱")
		if self.user_type == "Customer":
			self.box_window.geometry('550x200')                 #是x 不是*
		elif self.user_type == "Developer":
			self.box_window.geometry('550x350')
		self.box_window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True

		# 报文显示
		Label(self.box_window, text="Current File:", font=("Times", 10), width=10, height=2).place(x=10, y=20)
		self.routetable_pathname_display = Label(self.box_window, text="请选择 <xxx_路由表提取>", bg="white", font=("楷体", 9), width=56, height=2)
		self.routetable_pathname_display.place(x=90, y=22)

		self.routetable_select_buntton = Button(self.box_window, text="选择路由表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.select_route_table_callback)
		self.routetable_select_buntton.place(x=450, y=20)

		# PostBuild报文表
		self.signaltable_select_buntton = Button(self.box_window, text="PostBuild报文表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.postbuild_msg_table_callback)
		self.signaltable_select_buntton.place(x=100, y=80)

		# PostBuild信号表
		self.hex_select_buntton = Button(self.box_window, text="PostBuild信号表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.postbuild_sig_table_callback)
		self.hex_select_buntton.place(x=300, y=80)

		if self.user_type == "Developer":
			# DTC配置表
			self.signaltable_select_buntton = Button(self.box_window, text="DTC配置表", bg="lightgreen", activebackground="gold", \
													fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.dtc_cfg_table_callback)
			self.signaltable_select_buntton.place(x=100, y=140)

			# 节点使能配置表
			self.hex_select_buntton = Button(self.box_window, text="节点使能配置表", bg="lightgreen", activebackground="gold", \
													fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.node_en_cfg_table_callback)
			self.hex_select_buntton.place(x=300, y=140)

			# DTC配置表
			self.signaltable_select_buntton = Button(self.box_window, text="诊断请求表", bg="lightgreen", activebackground="gold", \
													fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.diag_req_table_callback)
			self.signaltable_select_buntton.place(x=100, y=200)

			# 节点使能配置表
			self.hex_select_buntton = Button(self.box_window, text="诊断响应表", bg="lightgreen", activebackground="gold", \
													fg="black", activeforeground="black", font=("楷体", 9), width=20, height=2, command=self.diag_res_table_callback)
			self.hex_select_buntton.place(x=300, y=200)

		# 帮助
		self.help = Button(self.box_window, text="帮助", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.help_callback)
		if self.user_type == "Customer":
			self.help.place(x=120, y=140)
		elif self.user_type == "Developer":
			self.help.place(x=120, y=280)
		# 退出
		self.exit = Button(self.box_window, text="退出", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2, command=self.back_callback)
		if self.user_type == "Customer":
			self.exit.place(x=325, y=140)
		elif self.user_type == "Developer":
			self.exit.place(x=325, y=280)
		# 
		# self.help = Button(self.box_window, text="帮助", bg="lightgreen", activebackground="gold", \
		# 					fg="black", activeforeground="black", font=("楷体", 9), width=12, height=2)
		# self.help.place(x=350, y=260)

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
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')

	def postbuild_sig_table_callback(self):
		'''生成postbuil工具所用信号表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				sig = sig2pbsig.SignalTableConvert()
				sig.pathname = self.public_for_all.pathname
				try:
					sig.main_pandas()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')


	def dtc_cfg_table_callback(self):
		'''生成代码DTC配置表'''
		pass

	def node_en_cfg_table_callback(self):
		'''生成代码节点配置表'''
		pass

	def diag_req_table_callback(self):
		'''生成诊断请求表'''
		if hasattr(self, "public_for_all"):
			if self.public_for_all.pathname != "":
				diag_req = diagreqmsgcfg.DiagReqTable()
				diag_req.pathname = self.public_for_all.pathname
				try:
					diag_req.main()
					messagebox.showinfo(title='提示', message='转换完成')
				except:
					messagebox.showinfo(title='提示', message='转换出错，请检查表格信息')

	def diag_res_table_callback(self):
		'''生成诊断响应表（硬件转发）'''
		pass

	def help_callback(self):
		'''帮助'''
		ret = messagebox.askquestion(title='Help', message='这么简单还需要帮助？！！！')
		if ret == "yes":
			messagebox.showinfo(title='Help', message='哈哈哈 逗你呢 并没有什么帮助')

	def back_callback(self):
		'''帮助'''
		self.box_window.destroy()
		del(self.main_window.tool_if)


