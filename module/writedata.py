import os

from platform import system

class WriteData(object):
	"""write"""
	def __init__(self):
		self.first_open_table_c = False
		self.first_open_proj_postbuild_cfg_c = False
	
	def mkdir(self, path:str): 
	    # 去除首位空格、尾部\
	    path=path.strip()
	    # 判断结果
	    if not os.path.exists(path):
	        os.makedirs(path) 

	def write_table_c(self, dataList):
		"""写入Table.c文件"""
		# 如果第一次写入，新建一个.c文件，否则接续写
		self.mkdir("output")
		if self.first_open_table_c == False:
			self.first_open_table_c = True
			with open("output/Table.c",'w') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)
		else:
			with open("output/Table.c",'a') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)

	def write_id2index_table_c(self, headerList, dataList):
		"""写入id2index_table.c"""
		self.mkdir("output")
		with open("output/id2index_table.c",'w') as Cfile:
				for tmp in headerList:
					Cfile.write(tmp)

				for tmp in dataList:
					Cfile.write(tmp)

	def write_proj_can_cfg_c(self, headerList, dataList):
		"""写入proj_can_cfg.c文件"""
		self.mkdir("output")
		with open("output/Proj_Can_Cfg.c",'w') as Cfile:
			for tmp in headerList:
				Cfile.write(tmp)

			for tmp in dataList:
				Cfile.write(tmp)
			Cfile.write("\n"*2)

	def write_proj_postbuild_cfg_c(self, dataList):
		"""写入proj_postbuild_cfg.c文件"""
		self.mkdir("output")
		# 如果第一次写入，新建一个.c文件，否则接续写
		if self.first_open_proj_postbuild_cfg_c == False:
			self.first_open_proj_postbuild_cfg_c = True
			with open("output/Proj_PostBuild_Cfg.c",'w') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)
		else:
			with open("output/Proj_PostBuild_Cfg.c",'a') as Cfile:
				for tmp in dataList:
					Cfile.write(tmp)
				Cfile.write("\n"*2)

	@staticmethod
	def checksum(dataList):
		"""计算校验和"""
		# for tmpStr in dataList:
		for i in range(len(dataList)):
			sum = 0
			for j in range(len(dataList[i][1:-3])//2):
				sum += int("0x" + dataList[i][1+j*2:1+j*2+2], 16)
				sum %= 256
			if sum != 0: 
				sum = 256 - sum
			# print(sum)
			dataList[i] = dataList[i][0:-3] +  "{0:02X}".format(sum) + dataList[i][-1]

	def write_hex(self, dataList):
		"""写hex文件"""
		if dataList != []:
			self.checksum(dataList)
			print(dataList[0:10])
			self.mkdir("output")
			with open("output/kanwairen.hex",'w') as hexf:
				for tmp in dataList:
					if system() == "Linux":
						hexf.write(tmp[0:-1])
						hexf.write("\r\n")
					elif system() == "Windows":
						hexf.write(tmp)



