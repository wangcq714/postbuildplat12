# V1.1

import os
from pandas import read_excel
from openpyxl.utils import get_column_letter, column_index_from_string
from tkinter.filedialog import askopenfilename


class DtcConfig(object):
	'''DTC配置'''
	def __init__(self):
		self.pathname = ""
		self.src_row_data_all = []   #存取源表的所有行数据列表
		self.Net2BusOffDTC = {}
		self.reportDTC_cycle = 10
		self.clearDTC_timer = 5

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathname = askopenfilename(filetypes = [("Excel",".xlsx")])
		if self.pathname == ():
			self.pathname = ""
		# print(self.self.self.pathname)
		# print(type(self.self.self.pathname))


	# 数据处理，将列表中所有int转为str
	def dataHandling(self, srcData:list):
		for i in range(len(srcData)):
			srcData[i] = [str(j) for j in srcData[i]]

	#读取网段与BusOffDTC映射关系
	def read_net2busoffDTCmapping(self):
		for row in self.src_row_data_all:
			if row[0] == "NA" or row[0] == "None":
				if (row[column_index_from_string('F') - 1] != "NA" and row[column_index_from_string('F') - 1] != "None"):
					self.Net2BusOffDTC[row[column_index_from_string('F') - 1]] = row[column_index_from_string('I') - 1]

	#依照ID大小对读出的节点丢失行进行排序
	def sort_src_row_data_all_Missing(self) -> list:
		sort_src_row_data_all_list = []
		i = 0
		for row in self.src_row_data_all:
			if row[0] != "NA" and row[0] != "None":
				if i == 0:
					sort_src_row_data_all_list.append(row)
				else:
					for j in range(len(sort_src_row_data_all_list)):
						if int(row[0].strip(' '), 16) < int(sort_src_row_data_all_list[j][0].strip(' '), 16):
							sort_src_row_data_all_list.insert(j, row)
							break
						else:
							if j == len(sort_src_row_data_all_list) - 1:
								sort_src_row_data_all_list.append(row)
				i += 1
		return sort_src_row_data_all_list

	#计算EEP_ConfigVal
	def cal_EEP_ConfigVal(self, ListValue) -> str:
		if ListValue[column_index_from_string('G') - 1] == "None" or ListValue[column_index_from_string('H') - 1] == "None":
			return "0xFF"
		else:
			EEP_ConfigVal = int(ListValue[column_index_from_string('G') - 1]) * 8 + int(ListValue[column_index_from_string('H') - 1])
			if EEP_ConfigVal < 10:
				return ' ' + str(EEP_ConfigVal)
			else:
				return str(EEP_ConfigVal)

	#创建gDEM_taDTCCfgPattern数组元素
	def build_gDEM_taDTCCfgPattern_Array_Element(self, ListValue) -> str:
		ElementStr = '\t' + '{' + '\t'	
		ElementStr += "{0x" + ListValue[column_index_from_string('E') - 1].strip(' ')[:2] + ',' \
						+ "0x" + ListValue[column_index_from_string('E') - 1].strip(' ')[2:4] + ','  \
						+ "0x" + ListValue[column_index_from_string('E') - 1].strip(' ')[4:6] + "},"
		ElementStr += '\t' + '1,'
		ElementStr += '\t' + '0x02,'
		ElementStr += '\t' + '1,'
		ElementStr += '\t' + '40,'
		ElementStr += '\t' + '0x00,'
		ElementStr += '\t' + '0x00,'
		ElementStr += '\t' + self.cal_EEP_ConfigVal(ListValue)
		ElementStr += '},'
		if ListValue[0] == "NA" or ListValue[0] == "None":
			if ListValue[column_index_from_string('F') - 1] == "NM":
				ElementStr += '\t' + '/*' + '_'.join(ListValue[column_index_from_string('J') - 1].strip(' ').split(' ')) + '*/'
			else:
				ElementStr += '\t' + '/*' + "DTC_" + ListValue[column_index_from_string('J') - 1] + '_' + ListValue[column_index_from_string('I') - 1] + '*/'
		else:
			ElementStr += '\t' + '/*' + "DTC_" + ListValue[column_index_from_string('B') - 1] + ListValue[column_index_from_string('A') - 1][2:] \
						+ '_TIMEOUT_' + '_' + ListValue[column_index_from_string('I') - 1]  + '*/'	
		ElementStr += '\n'
			
		return ElementStr

	#创建gDEM_taDTCCfgPattern数组
	def build_gDEM_taDTCCfgPattern_Array(self) -> list:
		gDEM_taDTCCfgPatternList = []
		gDEM_taDTCCfgPatternStr = "const TYPE_DTC_CFG_PATTERN gDEM_taDTCCfgPattern[DTC_MAX]=" + '\n'
		gDEM_taDTCCfgPatternStr += '{' + '\n'

		for ListValue in self.src_row_data_all:
			gDEM_taDTCCfgPatternStr += self.build_gDEM_taDTCCfgPattern_Array_Element(ListValue)

		gDEM_taDTCCfgPatternStr += '};' + '\n'

		gDEM_taDTCCfgPatternList.append(gDEM_taDTCCfgPatternStr)

		return gDEM_taDTCCfgPatternList


	#创建PB_Node_Missing_DTC_Tab数组元素
	def build_PB_Node_Missing_DTC_Tab_Array_Element(self, ListValue) -> str:
		if ListValue[0] != 'None' and ListValue[0] != 'NA':
			ElementStr = '\t' + '{'
			ElementStr += ListValue[column_index_from_string('B') - 1].strip(' ') + '_' + ListValue[column_index_from_string('A') - 1].strip(' ')[2:] + ','
			ElementStr += (10 - len(ElementStr))*' '
			ElementStr += '\t' + "DTC_" + ListValue[column_index_from_string('B') - 1].strip(' ') + '_' + ListValue[column_index_from_string('A') - 1].strip(' ')[2:] + '_TIMEOUT_' \
							+ ListValue[column_index_from_string('I') - 1] + ','
			ElementStr += (40 - len(ElementStr))*' '				
			ElementStr += '\t' + "TIME_VAL(" + ListValue[column_index_from_string('C') - 1] + "),"
			ElementStr += '\t' + str(self.reportDTC_cycle) + ","
			ElementStr += '\t' + "TIME_VAL(0),"
			ElementStr += '\t' + str(self.clearDTC_timer) + ","
			ElementStr += '\t' + "PB_RT_KL15,"
			ElementStr += '\t' + "0xFF,"
			ElementStr += '\t' + "DTC_" + ListValue[column_index_from_string('F') - 1] + "_BUSOFF_" + self.Net2BusOffDTC[ListValue[column_index_from_string('F') - 1]]
			ElementStr += "},"
			ElementStr += '\n'

		return ElementStr


	#创建PB_Node_Missing_DTC_Tab数组
	def build_PB_Node_Missing_DTC_Tab_Array(self) -> list:
		PB_Node_Missing_DTCList = []
		PB_Node_Missing_DTCStr = "const PB_NODEMISSINGDTC_TYP PB_Node_Missing_DTC_Tab[] = " + '\n'
		PB_Node_Missing_DTCStr += '{' + '\n'

		for ListValue in self.sort_src_row_data_all_Missing():
			PB_Node_Missing_DTCStr += self.build_PB_Node_Missing_DTC_Tab_Array_Element(ListValue)

		PB_Node_Missing_DTCStr += '};' + '\n'
		PB_Node_Missing_DTCList.append(PB_Node_Missing_DTCStr)
		return PB_Node_Missing_DTCList

	#创建DTC_TABLE枚举
	def build_DTC_TABLE_enum_defined(self) -> list:
		DTC_TABLE_enum_definedList = []
		DTC_TABLE_enum_definedStr = "typedef enum" + '\n'
		DTC_TABLE_enum_definedStr += '{' + '\n'
		for ListValue in self.sort_src_row_data_all_Missing():
			DTC_TABLE_enum_definedStr += '\t' + ListValue[column_index_from_string('B') - 1].strip(' ') + '_' + ListValue[column_index_from_string('A') - 1].strip(' ')[2:] + ',' + '\n'
		DTC_TABLE_enum_definedStr += '\t' + "NODE_MISSING_MAX_VAL" + "\n"
		DTC_TABLE_enum_definedStr += '}' + "DTC_TABLE;" + '\n'
		DTC_TABLE_enum_definedList.append(DTC_TABLE_enum_definedStr)

		return DTC_TABLE_enum_definedList

	#创建DTC_MAX枚举
	def build_DTC_Index_enum_defined(self) -> list:
		DTC_IndexList = []
		DTC_IndexStr = "enum" + '\n'
		DTC_IndexStr += '{' + '\n'
		for ListValue in self.src_row_data_all:
			if (ListValue[0] == "NA" or ListValue[0] == "None"):
				if (ListValue[column_index_from_string('F') - 1].strip(' ') == "NA" or ListValue[column_index_from_string('F') - 1].strip(' ') == "None"):
					if ListValue[column_index_from_string('E') - 1].strip(' ') == "911717":
						DTC_IndexStr += '\t' + "DTC_BATTERY_VOLTAGE_HIGH_B111717," + '\n'
					elif ListValue[column_index_from_string('E') - 1].strip(' ') == "911716":
						DTC_IndexStr += '\t' + "DTC_BATTERY_VOLTAGE_LOW_B111716," + '\n'
					elif ListValue[column_index_from_string('E') - 1].strip(' ') == "E00141":
						DTC_IndexStr += '\t' + "DTC_EEP_CHECKSUM_ERROR," + '\n'
					elif ListValue[column_index_from_string('E') - 1].strip(' ') == "E00242":
						DTC_IndexStr += '\t' + "DTC_ECU_RAM_ERROR," + '\n'
					elif ListValue[column_index_from_string('E') - 1].strip(' ') == "962F42":
						DTC_IndexStr += '\t' + "DTC_EEP_NVM_ERROR," + '\n'
					#DTC_IndexStr += '\t' + "DTC_" + '_'.join(ListValue[column_index_from_string('J') - 1].split(' ')) + '_' + ListValue[column_index_from_string('I') - 1] + ',' + '\n'
				elif ListValue[column_index_from_string('F') - 1] == "NM":
					DTC_IndexStr += '\t' + '_'.join(ListValue[column_index_from_string('J') - 1].strip(' ').split(' ')) + ',' + '\n'
				else:
					DTC_IndexStr += '\t' + "DTC_" + ListValue[column_index_from_string('F') - 1].strip(' ') + "_BUSOFF_" + ListValue[column_index_from_string('I') - 1].strip(' ') + ',' + '\n'
			else:
				DTC_IndexStr += '\t' + "DTC_" + ListValue[column_index_from_string('B') - 1].strip(' ') + '_' + ListValue[column_index_from_string('A') - 1].strip(' ')[2:] + '_TIMEOUT_' \
							+ ListValue[column_index_from_string('I') - 1].strip(' ') + ','
				DTC_IndexStr += '\n'
		'''
		for ListValue in sort_src_row_data_all_Missing():
			DTC_IndexStr += '\t' + "DTC_" + ListValue[column_index_from_string('B') - 1].strip(' ') + '_' + ListValue[column_index_from_string('A') - 1].strip(' ')[2:] + '_TIMEOUT_' \
							+ ListValue[column_index_from_string('I') - 1] + ','
			DTC_IndexStr += '\n'
		'''
		DTC_IndexStr += '\t' + 'DTC_MAX' + '\n'
		DTC_IndexStr += '};' + '\n'
		DTC_IndexList.append(DTC_IndexStr)

		return DTC_IndexList

	def mkdir(self, path:str): 
	    # 去除首位空格、尾部\
	    path=path.strip()
	    # 判断结果
	    if not os.path.exists(path):
	        os.makedirs(path) 

	#主函数
	def main(self):
		# 读取指定列的数据
		dataFrame = read_excel(self.pathname, sheet_name="DTC", header=None, na_values="", usecols="A:J")
		# print(dataFrame)
		# 将Frame格式数据转换成列表
		self.src_row_data_all = dataFrame.fillna("None").values[2:].tolist()	
		# print(self.src_row_data_all)
		# 将表中int转为str
		self.dataHandling(self.src_row_data_all)
		# print(self.src_row_data_all)

		self.read_net2busoffDTCmapping()
		
		self.mkdir("output")
		# with open(self.pathname[:self.pathname.rfind('/')+1] + "DTCCfg.c",'w') as Cfile:
		with open("output/DTCCfg.c",'w') as Cfile:
			#将gDEM_taDTCCfgPattern数组写入
			for tmp in self.build_gDEM_taDTCCfgPattern_Array():
				Cfile.write(tmp)
			Cfile.write('\n'*2)
			for tmp in self.build_PB_Node_Missing_DTC_Tab_Array():
				Cfile.write(tmp)
			Cfile.write('\n'*2)
			for tmp in self.build_DTC_TABLE_enum_defined():
				Cfile.write(tmp)
			Cfile.write('\n'*2)
			for tmp in self.build_DTC_Index_enum_defined():
				Cfile.write(tmp)

		# print(self.Net2BusOffDTC)
		# print(sort_src_row_data_all_Missing())

		print("------------------Finished--------------------------")


if __name__ == '__main__':
	dtc_config = DtcConfig()
	dtc_config.get_file_pathname()
	dtc_config.main()


