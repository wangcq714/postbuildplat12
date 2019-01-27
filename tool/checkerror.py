import re
from copy import deepcopy
from openpyxl.utils import get_column_letter, column_index_from_string
from tkinter.filedialog import askopenfilename
from pandas import read_excel


class MsgCheckError(object):
	'''错误检查'''
	def __init__(self):
		self.pathName = ""
		self.headerList = []
		self.dataList = []

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathName = askopenfilename(filetypes = [("Excel",".xlsx")])
		if self.pathName == ():
			self.pathName = ""
			self.headerList = []
			self.dataList = []
		# print(self.pathName)
		# print(type(self.pathName))

	def read_data(self):
		"""从路由表中读取数据"""
		self.headerList = []
		self.dataList = []
		if self.pathName != "":
			dataFrame = read_excel(self.pathName, sheet_name="Sheet1", header=None, na_values="", usecols="A:Q")			
			self.dataList = dataFrame.fillna("None").values[2:].tolist()
			header = dataFrame.fillna("None").values[:2].tolist()

			for i in range(column_index_from_string("Q")):
				if i <= (column_index_from_string("F") - 1) or ((column_index_from_string("O") - 1) <= i <= (column_index_from_string("Q") - 1)):
					self.headerList.append(header[0][i])
				else:
					self.headerList.append(header[1][i])

		print(self.headerList)
		# print(self.dataList)


if __name__ == '__main__':
	checkError = MsgCheckError()
	checkError.get_file_pathname()
	checkError.read_data()

