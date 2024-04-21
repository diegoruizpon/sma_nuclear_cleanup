'''

Created by Diego Ruiz, Joao Pedro, Lucas Vitoriano, Francisco García

Date of creation: 25/03/2024

Team number: 4


'''



from mesa import Agent
import random
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.agent.CommunicatingAgent import CommunicatingAgent

class baseAgent(CommunicatingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, unique_id)
        
        self.first_step = False
        self.robot_type = None

        self.knowledge = {
            "waste_type_I_can_hold": self.robot_type,
            "zone_I_can_move": self.robot_type,
            "pos": (0,0),
            "wasteCountHold": 0,
            "wasteTypeHold": 0,
            "have": [],
            "waste_pos": (0,0),
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

        #self. knowledge
        #teste

    def get_robot_type(self):
        return self.robot_type
    
    def get_count_waste(self):
        return self.knowledge["wasteCountHold"]
    
    def update(self, percepts):
        self.knowledge = percepts
    
    def deliberate(self):
        # positions = ["pos_robot", "pos_N", "pos_W", "pos_S", "pos_E"]
        # comprehended_list = [f"{pos}, {self.knowledge[pos]['wasteType']}" for pos in positions]
        
        possible_positions = self.model.grid.get_neighborhood(self.knowledge["pos"], moore=False, include_center=False)
        valid_directions = []

        messages = self.get_new_messages()
        if messages:
            for message in messages:
                if message.get_performative() == MessagePerformative.SEND_WASTE:
                    self.knowledge["waste_pos"] = message.get_content()
                    if self.knowledge["wasteCountHold"] == 0:
                        print("msg received")
                        return "move_to_waste"
                    
        if  self.knowledge["wasteCountHold"] == 0 and self.knowledge["waste_pos"] != None:
            return "move_to_waste"
        
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
                    pass
            elif cell[0] < self.pos[0]:  
                valid_directions.append("W")


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
                print(self.robot_type + 1)
                self.send_message(Message(self.unique_id, self.robot_type + 1, MessagePerformative.SEND_WASTE, self.knowledge["pos"])) 
                print("msg sent")
                
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
        return action 
        
    def step(self):
        percepts = None
        if self.first_step == False:
            action = self.deliberate()
            percepts = self.model.do(self, action)
            self.first_step = True
        else:
            if not percepts:
                percepts = self.knowledge
            self.update(percepts)
            action = self.deliberate()
            percepts = self.model.do(self, action)


class greenAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 0
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = self.robot_type



class yellowAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 1
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = self.robot_type



class redAgent(baseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.robot_type = 2
        self.knowledge["waste_type_I_can_hold"] = self.robot_type
        self.knowledge["zone_I_can_move"] = 10