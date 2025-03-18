import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime

# Load the provided files and inspect values
ana_wrmse_path = 'ana_wrmse.npy'
ana_bias_path = 'ana_bias.npy'

# Load the arrays
ana_wrmse = np.load(ana_wrmse_path)
ana_bias = np.load(ana_bias_path)

# Define the variable names
first_four_names = ["u10", "v10", "t2m", "msl"]
second_array = ["z", "q", "u", "v", "t"]
pressure_levels = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]

# Function to get the variable name based on index
def get_variable_name(var_idx):
    if var_idx < 4:
        return first_four_names[var_idx]
    else:
        # Calculate the correct index for second combination
        second_idx = (var_idx - 4) // len(pressure_levels)
        pressure_idx = (var_idx - 4) % len(pressure_levels)
        return f"{second_array[second_idx]}{pressure_levels[pressure_idx]}"

# Define a function to plot and save RMSE and Bias for each variable
def plot_rmse_bias(ana_wrmse, ana_bias, save_dir="ana_rmse_bias"):
    os.makedirs(save_dir, exist_ok=True)

    # Adjust to visualize data from day 3 onwards
    lead_time_days = 50  # Correct lead time is 50 days
    start_date = datetime.datetime(2018, 1, 1)  # Start from January 1, 2018
    end_date = datetime.datetime(2018, 2, 20)  # End on February 20, 2018

    # Create a list of dates from January 1, 2018, to February 20, 2018
    date_range = [start_date + datetime.timedelta(days=i) for i in range(lead_time_days)]
    
    # Adjust to skip the first two days (i.e., start from day 3)
    lead_time = date_range[2:]  # Skip the first two days, resulting in 58 dates
    
    for var_idx in range(ana_wrmse.shape[1]):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='black')

        # Ensure y-data also matches 58 data points (skip first 2, and limit to 60 days total)
        y_wrmse = ana_wrmse[2:2+lead_time_days-2, var_idx]
        y_bias = ana_bias[2:2+lead_time_days-2, var_idx]

        # Get the variable name for the title
        variable_name = get_variable_name(var_idx)
        
        # Plot RMSE
        ax1.plot(lead_time, y_wrmse, 'w-', label="RMSE")  # Skip first two days
        ax1.set_title(f"{variable_name} - RMSE\n(From {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')})", color="white")
        ax1.set_xlabel("Lead Time (Days)", color="white")
        ax1.set_ylabel("RMSE", color="white")
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Format x-axis dates
        ax1.tick_params(colors='white')
        ax1.legend()
        ax1.grid(True, color="gray", linestyle="--", linewidth=0.5)
        
        # Plot Bias
        ax2.plot(lead_time, y_bias, 'b-', label="Bias")  # Skip first two days
        ax2.set_title(f"{variable_name} - Bias\n(From {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')})", color="white")
        ax2.set_xlabel("Lead Time (Days)", color="white")
        ax2.set_ylabel("Bias", color="white")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Format x-axis dates
        ax2.tick_params(colors='white')
        ax2.legend()
        ax2.grid(True, color="gray", linestyle="--", linewidth=0.5)

        # Rotate the x-axis date labels for better readability
        fig.autofmt_xdate()

        # Set plot background colors
        fig.patch.set_facecolor('black')
        ax1.set_facecolor('black')
        ax2.set_facecolor('black')
        
        # Save the plot
        plt.savefig(os.path.join(save_dir, f"{var_idx}_{variable_name}_rmse_bias.png"), facecolor=fig.get_facecolor())
        plt.close(fig)

# Call the function to plot and save
plot_rmse_bias(ana_wrmse, ana_bias)
