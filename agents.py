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
            "have": [],
            "pos_robot": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos_N": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos_E": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos_S": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
            "pos_W": {
                "radioactivity_level": None,
                "wasteType": None,
                "agent": False
            },
        }

        #self.knowledge
        
    def update(self, knowledge, percepts):
        self.knowledge = percepts
        return self.knowledge
    
    def deliberate(self, knowledge):
        positions = ["pos_robot", "pos_N", "pos_W", "pos_S", "pos_E"]
        comprehended_list = [f"{pos}, {self.knowledge[pos]['wasteType']}" for pos in positions]
        #print(f"I am {self.unique_id}. My knowledge is {self.knowledge['pos']} : {comprehended_list}")
        print(self.knowledge)
        possible_positions = self.model.grid.get_neighborhood(self.knowledge["pos"], moore=False, include_center=False)
        valid_directions = []
        for cell in possible_positions:
            if cell[1] > self.pos[1]:
                valid_directions.append("N") #north
            elif cell[1] < self.pos[1]:
                valid_directions.append("S")
            elif cell[0] > self.pos[0]:
                valid_directions.append("E")
            elif cell[0] < self.pos[0]:  
                valid_directions.append("W")
        action = None
        # 2 green waste -> 1 yellow waste
        if self.knowledge["wasteCountHold"] == 2:
            action = "transform"
        # agent has 1 yellow waste -> either deposit or moves east
        elif self.knowledge["wasteTypeHold"] == "yellow":
            print("Está acáaaaa")
            # there is zone2 at east and agent has 1 yellow waste -> deposit
            if self.knowledge["pos_W"]["radioactivity_level"] > 0.33:
                action = "deposit"
            
            elif self.pos[0] >= 4:  # This is a function fake, delete when added zone 2
                action = "deposit"
            # he has 1 yellow waste -> move right
            elif "E" in valid_directions:
                action = "move_E"
        # Here we know that it has 0 or 1 green waste
        # there is a green waste in agent position -> collect
        
        elif self.knowledge["pos_robot"]["wasteType"] == "green":
            action = "collect"
        else:
            # Try to move to a place with waste
            for i in valid_directions:
                if self.knowledge[f"pos_{i}"]["wasteType"] == "green":
                    action = f"move_{i}"
                    break
        if action == None:
            action = f"move_{random.choice(valid_directions)}"
        print('action: ', action)
        return action 
        
    def step(self):
        percepts = None
        if self.first_step == 0:
            action = self.deliberate(self.knowledge)
            percepts = self.model.do(self, action)
            self.first_step = 1
        else:
            if not percepts:
                percepts = self.knowledge
            self.update(self.knowledge, percepts)
            action = self.deliberate(self.knowledge)
            percepts = self.model.do(self, action)
            #print(f"Agent {self.unique_id} has value {self.knowledge.get('wasteCount')}")   
            #print(f"Agent {self.unique_id} is in {self.pos}")   
        

