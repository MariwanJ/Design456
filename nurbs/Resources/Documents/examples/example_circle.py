import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import random

def test4():
    # kreistest

    uc=6
    vc=5

    a=nurbs.makeNurbs(uc,vc)
    a.degree_u=1

    a.degree_u=2

    a.degree_v=a.degree_u

    # punkte holen
    ps=a.Proxy.getPoints()

    ps=[]
    for v in range(vc):
            for u in range(uc):
                h=0
                if 1<=u and u<=3 and 1<=v and v<=3:
                    h=100 
                if u==2 and v==2:
                    h=105
                ps.append(App.Vector(u*100,v*100,h))
    k=3.7


    a.weights=[
        1,1,1,1,1,1,
        1,1,k,1,1,1,
        1,k,1,k,1,1,
        1,1,k,1,1,1,
        1,1,1,1,1,1,
    ]


    # daten in gitter
    a.Proxy.togrid(ps)


    a.Proxy.updatePoles()
    a.Proxy.showGriduv()


test4()
