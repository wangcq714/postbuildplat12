import re


class CheckError(object):
	'''错误检查'''
	def __init__(self):
		# 深拷贝一份路由数据，不破坏原有数据
		self.msgDataList = deepcopy(msgRoute.dataList)
		self.msgHeaderList = deepcopy(msgRoute.headerList)
		self.signalDataList = deepcopy(signalRoute.dataList)
		self.signalHeaderList = deepcopy(signalRoute.headerList)

	def id_is_hex(self, data:str):
		'''判断你是否为16进制'''
		if re.match("^0x(([0-9 A-F]{1,2})|([0-7]{1}[0-9 A-F]{2}))$", data, flags=re.IGNORECASE):
			# print("合法")
			return True
		else:
			print(data, "不合法")
			return False

	def msg_literal_check(self, msgRoute):
		'''报文数据字面合法性检查'''
		ret = "None" # 0：没有错误

		for i in range(len(self.msgDataList)):
			if not self.id_is_hex(self.msgDataList[i][self.msgHeaderList.index("TxCANID")]):
				ret = "TxCANID" # 1：发送报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)
				break
			if not re.match("^[1-9]{1}[0-9]+$", self.msgDataList[i][self.signalHeaderList.index("TxPeriod")]):
				ret = "TxPeriod" # 2：发送周期错误（填写十进制数字或NA)
				break
			if not re.match("^[1-8]{1}$", self.msgDataList[i][self.msgHeaderList.index("TxDLC")]):
				ret = "TxDLC" # 3：发送报文长度错误，请填写1-8
				break
			if not re.match("^[0-6]{1}$", self.msgDataList[i][self.msgHeaderList.index("TxChannle")]):
				ret = "TxChannle" # 4：发送报文通道错误，请填写0-6，0代表没有转发关系
				break

			if not self.id_is_hex(self.msgDataList[i][self.msgHeaderList.index("RxCANID")]):
				ret = "RxCANID" # 5：接收报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)
				break
			if not re.match("^[1-9]{1}[0-9]+$", self.msgDataList[i][self.signalHeaderList.index("RxPeriod")]):
				ret = "RxPeriod" # 6：接收报文周期错误（填写十进制数字或NA)
				break
			if not re.match("^[1-8]{1}$", self.msgDataList[i][self.msgHeaderList.index("RxDLC")]):
				ret = "RxDLC" # 7：接收报文长度错误，请填写1-8
				break
			if not re.match("^[0-6]{1}$", self.msgDataList[i][self.msgHeaderList.index("RxChannel")]):
				ret = "RxChannel" # 8：接收报文通道错误，请填写0-6，0代表没有转发关系
				break

			if not self.id_is_hex(self.msgDataList[i][self.msgHeaderList.index("RxMsk")]):
				ret = "RxMsk" # 9：接收报文掩码错误，请填写标准的十六进制格式(0x000-0xFFF)
				break
			if not re.match("^[0-1]{1}$", self.msgDataList[i][self.msgHeaderList.index("RxInterrupt")]):
				ret = "RxInterrupt" # 10：接收报文是否中断转发填写错误，请填写0或1，0代表不中断接收，1代表中断接收
				break
			if not re.match("^[YN]{1}$", self.msgDataList[i][self.msgHeaderList.index("RxDTC")]):
				ret = "RxDTC" # 11：接收报文是否作为节点丢失DTC判断条件填写错误，请填写Y或N，Y代表是节点丢失报文，N代表不是节点丢失报文
				break
			if not re.match("^[0-3]{1}$", self.msgDataList[i][self.msgHeaderList.index("RouteCondiction")]):
				ret = "RouteCondiction" # 11：接收报文路由条件填写错误，请填写0-3，一般为3
				break

		return ret, i

	def signal_literal_check(self, signalRoute):
		'''信号数据字面合法性检查'''
		ret = "None" # 0：没有错误

		for i in range(len(self.signalDataList)):
			if not self.id_is_hex(self.signalDataList[i][self.signalHeaderList.index("TxCANID")]):
				ret = "TxCANID" # 1：发送报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)
				break
			if not re.match("^[1-9]{1}[0-9]+$", self.signalDataList[i][self.signalHeaderList.index("TxPeriod")]):
				ret = "TxPeriod" # 2：发送周期错误（填写十进制数字且大于10)
				break
			if not re.match("^[1-8]{1}$", self.signalDataList[i][self.signalHeaderList.index("TxDLC")]):
				ret = "TxDLC" # 3：发送报文长度错误，请填写1-8
				break
			if not re.match("^[0-6]{1}$", self.signalDataList[i][self.signalHeaderList.index("TxChannle")]):
				ret = "TxChannle" # 4：发送报文通道错误，请填写0-6，0代表没有转发关系
				break
			if not (re.match("^[0-9]{1,2}$", self.signalDataList[i][self.signalHeaderList.index("TxStartBit")]) and (0 <= int(self.signalDataList[i][self.signalHeaderList.index("TxStartBit")]) <= 63)):
				ret = "TxStartBit" # 5：发送信号起始位错误，请填写0-63
				break
			if not re.match("^[1-9]{1}[0-9]?$", self.signalDataList[i][self.signalHeaderList.index("TxSigLen")] and (1 <= int(self.signalDataList[i][self.signalHeaderList.index("TxSigLen")]) <= 64)):
				ret = "TxSigLen" # 6：发送信号长度错误，请填写1-64
				break

			if not self.id_is_hex(self.signalDataList[i][self.signalHeaderList.index("RxCANID")]):
				ret = "RxCANID" # 7：接收报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)
				break
			if not re.match("^[1-9]{1}[0-9]+$", self.signalDataList[i][self.signalHeaderList.index("RxPeriod")]):
				ret = "RxPeriod" # 8：接收信号周期错误（填写十进制数字且大于10)
				break
			if not re.match("^[1-8]{1}$", self.signalDataList[i][self.signalHeaderList.index("RxDLC")]):
				ret = "RxDLC" # 9：发送报文长度错误，请填写1-8
				break
			if not re.match("^[0-6]{1}$", self.signalDataList[i][self.signalHeaderList.index("RxChannel")]):
				ret = "RxChannel" # 10：发送报文通道错误，请填写0-6，0代表没有转发关系
				break
			if not (re.match("^[0-9]{1,2}$", self.signalDataList[i][self.signalHeaderList.index("RxStartBit")]) and (0 <= int(self.signalDataList[i][self.signalHeaderList.index("RxStartBit")]) <= 63)):
				ret = "RxStartBit" # 11：发送信号起始位错误，请填写0-63
				break
			if not (re.match("^[1-9]{1}[0-9]?$", self.signalDataList[i][self.signalHeaderList.index("RxSigLen")]) and (1 <= int(self.signalDataList[i][self.signalHeaderList.index("RxSigLen")]) <= 64)):
				ret = "RxSigLen" # 12：发送信号长度错误，请填写1-64
				break

			if not re.match("^[0-1]{1}$", self.signalDataList[i][self.signalHeaderList.index("ByteOrder")]):
				ret = "ByteOrder" # 13：字节序错误，请填写0或1，0表示Motorola大端，1表示Intel小端
				break
			if not re.match("^[YN]{1}$", self.signalDataList[i][self.signalHeaderList.index("RxDTC")]):
				ret = "RxDTC" # 14：接收报文是否作为节点丢失DTC判断条件填写错误，请填写Y或N，Y代表是节点丢失报文，N代表不是节点丢失报文
				break
			if not re.match("0x[0-9 A-F]+", self.signalDataList[i][self.signalHeaderList.index("inival")], flags=re.IGNORECASE):
				ret = "inival" # 15：接收信号初始值填写错误，请填写标准的十六进制格式
				break
			if not re.match("0x[0-9 A-F]+", self.signalDataList[i][self.signalHeaderList.index("dfVal")], flags=re.IGNORECASE):
				ret = "dfVal" # 16：接收信号失效值填写错误，请填写标准的十六进制格式
				break

		return ret

	def msg_literal_check(self, msgRoute):
		'''报文数据逻辑性检查'''
		pass

	def signal_literal_check(self, signalRoute):
		'''信号数据逻辑性检查'''
		pass



if __name__ == '__main__':
	checkError = CheckError()
	for i in range(int("0x800", 16)):
		checkError.id_is_hex(hex(i))
	# checkError.is_dec("None")
