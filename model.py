from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import greenAgent
from objects import Radioactivity, WasteDisposalZone, NuclearWaste

class RobotMission(Model):
    def __init__(self, N, num_waste , width, height):
        super().__init__()
        self.num_agents = N
        self.num_waste = num_waste
        self.grid = MultiGrid(width, height, torus = False)
        self.schedule = RandomActivation(self)
        
        # Create robots
        for i in range(self.num_agents):
            a = greenAgent(i, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            
        # Create waste blocks
        for i in range(self.num_waste):
            a = NuclearWaste(i+self.num_agents, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        self.running = True
        
    def do(self, agent, action):
        percepts = agent.knowledge

        if action is tuple:
            x, y = agent.pos

            self.grid.move_agent(agent, (action[0], action[1]))

            for pos in ["pos1", "pos2", "pos3", "pos4", "pos5", "pos6", "pos7", "pos8", "pos9"]:
                percepts[pos]["radioactivity_level"] = self.model.grid.get_cell_list_contents([self.pos])
                percepts[pos]["wasteType"] = 
                percepts[pos]["agent"] = 

        if action == "collect":
            # Check if there is waste to collect
            if 
            agent.collect(self)

        if action == "deposit":
            # Check if there is a disposal zone to deposit
            agent.deposit(self)

        # IF ACTION == TRANSFORM
        if action == "transform":
            # Check if there is a disposal zone to transform
            agent.transform(self)   

        return percepts
        
    def step(self):
        self.schedule.step()