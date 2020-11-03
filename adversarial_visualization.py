from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from main import GridModel
from main import d

def agent_portrayal(agent):
	portrayal = {"Shape": "rect", "Color": agent.color, "Filled": "true", "Layer": 0, "w": 1, "h": 1}
	return portrayal

grid = CanvasGrid(agent_portrayal, d, d, 500, 500)

server = ModularServer(GridModel, [grid], "A* Search", {"width":d, "height":d})
server.port = 8521 # The default
server.launch()