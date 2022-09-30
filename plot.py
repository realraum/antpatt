import numpy as np
import matplotlib.pyplot as plt

from matplotlib import transforms
import datetime
import math

def show_plot(antenna_diagram):

	theta = np.array([i[0] for i in antenna_diagram])
	radius = np.array([40+10*math.log(i[1]) for i in antenna_diagram])
	theta = np.deg2rad(theta)
	
	fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
	ax.set_theta_zero_location('N')
	ax.plot(theta, radius)
	ax.set_rticks([ -40,-30, -20,-10, -3,0])  # Less radial ticks
	ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
	ax.grid(True)
	ax.set_title("Antenna Radiation Pattern V0.0", va='bottom')
	plt.autoscale(enable=True,axis='y',tight=None)
	plt.tight_layout()
	plt.show()

def load_plot(f):
	out = []
	try:
		f = open(f, "r")
		lines = f.readlines()
		for line in lines:
			values = list(map(float, line.strip().split()))
			out.append(values)
		f.close()
	except:
		print("error reading file")
		raise
	return out

def save_plot(antenna_diagram):
	try:
		antenna_diagram_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_antenna.diagram")
		f = open("./"+antenna_diagram_file, "w")
		for i in antenna_diagram:
			f.write(f"{i[0]} {i[1]}\n")
		f.close()
	except:
		print("error writing file")
		raise

