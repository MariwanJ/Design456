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


'''get cut wires or points from a scan point cloud'''
#-*- coding: utf-8 -*-
#-- microelly 2017 v0.2
#-- GNU Lesser General Public License (LGPL)

##\cond

import FreeCAD as App
import FreeCADGui as Gui
import Points,Part,Draft
import os
import Design456Init
try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random
import scipy as sp
from scipy import signal

from PySide import QtGui
import sys,traceback,random,os

import Points

##\endcond

## calculate the aprroximated cut of a point set by a plane
# @param label - label of the created cut
# @param pl - Placement of the cutting plane
# @param pts - points of the pointcloud
# @param showpoints - display the point sets
# @param showwire - create a wire which approximates the point set 
# @param showxywire - create a wire which approximates the point set as mapping in the xy-plane
# @param showxypoints - display the mapping of the point sets into the xy-plane
#
# .


def displayCut(label,pl,pts,showpoints=True,showwire=False,showxypoints=False,showxywire=False):
    ''' display approximation cut of a plane with a point cloud
    '''

    # offset parallel plane
    z0=0
    # distance from the cutting plane
    zmax=0.5
    zmin=-zmax


    color=(random.random(),random.random(),random.random())

    plst=" Base:" + str(pl.Base) +" Rot Euler:" + str(pl.Rotation.toEuler())
    plst="App.Placement(App." + str(pl.Base) +", App.Rotation" + str(pl.Rotation.toEuler())+") "


    plinv=pl.inverse()
    rot2=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),90))
    plinv=rot2.multiply(plinv)
    plaa=plinv.inverse()
    plcc=plaa.multiply(plinv)

# kann weg
#    print ("rotation A"
#    print (" Base:" + str(plinv.Base) +" Rot Euler:" + str(plinv.Rotation.toEuler())
#    print ("rotation B"
#    print (" Base:" + str(plaa.Base) +" Rot Euler:" + str(plaa.Rotation.toEuler())
#    print ("rotation C"
#    print (" Base:" + str(plcc.Base) +" Rot Euler:" + str(plcc.Rotation.toEuler())


    #pts2=[App.Vector(round(p.x),round(p.y),round(p.z)) for p in pts2]
    pts2=[plinv.multVec(p) for p in pts]

    #pts2a=[App.Vector(p.x,p.y,0) for p in pts2 if zmin<=p.z and p.z<=zmax]
    pts2a=[App.Vector(round(p.x),round(p.y),round(p.z)) for p in pts2 if round(p.z)==z0]

    try: scp=App.ActiveDocument.Scanpoints
    except: scp=App.ActiveDocument.addObject("App::DocumentObjectGroup","Scanpoints")
    try: scps=App.ActiveDocument.ScanpointsSource
    except: scps=App.ActiveDocument.addObject("App::DocumentObjectGroup","ScanpointsSource")


    # if no points found - create an empty point set
    if len(pts2a)==0: 

        if showxypoints:
            Points.show(Points.Points([]))
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
            App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
            App.ActiveDocument.ActiveObject.Label="Points Map xy " +plst
            App.ActiveDocument.ActiveObject.Label=label+"t=" +plst + "#"
            App.ActiveDocument.ActiveObject.Label="t=" +plst + "#"
            scp.addObject(App.ActiveDocument.ActiveObject)

        if showpoints:
            Points.show(Points.Points([]))
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
            App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
            App.ActiveDocument.ActiveObject.Label="Points " +plst
            scps.addObject(App.ActiveDocument.ActiveObject)

        return

    else:
        p2=Points.Points(pts2a)

        if showxypoints:
            Points.show(p2)
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
            App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
            App.ActiveDocument.ActiveObject.Label="Points Map xy " +plst
            App.ActiveDocument.ActiveObject.Label=label+"t=" +plst + "#"
            App.ActiveDocument.ActiveObject.Label="t=" +plst + "#"
            scp.addObject(App.ActiveDocument.ActiveObject)


    # create a wire from a central projection
    (px,py,pz)=np.array(pts2a).swapaxes(0,1)
    mymean=App.Vector(px.mean(),py.mean(),pz.mean())
    aps={}
    for v in pts2a:
        vm=v-mymean
    #    print np.arctan2(vm.x,vm.y)
        aps[np.arctan2(vm.x,vm.y)]=v

    kaps=aps.keys()
    kaps.sort()
    ptss=[aps[k] for k in kaps]

    l4=ptss

    # window size for smoothing
    f=5
    path=np.array([l4[0]] * f + l4 + [l4[-1]]*f)
    tt=path.swapaxes(0,1)
    y1 = sp.signal.medfilt(tt[1],f)
    y0 = sp.signal.medfilt(tt[0],f)
    l5=[App.Vector(p) for p in np.array([y0,y1,tt[2]]).swapaxes(0,1)] 

    if showxywire:
        Draft.makeWire(l5)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
        App.ActiveDocument.ActiveObject.Label="Median filter " + str(f)  + " " + plst

    if showwire:
        # place the wire back into the shoe
        invmin=[pl.multVec(p) for p in l5]
        Draft.makeWire(invmin)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
        App.ActiveDocument.ActiveObject.Label="Wire "+ plst

    if showpoints:
        # display the used points inside the shoe
        sels=[plaa.multVec(p) for p in pts2a]
        s2=Points.Points(sels)
        Points.show(s2)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
        App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
        App.ActiveDocument.ActiveObject.Label="Points " +plst
        scps.addObject(App.ActiveDocument.ActiveObject)

    return plaa

## For each rib of the backbone a point set is calculated
#
#  - the starting point cloud is a scanned shoe last asc file
#  - point sets and the corresponding rib sketches are grouped into  folders GRP_1, ...
#  - the folder **ScanpointsSource** contains all point slices  on their real position
#  - the folder **clones2** contains clones of the sketcher ribs on their right position
#
# @param model - name of the shoe model
# @param point_cloud - name of the point cloud document
# @param showpoints - display the point sets
# @param showxywire - create a wire which approximates the point set as mapping in the xy-plane
# @param showxypoints - display the mapping of the point sets into the xy-plane
#
# .

def run(model='shoeAdam', point_cloud='shoe_last_scanned',showpoints=True,showxywire=True,showxypoints=True):
    ''' create slices of the pointcloud near the ribs '''

    try: 
        App.ActiveDocument.getObject(point_cloud)
    except: 
        Points.insert(Design456Init.NURBS_DATA_PATH+point_cloud+".asc","Shoe")


    # load the shoedata
    shoedata
    #reload(shoedata)

    bbps=shoedata.shoeAdam.bbps
    boxes=shoedata.shoeAdam.boxes
    twister=shoedata.shoeAdam.twister
    sc=shoedata.shoeAdam.sc


    trafos=[]
    for i,b in enumerate(bbps):
        # if i!=5 : continue
        alpha=twister[i][1]
        beta=twister[i][2]
        alpha=0
        beta=0

        pla=App.Placement(App.Vector(b),App.Rotation(App.Vector(0,0,1),-beta).multiply(App.Rotation(App.Vector(0,1,0),alpha-90)))
        pcl=App.ActiveDocument.shoe_last_scanned.Points.Points

        trafo=displayCut("cut "+str(i),pla,pcl,showpoints=showpoints,showxywire=showxywire,showxypoints=showxypoints)
        trafos.append(trafo)

    # create the sketches
    createsketchspline
    #reload(.createsketchspline)

    scp=App.ActiveDocument.Scanpoints
    jj=scp.OutList

    clo=App.ActiveDocument.addObject("App::DocumentObjectGroup","clones2")

    for i,p in enumerate(jj):
        
        # move the sketches into the ribs folders
        grp=App.ActiveDocument.addObject("App::DocumentObjectGroup","GRP "+str(i+1))
        try:
            l2=App.ActiveDocument.Profiles.OutList[2].Label
            grp.addObject(jj[i])
            ao=App.ActiveDocument.Profiles.OutList[2]
            grp.addObject(ao)
        except:
            pass

        # place a clone of the ribs into the 3D space 
        try:
            grp.addObject(jj[i])
            obj=App.ActiveDocument.getObject('rib_'+str(i+1))
            grp.addObject(obj)
            skaa=Draft.clone(obj)
            skaa.Placement=trafos[i]
            clo.addObject(skaa)
        except:
            pass

    # display only special objects
    for i in App.ActiveDocument.Objects: i.ViewObject.hide()
    for i in [App.ActiveDocument.shoe_last_scanned] + App.ActiveDocument.clones2.OutList + App.ActiveDocument.ScanpointsSource.OutList:
        i.ViewObject.show()

