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
# -- bspline on top of a sketch
# --
# -- microelly 2016 v 0.5
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
# bspline von poles erzeugen

import FreeCAD as App
import Part
import FreeCADGui as Gui 

import NURBSinit


def printinfo(sp):
    print("\n" * 2)
    print("degree ", sp.Degree, " continuity ", sp.Continuity)
    print("count poles ", len(sp.getPoles()))
    print("knots ", sp.KnotSequence)
    print("weights ", sp.getWeights())


class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self


class MyBSpline(PartFeature):
    def __init__(self, obj):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "wire", "Wire", "")
        obj.addProperty("App::PropertyEnumeration", "mode", "Wire", "").mode = [
            "poles", "interpolate", "approximate"]
        obj.addProperty("App::PropertyEnumeration", "paramtype", "Wire", "")
        obj.paramtype = ['Default', 'Centripetal', 'Uniform', 'ChordLength']
        obj.addProperty("App::PropertyVector",
                        "InitialTangent", "Tangents", "")
        obj.addProperty("App::PropertyVector", "FinalTangent", "Tangents", "")
        obj.addProperty("App::PropertyStringList", "Tangents", "Tangents", "")
        obj.addProperty("App::PropertyStringList",
                        "TangentFlags", "Tangents", "")

    def recompute(self, fp):

        w = fp.wire
        eds = Part.__sortEdges__(w.Shape.Edges)
        pts = []
        for e in eds:
            ees = e.discretize(2)
            pts += ees[0:-1]

        pts.append(ees[-1])

        sp = Part.BSplineCurve()
        # sp.increaseDegree(3)
        if fp.mode == "poles":
            sp.buildFromPoles(pts)
        elif fp.mode == "interpolate":
            if fp.InitialTangent.Length != 0 and fp.FinalTangent.Length != 0:
                sp.interpolate(pts, InitialTangent=fp.InitialTangent,
                               FinalTangent=fp.FinalTangent)
            elif 1:
                # tangenten an einzelne Punkte
                Tangents = []
                Tangentflags = []
                tt = fp.Tangents
                print(tt)
                for i, p in enumerate(pts):
                    try:
                        #        print  str(tt[i])
                        j = ','.join(str(tt[i]).split())
                #        print j
                #        print str(fp.TangentFlags[i])
                        v = eval("App.Vector(" + j + ")")
                        v.normalize()
                        Tangents.append(v)
                        Tangentflags.append(str(fp.TangentFlags[i]) == '1')
                    except:
                        print("Fehler Tangenten Vektor ", i+1)
                        Tangents.append(App.Vector(1, 0, 0))
                        Tangentflags.append(0)
                try:
                    sp.interpolate(pts, Tangents=Tangents,
                                   TangentFlags=Tangentflags)
                except:
                    sp.interpolate(pts)
            else:
                sp.interpolate(pts)

        elif fp.mode == "approximate":
            paramtype = fp.paramtype
            if paramtype != 'Default':
                sp.approximate(Points=pts, ParamType=paramtype, DegMax=3)
            else:
                sp.approximate(pts)
        printinfo(sp)
        return sp

    def onChanged(self, fp, prop):
        if prop == "wire" and fp.wire != None:
            sp = self.recompute(fp)
            fp.Shape = sp.toShape()

    def execute(self, fp):
        if fp.wire != None:
            sp = self.recompute(fp)
            fp.Shape = sp.toShape()


class ViewProviderMyBSpline:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj


def makeMySpline():

    a = App.ActiveDocument.addObject("Part::FeaturePython", "MySpline")
    MyBSpline(a)
    ViewProviderMyBSpline(a.ViewObject)
    a.ViewObject.LineColor = (1.00, .00, .00)
    a.ViewObject.LineWidth = 3
    return a


def runtest():

    import Draft

    if App.ActiveDocument == None:
        App.newDocument("Unbenannt")
        App.setActiveDocument("Unbenannt")
        App.ActiveDocument = App.getDocument("Unbenannt")

    points = [App.Vector(-30, 0.0, 0.0), App.Vector(-20, 30, 0.0), App.Vector(20, 40, 0.0),
              App.Vector(40, -20, 0.0), App.Vector(150, -20, 0.0), App.Vector(190, 80, 0.0)]

    a = makeMySpline()
    a.wire = Draft.makeWire(points, closed=False, face=True, support=None)

    a.Tangents = '1 0 0,1 0 0,1 1 0,1 0 0,1 0 0,-1 0 0'.split(',')
    a.TangentFlags = ['0', '1', '1', '0', '0', '1']

    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")


print("bspline 2 loaded")

def ThousandsOfMainFunction():

    runtest()


def ThousandsOfRunWhatShouldIdo():
    runtest()
