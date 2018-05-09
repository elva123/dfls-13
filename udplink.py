# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets
import stopThreading
import net_ass3
import socket
import threading
import time
import sys
from global_var import Golbal_value
import numpy as np
import pyqtgraph as pg

class Udplink(net_ass3.Ui_UDP_Server):
    def __init__(self):
        super(Udplink,self).__init__()

        self.udp_socket = None
        self.address = None
        self.server_th = None
        self.dlist_gps=[]

    def udp_server_start(self):

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("set ip and port\n")
            port = int(self.ui.lineEdit_port.text())
            print(port)
            address = ('',port)
            self.udp_socket.bind(address)
        except Exception:
            print("check your set.\n")
            QtWidgets.QMessageBox.information(self,'tips','invaild port')
            return
        #except Exception as ret:
            #msg = '请检查端口\n'
            #self.signal_write_msg.emit(msg)
        else:
            self.link = True
            print("linked")
            self.ui.pushButton_link.setText("断开连接")
            self.ui.pushButton_link.setEnabled(True)
            self.server_th = threading.Thread(target=self.udp_server_concurrency)
            self.server_th.start()
            print("UDP server is listening:\n")
            #msg = 'UDP服务端口正在监听：{}\n'.format(port)
            #self.signal_write_msg.emit(msg)

    def udp_server_concurrency(self):
        temp=''
        global Addr

        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(2048)
            addr=recv_addr
            Addr = recv_addr
            print(Addr)

            self.ui.lineEdit_remote_ip.setText(str(recv_addr).strip('( )'))
            print("来自ip%s端口%s的数据"% (recv_addr[0],recv_addr[1]))
            print(recv_msg)
            print(type(recv_msg))
            print(str(recv_msg))
            temp = recv_msg
            dlist_sh=[]

            dlist_sh=list(recv_msg)
            dlist_s=''
            self.ui.textBrowser.append("receive:")

            if self.ui.checkBox_hex.isChecked:
                for ds in range(len(dlist_sh)):
                    dlist_sh[ds]=hex(dlist_sh[ds])

                dlist_s=' '.join(dlist_sh)

                print("checkbox is checked\n")

                self.ui.textBrowser.append(str(dlist_s))
            else:
                self.ui.textBrowser.append(str(list(recv_msg)))

            print(dlist_sh)

            self.udp_rec_process(temp,addr)


    def udp_client_start(self):
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            self.udp_socket = (str(self.lineEdit_ip.text()),int(self.lineEdit_port))
        except Exception as ret:
            msg = '请检查目标IP，端口port\n'
            self.signal_write_msg.emit(msg)
        else:
            msg = 'UDP客户端已启动\n'


    def udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """

        self.udp_socket.close()
        if self.link is True:
            print("已断开网络\n")
            #msg = '已断开网络\n'
            #self.signal_write_msg.emit(msg)
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass

    def udp_rec_process(self,temp,addr):

        gl = Golbal_value()
        flag = gl.get_value(1)
        print(flag)
        dl = ''
        re_flag=0
        ifreply=0
        print(temp)
        dlistr = list(temp)
        dlist=[]

        wavedlist = []
        package_num=[]
        package_num_cp=[]
        package_num_cp_re=[]
        package_index=0

        gl.set_value(2,dlistr[1:7])

        ref = gl.get_value(21)

        print(dlistr)
        dlists = dlistr.copy()
        if (dlistr[7]==0):
            print("receive connect data\n")

            if (ref == 1):
                gl.set_value(21,0)
            else:
                re_flag = 1

        elif (dlistr[7]==0x01):
            if(dlistr[9]==6):
                #receive reply,no need to resend
                print("receive sync reply\n")

            else:
                print("receive sync\n")
                dt=time.localtime()
                print(dt)
                del dlists[9:11]
                dlists.pop()
                #del dlistr[10]
                print(dlists)
                dlists.append(0x06)
                dlists.append(dt.tm_year - 2000)

                dlists.append(dt.tm_mon)
                dlists.append(dt.tm_mday)
                dlists.append(dt.tm_hour)
                dlists.append(dt.tm_min)
                dlists.append(dt.tm_sec)
                dlists.append((~(sum(dlists)-0x68))& 0xff)
                dlists.append(0x16)
                re_flag=1
                print(dlists)
        elif (dlistr[7] == 0x05):
            print("receive heart beat\n")
            re_flag=1

        elif (dlistr[7] == 0x06):
            print("reveive set net para return\n")
            print("password:%s,ip:%d.%d.%d.%d,port:%d"% (dlistr[9:13],dlistr[19],dlistr[20],dlistr[21],dlistr[22],(((dlistr[23]&0xff)<<8)&(dlistr[24]&0xff))))

        elif (dlistr[7] == 0x07):
            print("reveive get net para return\n")
            print("ip:%d.%d.%d.%d,port:%d" % (dlistr[10], dlistr[11], dlistr[12], dlistr[13], (((dlistr[14]&0xff)<<8)|(dlistr[15]&0xff))))
            #deal with dlistr[16]-'f1'
            dl_pn_1=str(dlistr[16]&0x0f)
            print(dl_pn_1)
            dl_pn=[]
            dl_pn.append(dl_pn_1)

            dl_pn_r=[dlistr[17],dlistr[18],dlistr[19],dlistr[20],dlistr[21]]
            print(dl_pn_r)
            for pn in range(len(dl_pn_r)):
                dl_pn_r[pn]=hex(int(dl_pn_r[pn]))[2:]
            print(dl_pn_r)
            dl_pn=dl_pn+dl_pn_r
            print(type(dl_pn))
            print("phone number:%s" % (''.join(dl_pn)))

            sd=[str(dlistr[10]),str(dlistr[11]),str(dlistr[12]),str(dlistr[13])]
            self.ui.lineEdit_ip2.setText('.'.join(sd))
            sdp=str(((dlistr[14]&0xff)<<8)|(dlistr[15]&0xff))
            self.ui.lineEdit_port2.setText(sdp)
            self.ui.lineEdit_phone_number.setText(''.join(dl_pn))

        elif (dlistr[7] == 0x08):
            print("receive reset data return\n")

        elif (dlistr[7] == 0x0a):
            print("receive para1\n")
            if(dlistr[10]==0xff):
                print("receive worng password data return\n")

            print("heart interval:%d,sample interval:%d,sleep times:%d,online times:%d,reset time:%d day %d hour %d minute" % (dlistr[10],dlistr[11]+dlistr[12],dlistr[13]+dlistr[14],dlistr[15]+dlistr[16],dlistr[17]-0x30,dlistr[18]-0x30,dlistr[19]-0x30))
            self.ui.lineEdit_heart.setText(str(dlistr[10]))
            self.ui.lineEdit_sample.setText(str(dlistr[11]+dlistr[12]))
            self.ui.lineEdit_sleep.setText(str(dlistr[13]+dlistr[14]))
            self.ui.lineEdit_online.setText(str(dlistr[15]+dlistr[16]))
            dlist_para1_reset=[]
            dlist_para1_reset.append(int(dlistr[17]-0x30))
            dlist_para1_reset.append(int(dlistr[18]-0x30))
            dlist_para1_reset.append(int(dlistr[19]-0x30))
            dlist_pr=' '.join('%s' %dl for dl in dlist_para1_reset)
            self.ui.lineEdit_reset_time.setText(dlist_pr)


        elif (dlistr[7] == 0x0d):
            print("receive time data from device\n")
            print("%d-%d-%d %d:%d:%d" %(dlistr[10],dlistr[11],dlistr[12],dlistr[13],dlistr[14],dlistr[15]))

        elif (dlistr[7] == 0x60):
            print("receive set fault para data return\n")
            if(dlistr[10]==dlistr[11]==0xff):
                print("return wrong passowrd\n")
            else:
                print("password:%s,freq limit:%d,wave limit:%d" % (dlistr[10:14],dlistr[14]+dlistr[15],dlistr[16]+dlistr[17]))

        elif (dlistr[7] == 0x6a):
            print("receive get fault para return\n")

            print("freq limit:%d,wave limit:%d,limit rate:%d" % (((dlistr[10]&0xff)<<8)|(dlistr[11]&0xff),((dlistr[12]&0xff)<<8)|(dlistr[13]&0x0ff),((dlistr[14]&0xff)<<8)|(dlistr[15]&0xff)))
            self.ui.lineEdit_freq.setText(str(((dlistr[10]&0xff)<<8)|(dlistr[11]&0xff)))
            self.ui.lineEdit_wave.setText(str(((dlistr[12]&0xff)<<8)|(dlistr[13]&0xff)))
            self.ui.lineEdit_limit_rate.setText(str(((dlistr[14]&0xff<<8)|(dlistr[15]&0xff))))


        elif (dlistr[7] == 0x61):
            print("receive condition,will return\n")
            if (ref==1):
                gl.set_value(21,0)
            else:
                #need to reply
                re_flag=1

            print("password verify:%s,pocket index:%d,freq current:%d\n" % (dlistr[10:14],dlistr[14],((dlistr[21]&0xff)<<8)|(dlistr[22]&0xff)))
            print("sample time %d-%d-%d %d:%d:%d\n" % (dlistr[15],dlistr[16],dlistr[17],dlistr[18],dlistr[19],dlistr[20]))
            if(dlistr[23]==0):
                print("power conduction mode.")
            elif(dlistr[23]==1):
                print("get voltage supply from battery.")

            if(dlistr[24]==0):
                print("GPS invaild.")
            elif(dlistr[24]==0xaa):
                print("GPS valid.")

            del dlists[9:]
            #dlists.pop()
            dlists.append(3)
            dlists.append(dlistr[14])
            dlists.append(0xaa)
            dlists.append(0x55)
            dlists.append((~(sum(dlists)-0x68))& 0xff)
            dlists.append(0x16)

        elif (dlistr[7] == 0x62):
            print("receive freq data\n")
            print(len(dlistr))
            freq_index = gl.get_value(23)

            del dlists[8:-1]

            dlists.pop()
            print(dlists)
            dlists.append(0)
            dlists.append(3)
            #package index
            dlists.append(dlistr[14])

            dlists.append(0xaa)
            dlists.append(0x55)

            dlists.append((~(sum(dlists)-0x68)&0xff))
            dlists.append(0x16)
            print("send freq return data:")
            print(dlists)

            if freq_index is 0:
                re_flag=1

            # show wave flag
            gl.set_value(22, 1)
            gl.save_freq(freq_index,dlistr[31:1031])

        elif (dlistr[7] == 0x64):
            print("receive wave request data from device\n")

            print("GPS timestamp:%d weeks since 1980,and %d ms,%d ns\n" % (dlistr[10]+dlistr[11],dlistr[12]+dlistr[13]+dlistr[14]+dlistr[15],dlistr[16]+dlistr[17]+dlistr[18]+dlistr[19]))
            if((dlistr[20]&0xf0)==0x10):
                print("BeiDou Navigation Satellite System.")
            elif((dlistr[20]&0xf0)==0x20):
                print("GPS system.")

            if((dlistr[20]&0x0f)==0x0):
                print("GPS invaild.")
            else:
                print("GPS vaild.")

            print("sample rate:%d,wave data points number before fault:%d,wave data length:%d,total pockets:%d" % (dlistr[21],dlistr[22]+dlistr[23],dlistr[24]+dlistr[25],dlistr[26]+dlistr[27]))
            package_index=(dlistr[26]+dlistr[27])
            for index in range(dlistr[26]+dlistr[27]):
                package_num.append(index+1)
            print(package_num)
            gl.set_value(25,package_num)

            if (ref == 1):
                gl.set_value(21,0)
            else:
                re_flag = 1

        elif (dlistr[7] == 0x65):
            print("wave data saved\n")
            package_index = dlistr[22]
            print(len(dlistr))
            print("GPS timestamp:%d weeks since 1980,and %d ms,%d ns\n" % (
                ((dlistr[10]&0xff)<<8)|(dlistr[11]&0xff), (dlistr[12]&0xff)<<24 |((dlistr[13]&0xff)<<16)|((dlistr[14]&0xff)<<8)|(dlistr[15]&0xff),
                ((dlistr[16]&0xff)<<24)| ((dlistr[17]&0xff)<<16) | ((dlistr[18]&0xff)<<8)|(dlistr[19]&0xff)))

            self.dlist_gps=[dlistr[10],dlistr[11],dlistr[12],dlistr[13],dlistr[14],dlistr[15],dlistr[16],dlistr[17],dlistr[18],dlistr[19]]


            if ((dlistr[20] & 0xf0) == 0x10):
                print("BeiDou Navigation Satellite System.")
            elif ((dlistr[20] & 0xf0) == 0x20):
                print("GPS system.")

            if ((dlistr[20] & 0x0f) == 0x0):
                print("GPS invaild.")
            else:
                print("GPS vaild.")

            pack_num = gl.get_value(25)
            print(pack_num)
            package_num_cp = gl.get_value(26)
            if package_index in pack_num:
                package_num_cp.insert(package_index,package_index)
                gl.set_value(26, package_num_cp)
                print("updata package number\n")
                print(package_num_cp)


                wavedlist+=(dlistr[23:523])

                wn = gl.get_value(24)
                print(package_index)
                gl.save_wave(wn,package_index,wavedlist)


        elif (dlistr[7] == 0x66):
            print("receive wave data end from device\n")

            del dlists[7:]
            dlists.append(0x67)
            dlists.append(0)
            re_flag = 1

            if(len(package_num)==len(package_num_cp)):
                print("receive all of wave data\n")
                dlists.append(12)
                #dlists.append(dlistr[10:21])
                print(self.dlist_gps)
                if(len(self.dlist_gps)==0):
                    dlists+=[0]*10
                else:
                    dlists=dlists+self.dlist_gps

                dlists.append(0)
                dlists.append(0)
                dlists.append(~(sum(dlists)-0x68)&0xff)
                dlists.append(0x16)

                #show wave flag
                gl.set_value(22,2)
                gl.set_value(26,[])

                wave_n = gl.get_value(24)
                wave_data = gl.read_wave(wave_n)
                #save as .txt
                np.savetxt('wave_%d.txt' % wave_n,wave_data)
                for n in range(1,9):
                    gl.save_wave(wave_n,n,[])



            else:
                nums=0
                #find which package num not receive
                for pnum in package_num_cp:
                    for pnum_p in package_num:
                        if (package_num_cp[pnum]==package_num[pnum_p]):
                            pass
                        else:
                            nums+=nums
                            package_num_cp_re.append(package_num[pnum])

                print("receive parts of wave data,need more\n")
                dlists.append(nums)
                for j in range(len(package_num_cp_re)):
                    if(package_num_cp_re[j]<256):
                        dlists.append(0)
                        dlists.append(package_num_cp_re[j])
                    else:
                        dlists.append((package_num_cp_re[j]&0xff00)>>8)
                        dlists.append(package_num_cp_re[j]&0xff)

                dlists.append(~(sum(dlists) - 0x68) & 0xff)
                dlists.append(0x16)

        print(re_flag)
        print((dlists))

        if(re_flag==1):
            re_flag=0
            self.udp_socket.sendto(bytes(dlists),addr)

            self.ui.textBrowser.append("send:")
            print("send return data\n")

            if self.ui.checkBox_hex.isChecked:
                dlists_h=[]
                for nd in range(len(dlists)):
                    dlists_h.append(hex(dlists[nd]))
                print(dlists_h)
                dlist_ss = ' '.join(dlists_h)
                self.ui.textBrowser.append(str(dlist_ss))
            else:
                self.ui.textBrowser.append(dlists)
        #主站主动下发，收到回复后不再回传
        if (flag == 0):
            print("no data need to send\n")
        elif (flag==1):
            #connect data--0
            dlist = gl.get_value(4)
            gl.set_value(4,dl)

            gl.set_value(21,1)
        elif (flag==2):
            #Synchronizer data--1
            dlist = gl.get_value(5)
            gl.set_value(5,dl)

            gl.set_value(21, 1)
        elif (flag == 3):
            #set password data--2
            dlist = gl.get_value(18)
            gl.set_value(18,dl)
        elif (flag == 4):
            #set para1 data--3
            dlist = gl.get_value(13)
            gl.set_value(13, dl)

        elif (flag == 7):
            #set net para data--6
            dlist = gl.get_value(15)
            gl.set_value(15, dl)

        elif (flag == 8):
            #get net para data--7
            dlist = gl.get_value(14)
            gl.set_value(14, dl)

        elif (flag == 9):
            #reset device data--8
            dlist = gl.get_value(6)
            gl.set_value(6, dl)
        elif (flag == 0x0b):
            #get para1 data--0x0a
            dlist = gl.get_value(12)
            gl.set_value(12,dl)

        elif (flag == 0x0e):
            #get device time data--0x0d
            dlist = gl.get_value(7)
            gl.set_value(7, dl)
        elif (flag == 0x61):
            #set fault para data--0x60
            dlist = gl.get_value(17)
            gl.set_value(17, dl)

        elif (flag == 0x6b):
            #get fault para data--0x6a
            dlist = gl.get_value(16)
            gl.set_value(16, dl)

        elif(flag == 0x62):
            #get condition data--0x61
            dlist = gl.get_value(8)
            gl.set_value(8,dl)

            gl.set_value(21, 1)
        elif (flag == 0x63):
            # get freq data--0x62
            dlist = gl.get_value(9)
            gl.set_value(9, dl)

            gl.set_value(21, 1)
        elif(flag == 0x65):
            #get wave requeset data--0x64
            dlist = gl.get_value(10)
            gl.set_value(10, dl)

            gl.set_value(21, 1)

        elif (flag == 0x68):
            #send wave complete data--0x67
            dlist = gl.get_value(11)
            gl.set_value(11, dl)

        if (flag != 0):

            print(dlist)
            print("need to send sth\n")
            self.udp_socket.sendto(bytes(dlist), addr)
            gl.set_value(1, 0)
            print("data send over\n")
        else:
            pass

        pw = gl.get_value(22)
        print(pw)
        if (pw ==1):
            #freq
            gl.set_value(22,0)
            self.wave_print('freq')
        elif (pw == 2):
            #wave
            gl.set_value(22,0)
            self.wave_print('wave')
        else:
            print("nothing happened\n")




    def udp_send(self):

        print("waiting for heart beat.\n")
        QtWidgets.QMessageBox.information(self,"tips","waiting for the heart beat")

    def wave_print(self,type_wave):
        glb = Golbal_value()
        numb = glb.get_value(23)
        print("if print wave\n")
        #reply = QtWidgets.QMessageBox.question(self,"tips","print this wave?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No ,QtWidgets.QMessageBox.Yes)
        reply = QtWidgets.QMessageBox.Yes
        if (reply == QtWidgets.QMessageBox.Yes):
            if (type_wave=='freq'):
                print("will print freq")
                data = glb.read_freq(numb)
                print(len(data))

                data1 = []
                for nb in range(0, len(data)-3, 2):
                    data1.append((((data[nb] & 0xff) << 8 )| (data[nb+1] & 0xff))/1000)

                print(data1)

                self.ui.graphicsView.clear()
                #self.ui.graphicsView.addPlot(title="freq data", y=np.random.normal(size=100), pen=pg.mkPen(color='b', width=2))
                self.ui.graphicsView.addPlot(title="freq data", y=data1,pen=pg.mkPen(color='b', width=2))

                glb.dele_freq(numb)
                #data1 = [50,100,2000,1000,50,0,50]
                #print(list(data))
                #pg.plot(data1,title="freq show")

            elif (type_wave == 'wave'):
                print("will print wave")
                numbw = glb.get_value(24)
                data =  glb.read_wave(numbw)
                print(len(data))

                data1 =[]
                data2 = [0]
                for nb in range(1, len(data)-2, 2):
                    data1.append((((data[nb] & 0xff) << 8 )| (data[nb+1] & 0xff))/1000)

                print(data1)
                #ps = pic_show.initui()
                #ps.show()
                #data2 = [50, 100, 2000, 1000, 50, 0, 50]
                #print(list(data))
                #pg.plot(data2,title="wave show")
                self.ui.graphicsView_2.clear()
                print("clear screen\r\n")
                self.ui.graphicsView_2.addPlot(title="wave data", y=data, pen=pg.mkPen(color='r', width=1))

                glb.dele_wave(numbw)
        else:
            print("no wave be print")






