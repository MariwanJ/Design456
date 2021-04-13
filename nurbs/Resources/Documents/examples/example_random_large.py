import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import random




def testRandomA():


    na=200
    b=100

    a=nurbs.makeNurbs(b,na)

    a.solid=False
    a.base=False
    #a.grid=False
    a.gridCount=80
    
    ps=a.Proxy.getPoints()

    if 0:
        print ("random ..")
        ps=np.array(App.ps).swapaxes(0,1)
        temp,ct=ps.shape
        ps[2] += 100*np.random.random(ct)
        ps=ps.swapaxes(0,1)
    #    ps[0:3]

    ps=np.array(ps)
    ps.resize(na,b,3)
    
    for k0 in range(350):
        k=random.randint(0,na-30)
        l=random.randint(1,b-1)
        for j in range(20):
            ps[k+j][l][2] += 60
        rj=random.randint(0,10)
        print (k,rj)
        for j in range(rj):
            ps[k+20+j][l][2] += 60

    for k0 in range(650):
        k=random.randint(0,na-12)
        l=random.randint(1,b-1)

        for j in range(7):
            ps[k+j][l][2] += 30
        rj=random.randint(0,3)
        print (k,rj)
        for j in range(rj):
            ps[k+7+j][l][2] += 30


    ps.resize(na*b,3)


    a.Proxy.togrid(ps)
    a.Proxy.elevateVline(2,0)

    a.Proxy.updatePoles()
    a.Proxy.showGriduv()
    
    App.a=a
    App.ps=ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


testRandomA()
