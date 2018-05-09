# -*- coding:utf-8 -*-
from PyQt5 import QtCore,QtGui,QtWidgets
from udplink import Udplink
import socket
import sys
import time
from global_var import Golbal_value


class MainWindow(QtWidgets.QWidget,Udplink):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Udplink()
        self.ui.setupUi(self)

        self.client_socket_list = list()
        self.click_get_ip()
#        self.another = None
        self.link = False
        self.ui.pushButton_link.clicked.connect(self.click_link)

        self.ui.pushButton_connect.clicked.connect(self.click_connect)
        self.ui.pushButton_syn.clicked.connect(self.click_syn)
        self.ui.pushButton_reset.clicked.connect(self.click_reset)
        self.ui.pushButton_get_time.clicked.connect(self.click_time)
        self.ui.pushButton_condition.clicked.connect(self.click_condition)
        self.ui.pushButton_freq.clicked.connect(self.click_freq)
        self.ui.pushButton_wave.clicked.connect(self.click_wave)
        self.ui.pushButton_set_password.clicked.connect(self.click_set_password)
        self.ui.pushButton_para1_get.clicked.connect(self.click_para1_get)
        self.ui.pushButton_para1_set.clicked.connect(self.click_para1_set)
        self.ui.pushButton_para2_get.clicked.connect(self.click_para2_get)
        self.ui.pushButton_para2_set.clicked.connect(self.click_para2_set)
        self.ui.pushButton_para3_get.clicked.connect(self.click_para3_get)
        self.ui.pushButton_para3_set.clicked.connect(self.click_para3_set)

        #self.pushBotton_link.clicked.connect(self.click_link)
        self.ui.pushButton_clear.clicked.connect(self.click_clear)

        #全局变量类的实例化
        self.g=Golbal_value()


    def click_link(self):
        if self.link is True:
            print("already link,unlink now.")
            self.click_unlink()
            self.ui.pushButton_link.setText("连接")
            print("unlink.\n")
        else:
            print("will link\n")
            if self.ui.comboBox.currentIndex()==0:
                self.udp_server_start()
            if self.ui.comboBox.currentIndex()==1:
                self.udp_client_start()

    def click_unlink(self):

        self.udp_close()
        self.link = False
        #self.ui.pushButton_link.setEnabled(False)

    def click_clear(self):

        self.ui.textBrowser.clear()

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        # 获取本机ip
        self.ui.lineEdit_ip.clear()
        my_addr = socket.gethostbyname(socket.gethostname())
        self.ui.lineEdit_ip.setText(str(my_addr))

    def click_connect(self):

        print("waiting for heart beat to send connect data\n")
        #dli=[0x68,0x48,0x4e,0x32,0x30,0x31,0x37,0x00,0x00,0x02,0x01,0x03,0x99,0x16]
        dli=[0x68]
        dli_id=self.g.get_value(2)
        #dli.append(dli_id[])
        dli=dli+dli_id
        dli.append(0)
        dli.append(0)
        dli.append(2)
        dli.append(0x01)
        dli.append(0x03)
        print(dli)
        dli.append(~(sum(dli)-0x68)&0xff)
        dli.append(0x16)

        self.g.set_value(1, 1)
        self.g.set_value(4,dli)
        self.udp_send()


    def click_syn(self):

        print("waiting for heart beat to send syn data\n")

        #dli = [0x68,0x48,0x4e,0x32,0x30,0x31,0x37,0x01,0x00,0x06]
        dli =[0x68]
        dli_id = self.g.get_value(2)

        dli=dli+dli_id
        dli.append(1)
        dli.append(0)
        dli.append(6)

        dt = time.localtime()
        dli.append(dt.tm_year-2000)
        dli.append(dt.tm_mon)
        dli.append(dt.tm_mday)
        dli.append(dt.tm_hour)
        dli.append(dt.tm_min)
        dli.append(dt.tm_sec)
        dli.append(~(sum(dli)-0x68)&0xff)
        dli.append(16)

        self.g.set_value(1, 2)
        self.g.set_value(5, dli)
        self.udp_send()

    def click_reset(self):

        print("waiting for heart beat to send reset data\n")

        #dli = [0x68,0x48,0x4E,0x32,0x30,0x31,0x37,0x08,0x00,0x04,0x31,0x32,0x33,0x34,0xC9,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli=dli+dli_id
        print(dli)
        dli.append(0x08)
        dli.append(0)
        dli.append(0x04)
        pw = self.g.get_value(3)
        dli=dli+pw
        dli.append(~(sum(dli)-0x68)&0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x09)
        self.g.set_value(6, dli)
        self.udp_send()

    def click_time(self):
        print("waiting for heart beat to send request time data\n")

        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x0D,0x00,0x00,0x8F,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli=dli+dli_id
        dli.append(0x0d)
        dli.append(0)
        dli.append(0)

        dli.append(~(sum(dli) - 0x68)&0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x0e)
        self.g.set_value(7, dli)
        self.udp_send()

    def click_condition(self):
        print("waiting for heart beat to send condition data\n")

        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x61)
        dli.append(0)
        dli.append(0)

        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x62)
        self.g.set_value(8, dli)
        self.udp_send()

    def click_freq(self):
        gl = Golbal_value()
        print("waiting for heart beat to send freq data\n")

        value, ok = QtWidgets.QInputDialog.getInt(self, 'input tips', 'please enter freq number you want:\n\n 0 means last 10 waves', 1, 0, 10,1)
        print(type(value))
        if (value>10):
            QtWidgets.QMessageBox.information(self, "tips", "input number must less than 10")
        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x62)
        dli.append(0)
        dli.append(1)

        dli.append(int(value))
        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        gl.set_value(23,value)

        self.g.set_value(1, 0x63)
        self.g.set_value(9, dli)
        self.udp_send()

    def click_wave(self):
        gl = Golbal_value()
        print("waiting for heart beat to send wave data\n")

        value,ok = QtWidgets.QInputDialog.getInt(self,'input tips','please enter wave numbers you want:\n\n 0 means last 10 waves',1,0,10,1)
        print(type(value))
        if (value>10):
            QtWidgets.QMessageBox.information(self, "tips", "input number must less than 10")
        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x64)
        dli.append(0)
        dli.append(1)

        dli.append(int(value))
        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        gl.set_value(24,value)

        print("wave request data %s" % dli)
        self.g.set_value(1, 0x65)
        self.g.set_value(10, dli)
        self.udp_send()

    def click_set_password(self):
        dli=[0x68]
        dli_id = self.g.get_value(2)
        dli = dli + dli_id
        dli.append(2)
        dli.append(0)
        dli.append(0x08)

        psold=self.ui.lineEdit_password_old.text()
        psnew=self.ui.lineEdit_password_new.text()
        if (psold !=""):
            if(psnew !=""):
                psold_l=[]
                for cont in range(len(psold)):
                    psold_l.append(int(psold[cont])+0x30)

                print(psold_l)
                #dli=dli+psold_l
                for cont in range(len(psnew)):
                    psold_l.append(int(psnew[cont])+0x30)

                dli=dli+psold_l
                print(dli)

                dli.append(~(sum(dli)-0x68)&0xff)
                self.g.set_value(1, 3)
                self.g.set_value(18, dli)
                self.udp_send()

            else:
                pass

        else:
            print("invaild password")


    def click_para1_get(self):
        print("waiting for heart beat to send get para1 data\n")

        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x0a)
        dli.append(0)
        dli.append(0)

        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x0b)
        self.g.set_value(12, dli)
        self.udp_send()


    def click_para1_set(self):
        dli = [0x68]
        dli_id = self.g.get_value(2)
        dli = dli + dli_id
        dli.append(0x03)
        dli.append(0)
        dli.append(0x12)
        dli_pw = self.g.get_value(3)
        dli = dli+dli_pw

        dli_h=self.ui.lineEdit_heart.text()
        dli.append(int(dli_h))
        print(dli)

        dli_s = self.ui.lineEdit_sample.text()
        if(dli_s!=""):
            if(int(dli_s)>255):
                dli.append(int(dli_s)&0xff00>>8)
                dli.append(int(dli_s)&0xff)
            else:
                dli.append(0)
                dli.append(int(dli_s)&0xff)

        else:
            print("empty para\n")
            return
        print(dli)
        dli_sl = self.ui.lineEdit_sleep.text()
        if(dli_sl!=""):
            if (int(dli_sl)>255):
                dli.append(int(dli_sl) & 0xff00 >> 8)
                dli.append(int(dli_sl) & 0xff)
            else:
                dli.append(0)
                dli.append(int(dli_sl) & 0xff)
        else:
            print("empty para\n")
            return
        print(dli)
        dli_ol = self.ui.lineEdit_online.text()
        if(dli_ol!=""):

            if (int(dli_ol) > 255):
                dli.append(int(dli_ol) & 0xff00 >> 8)
                dli.append(int(dli_ol) & 0xff)
            else:
                dli.append(0)
                dli.append(int(dli_ol) & 0xff)
        else:
            print("empty para\n")
            return
        print(dli)
        dli_r = self.ui.lineEdit_reset_time.text()
        if(dli_r!=""):
            dli_r=dli_r.split( )

            print(dli_r)
            dli_rl=[]
            for cont in range(len(dli_r)):
                dli_rl.append(int(dli_r[cont])+0x30)
            print(dli_rl)
            dli=dli+dli_rl

        else:
            print("empty para\n")
            return
        print(dli)

        dli=dli+[1,2,3,4]
        print(dli)
        dli.append(~(sum(dli)-0x68)&0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x04)
        self.g.set_value(13, dli)
        self.udp_send()



    def click_para2_get(self):
        print("waiting for heart beat to send get para2 data\n")

        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x07)
        dli.append(0)
        dli.append(0)

        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x08)
        self.g.set_value(14, dli)
        self.udp_send()

    def click_para2_set(self):
        dli = [0x68]
        dli_id = self.g.get_value(2)
        dli = dli + dli_id
        dli.append(0x06)
        dli.append(0)
        dli.append(0x1c)
        dli_pw = self.g.get_value(3)
        dli = dli + dli_pw

        dli_ip_re=[]
        dli_pt=[]

        dli_ip = self.ui.lineEdit_ip2.text()
        if(dli_ip==""):
            print("net para2 empty\n")
            return

        dli_ip_re=dli_ip.split('.')
        print(dli_ip_re)


        for cont in range(len(dli_ip_re)):
            dli_ip_re[cont]=(int(dli_ip_re[cont]))
        dli=dli+dli_ip_re

        print(dli)

        dli_port = self.ui.lineEdit_port2.text()
        if (dli_port != ""):
            print(dli_port)
            if (int(dli_port) > 255):
                print(int(dli_port))
                dli_pt=[((int(dli_port) & 0xff00) >> 8)]
                print(dli_pt)
                dli_pt.append(int(dli_port) & 0xff)
                print(dli_pt)

            else:
                dli_pt.append(0)
                dli_pt.append(int(dli_port) & 0xff)

            dli=dli+dli_pt

        else:
            print("empty para\n")
            return

        dli = dli + dli_ip_re
        dli=dli+dli_pt

        print(dli)

        dli_ph = self.ui.lineEdit_phone_number.text()
        if (dli_ph != ""):
            dli_ph=list(dli_ph)
            if (len(dli_ph)!=11):
                print("invailed phone number\n")
                return

            print(dli_ph)
            dli_ph_r=[]
            for pn in range(len(list(dli_ph))):
                dli_ph[pn]=(int(dli_ph[pn]))

            print(dli_ph)
            dli_ph_re=[dli_ph[0]|0xf0]
            dli_ph_re.append(((dli_ph[1] & 0xf )<<4 ) |(dli_ph[2]))
            dli_ph_re.append(((dli_ph[3] & 0xf )<< 4) | (dli_ph[4]))
            dli_ph_re.append(((dli_ph[5] & 0xf )<< 4) | (dli_ph[6]))
            dli_ph_re.append(((dli_ph[7] & 0xf )<< 4) | (dli_ph[8]))
            dli_ph_re.append(((dli_ph[9] & 0xf )<< 4) | (dli_ph[10]))

            print(dli_ph_re)
            dli = dli + dli_ph_re
            dli = dli + dli_ph_re

        else:
            print("empty para\n")
            return
        print(dli)

        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        self.g.set_value(1, 7)
        self.g.set_value(15, dli)
        self.udp_send()

    def click_para3_get(self):
        print("waiting for heart beat to send get para1 data\n")

        # dli = [0x68,0x48,0x4E,0x30,0x34,0x30,0x39,0x61,0x00,0x00,0x3B,0x16]
        dli = [0x68]
        dli_id = self.g.get_value(2)

        dli = dli + dli_id
        dli.append(0x6a)
        dli.append(0)
        dli.append(0)

        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x16)

        self.g.set_value(1, 0x6b)
        self.g.set_value(16, dli)
        self.udp_send()

    def click_para3_set(self):
        dli = [0x68]
        dli_id = self.g.get_value(2)
        dli = dli + dli_id
        dli.append(0x60)
        dli.append(0)
        dli.append(0x10)
        dli_pw = self.g.get_value(3)
        dli = dli + dli_pw


        dli_f = self.ui.lineEdit_freq.text()
        if (dli_f != ""):
            if (int(dli_f) > 255):
                dli.append(int(dli_f) & 0xff00 >> 8)
                dli.append(int(dli_f) & 0xff)
            else:
                dli.append(0)
                dli.append(int(dli_f) & 0xff)

        else:
            print("empty para\n")
            return

        print(dli)
        dli_w = self.ui.lineEdit_wave.text()
        if (dli_w != ""):
            if (int(dli_w) > 255):
                dli.append(int(dli_w) & 0xff00 >> 8)
                dli.append(int(dli_w) & 0xff)
            else:
                dli.append(0)
                dli.append(int(dli_w) & 0xff)
        else:
            print("empty para\n")
            return

        dli = dli + [0, 0, 0, 0, 0, 0, 0, 0]
        print(dli)
        dli.append(~(sum(dli) - 0x68) & 0xff)
        dli.append(0x10)

        self.g.set_value(1, 0x61)
        self.g.set_value(17, dli)
        self.udp_send()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())