# V1.6


# import sys
import os

# from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
# from openpyxl import Workbook
import csv
#from tkinter import *
from tkinter.filedialog import askopenfilename
# import pandas
from pandas import read_excel
#import numpy


class MsgTableConvert(object):
	'''报文表转换'''
	def __init__(self):
		self.pathname = ""
		self.src_row_data_all = []   #存取源表的所有行数据列表
		self.des_column_data_all = []   #存取目标表的所有行数据列表
		# self.diag_des_column_data_all = []   #存取目标表的所有行数据列表
		self.ChannalMapping = {}        #CAN通道与系统框图通道映射
		self.Can2num = {"CAN1":1, "CAN2":2, "CAN3":3, "CAN4":4, "CAN5":5, "CAN6":6}  #CAN通道与数字映射
		self.TableHeader = ["LineNumber", "TxMessageName", "TxCANID", "TxPeriod", "TxDLC", "TxChannle", "RxMessageName", \
						"RxCANID", "RxPeriod", "RxDLC", "RxChannel", "RxMsk", "RxInterrupt", "RxDTC", "RouteCondiction"]

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathname = askopenfilename(filetypes = [("Excel",".xlsx")])
		if self.pathname == ():
			self.pathname = ""
		# print(self.self.self.pathname)
		# print(type(self.self.self.pathname))

	# 获取通道映射
	def get_channalmapping_pandas(self, dataFrame):
		for i in range(6):
			self.ChannalMapping[dataFrame.values[i + 2][column_index_from_string('N') - 1]] = dataFrame.values[i +2][column_index_from_string('M') - 1]

	# 创建目标单行数据
	def build_des_column_data(self, LineNumber, Txchannal, src_num) -> list:
		des_column_data_list = []

		des_column_data_list.append(str(LineNumber))
		des_column_data_list.append(self.src_row_data_all[src_num][column_index_from_string('B') - 1])
		des_column_data_list.append(self.src_row_data_all[src_num][column_index_from_string('A') - 1])
		if self.src_row_data_all[src_num][column_index_from_string('C') - 1] != "None":
			des_column_data_list.append(str(self.src_row_data_all[src_num][column_index_from_string('C') - 1]))
		elif self.src_row_data_all[src_num][column_index_from_string('C') - 1] == "None":
			des_column_data_list.append("NA")
		des_column_data_list.append(str(self.src_row_data_all[src_num][column_index_from_string('D') - 1]))
		des_column_data_list.append(Txchannal)
		des_column_data_list.append(self.src_row_data_all[src_num][column_index_from_string('B') - 1])
		des_column_data_list.append(self.src_row_data_all[src_num][column_index_from_string('A') - 1])
		if self.src_row_data_all[src_num][column_index_from_string('C') - 1] != "None":
			des_column_data_list.append(str(self.src_row_data_all[src_num][column_index_from_string('C') - 1]))
		elif self.src_row_data_all[src_num][column_index_from_string('C') - 1] == "None":
			des_column_data_list.append("NA")
		des_column_data_list.append(str(self.src_row_data_all[src_num][column_index_from_string('D') - 1]))
		des_column_data_list.append(self.Can2num[self.ChannalMapping[self.src_row_data_all[src_num][column_index_from_string('F') - 1]]])
		des_column_data_list.append("0x7FF")
		if self.src_row_data_all[src_num][column_index_from_string('O') - 1] == "Y":
			des_column_data_list.append('1')
		else:
			des_column_data_list.append('0')
		if self.src_row_data_all[src_num][column_index_from_string('E') - 1] == "None" or self.src_row_data_all[src_num][column_index_from_string('E') - 1] == "NA":
			des_column_data_list.append('N')
		else:
			des_column_data_list.append('Y')
		des_column_data_list.append('3')

		return des_column_data_list

	# 获取要发送的通道
	def get_TxChannal(self, src_num) -> list:
		TxChannalList = []
		i = 1
		for tick in self.src_row_data_all[src_num][column_index_from_string('L') - 1 : column_index_from_string('G') -2 : -1]:
		#print(self.src_row_data_all[src_num][column_index_from_string('F')])
			if tick == '√':
				TxChannalList.append(i)
			i += 1

		return TxChannalList

	# 创建所有目标数据
	def build_des_column_data_all(self):
		LineNumber = 1
		diag_LineNumber = 1
		for num in range(len(self.src_row_data_all)):
			if self.src_row_data_all[num][column_index_from_string('Q') - 1] != 'Y':
				TxChList = self.get_TxChannal(num)
				#print(TxChList)
				if len(TxChList) > 0:
					for TxCh in TxChList:
						self.des_column_data_all.append(self.build_des_column_data(LineNumber, TxCh, num))
						LineNumber += 1
				else:
					self.des_column_data_all.append(self.build_des_column_data(LineNumber, 0, num))
					LineNumber += 1
			# else:
			# 	if self.src_row_data_all[num][column_index_from_string('F') - 1] == sys.argv[1]:
			# 		TxChList = get_TxChannal(num)
			# 		#print(TxChList)
			# 		if len(TxChList) > 0:
			# 			for TxCh in TxChList:
			# 				self.diag_des_column_data_all.append(self.build_des_column_data(diag_LineNumber, TxCh, num))
			# 				diag_LineNumber += 1
			# 		else:
			# 			self.diag_des_column_data_all.append(self.build_des_column_data(diag_LineNumber, 0, num))
			# 			diag_LineNumber += 1


	def mkdir(self, path:str): 
	    # 去除首位空格、尾部\
	    path=path.strip()
	    # 判断结果
	    if not os.path.exists(path):
	        os.makedirs(path) 

	# 主函数
	def main_pandas(self):
		if self.pathname != "":
			dataFrame = read_excel(self.pathname, sheet_name="Sheet1", header=None, na_values="", usecols="A:Q")
			
			self.src_row_data_all = dataFrame.fillna("None").values[2:].tolist()

			# #通道映射
			self.get_channalmapping_pandas(dataFrame)
			print(self.ChannalMapping)

			# #读取原表中的所有数据
			# read_lines_all(sheet)

			#创建目标表列表
			self.build_des_column_data_all()

			self.mkdir("output")
			#将目标列表写入目标文件中
			# with open(self.pathname[:self.pathname.rfind('/')+1] + "MessageRoute.csv", 'w', newline='') as csvfile:	
			with open("output/MessageRoute.csv", 'w', newline='') as csvfile:	
				writer = csv.writer(csvfile)
				#写入表头
				writer.writerow(self.TableHeader)
				#写入目标数据
				writer.writerows(self.des_column_data_all)

			# #将目标列表写入目标文件中
			# with open(self.pathname[:self.pathname.rfind('/')+1] + "DiagReqRoute.csv", 'w', newline='') as csvfile:	
			# 	writer = csv.writer(csvfile)
			# 	#写入表头
			# 	writer.writerow(self.TableHeader)
			# 	#写入目标数据
			# 	writer.writerows(self.diag_des_column_data_all)

			#print(self.src_row_data_all)
			#print(self.des_column_data_all)

			print("------------------Finished--------------------------")	
		else:
			print("请选择路由表")



if __name__ == '__main__':
	msg_table_convert = MsgTableConvert()
	msg_table_convert.get_file_pathname()
	msg_table_convert.main_pandas()



