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
        # IF ACTION == MOVE
        if action == "move":
            # Feasability of movement according to neighbors
            agent.move(self)
            
        percepts = {"nada" : 0} 
        return percepts
        
    def step(self):
        self.schedule.step()