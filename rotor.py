import serial
import time

class RotorDegreeOutOfRange(Exception):
    pass

class Rotor:

    serial_port = ""
    _rotor_port = None

    MaxRange_azi  = 75 # (+/- value) depends on your SAT-rotor type, check data sheet
    MaxRange_ele = 75 

    _current_azi = 0
    _current_ele = 0

    def __init__(self, serial_port):
        print(f"Opening Serial Port {serial_port}")

        try:
            self._rotor_port = serial.Serial(
                port     = serial_port,
                baudrate = 9600,
                bytesize = serial.EIGHTBITS,
                parity   = serial.PARITY_NONE,
                timeout  = 2)
        except IOError:
            print ("Problem communication with tracker. Check COM-port and cables/connectors!")
            exit(0)
        #endtry
        time.sleep(2) # wait for arduino to be initialized
        self._send_command("-h")
        self._send_command(f"max{self.MaxRange_azi}") # TODO: what if max range ele is smaller / bigger than azi ?
    #enddef

    def goto_azimuth(self, azi):
        if self._can_move_azimuth(azi):
            cmd = "azi{:6.2f}".format(azi)
            self._send_command(cmd)
            self._current_azi = azi
        else:
            print("WARN: azimuth out of range")
            raise RotorDegreeOutOfRange
        #enddef
    #enddef

    def step_azimuth(self, step=1):
        new_azi = self._current_azi+step
        self.goto_azimuth(new_azi)
    #enddef

    def get_azimuth(self):
        return self._current_azi
    #enddef

    def _can_move_azimuth(self, new_azi):
        if abs(new_azi) < self.MaxRange_azi:
            return True
        else:
            return False
        #endif
    #enddef

    def goto_elevation(self, ele):
        if self._can_move_elevation(ele):
            cmd = "ele{:6.2f}".format(ele)
            self._send_command(cmd)
            self._current_ele=ele
        else:
            print("WARN: elevation out of range")
            raise RotorDegreeOutOfRange
    #enddef

    def step_elevation(self, step=1):
        new_ele = self._current_ele+step
        self.goto_elevation(new_ele)
    #enddef

    def get_elevation(self):
        return self._current_ele
    #enddef

    def _can_move_elevation(self, new_ele):
        if abs(new_azi) < self.MaxRange_ele:
            return True
        else:
            return False
        #endif
    #enddef

    def _send_command(self, cmd):
        cmd = f"{cmd}\n"
        #print(f"{cmd}")
        try:
            self._rotor_port.write(cmd.encode())
            self._rotor_port.flush()
        except IOError:
            print ("Problem communication with tracker. Check COM-port and cables/connectors!")
        #endtry
    #enddef


    def __del__(self):
        if self._rotor_port:
            self._rotor_port.close()
    #enddef
