from model import RobotMission
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "grey",
                 "r": 0.5}
    
    if agent.unique_id > (25-1) and agent.unique_id < (25+3-1):
        portrayal["Color"] = agent.wasteType#"green"
    if agent.unique_id > (25+3-1):
        portrayal["Color"] = "red"
    return portrayal


if __name__=="__main__":
    grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    server = ModularServer(RobotMission, [grid], "Robot Mission", {"N": 1, "width": 5, "height": 5, "num_waste": 3})
    #server.port = 8540
    import random
    server.port = random.randint(1, 8540)

    server.launch()


