import re
from openpyxl.utils import get_column_letter, column_index_from_string


class CheckError(object):
	'''错误检查'''
	def __init__(self):
		pass

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
		# 深拷贝一份路由数据，不破坏原有数据
		msgDataList = deepcopy(msgRoute.dataList)
		msgHeaderList = deepcopy(msgRoute.headerList)

		row = None # 对应于excel表的行
		col = None # 对应于excel表的列
		hint = "" # ""：没有错误

		ret = False

		for i in range(len(msgDataList)):
			row = i + 2
			if not self.id_is_hex(msgDataList[i][msgHeaderList.index("TxCANID")]):
				col = get_column_letter(msgHeaderList.index("TxCANID") + 1)
				hint = "发送报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)"
				break
			if not re.match("^[1-9]{1}[0-9]+$", msgDataList[i][signalHeaderList.index("TxPeriod")]):
				col = get_column_letter(msgHeaderList.index("TxPeriod") + 1)
				hint = "发送周期错误（填写十进制数字或NA)"
				break
			if not re.match("^[1-8]{1}$", msgDataList[i][msgHeaderList.index("TxDLC")]):
				col = get_column_letter(msgHeaderList.index("TxDLC") + 1)
				hint = "发送报文长度错误，请填写1-8"
				break
			if not re.match("^[0-6]{1}$", msgDataList[i][msgHeaderList.index("TxChannle")]):
				col = get_column_letter(msgHeaderList.index("TxChannle") + 1)
				hint = "发送报文通道错误，请填写0-6，0代表没有转发关系"
				break

			if not self.id_is_hex(msgDataList[i][msgHeaderList.index("RxCANID")]):
				col = get_column_letter(msgHeaderList.index("RxCANID") + 1)
				hint = "接收报文ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)"
				break
			if not re.match("^[1-9]{1}[0-9]+$", msgDataList[i][signalHeaderList.index("RxPeriod")]):
				col = get_column_letter(msgHeaderList.index("RxPeriod") + 1)
				hint = "接收报文周期错误（填写十进制数字或NA)"
				break
			if not re.match("^[1-8]{1}$", msgDataList[i][msgHeaderList.index("RxDLC")]):
				col = get_column_letter(msgHeaderList.index("RxDLC") + 1)
				hint = "接收报文长度错误，请填写1-8"
				break
			if not re.match("^[0-6]{1}$", msgDataList[i][msgHeaderList.index("RxChannel")]):
				col = get_column_letter(msgHeaderList.index("RxChannel") + 1)
				hint = "接收报文通道错误，请填写0-6，0代表没有转发关系"
				break

			if not self.id_is_hex(msgDataList[i][msgHeaderList.index("RxMsk")]):
				col = get_column_letter(msgHeaderList.index("RxMsk") + 1)
				hint = "接收报文掩码错误，请填写标准的十六进制格式(0x000-0xFFF)"
				break
			if not re.match("^[0-1]{1}$", msgDataList[i][msgHeaderList.index("RxInterrupt")]):
				col = get_column_letter(msgHeaderList.index("RxInterrupt") + 1)
				hint = "接收报文是否中断转发填写错误，请填写0或1，0代表不中断接收，1代表中断接收"
				break
			if not re.match("^[YN]{1}$", msgDataList[i][msgHeaderList.index("RxDTC")]):
				col = get_column_letter(msgHeaderList.index("RxDTC") + 1)
				hint = "接收报文是否作为节点丢失DTC判断条件填写错误，请填写Y或N，Y代表是节点丢失报文，N代表不是节点丢失报文"
				break
			if not re.match("^[0-3]{1}$", msgDataList[i][msgHeaderList.index("RouteCondiction")]):
				col = get_column_letter(msgHeaderList.index("RouteCondiction") + 1)
				hint = "接收报文路由条件填写错误，请填写0-3，一般为3"
				break

		if hint：
			ret = (row, col, hint)

		return ret

	def signal_literal_check(self, signalRoute):
		'''信号数据字面合法性检查'''
		# 深拷贝一份路由数据，不破坏原有数据
		signalDataList = deepcopy(signalRoute.dataList)
		signalHeaderList = deepcopy(signalRoute.headerList)

		row = None
		col = None 
		hint = "" # ""：没有错误

		ret = False

		for i in range(len(signalDataList)):
			row = i + 2
			if not self.id_is_hex(signalDataList[i][signalHeaderList.index("TxCANID")]):
				col = get_column_letter(msgHeaderList.index("TxCANID") + 1)
				hint = "发送信号ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)"
				break
			if not re.match("^[1-9]{1}[0-9]+$", signalDataList[i][signalHeaderList.index("TxPeriod")]):
				col = get_column_letter(msgHeaderList.index("TxPeriod") + 1)
				hint = "发送信号周期错误（填写十进制数字且大于10)"
				break
			if not re.match("^[1-8]{1}$", signalDataList[i][signalHeaderList.index("TxDLC")]):
				col = get_column_letter(msgHeaderList.index("TxDLC") + 1)
				hint = "发送报文长度错误，请填写1-8"
				break
			if not re.match("^[0-6]{1}$", signalDataList[i][signalHeaderList.index("TxChannle")]):
				col = get_column_letter(msgHeaderList.index("TxChannle") + 1)
				hint = "发送信号通道错误，请填写0-6，0代表没有转发关系"
				break
			if not (re.match("^[0-9]{1,2}$", signalDataList[i][signalHeaderList.index("TxStartBit")]) and (0 <= int(signalDataList[i][signalHeaderList.index("TxStartBit")]) <= 63)):
				col = get_column_letter(msgHeaderList.index("TxStartBit") + 1)
				hint = "发送信号起始位错误，请填写0-63"
				break
			if not re.match("^[1-9]{1}[0-9]?$", signalDataList[i][signalHeaderList.index("TxSigLen")] and (1 <= int(signalDataList[i][signalHeaderList.index("TxSigLen")]) <= 64)):
				col = get_column_letter(msgHeaderList.index("TxSigLen") + 1)
				hint = "发送信号长度错误，请填写1-64"
				break

			if not self.id_is_hex(signalDataList[i][signalHeaderList.index("RxCANID")]):
				col = get_column_letter(msgHeaderList.index("RxCANID") + 1)
				hint = "接收信号ID格式错误，请填写标准的十六进制格式(0x000-0xFFF)"
				break
			if not re.match("^[1-9]{1}[0-9]+$", signalDataList[i][signalHeaderList.index("RxPeriod")]):
				col = get_column_letter(msgHeaderList.index("RxPeriod") + 1)
				hint = "接收信号周期错误（填写十进制数字且大于10)"
				break
			if not re.match("^[1-8]{1}$", signalDataList[i][signalHeaderList.index("RxDLC")]):
				col = get_column_letter(msgHeaderList.index("RxDLC") + 1)
				hint = "接收报文长度错误，请填写1-8"
				break
			if not re.match("^[0-6]{1}$", signalDataList[i][signalHeaderList.index("RxChannel")]):
				col = get_column_letter(msgHeaderList.index("RxChannel") + 1)
				hint = "报文报文通道错误，请填写0-6，0代表没有转发关系"
				break
			if not (re.match("^[0-9]{1,2}$", signalDataList[i][signalHeaderList.index("RxStartBit")]) and (0 <= int(signalDataList[i][signalHeaderList.index("RxStartBit")]) <= 63)):
				col = get_column_letter(msgHeaderList.index("RxStartBit") + 1)
				hint = "接收信号起始位错误，请填写0-63"
				break
			if not (re.match("^[1-9]{1}[0-9]?$", signalDataList[i][signalHeaderList.index("RxSigLen")]) and (1 <= int(signalDataList[i][signalHeaderList.index("RxSigLen")]) <= 64)):
				col = get_column_letter(msgHeaderList.index("RxSigLen") + 1)
				hint = "接收信号长度错误，请填写1-64"
				break

			if not re.match("^[0-1]{1}$", signalDataList[i][signalHeaderList.index("ByteOrder")]):
				col = get_column_letter(msgHeaderList.index("ByteOrder") + 1)
				hint = "字节序错误，请填写0或1，0表示Motorola大端，1表示Intel小端"
				break
			if not re.match("^[YN]{1}$", signalDataList[i][signalHeaderList.index("RxDTC")]):
				col = get_column_letter(msgHeaderList.index("RxDTC") + 1)
				hint = "接收报文是否作为节点丢失DTC判断条件填写错误，请填写Y或N，Y代表是节点丢失报文，N代表不是节点丢失报文"
				break
			if not re.match("0x[0-9 A-F]+", signalDataList[i][signalHeaderList.index("inival")], flags=re.IGNORECASE):
				col = get_column_letter(msgHeaderList.index("inival") + 1)
				hint = "接收信号初始值填写错误，请填写标准的十六进制格式"
				break
			if not re.match("0x[0-9 A-F]+", signalDataList[i][signalHeaderList.index("dfVal")], flags=re.IGNORECASE):
				col = get_column_letter(msgHeaderList.index("dfVal") + 1)
				hint = "接收信号失效值填写错误，请填写标准的十六进制格式"
				break

		if hint：
			ret = (row, col, hint)

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
