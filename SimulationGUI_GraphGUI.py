###############################
#
# Simulation Canvas - Graph GUI
#
# Won Yong Ha
#
# V.1.1 - Stabilizing
# V.1.0 - General Rigid Graph GUI
#
###############################

import tkinter as tk

import matplotlib as mp
import matplotlib.figure as np_fig
import matplotlib.animation as mp_ani
import matplotlib.backends.backend_tkagg as mp_tkagg

class SimulationGUI_GraphGUI():

	# Custom Variables
	graph_GUI_height = 300     # Pixel size
	graph_GUI_each_width = 2 # Inch size
	
	# Internal Varialbes
	tools = None

	canvas = None
	parent = None

	graph_data = None

	graph_frame = None
	graph_plots = None
	graph_animations = None

	# Constructor
	def __init__(self, _tools, padx = 0, pady = 0):
                self.tools = _tools

                self.parent = self.tools.GetParent()
                self.canvas = self.tools.GetCanvas()

                self.graph_data = self.tools.GetGraphData()
                self.graph_plots = {}
                self.graph_animations = []
                
                self.graph_frame = tk.Frame(self.parent)
                self.graph_frame.place(x = padx,
                                       y = int(self.canvas.cget("height")) + pady,
                                       height = self.graph_GUI_height,
                                       width = self.canvas.cget("width"))
                
                new_canvas_height = int(self.canvas.cget("height")) + self.graph_GUI_height
                self.canvas.config(height = new_canvas_height)
                self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
                
	# Graph animation function
	def GraphAnimation(self, _frame, _value_type):
		x_list, y_list = self.graph_data[_value_type]
		self.graph_plots[_value_type].plot(x_list, y_list)
                
	# Build a new graph
	def BuildGraph(self):
		eval_total, eval_varialbes = self.tools.GetGraphVariablesType()
		for each_value_type in [eval_total] + list(eval_varialbes):
			each_graph = np_fig.Figure(figsize=(self.graph_GUI_each_width, 1), dpi=100)
			each_plot = each_graph.add_subplot(111)
			graph_canvas = mp_tkagg.FigureCanvasTkAgg(each_graph, self.graph_frame)
			graph_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                        
			self.graph_plots[each_value_type] = each_plot
                        
			self.graph_animations.append(mp_ani.FuncAnimation(each_graph,
                                                                          self.GraphAnimation,
                                                                          fargs=(each_value_type,),
                                                                          interval=1000))
