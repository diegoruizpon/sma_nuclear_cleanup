from mesa import Agent
import random


class greenAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.first_step = 0

        self.knowledge = {
            "pos": (0,0),
            "wasteCountHold": 0,
            "wasteTypeHold": 0,
            "pos1": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos2": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos3": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos4": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos5": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos6": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos7": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos8": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos9": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            }
        }

        self.knowledge
        
    def update(self, percepts):
        self.knowledge = percepts
        return self.knowledge
    
    def deliberate(self):
        possible_positions = self.model.grid.get_neighborhood( self.knowledge["pos"], moore=True, include_center=False)


        action = None
        # 2 green waste -> 1 yellow waste
        if self.knowledge["wasteCountHold"] == 2:
            action = "transform"
        # agent has 1 yellow waste -> either deposit or moves east
        elif self.knowledge["wasteTypeHold"] == 1:
            # there is zone2 at east and agent has 1 yellow waste -> deposit
            if self.knowledge["pos6"]["radioactivity"] == 1:
                action = "deposit"
            # he has 1 yellow waste -> move right
            else:
                action = "move6"
        # Here we know that it has 0 or 1 green waste
        # there is a green waste in agent position -> collect
        
        elif self.knowledge["pos5"]["wasteType"] == 1:
            action = "collect"
        else:
            # Try to move to a place with waste
            for i in [1,2,3,4,7,8,9]:
                if self.knowledge[f"pos{i}"]["wasteType"] == 1:
                    action = f"move{i}"
                    break
        if action == None:
            action = f"move{random.choice([1,2,3,4,6,7,8,9])}"
        return action 
        
    def step(self):
        if self.first_step == 0:
            action = self.deliberate(self.knowledge)
            percepts = self.model.do(self, action)
            self.first_step = 1
        else:
            self.update(self.knowledge, percepts)
            action = self.deliberate(self.knowledge)
            percepts = self.model.do(self, action)
            print(f"Agent {self.unique_id} has value {self.knowledge.get('wasteCount')}")   
        

