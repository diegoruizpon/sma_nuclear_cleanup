"""

Created by Diego Ruiz, Joao Pedro, Lucas Vitoriano, Francisco García

Date of creation: 25/03/2024

Team number: 4


"""

import mesa
from model import RobotMission
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, NuclearWaste
import random

import mesa

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def agent_portrayal(agent):
    
    if isinstance(agent, Radioactivity):
        
        if agent.radioactivity_level == 0:
            portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "#238823",
                 "w": 1,
                 "h": 1,
                 }
            
            
        if agent.radioactivity_level == 1:
            portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "#FFBF00",
                 "w": 1,
                 "h": 1,
                 }
            
        if agent.radioactivity_level == 2:
            portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "#D2222D",
                 "w": 1,
                 "h": 1,
                 }
            
            
        if agent.radioactivity_level == 10: # waste disposal zone
            
            portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "#000000",
                 "w": 1,
                 "h": 1,
                 }      
        
    else:
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 2,
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
            
            portrayal = {
                "Shape": "ressources/green_black_rob.png",
                "scale": 0.9,
                "Layer": 2,
                
            }
            #portrayal["Color"] = "green"

        if isinstance(agent, yellowAgent):
            
            portrayal = {
                "Shape": "ressources\yellow_black_rob.png",
                "scale": 0.9,
                "Layer": 2,
                
            }
            #portrayal["Color"] = "#FFC03E"

        if isinstance(agent, redAgent):
            
            portrayal = {
                "Shape": "ressources/red_black_rob.png",
                "scale": 0.9,
                "Layer": 2,
                
            }

            
             
            
            
            #portrayal["Color"] = "red"

        if isinstance(agent, NuclearWaste):
            if agent.wasteType == 0:
                portrayal["Shape"] = "ressources\green_waste.png"
                #portrayal["Color"] = light_green
            if agent.wasteType == 1:
                
                portrayal["Shape"] = "ressources\yellow_waste.png"
            if agent.wasteType == 2:
                portrayal["Shape"] = r"ressources\red_waste.png"

        if isinstance(agent, Radioactivity):
            

            if agent.radioactivity_level == 10: # waste disposal zone
                portrayal["Color"] = "#000000"

    return portrayal


model_params = {
    # Parameter definition for the model 
    
    "title": mesa.visualization.StaticText("Robot Mission"),
    "N_green": mesa.visualization.Slider(
        "Number of green robots", 1, 1, 10, 2
    ),
    "N_yellow": mesa.visualization.Slider(
        "Number of yellow robots", 1, 1, 10, 2
    ),
    "N_red": mesa.visualization.Slider(
        "Number of red robots", 1, 1, 10, 2
    ),
    "width": 15,
    "height": 15,
    "num_waste": mesa.visualization.Slider(
        "Number of green waste", 1, 1, 10, 2
    ),
}


if __name__=="__main__":

    width = 16
    height = 15

    #model_params = {"N_green": 2, "N_yellow": 2, "N_red": 2, "width": width, "height": height, "num_waste": 8}
    model_params["width"] = width
    model_params["height"] = height
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)


    chart_element0 = mesa.visualization.ChartModule(
        [
            {"Label": "NuclearWaste_green", "Color": "#D0F0C0"},
            {"Label": "NuclearWaste_yellow", "Color": "#FFE8A1"},
            {"Label": "NuclearWaste_red", "Color": "#E8AFAF"},
        ]
    )
    chart_element1 = mesa.visualization.ChartModule(
        [
            {"Label": "NuclearWaste_taked_by_green", "Color": "#D0F0C0"},
            {"Label": "NuclearWaste_yellow", "Color": "#FFE8A1"},
            {"Label": "NuclearWaste_red", "Color": "#E8AFAF"},
        ]
    )



    from tests_parameters import params_simulation_height, params_simulation_width, params_simulation_num_waste
    # There must be a coherence between chosen_sumulation and labels_hue
    chosen_simulation = params_simulation_width # params_simulation_height # params_simulation_num_waste
    labels_hue = 'width' # "height" # 'num_waste'

    results = mesa.batch_run(
        RobotMission,
        parameters=chosen_simulation,
        iterations=5,
        max_steps=100,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )
    
    results_df = pd.DataFrame(results)
    #print(results_df.columns)

    g = sns.lineplot(
        data=results_df,
        x="Step",
        #y="NuclearWaste_in_disposal_zone", 
        y='avg_n_steps_without_waste_red',
        hue=labels_hue,
        errorbar=("ci", 95),
        palette="tab10",
    )
    g.figure.set_size_inches(8, 4)
    plot_title = "Number of red waste at the end of steps depending on number of initial waste"
    g.set(title=plot_title, ylabel="Number of red waste");
    plt.show()





    from tests_parameters import give_info_simulation, simulate_and_save_figure
    labels_hues = ["N_green", "width", "height", "num_waste"] #  
    colors = ["green", "yellow", "red"]

    # variable = "NuclearWaste_in_disposal_zone"
    # for labels_hue in labels_hues:
    #     simulate_and_save_figure(mission=RobotMission, it=100, max_steps=300, simulation=variable, hue=labels_hue, color=None, communication=True)
    variable = "avg_n_steps_without_waste_"
    for labels_hue in labels_hues:
        for color in colors:
            if labels_hue == "N_green" and color != "green":
                continue
            simulate_and_save_figure(mission=RobotMission, it=100, max_steps=300, simulation=variable+color, hue=labels_hue, color=color, communication=True)
    


    server = ModularServer(RobotMission, [grid, chart_element0, chart_element1], "Robot Mission", model_params)

    #server.port = 8540
    
    server.port = random.randint(1, 8540)

    server.launch()


