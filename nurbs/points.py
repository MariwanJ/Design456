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

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit
import Sketcher,Part
import Draft



try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import time
import Mesh
import random
import time

# point limbach oberfrohna
# http://www.landesvermessung.sachsen.de/inhalt/produkte/dhm/dgm/dgm_download.html

# utm 56.373500, 34.32500 
# lat lon 50.865968,12.772980

# bayern bruck
# 48.0211686,11.905581
# https://www.ldbv.bayern.de


def toUVMesh(bs, uf=5, vf=5):
        print ("los")
        uc=uf*bs.NbUPoles
        vc=vf*bs.NbVPoles
        ss=[]
        for x in range(uc+1): 
            for y in range(vc+1): 
                ss.append(bs.value(1.0/uc*x,1.0/vc*y))

        randfaces=[]
        for x in [0,uc]:
            for y in range(vc+1): 
                randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
                vek=bs.value(1.0/uc*x,1.0/vc*y)
                ss.append (vek)
                veks=App.Vector(vek.x,vek.y,-100)
                ss.append (veks)

        for y in [0,vc]:
            for x in range(uc+1): 
                randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
                vek=bs.value(1.0/uc*x,1.0/vc*y)
                ss.append (vek)
                veks=App.Vector(vek.x,vek.y,-100)
                ss.append (veks)

        randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
        for x in [0,uc]:
            for y in [0,vc]:
                vek=bs.value(1.0/uc*x,1.0/vc*y)
                veks=App.Vector(vek.x,vek.y,-100)
                ss.append (veks)

        scaler=1
        sst=[scaler*v for v in ss]
        ss=sst

        t=Mesh.Mesh((ss,randfaces[-2:]))
        faces1 = randfaces[:2*vc]+randfaces[2*vc+2:4*vc+2]+randfaces[4*vc+4:4*vc+2*uc+4]
        faces1 += randfaces[4*vc+2*uc+6:4*vc+4*uc+6] + randfaces[-2:]
        t=Mesh.Mesh((ss,faces1))
        Mesh.show(t)
        App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"

        faces=[]
        for x in range(uc): 
            for y in range(vc): 
                #if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
                #if len(faces)<100000:
                    faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
                    faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

        print ("hu")
        # print ss
        # print faces
        App.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
        App.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
        App.Console.PrintMessage(str(("faces:",len(faces)))+"\n")


        t=Mesh.Mesh((ss,faces+faces1))
        #t=Mesh.Mesh((ss,faces))
        Mesh.show(t)
        App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
        App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
        App.Console.PrintMessage(str(t))


        print (uc,vc)
        return t


def PointarrayToMesh(par, uf=5, vf=5,h=1100):
        print ("los")
        uc,vc,_=par.shape
        uc -= 1 
        vc -= 1
        print (uc,vc)
        ss=[]
        for x in range(uc+1): 
            for y in range(vc+1): 
                ss.append(App.Vector(par[x,y]))

        randfaces=[]
        if 10:
            for x in [0,uc]:
                for y in range(vc+1): 
                    randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
                    vek=App.Vector(par[x,y])
                    ss.append (vek)
                    veks=App.Vector(vek[0],vek[1],h)
                    ss.append (veks)

            for y in [0,vc]:
                for x in range(uc+1): 
                    randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
                    vek=par[x,y]
                    vek=App.Vector(par[x,y])
                    ss.append (vek)
                    veks=App.Vector(vek[0],vek[1],h)
                    ss.append (veks)

            randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
            for x in [0,uc]:
                for y in [0,vc]:
                    vek=par[x,y]
                    vek=App.Vector(par[x,y])
                    veks=App.Vector(vek[0],vek[1],h)
                    ss.append (veks)

        scaler=1
        sst=[scaler*v for v in ss]
        ss=sst

        t=Mesh.Mesh((ss,randfaces[-2:]))
        faces1 = randfaces[:2*vc]+randfaces[2*vc+2:4*vc+2]+randfaces[4*vc+4:4*vc+2*uc+4]
        faces1 += randfaces[4*vc+2*uc+6:4*vc+4*uc+6] + randfaces[-2:]
        t=Mesh.Mesh((ss,faces1))
        #Mesh.show(t)
        # App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"

        faces=[]
        for x in range(uc): 
            for y in range(vc): 
                #if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
                #if len(faces)<100000:
                    faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
                    faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

        print ("hu")
        # print ss
        # print faces
        App.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
        App.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
        App.Console.PrintMessage(str(("faces:",len(faces)))+"\n")

        t=Mesh.Mesh((ss,faces+faces1))
        #t=Mesh.Mesh((ss,faces))
        Mesh.show(t)
        App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
        #App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
        App.Console.PrintMessage(str(t))


        print (uc,vc)
        return t

if 0:
    bs=App.ActiveDocument.Nurbs.Shape.Face1.Surface

    # bs=App.ActiveDocument.Shape.Shape.Face1.Surface

    print (bs)

    t=toUVMesh(bs, uf=10, vf=10)


    print ("dine")
    print (t)




def machFlaeche(psta,ku=None,objName="XXd",degree=3):
        NbVPoles,NbUPoles,_t1 =psta.shape


        ps=[[App.Vector(psta[v,u,0],psta[v,u,1],psta[v,u,2]) for u in range(NbUPoles)] for v in range(NbVPoles)]

#        kv=[1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
#        if ku==None: ku=[1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]


        kv=[1.0/(NbVPoles-degree)*i for i in range(NbVPoles-degree+1)]
        if ku==None: ku=[1.0/(NbUPoles-degree)*i for i in range(NbUPoles-degree+1)]


#        mv=[4] +[1]*(NbVPoles-4) +[4]
#        mu=[4]+[1]*(NbUPoles-4)+[4]

        mv=[degree+1] +[1]*(NbVPoles-degree-1) +[degree+1]
        mu=[degree+1] +[1]*(NbUPoles-degree-1) +[degree+1]

#        print  (len(ku)
#        print  (len(mu)
#        print mu


        bs=Part.BSplineSurface()
        bs.buildFromPolesMultsKnots(ps, mv, mu, kv, ku, False, False ,degree,degree)

        res=App.ActiveDocument.getObject(objName)

        # if res==None:
        res=App.ActiveDocument.addObject("Part::Spline",objName)
            # res.ViewObject.ControlPoints=True

        res.Shape=bs.toShape()

        return bs




def createAll(mode="all",obj=None,dimU=500,dimV=500,
                ua=10,sizeU=100,va=10,sizeV=100,
                socketheight=10,saxonyflag=True,rowselector='',center=False,scale=1,
                createpart=False,createsurface=True 
            ):




#    obj=App.ActiveDocument.Points
    print (obj.Points.BoundBox.Center)
    # center=False

    if center:
        zmin=obj.Points.BoundBox.ZMin -obj.Points.BoundBox.Center.z
        zmax=obj.Points.BoundBox.ZMax -obj.Points.BoundBox.Center.z
    else:
        zmin=obj.Points.BoundBox.ZMin
        zmax=obj.Points.BoundBox.ZMax

    p=obj.Points.Points


    if center:
        p=np.array(obj.Points.Points)- obj.Points.BoundBox.Center

    assert dimU*dimV==len(p)

#    if mode!="all":
#        return


    zmin *=scale
    zmax *=scale
    socketheight *= scale
    p=[pp*scale for pp in p]


    pa2=np.array(p).reshape(dimU,dimV,3)

#    pa3=[]
#    a=0
#    for i in range(dimU):
#        if pa2[i][0][0]!=a:
#            pa3 += [pa2[i]] 
#            print pa2[i][0][0]-a
#        
#        print pa2[i][0]
#        a= pa2[i][0][0]

    # andere variante
    
    if saxonyflag:
        pa3=[]
        pmin=[]
        pmax=[]
        for i in range(dimU):
            if i%4==1:
                pmin += [pa2[i]]
            if i%4==3:
                pmax += [pa2[i]]
            if i%2==0:
                pa3 += [pa2[i]] 
            

    else:
        p3=p2
    pa4=np.array(pa3)
    pa4.shape
    
    if 0: # auswertung der anderen baender
        pmin=np.array(pmin)
        print (pmin.shape)
        pmax=np.array(pmax)
        print (pmax.shape)
        comp=[]
        for i in range(124):
            for j in range(500):
                if i<4 and j<4:
                    print [pmin[i+1],j,pmax[i,j]]
                a=App.Vector(pmin[i+1,j])
                b=App.Vector(pmax[i,j])
                if a!=b:
                    if b.z<a.z: a,b=b,a
                    comp += [ Part.makePolygon([a,a+(b-a)*10])]
                    

        print (len(comp))
        Part.show(Part.Compound(comp))


#    return


    if 0:
        ta=time.time()
        ss=PointarrayToMesh(pa4[60:70,60:70])
        siz=10
        tb=time.time()
        bc=Part.BSplineSurface()
        bc.interpolate(pa4[100:100+siz,100:100+2*siz])
        tc=time.time()
        Part.show(bc.toShape())
        td=time.time()
        tc-tb
        td-tc


    #ss=PointarrayToMesh(pa4)

    if mode=='mesh':
        ta=time.time()
        if 0:
            ss=PointarrayToMesh(pa4,h=zmax)
            ss=PointarrayToMesh(pa4,h=zmin)

        tb=time.time()
        print ("create meshes all", tb-ta)

        ta=time.time()
        #ss=PointarrayToMesh(pa4)
        if 1:
            print ("!",zmax,zmin,socketheight)
            # ss=PointarrayToMesh(pa4[ua:ua+sizeU,va:va+2*sizeV],h=zmax+socketheight)
            ss=PointarrayToMesh(pa4[ua:ua+sizeU,va:va+2*sizeV],h=zmin-socketheight)

        tb=time.time()
        print ("create meshes sub ", tb-ta)
        #return


#    if not createsurface: return


    if mode=='part' or mode=='nurbs':
        #create nurbs face
        tb=time.time()
        bs=machFlaeche(pa4[ua:ua+sizeU,va:va+2*sizeV])
        tc=time.time()
        print ("create surf 200 x 200 ", tc-tb)

        if 0:
            tb=time.time()
            bs=machFlaeche(pa4,degree=3)
            tc=time.time()
            print ("create surf all ", tc-tb)


#    if not createpart: return
    if not mode=='part': 
        return


    #create side faces
    ff=App.ActiveDocument.ActiveObject
    be=[]
    faces=[ff.Shape.Face1]
    for i,e in enumerate(ff.Shape.Face1.Edges):
        print (e)
        pa=e.Vertexes[0].Point
        pe=e.Vertexes[-1].Point

        h=zmin-socketheight
        pau=App.Vector(pa.x,pa.y,h)
        peu=App.Vector(pe.x,pe.y,h)

        e2=Part.makePolygon([pa,pau])
        e3=Part.makePolygon([peu,pe])
        e4=Part.makePolygon([pau,peu])

    #    Part.show(e2)
    #    Part.show(e3)
        Part.show(e4)
        App.ActiveDocument.recompute()
        eA=App.ActiveDocument.ActiveObject
        if i%2==0:
            be += [eA]

        Part.show(e)
        App.ActiveDocument.recompute()
        eB=App.ActiveDocument.ActiveObject
        
        rf=App.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')
        rf.Curve1=(eA,['Edge1'])
        rf.Curve2=(eB,['Edge1'])
        App.ActiveDocument.recompute()
        faces += [rf.Shape.Face1]

    # create bottom face
    rf=App.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')
    rf.Curve1=(be[0],['Edge1'])
    rf.Curve2=(be[1],['Edge1'])
    App.ActiveDocument.recompute()
    faces += [rf.Shape.Face1]


    #create shell and solid
    _=Part.Shell(faces)
    sh=App.ActiveDocument.addObject('Part::Feature','Shell2')
    sh.Shape=_.removeSplitter()
    del _
    App.ActiveDocument.recompute()

    shell=sh.Shape
    _=Part.Solid(shell)
    App.ActiveDocument.addObject('Part::Feature','Solid').Shape=_.removeSplitter()
    del _

    App.ActiveDocument.recompute()

    tc=time.time()

    # toUVMesh(bs)

    tc-tb


# createAll()


#I commented this .. don't know what is doing mariwan
# if 1:
#         import miki
#         import nurbs
#         #reload(nurbs.miki)
#         rc=nurbs.miki.runtest
        


layout2='''
VerticalLayoutTab:
    setText:"HUHUWAS"
    id:'main'

    VerticalLayout:

        QtGui.QLabel:
            setText:"***   N U R B S  YYY XX  E D I T O R   ***"
'''


layout2='''
MainWindow:

    VerticalLayout:
        QtGui.QLabel:
            setText:"***   create a surface for a point cloud   ***"
#        QtGui.QLabel:
#            setText:"<hr>you have <hr>to select <hr>a point cloud<br>"

        HorizontalLayout:
            QtGui.QCheckBox:
                id: 'createpart' 
                setText: 'Create Part Solid'
                setChecked: False

            QtGui.QCheckBox:
                id: 'createsurface' 
                setText: 'Create Surface'
                setChecked: False

            QtGui.QCheckBox:
                id: 'center' 
                setText: 'Origin to Center Bound Box'
                setChecked: True
            QtGui.QCheckBox:
                id: 'saxony' 
                setText: 'Saxon data format'
                setChecked: True
            QtGui.QLabel:
                setText:"row filter"
            QtGui.QComboBox:
                id: 'row'
                addItem: "even"
                addItem: "odd"
                addItem: "0 % 4"
                addItem: "1 % 4"
                addItem: "2 % 4"
                addItem: "3 % 4"

            QtGui.QLabel:
                setText:"socket height"
            QtGui.QLineEdit:
                setText:"10"
                id: 'socketheight'


        HorizontalLayout:
            QtGui.QLabel:
                setText:"scale "
            QtGui.QLineEdit:
                setText:"1000"
                id: 'scale'

            QtGui.QLabel:
                setText:"u dim "
            QtGui.QLineEdit:
                setText:"500"
                id: 'ud'
            QtGui.QLabel:
                setText:"v dim "
            QtGui.QLineEdit:
                setText:"500"
                id: 'vd'


        HorizontalLayout:
            QtGui.QLabel:
                setText:"u start "
            QtGui.QLineEdit:
                setText:"50"
                id: 'ua'
            QtGui.QLabel:
                setText:"u size "
            QtGui.QLineEdit:
                setText:"20"
                id: 'us'

        HorizontalLayout:

            QtGui.QLabel:
                setText:"v start "
            QtGui.QLineEdit:
                setText:"50"
                id: 'va'
            QtGui.QLabel:
                setText:"v size "
            QtGui.QLineEdit:
                setText:"20"
                id: 'vs'

        HorizontalLayout:
            QtGui.QPushButton:
                setText: "Run Mesh Socket"
                clicked.connect: app.createMesh

            QtGui.QPushButton:
                setText: "Run Nurbs at Socket"
                clicked.connect: app.createNurbs

            QtGui.QPushButton:
                setText: "Run planar Part at Socket"
                clicked.connect: app.createPart

            QtGui.QPushButton:
                setText: "Run "
                clicked.connect: app.run

            QtGui.QPushButton:
                setText: "Close"
                clicked.connect: app.close

'''



class MyApp(object):

    def __init__(self):
        self.pole1=[1,5]
        self.pole2=[3,1]
        self.lock=False

    def updateDialog(self):
        pass
        #self.root.ids['ud'].setMaximum(self.obj.Object.nNodes_u-2)
        #self.root.ids['vd'].setMaximum(self.obj.Object.nNodes_v-2)

    def run(self,mode='all'):

        print ("run",mode,self.obj.Label)
#        return

        createAll(
            mode,
            self.obj,
            int(self.root.ids['ud'].text()),
            int(self.root.ids['vd'].text()),

            int(self.root.ids['ua'].text()),
            int(self.root.ids['us'].text()),
            int(self.root.ids['va'].text()),
            int(self.root.ids['vs'].text()),
            int(self.root.ids['socketheight'].text()),
            self.root.ids['saxony'].isChecked(),
            self.root.ids['row'].currentText(),
            self.root.ids['center'].isChecked(),
            int(self.root.ids['scale'].text()),
            self.root.ids['createpart'].isChecked(),
            self.root.ids['createsurface'].isChecked(),
        )


    def createPart(self):
        self.run('part')

    def createMesh(self):
        self.run('mesh')

    def createNurbs(self):
        self.run('nurbs')

    def close(self):
        for w in App.w5: w.hide()
        App.w5=[]


def mydialog(obj):


    import nurbs.miki as miki
    #reload (miki)

    app=MyApp()
    miki=miki.Miki()

    miki.app=app
    app.root=miki
    app.obj=obj

    #miki.parse2(layout2)
    miki.run(layout2)

#    miki.ids['ud'].setMaximum(obj.Object.nNodes_u-2)
#    miki.ids['vd'].setMaximum(obj.Object.nNodes_v-2)

    return miki

class Nurbs_PointsRUNA:
    def Activated(self):
        self.runA()
    def runA(self):
        try:
            obj=Gui.Selection.getSelectionEx()[0]
        except:
            obj=App.ActiveDocument.Points
        mydialog(obj)
    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_PointsRUNA")
        return {'Pixmap': NURBSinit.ICONS_PATH+"points.svg",
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_PointsRUNA"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_PointsRUNA", Nurbs_PointsRUNA())


#-------------------------glaetten 


import random
import Points,Draft
import os

def init(d):
    anzp=400
    anze=80
    la=[random.random() for l in range(anzp)]
    a=10
    
    if 1:
        pts=[App.Vector(100*x+a*(random.random()-0.5),50*x+a*(random.random()-0.5),0) for x in la]
        pts += [App.Vector(100*random.random(),150*random.random()-50,0) for x in range(anze)]

    if 1:
        pts=[App.Vector(100*x+a*(random.random()-0.5),200+a*(random.random()-0.5)+50*np.sin(5.0*np.pi*x),0) for x in la]
        pts += [App.Vector(100*random.random(),100*random.random()+150,0) for x in range(anze)]

    if 1:
        a=1
        pts=[App.Vector(100*x+a*(random.random()-0.5),200+a*(random.random()-0.5)+50*np.sin(5.0*np.pi*x),0) for x in la]
        for ii in range(anze):
            x=random.random()
            pts += [App.Vector(100*x,80*random.random()+160+50*np.sin(5.0*np.pi*x),0)]


    # polare Transformation
    
    ptsp=[App.Vector(p.y*np.cos(p.x*np.pi*0.02),p.y*np.sin(p.x*np.pi*0.02),0) for p in pts]
    Points.show(Points.Points(ptsp))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,0.,1.)
    App.ActiveDocument.ActiveObject.ViewObject.PointSize=4



    Points.show(Points.Points(pts))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,0.,0.)
    App.ActiveDocument.ActiveObject.ViewObject.PointSize=4

    # d=5

    pts=sorted(pts,key=lambda x: x[0])
    return pts

def run(pts,loop,d,dd,outliner=True):


    pts2=np.array(pts)

    start=0
    pts3=[]
    anzp =pts2.shape[0]

    for xp in range(120): # total score
        yv=0
        wv=0
        for i in range(anzp):
            x,y,z=pts2[i]
            if x<xp-d:
                start=i
                continue
            if x>xp+d:
                end=i
                break
            fak=1-abs(xp-x)/d
            wv +=  fak
            yv +=  fak*y
        if wv!=0:
            yn=yv/wv
        else: continue

        if outliner:
            yv=0
            wv=0
            for i in range(start,end+1):
                x,y,z=pts2[i]
                
                if abs(y-yn)>dd:
                    print ("outliner",loop,xp,i,y-yn)
                else:
                    fak=1-abs(xp-x)/d
                    wv +=  fak
                    yv +=  fak*y
        if wv!=0:
            yn=yv/wv
            pts3 += [App.Vector(xp,yn,0)]



    Points.show(Points.Points(pts3))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(0.5+0.5*random.random(),0.5+0.5*random.random(),0.5+0.5*random.random())

    pts4= filter(lambda x: x[0] <=100, pts3)
    ptsp=[App.Vector(p.y*np.cos(p.x*np.pi*0.02),p.y*np.sin(p.x*np.pi*0.02),0) for p in pts4]
    Points.show(Points.Points(ptsp))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(0.5+0.5*random.random(),0.5+0.5*random.random(),0.5+0.5*random.random())



    return pts3,ptsp

def  results(ptsa,ptsb):
    ptsa= filter(lambda x: x[0] <=100, ptsa)

    bc=Part.BSplineCurve()
    bc.approximate(ptsa,DegMin=1,DegMax=3,Tolerance=0.3)
    Draft.makeWire(ptsa)
    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(0.,1.,1.)

    cww=App.ActiveDocument.getObject("FF2")
    if cww==None:
        cww=App.ActiveDocument.addObject('Part::Spline','FF2')

    cww.Shape=bc.toShape()

    bc=Part.BSplineCurve()
    bc.approximate(ptsb,DegMin=1,DegMax=3,Tolerance=5.)
    Draft.makeWire(ptsb)
    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,0.,1.)

    cwk=App.ActiveDocument.getObject("FF3")
    if cwk==None:
        cwk=App.ActiveDocument.addObject('Part::Spline','FF3')

    cwk.Shape=bc.toShape()


    _=App.ActiveDocument.recompute()
    cww.ViewObject.LineColor=(1.,1.,0.)
    cww.ViewObject.LineWidth=7

    cwk.ViewObject.LineColor=(1.,1.,0.)
    cwk.ViewObject.LineWidth=7


    print ("Poles:",bc.NbPoles)

class Nurbs_PointsRUNC:
    def Activated(self):
        self.runC
    def runC(self):
        d=5
        pts=init(d)
        App.pts=pts
    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_PointsRUNC")
        return {'Pixmap': NURBSinit.ICONS_PATH+"points.svg"
,
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_PointsRUNC"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_PointsRUNC", Nurbs_PointsRUNC())



class Nurbs_PointsRUND:
    def Activated(self):
        self.runD
    def runD(self):
        d=5
        pts=App.pts
        ptsa=pts

        for i in range(5):
            timea=time.time()
            ptsa,ptsb=run(ptsa,i,d,1*d)
            print ("loop",i,(time.time()-timea)/len(ptsa)*1000)

        results(ptsa,ptsb)
    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_PointsRUND")
        return {'Pixmap': NURBSinit.ICONS_PATH+"points.svg",
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_PointsRUND"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_PointsRUND", Nurbs_PointsRUND())





class Nurbs_PointsRUNE:
    def Activated(self):
        self.runE
    def runE(self):
        import time
        d=5
        pts=App.pts
        ptsa=pts

        for i in range(5):
            timea=time.time()
            ptsa,ptsb=run(ptsa,i,d,2*d,False)
            print ("loop",i,(time.time()-timea)/len(ptsa)*1000)

        results(ptsa,ptsb)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_PointsRUNE")
        return {'Pixmap': NURBSinit.ICONS_PATH+"points.svg",
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_PointsRUNE"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_PointsRUNE", Nurbs_PointsRUNE())


