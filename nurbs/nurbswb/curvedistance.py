# distance between the target curve 1st, and some other curves

import FreeCADGui as Gui
import numpy as np
import Draft

def  dist(a,b):

    [a,b]=[b,a]
    ptas=a.Shape.Edge1.Curve.discretize(100)
    cb=b.Shape.Edge1.Curve

    pts=[]
    ls=[]
    for pa in ptas:
        pm=cb.parameter(pa)
        v=cb.value(pm)
        ls.append((v-pa).Length**2)
        pts.append(v)

#    Draft.makeWire(pts)
#    Draft.makeWire(ptas)

    ls=np.array(ls)
#    print ls
    ls.min()
    ls.max()
#    print (ls.max(),ls.min(),ls.mean())
    return ls.mean()



def run():
    sel=Gui.Selection.getSelection()
    b=sel[0]
    for a in sel[1:]:
        print (str(a.Label),round(dist(a,b),3))
