from Generate_network import *

#Constant
n_networks=5;
p=0.7;

win = visual.Window(units='pix', fullscr=True, color='#c6a36d');

#nsize =.8;


start_screen(win);
for n in range(n_networks):
    #Initialisation of the new network
    if n == 0:
        adj_matrix, private_signal, objects = init_old(win);
    else:
        adj_matrix, private_signal, objects = init(win);

    #print(adj_matrix);
    #print(private_signal);
    uncover = [0];
    square = [];

    private_info = display_private_info(win,private_signal[0]);
    discovery_mat = np.eye(len(private_signal))[1:len(private_signal),:]; #At first noone have see noone and we do not take the player case
    visited = [];
    for phase in range(3):
        ## Selection of frames
        neighbours = np.where(adj_matrix[0,:]==1)[0];
        neighbours[~np.isin(neighbours, visited)];
        
        if len(square)!=0:
            square = np.array(square);visited_arr = np.array(visited)
            square = square[~np.isin(square, visited_arr)]; #Only keep the one that has not been shown 
            if len(neighbours[~np.isin(neighbours, np.concatenate((square,visited_arr)))])>0:
                new_tile = np.random.choice(neighbours[~np.isin(neighbours, np.concatenate((square,visited_arr)))],size=1);
            else:
                new_tile=square;
            square = [square[0],new_tile[0]];
        else:
            square = np.random.choice(neighbours,size=2,replace=False);

        pos =   generate_network(adj_matrix, square, uncover, private_signal=private_signal);
        network = visual.ImageStim(win=win,image=f"current_network.png", size=None ,pos=(0,0)); #Controling the size diminish the quality size=(nsize*win.size[1],nsize*win.size[1])
        network.draw();
        private_info.draw();
        win.flip();

        ## Player choice
        keys = event.waitKeys(keyList=['left', 'right', 'escape']);
        if 'escape' in keys:
            break
        else:
            rn = np.random.uniform();
            #print(rn);
            x1 = pos[square[0]][0];
            x2 = pos[square[1]][0];
            if 'left' in keys:
                if x1<x2:
                    if rn<p:
                        selected = square[0];
                    else:
                        selected = square[1];
                else:
                    if rn<p:
                        selected = square[1];
                    else:
                        selected = square[0];
            elif 'right' in keys:
                if x1>x2:
                    selected = square[0];
                else:
                    selected = square[1];
        
        uncover.append(selected);
        visited.append(selected);
        

        pos =   generate_network(adj_matrix, [], uncover, private_signal=private_signal); #Without the squares
        network = visual.ImageStim(win=win,image=f"current_network.png", size=None ,pos=(0,0)); #Controling the size diminish the quality size=(nsize*win.size[1],nsize*win.size[1])
        network.draw();
        private_info.draw();
        win.flip();
        core.wait(1);
        uncover = [0];

        #Transition
        win.flip();
        core.wait(.2);
        
        ## Update belief
        circles = objects[np.random.choice(['circle','invcircle'])];
        circles.draw();
        win.flip();
        
        keys = event.waitKeys(keyList=['left', 'right', 'escape']);
        if 'escape' in keys:
            break
        elif 'left' in keys:
            private_signal[0] = circles.name()[0];
        elif 'right' in keys:
            private_signal[0] = circles.name()[1];

        #Transition
        win.flip();
        core.wait(.1);

        ##Bot turn
        private_signal, discovery_mat = bot_behavior(adj_matrix, private_signal, discovery_mat);
        waiting_phase(win); #Simulate realtime behavior 
        
        #Transition
        win.flip();
        core.wait(.2);


        print(f'Network: {n}, Phase {phase}, belief: {private_signal[0]}');

finish_screen(win);

win.close();
core.quit();

