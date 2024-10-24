from psychopy import visual, core, event

win = visual.Window(units='pix', fullscr=True, color='black');

text = visual.TextStim(win, text="Welcome to this experiment!", color='#f5f5f5', height=0.1*win.size[1], pos=(0, 0.20*win.size[1]),wrapWidth=win.size[0]*0.8);
text.draw();
win.flip();
while True:
    keys = event.waitKeys();
    if 'escape' in keys:
        break
    else:
        input = visual.TextStim(win, text=str(keys), color='#f5f5f5', height=0.08*win.size[1], pos=(0, -0.10*win.size[1]),wrapWidth=win.size[0]*0.8);
        input.draw();
    text.draw();
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

