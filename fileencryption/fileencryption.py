from base64 import b64encode, b64decode
from pyDes import des, CBC, PAD_PKCS5
from tkinter.filedialog import askopenfilename


class FileEncryption(object):
	'''文件加密'''
	def __init__(self):
		"""初始化数据"""
		self.Des_Key = "Wang+-*%" # Key
		self.Des_IV = b"\x19\x90\x07\x14\x06\x12\x08\x23" # 自定IV向量
		self.pathname = ""
		self.original_data = []

	def get_file_pathname(self):
		"""获取路由表路径"""
		self.pathname = askopenfilename(filetypes = [("hex",".hex")])
		if self.pathname == ():
			self.pathname = ""
		# print(self.pathname) 

	def read_file(self):
		"""读取hex"""
		if self.pathname != "":
			with open(self.pathname, "r") as file:
				for colData in file:
					self.original_data.append(colData)

			print(self.original_data[0:10])

	def encrypting(self, data:str):
		'''DES+base64加密'''
		k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
		data = bytes(data, encoding="utf-8")
		encryptStr = k.encrypt(data)
		# print(encryptStr)

		return str(b64encode(encryptStr), encoding="utf-8") #转base64编码返回

	def file_encryption(self):
		'''对读取的数据进行加密'''
		with open(self.pathname[self.pathname.rfind('/') + 1:self.pathname.rfind('.')] + "_encrypt" + self.pathname[self.pathname.rfind('.'):], "w") as file:
			# print(self.pathname[self.pathname.rfind('/'):self.pathname.rfind('.')] + "_encrypt" + self.pathname[self.pathname.rfind('.'):])
			for subdata in self.original_data:
				encript_data = self.encrypting(subdata[:-1])
				file.write(encript_data + '\n')


class FileDecryption(object):
	'''文件解密'''
	def __init__(self):
		"""初始化数据"""
		self.Des_Key = "Wang+-*%" # Key
		self.Des_IV = b"\x19\x90\x07\x14\x06\x12\x08\x23" # 自定IV向量

	def decrypting(self, data:str):
		'''DES+base64解密'''
		k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
		data = bytes(data, encoding="utf-8")
		data = b64decode(data)
		decryptStr = k.decrypt(data)

		return str(decryptStr, encoding="utf-8")


	def file_decryption(self, dataList):
		'''对读取的数据进行加密, dataList:字符串列表'''
		# with open("decrypt_test.hex", "w") as file:
		for i in range(len(dataList)):
			dataList[i] = self.decrypting(dataList[i][:-1]) + dataList[i][-1]
				# file.write(dataList[i])
				

if __name__ == '__main__':
	fileEncryption = FileEncryption()
	fileEncryption.get_file_pathname()
	fileEncryption.read_file()
	# fileEncryption.file_encryption()
	fileDecryption = FileDecryption()
	fileDecryption.file_decryption(fileEncryption.original_data)

	print("-----------------END-----------------------")


