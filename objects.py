'''

Created by Diego Ruiz, Joao Pedro, Lucas Vitoriano, Francisco García

Date of creation: 25/03/2024

Team number: 4


'''



from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class Radioactivity(Agent):
    def __init__(self, unique_id, model, zone): #, pos):
        super().__init__(unique_id, model)
        
        # Radioactivity level 
        self.radioactivity_level = zone
        
        #Position
        #self.pos = pos It has to as self. pos to grid
        self.waste = None
        self.has_agent = False
        self.agent = None

    def add_agent(self, agent):
        self.has_agent = True
        self.agent = agent

    def remove_agent(self):
        self.has_agent = False
        self.agent = None

    def add_waste(self, waste):
        self.waste = waste

    def remove_waste(self):
        self.waste = None
        

class NuclearWaste(Agent):
    def __init__(self, unique_id, model, wasteType): #, pos):
        super().__init__(unique_id, model)
        
        self.wasteType = wasteType # Start being green at the begining
        self.robot = None
        self.in_disposal_zone = False
        #self.pos = pos It has to as self. pos to grid
        # self.is_green = self.is_yellow = self.is_red = False
        # if wasteType == 0:
        #     self.is_green = True
        # elif wasteType == 1:
        #     self.is_yellow = True
        # elif wasteType == 2:
        #     self.is_red = True
        
    def step(self):
        pass
        #... define the perception-deliberation-action loop here ...