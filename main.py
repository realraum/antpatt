from rotor import Rotor
from nanovna_mag import nanovna_mag

import time

import os
import shutil
from os import listdir
from os.path import isfile, join
from plot import save_plot, show_plot

import csv
import math

import threading
import sys

# TODO: CLEAN UP THIS MESS!!!!

# init rotor
my_rotor = Rotor("/dev/ttyUSB0")

my_rotor.goto_azimuth(-(my_rotor.MaxRange-1))
print("Rotor turning to start point, press ENTER when done")
input()

# init nanovna measurment system
my_nanovna = nanovna_mag(my_rotor)

try:
    my_nanovna.start(int(sys.argv[1]))
    my_nanovna.wait_for_continue()
    my_nanovna.stop()
except KeyboardInterrupt:
    my_nanovna.stop()
    #exit(0)

save_plot(my_nanovna.antenna_diagram)
show_plot(my_nanovna.antenna_diagram)

exit(0)
