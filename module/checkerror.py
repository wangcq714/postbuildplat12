import re

class CheckError(object):
	'''错误检查'''
	def __init__(self):
		pass

	def is_hex(self):
		'''判断你是否为16进制'''


	def msg_check(self, msgRoute):
		'''报文数据检查'''
		# 深拷贝一份路由数据，不破坏原有数据
		msgDataList = deepcopy(msgRoute.dataList)
		msgHeaderList = deepcopy(msgRoute.headerList)


		ret = 0

		for i in range(len(msgDataList)):
			if msgDataList[i][msgHeaderList.index("TxCANID")].startswith("0x") or msgDataList[i][msgHeaderList.index("TxCANID")].startswith("0X"):
				if not re.match("[0-9 A-F]{1,3}", msgDataList[i][msgHeaderList.index("TxCANID")][2:]):

			elif:
				ret = 1 # 发送ID格式错误，请填写标准的十六进制格式






		






	def signal_check(self, signalRoute):
		'''信号数据检查'''
		# 深拷贝一份路由数据，不破坏原有数据
		signalDataList = deepcopy(signalRoute.dataList)
		signalHeaderList = deepcopy(signalRoute.headerList)



