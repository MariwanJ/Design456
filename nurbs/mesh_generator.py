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
#-- test data for sculpter
#--
#-- microelly 2018  0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


##\cond
from PySide import QtGui,QtCore
from say import *
import Design456Init
import FreeCAD
import sys,time
import random

# create a mesh
import Mesh,Points
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    

class ViewProvider:

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class Nurbs:

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj
        obj.addProperty("App::PropertyBool", "autoUpdate", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyInteger", "uc", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyInteger", "vc", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyLink", "parent", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyEnumeration","mode","Base").mode=['poles','interpolate','approximate']


    def attach(self, vobj):
        self.Object = vobj.Object

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def execute(self,obj):
        pass


    def onChanged(self,obj,prop):
        pass

#    def onDocumentRestored(self, fp):
#        self.Object=fp

class Grid:


    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj
        obj.addProperty("App::PropertyBool", "autoUpdate", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyInteger", "uc", "_aux", "automatic update Shape")
        obj.addProperty("App::PropertyInteger", "vc", "_aux", "automatic update Shape")

    def attach(self, vobj):
        self.Object = vobj.Object

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def execute(self,obj):
        pass

    def onChanged(self,obj,prop):
        pass









def createPointGrid(pts,objname="MyGrid",uc=0,vc=0):
    '''create the grid point cloud''' 

    assert(len(pts)==(uc+1)*(vc+1))

    pc=App.ActiveDocument.getObject(objname)
    if pc == None:
        pc = App.ActiveDocument.addObject("Points::FeaturePython",objname)
        Grid(pc)

    ViewProvider(pc.ViewObject)
    pc.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
    pc.Points=Points.Points(pts)
    pc.uc=uc
    pc.vc=vc

    return pc


def createMesh(pts,parentName,parent=None,uc=0,vc=0):
    '''create the mesh representation'''
    d=vc+1
    topfaces=[]
    for x in range(uc):
        for y in range(vc): 
            topfaces.append((d*x+y,(d)*x+y+1,(d)*(x+1)+y))
            topfaces.append(((d)*x+y+1,(d)*(x+1)+y,(d)*(x+1)+y+1))

    t=Mesh.Mesh((pts,topfaces))

    mm=App.ActiveDocument.getObject(parentName+'_M')
    if mm == None:
        mm = App.ActiveDocument.addObject("Mesh::FeaturePython",parentName+'_M')
        mm.addProperty("App::PropertyInteger", "uc", "_aux", "automatic update Shape")
        mm.addProperty("App::PropertyInteger", "vc", "_aux", "automatic update Shape")
        mm.addProperty("App::PropertyLink", "parent", "_aux", "automatic update Shape")

    ViewProvider(mm.ViewObject)
    mm.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
    mm.ViewObject.Lighting="Two side"
    mm.Mesh=t
    mm.parent=parent

    return mm

def createNurbs(pts,parentName,parent=None,uc=0,vc=0):
    '''create the nurbs representation'''

    nu=App.ActiveDocument.getObject(parentName+"_N")
    if nu == None:
        nu = App.ActiveDocument.addObject("Part::FeaturePython",parentName+"_N")
        Nurbs(nu)

    ViewProvider(nu.ViewObject)
    nu.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

    bs=Part.BSplineSurface()
    if nu.mode=='iterpolate':
        bs.interpolate(np.array(pts).reshape(uc+1,vc+1,3))
    elif nu.mode=='poles':
        kv=[1.0/(uc-3+1)*i for i in range(uc-2+1)]
        mv=[4]+[1]*(uc-4+1)+[4]

        ku=[1.0/(vc-3+1)*i for i in range(vc-2+1)]
        mu=[4]+[1]*(vc-4+1)+[4]

        ptskarr=np.array(pts).reshape(uc+1,vc+1,3)
        bs.buildFromPolesMultsKnots(ptskarr, mv, mu, kv, ku, False, False ,3,3)
    else:
        raise Exception("not implemented")
    nu.Shape=bs.toShape()

    nu.parent=parent

    return nu





def modtest():
    '''update the points and the mesh example'''
    
    mm=App.ActiveDocument.getObject(pc.Name+'_M')
    pc=App.ActiveDocument.getObject(pc.Name)
    ptsk=mm.Mesh.Topology[0]
    faces=mm.Mesh.Topology[1]
    ptsk[128].z +=30
    pc.Points=Points.Points(ptsk)

    mm.Mesh=Mesh.Mesh((ptsk,faces))



def gentest():

    #create the testdata
    uc=200
    vc=100

    uc=80
    vc=60

    print ("uc,vc,size",uc,vc,uc*vc)
    z=time.time()
    pts=[]
    for u in range(uc+1):
        for v in range(vc+1):
            pts += [App.Vector(10*u,10*v,0)]

    ptsa=np.array(pts).reshape(uc+1,vc+1,3)

    hills=[
            [100,20,3,40,5,1.0,5],
            [2000,40,5,60,20,0.3,9],
            [2000,32,15,70,20,0.5,5],
            [2000,10,15,50,10,0.2,2],
            [3000,50,10,30,10,0.3,3],
            [2000,40,10,20,10,0.2,2],
        ]

#    hills=[]

    for h in hills:
        [s,y,dy,x,dx,dh,dd]=h
        sample_y = np.random.normal(y, dy, s)
        sample_x = np.random.normal(x, dx, s)
        for i in range(s):
            u=int(round(sample_x[i]))
            v=int(round(sample_y[i]))
            try: ptsa[u-dd:u+dd+1,v-dd:v+dd+1,2] += dh
            except:pass

    pts=[App.Vector(p) for p in np.array(ptsa).reshape((uc+1)*(vc+1),3)]
    a=time.time()
    print ("create data",a-z)
    Gui.updateGui()
    pcl=createPointGrid(pts,objname="MyGrid",uc=uc,vc=vc)
    b=time.time()
    print ("create grid",b-a)
    Gui.updateGui()
    mm=createMesh(pts,pcl.Name,parent=pcl,uc=uc,vc=vc)
    c=time.time()
    print ("create mesh",c-b)
    Gui.updateGui()
    nu=createNurbs(pts,pcl.Name,parent=pcl,uc=uc,vc=vc)
    d=time.time()
    print ("create nurbs",d-c)
    Gui.updateGui()

    import Draft
    points = [App.Vector(58.8695373535,57.1275939941,0.0),
        App.Vector(96.9049606323,188.666870117,0.0),App.Vector(209.426513672,218.778274536,0.0),
        App.Vector(358.398712158,192.62890625,0.0),App.Vector(499.446899414,143.499771118,0.0),
        App.Vector(624.646850586,206.09979248,0.0),App.Vector(680.11529541,388.352996826,0.0),
        App.Vector(581.064575195,518.307495117,0.0),App.Vector(383.755706787,529.401123047,0.0),
        App.Vector(285.497436523,488.196105957,0.0),App.Vector(76.302444458,466.801116943,0.0)]
    spline = Draft.makeBSpline(points,closed=False,face=True,support=None)



# gentest()
