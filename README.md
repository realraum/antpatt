# antpatt
Antenna Pattern Measurement System
Antenna Diagram with NanoVNA and DiSEqC-Rotor
Very quick+dirty hack that combine two existing Projects to create an antenna radiation diagram

Easy DiSEqC: https://www.e-callisto.org/hardware/callisto-hardware.html

NanoVNA-Saver (commandline version): https://github.com/spel-oe/nanovna-saver




TODOs:


 Explain purpose better in readme

 Commit changes made to nanovna-saver (Tempfile + capture rate slow down)

 Tidy up main.py + make OOP better



Dependencies:
pip3 install watchdog numpy matplotlib

Setup
Unzip modified nanovna-saver (not committed anywhere yet)
unzip nanovna-saver.zip
Connect DiSEqC adaptor and NanoVNA.
Assuming the DisEqC adaptor is /dev/ttyUSB0

Run
run: python3 main.py
Instructions will apear on screen

Rotor returns to start position, press enter when rotor has returned
NanoVNA will start continuous measruements and rotor will step 1 degree per measureemnt
After completing a 120 Degrees arc the resulting antenna diagram will be displayed on screen
