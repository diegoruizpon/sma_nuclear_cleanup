'''

Created by Diego Ruiz, Joao Pedro, Lucas Vitoriano, Francisco García

Date of creation: 25/03/2024

Team number: 4


'''


from model import RobotMission
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, NuclearWaste

import mesa

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
        portrayal["Color"] = "#FFC03E"

    if isinstance(agent, redAgent):
        portrayal["Color"] = "red"

    if isinstance(agent, NuclearWaste):
        if agent.wasteType == 0:
            portrayal["Color"] = light_green
        if agent.wasteType == 1:
            portrayal["Color"] = light_yellow
        if agent.wasteType == 2:
            portrayal["Color"] = light_red

    if isinstance(agent, Radioactivity):
        if agent.radioactivity_level == 0:
            portrayal["Color"] = "#eeeeee"

        if agent.radioactivity_level == 1:
            portrayal["Color"] = "#bcbcbc"

        if agent.radioactivity_level == 2:
            portrayal["Color"] = "#777777"

        if agent.radioactivity_level == 10: # waste disposal zone
            portrayal["Color"] = "#000000"

    return portrayal


if __name__=="__main__":

    width = 15
    height = 15

    model_params = {"N_green": 2, "N_yellow": 2, "N_red": 2, "width": width, "height": height, "num_waste": 8}
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)


    chart_element = mesa.visualization.ChartModule(
        [
            {"Label": "NuclearWaste_green", "Color": "#D0F0C0"},
            {"Label": "NuclearWaste_yellow", "Color": "#FFE8A1"},
            {"Label": "NuclearWaste_red", "Color": "#E8AFAF"},
        ]
    )


    server = ModularServer(RobotMission, [grid, chart_element], "Robot Mission", model_params)

    #server.port = 8540
    import random
    server.port = random.randint(1, 8540)

    server.launch()


