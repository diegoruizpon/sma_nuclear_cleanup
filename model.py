'''

Created by Diego Ruiz, Joao Pedro, Lucas Vitoriano, Francisco García

Date of creation: 25/03/2024

Team number: 4


'''




from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import greenAgent, yellowAgent, redAgent
from objects import Radioactivity, NuclearWaste
from communication.message.MessageService import MessageService
import random

class RobotMission(Model):
    def __init__(self, N_green, N_yellow, N_red, num_waste , width, height):
        super().__init__()
        self.__messages_service = MessageService(self.schedule)
        #MessageService.get_instance().set_instant_delivery(False)
        self.N_green = N_green
        self.N_yellow = N_yellow
        self.N_red = N_red
        self.num_waste = num_waste
        self.grid = MultiGrid(width, height, torus = False)
        self.schedule = RandomActivation(self)

        # Create Radioactivity
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                
                if x <= self.grid.width//3:
                    a = Radioactivity(y+x*self.grid.height, self, 0)
                elif x <= 2*self.grid.width//3 and x > self.grid.width//3:
                    a = Radioactivity(y+x*self.grid.height, self, 1)
                elif x == self.grid.width-1: # waste disposal zone
                    a = Radioactivity(y+x*self.grid.height, self, 10)                
                else:
                    a = Radioactivity(y+x*self.grid.height, self, 2)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))

        # Create waste blocks
        for i in range(self.num_waste):
            index_ = i+self.grid.width*self.grid.height
            a = NuclearWaste(index_, self, 0) # All the waste starts being green
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width//3)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        # Create robots
        def create_agent(AgentClass, color):
            a = AgentClass(i+self.num_waste+self.grid.width*self.grid.height, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            if color == "green":
                p1, p2 = 0, self.grid.width//3
            elif color == "yellow":
                p1, p2 = self.grid.width//3, 2*self.grid.width//3
            else:
                p1, p2 = 2*self.grid.width//3+1, self.grid.width-1
            x = self.random.randrange(p1, p2)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            a.knowledge["pos"] = (x, y)
            
            neighborhood = self.grid.get_neighborhood(a.pos, moore=False, include_center=True)
        
            for cell in neighborhood:
                if cell[0] == a.pos[0] and cell[1] == a.pos[1]:
                    direction = "robot"
                if cell[1] > a.pos[1]:
                    direction = "N" #north
                elif cell[1] < a.pos[1]:
                    direction = "S"
                elif cell[0] > a.pos[0]:
                    direction = "E"
                elif cell[0] < a.pos[0]:  
                    direction = "W"
                a.knowledge[f"pos_{direction}"]["wasteType"] = None
                elements = self.grid.get_cell_list_contents([cell])
                for element in elements:
                    if isinstance(element, Radioactivity):
                        a.knowledge[f"pos_{direction}"]["radioactivity_level"] = element.radioactivity_level
                    if isinstance(element, greenAgent) or isinstance(element, yellowAgent) or isinstance(element, redAgent):
                        a.knowledge[f"pos_{direction}"]["agent"] = True
                    if isinstance(element, NuclearWaste):
                        a.knowledge[f"pos_{direction}"]["wasteType"] = element.wasteType

        for i in range(N_green):
            create_agent(greenAgent, "green")

        for i in range(N_yellow):
            create_agent(yellowAgent, "yellow")

        for i in range(N_red):
            create_agent(redAgent, "red")

        
            
            
        self.running = True
        
    def do(self, agent, action):
        percepts = agent.knowledge

        if "move" in action:
            x, y = agent.pos
            if "N" in action:
                y += 1
            elif "E" in action:
                x += 1
            elif "S" in action:
                y -= 1
            elif "W" in action:
                x -= 1
            self.grid.move_agent(agent, (x, y))
            agent.knowledge["pos"] = (x, y)

            neighborhood = self.grid.get_neighborhood(agent.pos, moore=False, include_center=True)
        
            for cell in neighborhood:
                if cell[0] == agent.pos[0] and cell[1] == agent.pos[1]:
                    direction = "robot"
                if cell[1] > agent.pos[1]:
                    direction = "N" #north
                elif cell[1] < agent.pos[1]:
                    direction = "S"
                elif cell[0] > agent.pos[0]:
                    direction = "E"
                elif cell[0] < agent.pos[0]:  
                    direction = "W"
                agent.knowledge[f"pos_{direction}"]["wasteType"] = None
                elements = self.grid.get_cell_list_contents([cell])
                for element in elements:
                    if isinstance(element, Radioactivity):
                        agent.knowledge[f"pos_{direction}"]["radioactivity_level"] = element.radioactivity_level
                    if isinstance(element, greenAgent) or isinstance(element, yellowAgent) or isinstance(element, redAgent):
                        agent.knowledge[f"pos_{direction}"]["agent"] = True
                    if isinstance(element, NuclearWaste):
                        if element.robot == None:
                            #print("--"*10)
                            agent.knowledge[f"pos_{direction}"]["wasteType"] = element.wasteType
             
        elif action == "collect":
            # Check if there is waste to collect
            #agent.collect(self)
            elements = self.grid.get_cell_list_contents([agent.pos])
            for element in elements:
                if isinstance(element, NuclearWaste):
                    element.robot = agent
                    agent.knowledge["have"].append(element)
                    agent.knowledge["wasteCountHold"] += 1
                    agent.knowledge["wasteTypeHold"] = element.wasteType
                    agent.knowledge["pos_robot"]["wasteType"] = None
                    self.grid.remove_agent(element)

        elif action == "deposit":
            # Check if there is a disposal zone to deposit
            #agent.deposit(self)
            for element in agent.knowledge["have"]:
                element.robot = None
                if not isinstance(agent, redAgent):
                    self.grid.place_agent(element, agent.pos)
            agent.knowledge["have"] = []
            agent.knowledge["wasteCountHold"] = 0
            agent.knowledge["wasteTypeHold"] = None

        elif action == "transform":
            # Check if there is a disposal zone to transform 
            #agent.transform(self)  
            # Here i have also to destroy one of the elements 
            agent.knowledge["wasteCountHold"] = 1
            elements = agent.knowledge["have"]
            # for element in elements:
            #     print(element)
            self.schedule.remove(elements[0])
            elements[0].robot = None
            # if elements[1].wasteType == "green":
            #     elements[1].wasteType = "yellow"
            elements[1].wasteType += 1

            agent.knowledge["wasteTypeHold"] = elements[1].wasteType
            agent.knowledge["have"] = [elements[1]]

        percepts = agent.knowledge

        return percepts
        
    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

    # Assuming 'model' is your model instance and it has attributes 'schedule' for the scheduler
# and 'space' for the space where agents are placed (like a Grid or Network).

   