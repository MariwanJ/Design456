'''tools for shoe editor'''

from say import *


## toggle all position constraints of a gui selected shoe rib
#
#Rippe auswaehlen
#Menu Shoe -> toggle constraints of a rib  (oder symbol blaue sohle)
#
#Alle Positionsconstraints sind blau
#
#bei Wiederholung werden alle wieder rot
#


def toggleShoeSketch():
    '''toggle all position constraints of a gui selected shoe rib'''
    if len( Gui.Selection.getSelection())!=0:
        sk=Gui.Selection.getSelection()[0]
    print ("toggle sketch constraints for " + sk.Label
    for i,c in enumerate(sk.Constraints):
        if c.Name.startswith('p') or c.Name.startswith('tang') or c.Name.startswith('Width'):
            print c.Name
            try:
                sk.toggleDriving(i)
        #        sk.setDriving(i,False)
            except: pass


