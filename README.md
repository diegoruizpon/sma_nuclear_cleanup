# Self-Organization of Robots in a Hostile Environment
The project has been realized by the group:

Francisco Garcia

Diego Ruiz

Lucas Vitoriano

João Pedro Volpi

## Description

This project implements an agent-based simulation where robots operate in a hostile environment to collect, transform, and transport hazardous waste to a secure zone. The environment is divided into three zones, each with varying levels of radioactivity. Robots are designed with specific capabilities tailored to their operational zone, handling waste of different radioactivity levels—green, yellow, and red. The simulation explores concepts of self-organization, task allocation, and environmental interaction within robotic agents.

## Installation

To run this simulation, follow these steps:

1. Clone the repository to your local machine.
2. Ensure Python 3. or higher is installed on your system.
3. Install the required dependencies by running `pip install -r requirements.txt` in the terminal within the project directory.

## Usage

To start the simulation, navigate to the project directory and execute:

python run.py

## Features

- **Agent-Based Modeling:** Utilizes green, yellow, and red robots with distinct behaviors and capabilities.
- **Environmental Challenges:** Simulates various zones with differing levels of radioactivity, impacting robot movement and task execution.
- **Task Transformation:** Robots collect and transform waste, simulating a process of hazardous waste management.
- **Visualization:** Provides a graphical representation of the simulation, offering insights into the dynamic interaction between agents and their environment.

## Assummptions:

### Variables

The robot agents in this simulation operate with a knowledge base represented as a Python dictionary with the following structure:
```

knowledge = {
    "waste_type_I_can_hold": self.robot_type,  # Defines the type of waste the robot can hold
    "zone_I_can_move": self.robot_type,        # Indicates the zones where the robot can move
    "pos": (0, 0),                             # Current position of the robot
    "wasteCountHold": 0,                       # Count of waste currently held
    "wasteTypeHold": 0,                        # Type of waste currently held
    "have": [],                                # List of items the robot currently has
    "pos_robot": {                             # Information about the robot's current position
        "radioactivity_level": None,
        "wasteType": None,
        "agent": False
    },
    # Information about the positions North, East, South, and West of the robot
    "pos_N": {"radioactivity_level": None, "wasteType": None, "agent": False},
    "pos_E": {"radioactivity_level": None, "wasteType": None, "agent": False},
    "pos_S": {"radioactivity_level": None, "wasteType": None, "agent": False},
    "pos_W": {"radioactivity_level": None, "wasteType": None, "agent": False},
}
```

### Robot Functions

Robots in this simulation can perform the following functions:

Move: Change position within the allowed zone.

Collect Waste: Pick up waste if the robot's capacity allows.

Transform Waste: Convert collected waste into a different type, if applicable.

Deposit Waste: Place waste in a designated zone or facility.

### Model Restrictions

No two agents can occupy the same cell. The deliberate() function must avoid cells occupied by another robot.

Green robots are restricted to the green (low radioactivity) zone.

Yellow robots can operate in both green and yellow (medium radioactivity) zones.

Red robots have access to all zones.

Waste is initially placed randomly within the environment and can be of different types, corresponding to 
the robot that can handle it.

### Procedure with reasoning and without communication 

Determine potential movement blocks based on robot type and zone limitations.

If a red robot holds a red waste and can move east, it should do so. If not, deposit the waste.

If a robot holds waste that can be transformed and is in a block with similar waste, transform it.

If a robot can transform the waste it holds but cannot move east, it should deposit the waste.

If a robot is on top of waste, it should collect it.

If there's waste in the neighborhood, move towards the waste.

Otherwise, move randomly, avoiding cells with other robots.


## Credits

This project was inspired by the work detailed in [Agent-based model for hazardous waste management](http://emmanuel.adam.free.fr/site/spip.php?article80). Special thanks to all contributors and members of the project team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
