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

# ask user where the roror is and move it to the extreme if necessary
position_unknown = True
rotor_init_degrees = -(my_rotor.MaxRange_azi-1)
rotor_step = 1
while position_unknown:
    user_input = input("Rotor is closer to which starting point?\n\n +70° = '+' / -70° = '-' / i don't know = '?' \n\n> ")
    if user_input == '+':
        print("positive")
        position_unknown = False
        rotor_init_degrees = (my_rotor.MaxRange_azi-1)
        rotor_step = -1
    elif user_input == '-':
        print("negative")
        position_unknown = False
        rotor_init_degrees = -(my_rotor.MaxRange_azi-1)
        rotor_step = 1
    elif user_input == '?':
        print("don't know")
        position_unknown = False
        rotor_init_degrees = -(my_rotor.MaxRange_azi-1)
        rotor_step = 1
    else:
        print("incorrect input")
    #endif
#endwhile

my_rotor.goto_azimuth(rotor_init_degrees)
print("Rotor turning to start point, press ENTER when done")
input()

# init nanovna measurment system
my_nanovna = nanovna_mag(my_rotor, rotor_step)

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
