from mesa import Agent
import random


class baseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.first_step = 0
        self.robot_type = None

        self.knowledge = {
            "waste_type_I_can_hold": self.robot_type,
            "zone_I_can_move": self.robot_type,
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
        # positions = ["pos_robot", "pos_N", "pos_W", "pos_S", "pos_E"]
        # comprehended_list = [f"{pos}, {self.knowledge[pos]['wasteType']}" for pos in positions]
        #print(f"I am {self.unique_id}. My knowledge is {self.knowledge['pos']} : {comprehended_list}")
        print(self.knowledge)
        possible_positions = self.model.grid.get_neighborhood(self.knowledge["pos"], moore=False, include_center=False)
        valid_directions = []
        cant_move_east = self.knowledge["pos_E"]["radioactivity_level"] > self.knowledge["zone_I_can_move"]
        for cell in possible_positions:
            if cell[1] > self.pos[1]:
                valid_directions.append("N") #north
            elif cell[1] < self.pos[1]:
                valid_directions.append("S")
            elif cell[0] > self.pos[0]:
                if not cant_move_east:
                    valid_directions.append("E")
                else:
                    print(self.knowledge["pos_E"]["radioactivity_level"], self.knowledge["zone_I_can_move"])
            elif cell[0] < self.pos[0]:  
                valid_directions.append("W")

        # pos_list = ["N", "S", "E", "W"]
        # for pos in pos_list:
        #     # if there is a robot in the position, the agent can't move there
        #     if self.knowledge[f"pos_{pos}"]["agent"] != False and pos in valid_directions:
        #         print(f"Agent {self.unique_id} can't move to {pos}")
        #         print(valid_directions)
        #         valid_directions.remove(pos)
        #         print(self.knowledge)


        action = None

        if self.knowledge["waste_type_I_can_hold"] == 2 and self.knowledge["wasteCountHold"] == 1:
            if "E" in valid_directions:
                action = "move_E"
            else:
                action = "deposit"
        elif self.knowledge["wasteCountHold"] == 2:
            action = "transform"
        # agent has 1 yellow waste -> either deposit or moves east
        elif self.knowledge["wasteTypeHold"] == (self.knowledge["waste_type_I_can_hold"] + 1): # Means he holds a waste that has been transformed
            # there is zone2 at east and agent has 1 yellow waste -> deposit
            if cant_move_east: # WHY Pos_W ??  --> True, it is not Pos_W, but E, I corrected :)
                action = "deposit"
            
            # elif self.pos[0] >= 4:  # This is a function fake, delete when added zone 2
            #     action = "deposit"
            # he has 1 yellow waste -> move right
            elif "E" in valid_directions:
                action = "move_E"
        # Here we know that it has 0 or 1 green waste
        # there is a green waste in agent position -> collect
        
        elif self.knowledge["pos_robot"]["wasteType"] == self.knowledge["waste_type_I_can_hold"]:
            action = "collect"
        else:
            # Try to move to a place with waste
            for i in valid_directions:
                if self.knowledge[f"pos_{i}"]["wasteType"] == self.knowledge["waste_type_I_can_hold"]:
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
        

class greenAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 0
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = self.robot_type

    def deliberate(self, knowledge):
        action = super().deliberate(knowledge)  
        return action

class yellowAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 1
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = self.robot_type

    def deliberate(self, knowledge):
        action = super().deliberate(knowledge)  
        return action

class redAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 2
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = 10

    def deliberate(self, knowledge):
        action = super().deliberate(knowledge)  
        return action
