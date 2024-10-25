from Generate_network import *

win = visual.Window(units='pix', fullscr=True, color='#c6a36d');

nsize =.8;
#Initialisation
adj_matrix = init();
uncover = [0];
square = [];
square_pos = 0;


generate_network(adj_matrix, square, uncover);
network = visual.ImageStim(win=win,image=f"current_network.png", size=None, pos=(0,0)); #Controling the size diminish the quality size=(nsize*win.size[1],nsize*win.size[1])
network.draw();
win.flip();

while True:
    keys = event.waitKeys(keyList=['left', 'right', 'return', 'escape']);
    if 'escape' in keys:
        break
    elif 'left' in keys:
        square_pos+=1;
        square_pos = square_pos%adj_matrix.shape[0];
    elif 'right' in keys:
        square_pos-=1;
        square_pos = square_pos%adj_matrix.shape[0];
    elif 'return' in keys:
        uncover.append(square_pos);
        print(uncover);
    
    square = [square_pos];
    generate_network(adj_matrix, square, uncover);
    network = visual.ImageStim(win=win,image=f"current_network.png", size=None ,pos=(0,0)); #Controling the size diminish the quality size=(nsize*win.size[1],nsize*win.size[1])
    network.draw();
    win.flip();
    

    
    '''
    Presentation réseau blanc: 
    Deux carrés blanc sur deux voisins
    input le carré de l'input devient vert
    la case correspondant au carré devient alors de sa couleurs
    nouveau round avec le même network    
    '''



win.close();
core.quit();

