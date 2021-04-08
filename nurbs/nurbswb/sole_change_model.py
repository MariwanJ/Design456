import FreeCAD as App
import FreeCADGui as Gui

import numpy as np


def srun(w):
    print (w.m.currentIndex())
    a=w.target
    model='modelS'
    import nurbswb.sole_models
    reload(nurbswb.sole_models)
    lm=nurbswb.sole_models.listModels(silent=True)
    print (lm[w.m.currentIndex()])
    model=lm[w.m.currentIndex()][0]

    reload(nurbswb.sole)
    cmd="nurbswb.sole.runA(model=nurbswb.sole_models." + model +"())"
    print (cmd)
    eval(cmd)
    # w.hide()

from PySide import QtGui, QtCore

def MyDialog(target=None):

    import nurbswb.sole_models
    reload(nurbswb.sole_models)
    lm=nurbswb.sole_models.listModels()

    w=QtGui.QWidget()
    w.target=target

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)



    l=QtGui.QLabel("Select the model" )
    box.addWidget(l)


    combo = QtGui.QComboBox()
    
    for item in lm:
        combo.addItem(str(item))
    

    w.m=combo
    combo.activated.connect(lambda:srun(w))  

    box.addWidget(combo)


    w.show()
    return w


def run():
    #[target]=FreeCADGui.Selection.getSelection()
    target=None
    return MyDialog(target)



if __name__=='__main__':
    run()



