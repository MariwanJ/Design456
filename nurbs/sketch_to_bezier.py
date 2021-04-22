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
#-- create a sketch for a closed bezier curves chain
#--
#-- microelly 2018  0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit
import Sketcher,Part
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import time
import random

import pyob
from pyob import  FeaturePython,ViewProvider
#reload (pyob)



class _VP(ViewProvider):
    ''' basic defs '''


    def setupContextMenu(self, obj, menu):
        menu.clear()
        action = menu.addAction("MyMethod #1")
        action.triggered.connect(lambda:self.methodA(obj.Object))
        action = menu.addAction("MyMethod #2")
        menu.addSeparator()
        action.triggered.connect(lambda:self.methodB(obj.Object))
        action = menu.addAction("Edit Sketch")
        action.triggered.connect(lambda:self.myedit(obj.Object))


    def myedit(self,obj):
        self.methodB(None)
        Gui.activeDocument().setEdit(obj.Name)
        obj.ViewObject.show()
        self.methodA(None)

    def methodA(self,obj):
        print ("my Method A")
        App.ActiveDocument.recompute()

    def methodB(self,obj):
        print ("my method B")
        App.ActiveDocument.recompute()

    def methodC(self,obj):
        print ("my method C")
        App.ActiveDocument.recompute()

    def unsetEdit(self,vobj,mode=0):
        self.methodC(None)


    def doubleClicked(self,vobj):
        print ("double clicked")
        self.myedit(vobj.Object)

        print ("Ende double clicked")


def getNamedConstraint(sketch,name):
    '''get the index of a constraint name'''
    for i,c in enumerate (sketch.Constraints):
        if c.Name==name: return i
    print ('Constraint name "'+name+'" not in ' +sketch.Label)
    raise Exception ('Constraint name "'+name+'" not in ' + sketch.Label)



def clearReportView(name):
    from PySide import QtGui
    mw=Gui.getMainWindow()
    r=mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()
    import time
    now = time.ctime(int(time.time()))
    App.Console.PrintWarning("Cleared Report view " +str(now)+" by " + name+"\n")
##\endcond


class BezierSketch(FeaturePython):
    '''Sketch Object with Python for Bezier Curve'''

    ##\cond
    def __init__(self, obj, icon=NURBSinit.ICONS_PATH+'draw.svg'):
        obj.Proxy = self
        self.Type = self.__class__.__name__
        self.obj2 = obj
        self.aa = None
        obj.addProperty("App::PropertyInteger",'polescount',).polescount=12
        obj.addProperty("App::PropertyBool",'init')
        _VP(obj.ViewObject)
    ##\endcond


    def execute(proxy,obj):
        obj.Shape=run(obj)


def run(sk):

    gc=sk.GeometryCount
    ap=gc/3
    print ("geometry count, poles, constraints count",gc,ap,sk.ConstraintCount)

    try:
        if sk.init:
            if sk.ConstraintCount <= 150:
                for i in range(ap-1):
                    rc=sk.addConstraint(Sketcher.Constraint('Parallel',3*i+3,3*i+2))
#                    sk.setVirtualSpace(rc, True)
                    sk.solve()

            rc=sk.addConstraint(Sketcher.Constraint('Parallel',gc-1,0))
#            sk.setVirtualSpace(rc, True)

            sk.init=False

            for i in range(90):
                # must become parameteric, depends on the number sk.polescount
                #if i in [2,3,8,9,15,16,]: # for 3
                # if i in [0,1,6,7,13,14,19,20]: # for 5
                if i in [0,1, 6,7, 13,14, 20,21, 27,28, 34,35, 41,42, 47,48 ]: # for 7
                    sk.setDriving(i,False)
                    sk.setVirtualSpace(i, True)

            jj=sk.addConstraint(Sketcher.Constraint('Distance',0,10))
            sk.setDriving(jj,False)
            sk.setVirtualSpace(jj, True)

            jj=sk.addConstraint(Sketcher.Constraint('Distance',20,10))
            sk.setDriving(jj,False)
            sk.setVirtualSpace(jj, True)
            print ("done")

    except: pass

#    for c in range(sk.ConstraintCount):
#        sk.setVirtualSpace(c, True)

    try:
        #poles=[ sk.getPoint(i,1) +App.Vector(0,0,random.random()*2000) for i in range(sk.polescount)]
        #poles=[ sk.getPoint(i,1) +App.Vector(0,0,0) for i in range(sk.polescount*3)]

        # gleich doppelte Punkte
        poles=[]
        for i in range(sk.polescount*3):
            p=sk.getPoint(i,1)
            if i%3== 0:
                poles += [p,p,p] # corner pole -- multiplicity 3
            else:
                poles += [p] # tangent pole

        cc=Part.BSplineCurve(poles+[poles[0]])
        return cc.toShape()
    except:
        return Part.Shape()


def init_bezierring(sk,count=5,source=None):


    if source != None:
        ptsa=source.Shape.Wires[0].discretize(count*2*10)
        ptsb=[]

        # read some exact point p for the pole and a approx tangent p2-p, pv-p for the tangent indicators
        for n in range(count):
            p=ptsa[2*n*10]
            p2=p+ (ptsa[2*n*10+1]-p).normalize()*10
            pv=p+((p-p2).normalize())*(10)
            if n==0:
                last=pv
                ptsb += [p,p2]
            else:
                ptsb += [pv,p,p2]

        # the tangent from the first pole
        ptsb += [last]

        # map from xz scan to xy sketch
        pts=[App.Vector(p.x,p.z,0) for p in ptsb]

    else: # a generated circle with some noise
        r=100
        pts=[]
        for i in range(count):
            p=App.Vector(r*np.cos(2*i*np.pi/count),r*np.sin(2*i*np.pi/count),0)
            p2=App.Vector(r*np.cos((2*i+1)*np.pi/count),r*np.sin((2*i+1)*np.pi/count),0)
            p2 += App.Vector((0.5-random.random())*0.2*r,(0.5-random.random())*0.2*r)
            pm=(p+p2)*0.5
            pts +=[p,pm,p2]

    for i in range(count):
            if i != 0: # connect to the last segment with a connector line
                lc=sk.addGeometry(Part.LineSegment(pts[3*i-1],pts[3*i]),False)
                sk.addConstraint(Sketcher.Constraint('Coincident',lb,2,lc,1))

            la=sk.addGeometry(Part.LineSegment(pts[3*i],pts[3*i+1]),False)
            lb=sk.addGeometry(Part.LineSegment(pts[3*i+1],pts[3*i+2]),False)

            if 1: # avoid moving of points
                p2=sk.getPoint(lb,1)
                cc=sk.addConstraint(Sketcher.Constraint('DistanceX',lb,1,p2.x))
                sk.addConstraint(Sketcher.Constraint('DistanceY',lb,1,p2.y))
                sk.renameConstraint(cc, u'aa ' + str(i))
                p2=sk.getPoint(la,1)
                cc=sk.addConstraint(Sketcher.Constraint('DistanceX',la,1,p2.x))
                sk.addConstraint(Sketcher.Constraint('DistanceY',la,1,p2.y))
                sk.renameConstraint(cc, u'bb ' + str(i))

            # blocking does not work (unsolvable by sketcher) why?
#            sk.addConstraint(Sketcher.Constraint('Block',lb))
            sk.addConstraint(Sketcher.Constraint('Coincident',la,2,lb,1))

            if i != 0: # connect connector line to the new created segment
                sk.addConstraint(Sketcher.Constraint('Coincident',lc,2,la,1))

    # close the figure
    # the last connector
    la=sk.addGeometry(Part.LineSegment(pts[3*i],pts[0]),False)
    p2=sk.getPoint(la,1)
    cc=sk.addConstraint(Sketcher.Constraint('DistanceX',la,1,p2.x))
    sk.addConstraint(Sketcher.Constraint('DistanceY',la,1,p2.y))
    sk.renameConstraint(cc, u'cc ' + str(i))

    # connect head and foot
    sk.addConstraint(Sketcher.Constraint('Coincident',lb,2,la,1))
    sk.addConstraint(Sketcher.Constraint('Coincident',la,2,0,1))


def createBezierSketch(name="BezierRing",source=None):

    if source != None:
        name="Sk_"+source.Label+'_'

    obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
    BezierSketch(obj)
    obj.polescount=7
    init_bezierring(obj,count=obj.polescount,source=source)
    obj.init=True
    return obj

def createBezierRingSketch(name="BezierRing",source=None):
    return createBezierSketch(name,source)




import time

class FollowerSketch(FeaturePython):
    '''Sketch Object with Python which puts one point (by named constraints) onto a wire'''

    ##\cond
    def __init__(self, obj, icon=NURBSinit.ICONS_PATH+'draw.svg'):
        obj.Proxy = self
        self.Type = self.__class__.__name__
        self.obj2 = obj
        self.aa = None
        obj.addProperty("App::PropertyBool",'init')
        _VP(obj.ViewObject)
        self.timestamp=time.time()
    ##\endcond


    def onChanged(self, obj, prop):
        print ("onChange", prop)
        if len(obj.Geometry)==0: return
        if not obj.init:return

        if time.time()-self.timestamp<0.1 and prop!="force":
            return
        self.timestamp=time.time()


        if prop=='Geometry' or prop=="force":
            print ("Anpassen")
            try:
                print (obj.getPoint(0,1))
            except:
                print ("noch nix da")

                return
            p=obj.getPoint(0,1)
            c=App.ActiveDocument.BSpline.Shape.Curve
            u=c.parameter(p)
            print ("versuche zu setzen")

            p2=c.value(u)

            print (p)
            print (p2)
            print ("##")
            obj.movePoint(0,1,p2)
            # constraints einschalten hier haRD CODED
            ax=getNamedConstraint(obj,"ax")
            ay=getNamedConstraint(obj,"ay")

            App.ActiveDocument.Sketch.setDriving(ax,True)
            App.ActiveDocument.Sketch.setDriving(ay,True)
            obj.setDatum(ax,p2.x)
            obj.setDatum(ay,p2.y)
            obj.solve()
            App.ActiveDocument.Sketch.setDriving(ax,False)
            App.ActiveDocument.Sketch.setDriving(ay,False)
            # auschcalten
            print ("finished")



    def execute(proxy,obj):
        print ("execute")
        obj.recompute()


def createFollowerSketch(name="Follower",source=None):

    if source != None:
        name="Sk_"+source.Label+'_'

    obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
    FollowerSketch(obj)
    import sketcher
    import sketcher.feedbacksketch
    #reload(sketcher.feedbacksketch)
    sketcher.feedbacksketch.copySketch(App.ActiveDocument.Sketch,obj)

    obj.init=True
    time.sleep(0.2)
    obj.Proxy.onChanged(obj,"Geometry")
    App.ActiveDocument.recompute()
    return obj





class ArcSketch(FeaturePython):
    '''Sketch Object with Python to create two smoothing arcs''' 

    ##\cond
    def __init__(self, obj, icon=NURBSinit.ICONS_PATH+'draw.svg'):
        obj.Proxy = self
        self.Type = self.__class__.__name__
        self.obj2 = obj
        self.aa = None
        obj.addProperty("App::PropertyBool",'init')
        obj.addProperty("App::PropertyBool",'displayFirst')
        obj.addProperty("App::PropertyBool",'displayLast')
        obj.addProperty("App::PropertyLink",'source')
        obj.addProperty("App::PropertyInteger",'countArcs').countArcs=2

        _VP(obj.ViewObject)
        self.timestamp=time.time()
    ##\endcond


    def onChanged(self, obj, prop):
        #print ("onChange", prop)
        pass

    def execute(proxy,obj):
        sk=obj.source
        obj.deleteAllGeometry()
        if obj.displayFirst:
            obj.addGeometry(sk.Geometry[0])
        for i in range(obj.countArcs+1):
            obj.addGeometry(sk.Geometry[1+3*i])

        if obj.displayLast:
            obj.addGeometry(sk.Geometry[3*obj.countArcs+2])



        def run(ag,bg):

            try:
                p2=sk.getPoint(ag,1)
                p0=sk.getPoint(bg,2)
                ps=sk.getPoint(ag,2)
            except:
                print ("points not found")
                return

            alpha=np.arccos((p2-ps).normalize().dot((p0-ps).normalize()))
            radius=(p2-ps).Length*np.tan(alpha*0.5)

            print ("Richtung ", (p2-ps).normalize().dot((p0-ps).normalize()))

            vv=(p2-ps).normalize().cross((p0-ps).normalize())

            f= vv.z< 0

            if not f:
                mp=p2-(p2-ps).normalize().cross(App.Vector(0,0,1))*radius
            else:
                mp=p2+(p2-ps).normalize().cross(App.Vector(0,0,1))*radius

            r2=(p2-mp)
            r0=(p0-mp)
            w1=np.arctan2(r2.y,r2.x)
            w2=np.arctan2(r0.y,r0.x)

            if not f:
                w1,w2=w2,w1

            cc=obj.addGeometry(Part.ArcOfCircle(Part.Circle(mp,
            App.Vector(0,0,1),radius),w1,w2),False)
            obj.solve()

        run(2,3)

        if obj.countArcs>1:
            run(5,6)

        if obj.countArcs>2:
            run(8,9)

        obj.recompute()


def createArcSketch(name="TwoArc",source=None):

    try:
        if source == None:
            source=Gui.Selection.getSelectionEx()[0]
    except:
        pass

    if source != None:
        name="Sk_"+source.Label+'_'

    obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
    ArcSketch(obj)
    obj.source=source
    obj.init=True
    time.sleep(0.2)

    obj.Proxy.onChanged(obj,"Geometry")
    App.ActiveDocument.recompute()
    return obj

#-----------------------


def createLabel(obj,ref,ctext):

    l = Draft.makeLabel(
    target=(obj,ref),
    direction='Horizontal',distance=.0,
    labeltype='Custom',
    )

    l.CustomText = ctext
    l.Label=l.CustomText[0]
    print (l.Target[1][0])

    ##-----------------------
    #com=l.Target[0].Shape.CenterOfMass
    com=l.Target[0].Shape.BoundBox.Center

    xmin=l.Target[0].Shape.BoundBox.XMin

    l.CustomText = ctext
    l.Label=l.CustomText[0]
    print (l.Target[1][0])

    if l.Target[1][0].startswith("Edge") or l.Target[1][0].startswith("Fac") :
        print ("a")
        pp=getattr(l.Target[0].Shape,l.Target[1][0]).CenterOfMass
        l.TargetPoint=getattr(l.Target[0].Shape,l.Target[1][0]).CenterOfMass
    else:
        print ("b")
        pp=getattr(l.Target[0].Shape,l.Target[1][0]).Point
        l.TargetPoint=getattr(l.Target[0].Shape,l.Target[1][0]).Point

    l.Placement.Base = pp
#    l.Placement.Base.x=l.Target[0].Shape.BoundBox.XMax +20
#    l.Placement.Base.y=l.Target[0].Shape.BoundBox.YMax +20
#    l.Placement.Base.z=l.Target[0].Shape.BoundBox.ZMax +20
    l.Placement.Base += (pp-com)*1.5
    diff=(pp-com)
    if diff.x < 0:
        l.StraightDistance = 1
    else:
        l.StraightDistance = -1

#----------------------------------------

    l.ViewObject.TextSize = '16 mm'
    l.ViewObject.DisplayMode =  "2D text"
    l.ViewObject.TextAlignment = "Top"

# labesl for the arc creation task template
import Draft
def createLabels():

    obj=App.ActiveDocument.Sketch
    dat=[
        ['Vertex1',['extern ref start',]],
        ['Vertex2',['extern ref end',]],
        ['Vertex3',['start arc 1',]],
        ['Vertex4',['tangent pole arc 1',]],
        ['Vertex5',['end arc 1',]],

        ['Vertex6',['start arc 2',]],
        ['Vertex7',['tangent pole arc 2',]],
        ['Vertex8',['end arc 2',]],

        ['Vertex9',['extern ref 2 start',]],
        ['Vertex10',['extern ref 2 end',]],

        ['Edge2',['line connector to extern 1',]],
        ['Edge5',['line connector of the arcs',]],
        ['Edge8',['line connector to extern 2',]],

    ]


    for d  in dat:
        createLabel(obj,d[0],d[1])

def createLabels():

#    obj=App.ActiveDocument.Sketch
    for obj in Gui.Selection.getSelectionEx():
        dat=[]
        for i,e in enumerate(obj.Shape.Vertexes):
            dat += [[ "Vertex"+str(i+1), ["V "+str(i+1) + " @ " + obj.Label]]]
        for i,e in enumerate(obj.Shape.Edges):
            dat += [[ "Edge"+str(i+1), ["E "+str(i+1) + " @ " + obj.Label]]]
        for i,e in enumerate(obj.Shape.Faces):
            dat += [[ "Face"+str(i+1), ["F "+str(i+1) + " @ " + obj.Label]]]


        for d  in dat:
            createLabel(obj,d[0],d[1])





def updateLabels():

    for l in Gui.Selection.getSelectionEx():
        if l.Target[1][0].startswith("Edge"):
            l.TargetPoint=getattr(l.Target[0].Shape,l.Target[1][0]).CenterOfMass
        else:
            l.TargetPoint=getattr(l.Target[0].Shape,l.Target[1][0]).Point





def ThousandsOfMainFunction():

#    createBezierRingSketch()
#    obj=createFollowerSketch()

    obj=createArcSketch()
