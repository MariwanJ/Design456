import nurbswb.nurbs
import numpy as np
import random


def testA():

    a=nurbswb.nurbs.makeNurbs(4,4)

    a.solid=False
    a.base=False

    ps=a.Proxy.getPoints()
    a.Proxy.togrid(ps)


    a.Proxy.addVline(2,0.9)
    a.Proxy.addVline(3,0.1)
    a.Proxy.addVline(2,0.3)
    a.Proxy.addVline(2,0.9)

    for l in [2,3,4,5]:
        a.Proxy.elevateVline(l,100)

    a.Proxy.addUline(2,0.8)
    a.Proxy.addUline(3,0.5)
    a.Proxy.addUline(2,0.4)
    a.Proxy.addUline(2,0.5)

    for l in [2,3,4,5]:
        a.Proxy.elevateUline(l,100)


    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    App.activeDocument().recompute()
    Gui.updateGui()

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


testA()
