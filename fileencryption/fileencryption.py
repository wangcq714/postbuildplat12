from base64 import b64encode, b64decode
from pyDes import des, CBC, PAD_PKCS5
from tkinter.filedialog import askopenfilename
from multiprocessing import Pool, Manager
import time
from Crypto.Cipher import AES


def calc_run_time(func):
	'''计算函数运行时间'''
	def wrapper(*args, **kwargs):
		start_time = time.time()
		ret = func(*args, **kwargs)
		stop_time = time.time()
		print("runtime = {}".format(stop_time - start_time))
		return ret
	return wrapper


class FileEncryption(object):
	'''文件加密'''
	def __init__(self):
		"""初始化数据"""
		self.Des_Key = "Wang+-*%" # Key
		self.Des_IV = b"\x19\x90\x07\x14\x06\x12\x08\x23" # 自定IV向量
		self.pathname = ""
		self.original_data = []

		self.Aes_Key = bytes("keyskeyskeyskeys", encoding="utf-8")
		self.Aes_IV = bytes("keyskeyskeyskeys", encoding="utf-8")

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

	def encrypt_des(self, data:str):
		'''DES+base64加密'''
		k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
		data = bytes(data, encoding="utf-8")
		encryptStr = k.encrypt(data)
		# print(encryptStr)

		return str(b64encode(encryptStr), encoding="utf-8") #转base64编码返回

	def encrypt_aes(self, data):
		BS = 16
		pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
		cipher = AES.new(self.Aes_Key, AES.MODE_CBC, self.Aes_IV)
		en_data = cipher.encrypt(bytes(pad(data), encoding="utf-8"))
		en_data = b64encode(en_data)

		return str(en_data, encoding="utf-8")

	@calc_run_time
	def file_encryption(self):
		'''对读取的数据进行加密'''
		with open(self.pathname[self.pathname.rfind('/') + 1:self.pathname.rfind('.')] + "_encrypt_aes" + self.pathname[self.pathname.rfind('.'):], "w") as file:
			# print(self.pathname[self.pathname.rfind('/'):self.pathname.rfind('.')] + "_encrypt" + self.pathname[self.pathname.rfind('.'):])
			for subdata in self.original_data:
				# encript_data = self.encrypting(subdata[:-1])
				encript_data = self.encrypt_aes(subdata[:-1])
				file.write(encript_data + '\n')


class FileDecryption(object):
	'''文件解密'''
	def __init__(self):
		"""初始化数据"""
		self.Des_Key = "Wang+-*%" # Key
		self.Des_IV = b"\x19\x90\x07\x14\x06\x12\x08\x23" # 自定IV向量

		self.Aes_Key = bytes("keyskeyskeyskeys", encoding="utf-8")
		self.Aes_IV = bytes("keyskeyskeyskeys", encoding="utf-8")

	def decrypt_des(self, data:str):
		'''DES+base64解密'''
		k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
		data = bytes(data, encoding="utf-8")
		data = b64decode(data)
		decryptStr = k.decrypt(data)

		return str(decryptStr, encoding="utf-8")

	def decrypt_aes(self, en_data):
		en_data = b64decode(en_data)
		unpad = lambda s: s[0:-s[-1]]
		cipher = AES.new(self.Aes_Key, AES.MODE_CBC, self.Aes_IV)
		de_data = unpad(cipher.decrypt(en_data))

		# return de_data.decode('utf-8')
		return str(de_data, encoding="utf-8")



	@calc_run_time
	def file_decryption(self, dataList):
		'''对读取的数据进行加密, dataList:字符串列表'''
		# with open("decrypt_test_aes.hex", "w") as file:
			# print(len(dataList))
		for i in range(len(dataList)):
			dataList[i] = self.decrypt_aes(dataList[i][:-1]) + dataList[i][-1]
			# file.write(dataList[i])

	def __file_decryption(self, dataList, num, queue):
		'''对读取的数据进行加密, dataList:字符串列表'''
		print(num, len(dataList))
		res = []
		for i in range(len(dataList)):
			res.append(self.decrypting(dataList[i][:-1]) + dataList[i][-1])
		queue.put((num, res))
		print(num, res[0])


	@calc_run_time
	def file_file_decryption_multithread(self, dataList):
		'''多进程解密'''
		print(len(dataList))
		processer = 2
		pool = Pool(processer)
		queue = Manager().Queue()
		for i in range(processer):
			pool.apply_async(self.__file_decryption, args=(dataList[len(dataList)*i//processer:len(dataList)*(i+1)//processer], i, queue))
		pool.close()
		pool.join()




if __name__ == '__main__':
	fileEncryption = FileEncryption()
	fileEncryption.get_file_pathname()
	fileEncryption.read_file()
	fileEncryption.file_encryption()
	fileDecryption = FileDecryption()
	# fileDecryption.file_decryption(fileEncryption.original_data)
	# fileDecryption.file_file_decryption_multithread(fileEncryption.original_data)

	print("-----------------END-----------------------")


