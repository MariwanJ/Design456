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

from PySide import QtGui, QtCore

from PySide.QtCore import *
from PySide.QtGui import *

import NURBSinit

import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import time
 
import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit
import Part,Draft



# methods for the 3D object interface
def getArr(obj,scale=1):
    arr=[[p.x,p.y,p.z] for p in obj.Points]
    return np.array(arr)/scale

def setArr(arr,obj,scale=1):
    obj.Points=[App.Vector(tuple(p)) for p in arr*scale]
    App.ActiveDocument.recompute()




def np2tab(arr,tab):
    (xc,yc)=arr.shape
    for x in range(xc):
        for y in range(yc):
            newitem = QTableWidgetItem(str(arr[x,y]))
            tab.setItem(x, y, newitem)

def tab2np(tab):
    arr=[]
    rc=tab.rowCount()
    cc=tab.columnCount()
    for r in range(rc):
        for c in range(cc):
            arr.append(float(tab.item(r,c).text().replace(',', '.')))
    return np.array(arr).reshape(rc,cc)


def itemChanged(widget,*args):
    arr=tab2np(widget.table)
    widget.data=arr
    widget.target.update(arr,scale=widget.scale)
    rowcol(widget)


class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setdata()


    def setdata(self):
        (xc,yc)=self.data.shape
        for x in range(xc):
            for y in range(yc):
                newitem = QTableWidgetItem(str(self.data[x,y]))
                self.setItem(x, y, newitem)

        horHeaders=['x','y','z']
        self.setHorizontalHeaderLabels(horHeaders)


def pressed(index):
    print ("pressed",index.column(),index.row())

def rowcol(w,*args):
    print ("selection row/column changed")


    print (w,args)
    for i in w.table.selectedItems():
        print (i.row(),i.column())

    pts=[]
    for i in w.table.selectedItems():
        print (i.row(),i.column())
        pts.append(App.Vector(w.data[i.row()]))

    print ("huhuhuhsfsdfdf u")
    print (pts)
    print ("selection changed ---------------",w.scale)
    w.selection.update(pts,scale=w.scale)
    print ("-----------------")

def rowcol2(w,*args):
    print ("2-------------------selection row/column changed")


    print (w,args)
    for i in w.table.selectedItems():
        print (i.row(),i.column())

    pts=[]
    for i in w.table.selectedItems():
        print (i.row(),i.column())
        pts.append(App.Vector(w.data[i.row()]))
    print ("huhuhuhu")
    print (pts)
    print ("selection changed ---------------",w.scale)
    w.selection.update(pts,scale=w.scale)
    print ("-----------------")

def posfromsel(w):
    t=Gui.Selection.getSelectionEx()[0]
    v=t.PickedPoints[0]

    for i in w.table.selectedItems():
        print (i.row(),i.column())
#        v=[3,4,5]
        c=i.column()
        i.setText(str(v[c]))


def button(widget):
    arr=tab2np(widget.table)
    widget.setArr(arr,widget.obj,scale=widget.scale)
    widget.target.update(arr,scale=widget.scale)

def reload(widget):
    arr=getArr(widget.obj,scale=widget.scale)
    np2tab(arr,widget.table)

def die(widget):
    widget.target.die()
    widget.selection.die()
    widget.close()


class MyTarget():
    ''' visualization of the dialog data'''

    def __init__(self):
        self.obj=App.ActiveDocument.addObject("Part::Feature","__tmp" +str(time.time()))
        self.obj.ViewObject.PointSize=10
        self.obj.ViewObject.PointColor=(0.,0.,1.)
        self.obj.ViewObject.LineColor=(0.,0.,1.)

    def update(self,coor=[0,0,0],scale=1):
        pts=[App.Vector(tuple(c)) for c in np.array(coor)*scale]
        try: 
            pol=Part.makePolygon(pts)
            self.obj.Shape=pol
        except: 
            pol=[]
            #vts=[Part.Vertex(pp) for pp in pts]
            #comp=Part.makeCompound(vts)
            if len(pts)>0:
                self.obj.Shape=Part.Vertex(pts[0]) 

    def die(self):
        try: App.ActiveDocument.removeObject(self.obj.Name)
        except: pass



def pointEditor(obj,scale=1):

    w=QtGui.QWidget()
    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setGeometry(50, 30, 350, 630)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    dt=Draft.getType(obj)
    if dt in ['BSpline','Wire','BezCurve']:
        w.setArr=setArr
        w.getArr=getArr
    else: 
        raise Exception("Unhandled type " + dt)

    w.scale=scale
    w.obj=obj
    arr=getArr(obj,scale=w.scale)
    w.data=arr/w.scale
    rs=arr.shape[0]


    w.target=MyTarget()
    w.target.update(arr,scale)
    
    w.selection=MyTarget()
    w.selection.obj.ViewObject.PointSize=15
    w.selection.obj.ViewObject.PointColor=(2.,0.,0.)


    w.table = MyTable(arr,rs,3)
    w.table.pressed.connect(pressed)
    y=lambda a,b: rowcol(w,a,b)
    y=lambda: rowcol(w)
    y2=lambda: rowcol2(w)
    w.table.currentCellChanged.connect(y2)
    w.table.itemSelectionChanged.connect(y)
    

    w.table.itemSelectionChanged.connect(lambda:itemChanged(w))
    w.table.itemChanged.connect(lambda:itemChanged(w))


    l=QtGui.QLabel("Editor Points of: " + obj.Label)
    box.addWidget(l)

    box.addWidget(w.table)

    b=QtGui.QPushButton("Get Pos from Selection")
    b.pressed.connect(lambda:posfromsel(w))
    box.addWidget(b)


    b=QtGui.QPushButton("Reload")
    b.pressed.connect(lambda:reload(w))
    box.addWidget(b)

    b=QtGui.QPushButton("Apply Table")
    b.pressed.connect(lambda:button(w))
    box.addWidget(b)

    b=QtGui.QPushButton("Close")
    b.pressed.connect(lambda:die(w))
    box.addWidget(b)

    w.show()
    return w

class Nurbs_DraftBSplineEditorR1:
    """  This is the run part"""
    def Activated(self):
        scale=1
        print ("RUN ---",scale)
        obj=Gui.Selection.getSelectionEx()[0]
        print (obj)
        return pointEditor(obj,scale=scale)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_DraftBSplineEditorR1")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_DraftBSplineEditorR1"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_DraftBSplineEditorR1", Nurbs_DraftBSplineEditorR1())



class Nurbs_DraftBSplineEditorR2:
    """  This is the run2 part"""
    def Activated(self):
        self.run2()
    def run2(self):
        #create the Bspline
        p1 = App.Vector(0,0,0)
        p2 = App.Vector(1,1,0)
        p3 = App.Vector(0,2,0)
        p4 = App.Vector(-1,1,0)
        p5 = App.Vector(-1,1,3)

        import Draft
        Draft.makeBSpline([p1,p2,p3,p4,p5],closed=True)
        obj=App.ActiveDocument.ActiveObject
        w=pointEditor(obj)
        w.show()
        return w

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_DraftBSplineEditorR1")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_DraftBSplineEditorR1"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_DraftBSplineEditorR2", Nurbs_DraftBSplineEditorR2())

