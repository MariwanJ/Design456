# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- # kurven abwickeln
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtCore
from pivy import coin
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')

import Part,Draft


def unroll(mode):


    edge=Gui.Selection.getSelection()[0]
    face=Gui.Selection.getSelection()[1]


    # referenzflaeche
    # sf=App.ActiveDocument.Poles.Shape.Face1.Surface
    sf=face.Shape.Face1.Surface


    # pfad
    #e=App.ActiveDocument.map3D_for_Sketch001_on_Poles_by_MAP002_Spline.Shape.Edge1
    #e=App.ActiveDocument.map3D_for_map2D_for_Drawing_on_Poles__Face1_on_Poles_by_MAP_Spline.Shape.Edge1

    # wenn nicht bereits spline
    # fall eoinfacher wire
    # w=App.ActiveDocument.Drawing_on_Poles__Face1.Shape
    w=edge.Shape
    wpts=w.discretize(30)
    bb=Draft.makeBSpline(wpts)
    e=bb.Shape.Edge1



    c=e.Curve

    import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')

    lenp=100
    
    el=e.Length/lenp

    pts=c.discretize(lenp)

    for p in pts:
        t=c.parameter(p)
        print(c.tangent(t))
        (u,v)=sf.parameter(p)
        print (sf.normal(u,v))


    tgs=[c.tangent(c.parameter(p))[0] for p in pts]
    nos=[]
    for p in pts:
        (u,v)=sf.parameter(p)
        nos += [sf.normal(u,v)]




    if mode=='yaw':
        pp=c.value(0)
        print ( "Startpunkt",pp)
        #bp=nos[0]
        #bp=App.Vector(0,1,0)

    else:
        pp=App.Vector()
        bp=App.Vector(0,1,0)

    tp=App.Vector(1,0,0)
#    tp=App.Vector(1,0,0.3).normalize()
    tp=c.tangent(0)[0]
    print ("-------------------")
    print ("Startpunk",pp)
    print ("Tangente",tp)

    if 1:
        pp=App.Vector()
        tp=App.Vector(1,0,0)
        bp=App.Vector(0,1,0)



    # bp=App.Vector(0,1,0)
    ptsn=[pp]

    for i in range(lenp-1):

        
        a=tgs[i+1]-tgs[i]
        if mode=='yaw':
            w=a.dot(nos[i].cross(tgs[i]))
            npa=App.Vector(0,0,1).cross(tp)
        else:
            w=a.dot(nos[i])
            npa=App.Vector(0,0,1)
            npa=tp.cross(bp)
        print (i,w)
        tpn=tp*np.cos(np.arcsin(w)) + npa*np.sin(np.arcsin(w))
        a=tpn.normalize()

        a *= el
        ppn=pp+ a 
        ptsn +=  [ppn]
        bp=tp.cross(tpn).normalize()
        tp=tpn.normalize()

        pp=ppn

    #Draft.makeWire(pts[:-2])
    #ptsn2=[p+App.Vector(0,0,10) for p in ptsn]
    #ptsn=ptsn2
    
    if 1:
        res=Draft.makeBSpline(ptsn)
    else:
        res=App.activeDocument().addObject('Part::Feature','unroll')
        res.Shape=Part.makePolygon(ptsn)

    res.Label=mode + " for " + edge.Label + " on " + face.Label
    App.ActiveDocument.removeObject(bb.Name)







def unroll_yaw():
        unroll(mode='yaw')


def unroll_pitch():
        unroll(mode='pitch')



import Draft


def combineCT():

    objc=Gui.Selection.getSelection()[0]
    objt=Gui.Selection.getSelection()[1]


    #ec=App.ActiveDocument.BSpline001.Shape.Edge1
    ec=objc.Shape.Edge1
    kc=ec.Curve

 
    #et=App.ActiveDocument.BSpline002.Shape.Edge1
    et=objt.Shape.Edge1
    kt=et.Curve

    p=App.Vector()
    start=App.Vector()
    start=kc.value(0)
    print ("start",start)
    
    
    
    

    t=App.Vector(1,0,0)
    t=App.Vector(1,0,0.8).normalize()
    
    t=kc.tangent(0)[0]

    #-------------------
    start=App.Vector (1000.0000000000025, -6.585502339306361e-13, -5.684341886080802e-14)
    t=App.Vector (0.12085567006180127, 0.9814887436862094, -0.14857238313757795)
#    t=App.Vector ( 0.9814887436862094, 0.12085567006180127,0.14857238313757795)
    
    #-------------------



    if 0:
        p=App.Vector()
        start=App.Vector()
        t=App.Vector(1,0,0)

    nn=App.Vector(0,0,1)
    b=t.cross(nn)
    print (nn)

    if 0:
        a=App.ActiveDocument.Drawing_on_Face__Face1_Spline.Shape.Edge1.Curve
        # p0=a.value(0)
        t=a.tangent(0)[0]
        nn=a.normal(0)
        b=t.cross(nn)
        start=a.value(0)

    ptt=App.Placement(t,App.Rotation())
    ptn=App.Placement(nn,App.Rotation())

    tpts=[p]

    n=200
    ptsc=kc.discretize(n)

    for i in range(0,n):
        r=App.Rotation(kc.tangent(ec.FirstParameter+1.0*i/n*(ec.LastParameter-ec.FirstParameter))[0],
        kc.tangent(ec.FirstParameter+1.0*(i-1)/n*(ec.LastParameter-ec.FirstParameter))[0])

        if r.Axis.y>0:
            rc=r.Angle
        else:
            rc=-r.Angle
        rc=r.Angle

        r2=App.Rotation(kt.tangent(et.FirstParameter+1.0*i/n*(et.LastParameter-et.FirstParameter))[0],
        kt.tangent(et.FirstParameter+1.0*(i-1)/n*(et.LastParameter-et.FirstParameter))[0])

        if r2.Axis.z>0:
            rt=r2.Angle
        else:
            rt=-r2.Angle
        #rt=r2.Angle

#        rt *= 1.3

#        rt *= 0.4
#        rt *= 0.1

    #    r3=App.Rotation(App.Vector(0,0,1),rc)

        rX=App.Rotation(b,rc*180/np.pi)
    #    rX=App.Rotation(b,0)
        rY=App.Rotation(nn,rt*180/np.pi)

        #print (rc,rt)

        pc=App.Placement(App.Vector(),rX)
        pt=App.Placement(App.Vector(),rY)
    #    pc=App.Placement()


        t9=pt.multiply(pc).multiply(ptt)
        t9=pc.multiply(pt).multiply(ptt)
        #t9=ptt.multiply(pc).multiply(pt)
        ptt=t9
        t=t9.Base
        #ptn=App.Placement(nn,App.Rotation())
        
        t8=pc.multiply(ptn)
        nn=t8.Base.normalize()
        ptn=t8
        
        b=t.cross(nn).normalize()
        p=p+t
    #    print ("t ",t
        print ("n ",nn)
    #    print ("b ",b
    #    print 
        tpts += [p]

    tpts2=[p*(1*ec.Length/n ) +start  for p in tpts]

    Draft.makeWire(tpts2)




if __name__ =='__main__':
    unroll_yaw()
    unroll_pitch()
