from module import readdata
from module import buildtable
from module import writedata
from module import checkerror
from ui import ui
from register import register
from header import id2indextableheader
from header import projcancfgheader
from header import projpostbuildcfgheader
from fileencryption import fileencryption


def run(config, msgRoute, signalRoute, readHex):
	# 读取数据
	# config.read_data()
	if config.platInfo == "MAXUS":
		msgRoute.read_data("Q")
	else:
		msgRoute.read_data("O")

	if config.platInfo == "Qoros_C6M0":
		signalRoute.read_data("U")
		# print(signalRoute.dataList)
	else:
		signalRoute.read_data("T")

	readHex.read_hex()

	# 数据合法性检查
	# 创建数据检查模块
	checkError = checkerror.CheckError(config)
	# 字面上合法性校验
	ret = checkError.msg_literal_check(msgRoute)
	if ret:
		return ret
	ret = checkError.signal_literal_check(signalRoute)
	if ret:
		return ret
	# 逻辑上合法性检校验
	ret = checkError.msg_logic_check(msgRoute)
	if ret:
		return ret
	ret = checkError.signal_logic_check(signalRoute)
	if ret:
		return ret
	# 报文和信号一致性混合校验
	ret = checkError.msgsignal_logic_check(msgRoute, signalRoute)
	if ret:
		return ret

	# 加密hex文件解密(此处DES耗时会很长，AES比较快)
	try:
		fileDecryption = fileencryption.FileDecryption()
		fileDecryption.file_decryption(readHex.hexData)
	except:
		return "DecryptionError"

	

	# 中断MO初始化表
	canFullIdNameISR = buildtable.CanFullIdNameISR(config)
	canFullIdNameISR.get_valid_data(msgRoute, signalRoute)
	canFullIdNameISR.data_handle()
	canFullIdNameISR.build_table()
	canFullIdNameISR.build_table_len_hex_data(len(canFullIdNameISR.CanFullIDNameISRList))
	canFullIdNameISR.modify_hex_data(readHex.hexData, canFullIdNameISR.tableLenAddr, 1, canFullIdNameISR.lenHexDataList)
	canFullIdNameISR.build_hex_data(canFullIdNameISR.CanFullIDNameISRList)
	canFullIdNameISR.modify_hex_data(readHex.hexData, canFullIdNameISR.tableAddr, canFullIdNameISR.structLen*canFullIdNameISR.tableLen, canFullIdNameISR.hexDataList)

	# 中断轮询表
	pbDirectRoutingTable = buildtable.PbDirectRoutingTable(config)
	pbDirectRoutingTable.get_valid_data(msgRoute, signalRoute)
	pbDirectRoutingTable.data_handle()
	pbDirectRoutingTable.build_table()
	pbDirectRoutingTable.build_table_len_hex_data(len(pbDirectRoutingTable.routerTableISRList))
	pbDirectRoutingTable.modify_hex_data(readHex.hexData, pbDirectRoutingTable.tableLenAddr, 1, pbDirectRoutingTable.lenHexDataList)
	pbDirectRoutingTable.build_hex_data([subList[1:-3] for subList in pbDirectRoutingTable.routerTableISRList])
	pbDirectRoutingTable.modify_hex_data(readHex.hexData, pbDirectRoutingTable.tableAddr, pbDirectRoutingTable.structLen*pbDirectRoutingTable.tableLen, pbDirectRoutingTable.hexDataList)

	# 报文轮询表
	pbMsgRoutingTable = buildtable.PbMsgRoutingTable(config)
	pbMsgRoutingTable.get_valid_data(msgRoute, signalRoute)
	pbMsgRoutingTable.data_handle()
	pbMsgRoutingTable.build_table()
	pbMsgRoutingTable.build_table_len_hex_data(len(pbMsgRoutingTable.routerTableFIFOList))
	pbMsgRoutingTable.modify_hex_data(readHex.hexData, pbMsgRoutingTable.tableLenAddr, 1, pbMsgRoutingTable.lenHexDataList)
	pbMsgRoutingTable.build_hex_data([subList[1:-3] for subList in pbMsgRoutingTable.routerTableFIFOList])
	pbMsgRoutingTable.modify_hex_data(readHex.hexData, pbMsgRoutingTable.tableAddr, pbMsgRoutingTable.structLen*pbMsgRoutingTable.tableLen, pbMsgRoutingTable.hexDataList)

	# 信号报文接收表
	pbMsgRecvTable = buildtable.PbMsgRecvTable(config)
	pbMsgRecvTable.get_valid_data(signalRoute)
	pbMsgRecvTable.data_handle()
	pbMsgRecvTable.build_table()
	pbMsgRecvTable.build_table_len_hex_data(len(pbMsgRecvTable.PBMsgRecvTableList))
	pbMsgRecvTable.modify_hex_data(readHex.hexData, pbMsgRecvTable.tableLenAddr, 1, pbMsgRecvTable.lenHexDataList)
	pbMsgRecvTable.build_hex_data(pbMsgRecvTable.PBMsgRecvTableList)
	pbMsgRecvTable.modify_hex_data(readHex.hexData, pbMsgRecvTable.tableAddr, pbMsgRecvTable.structLen*pbMsgRecvTable.tableLen, pbMsgRecvTable.hexDataList)

	# 信号路由表
	pbSignalRoutingTable = buildtable.PbSignalRoutingTable(config)
	pbSignalRoutingTable.get_valid_data(signalRoute)
	pbSignalRoutingTable.data_handle()
	pbSignalRoutingTable.build_table()
	pbSignalRoutingTable.build_hex_data(pbSignalRoutingTable.PbSignalRoutingTableList)
	pbSignalRoutingTable.modify_hex_data(readHex.hexData, pbSignalRoutingTable.tableAddr, pbSignalRoutingTable.structLen*pbSignalRoutingTable.tableLen, pbSignalRoutingTable.hexDataList)

	# 信号报文发送表
	pbMsgSendTable = buildtable.PbMsgSendTable(config)
	pbMsgSendTable.get_valid_data(signalRoute)
	pbMsgSendTable.data_handle()
	pbMsgSendTable.build_table()
	pbMsgSendTable.build_hex_data(pbMsgSendTable.PbMsgSendTableList)
	pbMsgSendTable.modify_hex_data(readHex.hexData, pbMsgSendTable.tableAddr, pbMsgSendTable.structLen*pbMsgSendTable.tableLen, pbMsgSendTable.hexDataList)

	# 目标信号对应源信号ID索引
	pbMsgSrcTable = buildtable.PbMsgSrcTable(config)
	pbMsgSrcTable.get_valid_data(signalRoute)
	pbMsgSrcTable.data_handle()
	pbMsgSrcTable.build_table()
	if config.platInfo == "CHJ" or config.platInfo == "MAXUS":
		pbMsgSrcTable.build_hex_data(pbMsgSrcTable.PbMsgSrcTableList)
		pbMsgSrcTable.modify_hex_data(readHex.hexData, pbMsgSrcTable.tableAddr, pbMsgSrcTable.structLen*pbMsgSrcTable.tableLen, pbMsgSrcTable.hexDataList)

	# 信号报文发送调度表
	pbMsgSendSchedule = buildtable.PbMsgSendSchedule(config)
	pbMsgSendSchedule.get_valid_data(signalRoute)
	pbMsgSendSchedule.data_handle()
	pbMsgSendSchedule.build_table()
	pbMsgSendSchedule.build_hex_data(pbMsgSendSchedule.PbMsgSendSchedule)
	pbMsgSendSchedule.modify_hex_data(readHex.hexData, pbMsgSendSchedule.tableAddr, pbMsgSendSchedule.structLen*pbMsgSendSchedule.tableLen, pbMsgSendSchedule.hexDataList)

	# 信号初始值
	pbMsgRevInitVal = buildtable.PbMsgRevInitVal(config)
	pbMsgRevInitVal.get_valid_data(signalRoute)
	pbMsgRevInitVal.data_handle()
	pbMsgRevInitVal.build_table()
	pbMsgRevInitVal.build_hex_data(pbMsgRevInitVal.PbMsgRevInitValList)
	pbMsgRevInitVal.modify_hex_data(readHex.hexData, pbMsgRevInitVal.tableAddr, pbMsgRevInitVal.structLen*pbMsgRevInitVal.tableLen, pbMsgRevInitVal.hexDataList)

	# 信号失效值
	pbMsgRevDefaultVal = buildtable.PbMsgRevDefaultVal(config)
	pbMsgRevDefaultVal.get_valid_data(signalRoute)
	pbMsgRevDefaultVal.data_handle()
	pbMsgRevDefaultVal.build_table()
	pbMsgRevDefaultVal.build_hex_data(pbMsgRevDefaultVal.PbMsgRevDefaultVal)
	pbMsgRevDefaultVal.modify_hex_data(readHex.hexData, pbMsgRevDefaultVal.tableAddr, pbMsgRevDefaultVal.structLen*pbMsgRevDefaultVal.tableLen, pbMsgRevDefaultVal.hexDataList)

	# 报文索引
	id2IndexTable = buildtable.Id2IndexTable(config)
	id2IndexTable.get_valid_data(msgRoute, signalRoute)
	id2IndexTable.data_handle()
	id2IndexTable.build_table()
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableA])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrA, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableB])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrB, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableC])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrC, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableD])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrD, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableE])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrE, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableF])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrF, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)


	# 创建写文件对象
	writeData = writedata.WriteData()	

	# 只有当用户模式为开发者模式时才会生成配置表文件；客户模式下只可操作加密hex.
	if config.user_type == "Developer":
		# 写入Table.c文件
		if config.platInfo == "GAW1.2_OldPlatform" or config.platInfo == "Qoros_C6M0" or config.platInfo == "CHJ" or config.platInfo == "MAXUS":
			writeData.write_table_c(canFullIdNameISR.CAN_FULL_ID_NAME_ISR)
			writeData.write_table_c(pbDirectRoutingTable.PB_DirectRoutingTable)
			writeData.write_table_c(pbMsgRoutingTable.PB_MsgRoutingTable)
			writeData.write_table_c(pbMsgRecvTable.PB_Msg_Recv_Table)
			writeData.write_table_c(pbSignalRoutingTable.PB_Signal_Routing_Table)
			writeData.write_table_c(pbMsgSendTable.PB_Msg_Send_Table)
			writeData.write_table_c(pbMsgSrcTable.PB_Msg_Src_Table)
			writeData.write_table_c(pbMsgSendSchedule.PB_Msg_Send_Schedule)
			# writeData.write_table_c(id2IndexTable.id2index_table_a)
			# writeData.write_table_c(id2IndexTable.id2index_table_b)
			# writeData.write_table_c(id2IndexTable.id2index_table_c)
			# writeData.write_table_c(id2IndexTable.id2index_table_d)
			# writeData.write_table_c(id2IndexTable.id2index_table_e)
			# writeData.write_table_c(id2IndexTable.id2index_table_f)
			writeData.write_table_c(pbMsgRevInitVal.PB_MsgRevInitVal)
			writeData.write_table_c(pbMsgRevDefaultVal.PB_MsgRevDefaultVal)
			writeData.write_table_c(id2IndexTable.id2index_table_a)
			writeData.write_table_c(id2IndexTable.id2index_table_b)
			writeData.write_table_c(id2IndexTable.id2index_table_c)
			writeData.write_table_c(id2IndexTable.id2index_table_d)
			writeData.write_table_c(id2IndexTable.id2index_table_e)
			writeData.write_table_c(id2IndexTable.id2index_table_f)

			writeData.write_id2index_table_c(id2indextableheader.id2indextable_headerList, id2IndexTable.id2index_table)
		
		if config.platInfo == "GAW1.2_NewPlatform":
			# 写入中断初始化文件Proj_Can_Cfg.c
			writeData.write_proj_can_cfg_c(projcancfgheader.projcancfg_headerList, canFullIdNameISR.CAN_FULL_ID_NAME_ISR)

			# 写入Proj_PostBuild_Cfg.c
			writeData.write_proj_postbuild_cfg_c(projpostbuildcfgheader.projpostbuildcfg_headerList)
			writeData.write_proj_postbuild_cfg_c(pbDirectRoutingTable.PB_DirectRoutingTable)
			writeData.write_proj_postbuild_cfg_c(pbMsgRoutingTable.PB_MsgRoutingTable)
			writeData.write_proj_postbuild_cfg_c(pbMsgRecvTable.PB_Msg_Recv_Table)
			writeData.write_proj_postbuild_cfg_c(pbSignalRoutingTable.PB_Signal_Routing_Table)
			writeData.write_proj_postbuild_cfg_c(pbMsgSendTable.PB_Msg_Send_Table)
			writeData.write_proj_postbuild_cfg_c(pbMsgSendSchedule.PB_Msg_Send_Schedule)
			writeData.write_proj_postbuild_cfg_c(pbMsgRevInitVal.PB_MsgRevInitVal)
			writeData.write_proj_postbuild_cfg_c(pbMsgRevDefaultVal.PB_MsgRevDefaultVal)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_a)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_b)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_c)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_d)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_e)
			writeData.write_proj_postbuild_cfg_c(id2IndexTable.id2index_table_f)

	# 写入hex
	writeData.write_hex(readHex.hexData)

	

	print("------------------END-------------------")

	return "Success"


def ui_main():
	'''UI版'''
	# 创建配置信息对象
	config = readdata.Config()
	config.read_data()
	# 创建普通报文对象
	msgRoute = readdata.MsgRoute()
	# 创建信号报文对象
	signalRoute = readdata.SignalRoute()
	# 创建一个读hex对象
	readHex = readdata.ReadHex()
	# 创建一个校验是否注册类
	reg = register.Register()
	# 创建一个界面类
	my_main_window = ui.MyWindow(config, msgRoute, signalRoute, readHex, reg, run)
	# 初始会主界面参数
	my_main_window.setup()
	# 主界面显示
	my_main_window.show()


def cmd_main():
	'''命令行版'''
	# 创建配置信息对象
	config = readdata.Config()
	config.read_data()

	# 创建普通报文对象
	msgRoute = readdata.MsgRoute()
	msgRoute.get_file_pathname()

	# 创建信号报文对象
	signalRoute = readdata.SignalRoute()
	signalRoute.get_file_pathname()

	# 创建一个读hex对象
	readHex = readdata.ReadHex()
	readHex.get_file_pathname()

	run(config, msgRoute, signalRoute, readHex)


# if __name__ == '__main__':
# 	# cmd_main()
# 	ui_main()

ui_main()
