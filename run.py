from model import RobotMission
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "green",
                 "r": 0.5}
    
    if agent.unique_id > 2:
        portrayal["Color"] = "grey"
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RobotMission, [grid], "Robot Mission", {"N": 3, "width": 10, "height": 10, "num_waste": 2})
server.port = 8540

server.launch()


