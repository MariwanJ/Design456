import nurbswb.nurbs
import numpy as np
import random


def testRandomB():
    ''' create a random testnurbs'''


    na=20
    b=10

    a=nurbswb.nurbs.makeNurbs(b,na)

    a.solid=False
    a.base=False
    a.grid=False

    a.gridCount=80

    ps=a.Proxy.getPoints()

    ps=np.array(ps)
    ps.resize(na,b,3)
    
    for k0 in range(10):
        k=random.randint(0,na-6)
        l=random.randint(1,b-1)
        for j in range(3):
            ps[k+j][l][2] += 60
        rj=random.randint(0,2)
        print (k,rj)
        for j in range(rj):
            ps[k+3+j][l][2] += 60

    for k0 in range(10):
        k=random.randint(0,na-5)
        l=random.randint(1,b-1)

        for j in range(2):
            ps[k+j][l][2] += 30
        rj=random.randint(0,2)
        print (k,rj)
        for j in range(rj):
            ps[k+2+j][l][2] += 30

    ps.resize(na*b,3)

    a.Proxy.togrid(ps)
    a.Proxy.elevateUline(17,120)

    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")

testRandomB()
