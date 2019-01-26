# import platform
import os
from platform import system
# import ctypes
from ctypes import cdll, create_string_buffer
# import base64
from base64 import b64encode
from pyDes import des, CBC, PAD_PKCS5


if system() == "Windows":
    import wmi
    import json


class Register(object):
    def __init__(self):
        self.Des_Key = "Wang+-*%" # Key
        self.Des_IV = b"\x19\x90\x07\x14\x06\x12\x08\x23" # 自定IV向量
        self.authored_result = False
        if system() == "Windows":
            self.wm = wmi.WMI()

    
    # cpu 序列号
    def get_CPU_info(self):
        if system() == "Windows":
            cpu = []
            cp = self.wm.Win32_Processor()
            for u in cp:
                cpu.append(
                    {
                        "Name": u.Name,
                        "Serial Number": u.ProcessorId,
                        "CoreNum": u.NumberOfCores
                    }
                )
            # print(":::CPU info:", json.dumps(cpu))
            # print(cpu[0]["Serial Number"])
            return cpu[0]["Serial Number"]
        elif system() == "Linux":
            return ""

    # 硬盘序列号  
    def get_disk_info(self):
        if system() == "Windows":
            disk = []
            for pd in self.wm.Win32_DiskDrive():
                disk.append(
                    { 
                        "Serial": self.wm.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(), # 获取硬盘序列号，调用另外一个win32 API
                        "ID": pd.deviceid,
                        "Caption": pd.Caption,
                        "size": str(int(float(pd.Size)/1024/1024/1024))+"G"
                    }
                )
            # print(":::Disk info:", json.dumps(disk))
            # print(disk[0]["Serial"])
            return disk[0]["Serial"]
        elif system() == "Linux":
            #调用库
            ll = cdll.LoadLibrary
            if __name__ != '__main__':
                lib = cdll.LoadLibrary("./register/libpycalldiskinfo.so")  #调用so
            else:
                lib = cdll.LoadLibrary("./libpycalldiskinfo.so")  #调用so
            hardseri = create_string_buffer(19) #申请出参的内存大小
            lib.get_disk_serial_no(hardseri)
            # print (hardseri.raw)    #出参的访问方式
            disk_info = str(hardseri.raw, encoding = "utf-8")
            # print(disk_info)

            return disk_info

    # mac 地址（包括虚拟机的）
    def get_network_info(self):
        if system() == "Windows":
            network = []
            for nw in self.wm.Win32_NetworkAdapterConfiguration ():  # IPEnabled=0
                if nw.MACAddress != None:
                    network.append(
                        {
                            "MAC": nw.MACAddress,  # 无线局域网适配器 WLAN 物理地址
                            "ip": nw.IPAddress
                        }
                    )
            # print(":::Network info:", json.dumps(network))
            # print(network[0]["MAC"])
            return network[0]["MAC"]
        elif system() == "Linux":
            return ""

    # 主板序列号
    def get_mainboard_info(self):
        if system() == "Windows":
            mainboard=[]
            for board_id in self.wm.Win32_BaseBoard ():
                mainboard.append(board_id.SerialNumber.strip().strip('.'))
            # print(mainboard[0])
            return mainboard[0]   
        elif system() == "Linux":
            return "" 
   
    # 获得机器码
    def getmachinecode(self):
        # mac = self.get_network_info()
        mac = ""
        # cpu_serial_no = self.get_CPU_info()
        cpu_serial_no = ""
        disk_seral_no = self.get_disk_info()
        mainboard_seral_no = self.get_mainboard_info()
        machinecode_str = ""
        machinecode_str = machinecode_str + mac + cpu_serial_no + disk_seral_no + mainboard_seral_no
        # selectindex=[15,30,32,38,43,46]
        # macode=""
        # for i in selectindex:
            # macode=macode+machinecode_str[i]
        # print(macode)
        print(machinecode_str)
        return machinecode_str


    #DES+base64加密
    def Encrypted(self,tr):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(tr)
        # print('注册码：', b64encode(EncryptStr))
        return b64encode(EncryptStr) #转base64编码返回

    def mkdir(self, path:str): 
        # 去除首位空格、尾部\
        path=path.strip()
        # 判断结果
        if not os.path.exists(path):
            os.makedirs(path)

    #获取注册码，验证成功后生成注册文件
    def regist(self, reg_code):
        # key = input('please input your register code: ')
        key = reg_code
        #由于输入类似“12”这种不符合base64规则的字符串会引起异常，所以需要增加输入判断
        if key:
            disk_info = self.getmachinecode() 
            disk_info_b=bytes(disk_info, encoding='utf-8')
            disk_info_encryption=self.Encrypted(disk_info_b)
            # print('disk_info_encryption :',disk_info_encryption)
            # print(type(disk_info_encryption)) 
            key_b=bytes(key, encoding='utf-8')
            if disk_info_encryption!=0 and key_b!=0:
                if disk_info_encryption != key_b:
                    print("wrong register code, please check and input your register code again:") 
                    return 1 # 注册码错误，返回1
                    # self.regist()
                elif disk_info_encryption==key_b:
                    print("register succeed.") 
                    #读写文件要加判断
                    self.mkdir("license")
                    if __name__ == '__main__':
                        with open('../license/license.lic','w') as f:
                            f.write(key)
                            f.close()
                    else:
                        with open('./license/license.lic','w') as f:
                            f.write(key)
                            f.close()
                    return 0 # 注册成功，返回0
            else:
                print("读取硬盘信息失败")
                return 2 # 获取机器码出错，返回2
        else:
            # self.regist()
            return 3 # 注册码为空，返回3


    # 打开程序先调用注册文件，比较注册文件中注册码与此时获取的硬件信息编码后是否一致
    def checkAuthored(self):
        disk_info = self.getmachinecode() 
        disk_info_b=bytes(disk_info, encoding='utf-8')
        disk_info_encryption=self.Encrypted(disk_info_b)
        #读写文件要加判断
        try:
            if __name__ == '__main__': 
                f = open('../license/license.lic','r')
            else:
                f = open('./license/license.lic','r')
            if f:
                key=f.read()
                if key:
                    key_b=bytes(key, encoding='utf-8')
                    if key_b == disk_info_encryption:
                        authored_result = 0 # 验证通过返回0
                        print("register succeed.")               
                    else:
                        authored_result = 1 # 注册码错误，返回1
                        print('注册码错误','请重新输入注册码','或发送',disk_info,'至wangcq714@163.com','获取注册码')
                        # self.regist()
                else:
                    authored_result = 2 # 注册文件为空，返回2 
                    print('注册文件为空','请重新输入注册码','或发送',disk_info,'至wangcq714@163.com','获取注册码')
                    # self.regist()                  
            else:
                authored_result = 3 # 打开注册文件，返回3
                print('打开注册文件失败','请重新输入注册码','或发送',disk_info,'至wangcq714@163.com','获取注册码')
                # self.regist()                            
        except:
            authored_result = 4 # 没有注册文件，返回4
            print('请发送',disk_info,'至wangcq714@163.com','获取注册码')
            # self.regist()
        print(authored_result) 
        return authored_result



if __name__ == '__main__':   
    reg=Register()   
    # reg.checkAuthored()
    # reg.regist()
    reg.get_CPU_info()
    reg.get_disk_info()
    reg.get_mainboard_info()
    reg.get_network_info()
    reg.getmachinecode()