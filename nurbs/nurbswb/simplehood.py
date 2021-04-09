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
# -------------------------------------------------
# -- nurbs corner fillet -
# --
# -- microelly 2017
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------

import Part
import FreeCAD as App

import numpy as np
import random

# -------------------------


def getpols(obj):
    c1 = obj.Geometry[0]
    pl1 = obj.Placement

    po1a = []
    po1 = c1.getPoles()
    for p in po1:
        pm = App.Placement()
        pm.Base = p
        pn = pl1.multiply(pm)
        po1a.append(pn.Base)

    return po1a


def createShape(obj):

    mu = [4, 4]
    ku = [0, 1]
    mv = mu
    kv = ku

    # simple: 3 pole und ecke
    z = 100
    y = -100
    x = 100

    (x, y, z) = tuple(obj.Size)

    ps = [
        [[0, 0, z], [0, y, z], [0, y, z], [0, y, 0]],
        [[0, 0, z], [x, y, z], [x, y, z], [x, y, 0]],
        [[0, 0, z], [x, y, z], [x, y, z], [x, y, 0]],
        [[0, 0, z], [x, 0, z], [x, 0, z], [x, 0, 0]],
    ]

    color = (random.random(), random.random(), random.random())

    ps = np.array(ps)
    ps3 = ps.swapaxes(0, 1)

    # create the hood
    bs = Part.BSplineSurface()
    bs.buildFromPolesMultsKnots(ps, mv, mu, kv, ku, False, False, 3, 3)

    # ellipsoid  weights
    if 1:
        for u in [2, 3]:
            for v in [2, 3]:
                bs.setWeight(u, v, 0.121)

        bs.setWeight(1, 4, 1)
        bs.setWeight(4, 4, 1)

        bs.setWeight(2, 4, 0.24)
        bs.setWeight(3, 4, 0.24)

        bs.setWeight(1, 2, 0.24)
        bs.setWeight(1, 3, 0.24)

        bs.setWeight(4, 2, 0.24)
        bs.setWeight(4, 3, 0.24)

    if 0:
        for u in [2, 3]:
            for v in [2, 3]:
                bs.setWeight(u, v, 0.121)

        bs.setWeight(1, 4, 1)
        bs.setWeight(4, 4, 1)

        bs.setWeight(2, 4, 0.24)
        bs.setWeight(3, 4, 0.24)

        bs.setWeight(1, 2, 0.24)
        bs.setWeight(1, 3, 0.24)

    # hyperbolic  weights
    if obj.zProfile == "hyperbola":
        bs.setWeight(2, 4, 0.2)
        bs.setWeight(3, 4, 0.003)
    if obj.zProfile == "parabola":
        bs.setWeight(2, 4, 0.02)
        bs.setWeight(3, 4, 0.15)

    if obj.xProfile == "parabola":
        # parabolic weights
        bs.setWeight(1, 2, 0.02)
        bs.setWeight(1, 3, 0.15)
    if obj.xProfile == "hyperbola":
        bs.setWeight(1, 3, 0.2)
        bs.setWeight(1, 2, 0.003)

    if obj.yProfile == "parabola":
        # parabolic weights
        bs.setWeight(4, 2, 0.02)
        bs.setWeight(4, 3, 0.15)
    if obj.yProfile == "hyperbola":
        bs.setWeight(4, 3, 0.2)
        bs.setWeight(4, 2, 0.003)

    sh = bs.toShape()

    try:
        sp = App.ActiveDocument.helper
    except:
        sp = App.ActiveDocument.addObject("Part::Spline", "helper")
        App.ActiveDocument.ActiveObject.ViewObject.hide()

    sp.Shape = sh
    sp.ViewObject.ControlPoints = True
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = color
    App.ActiveDocument.ActiveObject.ViewObject.LineWidth = 10
    App.ActiveDocument.ActiveObject.ViewObject.LineColor = (1.0, 1.0, 0.0)

    obj.Shape = sh
    obj.ViewObject.LineWidth = 10
    obj.ViewObject.LineColor = (1.0, 1.0, 0.0)
    obj.ViewObject.ShapeColor = color

    print("Weights ..")
    print(bs.getWeights())


if 0:
    # border curves
    bc = Part.BSplineCurve()
    bc.buildFromPolesMultsKnots(ps[0], mv, kv, False, 3)
    Part.show(bc.toShape())
    App.ActiveDocument.ActiveObject.ViewObject.LineColor = color

    bc = Part.BSplineCurve()
    bc.buildFromPolesMultsKnots(ps[3], mv, kv, False, 3)
    Part.show(bc.toShape())

    bc = Part.BSplineCurve()
    bc.buildFromPolesMultsKnots(ps3[3], mv, kv, False, 3)
    Part.show(bc.toShape())


def makeEdge(pts, dim, step, w):

    k = pts.copy()
    k[:, dim] += step

    k2 = pts.copy()
    k2[:, dim] += 2 * step

    k3 = pts.copy()
    k3[:, dim] += 3*step

    bc = Part.BSplineCurve()
    bc.buildFromPolesMultsKnots(k3, mv, kv, False, 3, w)
    Part.show(bc.toShape())
    App.ActiveDocument.ActiveObject.ViewObject.LineColor = color

    bs = Part.BSplineSurface()
    bs.buildFromPolesMultsKnots(
        [pts, k, k2, k3], mv, mu, kv, ku, False, False, 3, 3, [w]*4)
    sh = bs.toShape()
    sp = App.ActiveDocument.addObject("Part::Spline", "leg "+str(dim))
    sp.Shape = sh
    sp.ViewObject.ControlPoints = True
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = color


if 0:
    makeEdge(ps3[3], 2, -100, [1, 0.5, 0.5, 1])
    makeEdge(ps[3], 1, 100, [1, 0.1, 0.1, 1])
    makeEdge(ps[0], 0, -100, [1, 0.1, 0.1, 1])

    makeEdge(ps[0], 1, -100, [1, 1, 1, 1])
    makeEdge(ps[3], 0, -100, [1, 1, 1, 1])
    makeEdge(ps3[3], 2, -100, [1, 1, 1, 1])

    bs.getWeights()


class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

# grundmethoden zum sichern

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class SimpleHood(PartFeature):
    def __init__(self, obj):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyVector", "Size",
                        "Base").Size = App.Vector(300, -100, 200)
        obj.addProperty("App::PropertyEnumeration", "xProfile", "Base")
        obj.xProfile = ["ellipse", "parabola", "hyperbola"]
        obj.addProperty("App::PropertyEnumeration", "yProfile", "Base")
        obj.yProfile = ["ellipse", "parabola", "hyperbola"]
        obj.addProperty("App::PropertyEnumeration", "zProfile", "Base")
        obj.zProfile = ["ellipse", "parabola", "hyperbola"]

        obj.yProfile = "ellipse"
        obj.xProfile = "parabola"
        obj.zProfile = "hyperbola"
        createShape(obj)
        ViewProvider(obj.ViewObject)

    def onChanged(self, fp, prop):
        print("onChanged", prop)
        if prop == "Size" or prop in ["xProfile", "yProfile", "zProfile"]:
            createShape(fp)


def run():
    b = App.activeDocument().addObject("Part::FeaturePython", "MySimpleHood")
    bn = SimpleHood(b)
