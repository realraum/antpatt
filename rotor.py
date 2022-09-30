import serial
import time

class Rotor:

    serial_port = ""
    _rotor_port = None

    MaxRange  = 75 # (+/- value) depends on your SAT-rotor type, check data sheet

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
        self._send_command(f"max{self.MaxRange}")
    #enddef

    def goto_azimuth(self, azi):
        if (abs(azi)<=self.MaxRange):
            cmd = "azi{:6.2f}".format(azi)
            self._send_command(cmd)
            self._current_azi = azi
        else:
            print("ERROR: azimuth out of range")
        #enddef
    #enddef

    def step_azimuth(self, step=1):
        new_azi = self._current_azi+step
        self.goto_azimuth(new_azi)
    #enddef

    def get_azimuth(self):
        return self._current_azi
    #enddef

    def can_move_azimuth(self, dir=1):
        if self._current_azi+dir <= self.MaxRange:
            return True
        else:
            return False
        #endif
    #enddef

    def goto_elevation(self, ele):
        if (abs(ele)<=self.MaxRange):
            cmd = "ele{:6.2f}".format(ele)
            self._send_command(cmd)
            self._current_ele=ele
        else:
            print("ERROR: elevation out of range")
    #enddef

    def step_elevation(self, step=1):
        new_ele = self._current_ele+step
        self.goto_elevation(new_ele)
    #enddef

    def get_elevation(self):
        return self._current_ele
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
        self._rotor_port.close()
    #enddef
