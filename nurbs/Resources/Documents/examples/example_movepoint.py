import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import random






def test5():

    uc=8
    vc=8

    a=nurbs.makeNurbs(uc,vc)
    a.grid=False
    a.degree_u=2
    a.degree_v=2


    # punkte holen
    ps=a.Proxy.getPoints()

    # daten in gitter
    a.Proxy.togrid(ps)


    a.Proxy.addVline(3)
    a.Proxy.elevateVline(3,100)

    a.Proxy.addUline(3)
    a.Proxy.elevateUline(3,100)


    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


    if 10:
        a.Proxy.addVline(3,0.7)
        a.Proxy.addVline(3,0.2)

        a.Proxy.addS(4)
        a.Proxy.addVline(2,1)
        a.Proxy.elevateVline(2,0)

        a.Proxy.addVline(8,0)
        a.Proxy.elevateVline(8,0)

    if 10:
        a.Proxy.movePoint(1,1,0,0,40)
        a.Proxy.movePoint(2,4,0,0,60)
        a.Proxy.movePoint(2,5,0,0,60)


test5()

