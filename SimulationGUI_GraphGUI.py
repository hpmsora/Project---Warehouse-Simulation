###############################
#
# Simulation Canvas - Graph GUI
#
# Won Yong Ha
#
# V.1.0 - General Graph GUI
#
###############################

import matplotlib.animation as ani

class SimulationGUI_GraphGUI():

	
	# Internal Varialbe
	tools = None
	canvas = None

	graph_GUI_height = 500     # Pixel size

	# Constructor
	def __init__(self, _tools):
		self.tools = _tools

		self.canvas = self.tools.GetCanvas()

		new_canvas_height = int(self.canvas.cget("height")) + self.graph_GUI_height
		self.canvas.config(height = new_canvas_height)
