import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random

def testRandomTorus():


    na=7
    b=4


    a=nurbs.makeNurbs(b,na)
    a.model="NurbsTorus"

    a.solid=False
    a.base=False
    #a.grid=False
    a.gridCount=20
    
    ps=a.Proxy.getPoints()
    print ("points ps",len(ps))

    ps=a.Proxy.getPoints()
    print ("A")
    a.Proxy.togrid(ps)
    print ("B")
    a.Proxy.updatePoles()
    print ("C")
    a.Proxy.showGriduv()

    '''
    if 0:
        print ("random ..")
        ps=np.array(App.ps).swapaxes(0,1)
        temp,ct=ps.shape
        ps[2] += 100*np.random.random(ct)
        ps=ps.swapaxes(0,1)
    #    ps[0:3]
    
    ps=np.array(ps)
    ps.resize(na,b,3)

    
    for k0 in range(15):
        k=random.randint(2,na-3)
        l=random.randint(1,b-1)
        for j in range(1):
            ps[k+j][l][2] += 100*random.random()
        rj=random.randint(0,1)
        print (k,rj)
        for j in range(rj):
            ps[k+j][l][2] += 100*random.random()

    for k0 in range(10):
        k=random.randint(2,na-3)
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

    '''


    App.a=a
    App.ps=ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")



testRandomTorus()
