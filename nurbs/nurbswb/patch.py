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
'''
#-------------------------------------------------
#-- methods for drawing on faces 
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''

# \cond
from nurbswb.say import *

import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui
import Part
import Mesh
import Draft
import Points

import numpy as np
import random


def machkurve(pss):
    ps = [App.Vector(p) for p in pss]
    bc = Part.BSplineCurve()
    bc.buildFromPoles(ps)
    res = App.ActiveDocument.addObject("Part::Spline", "kurve")
    res.Shape = bc.toShape()

    return bc


def normalizek(bc):

    bx = Part.BSplineCurve()

    poles = bc.getPoles()
    mults = bc.getMultiplicities()

    knots = bc.getKnots()
    knots = np.array(knots)
    knots *= 3
    knots -= knots.min()
    knots /= knots.max()

    bx.buildFromPolesMultsKnots(poles, mults, knots)
    return bx


def createSubEdge(ed, p1, p2):
    v1 = p1.Point
    v2 = p2.Point
    k1 = ed.Curve
    rc = createSubcurve(k1, v1, v2)
    return rc


def createSubcurve(k1, v1, v2):
    k1c = k1.copy()
    kka = k1.parameter(v1)
    kkb = k1.parameter(v2)

    k1c.insertKnot(kka, 2, 0)
    k1c.insertKnot(kkb, 2, 0)

    if kka > kkb:
        kka, kkb = kkb, kka

    k1c.segment(kka, kkb)
    k1cn = normalizek(k1c)

    b3 = App.ActiveDocument.addObject("Part::Spline", "subedge")
    b3.ViewObject.LineColor = (10.0, 0.0, 1.0)
    b3.ViewObject.LineWidth = 4
    b3.Shape = k1cn.toShape()

    return k1cn


def machFlaeche(psta, ku=None, objName="XXd"):
    NbVPoles, NbUPoles, _t1 = psta.shape

    degree = 3

    ps = [[App.Vector(psta[v, u, 0], psta[v, u, 1], psta[v, u, 2])
           for u in range(NbUPoles)] for v in range(NbVPoles)]

    kv = [1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
    if ku == None:
        ku = [1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]
    mv = [4] + [1]*(NbVPoles-4) + [4]
    mu = [4]+[1]*(NbUPoles-4)+[4]

    bs = Part.BSplineSurface()
    bs.buildFromPolesMultsKnots(
        ps, mv, mu, kv, ku, False, False, degree, degree)

    res = App.ActiveDocument.getObject(objName)

    # if res==None:
    res = App.ActiveDocument.addObject("Part::Spline", objName)
    # res.ViewObject.ControlPoints=True

    res.Shape = bs.toShape()

    return bs


def run():

    # edge and 2 points
    # ed=App.ActiveDocument.Sketch.Shape.Edge1
    # p1=App.ActiveDocument.Point.Shape.Vertex1
    # p2=App.ActiveDocument.Point002.Shape.Vertex1

    # eda=App.ActiveDocument.Sketch001.Shape.Edge1
    # p1a=App.ActiveDocument.Point001.Shape.Vertex1
    # p2a=App.ActiveDocument.Point003.Shape.Vertex1

    s = FreeCADGui.Selection.getSelectionEx()

    if len(s) == 6:
        ed = s[0].SubObjects[0]
        p1 = s[1].SubObjects[0]
        p2 = s[2].SubObjects[0]

        eda = s[3].SubObjects[0]
        p1a = s[4].SubObjects[0]
        p2a = s[5].SubObjects[0]
    else:
        ed = s[0].SubObjects[0]
        eda = s[1].SubObjects[0]
        p1 = ed.Vertex1
        p2 = ed.Vertex2
        p1a = eda.Vertex1
        p2a = eda.Vertex2

    # erzeuge zwei normalisierte subkurven
    c = createSubEdge(ed, p1, p2)
    ca = createSubEdge(eda, p1a, p2a)

    kns = c.getKnots()
    knsa = ca.getKnots()

    for k in kns+knsa:
        if k not in kns:
            c.insertKnot(k, 1, 0)
        if k not in knsa:
            ca.insertKnot(k, 1, 0)

    kns = c.getKnots()
    knsa = ca.getKnots()

    pl2 = c.getPoles()
    pl3 = ca.getPoles()

    pl3.reverse()

    # tangent constraint
    pl1x = [p+App.Vector(10, 0, -10) for p in pl2]
    pl1xa = [p+App.Vector(20, 0, -20) for p in pl2]
    pl1xb = [p+App.Vector(30, 0, -30) for p in pl2]

    # bergruecken
    pl3x = []
    for i in range(len(pl2)):
        pl3x += [pl2[i]*0.7+pl3[i]*0.3+App.Vector(0, 0, 500*random.random())]

    pl2x = []
    for i in range(len(pl2)):
        pl2x += [pl2[i]*0.2+pl3[i]*0.8+App.Vector(0, 0, 500*random.random())]

    # tangent constraint
    pl3xa = [p+App.Vector(-10, 0, 0) for p in pl3]
    pl3xb = [p+App.Vector(-20, 0, 0) for p in pl3]
    pl3xc = [p+App.Vector(-30, 0, 0) for p in pl3]

    psta = np.array([pl2, pl1x, pl1xa, pl1xb, pl3x,
                     pl2x, pl3xc, pl3xb, pl3xa, pl3])
    bs = machFlaeche(psta, kns, "mountains")


def runB():
    ''' testcase for a expression baes mountain profile '''

    import numpy as np
    print("WARNING:this is a testcase only")
    # hard coded test data
    kl = App.ActiveDocument.subedge
    kr = App.ActiveDocument.subedge001

    kali = kl.Shape.Edge1.Curve.getPoles()
    kare = kr.Shape.Edge1.Curve.getPoles()

    lena = len(kali)

    l0 = (kali[0]-kare[0]).Length

    scales = [(kali[i]-kare[i]).Length/l0 for i in range(lena)]

    rots = [0.0] + [
        (kali[i]-kare[i]).normalize().cross((kali[0] -
                                             kare[0]).normalize()).dot(App.Vector(0, 0, 1))
        for i in range(1, lena)
    ]
    rots = np.arcsin(rots)

    apts = []
    for i in range(lena):
        yy = (kare[0]-kali[0])*scales[i]

        polyp = [
            App.Vector(),
            App.Vector(0, 0, 115),
            App.Vector(0, 0, 130),

            ((kare[0]-kali[0])*0.3+App.Vector(0, 0, 200))*scales[i],
            ((kare[0]-kali[0])*0.3+App.Vector(0, 0, 200)) *
            scales[i]+App.Vector(40, 0, 0),
            ((kare[0]-kali[0])*0.3+App.Vector(0, 0, 200)) *
            scales[i]+App.Vector(80, 0, 0),

            yy+App.Vector(0, 0, 50),
            yy+App.Vector(0, 0, 25),
            yy+App.Vector(),
        ]

        pol = Part.makePolygon(polyp)

        if 1:  # display the control points polygons
            res = App.ActiveDocument.addObject(
                "Part::Spline", "aa"+str(i)+"__")
            res.Shape = pol
            res.Placement = App.Placement(kali[i], App.Rotation()).multiply(
                App.Placement(App.Vector(), App.Rotation(App.Vector(0, 0, 1), -180.0*rots[i]/np.pi)))

#        print kali[i]
#        print rots[i]
#        print scales[i]

        pts = [v.Point for v in res.Shape.Vertexes]
        apts += [pts]

    machFlaeche(np.array(apts))

    # display the controlpoint curves
    bpts = np.array(apts).swapaxes(0, 1)
    for l in bpts:
        machkurve(l)
