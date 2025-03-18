import os
import numpy as np
import matplotlib.pyplot as plt

# Load the .npy file
data = np.load('xb.npy')

# Get the number of slices
num_slices = data.shape[0]

# Create a directory to save the plots
save_dir = "result"
os.makedirs(save_dir, exist_ok=True)

# Define the names for the first four slices and for the rest
first_four_names = ["u10", "v10", "t2m", "msl"]
second_part_names = ["z", "q", "u", "v", "t"]
levels = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]

# Function to get the correct slice name
def get_slice_name(slice_idx):
    if slice_idx < 4:
        return first_four_names[slice_idx]
    else:
        # Compute the name from the second part
        var_idx = (slice_idx - 4) // len(levels)  # Which variable (z, q, etc.)
        level_idx = (slice_idx - 4) % len(levels)  # Which level (50, 100, etc.)
        return f"{second_part_names[var_idx]}{levels[level_idx]}"

# Function to plot and save each slice with detailed information
def plot_slice(slice_idx):
    # Extract the current slice
    current_slice = data[slice_idx, :, :]
    
    # Create figure for the image slice
    fig, ax_img = plt.subplots(figsize=(6, 5))
    
    # Plot the image slice
    im = ax_img.imshow(current_slice, cmap='viridis', aspect='auto')
    
    # Add the correct title with Min/Max and slice name
    slice_name = get_slice_name(slice_idx)
    ax_img.set_title(f"{slice_name} - Min: {current_slice.min():.2f}, Max: {current_slice.max():.2f}")
    ax_img.set_xlabel("X-axis")
    ax_img.set_ylabel("Y-axis")
    
    # Add colorbar for the image
    fig.colorbar(im, ax=ax_img, orientation='vertical')
    
    plt.tight_layout()
    
    # Save the plot as an image file
    plt.savefig(os.path.join(save_dir, f"slice_{slice_idx}_{slice_name}.png"))
    plt.close(fig)

# Loop through all slices and plot/save them
for slice_idx in range(0, num_slices):
    plot_slice(slice_idx)
