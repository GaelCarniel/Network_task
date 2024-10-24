import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_square_around_node(ax, pos, node_index, x_range, y_range, size=0.1):
    """
    Draws a square around the specified node index in the graph.

    Parameters:
        ax: The axes to draw on.
        pos: Dictionary of node positions.
        node_index: Index of the node to draw the square around.
        size: Size of the square.
    """
    x, y = pos[node_index]
    square = Rectangle((x - size*x_range / 2, y - size*y_range / 2), size*x_range, size*y_range, linewidth=5, edgecolor='green', facecolor='none')
    ax.add_patch(square)

# Create the adjacency matrix
adj_matrix = np.array([[0, 1, 1, 0, 0, 1, 1],
                       [1, 0, 1, 0, 0, 0, 0],
                       [1, 1, 0, 1, 0, 0, 1],
                       [0, 0, 1, 0, 1, 0, 1],
                       [0, 0, 0, 1, 0, 1, 1],
                       [1, 0, 0, 0, 1, 0, 1],
                       [1, 0, 1, 1, 1, 1, 0]])

# Create a graph from the adjacency matrix
G = nx.from_numpy_array(adj_matrix)

# Define the private signal vector
private_signal = [0, 0, 1, 0, 1, 0, 1]

# Map the private signal to colors: 0 -> blue, 1 -> yellow
node_colors = ['blue' if signal == 0 else 'yellow' for signal in private_signal]


# Fix the seed for reproducibility in the layout
seed_value = 28
pos = nx.spring_layout(G, k=1.25, seed=seed_value)  # Use 'seed' parameter

# Create the network plot
fig, ax = plt.subplots(figsize=(8, 8))
#plt.figure(figsize=(8, 8))
#ax = plt.gca()  # Get the current axis

nx.draw(G, pos,
         node_color=node_colors,
         node_size=2500,  # Customize node size (adjust as needed)
         width=3,        # Customize edge width (adjust as needed)
         with_labels=False, # Remove labels
         ax=ax,
        linewidths=3,
        edgecolors="black")
# Print current axis limits and aspect ratio
x_limits = ax.get_xlim()
y_limits = ax.get_ylim()
x_range = x_limits[1] - x_limits[0]
y_range = y_limits[1] - y_limits[0]
print(f"x limits: {x_limits}, y limits: {y_limits}")
print(f"x range: {x_range}, y range: {y_range}")
print(f"Aspect ratio (y/x): {y_range / x_range}")

# Draw a circle around node number 3 (index 2 since it's zero-indexed)
draw_square_around_node(ax, pos, node_index=2, x_range=x_range, y_range=y_range,size=0.2)  # Adjust radius as needed



# Save the figure with a transparent background
#plt.title("Network")
plt.savefig("current_network.png", transparent=True)  # Save with transparent background
plt.close()  # Close the plot
