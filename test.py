from Generate_network import *

win = visual.Window(units='pix', fullscr=True, color='#c6a36d');
adj_matrix, private_signal, objects = init(win);

print(objects['invcircle'].name())


win.close();
core.quit();

