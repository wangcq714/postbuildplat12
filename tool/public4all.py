from tkinter.filedialog import askopenfilename

class Public4All(object):
	'''为其他小工具服务的公共类'''
	def __init__(self):
		'''初始化'''
		self.pathname = ""

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathname = askopenfilename(filetypes = [("Excel",".xlsx")])
		if self.pathname == ():
			self.pathname = ""
		print(self.pathname)
		# print(type(self.pathName))




