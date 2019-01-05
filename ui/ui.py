from tkinter import *
from tkinter import messagebox

class MainWindow(object):
	"""UI类"""
	def __init__(self):
		self.window = Tk()

	def setup(self):
		"""主界面参数配置"""
		self.window.title("PostBuild(开发版) kanwairen")
		self.window.geometry('500x200')                 #是x 不是*
		self.window.resizable(width=False, height=False) #宽不可变, 高可变, 默认为True


		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=19)
		self.msgtable_pathname_display = Label(self.window, text="如无报文可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.msgtable_pathname_display.place(x=80, y=19)

		self.msgtable_select_buntton = Button(self.window, text="选择报文表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_msgtable)
		self.msgtable_select_buntton.place(x=400, y=20)


		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=59)
		self.signaltable_pathname_display = Label(self.window, text="如无信号可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.signaltable_pathname_display.place(x=80, y=59)

		self.signaltable_select_buntton = Button(self.window, text="选择信号表", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_signaltable)
		self.signaltable_select_buntton.place(x=400, y=60)


		Label(self.window, text="Current File:", font=("Arial", 8), width=10, height=2).place(x=10, y=99)
		self.hex_pathname_display = Label(self.window, text="如不操作hex可不选", bg="white", font=("Arial", 8), width=50, height=2)
		self.hex_pathname_display.place(x=80, y=99)

		self.hex_select_buntton = Button(self.window, text="选择源HEX", bg="lightgreen", activebackground="gold", \
												fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.select_hex)
		self.hex_select_buntton.place(x=400, y=100)


		self.run = Button(self.window, text="运行", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.run)
		self.run.place(x=100, y=150)

		self.exit = Button(self.window, text="退出", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.exit)
		self.exit.place(x=200, y=150)

		self.help = Button(self.window, text="帮助", bg="lightgreen", activebackground="gold", \
							fg="black", activeforeground="black", font=("Arial", 8), width=8, height=1, command=self.help)
		self.help.place(x=300, y=150)


	def show(self):
		self.window.mainloop()


class MyWindow(MainWindow):
	"""UI"""
	def __init__(self, msgRoute, signalRoute, readHex, run):
		super().__init__()
		self.msgRoute = msgRoute
		self.signalRoute = signalRoute
		self.readHex = readHex
		self.ui_run = run

	def run(self):
		self.ui_run(self.msgRoute, self.signalRoute, self.readHex)
		messagebox.showinfo(title='提示', message='运行结束')

	def exit(self):
		self.window.quit()

	def help(self):
		ret = messagebox.askquestion(title='Help', message='这么简单还需要帮助？！！！')
		if ret == "yes":
			messagebox.showinfo(title='Help', message='哈哈哈 逗你呢 并没有什么帮助')

	def select_msgtable(self):
		self.msgRoute.get_file_pathname()
		if self.msgRoute.pathName != "":
			self.msgtable_pathname_display["text"] = self.msgRoute.pathName
			self.msgtable_pathname_display["anchor"] = W
		else:
			self.msgtable_pathname_display["text"] = "如无报文可不选"
			self.msgtable_pathname_display["anchor"] = "center"

	def select_signaltable(self):
		self.signalRoute.get_file_pathname()
		if self.signalRoute.pathName != "":
			self.signaltable_pathname_display["text"] = self.signalRoute.pathName
			self.signaltable_pathname_display["anchor"] = W
		else:
			self.signaltable_pathname_display["text"] = "如无信号可不选"
			self.signaltable_pathname_display["anchor"] = "center"

	def select_hex(self):
		self.readHex.get_file_pathname()
		if self.readHex.pathName != "":
			self.hex_pathname_display["text"] = self.readHex.pathName
			self.hex_pathname_display["anchor"] = W
		else:
			self.hex_pathname_display["text"] = "如不操作hex可不选"
			self.hex_pathname_display["anchor"] = "center"


if __name__ == '__main__':
	pass



