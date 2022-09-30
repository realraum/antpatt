from rotor import Rotor
import time

import os
import shutil
from os import listdir
from os.path import isfile, join

import csv
import math

import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import threading


class nanovna_mag(FileSystemEventHandler):

    basepath = "/tmp"
    temp_folder = basepath+"/antenna_diagram"
    ts_folder = temp_folder+"/ts_temp"
    ts_file = ""

    _proc = 0
    _rotor = None
    _continue_event = None
    antenna_diagram = []

    def __init__(self, rotor):
        # get rotor from main
        self._rotor = rotor

        #init fs
        try:
            shutil.rmtree(self.temp_folder)
        except FileNotFoundError:
            print("removing folder failed, does not exist")
        #endtry

        os.mkdir(self.temp_folder)
        os.mkdir(self.ts_folder)

        # init event handler (watchdog)
        self._event_handler = self
        self._observer = Observer()
        self._observer.schedule(self._event_handler, path=self.ts_folder, recursive=False)
        self._observer.start()
    #enddef

    def __del__(self):
        self._observer.stop()

    def start(self, freq):
        self._proc = subprocess.Popen(["python3", "./nanovna-saver/nanovna-saver.py", "-o", self.ts_folder, "-f", str(freq * 1000000), "-t", str((freq * 1000000) + 1000), "-i"], 
                                      stdout=subprocess.DEVNULL)
        self._continue_event = threading.Event()
    
    def stop(self):
        self._proc.terminate()
    #enddef


    def on_created(self, event):
        #print("on_created", event.src_path)
        self._rotor.step_azimuth()

        mag_array = []

        file_ok = False
        while not file_ok:
            # read touchstone file and calculate magnitude of S21 for all sweep points
            with open(event.src_path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ')
                for row in reader:
                    #print(f"row = '{row}'")
                    if row[0] != '#':
                        mag = math.sqrt(math.pow(float(row[4]), 2) + math.pow(float(row[5]), 2))
                        mag_array.append(mag)
                #endfor
            #endwith
            # retry until file has correct length (101 lines)
            if len(mag_array) == 101:
                file_ok=True
            else:
                mag_array=[]
            #endif
        #endfor

        # calculate average magnitude -> we want one value for one step
        avg = 0
        for i in mag_array:
            avg = avg + i
        avg = avg / len(mag_array)

        az = self._rotor.get_azimuth()
        print(f"{az} {avg}")
        self.antenna_diagram.append([az, avg])

        if not self._rotor.can_move_azimuth():
            print("Rotor at end, stopping")
            self._continue_event.set()
    #enddef

    def wait_for_continue(self):
        self._continue_event.wait()
    #enddef

    def _meas(self):
        # run nano-vna saver to obtain measurements in a file which is then rea dback to calculate the average magnitude
        # ugly hack to call nanovna-saver with args, could be done with subprocess instead
        # WONTFIX: proper way would be to use nanovna-saver modules here and skip the os / file step
        #          but as this is just a quick hack and /tmp is mounted in RAM this is not a prob.
        #os.system(f"python3 ./nanovna-saver/nanovna-saver.py -o {self.ts_folder} -f 145000000 -t 145001000 > /dev/null")
        subprocess.run(["python3", "./nanovna-saver/nanovna-saver.py", "-o", self.ts_folder, "-f", "145000000", "-t", "145001000"])
        onlyfiles = [f for f in listdir(self.ts_folder) if isfile(join(self.ts_folder, f))]
        if len(onlyfiles) != 1:
            print("ERROR: Too many files")
            exit(0)
        #endif
        ts_file=self.ts_folder+"/"+onlyfiles[0]
        print(f"{ts_file}")

        mag_array = []

        # read touchstone file and calculate magnitude of S21 for all sweep points
        with open(ts_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                if row[0] != '#':
                    mag = math.sqrt(math.pow(float(row[4]), 2) + math.pow(float(row[5]), 2))
                    mag_array.append(mag)
            #endfor
        #endwith

        # delete touchstone file
        os.remove(ts_file)

        # calculate average magnitude -> we want one value for one step
        avg = 0
        for i in mag_array:
            avg = avg + i
        avg = avg / len(mag_array)

        print(f"avg = {avg}")
        return avg
    #enddef
#endclass
