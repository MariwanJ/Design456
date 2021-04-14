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



import os
import Design456Init
try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui
import Part
import Mesh
import Draft
import Points


def ThousandsOfRunWhatShouldIdo():

    try:
        [sourcex, targetx] = Gui.Selection.getSelectionEx()
        s = sourcex.SubObjects[0]
        f = targetx.SubObjects[0]

    except:
        [source, target] = Gui.Selection.getSelectionEx()

        s = source.Shape.Edge1
        f = target.Shape.Face1

    p = f.makeParallelProjection(s, App.Vector(0, 0, 1))
    Part.show(p)


def OLDrunAll():

    wires = []
    alls = Gui.Selection.getSelectionEx()
    target = alls[-1]
    for source in alls[:-1]:
        for s in source.Shape.Edges:

            f = target.Shape.Face1

            p = f.makeParallelProjection(s, App.Vector(0, 0, 1))
            wires += p.Wires[0].Edges
#                print p.Vertexes[0].Point
#                print p.Vertexes[1].Point
#                Part.show(p)

    Part.show(Part.Compound(wires))
    App.w = wires

    # ---------------------------------

    wsort = [wires[0]]
    for i, w in enumerate(wires):
        if i == 0:
            continue
        w2 = wsort[-1]
        print(min(
            (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length,
            (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length,
            (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length,
            (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length,
        ))
        if (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length < 0.1:
            wsort += [w]
        elif (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length < 0.1:
            wsort += [w]
        elif (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length < 0.1:
            print("gedreht")
            w.reverse()
            wsort += [w]
        elif (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length < 0.1:
            print("gedreht")
            w.reverse()
            wsort += [w]

        else:
            print("Fehler")
            raise Exception("Gehrte")

    w = Part.Wire(wsort)
    Part.show(w)

    # ----------------------------------

#        ww=Part.__sortEdges__(wires)
#        App.ww=ww
#        App.wires=wires
#        assert len(ww) == len(wires)

#        w=Part.Wire(ww)
#        Part.show(w)
    pts = w.discretize(200)
    Draft.makeBSpline(pts)


def runAll():

    pointgrps = []
    wires = []
    alls = Gui.Selection.getSelectionEx()
    target = alls[-1]
    for source in alls[:-1]:

        pgs = []
        for s in source.Shape.Edges:

            f = target.Shape.Face1

            p = f.makeParallelProjection(s, App.Vector(0, 0, 1))
            wires += p.Wires[0].Edges
#                print p.Vertexes[0].Point
#                print p.Vertexes[1].Point
# Part.show(p)
            print("Diskret")
            pgs += p.Wires[0].discretize(200)
#                Draft.makeWire(p.Wires[0].discretize(200))

        pointgrps += [pgs]

#        Part.show(Part.Compound(wires))
    App.w = wires
    App.pointgrps = pointgrps
    concatenateWires(pointgrps)
    return

    # ---------------------------------

    pointgrps = []

    wsort = [wires[0]]
    for i, w in enumerate(wires):
        if i == 0:
            continue
        w2 = wsort[-1]
        print(min(
            (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length,
            (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length,
            (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length,
            (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length,
        ))
        if (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length < 0.1:
            wsort += [w]
        elif (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length < 0.1:
            wsort += [w]
        elif (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length < 0.1:
            print("gedreht")
            w.reverse()
            wsort += [w]
        elif (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length < 0.1:
            print("gedreht")
            w.reverse()
            wsort += [w]

        else:
            print("Fehler")
            raise Exception("Gehrte")

        w = Part.Wire(wsort)
#            Part.show(w)

        # ----------------------------------

    #        ww=Part.__sortEdges__(wires)
    #        App.ww=ww
    #        App.wires=wires
    #        assert len(ww) == len(wires)

    #        w=Part.Wire(ww)
    #        Part.show(w)

        pts = w.discretize(200)
        pointgrps += [pts]

        Draft.makeBSpline(pts)

#        concatenateWires(pointgrps)


def concatenateBSplines():
    ''' Draft BSsplines  zusammenfuegen'''

    import Draft

    wires = []
    for s in Gui.Selection.getSelectionEx():
        wires += [s.Points]
        print(wires)
        print(s.Label)

    concatenateWires(wires)


def concatenateWires(wires):

    pts = wires[0]

#    print pts
#    print  wires[0][0]
#    print  wires[1][1]

    dista = min(
        (wires[0][0]-wires[1][0]).Length,
        (wires[0][0]-wires[1][-1]).Length,
        (wires[0][-1]-wires[1][0]).Length,
        (wires[0][-1]-wires[1][-1]).Length
    )

    if dista == (wires[0][0]-wires[1][0]).Length or dista == (wires[0][0]-wires[1][-1]).Length:
        print("Drehe Start")
        pts.reverse()

    wa = pts

    for w in wires[1:]:
        dista = min(
            (wa[-1]-w[0]).Length,
            (wa[-1]-w[-1]).Length,
        )
        wb = w
        if dista == (wa[-1]-w[-1]).Length:
            print("Drehe")
            wb.reverse()

        pts += wb
        wa = wb

    print(len(pts))

    pts2 = []
    for i, p in enumerate(pts):
        if (p-pts[i-1]).Length < 0.001:
            print("Doppel", i)
            print((p-pts[i-1]).Length)
        else:
            pts2 += [p]

    import Draft
    Draft.makeWire(pts2)
    Draft.makeBSpline(pts2)


def splitCurve():
    # split an recombine curve
    sw = Gui.Selection.getSelectionEx()[0]

    w = sw.Shape.Edges[0]
    # App.ActiveDocument.BSpline001.Shape

    step = 10
    anz = int(round(w.Curve.length()/step+1))
    pts = w.discretize(anz)

    pxy = [App.Vector(p.x, p.y, 0) for p in pts]

    for i in range(anz):
        print((pts[i]-pts[i-1]).Length)

    len = round(w.Curve.length()+1)/anz

    psz = [App.Vector(len*i, 0, p.z) for i, p in enumerate(pts)]
    psz = [App.Vector(0, len*i, p.z) for i, p in enumerate(pts)]

    # split
    wsz = Draft.makeWire(psz)
    wxy = Draft.makeWire(pxy)


def combineCurve():
    # recombine
    [wsz, wxy] = Gui.Selection.getSelectionEx()
    pts = [App.Vector(b.x, b.y, a.z) for a, b in zip(wsz.Points, wxy.Points)]
    aa = Draft.makeWire(pts)
    ptsb = aa.Shape.discretize(40)
    Draft.makeBSpline(ptsb)

    for i, p in enumerate(pts):
        if i == 0:
            ptsa = []
        else:
            t = p-pts[i-1]
            t.normalize()
            t *= 10
            n = App.Vector(0, 0, 1)
            h = t.cross(n).normalize() * 10

            ptsa += [p, p+h, pts[i-1]+h, pts[i-1]-h, p-h, p]

    Draft.makeWire(ptsa)
