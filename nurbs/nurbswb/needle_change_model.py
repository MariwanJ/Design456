import FreeCAD 
import FreeCADGui

import numpy as np


def srun(w):
    print (w.m.currentIndex())
    a=w.target
    model='modelS'
    import nurbswb.needle_models
    reload(nurbswb.needle_models)
    lm=nurbswb.needle_models.listModels(silent=True)
    print (lm[w.m.currentIndex()])
    model=lm[w.m.currentIndex()][0]

    print ("a.Proxy.getExampleModel(nurbswb.needle_models."+ model+")")
    eval("a.Proxy.getExampleModel(nurbswb.needle_models."+ model+")")
    w.hide()

from PySide import QtGui, QtCore

def MyDialog(target):

    import nurbswb.needle_models
    reload(nurbswb.needle_models)
    lm=nurbswb.needle_models.listModels()

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
    [target]=FreeCADGui.Selection.getSelection()
    MyDialog(target)


# run()



