import nurbs
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random




def test2():

    uc=8
    vc=8

    a=nurbs.makeNurbs(uc,vc)
    a.degree_u=1

    a.degree_u=2

    a.degree_v=a.degree_u

    # punkte holen
    ps=a.Proxy.getPoints()

    # daten in gitter
    a.Proxy.togrid(ps)

    a.Proxy.addVline(3,0.9)
    a.Proxy.addVline(3,0.1)

    a.Proxy.addS(4)
    a.Proxy.elevateVline(4,30)


    a.Proxy.addVline(10,0.9)
    a.Proxy.addVline(10,0.1)

    a.Proxy.addS(11)
    a.Proxy.elevateVline(11,30)
    
    a.Proxy.addVline(10,0)
    a.Proxy.elevateVline(10,0)
    a.Proxy.addVline(14,0)


test2()

