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

'''objekt auf curve positionieren und ausrichten'''


import FreeCAD 
import FreeCADGui
import Design456Init
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    


## callback from widget

def srun(w):

    bc=w.path.Shape.Edge1.Curve
    c=w.target
    v=w.ha.value()*0.01
    movepos(bc,c,v)


## create a copy on the current position

def dropcopy(w):
    c=w.target
    App.ActiveDocument.addObject('Part::Feature','Copy_of_'+c.Label+"_at_"+str(w.ha.value())).Shape=c.Shape
    App.ActiveDocument.recompute()

## put the object c  on the curve bc in relative position  v
# @param bc bspline curve
# @param c part
# @param v float between 0 and 1 
#
#.

def movepos(bc,c,v):
    '''movepos(bc,c,v)'''

    pa=bc.LastParameter
    ps=bc.FirstParameter

    v=ps +(pa-ps)*v

    t=bc.tangent(v)[0]
    p=bc.value(v)

    zarc=np.arctan2(t.y,t.x)
    zarc *=180.0/np.pi

    harc=np.arcsin(t.z)
    harc *=180.0/np.pi

    pl=App.Placement()
    pl.Rotation=App.Rotation(App.Vector(0,1,0,),90-harc)

    pa=App.Placement()
    pa.Rotation=App.Rotation(App.Vector(0,0,1,),zarc)
    pl2=pa.multiply(pl)

    pl2.Base=p
    c.Placement=pl2




from PySide import QtGui, QtCore

## Dialog mit einem Dialer zur Postionsbestimmung

def MyDialog(path,target):

    w=QtGui.QWidget()
    w.path=path
    w.target=target

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


    l=QtGui.QLabel("MOVE {}<br>ALONG {}.Edge1".format(target.Label,path.Label))
    box.addWidget(l)


    l=QtGui.QLabel("Position 0 .. 100" )
    box.addWidget(l)

    h=QtGui.QDial()
    
    h.setMaximum(100)
    h.setMinimum(0)
    w.ha=h
    srun(w)

    h.valueChanged.connect(lambda:srun(w))
    box.addWidget(h)

    b=QtGui.QPushButton("Drop copy")
    box.addWidget(b)
    b.clicked.connect(lambda:dropcopy(w))

    w.show()
    return w

## run on the selection
#
# selection is
# 1. animated object,
# 2. path to follow 

def ThousandsOfRunWhatShouldIdo():
    [target,path]=Gui.Selection.getSelection()
    MyDialog(path,target)

# selektion:
# 1. pfad spline
# 2. zu platzierendes objekt

def EndlessMains():
    run()
