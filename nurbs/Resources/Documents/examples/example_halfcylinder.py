nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random


def test3():

    a= nurbs.makeNurbs(5,9)
    a.model="NurbsCylinder"
    a.solid=False
    a.base=False
    # a.grid=False
    ps=a.Proxy.getPoints()
    a.Proxy.togrid(ps)
    
    
    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    App.ActiveDocument.recompute()
    Gui.updateGui()

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


test3()
