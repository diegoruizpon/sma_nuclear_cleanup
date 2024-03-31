from model import RobotMission
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, WasteDisposalZone, NuclearWaste

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "grey",
                 "r": 0.5}
    
    # if agent.unique_id > (25-1) and agent.unique_id < (25+3-1):
    #     portrayal["Color"] = agent.wasteType#"green"
    # if agent.unique_id > (25+3-1):
    #     portrayal["Color"] = "red"
    
    light_green = "#D0F0C0"
    light_yellow = "#FFE8A1"
    light_red = "#E8AFAF"

    if isinstance(agent, greenAgent):
        portrayal["Color"] = "green"

    if isinstance(agent, yellowAgent):
        portrayal["Color"] = "yellow"

    if isinstance(agent, redAgent):
        portrayal["Color"] = "red"

    if isinstance(agent, NuclearWaste):
        if agent.wasteType == 0:
            portrayal["Color"] = light_green
        if agent.wasteType == 1:
            portrayal["Color"] = light_yellow
        if agent.wasteType == 2:
            portrayal["Color"] = light_red

    return portrayal


if __name__=="__main__":
    grid = CanvasGrid(agent_portrayal, 15, 5, 600, 400)
    server = ModularServer(RobotMission, [grid], "Robot Mission", {"N": 1, "width": 5, "height": 5, "num_waste": 3})
    #server.port = 8540
    import random
    server.port = random.randint(1, 8540)

    server.launch()


