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

import argparse

# TODO: CLEAN UP THIS MESS!!!!


def main():

    verbosity_level = 0
    frequency = 0
    rotor_serial_port = "/dev/ttyUSB0"

    parser = argparse.ArgumentParser(description="Antenna Pattern measurement tool using NanoVNA + DiSECq Rotor(s)")
    parser.add_argument('-v','--verbose', type=int, dest='verbose', help="verbostiy level")
    parser.add_argument('-f','--frequency', dest='frequency', help="Test Frequency [Hz]")
    parser.add_argument('-r', '--rotor', dest='rotor_serial_port', help="serial device for rotor (default: /dev/ttyUSB0)")

    args = parser.parse_args()

    if args.verbose:
        if args.verbose <= 5 and args.verbose >=0:
            pass # TODO: implement debug verbosity
        else:
            print("ERROR: stdout verbosity level must be between 0 and 5")
            sys.exit()
        #endif
    #endif
    if args.frequency:
        frequency = int(args.frequency) # TODO: accept prefixes: k / Meg / G maybe check if nanovna can measure at this freq.
    else:
        print("ERROR: Frequency must be given")
        sys.exit()
    #endif
    if args.rotor_serial_port:
        rotor_serial_port = str(args.rotor_serial_port)
    #endif

    print("Hello")

    print(f"verbosity: {verbosity_level}")
    print(f"frequency: {frequency}")
    print(f"rotor_serial_port: {rotor_serial_port}")

    # init rotor
    my_rotor = Rotor(rotor_serial_port)

    # ask user where the rotor is and move it to one of the extremes if necessary
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

    # rotate rotor to one or the other end of it's max. travel
    my_rotor.goto_azimuth(rotor_init_degrees)
    print("Rotor turning to start point, press ENTER when done")
    input() # wait for user to confirm that rotor has reached the starting point

    # init nanovna measurment system
    my_nanovna = nanovna_mag(my_rotor, rotor_step)

    try:
        my_nanovna.start(frequency)
        my_nanovna.wait_for_continue()
        my_nanovna.stop()
    except KeyboardInterrupt:
        my_nanovna.stop()
    #endtry

    save_plot(my_nanovna.antenna_diagram)
    show_plot(my_nanovna.antenna_diagram)

    exit(0)
#enddef

if __name__ == "__main__":
    main()
