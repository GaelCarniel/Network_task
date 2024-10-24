from psychopy import visual, core, event
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def init():
    # Create the adjacency matrix
    adj_matrix = np.array([[0, 1, 1, 0, 0, 1, 1],
                           [1, 0, 1, 0, 0, 0, 0],
                           [1, 1, 0, 1, 0, 0, 1],
                           [0, 0, 1, 0, 1, 0, 1],
                           [0, 0, 0, 1, 0, 1, 1],
                           [1, 0, 0, 0, 1, 0, 1],
                           [1, 0, 1, 1, 1, 1, 0]]);
    return adj_matrix 

def square_the_node(ax, pos, node_index, x_range, y_range, size=0.1):
    x, y = pos[node_index];
    square = Rectangle((x - size*x_range / 2, y - size*y_range / 2), size*x_range, size*y_range, linewidth=5, edgecolor='green', facecolor='none');
    ax.add_patch(square);

def generate_network(adj_mat, node_index, uncover = [0], private_signal = [0, 0, 1, 0, 1, 0, 1],colours=['#cab79a','blue','yellow'],seed_value = 28,outputname="current_network.png"):
    '''Create a .png containing the appropriate graph'''
    if uncover == 'clear':
        uncover = [0,1,2,3,4,5,6];

    G = nx.from_numpy_array(adj_mat);

    #Create white network
    node_colors = [colours[0]]*len(private_signal);
    node_edge_colors = ['green'] + ['black']*(len(private_signal)-1);


    #Apply colors on uncover part
    for i in range(len(node_colors)):
        if i in uncover:
            node_colors[i] = colours[private_signal[i]+1];

    pos = nx.spring_layout(G, k=1.25, seed=seed_value);
    
    #Create the figure
    fig, ax = plt.subplots(figsize=(8, 8));
    ax.margins(x=0.1, y=0.1)

    nx.draw(G, pos,
            node_color=node_colors,
            node_size=2500,
            width=3,
            with_labels=False,
            ax=ax,
            linewidths=[5]+ [3]*(len(private_signal)-1),
            edgecolors=node_edge_colors);

    # Cast the square in the right plane and draws it
    x_limits = ax.get_xlim()
    y_limits = ax.get_ylim()
    x_range = x_limits[1] - x_limits[0]
    y_range = y_limits[1] - y_limits[0]

    for n in node_index:
        square_the_node(ax, pos, n, x_range=x_range, y_range=y_range,size=0.2)


    # Save the figure
    plt.savefig(outputname, transparent=True)  # Save with transparent background
    plt.close()

