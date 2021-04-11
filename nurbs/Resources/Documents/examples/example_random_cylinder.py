import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import random


def testRandomCylinder():

    try:
        App.closeDocument("Unnamed")
    except:
        pass

    if App.ActiveDocument==None:
        App.newDocument("Unnamed")
        App.setActiveDocument("Unnamed")
        App.ActiveDocument=App.getDocument("Unnamed")
        Gui.ActiveDocument=Gui.getDocument("Unnamed")

    na=7
    b=5

    a=nurbs.makeNurbs(b,na)
    a.model="NurbsCylinder"

    a.solid=False
    a.base=False
    #a.grid=False
    a.gridCount=20
    
    ps=a.Proxy.getPoints()
    print ("points ps",len(ps))

    if 0:
        print ("random ..")
        ps=np.array(App.ps).swapaxes(0,1)
        temp,ct=ps.shape
        ps[2] += 100*np.random.random(ct)
        ps=ps.swapaxes(0,1)
    #    ps[0:3]

    ps=np.array(ps)
    ps.resize(na,b,3)
    
    for k0 in range(25):
        k=random.randint(0,na-3)
        l=random.randint(1,b-1)
        for j in range(1):
            ps[k+j][l][2] += 100*random.random()
        rj=random.randint(0,1)
        print (k,rj)
        for j in range(rj):
            ps[k+j][l][2] += 100*random.random()

    for k0 in range(10):
        k=random.randint(0,na-3)
        l=random.randint(1,b-1)

        for j in range(1):
            ps[k+j][l][2] += 200*random.random()
        rj=random.randint(0,1)
        print (k,rj)
        for j in range(rj):
            ps[k+j][l][2] += 200*random.random()


    ps.resize(na*b,3)


    a.Proxy.togrid(ps)
#    a.Proxy.elevateVline(2,0)

    a.Proxy.updatePoles()
    a.Proxy.showGriduv()
    
    App.a=a
    App.ps=ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


testRandomCylinder()
