params_simulation_height = {
    "N_green": 2,
    "N_yellow": 2,
    "N_red": 2,
    "width": 20,
    "height": range(10, 30, 5),
    "num_waste": 15
}

params_simulation_width = {
    "N_green": 2,
    "N_yellow": 2,
    "N_red": 2,
    "width": range(10, 30, 5),
    "height": 20,
    "num_waste": 15
}

params_simulation_num_waste = {
    "N_green": 2,
    "N_yellow": 2,
    "N_red": 2,
    "width": 15,
    "height": 15,
    "num_waste": range(10, 15)
}


import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def give_info_simulation(simulation, hue, color, communication=False):
    
    params_simulation_height = {
        "N_green": 2,
        "N_yellow": 2,
        "N_red": 2,
        "width": 20,
        "height": range(10, 50, 10),
        "num_waste": 15
    }

    params_simulation_width = {
        "N_green": 2,
        "N_yellow": 2,
        "N_red": 2,
        "width": range(10, 50, 10),
        "height": 20,
        "num_waste": 15
    }

    params_simulation_num_waste = {
        "N_green": 2,
        "N_yellow": 2,
        "N_red": 2,
        "width": 15,
        "height": 15,
        "num_waste": range(10, 30, 5)
    }

    params_simulation_num_green_robots = {
        "N_green": range(1, 7, 2),
        "N_yellow": 2,
        "N_red": 2,
        "width": 15,
        "height": 15,
        "num_waste": 20
    }

    text_communication = " With communication" if communication else "No communication"
    text_communication2 = " with_communication" if communication else "no_communication"
    if hue == "N_green":
        hue_ = "the number of green robots"
    else:
        hue_ = hue

    if hue == "height":
        params = params_simulation_height
    elif hue == "width":
        params = params_simulation_width
    elif hue == "num_waste":
        params = params_simulation_num_waste
    elif hue == "N_green":
        params = params_simulation_num_green_robots
    if simulation == f"avg_n_steps_without_waste_{color}":
        title = f"Average n° steps without {color} waste depending\non {hue_} at each step ({text_communication})"
        y_label = "Average number of steps"
        path = f"avg_n_steps_without_waste_{color}_{text_communication2}_hue_{hue}.png"
    elif simulation == f"NuclearWaste_in_disposal_zone":
        title = f"N° of waste in disposal zone depending\non {hue_} at each step ({text_communication})"
        y_label = f"Waste in disposal zone"
        path = f"NuclearWaste_in_disposal_zone_{text_communication2}_hue_{hue}.png"
    else: 
        print("Simulation not found : ", simulation)
    return params, title, y_label, path

def simulate_and_save_figure(mission, it, max_steps, simulation, hue, color, communication=False):
    params, title, y_label, path = give_info_simulation(simulation, hue, color, communication)

    results = mesa.batch_run(
        mission,
        parameters=params,
        iterations=it,
        max_steps=max_steps,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )
    results_df = pd.DataFrame(results)

    g = sns.lineplot(
        data=results_df,
        x="Step",
        y=simulation,
        hue=hue,
        errorbar=("ci", 95),
        palette="tab10",
    )

    g.figure.set_size_inches(8, 4)
    g.set(title=title, ylabel=y_label);
    g.figure.savefig("Images/With_communication/"+path)
    #plt.show()
    plt.close(g.figure)

    # The simulation where you can see how many steps it takes to 
    # collect all the garbage is not suggested, because sometimes 
    # the game does not end. However, you can make a simulation 
    # where you can see the amount of garbage deposited, which is 
    # a proxy for the quality of the robot's strategy.