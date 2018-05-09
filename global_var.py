import sys


class Golbal_value(object):

    send_flag=0
    ID=[]
    password =[0x31,0x32,0x33,0x34]
    dlist_c=[]
    dlist_s=[]
    dlist_r=[]
    dlist_t=[]
    dlist_cond=[]
    dlist_freq=[]
    dlist_wave=[]
    dlist_wave_c=[]
    dlist_para1_get=[]
    dlist_para1_set=[]
    dlist_para2_get=[]
    dlist_para2_set=[]
    dlist_para3_get=[]
    dlist_para3_set=[]
    dlist_password=[]
    dlist_freq_data=[]
    dlist_wave_data=[]

    resend_flag = 0
    fw_show_flag = 0

    freq_index = 0
    wave_index = 0

    dlist_freq_data_save = [[0 for i in range(1)]for j in range(10)]

    dlist_wave_data_save = [[0 for i in range(1)]for j in range(10)]


    wave_package_number = []
    wave_package_number_cp = []




    def set_value(self,var_number,set_value):
        if (var_number==1):
            Golbal_value.send_flag=set_value
        elif(var_number==2):
            Golbal_value.ID=set_value
        elif(var_number==3):
            Golbal_value.password=set_value
        elif (var_number==4):
            Golbal_value.dlist_c=set_value
        elif (var_number==5):
            Golbal_value.dlist_s=set_value
        elif (var_number==6):
            Golbal_value.dlist_r=set_value
        elif (var_number==7):
            Golbal_value.dlist_t=set_value
        elif(var_number==8):
            Golbal_value.dlist_cond=set_value
        elif(var_number==9):
            Golbal_value.dlist_freq=set_value
        elif(var_number==10):
            Golbal_value.dlist_wave=set_value
        elif(var_number==11):
            Golbal_value.dlist_wave_c=set_value
        elif(var_number==12):
            Golbal_value.dlist_para1_get=set_value
        elif(var_number==13):
            Golbal_value.dlist_para1_set=set_value
        elif(var_number==14):
            Golbal_value.dlist_para2_get=set_value
        elif(var_number==15):
            Golbal_value.dlist_para2_set=set_value
        elif(var_number==16):
            Golbal_value.dlist_para3_get=set_value
        elif(var_number==17):
            Golbal_value.dlist_para3_set=set_value
        elif(var_number==18):
            Golbal_value.dlist_password=set_value
        elif(var_number==19):
            Golbal_value.dlist_freq_data=set_value
        elif(var_number==20):
            Golbal_value.dlist_wave_data=set_value
        elif (var_number == 21):
            Golbal_value.resend_flag = set_value
        elif (var_number == 22):
            Golbal_value.fw_show_flag = set_value
        elif (var_number == 23):
            Golbal_value.freq_index = set_value
        elif (var_number == 24):
            Golbal_value.wave_index = set_value
        elif (var_number == 25):
            Golbal_value.wave_package_number = set_value
        elif (var_number == 26):
            Golbal_value.wave_package_number_cp = set_value




    def get_value(self,var_number):
        if(var_number==1):
            return Golbal_value.send_flag
        elif(var_number==2):
            return Golbal_value.ID
        elif(var_number==3):
            return Golbal_value.password
        elif(var_number==4):
            return Golbal_value.dlist_c
        elif (var_number==5):
            return  Golbal_value.dlist_s
        elif(var_number==6):
            return Golbal_value.dlist_r
        elif(var_number==7):
            return Golbal_value.dlist_t
        elif(var_number==8):
            return Golbal_value.dlist_cond
        elif (var_number == 9):
            return Golbal_value.dlist_freq
        elif (var_number == 10):
            return Golbal_value.dlist_wave
        elif (var_number == 11):
            return Golbal_value.dlist_wave_c
        elif (var_number == 12):
            return Golbal_value.dlist_para1_get
        elif (var_number == 13):
            return Golbal_value.dlist_para1_set
        elif (var_number == 14):
            return Golbal_value.dlist_para2_get
        elif (var_number == 15):
            return Golbal_value.dlist_para2_set
        elif (var_number == 16):
            return Golbal_value.dlist_para3_get
        elif (var_number == 17):
            return Golbal_value.dlist_para3_set
        elif (var_number == 18):
            return Golbal_value.dlist_password
        elif(var_number==19):
            return Golbal_value.dlist_freq
        elif(var_number==20):
            return Golbal_value.dlist_wave_data
        elif (var_number == 21):
            return Golbal_value.resend_flag
        elif (var_number == 22):
            return Golbal_value.fw_show_flag
        elif (var_number == 23):
            return Golbal_value.freq_index
        elif (var_number == 24):
            return Golbal_value.wave_index
        elif (var_number == 25):
            return Golbal_value.wave_package_number
        elif (var_number == 26):
            return Golbal_value.wave_package_number_cp

    def save_freq(self,num,data):
        for nf in range(len(data)):
            Golbal_value.dlist_freq_data_save[num].insert(nf,data[nf])
        print(Golbal_value.dlist_freq_data_save[num])

    def read_freq(self,num):
        return Golbal_value.dlist_freq_data_save[num]

    def dele_freq(self,num):
        del Golbal_value.dlist_freq_data_save[num]

    def save_wave(self, num,index,data):
        for nw in range(len(data)):
             Golbal_value.dlist_wave_data_save[num].insert(index*502+nw,data[nw])
        print(Golbal_value.dlist_wave_data_save[num])

    def read_wave(self, num):
        return Golbal_value.dlist_wave_data_save[num]

    def dele_wave(self,num):
        del Golbal_value.dlist_wave_data_save[num]



