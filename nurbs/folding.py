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


# from say import *
import FreeCAD as App
import FreeCADGui as Gui
import Sketcher,Part



import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import time

pyob
from .pyob import  FeaturePython,ViewProvider
#reload (.pyob)


#-------------------------------


class Folding(FeaturePython):
    def __init__(self, obj,uc=5,vc=5):
        FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyInteger","count","config", "count of segments").count=20
        obj.addProperty("App::PropertyInteger","maxi","config", "animation folding")
        obj.addProperty("App::PropertyLink","faceobj","config","face to envelope")
        obj.addProperty("App::PropertyInteger","facenumber","config", "number of the face")
        obj.addProperty("App::PropertyLink","trackobj","config","track for envelope")
        obj.addProperty("App::PropertyLink","arcobj","config","curvature for envelope")
        obj.addProperty("App::PropertyFloat","factor","config", "scale the curvature in percent").factor=100
        obj.addProperty("App::PropertyBool","useSplines","config", "use Spline instead of Polylines").useSplines=True
        obj.addProperty("App::PropertyBool","flipStart","config")


    def attach(self,vobj):
        self.Object = vobj.Object
        self.obj2 = vobj.Object

    def onChanged(self, fp, prop):
        if prop=="count" or prop=="maxi" or prop=="factor":
            try: fp.Shape=fold(fp)
            except: pass

    def execute(self, fp):
        fp.Shape=fold(fp)


def createFolding(obj=None):

    a=App.ActiveDocument.addObject("Part::FeaturePython","Folding")
    Folding(a)
    ViewProvider(a.ViewObject)
    return a




def fold(obj):

    bs=obj.faceobj.Shape.Face1
    track=obj.trackobj.Shape
    cuarcs=obj.arcobj.Shape

    count=obj.count

    pats=cuarcs.discretize(count)
    arcs=[p.y for  p in pats]

    ptsa=[]
    ptsb=[]

    try: curve=track.Curve
    except: curve=track.Edges[0].Curve


    #print track.Edges
    
    tps=track.discretize(count)
#    aa=App.ActiveDocument.addObject("Part::Feature","aa")
#    aa.Shape= Part.makePolygon(tps)
    
    col2=[]
    for p in tps:
            v=curve.parameter(p)
            t=curve.tangent(v)
    #        print (v,t,p)
            n=t[0].cross(App.Vector(0,0,1))
            polg=Part.makePolygon([p+10000*n,p-10000*n])
            col2 += [polg]
            
            ss=bs.makeParallelProjection(polg,App.Vector(0,0,1))
            sps=[v.Point for v in ss.Vertexes]
            #print sps
            if len(sps) == 2:
                ptsa += [sps[0]]
                ptsb += [sps[1]]
            if len(sps) == 1:
                ptsa += [sps[0]]
                ptsb += [sps[0]]

    ppsa=[]
    ppsb=[]

    segments=App.ActiveDocument.getObject("Segments")
    if segments==None:
        segments=App.ActiveDocument.addObject("Part::Feature","Segments")



    comp=[]
    for i,p in enumerate(ptsa):
        if ptsa[i]!=ptsb[i]:
            pol=Part.makePolygon([ptsa[i],ptsb[i]])
            comp.append(pol)
    segments.Shape=Part.Compound(comp)
    #segments.Shape=Part.Compound(col2)


    for i,p in enumerate(ptsa):

        if i<obj.maxi or obj.maxi==0:

            if i==0:
                matrix3=App.Placement(App.Vector(0,0,0),
                    App.Rotation(ptsa[i]-ptsb[i],
                    0.01*obj.factor*arcs[0]),ptsa[i]).toMatrix()
            else:
                matrix3=App.Placement(App.Vector(0,0,0),
                    App.Rotation(ptsa[i]-ptsb[i],
                    0.01*obj.factor*(arcs[i]-arcs[i-1])),ptsa[i]).toMatrix()

        else:
            matrix3=App.Placement().toMatrix()

        a=ptsa[i]
        b=ptsb[i]

        if obj.flipStart:
            if i==len(ptsa)-1 or i==0: a,b=b,a

        ppsa2=[  matrix3.multiply(p) for p in ppsa] + [a]
        ppsa=ppsa2

        ppsb2=[  matrix3.multiply(p) for p in ppsb] + [b]
        ppsb=ppsb2

    if obj.useSplines:
        ca=Part.BSplineCurve()
        ca.interpolate(ppsa)
        cb=Part.BSplineCurve()
        cb.interpolate(ppsb)
        ll=Part.makeLoft([ca.toShape(),cb.toShape()])
    else:
        ll=Part.makeLoft([Part.makePolygon(ppsa),Part.makePolygon(ppsb)])
    return ll



def run():

    ss=Gui.Selection.getSelection()

    folder=createFolding(obj=None)
    folder.faceobj=ss[0]
    folder.trackobj=ss[1]
    folder.arcobj=ss[2]

    App.activeDocument().recompute()
