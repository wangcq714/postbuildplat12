from openpyxl.utils import get_column_letter, column_index_from_string
from tkinter.filedialog import askopenfilename
from pandas import read_excel

if __name__ == '__main__':
	from header import projdiagroutercfgheader
else:
	from tool.header import projdiagroutercfgheader


class DiagRouteTable(object):
	def __init__(self):
		self.Can2num = {"CAN1":1, "CAN2":2, "CAN3":3, "CAN4":4, "CAN5":5, "CAN6":6}
		self.pathname = None
		self.ChannalMapping = {}
		self.srcChList = []
		self.validDataList = []
		self.reqDataList = []
		self.diagB_validDataList = []
		self.diagB_reqDataList = []
		self.reqMsgCfgList = []

	# 获取文件路径名
	def get_file_pathname(self):
		# 选择文件
		self.pathname = askopenfilename(filetypes = [("Excel",".xlsx")])
		if self.pathname == '':
			print("没有选择文件")
			exit()

	# 读取Excel
	def read_data(self):
		dataFrame = read_excel(self.pathname, sheet_name="Sheet1", header=None, na_values="", usecols="A:Q")
		self.msgDataList = dataFrame.fillna("None").values[2:].tolist()
		# print(self.msgDataList)
		self.msgDataList = self.int2str(self.msgDataList)
		# print(self.msgDataList)

	#获取通道映射
	def get_channalmapping(self):
		for i in range(6):
			self.ChannalMapping[self.msgDataList[i][column_index_from_string('N') - 1]] = self.msgDataList[i][column_index_from_string('M') - 1]
		print(self.ChannalMapping)

	# 获取有效数据
	def get_valid_data(self):
		for subList in self.msgDataList:
			if subList[column_index_from_string('Q') - 1].strip(' ') == 'Y':
				self.validDataList.append(subList)
		
		# 获取诊断通道并以通道号升序排列	
		for subList in self.validDataList:
			if subList[column_index_from_string('F') - 1] not in self.srcChList:
				self.srcChList.append(subList[column_index_from_string('F') - 1])
		self.srcChList = sorted(self.srcChList, key=lambda srcCh:self.Can2num[self.ChannalMapping[srcCh]])
		print(self.srcChList)


		self.validDataList = sorted(self.validDataList, key=lambda subList: self.Can2num[self.ChannalMapping[subList[column_index_from_string('F') - 1]]])


		# print(self.validDataList)

	# 获取要发送的通道
	def get_tx_ch(self, dataList) -> int:
		ch = 1
		for tick in dataList[column_index_from_string('L') - 1 : column_index_from_string('G') -2 : -1]:
			if tick == '√':
				break
			ch += 1

		return ch

	# 获取要发送的通道列表
	def get_tx_ch_list(self, dataList) -> list:
		chList = []
		ch = 1
		for tick in dataList[column_index_from_string('L') - 1 : column_index_from_string('G') -2 : -1]:
			if tick == '√':
				chList.append(ch)
			ch += 1

		return chList


	# 诊断请求报文配置表元素
	def __req_msg_element(self, dataList) -> list:
		retList = []
		# retList.append(dataList[column_index_from_string('A') - 1].strip(' ') + 'u') # ID
		retList.append(str(len(self.get_tx_ch_list(dataList))) + 'u') # dest_mo_num
		retList.append("255u") # src_ecu_node
		retList.append("255u") # valid_flg_index(DTC)
		retList.append(dataList[column_index_from_string('D') - 1].strip(' ') + 'u') # DLC
		for ch in sorted(self.get_tx_ch_list(dataList)):
			retList.append("NODE_" + get_column_letter(ch) + "_TX_DIAGROUTING")
			retList.append("PB_RT_OFF")
		for i in range(5 - len(self.get_tx_ch_list(dataList))):
			retList.append('0u')
			retList.append('0u')
		retList.append('0u')
		retList.append('0u') # msg_index
		retList.append('0x0000u') # buf_index
		retList.append('0u') # pre_callback
		retList.append('0u') # post_callback

		return retList


	# 对得到的有效数据进行加工处理
	def data_handling(self):
		for subList in self.validDataList:
			self.reqDataList.append(self.__req_msg_element(subList))

		# print(self.reqDataList)

	# 创建诊断请求报文配置表
	def buid_req_msg_list(self) -> list:
		self.reqMsgCfgList.append("const DiagRouter_Table DiagRoutingTable[DIAGROUTER_TABLE_SIZE] = \n")
		self.reqMsgCfgList.append("{\n")
		for index, subList in enumerate(self.reqDataList):
			self.reqMsgCfgList.append('/*' + self.validDataList[index][column_index_from_string('A') - 1].strip(' ') + '*/')
			self.reqMsgCfgList.append("{")
			self.reqMsgCfgList.append(', '.join(subList))
			self.reqMsgCfgList.append("},\n")
		self.reqMsgCfgList.append("};\n")

	# 将列表中的所有int转为str
	@staticmethod
	def int2str(dataList) -> list:
		retDataList = []
		for i in range(len(dataList)):
			retDataList.append([str(j) for j in dataList[i]])

		return retDataList

# 报文索引
class Id2IndexTable(object):
	"""diagid2index_table"""
	def __init__(self, diagRouteTable):
		"""初始化"""
		self.validDataList = diagRouteTable.validDataList
		self.srcChList = diagRouteTable.srcChList
		self.idList = []

		self.diagid2IndexTableA = []
		self.diagid2IndexTableB = []

		self.diagid2index_table_a = []
		self.diagid2index_table_b = []

		self.diagid2index_table = []


	def data_handle(self):
		"""数据处理"""
		for i in range(int("0x100", 16)):
			self.diagid2IndexTableA.append("0xFFFu")
			self.diagid2IndexTableB.append("0xFFFu")


		# 将ID单独提取出来，用于后面获取索引
		for subList in self.validDataList:
			self.idList.append(subList[column_index_from_string('A') - 1].strip(' '))

		# 轮询所有轮询发送的报文，获得索引值
		for subList in self.validDataList:
			if subList[column_index_from_string('F') - 1] == self.srcChList[0]:
				self.diagid2IndexTableA[int(subList[column_index_from_string('A') - 1].strip(' '), 16) - int("0x700", 16)] = \
				"0x{0:03X}u".format(self.idList.index(subList[column_index_from_string('A') - 1].strip(' ')))
			elif subList[column_index_from_string('F') - 1] == self.srcChList[1]:
				self.diagid2IndexTableB[int(subList[column_index_from_string('A') - 1].strip(' '), 16) - int("0x700", 16)] = \
				"0x{0:03X}u".format(self.idList.index(subList[column_index_from_string('A') - 1].strip(' ')))


		# print(self.diagid2IndexTableA)
		# print(self.diagid2IndexTableB)


	def build_table(self):
		"""创建数组表"""
		self.diagid2index_table_a.append("FAR const uint16 diagid2index_table_a[0x100] =\n")
		self.diagid2index_table_b.append("FAR const uint16 diagid2index_table_b[0x100] =\n")
		# self.diagid2index_table_a.append("table8_IdIndex0={\n")
		# self.diagid2index_table_b.append("table8_IdIndex1={\n")

		self.diagid2index_table_a.append("{\n")
		self.diagid2index_table_b.append("{\n")

		for i in range(int("0x100", 16)):
			self.diagid2index_table_a.append("/*" + "0x{0:03X}".format(i + int("0x700", 16)) + "*/" + self.diagid2IndexTableA[i] + ",\n")
			self.diagid2index_table_b.append("/*" + "0x{0:03X}".format(i + int("0x700", 16)) + "*/" + self.diagid2IndexTableB[i] + ",\n")


		self.diagid2index_table_a.append("};\n")
		self.diagid2index_table_b.append("};\n")

		self.diagid2index_table.extend(self.diagid2index_table_a)
		self.diagid2index_table.extend(self.diagid2index_table_b)


class WriteData(object):
	"""write"""
	def __init__(self):
		self.first_open_Proj_DiagRouter_Cfg_c = False

	def write2Proj_DiagRouter_Cfg_c(self, dataList):
		# 如果第一次写入，新建一个.c文件，否则接续写
		if self.first_open_Proj_DiagRouter_Cfg_c == False:
			self.first_open_Proj_DiagRouter_Cfg_c = True
			with open("output/Proj_DiagRouter_Cfg.c",'w') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)
		else:
			with open("output/Proj_DiagRouter_Cfg.c",'a') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)

class DiagReqTable(object):
	def __init__(self):
		self.pathname = ""

	def main(self):
		diagRouteTable = DiagRouteTable()

		diagRouteTable.pathname = self.pathname

		diagRouteTable.read_data()

		diagRouteTable.get_channalmapping()

		diagRouteTable.get_valid_data()

		diagRouteTable.data_handling()

		diagRouteTable.buid_req_msg_list()


		id2IndexTable = Id2IndexTable(diagRouteTable)
		id2IndexTable.data_handle()
		id2IndexTable.build_table()

		writeData = WriteData()
		writeData.write2Proj_DiagRouter_Cfg_c(projdiagroutercfgheader.projdiagrouter_headerList)
		writeData.write2Proj_DiagRouter_Cfg_c(diagRouteTable.reqMsgCfgList)
		writeData.write2Proj_DiagRouter_Cfg_c(id2IndexTable.diagid2index_table)

def main():

	diagRouteTable = DiagRouteTable()

	diagRouteTable.get_file_pathname()

	diagRouteTable.read_data()

	diagRouteTable.get_channalmapping()

	diagRouteTable.get_valid_data()

	diagRouteTable.data_handling()

	diagRouteTable.buid_req_msg_list()


	id2IndexTable = Id2IndexTable(diagRouteTable)
	id2IndexTable.data_handle()
	id2IndexTable.build_table()

	writeData = WriteData()
	writeData.write2Proj_DiagRouter_Cfg_c(projdiagroutercfgheader.projdiagrouter_headerList)
	writeData.write2Proj_DiagRouter_Cfg_c(diagRouteTable.reqMsgCfgList)
	writeData.write2Proj_DiagRouter_Cfg_c(id2IndexTable.diagid2index_table)




	print("------------------Finished--------------------------")



if __name__ == '__main__':
	main()
