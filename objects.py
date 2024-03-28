from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid



class Radioactivity(Agent):
    def __init__(self, unique_id, model, zone):
        super().__init__(unique_id, model)
        
        # Radioactivity level
        self.level = self.random.uniform(0, 1.0/3 * zone)
        
        #Position
        self.pos = (0,0)
        

class WasteDisposalZone(Agent):
    def __inti__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        #Position
        self.pos = (0,0)
        
        self.wasteCollected = 0
        
    def step(self):
        #... define the perception-deliberation-action loop here ...
        
        print("No waste collected yet")

class NuclearWaste(Agent):
    def __inti__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        # Waste type
        
        
        
        #Position
        self.pos = (0,0)
        
    def step(self):
        #... define the perception-deliberation-action loop here ...
        
        print("Not collected yet")