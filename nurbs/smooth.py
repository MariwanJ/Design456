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

#-----------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- taubin smooth for wire
#--
#-- microelly 2018 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtCore,QtGui
from pivy import coin
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import random
import Draft
import os


Gui=FreeCADGui
import Part

class PartFeature:
    ''' base class for part feature '''
    def __init__(self, obj):
        obj.Proxy = self

# grundmethoden zum sichern

    def attach(self,vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class ViewProvider:
    ''' view provider class for Tripod'''
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def onDelete(self, obj, subelements):
        print ("on Delete ")
        return True

    def onChanged(self, obj, prop):
            print ("onchange",prop)




#---------------------


def runtaubin(obj):
    try:
        obj.Wire
    except:
        return

#    print obj
#    print obj.Shape
    if obj.discretizeCount == 0:
        pts=[v.Point for v in obj.Wire.Shape.Vertexes]
        #pts=obj.Wire.Points
#        print pts
        if len(pts)==2:
            pts=obj.Wire.Shape.Edge1.discretize(obj.discretizeCount)
    else:
        try: pts=obj.Wire.Shape.discretize(obj.discretizeCount)
        except: pts=obj.Wire.Shape.Wire1.discretize(obj.discretizeCount)
    
    
    qts=np.array(pts)

    for j in range(obj.count):
        
        a=len(pts)
        if j%2==0:
            f=0.01*obj.pf
        else:
            f=-0.01*obj.pf2

        if obj.end==0:
            mend=obj.discretizeCount-1
        else:
            mend=obj.end
        for i in range(obj.start,mend):
            qts[i] += f*(pts[i-1]+pts[i+1]-2*pts[i])

        #pts=np.array(qts)
        pp=[App.Vector(p) for p in qts]


    drawtracks(pts,pp,"Diff_for_"+str(obj.Name))

    if obj.createBSpline:
        if obj.closeBSpline:
            qq=[(pp[0]+pp[-1])*0.5]+pp[1:-1]+[(pp[0]+pp[-1])*0.5]
            obj.Shape=Part.BSplineCurve(qq).toShape()
        else:
            obj.Shape=Part.BSplineCurve(pp).toShape()
    else:
        obj.Shape=Part.makePolygon(pp)        

#    App.activeDocument().recompute()




class Taub(PartFeature):
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyInteger","pf","smooth").pf=30
        obj.addProperty("App::PropertyInteger","pf2","smooth").pf2=30
        obj.addProperty("App::PropertyInteger","count").count=40
        obj.addProperty("App::PropertyInteger","start").start=1
        obj.addProperty("App::PropertyInteger","end").end=0
    
        obj.addProperty("App::PropertyLink","Wire")
        obj.addProperty("App::PropertyBool","createBSpline","smooth")
        obj.addProperty("App::PropertyBool","closeBSpline","smooth")
        obj.addProperty("App::PropertyInteger","discretizeCount").discretizeCount=30
        
        
    
    def onChanged(self, obj, prop):
            print ("onchange--",prop)
            if prop in ["pf","pf2",'count','discretizeCount','start','end','createBSpline']:
                print ("Aktualisierebn")
                runtaubin(obj)



def smoothWire(sel=None,name=None):
    if name == None:
        name= "smooth"
    a=App.ActiveDocument.addObject("Part::FeaturePython",name)
    Taub(a,"Smooth")
    #a.Wire=App.ActiveDocument.DWire
    if sel !=None:
        a.Wire=sel
    else:
        try: a.Wire=Gui.Selection.getSelection()[0]
        except: pass

    ViewProvider(a.ViewObject)
    a.ViewObject.LineColor=(1.,1.,0.)
    a.ViewObject.PointColor=(0.5,0.,0.)
    a.ViewObject.PointSize=6
    a.ViewObject.LineWidth=1
    runtaubin(a)


# 3D smooth
import Mesh

def run3D(self,mobj):
    import time
    #m=App.ActiveDocument.K147909
    #=a.Source.Mesh

    try:
        mobj.Source
    except:
        return


    mobj.Source.ViewObject.hide()
#    obj=App.ActiveDocument.copyObject(App.ActiveDocument.K147909)
#    obj.ViewObject.hide()
#    self.bob=obj

#    m=obj.Mesh
    m=mobj.Source.Mesh
    m=m.copy()

    if 1:
        i=mobj.Iterations
        print ("iterations ",i)
        print (mobj.Lambda)
        print ("------------------")
        
        m.smooth(Method="Taubin",Iteration=i,Lambda=mobj.Lambda*0.01,Micro=mobj.Micro*0.01)
#        import Mesh
        #    App.ActiveDocument.ActiveObject.ViewObject.hide()
        #Mesh.show(m)
        #App.ActiveDocument.ActiveObject.Placement.Base=App.Vector(15*i,10,-10*i)
        mobj.Mesh=m
        Gui.updateGui()
        #time.sleep(0.1)

class TaubM(PartFeature):
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

#        obj.addProperty("App::PropertyInteger","pf","smooth").pf=30
#        obj.addProperty("App::PropertyInteger","pf2","smooth").pf2=30
        obj.addProperty("App::PropertyInteger","Iterations").Iterations=40
        obj.addProperty("App::PropertyFloat","Lambda").Lambda=50
        obj.addProperty("App::PropertyFloat","Micro").Micro=1
#        obj.addProperty("App::PropertyInteger","start").start=1
#        obj.addProperty("App::PropertyInteger","end").end=30

        obj.addProperty("App::PropertyLink","Source")
#        obj.addProperty("App::PropertyBool","createBSpline","smooth")
#        obj.addProperty("App::PropertyInteger","discretizeCount").discretizeCount=30


    def onChanged(self, obj, prop):
            print ("onchange",prop)
            if prop in ['Iterations','Lambda','Micro']:
                run3D(self,obj)


    
def smoothMesh():
    a=App.ActiveDocument.addObject("Mesh::FeaturePython","Meshsmooth")
    TaubM(a,"Smooth")
    # a.Mesh=App.ActiveDocument.DWire
    # a.Source=App.ActiveDocument.K147909
    a.Source=Gui.Selection.getSelection()[0]
    ViewProvider(a.ViewObject)
    run3D(None,a)


#---------------




def splitMesh():
    ribc=40
    merc=601

    pixl=[0,10,20,30,31,50,60]

    rstep=10
    rstep=10
    ribrange=range(ribc)
    ribrange=range(1,25)
    
    #ribrange=[13,14,15,16,17]

    #ribrange=[10]

    import Mesh
    #Gui.activateWorkbench("MeshWorkbench")

    Gui.activateWorkbench("MeshWorkbench")
    import MeshPartGui, FreeCADGui
#    FreeCADGui.runCommand('MeshPart_TrimByPlane')
    Gui.activateWorkbench("NurbsWorkbench")

    plane=App.ActiveDocument.addObject("Part::Plane","Plane")
    #>>> App.ActiveDocument.Plane.Length=10.000
    #>>> App.ActiveDocument.Plane.Width=10.000

    ptsa=[]

    #s=App.ActiveDocument.K147908
    s=Gui.Selection.getSelection()[0]

    ribs=[]
    #ribc
    for i  in ribrange:

        start=round(s.Mesh.BoundBox.YMin)+5
        pos=int(start+i*rstep)
        if pos>s.Mesh.BoundBox.YMax:
            App.ActiveDocument.removeObject(plane.Name)
            return
        pm=App.Placement(App.Vector(0,pos,0.000),
            App.Rotation(App.Vector(1.000,0.000,0.000),90.000))
        plane.Placement=pm



        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(plane)
        Gui.Selection.addSelection(s)




        '''
        plane.Placement.App.z =   s.Mesh.BoundBox.ZMax

        for i in range(80):
            plane.Placement.App.z -=  2
            FreeCADGui.runCommand('MeshPart_SectionByPlane')

        '''


        FreeCADGui.runCommand('MeshPart_SectionByPlane')
        # FreeCADGui.runCommand('MeshPart_SectionByPlane')

        pp=plane.Placement.inverse()

        if 0:
            rc=App.ActiveDocument.ActiveObject
            rc.Placement=pp
            rc.Shape.Edges

            import Draft
            ptsw=[v.Point for v in rc.Shape.Wires[0].Vertexes]
            # Draft.MakeBSpline(ptsw)



        rc=App.ActiveDocument.ActiveObject
        rc.Label="Section y="+ str(pos)
        rc.ViewObject.LineColor=(0.3,0.3,1.0)
        rc.ViewObject.LineWidth=6
        Gui.updateGui()
        pts=rc.Shape.Wires[0].discretize(merc)
        ptsa += [pts]

        if 0: # spaeter
            sk=App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
            sk.addGeometry(Part.Circle(App.Vector(0.,0.,0),App.Vector(0,0,1),50),False)
            sk.Placement=pm

#        import sketch_to_bezier
#        #reload (sketch_to_bezier)
#        sk=sketch_to_bezier.createBezierSketch(name="Arc",source=rc)
#        sk.Placement=pm
#        ribs +=[sk]





    if 0:
        if len(ribrange)>1:
            loft=App.ActiveDocument.addObject('Part::Loft','Loft')
            loft.Sections=ribs
            loft.ViewObject.Transparency=70
            loft.ViewObject.DisplayMode = u"Shaded"
            for r in ribs:
                r.ViewObject.hide()


    if 1: # speater

        import os

        ribs2=[]

        ptsa=np.array(ptsa)

        '''
        ptsb=[]

        p0=App.Vector()
        p1=p0
        import Draft
        for pts in ptsa:
            ij=0
            mj=10**10
            pps=[App.Vector(p) for p in pts]
            for i,p in enumerate(pps):
                if (p-p0).Length<mj:
                    mj=(p-p0).Length
                    ij=i
            pps2=pps[ij:] +pps[:ij]
            

            p0=pps[ij]
            if (pps2[1]-p1).Length>(pps2[-1]-p1).Length:
                pps2.reverse()

            p1=pps2[1]
            ptsb += [pps2]    
            print ij
        '''

        ptsb=[]
        ribs=[]

        p0=App.Vector()
        p1=p0
        zmax=0
        import Draft
        print ("umsortieren")
        for pts in ptsa:
            ij=0
            mj=10**10
            xmi=10**10
            pps=[App.Vector(p) for p in pts]
            for i,p in enumerate(pps):
                if p.x<xmi:
                    ij=i
                    xmi=p.x
                    p1=p
            pps2=pps[ij:] +pps[:ij]


            if (pps2[1].z-pps2[0].z)<=0:
                print ("!!")
                pps2.reverse()

            p1=pps2[1]
            ptsb += [pps2]
            print (ij)
            rcc=Draft.makeWire(pps2)

            pos=pts[0][1]
            pm=App.Placement(App.Vector(0,pos,0.000),
                App.Rotation(App.Vector(1.000,0.000,0.000),90.000))
            plane.Placement=pm


            import sketch_to_bezier
            #reload (sketch_to_bezier)
            sk=sketch_to_bezier.createBezierSketch(name="Arc",source=rcc)
            sk.Placement=pm
            ribs +=[sk]






        if 0:

            ptsb=np.array(ptsb).swapaxes(0,1)

            for pix in pixl:
                print (pix)
                pts=ptsb[pix*10]
                ij=0
                mj=10**10
                pps=[App.Vector(p) for p in pts]
                _=Draft.makeWire(pps)
                ribs2 += [_]


    if 0:
        if len(ribrange)>1:
            loft=App.ActiveDocument.addObject('Part::Loft','LoftYY')
            loft.Sections=ribs
            loft.ViewObject.Transparency=70
            loft.ViewObject.DisplayMode = u"Shaded"
            for r in ribs:
                r.ViewObject.hide()

    App.ActiveDocument.removeObject(plane.Name)

#--------------------------------
# schicht aus mesh schneiden - von splitmesh vereinfacht

# https://autrimncpa.wordpress.com/bhairavi/

def sliceMeshbySketch():


    [s,sk]=Gui.Selection.getSelection()
    if s.TypeId != 'Mesh::Feature':
        s,sk=sk,s

    try:
        DatumPlane=sk.Support[0][0]
    except:
        DatumPlane=sk



    import Mesh
    import Draft

    pma=DatumPlane.Placement.copy()
    ddB=pma.Rotation.multVec(App.Vector(0,0,50))
    ddA=pma.Base
    mesh=s.Mesh

    cs = mesh.crossSections([(ddA,ddB)],0.01)
    ptsW=[App.Vector(p) for p in cs[0][0]]
    print  (len(ptsW))
    import Draft
    pol=Part.makePolygon(ptsW)
    ptsW=pol.discretize(20)
    
    rcc=Draft.makeWire(ptsW)

    if 0:
        import sketch_to_bezier
        #reload (sketch_to_bezier)
        sk=sketch_to_bezier.createBezierSketch(name="Arc",source=rcc)

    s.ViewObject.hide()
    DatumPlane.ViewObject.hide()



#--------------------------------

def distanceCurves():
    pass

    [a,b]=Gui.Selection.getSelection()
    #a.Shape.Wires
    #b.Shape.Wires

    anz=200
    ptsa=a.Shape.Wires[0].discretize(anz)
    ptsb=b.Shape.Wires[0].discretize(anz)
    ls=0
    for p,q in zip(ptsa,ptsb):
        ls += (p-q).Length
    
    print ("Distance ",a.Label,b.Label,ls/anz)



#---------------------




## create the inventor string for the colored wire

def genbuffer(pts,color=0):
    '''create the inventor string for the colored wire
    pts - list of points
    colors - list of color indexes
    '''

    colix=""
    pix=""
    cordix=""
    for i,p in enumerate(pts):
        if i>0:
            #if colors==None:colix += " "+str(random.randint(0,7))
            #else:
            #    colix += " "+str(colors[i])
            colix += " "+str(color)
        pix += str(p.x)+" "+str(p.y) +" " +str(p.z)+"\n"
        if i>0:cordix +=  str(i-1)+" "+str(i)+" -1\n" 

    buff ='''#Inventor V2.1 ascii
    Separator {
        Transform {
            translation 0 0 0
            rotation 0 0 1  0
            scaleFactor 1 1 1
            center 0 0 0
        }
        Separator {
            VRMLGroup {
                children 
                VRMLShape {
                    geometry 
                        VRMLIndexedLineSet {
                            coord 
                                VRMLCoordinate {
                                    point 
    '''

    buff += " [" + pix + "]}\n"

    buff +='''
                        color 
                            VRMLColor {
                                color [ 0 0 0, 1 0 0, 0 1 0,
                                        0 0 1, 1 1 0, 0 1 1, 1 0 1 , 1 1 1,
                                    ]
                              }
                        colorPerVertex FALSE
    '''

    buff += "colorIndex [" + colix + "]\n"
    buff += "coordIndex [" + cordix + "]\n"
    buff += "}}}}}"

    return buff


def drawtracks(ptsa,ptsb,name='ColorPath'):
    '''create a vrml indexed color path as an inventor object'''

    iv=App.ActiveDocument.getObject(name)
    if iv==None:iv=App.ActiveDocument.addObject("App::InventorObject",name)

    ls=[]
    n=App.Vector()
    for p,q in zip(ptsa,ptsb):
#        print q-p
        ls += [p,p+(q-p)*20,p]

    iv.Buffer=genbuffer(ls,8)


