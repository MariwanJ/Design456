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
'''interactive drawing of a curve onto a face'''
# -------------------------------------------------
# -- interctive draw on face
# --
# -- microelly 2017  0.2
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


# \cond
import Points
import Mesh
import time
from PySide import QtGui, QtCore
from say import *

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import time
import random

import NURBSinit

import isodraw
#reload(isodraw)


'''
# parameter
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MovePageStep",50)
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveCursorStep",10)

'''


# App.pts=App.ActiveDocument.Points.Points.Points

def check(pp, mode, updateNurbs=False, widget=None):
    print("check B ", mode)
    if mode == 'marker':
        createMarker(pp)
        return

    a = time.time()

    pc = App.ActiveDocument.getObject("MyGrid")
    nu = App.ActiveDocument.getObject(pc.Name+'_N')
    mm = App.ActiveDocument.getObject(pc.Name+'_M')

    nu.ViewObject.hide()
    mm.ViewObject.show()

    uc = pc.uc
    vc = pc.vc

    ptsk = mm.Mesh.Topology[0]
    faces = mm.Mesh.Topology[1]

    if not updateNurbs:
#        print ("modify"
        App.ptsk = ptsk
#        print  (len(ptsk)
        ff = -1
        for i, p in enumerate(ptsk):
            # if i <2: print (i,(p-pp).Length)
            if (p-pp).Length < 10:
#                print ("found ",i,(p-pp).Length)
                ff = i
                break

        ui = ff % (vc+1)
        vi = ff/(vc+1)
#        print (ui,vi)
        ptskarr = np.array(ptsk).reshape(uc+1, vc+1, 3)

        if mode == 'reset':
            ptskarr[:, :, 2] = 0
            ptsk = [App.Vector(p) for p in ptskarr.reshape((uc+1)*(vc+1), 3)]

        else:

            # r=int(widget.area.value())+1
            r = widget.r
            # h=(int(widget.height.value())+1)*0.1
            h = widget.h
            # h *= 100
            print(r, h, mode, '##', uc, vc, ui, vi)

            if r > 0:
                if mode == 'up':
                    ptskarr[vi-r:vi+r+1, ui-r:ui+r+1, 2] += h
                if mode == 'down':
                    ptskarr[vi-r:vi+r+1, ui-r:ui+r+1, 2] -= h
                if mode == 'zero':
                    ptskarr[vi-r:vi+r+1, ui-r:ui+r+1, 2] = 0

                ptsk = [App.Vector(p)
                                   for p in ptskarr.reshape((uc+1)*(vc+1), 3)]
                print(ptskarr[:, :, 2].max())

            else:
                if mode == 'up':
                    ptsk[ff].z += h
                if mode == 'down':
                    ptsk[ff].z -= h
                if mode == 'zero':
                    ptsk[ff].z = 0

        pc.Points = Points.Points(ptsk)
        mm.Mesh = Mesh.Mesh((ptsk, faces))

    b = time.time()
    print("update time ", b-a)

    if updateNurbs:
            print("upd Nurbs")
#            nu=App.ActiveDocument.getObject("Nurbs")
            nu.ViewObject.show()
#            mm=App.ActiveDocument.getObject("Mesh")
            mm.ViewObject.hide()
#            uc=60
#            vc=40
            bs = Part.BSplineSurface()

            if 0:
                bs.interpolate(np.array(ptsk).reshape(uc+1, vc+1, 3))
            else:
                kv = [1.0/(uc-3+1)*i for i in range(uc-2+1)]
                mv = [4]+[1]*(uc-4+1)+[4]

                ku = [1.0/(vc-3+1)*i for i in range(vc-2+1)]
                mu = [4]+[1]*(vc-4+1)+[4]

                ptskarr = np.array(ptsk).reshape(uc+1, vc+1, 3)
                bs.buildFromPolesMultsKnots(
                    ptskarr, mv, mu, kv, ku, False, False, 3, 3)

            nu.Shape = bs.toShape()

            c = time.time()
            print("nurbs time", c-b)


def createMarker(self):
    print("create Marker")
    import geodesic_lines
    #reload(.geodesic_lines)

    l = geodesic_lines.makeLabel(
        direction='Horizontal', labeltype='Position')
    l.obj = self.nu  # Gui.Selection.getSelectionEx()[0]
    l.LabelType = u"Custom"
    l.Label = "MyMarker"
    l.ViewObject.DisplayMode = u"2D text"
    l.ViewObject.TextSize = '15 mm'
    App.ActiveDocument.recompute()
#    l.TargetPoint=l.obj.Shape.Faces[0].Surface.value(l.u*0.01,l.v*0.01)
    geodesic_lines.hideAllProps(
        l, pns=['Text', 'CustomText', 'LabelType'])
#    return l
    sf = l.obj.Shape.Face1.Surface
    (u, v) = sf.parameter(self.pos)
    l.u = u*100
    l.v = v*100
    l.TargetPoint = self.pos
    l.Label = str((round(self.pos.x, 1), round(
        self.pos.y, 1), round(self.pos.z, 1)))


# \endcond

# Eventfilter for facedrawing

class EventFilter(QtCore.QObject):
    '''Eventfilter for facedrawing'''

# \cond

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.mouseWheel = 0
        self.enterleave = False
        self.enterleave = True
        self.keyPressed2 = False
        self.editmode = False
        self.key = 'x'
        self.posx = -1
        self.posy = -1
        self.lasttime = time.time()
        self.lastkey = '#'
        self.colorA = 0
        self.colors = []
        self.pts = []
        self.ptsm = []
        self.mode = 'n'

    def eventFilter(self, o, e):
        ''' the eventfilter for the facedraw server'''

        z = str(e.type())

        event = e

        if event.type() == QtCore.QEvent.ContextMenu: return True

        # not used events
        if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
                z == 'PySide.QtCore.QEvent.Type.ChildRemoved' or \
                z == 'PySide.QtCore.QEvent.Type.User' or \
                z == 'PySide.QtCore.QEvent.Type.Paint' or \
                z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
                z == 'PySide.QtCore.QEvent.Type.UpdateRequest':
            return QtGui.QWidget.eventFilter(self, o, e)

        if z == 'PySide.QtCore.QEvent.Type.KeyPress':
            # http://doc.qt.io/qt-4.8/qkeyevent.html
            print("key", e.key())

            # ignore editors
            try:
                if self.editmode:
                    return QtGui.QWidget.eventFilter(self, o, e)
            except: pass

            # only first time key pressed
            if not self.keyPressed2:
                self.keyPressed2 = True
                time2 = time.time()
                ee = e.text()

                if time2-self.lasttime < 0.01 and len(ee) > 0 and ee[0] == self.lastkey:
                    self.lasttime = time2
                    return False

                try:
                    # only two function keys implemented, no modifieres
                    if e.key() == QtCore.Qt.Key_F2:
                        say("------------F2-- show mode and moddata---------------")
                        return False

                    elif e.key() == QtCore.Qt.Key_Escape:
                        say("------------Escape = Stop-----------------")
                        stop()

                    elif e.key() == QtCore.Qt.Key_F3:
                        say("------------F3 up x-----------------")
                        self.dialog.modl.setText("Mode: add")
                        self.mode = 'up'
                        return False
                    elif e.key() == QtCore.Qt.Key_F4:
                        say("------------D down y-----------------")
                        self.dialog.modl.setText("Mode: subtract")
                        self.mode = 'down'
                        return False
                    elif e.key() == QtCore.Qt.Key_F5:
                        say("------------F3 zero-----------------")
                        self.dialog.modl.setText("Mode: reset to null")
                        self.mode = 'zero'
                        return False
                    elif e.key() == QtCore.Qt.Key_F6:

                        say("------------F6 none-----------------")
                        self.dialog.modl.setText("Mode: none")
                        self.mode = 'none'
                        return False


# some key bindings not used at the moment
#                    elif  e.key()== QtCore.Qt.Key_Return:
#                        say("------------Enter-----------------")
#                        self.update()

                    elif e.key() == QtCore.Qt.Key_Right:
                        print("Go right")
                        return True
                    elif e.key() == QtCore.Qt.Key_Left:
                        print("Go Left")
                        return True
                    elif e.key() == QtCore.Qt.Key_Up:
#                        self.mouseWheel += App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveCursorStep",10)
                        print("go up")
                        return True
                    elif e.key() == QtCore.Qt.Key_Down:
                        print("Go Down")
                        return True
                    elif e.key() == QtCore.Qt.Key_PageUp:
                        self.mouseWheel += App.ParamGet(
                            'User parameter:Plugins/nurbs').GetFloat("MovePageStep", 50)
                        self.dialog.ef_action("up!", self, self.mouseWheel)
                        return True
                    elif e.key() == QtCore.Qt.Key_PageDown:
                        self.mouseWheel -= App.ParamGet(
                            'User parameter:Plugins/nurbs').GetFloat("MovePageStep", 50)
                        self.dialog.ef_action("down!", self, self.mouseWheel)
                        return True

                    if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                        print("Enter Action-----------------------------")
                        # enter creates a new point ...
                        # vf=App.Vector(self.x,self.y,self.z)
                        print(self.pos)
                        if self.mode == 'marker':
                            createMarker(self)
                        return True
#                        self.colors += [self.colorA]
#                        self.pts += [vf]
#
#                        if len(self.pts)>1:
#                            self.wire.Shape=Part.makePolygon(self.pts)
#                            drawColorpath(self.pts,self.colors,self.colorA)

                    else:  # letter key pressed
                        ee=e.text()
                        if len(ee) > 0: r=ee[0]
                        else: r="key:" + str(e.key())

                        self.lastkey=e.text()

                        # zooming +-*
                        if r == '+':
                            Gui.activeDocument().ActiveView.zoomIn()
                            return True
                        if r == '-':
                            Gui.activeDocument().ActiveView.zoomOut()
                            return True
                        if r == '*':
                            Gui.activeDocument().ActiveView.fitAll()
                            return True

                        if r in ['a', 'b', 'c']:

                                print("KEY pressed ----------------------", r)



                except:
                    sayexc()




        if event.type() == QtCore.QEvent.MouseMove:
                (x, y)=Gui.ActiveDocument.ActiveView.getCursorPos()
                t=Gui.ActiveDocument.ActiveView.getObjectsInfo((x, y))

                # ---------------------

                cursor=QtGui.QCursor()
                p=cursor.pos()
#                if p.x()<100 or p.y()<100:
#                    print ("jump cursor facedraw 92"
#                    cursor.setPos(p.x()+100, p.y()+100)
                # -----------------------------------

                if t != None:  # if objects are under the mouse
                    # pts=App.ActiveDocument.shoe_last_scanned.Points.Points
#                    print ("-----!"
                    for tt in t:
                        if tt['Object'] == "MyGrid_N":
                            pp=App.Vector(tt['x'], tt['y'], tt['z'])

                            sp=App.ActiveDocument.getObject("Sphere")
                            if sp == None:
                                sp=App.ActiveDocument.addObject(
                                    "Part::Sphere", "Sphere")
                            sp.Placement.Base=pp


                            sf=self.nu.Shape.Face1.Surface
                            print("Position on nurbs:", sf.parameter(pp))
                            self.pos=pp
                            sf.parameter(pp)
                            if event.buttons() == QtCore.Qt.LeftButton:
#                                print ("LEFT BUTTON drawing"
                                check(pp, self.mode, False, self)
                            break
                    for tt in t:
                        if tt['Object'] == "MyGrid_M":
#                            print (tt['Object'],tt['Component'])
#                            print (tt['x'])
#                            print (tt['y'])
#                            print (tt['z'])
                            pp=App.Vector(tt['x'], tt['y'], tt['z'])

                            sp=App.ActiveDocument.getObject("Sphere")
                            if sp == None:
                                sp=App.ActiveDocument.addObject(
                                    "Part::Sphere", "Sphere")
                            sp.Placement.Base=pp



                            # sf=App.ActiveDocument.Nurbs.Shape.Face1.Surface
                            sf=self.nu.Shape.Face1.Surface
#                            print ("Position on nurbs:",sf.parameter(pp)
                            sf.parameter(pp)
                            if event.buttons() == QtCore.Qt.LeftButton:
#                                print ("LEFT BUTTON drawing"
                                check(pp, self.mode, False, self)
                            break
                    return False

        # end of a single key pressed
        if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
            self.lasttime=time.time()
            self.keyPressed2=False

        # enter and leave a widget - editor widgets
        if z == 'PySide.QtCore.QEvent.Type.Enter' or z == 'PySide.QtCore.QEvent.Type.Leave':
            pass

        # deactivate keys in editors context
        if z == 'PySide.QtCore.QEvent.Type.Enter' and \
            (o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
            self.editmode=True
        elif z == 'PySide.QtCore.QEvent.Type.Leave' and \
            (o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
            self.editmode=False

        # mouse movement only leaves and enters
        if z == 'PySide.QtCore.QEvent.Type.HoverMove':
            pass

        return QtGui.QWidget.eventFilter(self, o, e)

# \endcond

# draw a curve on a face and create the two subfaces defined by the curve

def drawcurve(wire, face, facepos=App.Vector()):
    '''draw a curve on a face and create the two subfaces defined by the curve'''

    print("drawcurve")

    # startposition
    wplace=wire.Placement
#    print wplace
    wpos=wplace.Base
#    print ("facepos ",facepos


    w=wire.Shape
    t=face

    # pts=[p.Point for p in w.Vertexes]
    pts=[p.Point - wpos for p in w.Vertexes]

    sf=t.Surface

    bs=sf

    print("hacks SSetze uv, sv auf 1")
    su=face.ParameterRange[1]
    sv=face.ParameterRange[3]


    if 0:
        pts2da=[sf.parameter(p) for p in pts[1:]]
        pts2d=[App.Base.Vector2d(p[0], p[1]) for p in pts2da]

        bs2d=Part.Geom2d.BSplineCurve2d()
        bs2d.setPeriodic()

        bs2d.interpolate(pts2d)
        bs2d.setPeriodic()

        e1=bs2d.toShape(t)


    bs2d=Part.Geom2d.BSplineCurve2d()
    pts2da=[sf.parameter(p) for p in pts]
    pts2d=[App.Base.Vector2d(p[0], p[1]) for p in pts2da]
    bs2d.buildFromPolesMultsKnots(
        pts2d, [1]*(len(pts2d)+1), range(len(pts2d)+1), True, 1)
    e1=bs2d.toShape(t)

    sp=App.ActiveDocument.getObject(wire.Label+"_Spline")
    if sp == None:
        sp=App.ActiveDocument.addObject("Part::Spline", wire.Label+"_Spline")
    sp.Shape=e1
    sp.ViewObject.LineColor=wire.ViewObject.ShapeColor
    sp.ViewObject.ShapeColor=wire.ViewObject.ShapeColor

    edges=e1.Edges
    ee=edges[0]
    splita=[(ee, face)]
    r=Part.makeSplitShape(face, splita)

    ee.reverse()
    splitb=[(ee, face)]
    r2=Part.makeSplitShape(face, splitb)

    if hasattr(wire, "drawFace"):

            try:
                rc=r2[0][0]
                rc=r[0][0]
            except: return

            sp=App.ActiveDocument.getObject(wire.Label+"_SplineFaceA")
            if sp == None:
                sp=App.ActiveDocument.addObject(
                    "Part::Spline", wire.Label+"_SplineFaceA")

            if wire.reverseFace: sp.Shape=r2[0][0]
            else: sp.Shape=r[0][0]

            # sp.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
            sp.ViewObject.ShapeColor=wire.ViewObject.ShapeColor
            # sp.ViewObject.LineColor=sp.ViewObject.ShapeColor

            # wire.ViewObject.LineColor=sp.ViewObject.ShapeColor
            # wire.ViewObject.ShapeColor=sp.ViewObject.ShapeColor
            print("HHHHHHHHHHHHHHHHH")

# new wire for next drawing

# -------------------- ring

def _drawring(name, wires, dirs, face, facepos=App.Vector()):
    '''draw a curve on a face and create the two subfaces defined by the curve'''

    print("drawring")

    es=[]
    for wireA in wires:
        # startposition
        wplace=wireA.Placement
    #    print wplace
        wpos=wplace.Base
    #    print ("facepos ",facepos
        wire=wireA


        # --------------- teil 1
        w=wireA.Shape
        t=face

        # pts=[p.Point for p in w.Vertexes]
        pts=[p.Point - wpos for p in w.Vertexes]

        sf=t.Surface

        bs=sf

        su=face.ParameterRange[1]
        sv=face.ParameterRange[3]

        pts2da=[sf.parameter(p) for p in pts[1:]]
        pts2d=[App.Base.Vector2d(p[0], p[1]) for p in pts2da]


        bs2d=Part.Geom2d.BSplineCurve2d()
        bs2d.setPeriodic()

        bs2d.interpolate(pts2d)
        bs2d.setPeriodic()

        e1_1=bs2d.toShape(t)


        print("huhuhu22")

        sp=App.ActiveDocument.getObject(wireA.Label+"_ASpline")
        print(sp)
        print(wireA.Label)
        if sp == None:
            sp=App.ActiveDocument.addObject(
                "Part::Spline", wireA.Label+"_Spline")
        sp.Shape=e1_1
        sp.ViewObject.LineColor=wireA.ViewObject.ShapeColor
        sp.ViewObject.ShapeColor=wireA.ViewObject.ShapeColor

        es.append(e1_1)
    # -------------------- teoil 2

        if 0:
            # --------------- teil 1
            w=wire2.Shape
            t=face

            # pts=[p.Point for p in w.Vertexes]
            pts=[p.Point - wpos for p in w.Vertexes]

            sf=t.Surface

            bs=sf
            su=bs.UPeriod()
            sv=bs.VPeriod()

            print("hacks etze uv, sv auf 1")
            su=face.ParameterRange[1]
            sv=face.ParameterRange[3]

        #    print ("debug map"
        #    print ("su ",su
        #    print ("sv ",sv
        #    print ("param range ", face.ParameterRange

            if su > 1000: su=face.ParameterRange[1]
            if sv > 1000: sv=face.ParameterRange[3]

            pts2da=[sf.parameter(p) for p in pts[1:]]
            pts2d=[App.Base.Vector2d(p[0], p[1]) for p in pts2da]

            bs2d=Part.Geom2d.BSplineCurve2d()
            bs2d.setPeriodic()

            bs2d.interpolate(pts2d)
            bs2d.setPeriodic()

            e1_2=bs2d.toShape(t)

            sp=App.ActiveDocument.getObject(wire2.Label+"_Spline")
            if sp == None:
                sp=App.ActiveDocument.addObject(
                    "Part::Spline", wire2.Label+"_Spline")
            sp.Shape=e1_2
            sp.ViewObject.LineColor=wire.ViewObject.ShapeColor
            sp.ViewObject.ShapeColor=wire.ViewObject.ShapeColor

        # --------------------------------------



        splita=[]
        for i, e in enumerate(es):

            edges=e.Edges
            ee=edges[0]
            if dirs[i]: ee.reverse()

            splita += [(ee, face)]

        r=Part.makeSplitShape(face, splita)




        if 1:

                sp=App.ActiveDocument.getObject(name)
                if sp == None:
                    sp=App.ActiveDocument.addObject("Part::Spline", name)

                # if wire.reverseFace: sp.Shape=r2[0][0]
                # else:

                sp.Shape=r[0][0]

                # sp.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
                sp.ViewObject.ShapeColor=wire.ViewObject.ShapeColor
                # sp.ViewObject.LineColor=sp.ViewObject.ShapeColor

                # wire.ViewObject.LineColor=sp.ViewObject.ShapeColor
                # wire.ViewObject.ShapeColor=sp.ViewObject.ShapeColor
                print("RRRRRRRRRRRRRRRRR")



def drawring(name, wires, dirs, faceobj, facepos=App.Vector()):
        _drawring(name, wires, dirs, faceobj.Shape.Face1, facepos)


def createnewwire(widget):
    '''new wire for next drawing'''

    ef=widget.ef

    w=App.ActiveDocument.addObject(
        "Part::Feature", "A Drawing on " + ef.objname + ": " + ef.subelement + "#")
    w.Shape=Part.Shape()
    wam=App.ActiveDocument.addObject(
        "Part::Feature", "YY Drawing on " + ef.objname + ": " + ef.subelement + "#")
    wam.Shape=Part.Shape()

    if 10:
        c=PySide.QtGui.QColorDialog.getColor(QtGui.QColor(random.randint(
            10, 255), random.randint(10, 255), random.randint(10, 255)))
        w.ViewObject.LineColor=(1.0/255*c.red(), 1.0 / \
                                255*c.green(), 1.0/255*c.blue())
        w.ViewObject.PointColor=(
            1.0/255*c.red(), 1.0/255*c.green(), 1.0/255*c.blue())
    else:
        w.ViewObject.LineColor=(
            random.random(), random.random(), random.random())

    ef.wire=w
    ef.wirem=wam
    ef.pts=[]



# dialog for facedrawing options

class MyWidget(QtGui.QWidget):
    '''dialog for facedrawing '''

    def commit(self):
        '''stop the dialog and server'''
        stop()

    def apply(self):
        '''draw the curve and stop'''
#        try: drawcurve(self.ef.wire,self.ef.subobj)
#        except: sayexc2()
        stop()




    def update(self):
        ''' dummy method'''
        sp=App.ActiveDocument.getObject("Sphere")
        if sp == None:
            sp=App.ActiveDocument.addObject("Part::Sphere", "Sphere")

        r=int(self.area.value())
        h=int(self.height.value())
        sp.Radius=(1+r)*10
        App.ActiveDocument.recompute()
        return

    def ef_action(self, *args):
        ''' dummy method'''
        return


def dialog(source=None):
    ''' create dialog widget'''

    w=MyWidget()
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    w.source=source
    w.imode=-1
    w.ef="no eventfilter defined"

#    mode=QtGui.QComboBox()
#    mode.addItem("up") #0
#    mode.addItem("down") #1
#    mode.addItem("zero") #2
#    mode.addItem("none") #3

#    w.mode='n'


    editorkey=App.ParamGet(
        'User parameter:Plugins/nurbs').GetString("editorKey", "h")
#    lab=QtGui.QLabel("Direction: " + editorkey)
    w.key=editorkey
#    w.modelab=lab

    modl=QtGui.QLabel("Mode -none-")
    w.modl=modl

    btn2=QtGui.QPushButton("Update Nurbs")
    btn2.clicked.connect(w.updateNurbs)


    btn=QtGui.QPushButton("Apply and close")
    btn.clicked.connect(w.apply)

    cobtn=QtGui.QPushButton("Reset")
    cobtn.clicked.connect(w.reset)

    cbtn=QtGui.QPushButton("Stop Dialog (preserve Aux)")
    cbtn.clicked.connect(stop)

    poll=QtGui.QLabel("Area:")

    ar=QtGui.QDial()
    ar.setMaximum(10)
    ar.setNotchesVisible(True)
    ar.valueChanged.connect(w.update)
    w.area=ar

    poll2=QtGui.QLabel("height:")

    he=QtGui.QDial()
    he.setMaximum(10)
    he.setNotchesVisible(True)
#    he.valueChanged.connect(w.setcursor2)
    w.height=he


    box=QtGui.QVBoxLayout()
    w.setLayout(box)

    for ww in [modl, btn2, btn, cobtn, poll, ar, poll2, he]:
        box.addWidget(ww)

    return w




# start the eventserver
class Nurbs_CulpterEventStarter:
    def Activated(self):
        try: 
            self.stop()
        except: pass
        self.start()
# stop the eventserver

    def stop(self):
        ''' stop eventserver'''
        mw=QtGui.qApp
        ef=App.eventfilter
        mw.removeEventFilter(ef)
        ef.keyPressed2=False
        ef.dialog.app.resetEdit()
        # ef.dialog.hide()

# create and initialize the event filter

    def start(self):
        '''create and initialize the event filter'''

        ef=EventFilter()
        ef.mouseWheel=0

        ef.subelement='SUBELE'
        ef.mode='up'
        ef.pc=App.ActiveDocument.MyGrid
        ef.mm=App.ActiveDocument.MyGrid_M
        ef.nu=App.ActiveDocument.MyGrid_N
        ef.objname=ef.pc.Name
        '''
        try:
                sel=Gui.Selection.getSelectionEx()
                fob=sel[0]
                s=Gui.Selection.getSelectionEx()
                print s,s[0].SubObjects

                if len(s[0].SubObjects)>0:
                    ef.subobj=s[0].SubObjects[0]
                    ef.objname=s[0].Object.Name
                    ef.subelement=s[0].SubElementNames[0]
                else:
                    ef.subobj=fob.Shape.Face1
                    ef.objname=fob.Name
                    ef.subelement="Face1"

                if ef.subobj.Surface.__class__.__name__ == 'BSplineSurface':
                    ef.rc=createRibCage(ef.subobj.Surface)

                ef.stack=[fob.ViewObject.Visibility,fob.ViewObject.Transparency,fob.ViewObject.Selectable]
                ef.fob=fob

                fob.ViewObject.Visibility=True
                fob.ViewObject.Transparency=70
                fob.ViewObject.Selectable=False

                Gui.Selection.clearSelection()

        except:
            sayexc2("no surface selected",
                    "Select first a face you want to draw on it")
            return
        '''

        App.eventfilter=ef

        mw=QtGui.qApp
        mw.installEventFilter(ef)
        ef.keyPressed2=False

        # ef.dialog=dialog()
        ef.dialog=mydialog(None)


        ef.dialog.ef=ef
        ef.r=2
        ef.h=2
    #    ef.dialog.show()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_CulpterEventStarter"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_CulpterEventStarter", Nurbs_CulpterEventStarter())






from say import *


layout='''
VerticalLayoutTab:
# VerticalLayout:
    id:'main'

    VerticalLayout:
#    HorizontalLayout:

        QtGui.QLabel:
            setText:"***   S C U L P T E R   ***"
            setVerticalStrech:  2


        HorizontalLayout:

            QtGui.QLabel:
                setText:"Select Action:"

            QtGui.QComboBox:
                id: 'actionmode'
                addItem: "up"
                addItem: "down"
                addItem: "zero"
                addItem: "none"
                addItem: "marker"
                currentIndexChanged.connect: app.modMode


#    VerticalLayout:
        setVerticalStrech:  10

        QtGui.QLabel:
            setText: "    C O N F I G U R E"


        HorizontalLayout:
            addSpacing: 0

            QtGui.QLabel:
                setText: "height"


            QtGui.QComboBox:
                id: 'heightc'
#                currentIndexChanged.connect: app.processHcombo


            QtGui.QDial:
                setValue: 2
                setMinimum: 1
                setMaximum: 10
                id: 'heightd'
                valueChanged.connect: app.modHeight
            QtGui.QLabel:
            QtGui.QLabel:

        HorizontalLayout:

            QtGui.QLabel:
                setText:"Area"

            QtGui.QComboBox:
                id: 'areac'
#                currentIndexChanged.connect: app.processWcombo

            QtGui.QDial:
                setValue: 1
                setMinimum: 1
                setMaximum: 10
                id: 'aread'
                valueChanged.connect: app.modArea
            QtGui.QLabel:
            QtGui.QLabel:




        HorizontalLayout:
            QtGui.QPushButton:
                id: "runbutton"
                setText: "Reset"
                clicked.connect: app.reset

            QtGui.QPushButton:
                setText: "Recompute Nurbs"
                clicked.connect: app.updateNurbs


            QtGui.QPushButton:
                setText: "Close"
                clicked.connect: app.resetEdit


'''

layoutAAAAAAAAA='''
VerticalLayoutTab:
# VerticalLayout:
    id:'main'

    VerticalLayout:

#        QtGui.QLabel:
#            setText:"***   N U R B S     E D I T O R   ***"


        HorizontalLayout:

            QtGui.QCheckBox:
                id: 'polegrid'
                setText: 'calculate PoleGrid'
#                stateChanged.connect: app.calculatePoleGrid
                visibility: False

            QtGui.QCheckBox:
                id: 'setmode'
                setText: 'Pole only'
                setVisible: False

            QtGui.QCheckBox:
                id: 'relativemode'
                setText: 'Height relative'
#                stateChanged.connect: app.relativeMode
                setChecked: True

            QtGui.QComboBox:
                id: 'focusmode'
    #            addItem: "single Pole"
    #            addItem: "VLine"
    #            addItem: "ULine"
    #            addItem: "UV Cross"
                addItem: "Rectangle"
#                currentIndexChanged.connect: app.setFocusMode

    VerticalLayout:



        QtGui.QLabel:
            setText: "    A C T I O N "

        HorizontalLayout:




    VerticalLayout:

        QtGui.QLabel:
            setText: "    S E L E C T I O N"

        HorizontalLayout:

            QtGui.QLabel:
                id: 'pole1'
                setText: " pole1: "
            QtGui.QLabel:
                id: 'pole2'
                setText: " pole2: "


        HorizontalLayout:
            addSpacing: 0

            QtGui.QLabel:
                setText: "u"


            QtGui.QLineEdit:
                setText: "1"
                setMaxLength: 3
#                editingFinished: app.getInfo
                id: 'u'

            QtGui.QComboBox:
                id: 'ucombo'
#                currentIndexChanged.connect: app.processUcombo


            QtGui.QDial:
                setValue: 2
                id: 'ud'
                setMinimum: 1
                setMaximum: 7
                setTickInterval: 1
#                valueChanged.connect: app.getDataFromNurbs
#            QtGui.QSpacerItem:
#                is:'spacer'


            QtGui.QLabel:
                setText:"v "

            QtGui.QLineEdit:
                setText:"1"
                id: 'v'
#                returnPressed.connect: app.vFinished


            QtGui.QComboBox:
                id: 'vcombo'
#                currentIndexChanged.connect: app.processVcombo


            QtGui.QDial:
                setValue: 2
                id: 'vd'
                setMinimum: 1
                setMaximum: 5
                setTickInterval: 1
#                valueChanged.connect: app.getDataFromNurbs


#        HorizontalLayout:
#            QtGui.QPushButton:
#                setText: "u++"
#                clicked.connect: app.upp

#            QtGui.QPushButton:
#                setText: "u --"
#                clicked.connect: app.umm

#            QtGui.QPushButton:
#                setText: "v++"
#                clicked.connect: app.vpp


#            QtGui.QPushButton:
#                setText: "v --"
#                clicked.connect: app.vmm
#                clicked.connect: app.vmm

#        HorizontalLayout:
#            QtGui.QPushButton:
#                setText: "edit selected pole"
#                clicked.connect: app.getselection

#            QtGui.QPushButton:
#                setText: "set pole 1"
#                clicked.connect: app.setPole1

#            QtGui.QPushButton:
#                setText: "set pole 2"
#                clicked.connect: app.setPole2

        QtGui.QCheckBox:
            id: 'pole1active'
            setText: 'Pole 1 in change'
#            stateChanged.connect: app.relativeMode
            setChecked: True

        QtGui.QCheckBox:
            id: 'singlepole'
            setText: 'Single Pole mode'
#            stateChanged.connect: app.relativeMode
            setChecked: True




#        QtGui.QPushButton:
#            setText: "Commit relative values"
#            id: 'updateRelative'
#            clicked.connect: app.updateRelative


'''


class MyApp(object):

    def __init__(self):
        self.lock=False


    def resetEdit(self):
        Gui.ActiveDocument.resetEdit()
        import miki as miki
        # #reload(miki)
        mw=miki.getMainWindow()
        miki.getComboView(mw).removeTab(2)
        miki.getComboView(mw).setCurrentIndex(0)
        # stop()


    '''
        def updateDialog(self):
            self.root.ids['ud'].setMaximum(self.obj.Object.nNodes_u-2)

            rc=self.root.ids['focusmode'].currentText()
            v=self.root.ids['vd'].value()
            self.root.ids['pole1'].setText("Pole 1:" + str([u+1,v+1]))
            if self.root.ids['singlepole'].isChecked():
            self.root.ids['runbutton'].hide()
            self.root.ids['runbutton'].show()

            self.update()
            print (self.root
            print (self.obj
            print (self.obj.Object.Label

            print ("shape .."
            print (self.obj.Object.Proxy.g.shape


    '''

    def modHeight(self):
        h=int(round(self.root.ids['heightd'].value()))
        self.root.ids['heightc'].setCurrentIndex(int(h)-1)
        self.dialog.ef.h=int(h)
        self.update()

    def modArea(self):
        h=int(round(self.root.ids['aread'].value()))
        self.root.ids['areac'].setCurrentIndex(int(h)-1)
        self.dialog.ef.r=int(h)
        self.update()


    def modMode(self):
        m=self.root.ids['actionmode'].currentText()
        self.dialog.ef.mode=m
        self.update()


    def reset(self):
        check(App.Vector(), 'reset', False)

    def updateNurbs(self):
        check(App.Vector(), 'no', updateNurbs=True)

    def update(self):
        print("update")
        print(self.dialog.ef.mode)
        print(self.dialog.ef.h)
        print(self.dialog.ef.r)



def mydialog(obj):

    import miki as miki
    #reload(miki)

    app=MyApp()
    miki=miki.Miki()

    miki.app=app
    app.root=miki
    app.obj=obj
    app.dialog=miki

#    miki.parse2(layout)
    miki.run(layout)

    miki.ids['areac'].addItems([str(n) for n in range(1, 11)])
    miki.ids['areac'].setCurrentIndex(1)

    miki.ids['heightc'].addItems([str(n) for n in range(1, 11)])
    miki.ids['heightc'].setCurrentIndex(1)

    return miki




# ------------------
