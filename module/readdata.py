# import pandas
from pandas import read_csv
import numpy

from tkinter.filedialog import askopenfilename
from openpyxl.utils import get_column_letter, column_index_from_string


# 定义一个路由表类
class RouterTable(object):
	"""Route Table"""
	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathName = askopenfilename(filetypes = [("Excel",".csv")])
		if self.pathName == ():
			self.pathName = ""
			self.headerList = []
			self.dataList = []
		# print(self.pathName)
		# print(type(self.pathName))

	def read_data(self, row:str):
		"""从路由表中读取数据"""
		self.headerList = []
		self.dataList = []
		if self.pathName != "":
			dataFrame = read_csv(self.pathName, header=None, na_values="", usecols=[i for i in range(column_index_from_string(row))])
			self.dataList = dataFrame.fillna("None").values[1:].tolist()
			self.headerList = dataFrame.fillna("None").values[:1].tolist()[0]
		# print(self.headerList)
		# print(self.dataList)


# 普通报文类
class MsgRoute(RouterTable):
	"""普通报文信息"""
	def __init__(self):
		self.pathName = ""
		self.headerList = []
		self.dataList = []


# 信号报文类
class SignalRoute(RouterTable):
	"""信号报文信息"""
	def __init__(self):
		self.pathName = ""
		self.headerList = []
		self.dataList = []


# 诊断请求报文类
class DiagReqRoute(RouterTable):
	"""信号报文信息"""
	def __init__(self):
		self.pathName = ""
		self.dataList = []


# 定义一个读hex文件类
class ReadHex(object):
	"""读取hex"""
	def __init__(self):
		"""初始化数据"""
		self.pathName = ""
		self.hexData = []

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathName = askopenfilename(filetypes = [("hex",".hex")])
		if self.pathName == ():
			self.pathName = ""
			self.hexData = []
		# print(self.pathName) 

	def read_hex(self):
		"""读取hex"""
		self.hexData = []
		if self.pathName != "":
			with open(self.pathName, "r") as hexf:
				for colData in hexf:
					self.hexData.append(colData)

			print(self.hexData[0:10])


class Config(object):
	def __init__(self):
		self.configInfo = {}

	def read_data(self):
		'''读取配置信息'''
		with open("config.ini", 'r') as file:
			for line in file:
				if line.find(':') != -1:
					tmpDict = {}
					tmpList = line[line.find(':')+1:-1].split(',')
					tmpDict["tableLenAddr"] = tmpList[0]
					tmpDict["lenType"] = tmpList[1]
					tmpDict["tableAddr"] = tmpList[2]
					tmpDict["tableLen"] = tmpList[3]
					self.configInfo[line[:line.find(':')]] = tmpDict

		print(self.configInfo)


if __name__ == '__main__':
	# msgRoute = MsgRoute()
	# msgRoute.get_file_pathname()
	# msgRoute.read_data("O")
	# print(msgRoute.dataList)
	# print(len(msgRoute.dataList))


	# signalRoute = SignalRoute()
	# signalRoute.get_file_pathname()
	# signalRoute.read_data("T")
	# print(signalRoute.dataList)
	# print(len(signalRoute.dataList))

	config = Config()
	config.read_data()





