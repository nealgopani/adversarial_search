from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from main import Board
from main import d

def agent_portrayal(agent):
	if agent.name == 'pit':
		portrayal = {"Shape": "rect", "Color": agent.color, "Filled": "true", "Layer": 0, "w": 1, "h": 1}
	else:
		portrayal = {"Shape": f'img/{agent.img}', "Filled": "true", "Layer": 0, "w": 1, "h": 1}
	return portrayal

grid = CanvasGrid(agent_portrayal, d, d, 500, 500)

server = ModularServer(Board, [grid], "Adversarial Search", {"width":d, "height":d})
server.port = 8521 # The default
server.launch()