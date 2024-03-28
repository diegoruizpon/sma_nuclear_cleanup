from mesa import Agent

class greenAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        #Number of waste stocked  
        self.WasteCount = 0
        #Position
        self.pos = (0,0)
        
        
        self.knowledge = {
            "wasteCount": 0,
            "wasteType": 1
        }
        
    def update(self, knowledge, percepts):
        return knowledge
    
    def deliberate(self, knowledge):
        return "move"
    
    
        
        
        
    def move(self,model):
        
        x, y = self.pos
        
        possible_positions = model.grid.get_neighborhood( (x, y), moore=True, include_center=False )
       
        # moving an agent to a random position in this list is then easy:
        new_position = model.random.choice(possible_positions)

        model.grid.move_agent(self, new_position)
        
    def step(self):
        #... define the perception-deliberation-action loop here ...
        
        percepts = {"nada" : 0}
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        percepts = self.model.do(self, action)
        print(f"Agent {self.unique_id} has value {self.knowledge.get('wasteCount')}")   
        

