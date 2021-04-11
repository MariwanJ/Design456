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
#-- create test data for curve approximations
#--
#-- microelly 2017 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import random
import Draft,Part,Points

import FreeCAD as App
import FreeCADGui as Gui

from scipy.signal import argrelextrema
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
#import matplotlib.pyplot as plt

def run():

    #default parameters
    p={
        "count":[1000,'Integer'],
        "radius":[400,'Float'],
        "wave":[100,'Float'],
        "debug":[False,'Boolean'],
    }

    # parameter -----------------
    t=App.ParamGet('User parameter:Plugins/nurbs/'+'genrandomdat')
    l=t.GetContents()
    if l==None: l=[]
    for k in l: p[k[1]]=k[2]
    for k in p:
        if p[k].__class__.__name__=='list':
            typ=p[k][1]
            if typ=='Integer':t.SetInt(k,p[k][0]);
            if typ=='Boolean':t.SetBool(k,p[k][0])
            if typ=='String':t.SetString(k,p[k][0])
            if typ=='Float':t.SetFloat(k,p[k][0])
            p[k]=p[k][0]
    #--------------------

    count=p["count"]
    ri=p["wave"]
    rm=p["radius"]

    kaps=np.random.random(count)*2*np.pi
    mmaa=np.random.random(count)*ri*np.cos(kaps*5)*np.cos(kaps*1.3) + rm

    y= np.cos(kaps) * mmaa
    x=np.sin(kaps) * mmaa
    z=np.zeros(count)

    pps=np.array([x,y,z]).swapaxes(0,1)
    goods=[App.Vector(tuple(p)) for p in pps]

    Points.show(Points.Points(goods))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,0.0,0.0)
    App.ActiveDocument.ActiveObject.ViewObject.PointSize=10

#    Draft.makeWire(goods,closed=True)
