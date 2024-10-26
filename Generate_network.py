from psychopy import visual, core, event
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Create a class to group stimuli
class StimGroup:
    def __init__(self, win, stimuli):
        self.win = win;
        self.stimuli = stimuli;

    def draw(self):
        for stim in self.stimuli:
            stim.draw();

    def name(self):
        names = [];
        for stim in self.stimuli:
            names.append(stim.name);
        return names

def init(win):
    # Create the adjacency matrix
    n=7;p=0.35;
    adj_matrix = generate_erdos_renyi(n,p);

    prob = 0.5; #proportion of yellow and bleu (probabilistic)
    private_signal = np.random.choice([0,1],p=[prob,1-prob],size=n);

    #Draw the circles
    cir = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='blue',lineColor='black',pos= (-0.2*win.size[0],0),name=0);
    cle = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='yellow',lineColor='black',pos= (0.2*win.size[0],0),name=1);
    circle = StimGroup(win,[cir,cle]);
    
    ric = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='yellow', lineColor='black',pos= (-0.2*win.size[0],0),name=1);
    elc = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='blue', lineColor='black',pos= (0.2*win.size[0],0),name=0);
    invcircle = StimGroup(win,[ric,elc]);
    
    objects = {'circle':circle,'invcircle':invcircle};
    
    return adj_matrix, private_signal, objects

def square_the_node(ax, pos, node_index, x_range, y_range, size=0.1):
    x, y = pos[node_index];
    square = Rectangle((x - size*x_range / 2, y - size*y_range / 2), size*x_range, size*y_range, linewidth=5, edgecolor='green', facecolor='none');
    ax.add_patch(square);

#def generate_network(adj_mat, node_index, uncover = [0], private_signal = [0, 0, 1, 0, 1, 0, 1],colours=['#cab79a','blue','yellow'],seed_value = 28,outputname="current_network.png",screen_height= 800):
def generate_network(adj_mat, node_index, uncover = [0], private_signal = [0, 0, 1, 0, 1, 0, 1],colours=['#cab79a','blue','yellow'],seed_value = 28,outputname="current_network.png"):
    '''Create a .png containing the appropriate graph'''
    if uncover == 'clear':
        uncover = [0,1,2,3,4,5,6];

    G = nx.from_numpy_array(adj_mat);

    #Create white network
    node_colors = [colours[0]]*len(private_signal);
    node_edge_colors = ['red'] + ['black']*(len(private_signal)-1);


    #Apply colors on uncover part
    for i in range(len(node_colors)):
        if i in uncover:
            node_colors[i] = colours[private_signal[i]+1];

    pos = nx.spring_layout(G, k=1.25, seed=seed_value);
    
    
    #Create the figure
    #px = 1/plt.rcParams['figure.dpi']
    #print("px", px)
    #fig, ax = plt.subplots(figsize=(screen_height*px, screen_height*px));
    fig, ax = plt.subplots(figsize=(8,8));
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
    plt.savefig(outputname, transparent=True)  # Save with transparent background  #, dpi= 1/px
    plt.close()

    return pos


def display_private_info(win,signal, colours=['#cab79a','blue','yellow'], radius = 0.04):
    frame = visual.Rect(win, width=3*radius*win.size[1], height=3*radius*win.size[1],lineColor='black',lineWidth=0.005*win.size[1],pos=(-0.4*win.size[0],0.4*win.size[1]));
    first_info = visual.Circle(win, radius = radius*win.size[1],lineWidth=0.01*win.size[1],color=colours[signal+1], lineColor='red',pos= (-0.4*win.size[0],0.4*win.size[1]));

    obj = StimGroup(win,[first_info,frame]);

    return obj

def start_screen(win):
    """
    Display the start panel
    """

    text = visual.TextStim(win, text="Welcome to this experiment!", color='#f5f5f5', height=0.1*win.size[1], pos=(0, 0.20*win.size[1]),wrapWidth=win.size[0]*0.8)
    text2 = visual.TextStim(win, text="Press 'space' if you are ready to start.", color='#f5f5f5', height=0.05*win.size[1], pos=(0, -0.2*win.size[1]),wrapWidth=win.size[0]*0.8)

    text.draw()
    text2.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])

    return keys


def finish_screen(win):
    """
    Display the end panel
    """
    bg = visual.ImageStim(win=win,image="IMG/Fireworks.jpg",size = win.size,pos=(0,0));
    bg.draw();

    text = visual.TextStim(win, text="Thank you for participating!", color='white', height=0.12*win.size[1], pos=(0, -0.05*win.size[1]),wrapWidth=win.size[0]*0.95)
    text2 = visual.TextStim(win, text="Press any key to exit", color='white',height=0.08*win.size[1], pos=(0, -0.3*win.size[1]),wrapWidth=win.size[0]*0.8)
    text.draw()
    text2.draw()
    
    

    win.flip()
    
    event.waitKeys()
    return 0


def softmax_of_prob(p,T=1):
    p_adjusted = np.exp(p/T)/np.exp(1/T)
    return p_adjusted

def bot_behavior(adj_matrix, private_signal, discovery_mat, model='DeGroot'):
  private_signal = np.array(private_signal);
  new_private_signal = private_signal.copy();

  for i in range(discovery_mat.shape[0]):
    ## Node selection
    links = np.where(adj_matrix[i+1, :]==1)[0];
    discovered = np.where(discovery_mat[i,:]==0)[0];

    options = [value for value in discovered if value in links];
    if len(options)>0:
      discovery_mat[i,np.random.choice(options)]=1;

    ## Update belief
    neighbours_belief = private_signal[discovery_mat[i,:]==1];
    rn = np.random.uniform(size=1);
    if model =='DeGroot':
      g = sum(neighbours_belief)/len(neighbours_belief);
      if rn<softmax_of_prob(g):
        new_private_signal[i+1]=1;
      else:
        new_private_signal[i+1]=0      

    elif model =='RL':
      print("Need to code it")

    return private_signal, discovery_mat


def waiting_phase(win, mean=0.7, hourglass_path= 'IMG/hourglass.png'):
    time=np.random.poisson(mean*100, 1)/100;
    if time[0] > 1:
        hourglass = visual.ImageStim(win=win,image=hourglass_path, size=(0.3*win.size[1],0.3*win.size[1]) ,pos=(0,0));
        hourglass.draw();
        win.flip();
    core.wait(time[0]);


def generate_erdos_renyi(n, p):
    '''Normal erdos renye function with only one specificity the player 0 needs to have at least 3 links'''
    adj_matrix = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):  # But myself
            if np.random.rand() < p:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1  # Symetry
            if i==0:
                while sum(adj_matrix[i,:])<3:
                    available_links = np.where(adj_matrix[i,:]==0)[0];
                    available_links = available_links [available_links !=0];
                    adj_matrix[i,np.random.choice(available_links)]=1;

    return adj_matrix
    







def init_old(win):
    # Create the adjacency matrix
    adj_matrix = np.array([[0, 1, 1, 0, 0, 1, 1],
                           [1, 0, 1, 0, 0, 0, 0],
                           [1, 1, 0, 1, 0, 0, 1],
                           [0, 0, 1, 0, 1, 0, 1],
                           [0, 0, 0, 1, 0, 1, 1],
                           [1, 0, 0, 0, 1, 0, 1],
                           [1, 0, 1, 1, 1, 1, 0]]);

    private_signal = [0, 0, 1, 0, 1, 0, 1]

    #Draw the circles
    cir = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='blue',lineColor='black',pos= (-0.2*win.size[0],0),name=0);
    cle = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='yellow',lineColor='black',pos= (0.2*win.size[0],0),name=1);
    circle = StimGroup(win,[cir,cle]);
    
    ric = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='yellow', lineColor='black',pos= (-0.2*win.size[0],0),name=1);
    elc = visual.Circle(win, radius = 0.07*win.size[1],lineWidth=0.01*win.size[1],color='blue', lineColor='black',pos= (0.2*win.size[0],0),name=0);
    invcircle = StimGroup(win,[ric,elc]);
    
    objects = {'circle':circle,'invcircle':invcircle};
    
    return adj_matrix, private_signal, objects
