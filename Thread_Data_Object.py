
import sys



class Thread_Data(object):
    def __init__(self):
        self._Sys='IDLE'
        self._Alert='blue_'
        pass
    def get_Sys_State(self):
        return self._Sys
    def get_Alert_State(self):
        return self._Alert
    def set_Sys_State(self,new_sys):
        self._Sys=new_sys
    def set_Alert_State(self,new_Alert):
        self._Alert=new_Alert
    def set_Sec_Count(self,new_Sec_Count):
        self._Sec_Count=new_Sec_Count
    def get_Sec_Count(self):
        return self._Sec_Count
    
    #private
    _Sys='' #system state
    _Alert='' #alert state
    _Sec_Count=0
        

