import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from ipywidgets import widgets, VBox
from IPython.display import display, clear_output

# Step 1: Display base path dropdown for selection
def display_base_path_selector():
    base_path_widget = widgets.Dropdown(
        options=['Results_Concrete', '../Push results'],
        value=None,
        description='Base Path:',
        disabled=False
    )
    return base_path_widget

# Step 2: Function to get directories in the base path
def get_directories(base_path):
    directories = []
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            dir_path = os.path.relpath(os.path.join(root, dir_name), base_path)
            directories.append(dir_path)
    return directories

# Step 3: Display multi-select widget for directories
def display_directory_selector(base_path):
    directories = get_directories(base_path)
    combo_widget = widgets.SelectMultiple(
        options=directories,
        value=[],  # Allows selecting multiple items
        description='Directories:',
        disabled=False,
        layout = widgets.Layout(width='100%')
    )
    return combo_widget

# Step 4: Load and process the data from a CSV file
def load_data(filename, budget=10):
    df = pd.read_csv(filename)
    strength = df['Compressive Strength'].values

    if len(strength) < budget:
        last_value = strength[-1] if len(strength) > 0 else 0
        strength = np.pad(strength, (0, budget - len(strength)), constant_values=last_value)
    return strength

# Step 5: Load data from all selected directories and accumulate it
def load_selected_data(selected_direrctory):
    data = []
    for dir_name in os.listdir(selected_direrctory):
        file = os.path.join(selected_direrctory, dir_name)
        if file.endswith('.csv'):
            strength = load_data(file)
            data.append(strength)
    return data

# Step 6: Trigger the plot based on selected directories
def plot_results(base_path, selected_dirs, desired_target=64.86370000000001):
    plt.figure(figsize=(10, 6))
    #print(selected_dirs)
    # Load and process data
    for dir_name in selected_dirs:
        dir_path = os.path.join(base_path, dir_name)
        #print(dir_path)

        data = load_selected_data(dir_path)
        max_length = max(len(arr) for arr in data)
        data = [arr for arr in data if len(arr) == max_length]
        #print(data)
        data = np.array(data)
        number_of_runs = len(data)
        cumulative_data = []
        for line in data:
            if line is None:
                continue  # Skip if no data for this line
                # Calculate cumulative max for each run
            cumulative_strengths = np.maximum.accumulate(line)
            cumulative_data.append(cumulative_strengths)
        cumulative_data = np.array(cumulative_data)
        average_array = np.mean(cumulative_data, axis=0)
        #print(average_array)
        
        percentile_10 = np.percentile(cumulative_data, 10, axis=0)
        standard_deviation = np.std(cumulative_data, axis=0)

        x = list(range(1, len(average_array) + 1))
        plt.plot(x, average_array, linestyle='-', label=f"{dir_name}, Runs = {number_of_runs}")
        plt.plot(x, percentile_10, linestyle='--', label=f"{dir_name} 10th Percentile")
        plt.errorbar(x, average_array, yerr=standard_deviation, fmt='-.', label=f"{dir_name} Mean ± Std Dev")
    # Plotting settings
    plt.axhline(y=desired_target, color='r', linestyle='--', label='Desired Target')
    plt.xlabel('Number of Development Cycles')
    plt.ylabel('Compressive Strength')
    plt.title("Compressive Strengths for different prompts")
    plt.legend()
    plt.grid(True)
    plt.show()

# Step 7: Initialize and display the widgets
base_path_widget = display_base_path_selector()
directory_selector = widgets.SelectMultiple(description="Directories", options=[])
plot_button = widgets.Button(description="Plot Results")

# Step 8: Handle base path selection change
def on_base_path_change(change):
    if change['new']:
        # Update the directory selector with new base path directories
        base_path = change['new']
        directories = get_directories(base_path)
        directory_selector.options = directories

# Step 9: Handle the plot button click
def on_plot_button_click(b):
    selected_dirs = directory_selector.value
    if not selected_dirs:
        print("Please select at least one directory.")
        return
    
    # Clear only the previous plot output, keeping widgets intact
    clear_output(wait=True)
    display(VBox([base_path_widget, directory_selector, plot_button]))  # Keep widgets displayed
    plot_results(base_path_widget.value, selected_dirs)

# Attach observers and event handlers
base_path_widget.observe(on_base_path_change, names='value')
plot_button.on_click(on_plot_button_click)

# Display the widgets in the notebook
display(VBox([base_path_widget, directory_selector, plot_button]))
