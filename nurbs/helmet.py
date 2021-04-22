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
# -- helmlet with bezier border
# --
# -- microelly 2018 v 0.1
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit
import Sketcher
import Part
from say import *



import os

try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")

import time

from pyob import FeaturePython, ViewProvider
#reload (pyob)


class _VPH(ViewProvider):
    ''' basic defs '''

    def setupContextMenu(self, obj, menu):
        menu.clear()
        action = menu.addAction("MyMethod #1")
        action.triggered.connect(lambda: self.methodA(obj.Object))
        action = menu.addAction("MyMethod #2")
        menu.addSeparator()
        action.triggered.connect(lambda: self.methodB(obj.Object))
        action = menu.addAction("Edit Sketch")
        action.triggered.connect(lambda: self.myedit(obj.Object))

    def myedit(self, obj):
        self.methodB(None)
        self.pm = obj.Placement
        Gui.activeDocument().setEdit(obj.Name)
        obj.ViewObject.show()
        run(obj)
        self.methodA(None)

    def methodA(self, obj):
        print("my Method A")
        App.ActiveDocument.recompute()

    def methodB(self, obj):
        print("my method B")
        App.ActiveDocument.recompute()

    def methodC(self, obj):
        print("my method C !!")
        print(obj)

        App.ActiveDocument.recompute()
        run(obj)
        obj.Placement = self.pm

    def unsetEdit(self, vobj, mode=0):
        self.methodC(vobj.Object)
        vobj.Object.Placement = self.pm

    def doubleClicked(self, vobj):
        print("double clicked")
        self.myedit(vobj.Object)

        print("Ende double clicked")

# -------------------------------


def hideAllProps(obj, pns=None):
    if pns == None:
        pns = obj.PropertiesList
    for pn in pns:
        obj.setEditorMode(pn, 2)


def readonlyProps(obj, pns=None):
    if pns == None:
        pns = obj.PropertiesList
    for pn in pns:
        try:
            obj.setEditorMode(pn, 1)
        except:
            pass


def setWritableAllProps(obj, pns=None):
    if pns == None:
        pns = obj.PropertiesList
    for pn in pns:
        obj.setEditorMode(pn, 0)


class Helmet(FeaturePython):
    def __init__(self, obj, patch=False, uc=5, vc=5):
        FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyLink", "equator")
        obj.addProperty("App::PropertyLink", "meridian")
        obj.equator = createHelperSketch("Equator")
        obj.meridian = createHelperSketch("Meridian")

        obj.addProperty("App::PropertyBool", "onlyFace")
        obj.addProperty("App::PropertyLink", "sketch")
        obj.addProperty("App::PropertyFloat", "height").height = 100
        obj.addProperty("App::PropertyFloat", "border").border = 100
        obj.addProperty("App::PropertyVector", "offset")
        obj.offset = App.Vector(500, 300, 0)
#        try:
#            obj.equator=App.ActiveDocument.Sketch
#            obj.meridian=App.ActiveDocument.Sketch001
#        except:

#            print ("keine Hilfskurven verfuegbar"

    def attach(self, vobj):
        print("attach -------------------------------------")
        self.Object = vobj.Object
        self.obj2 = vobj.Object

    def onChanged(self, fp, prop):
        # if not hasattr(fp,'onchange') or not fp.onchange : return
        print("########################## changed ", prop)
        if prop == "height":
            print("change XXXX")
            print(fp.height)
            fp.equator.movePoint(1, 2, App.Vector(0, fp.height))
            fp.meridian.movePoint(1, 2, App.Vector(0, fp.height))
            fp.equator.solve()
            fp.meridian.solve()
            fp.equator.recompute()
            fp.meridian.recompute()
            fp.equator.purgeTouched()
            fp.meridian.purgeTouched()
            return

        if prop in ["sketch", "height", "border"]:
            try:
                run(fp)
            except:
                sayexc("fhelre run")
#        run(fp)

    def execute(self, fp):
        try:
            self.Lock
        except:
            self.Lock = False
        if not self.Lock:
            self.Lock = True
            try:
                fp.equator.Placement.Rotation = App.Rotation(
                    App.Vector(1, 0, 0), 90)
                fp.meridian.Placement.Rotation = App.Rotation(
                    App.Vector(1, 1, 1), 120)
                run(fp)
            except:
                sayexc('update error')
            self.Lock = False


def createSketch(sk):

    # sk=App.ActiveDocument.addObject('Sketcher::SketchObject','helmlet')

    # aussenring

    pts2 = [
        (-200, 0, 0), (-200, -50, 0), (-150, -75, 0), (-100, -100, 0),
        (0, -100, 0), (100, -100, 0), (150, -75, 0), (200, -50, 0), (200, 0, 0),
        (200, 50, 0), (150, 75, 0), (100, 100, 0),
        (0, 100, 0), (-100, 100, 0), (-150, 75, 0), (-200, 50, 0), (-200, 0, 0),
    ]

    import Draft

    pts = [App.Vector(p) for p in pts2]
    # Draft.makeWire(pts)

    for i in range(16):
        sk.addGeometry(Part.LineSegment(pts[i], pts[i+1]), False)

    for i in range(15):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, i+1, 1))

    sk.addConstraint(Sketcher.Constraint('Coincident', 15, 2, 0, 1))

    # innenring

    pts2 = [(-50, -30, 0), (50, -30, 0), (50, 30, 0), (-50, 30, 0)]
    pts = [App.Vector(p) for p in pts2]
    # Draft.makeWire(pts)

    for i in range(4):
        sk.addGeometry(Part.LineSegment(pts[i-1], pts[i]), False)

    for i in range(3):
        print("aa", i)
        sk.addConstraint(Sketcher.Constraint('Coincident', 16+i, 2, 16+i+1, 1))

    sk.addConstraint(Sketcher.Constraint('Coincident', 19, 2, 16, 1))

    # parallele gruppen

    sk.addConstraint(Sketcher.Constraint('Parallel', 0, 15))
    for i in range(7):
        sk.addConstraint(Sketcher.Constraint('Parallel', 2*i+1, 2*i+2))

    for i in [0, 7, 16, 18]:
        print(i)
        sk.addConstraint(Sketcher.Constraint('Vertical', i))

    for i in [3, 11, 17, 19]:
        sk.addConstraint(Sketcher.Constraint('Horizontal', i))

    for i, c in enumerate(sk.Constraints):
        sk.setVirtualSpace(i, True)

    sk.solve()
    sk.recompute()


def createHelperSketch(role):
    ''' sketch for equator and meridian'''
    sk = App.ActiveDocument.addObject('Sketcher::SketchObject', role)
    for i in range(4):
        sk.addGeometry(Part.LineSegment(App.Vector(
            i*100, 0, 0), App.Vector((i+1)*100., 0, 0)))
    for i in range(3):
        sk.addConstraint(Sketcher.Constraint('Coincident', i, 2, i+1, 1))
    sk.movePoint(1, 2, App.Vector(200, 100))
    return sk


class Nurbs_commandCreateHelmet:

    def Activated(self):
        # a=App.ActiveDocument.addObject("Part::FeaturePython","helmet")
        a = App.ActiveDocument.addObject(
            'Sketcher::SketchObjectPython', "helmet")

        self.makeHelmet(a)
        a.onlyFace = True
        a.sketch = obj
        createSketch(a)
        a.recompute()

        _VPH(a.ViewObject, NURBSinit.ICONS_PATH+'createHelmet.svg')
        # a.ViewObject.Transparency=60
        a.ViewObject.ShapeColor = (0.3, 0.6, 0.3)
        if obj != None:
            a.Label = "Helmet for "+obj.Label

    def makeHelmet(self, fp):
        self.fp = fp
        pts = [self.fp.getPoint(i, 1) for i in range(16)]
        pts2 = [self.fp.getPoint(i, 1) for i in range(16, 20)]
        ptsall = np.zeros(25*3).reshape(5, 5, 3)
        ptsall[0, 2] = pts[0]
        ptsall[0, 3] = pts[1]
        ptsall[0, 4] = pts[2]
        ptsall[1, 4] = pts[3]
        ptsall[2, 4] = pts[4]
        ptsall[3, 4] = pts[5]
        ptsall[4, 4] = pts[6]
        ptsall[4, 3] = pts[7]
        ptsall[4, 2] = pts[8]
        ptsall[4, 1] = pts[9]
        ptsall[4, 0] = pts[10]
        ptsall[3, 0] = pts[11]
        ptsall[2, 0] = pts[12]
        ptsall[1, 0] = pts[13]
        ptsall[0, 0] = pts[14]
        ptsall[0, 1] = pts[15]

        ptsall[1:4, 3, 1] = pts2[1].y
        ptsall[1:4, 1, 1] = pts2[3].y
        ptsall[3, 1:4, 0] = pts2[3].x
        ptsall[1, 1:4, 0] = pts2[1].x

        print("arquator")
        pa = self.fp.equator.getPoint(1, 1)
        pb = self.fp.equator.getPoint(2, 2)

        ptsall[3, 1:4, 0] = pb.x
        ptsall[1, 1:4, 0] = pa.x

        print("meridan")
        pa = self.fp.meridian.getPoint(1, 1)
        pb = self.fp.meridian.getPoint(2, 2)

        ptsall[1:4, 3, 1] = pa.x
        ptsall[1:4, 1, 1] = pb.x

        h = fp.equator.getPoint(1, 2).y
        print("HEights", h, fp.height)
        if h != fp.height:
            fp.height = h

        # fp.equator.movePoint(1,2,App.Vector(0,fp.height))
        self.fp.equator.movePoint(0, 1, fp.getPoint(0, 1))
        self.fp.equator.movePoint(3, 2, fp.getPoint(7, 2))
        self.fp.equator.solve()
        self.fp.equator.purgeTouched()

        self.fp.meridian.movePoint(1, 2, App.Vector(0, fp.height))
        t = self.fp.getPoint(4, 1)
        t2 = self.fp.getPoint(12, 1)
        self.fp.meridian.movePoint(0, 1, App.Vector(t.y, 0, 0))
        self.fp.meridian.movePoint(3, 2, App.Vector(t2.y, 0, 0))

        self.fp.meridian.solve()
        self.fp.meridian.purgeTouched()

        ptse = [self.fp.equator.getPoint(
            0, 1)+App.Vector(0, -self.fp.border, 0)]
        ptse += [self.fp.equator.getPoint(i, 1) for i in range(4)]
        ptse += [self.fp.equator.getPoint(3, 2)]
        ptse += [self.fp.equator.getPoint(3, 2) +
                 App.Vector(0, -self.fp.border, 0)]

        ptsf = [self.fp.meridian.getPoint(
            0, 1)+App.Vector(0, -self.fp.border, 0)]
        ptsf += [self.fp.meridian.getPoint(i, 1) for i in range(4)]
        ptsf += [self.fp.meridian.getPoint(3, 2)]
        ptsf += [self.fp.meridian.getPoint(3, 2) +
                 App.Vector(0, -self.fp.border, 0)]

        ptse2 = [App.Vector(p.x, 0, p.y) for p in ptse]
        ptsf2 = [App.Vector(0, p.x, p.y) for p in ptsf]

        ptsall[1:4, 1:4, 2] = fp.height

        yy = np.array(ptsall)
        yy2 = np.array([yy[0], yy[0], yy[1], yy[2], yy[3], yy[4], yy[4]])

        yy2[0, :, 2] = - self.fp.border
        yy2[-1, :, 2] = -self.fp.border

        yy = yy2.swapaxes(0, 1)
        yy2 = np.array([yy[0], yy[0], yy[1], yy[2], yy[3], yy[4], yy[4]])
        yy2[0, 1:-1, 2] = -self.fp.border
        yy2[-1, 1:-1, 2] = -self.fp.border

        af = Part.BSplineSurface()

        yy2a = np.array(yy2)
        yy3a = yy2a.swapaxes(0, 1)

        print("!!", Gui.ActiveDocument.getInEdit(), "!!")

        vp = Gui.ActiveDocument.getInEdit()
        if vp != None and vp.Object == self.fp:
            yy2 += self.fp.offset

#        af.buildFromPolesMultsKnots(yy2,
#            [4,1,1,1,4],[4,1,1,1,4],
#            [0,1,2,3,4],[0,1,2,3,4],
#            False,False,3,3)

        af.buildFromPolesMultsKnots(yy2,
                                    [4, 3, 4], [4, 3, 4],
                                    [0, 1, 2, ], [0, 1, 2, ],
                                    False, False, 3, 3)

        if self.fp.onlyFace:
            self.fp.Shape = af.toShape()
            return

        comps = []
        comps += [af.toShape()]

        yy3 = yy2.swapaxes(0, 1)

        for yy in [yy2, yy3]:
            for r in [0, 3, 6]:
                bc = Part.BSplineCurve()
                bc.buildFromPolesMultsKnots(yy[r],
                                            [4, 1, 1, 1, 4],
                                            [0, 1, 2, 3, 4],
                                            False, 3)
                comps += [bc.toShape()]

#        print ("ptse23,",ptse2)

        if 0:
            for yy in [yy2a, yy3a]:
                for r in [0, 6]:
                    bc = Part.BSplineCurve()
                    bc.buildFromPolesMultsKnots(yy[r],
                                                [4, 1, 1, 1, 4],
                                                [0, 1, 2, 3, 4],
                                                False, 3)
                    comps += [bc.toShape()]

        for yy in [ptse2, ptsf2]:
            bc = Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(yy,
                                        [4, 1, 1, 1, 4],
                                        [0, 1, 2, 3, 4],
                                        False, 3)
            comps += [bc.toShape()]

        # comps += [Part.makePolygon(ptse)]

        self.fp.Shape = Part.Compound(comps)
        
        
    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_commandCreateHelmet")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_commandCreateHelmet"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs commandCreateHelmet", _tooltip)}
        
Gui.addCommand("Nurbs_commandCreateHelmet", Nurbs_commandCreateHelmet())



class Nurbs_HelmetCreateTriangel:
    def Activated(self):
        self.createTriangle()

    def createTriangle(self):
        import numpy as np
        k = 10
        rings = [
            [[-100, 0, 0], [-80, 20, 0], [-20, 80, 0], [0, 100, 0]],
            [[-80, 0, 0], [-50, 20, 40], [0, 50, 40], [20, 80, 0]],
            [[-20, 0, -20+k], [0, 20, 20], [50, 30, 40], [80, 20, 0]],
            [[0, 0, -20+k], [20, 0, -20+k], [80, 0, 0], [100, 0, 0]],
        ]
        rr = np.array(rings)

        bs = Part.BSplineSurface()
        bs.buildFromPolesMultsKnots(rr,
                                    [4, 4], [4, 4],
                                    [0, 2], [0, 2],
                                    False, False, 3, 3)
        if 0:
            bs.insertUKnot(1, 3, 0)
            bs.insertVKnot(1, 3, 0)

            bs.insertUKnot(1.5, 3, 0)

        sk = App.ActiveDocument.addObject('Part::Spline', 'adapter')
        sk.Shape = bs.toShape()

        rA = np.array([rr[0], rr[0]+[-30, 30, 30]])
        bs = Part.BSplineSurface()
        bs.buildFromPolesMultsKnots(rA,
                                    [2, 2], [4, 4],
                                    [0, 2], [0, 2],
                                    False, False, 1, 3)
        sk = App.ActiveDocument.addObject('Part::Spline', 'rA')
        sk.Shape = bs.toShape()

        rr[1] = rr[0]+rA[0]-rA[1]

        rrs = rr.swapaxes(0, 1)
        rB = np.array([rrs[-1], rrs[-1]+[30, 30, 20]])
        bs = Part.BSplineSurface()
        bs.buildFromPolesMultsKnots(rB,
                                    [2, 2], [4, 4],
                                    [0, 2], [0, 2],
                                    False, False, 1, 3)
        sk = App.ActiveDocument.addObject('Part::Spline', 'rB')
        sk.Shape = bs.toShape()

        # rrs[-2][2:]=rrs[-1][2:]+rB[0][2:]-rB[1][2:]
        rrs[-2][1:] = rrs[-1][1:]+rB[0][1:]-rB[1][1:]

        rru = rrs.swapaxes(0, 1)
        # rru=rings
        # rru=rr

        bs = Part.BSplineSurface()
        bs.buildFromPolesMultsKnots(rru,
                                    [4, 4], [4, 4],
                                    [0, 2], [0, 2],
                                    False, False, 3, 3)
        if 0:
            bs.insertUKnot(1, 3, 0)
            bs.insertVKnot(1, 3, 0)

            bs.insertUKnot(1.5, 3, 0)

        sk = App.ActiveDocument.addObject('Part::Spline', 'adapter')
        sk.Shape = bs.toShape()

        if 0:
            comps = []
            bsa = bs.copy()
            bsasegment(0, 1, 0, 1)
            comps += [bsa.toShape()]

            bsa = bs.copy()
            bsasegment(0, 1, 1, 2)
            comps += [bsa.toShape()]

            bsa = bs.copy()
            bsasegment(1, 2, 0, 1)
            comps += [bsa.toShape()]

            bsa = bs.copy()
            bsasegment(1, 2, 1, 2)
            comps += [bsa.toShape()]

            sk = App.ActiveDocument.addObject('Part::Spline', 'split')
            sk.Shape = Part.Compound(comps)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_HelmetCreateTriangel")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_HelmetCreateTriangel"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_HelmetCreateTriangel", Nurbs_HelmetCreateTriangel())

