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


'''shoe xyz'''
# -*- coding: utf-8 -*-

#-------------------------------------------------
#-- create a shoe
#--
#-- microelly 2017 v 0.4
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

##\cond
import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui
import Part,Mesh,Draft,Points
import Design456Init
import os,sys

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import random

##\endcond


##\cond
def Myarray2Poly(arr,bb):

    print ("Polygon Variante")

    pst=np.array(arr)
    try: NbVPoles,NbUPoles,_t1 =pst.shape
    except: return (Part.Shape(),Part.Shape())

    comp=[]
    print (pst.shape)
    for i,pps in enumerate(pst):
        if i == 0: continue 

        pvs=[App.Vector(p) for p in pps]
        # print pvs
        pol=Part.makePolygon(pvs)
        comp.append(pol)
        App.pol=pol
        App.ActiveDocument.RibsPoly.OutList[i].Shape=pol

    for i,pps in enumerate(pst.swapaxes(0,1)):
        pvs=[App.Vector(p) for p in pps[1:]]
        pol=Part.makePolygon(pvs)
        comp.append(pol)
        App.ActiveDocument.MeridiansPoly.OutList[i].Shape=pol

    pvs=[App.Vector(p) for p in bb[1:]]
    pol=Part.makePolygon(pvs)
    comp.append(pol)

    for i,pps in enumerate(pst):
        if i == 0: continue 
        pvs=[App.Vector(pps[0]),App.Vector(bb[i]),App.Vector(pps[-1])]
        pol=Part.makePolygon(pvs)
        comp.append(pol)


    t=Part.Compound(comp)
    App.t=t

    return (t,comp)

#---------------------------
'''
nachverarbeitung shoe
testskript zum abloesen der methoden in shoe.py fuer die
generierung des nurbs shoe last
'''


def createBS(arr):
    ''' createBS(arr): create a BSpline Surface with the poles array arr'''

    cylinder=True
    #cylinder=False

    arr=np.array(arr)
    # pst=arr.swapaxes(0,1)
    pst=arr

    NbVPoles,NbUPoles,_t1 =pst.shape

    degree=3

    udegree=degree
    vdegree=degree

    if degree == 1: cylinder = False

    ps=[[App.Vector(pst[v,u,0],pst[v,u,1],pst[v,u,2]) for u in range(NbUPoles)] for v in range(NbVPoles)]

    kv=[1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
    mv=[4] +[1]*(NbVPoles-4) +[4]


    if  NbVPoles == 2:
        print ("KKKK")
        kv=[0,1]
        mv=[2,2]
        vdegree=1


    if cylinder:
        ku=[1.0/(NbUPoles-1)*i for i in range(NbUPoles)]
        mu=[2]+[1]*(NbUPoles-2)+[2]

        # bug 
        ku=[1.0/(NbUPoles)*i for i in range(NbUPoles+1)]
        mu=[1]*(NbUPoles+1)
        print  (len(ps))
        print (sum(mu))

    else:
        ku=[1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]
        mu=[4]+[1]*(NbUPoles-4)+[4]


    bs=Part.BSplineSurface()
    bs.buildFromPolesMultsKnots(ps, mv, mu, kv, ku, False,cylinder ,vdegree,udegree)

    print ("Cylinmder::",cylinder)
    return bs

#----------------------------------------------


def createSimpleBSC(pols, degree=3):
    ''' createSimpleBSC(pols): create a BSpline Curve with poles pols
    
    '''

    bc=Part.BSplineCurve()
    du=degree
    cu=len(pols)

    period=False
    kus=[1.0/(cu-du)*i for i in range(cu-du+1)]
    mu=[du+1]+[1]*(cu-du-1)+[du+1]

    #geschlossen/periodisch
    #period=True
    #kus=[1.0/(cu)*i for i in range(cu-1)]
    #mu=[3]+[1]*(cu-3)+[3]

    bc.buildFromPolesMultsKnots(pols,mu,kus,period,du,)
    return bc


def Xrun():
    ''' run(): test script
    creates the surface and some helpers
    
    '''


    # get the poles from shoe.py 
    pts=App.shoe_pst.copy()
    pts[:,:,1] *= -1

    # die flaeche
    bs=createBS(pts)
    try: fa=App.ActiveDocument.curve
    except: fa=App.ActiveDocument.addObject('Part::Spline','curve')

    fa.Shape=bs.toShape()





#----------------------------


def Myarray2NurbsD3(arr,label="MyWall",degree=3):

    pstb=np.array(arr).swapaxes(0,1)
    pst2=np.concatenate([pstb[7:-1],pstb[1:7]])
    psta=pst2.swapaxes(1,0)

    # ptsa=np.array(arr)

    try: NbVPoles,NbUPoles,_t1 =psta.shape
    except: return (Part.Shape(),Part.Shape())

#    bs=Part.BSplineSurface()
#    bs.interpolate(psta)

    pst=psta

    App.shoe_pst=pst
#    bs.setVPeriodic()

    pst[:,:,1] *= -1
    psta=pst

    # die flaeche
    bs=createBS(pst)

#    try: fa=App.ActiveDocument.curveA
#    except: fa=App.ActiveDocument.addObject('Part::Spline','curveA')
#
#    fa.Shape=bs.toShape()



    color=(random.random(),random.random(),random.random())

#- kann qwg
#    for i,pps in enumerate(psta):
#        if i == 0 : continue
#        bc=Part.BSplineCurve()
#        bc.interpolate(pps)
#        App.ActiveDocument.Ribs.OutList[i].Shape=bc.toShape()
#        App.ActiveDocument.Ribs.OutList[i].ViewObject.LineColor=color
#
#    for i,pps in enumerate(psta.swapaxes(0,1)):
#        bc=Part.BSplineCurve()
#        bc.interpolate(pps[2:])
#        App.ActiveDocument.Meridians.OutList[i].Shape=bc.toShape()
#        App.ActiveDocument.Meridians.OutList[i].ViewObject.LineColor=color

    if 1:
        sf2=bs.copy()
        sf2.setVPeriodic()
        uks=sf2.getUKnots()
        sf2segment(uks[1],1,0,1)
        sh2=sf2.toShape()

    uks=bs.getUKnots()
    bssegment(uks[1],1,0,1)
    sh=bs.toShape()

    vcp=False
    try:
        sp=App.ActiveDocument.Poles
        vcp=sp.ViewObject.ControlPoints
    except: sp=App.ActiveDocument.addObject("Part::Spline","Poles")
    sp.Shape=sh2
    sp.ViewObject.ControlPoints=vcp
    #sp.ViewObject.hide()

    try:
        fa=bs.uIso(0)
        sha1 = Part.Wire(fa.toShape())
        sha = Part.Face(sha1)

        fb=bs.uIso(1)
        shb1 = Part.Wire(fb.toShape())
        shb = Part.Face(shb1)

        sol=Part.Solid(Part.Shell([sha.Face1,shb.Face1,sh.Face1]))
    except:
        try:
            sha=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Poles.Shape.Edge3, ]))
            shb=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Poles.Shape.Edge1, ]))
            sol=Part.Solid(Part.Shell([sha.Face1,shb.Face1,sh.Face1]))
        except:
            sol=sh

    return (sol,bs)


def toUVMesh(bs, uf=5, vf=5):
        uc=uf*bs.NbUPoles
        vc=vf*bs.NbVPoles
        ss=[]
        for x in range(uc+1): 
            for y in range(vc+1): 
                ss.append(bs.value(1.0/uc*x,1.0/vc*y))

        mm=np.array(ss)[:,2].max()
        #add closing points
        ss.append(App.Vector(0,0,0))
        ss.append(App.Vector(0,0,mm))

        topfaces=[]
        x=0
        x=-1
        for y in range(-1,vc): 
            topfaces.append(((vc+1)*x+y,(vc+1)*x+y+1,len(ss)-2))
        x=uc+1
        for y in range(-1,vc): 
            topfaces.append(((vc+1)*x+y,(vc+1)*x+y+1,len(ss)-1))

        #t=Mesh.Mesh((ss,topfaces))
        #Mesh.show(t)
        #App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"


        faces=[]
        for x in range(-1,uc): 
            for y in range(-1,vc+1): 
                #if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
                #if len(faces)<100000:
                    faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
                    faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

        if 0:
            App.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
            App.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
            App.Console.PrintMessage(str(("faces:",len(faces)))+"\n")

        if len(faces)<100000:
            t=Mesh.Mesh((ss,faces))
            Mesh.show(t)
            App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
            App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
            App.ActiveDocument.ActiveObject.ViewObject.LineColor = (.0,.00,0.70)
            return App.ActiveDocument.ActiveObject
        else:
            raise Exception("big mesh not implemented")

            ks=len(faces)//100000
            for i in range(ks+1):
                t=Mesh.Mesh((ss,faces[i*100000:(i+1)*100000]))
                Mesh.show(t)
                App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
                App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
                App.ActiveDocument.ActiveObject.ViewObject.LineColor = (.70,.00,0.00)
                App.Console.PrintMessage(str(t))

        return t


def scale2(curves,scaler=None):

    c=np.array(curves)
#    print ("scale2 c.shape ",c.shape)
#    print ("len scaler",len(scaler))

    if scaler == None: scaler= [1]*10
    poles=np.array([c[i]*[scaler[i,0],scaler[i,0],scaler[i,1]] for i in range(len(scaler))])
    return poles


def extrude(profile,path=None):
    c=np.array(profile)
    try:
        vc,uc,_t=c.shape
    except:
        return c

    vc,uc,_t=c.shape
    for v in range(vc):
        c[v] += path[v]
    return c

def myrot(v,twister):
    v=App.Vector(v)
    [xa,ya,za]=twister
    p2=App.Placement()
    p2.Rotation=App.Rotation(App.Vector(0,0,1),za).multiply(App.Rotation(App.Vector(0,1,0),ya).multiply(App.Rotation(App.Vector(1,0,0),xa)))
#    print ("Rotation Euler",p2.Rotation.toEuler())

    p=App.Placement()
    p.Base=v
    rc=p2.multiply(p)
    return rc.Base


def twist(profile,twister):

    c=np.array(profile)
    try: vc,uc,_t=c.shape
    except: return c
    rc=[]
    for v in range(vc):
        cv=[]
#        print twister[v]
        for u in range(uc):
            sp=c[v,u]
            tpp=myrot(sp,twister[v])
            cv.append(tpp)
        c[v]=cv
    return c



#---------------------
# daten aus sheet



def cellname(col,row):
    #limit to 26
    if col>90-64:
        raise Exception("not implement")
    char=chr(col+64)
    cn=char+str(row)
    return cn



def npa2ssa(arr,spreadsheet,c1,r1,color=None):
    ''' write 2s array into spreadsheet '''
    ss=spreadsheet
    arr=np.array(arr)
    try:
        rla,cla=arr.shape
    except:
        rla=arr.shape[0]
        cla=0
    c2=c1+cla
    r2=r1+rla
#    print ("update ss -------------  xxx"
#    print arr
#    print (c1,r1,cla)

    if cla==0:
        for r in range(r1,r2):
            cn=cellname(c1,r)
            ss.set(cn,str(arr[r-r1]))
            if color!=None: ss.setBackground(cn,color)
    else:
        for r in range(r1,r2):
            for c in range(c1,c2):
                cn=cellname(c,r)
                #print (cn,c,r,arr[r-r1,c-c1])
                ss.set(cn,str(arr[r-r1,c-c1]))
                #print ("!!",cn,c,r,arr[r-r1,c-c1],ss.get(cn))
                if color!=None: ss.setBackground(cn,color)

def gendata(ss,twister,sc):
    print ("gendata",ss.Label)

    bb=[]

#    npa2ssa(curve,ss,2,3,(1.0,1.0,0.5))
    npa2ssa(bb,ss,7,3,(1.0,.5,1.0))
    npa2ssa(sc,ss,10,3,(0.5,1.0,1.0))
    npa2ssa(twister,ss,13,3,(1.0,.5,0.5))
#    ss.set('B1',str(len(curve)))
    ss.set('G1',str(len(bb)))

    ss.set('G2','Backbone x')
    ss.set('H2','y')
    ss.set('I2','z')
    ss.set('J2','Scale xy')
    ss.set('K2','z')
    ss.set('M2','Rotation x')
    ss.set('N2','y')
    ss.set('O2','z')
#    ss.set('B2','Rib x')
#    ss.set('C2','y')
#    ss.set('D2','z')

    App.ActiveDocument.recompute()


## spreadsheat to numpy array 
def ssa2npa(spreadsheet,c1,r1,c2,r2,default=None):
    ''' create array from table'''

    c2 +=1
    r2 +=1

    ss=spreadsheet
    z=[]
    for r in range(r1,r2):
        for c in range(c1,c2):
            cn=cellname(c,r)
            # print cn
            try:
                v=ss.get(cn)
                z.append(ss.get(cn))
            except:
                z.append(default)


    z=np.array(z)
#    print z
    ps=np.array(z).reshape(r2-r1,c2-c1)
    return ps


def WasDefinedAsmain():

    App.ActiveDocument=None
    Gui.ActiveDocument=None
    App.open(Design456Init.NURBS_DATA_PATH+ "nadel_daten.fcstd")
    App.setActiveDocument("nadel_daten")
    App.ActiveDocument=App.getDocument("nadel_daten")
    Gui.ActiveDocument=Gui.getDocument("nadel_daten")




##\cond
class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

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
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None
##\endcond


class Needle(PartFeature):
    ##cond
    def __init__(self, obj,uc=5,vc=5):
        PartFeature.__init__(self, obj)

        self.Type="Needle"
        self.TypeId="Needle"

        for l in ['Mesh','Backbone','Profile','RibCage','RibTemplate','Spreadsheet']:
            obj.addProperty("App::PropertyLink",l,l)
            obj.addProperty("App::PropertyBool","use" + l ,l)
            setattr(obj,"use"+l,False)

        obj.addProperty("App::PropertyLinkList","Ribs","Ribs")

        obj.addProperty("App::PropertyBool","noExecute" ,"Base")
        obj.addProperty("App::PropertyInteger","Degree","Base").Degree=3
        obj.addProperty("App::PropertyLink","Meridians","RibCage")
        obj.addProperty("App::PropertyInteger","MeridiansCount","RibCage").MeridiansCount=20
        obj.addProperty("App::PropertyInteger","RibCount","RibCage").RibCount=10
        obj.addProperty("App::PropertyInteger","MeshUCount","Mesh").MeshUCount=5
        obj.addProperty("App::PropertyInteger","MeshVCount","Mesh").MeshVCount=5

        # obj.ViewObject.LineColor=(1.0,0.0,1.0)
        #obj.ViewObject.DisplayMode = "Shaded"
        obj.ViewObject.Transparency = 50
        obj.addProperty("App::PropertyLink","ribtemplateSource","Spreadsheet")
        obj.addProperty("App::PropertyLink","backboneSource","Spreadsheet")
        obj.addProperty("App::PropertyBool","externSourcesOff" ,"Spreadsheet")
        ViewProvider(obj.ViewObject)

    def onDocumentRestored(self, fp):
        print ("onDocumentRestored ")
        print (fp.Label)
        self.Object=fp
    ##endcond

    def onChanged(self, fp, prop):
        
        if prop == 'useSpreadsheet':
            if fp.useSpreadsheet:
                if fp.Spreadsheet == None:
                    fp.Spreadsheet = App.ActiveDocument.addObject('Spreadsheet::Sheet','Spreadsheet')
                    ##gendata(fp.Spreadsheet)
            return
        if prop in ["Shape", 'Spreadsheet']: return
#        print ("onChanged",prop)


    def execute(proxy,obj):
#        print("execute ")
        if obj.noExecute: return
        try: 
            if proxy.lock: return
        except:
            print("except proxy lock")
        proxy.lock=True
#        print("myexecute")
        proxy.myexecute(obj)
        proxy.lock=False

    def myexecute(proxy,obj):

        ss=obj.Spreadsheet

        curves=[]
        pols=[]
        ribs=App.ribs

        #for r in obj.Ribs:
        for r in ribs:
            # pols=r.Points
            
            #pols=r.Shape.Edge1.Curve.discretize(obj.MeridiansCount)
            pols=r.Shape.Edge1.Curve.getPoles()
            
            #c=[[v[0],v[1],v[2]] for v in pols]
            c=[[v[2],v[0],v[1]] for v in pols]
            curves += c 

        if  len(obj.Ribs)>0:
            curves=np.array(curves)
            curves=curves.reshape(len(obj.Ribs),len(pols),3)

        if obj.backboneSource != None and not obj.externSourcesOff:
            cs=obj.backboneSource.Shape.Edge1.Curve
            bb=obj.backboneSource.Points
            bl=len(bb)
            npa2ssa(bb,ss,7,3,(1.0,1.,.0))

        else:
            bl=int(ss.get('G1'))
            bb=ssa2npa(ss,7,3,9,3+bl-1)

        scaler=ssa2npa(ss,10,3,11,3+bl-1,default=1.0)
        twister=ssa2npa(ss,13,3,15,3+bl-1,default=0.0)


#----------------------------
        '''
        # backbone machen
        #bbc=Part.BSplineCurve()
        #bbc.buildFromPoles(bb)

        #pa=bbc.LastParameter
        #ps=bbc.FirstParameter

        #print ("-----------------------------------------------"
        for n in range(len(bb)):

            v=ps +(pa-ps)*n/(len(bb)-1)
#            print ("!!",n,v)
#            print bbc.tangent(v)
            t=bbc.tangent(v)[0]
            p=bbc.value(v)
#            
#            print t
            zarc=np.arctan2(t.y,t.x)
            zarc *=180.0/np.pi
            zarc=0

            harc=np.arcsin(t.z)
            harc *=180.0/np.pi

        #    print twister[n]
            # twister[n]=[0,0,harc]
            
        #    print twister[n]
        print ("len twister",len(twister))
        #print twister
        '''


#-----------------------------

        if len(curves) <len(scaler):
                print ("zu wenig rippen")
                return

        poles= scale2(curves,scaler)
#        print ("poles shape",poles.shape)

        poles= twist(poles,twister)
        poles= extrude(poles,bb)

# kann weg
#        if 1:
#            (nn,comp)=Myarray2Poly(poles,bb)
#
#            try: poly=App.ActiveDocument.Poly
#            except: 
#                poly=App.ActiveDocument.addObject("Part::Compound",'Poly')
#                poly.ViewObject.PointSize = 10.00
#
#            poly.Shape=nn
#            #return

        if 1 :
            (nn,bs)=Myarray2NurbsD3(poles,"Nadelhuelle",degree=obj.Degree)

            obj.Shape=nn

            if obj.useBackbone: proxy.createBackbone(obj,bb)
            if obj.useRibTemplate: proxy.createRibTemplate(obj,curve)
            if obj.useRibCage: proxy.createRibCage(obj,bs)
            if obj.useMesh: proxy.createMesh(obj,bs)

    def createBackbone(proxy,obj,bb):
        return
        # deaktivert

        if obj.Backbone == None:
            obj.Backbone=App.ActiveDocument.addObject('Part::Feature','Backbone')
        
        #obj.Backbone.Shape=Part.makePolygon([App.Vector(b) for b in bb])
        bs=Part.BSplineCurve()
        #bs.buildFromPoles(bb)
        bs.interpolate(bb)
        obj.Backbone.Shape=bs.toShape()

        vob=obj.Backbone.ViewObject
        vob.LineColor=(0.,1.,1.)
        vob.LineWidth = 5.00

    def createRibTemplate(proxy,obj,curve):
        if obj.RibTemplate == None:
            obj.RibTemplate=App.ActiveDocument.addObject('Part::Feature','Rib template')
        #obj.RibTemplate.Shape=Part.makePolygon([App.Vector(c) for c in curve])

        bs=Part.BSplineCurve()
        c=curve
        ms=[2] +[1]*(len(c)-2) +[2]
        ks=[1.0/(len(c)-1)*i for i in range(len(c))]
        bs.buildFromPolesMultsKnots(c,ms,ks,True,3)
        obj.RibTemplate.Shape=bs.toShape()

        vob=obj.RibTemplate.ViewObject
        vob.LineColor=(1.,0.6,.0)
        vob.LineWidth = 5.00

    def createMesh(proxy,obj,bs):
            vb=True
            if obj.Mesh != None:
                vb=obj.Mesh.ViewObject.Visibility
                App.ActiveDocument.removeObject(obj.Mesh.Name)
            obj.Mesh=toUVMesh(bs,obj.MeshUCount,obj.MeshVCount)
            obj.Mesh.ViewObject.Visibility=vb

    def createRibCage(proxy,obj,bs):
        # deaktivert
        return 

        rc=obj.RibCount


        if rc>0:
            ribs=[]
            for i in range(rc+1):
                f=bs.uIso(1.0/rc*i)
                ribs.append(f.toShape())
        else:
            ribs=[]
            for i,j in enumerate(bs.getUKnots()):
                f=bs.uIso(j)
                ribs.append(f.toShape())


        comp=Part.Compound(ribs)
        if obj.RibCage == None:
            obj.RibCage=App.ActiveDocument.addObject('Part::Feature','Ribs')
        obj.RibCage.Shape=comp
        vob=App.ActiveDocument.ActiveObject.ViewObject
        vob.LineColor=(1.,1.,0.)
        vob.LineWidth = 5.00

        mers=[]
        for i,j in enumerate(bs.getVKnots()):
            f=bs.vIso(j)
            mers.append(f.toShape())
        comp=Part.Compound(mers)
        if obj.Meridians == None:
            obj.Meridians=App.ActiveDocument.addObject('Part::Feature','Meridians')
        obj.Meridians.Shape=comp
        vob=App.ActiveDocument.ActiveObject.ViewObject
        vob.LineColor=(1.,0.,0.4)
        vob.LineWidth = 5.00


    def updateSS(self,curve,bb,sc,twister):

            ss=self.Object.Spreadsheet
            ss.clearAll()
            npa2ssa(curve,ss,2,3,(1.0,1.0,0.5))
            npa2ssa(bb,ss,7,3,(1.0,.5,1.0))
            npa2ssa(sc,ss,10,3,(0.5,1.0,1.0))
            npa2ssa(twister,ss,13,3,(1.0,.5,0.5))
            ss.set('B1',str(len(curve)))
            ss.set('G1',str(len(bb)))
            ss.set('G2','Backbone x')
            ss.set('H2','y')
            ss.set('I2','z')
            ss.set('J2','Scale xy')
            ss.set('K2','z')
            ss.set('M2','Rotation x')
            ss.set('N2','y')
            ss.set('O2','z')
            ss.set('B2','Rib x')
            ss.set('C2','y')
            ss.set('D2','z')
            try:
                App.ActiveDocument.recompute()
            except:
                print ("recompute jack ")
                dokname=App.ParamGet('User parameter:Plugins/shoe').GetString("Document","Shoe")
                App.getDocument(dokname).recompute()
                pass

    def getExampleModel(self,model):
        print ("getExampleModel")
        print (model)
        m=model()
        print (model().curve)
        self.updateSS(m.curve,m.bb,m.sc,m.twister)

    def Model(self):
        ''' get model data from Spreadsheet 
        returns tuple: curve, backbone, scaler, twister
        '''
        ss=self.Object.Spreadsheet
        cl=int(ss.get('B1'))
        curve=ssa2npa(ss,2,3,4,3+cl-1)
        bl=int(ss.get('G1'))
        bb=ssa2npa(ss,7,3,9,3+bl-1)
        scaler=ssa2npa(ss,10,3,11,3+bl-1,default=1.0)
        twister=ssa2npa(ss,13,3,15,3+bl-1,default=0.0)
        return(curve,bb,scaler,twister)

    def setModel(self,curve,bb,scaler,twister):
        self.updateSS(curve,bb,scaler,twister)

    def startssevents(self):

        mw=Gui.getMainWindow()
        mdiarea=mw.findChild(QtGui.QMdiArea)

        App.ActiveDocument.Spreadsheet.ViewObject.startEditing(0)
        subw=mdiarea.subWindowList()
    #    print  (len(subw)
        for i in subw:
    #        print i.widget().metaObject().className()
            if i.widget().metaObject().className() == "SpreadsheetGui::SheetView":
                sheet = i.widget()
                table=sheet.findChild(QtGui.QTableView)

        table.clicked.connect(self.clicked)
    #    table.entered.connect(entered)
        table.pressed.connect(self.pressed)
        self.table=table

    def clicked(self,index):
        print ("Clicked",index)
        self.dumpix(index)
        print (getdata(index))

    def entered(self,index):
        print ("Entered")
        self.dumpix(index)

    def pressed(self,index):
        needle_cmds
        #reload(.needle_cmds)
        needle_cmds.pressed(index,App.ActiveDocument.MyNeedle)
        print ("Pressed")

    def changed(self,index):
        print ("Changed")
        self.dumpix(index)

    def dumpix(self,index): 
        print ("dumpix", index.row(),index.column(),(getdata(index)))
        self.show(getdata(index))


    def showRib(self,ri):
        Gui.Selection.clearSelection()
        dokname=App.ParamGet('User parameter:Plugins/shoe').GetString("Document","Shoe")
        d=App.getDocument(dokname)
        Gui.Selection.addSelection(d.getObject('Ribs'),"Edge" +str(ri))

    def showMeridian(self,ri):
        Gui.Selection.clearSelection()
        dokname=App.ParamGet('User parameter:Plugins/shoe').GetString("Document","Shoe")
        d=App.getDocument(dokname)
        Gui.Selection.addSelection(d.getObject('Meridians'),"Edge" +str(ri))


    def show(self,dat):
        sel,ci,ri,data=dat
        print ("show",dat)
        if sel=="bb" or sel=="bcmd": self.showRib(ri)
        elif sel=="rib" or sel=="ccmd": self.showMeridian(ri)
        else: Gui.Selection.clearSelection()





def importCurves(obj):
    ss=obj.Spreadsheet
    print (ss.Label)
    if obj.ribtemplateSource != None and not obj.externSourcesOff:
        cs=obj.ribtemplateSource.Shape.Edge1.Curve
        curve=cs.getPoles()
        cl=len(curve)
        npa2ssa(curve,ss,2,3)
        print ("update curve",curve)


    if obj.backboneSource != None and not obj.externSourcesOff:
        cs=obj.backboneSource.Shape.Edge1.Curve
        bb=cs.getPoles()
        bl=len(bb)
        npa2ssa(bb,ss,7,3)
        print ("update backbone",bb)

def createShoeNeedle(label="MyShoe"):
    a=App.ActiveDocument.addObject("Part::FeaturePython",label)

    n=Needle(a)
    a.useSpreadsheet=True
    # gendata(a.Spreadsheet)
    a.ViewObject.DisplayMode="Shaded"
    a.ViewObject.Transparency=20

    return a



'''
table.clicked.disconnect(clicked)
table.entered.disconnect(entered)
'''


#global globdat
#globdat=None

def commitData(editor):
#    print ("commit data",editor)

    needle_cmds
    #reload(.needle_cmds)
    global globdat
#    print globdat
    if globdat[0]=='ccmd':
        cn=cellname(int(globdat[1])+1,int(globdat[2])+3)
        old=globdat[3]
        needle_cmds.runCmd(old,cn,globdat[2],App.ActiveDocument.Spreadsheet)


def startssevents2():
    ''' start events for spreadsheet gui '''
    global table

    mw=Gui.getMainWindow()
    mdiarea=mw.findChild(QtGui.QMdiArea)

    App.ActiveDocument.Spreadsheet.ViewObject.startEditing(0)
    subw=mdiarea.subWindowList()
#    print  (len(subw)
    for i in subw:
#        print i.widget().metaObject().className()
        if i.widget().metaObject().className() == "SpreadsheetGui::SheetView":
            sheet = i.widget()
            table=sheet.findChild(QtGui.QTableView)

    table.clicked.connect(clicked)
#    table.entered.connect(entered)
    table.pressed.connect(pressed)




#    table.itemDelegate().commitData.connect(commitData)


'''
    from PySide import QtCore
    class SheetFilter(QtCore.QObject):
        def eventFilter(self,obj,event):
            print type(event)
            return False

    filter=SheetFilter()
    table.installEventFilter(filter)
    # table.removeEventFilter(filter)
 
'''




def getdata(index):
    r=index.row()
    c=index.column()

    if c == 0: # command fuer curve
        sel="ccmd"
        ri=r-2
        ci=0
        return sel,ci,ri,index.data()

    if c == 5: # command fuer curve
        sel="bcmd"
        ri=r-2
        ci=0
        return sel,ci,ri,index.data()


    if c in range(1,4):
        sel="rib"
        ci=c-1
    elif c in range(6,9):
        sel="bb"
        ci=c-6
    else:
        sel=None
        ci=-1

    ri=r-2

    return sel,ci,ri,index.data()




#-----------------------------------------
# TEST CASE
#-----------------------------------------

#if  __name__=='__main__':


def main_test():
    # test aus parametern
    import shoe as shoe
    #reload( .shoe)

    dokname=App.ParamGet('User parameter:Plugins/shoe').GetString("Document","Shoe")
    try: App.closeDocument(dokname)
    except: pass

    App.newDocument(dokname)
    App.setActiveDocument(dokname)
    App.ActiveDocument=App.getDocument(dokname)
    Gui.ActiveDocument=Gui.getDocument(dokname)

    if 1:
        points=[App.Vector(192.694291746,-129.634476444,0.0),App.Vector(130.429397583,-0.657173752785,0.0),App.Vector(-52.807308197,-112.73400116,0.0),App.Vector(-127.525184631,-71.8170700073,0.0),App.Vector(-205.801071167,-274.622741699,0.0),App.Vector(28.1370697021,-262.169769287,0.0),App.Vector(125.981895447,-187.451873779,0.0)]
        Draft.makeBSpline(points,closed=True,face=True,support=None)
        # BSpline

        points=[App.Vector(-37.2293014526,1.68375661825e-08,0.28248746792),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,951.294546262)]
        Draft.makeBSpline(points,closed=False,face=True,support=None)
        # Bspline001


        #points=[App.Vector(-73.5499812578,-192.458589192,0.0),App.Vector(-35.2118430692,-245.401746512,0.0),App.Vector(-148.400562353,-232.622317741,0.0),App.Vector(-115.539281652,-172.376687886,0.0)]
        points=[App.Vector(592.694291746,-169.634476444,0.0),App.Vector(130.429397583,-0.657173752785,0.0),App.Vector(-52.807308197,-112.73400116,0.0),App.Vector(-127.525184631,-71.8170700073,0.0),App.Vector(-295.801071167,-294.622741699,0.0),App.Vector(28.1370697021,-262.169769287,0.0),App.Vector(125.981895447,-187.451873779,0.0)]

        Draft.makeBSpline(points,closed=True,face=True,support=App.ActiveDocument.getObject("BSpline"))
        # Bspline002

        points=[App.Vector(-37.2293014526,1.68375661825e-08,-10),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,1200)]
        Draft.makeBSpline(points,closed=False,face=True,support=None)
        # Bspline003


    a=shoe.createNeedle()


    gendata(a.Spreadsheet)

    App.ActiveDocument.recompute()

    a.Ribs=[App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,
        App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,
        App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,App.ActiveDocument.BSpline,App.ActiveDocument.BSpline002,
    ]


    a.useBackbone=True
    a.useRibTemplate=True
    a.useRibCage=True
    a.useMesh=False



    a.ribtemplateSource=App.ActiveDocument.BSpline
    a.backboneSource=App.ActiveDocument.BSpline001



    App.ActiveDocument.recompute()

#    vp=needle.ViewProvider(a.ViewObject)
    App.ActiveDocument.recompute()

    if 0:

        # zweiter koerper

        b=App.ActiveDocument.addObject("Part::FeaturePython","MyShoe")
        bn=needle.Needle(b)


        '''
        b.useBackbone=True
        b.useRibTemplate=True
        b.useRibCage=True
        b.useMesh=True
        '''
        b.useSpreadsheet=True


        # b.Spreeadsheet=App.ActiveDocument.addObject('Spreadsheet::Sheet','huhu')
        bss=b.Spreadsheet
        needle.gendata(bss)

        b.ribtemplateSource=App.ActiveDocument.BSpline002
        b.backboneSource=App.ActiveDocument.BSpline003
        App.ActiveDocument.recompute()


        vp=needle.ViewProvider(b.ViewObject)


        Gui.SendMsgToActiveView("ViewFit")
        print ("finished")
         


        needle.importCurves(a)
        needle.importCurves(b)
        
    App.ActiveDocument.recompute()
    App.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")


    print (a)
    for r in a.Ribs:
        print( r.Label)

def genss(sk):
        ''' ribs aus daten'''

        poles=sk.Shape.Edge1.Curve.getPoles()
        points=[App.Vector(0,p[0],p[1]) for p in poles]


#        ps=points[8:]+points[:8]
        points=ps

#        p=points[0]
#        ps=[App.Vector(0,p.y-5,p.z),App.Vector(0,p.y-10,p.z)]+points+[App.Vector(0,p.y+10,p.z),App.Vector(0,p.y+5,p.z)] 
#        points=ps

        print  (len(points))
        return sk



## create the default shoe

##\endcond

## Erstellung eines Schuh Leisten und einiger Hilfsobjekte
#
# - Laden eins Laengsprofiles zum Vergleich
# - Laden einer gescannten Punktwolke zum Vergleich
#
# Erzeugen von Segmenten als Schritt fuer die Nachbereitung
#
# <a href='http://freecadbuch.de/doku.php?id=shoe'>Anwender Doku</a>
#

 
def ThousandsOfRunWhatShouldIdo():
    ''' shoe.run() '''

    # get the name for the documente from FC config
    dokname=App.ParamGet('User parameter:Plugins/shoe').GetString("Document","Shoe")

    # start with a new document
    try: App.closeDocument(dokname)
    except: pass

    App.newDocument(dokname)
    App.setActiveDocument(dokname)
    App.ActiveDocument=App.getDocument(dokname)
    Gui.ActiveDocument=Gui.getDocument(dokname)


#- kann weg
#    g=App.ActiveDocument.addObject("App::DocumentObjectGroup","Ribs")
#    m=App.ActiveDocument.addObject("App::DocumentObjectGroup","Meridians")
#    gp=App.ActiveDocument.addObject("App::DocumentObjectGroup","RibsPoly")
#    mp=App.ActiveDocument.addObject("App::DocumentObjectGroup","MeridiansPoly")

    #create a container for the rib sketches
    profiles=App.ActiveDocument.addObject("App::DocumentObjectGroup","Profiles")

    # load an example skethc for the xz-silouette
    App.Gui.activeDocument().mergeProject( Design456Init.NURBS_DATA_PATH+"last_sketch_sagittal.fcstd")
    App.ActiveDocument.Sketch.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0.707107,0.707107),180), App.Vector(0,0,0))



    print ("import ............")
    # import the configuration from shoedata 
    shoedata
    #reload(shoedata)

    bbps=shoedata.shoeAdam.bbps
    boxes=shoedata.shoeAdam.boxes
    twister=shoedata.shoeAdam.twister
    sc=shoedata.shoeAdam.sc


    # create the shoe ribs
    createshoerib
    #reload(.createshoerib)

    ribs=[createshoerib.run("rib_"+str(i),[[8,0,0]],boxes[i],zoff=0) for i in range(1,15)]

    # for debugging 
    App.ribs=ribs

    # create a backbone curve
    points=[App.Vector(tuple(v)) for v in bbps]

    babo=Draft.makeBSpline(points,closed=False,face=True,support=None)
    babo.Label="Backbone"
    profiles.addObject(babo)

    assert len(ribs)==len(twister)
    assert len(ribs)==len(sc)

    #create the Shoe Needle
    a=createShoeNeedle()

    gendata(a.Spreadsheet,twister,sc)
    App.ActiveDocument.recompute()

    #connect the shoeNeedle with the existing parts
    a.Ribs=ribs
    a.backboneSource=babo

    a.useBackbone=True
    a.useRibTemplate=False
    a.useRibCage=True
    a.useMesh=False


    # hack to update the spreadsheet
    a.Proxy.myexecute(a)


    App.ActiveDocument.recompute()
    App.ActiveDocument.recompute()
    Gui.activeDocument().activeView().viewFront()

    Gui.SendMsgToActiveView("ViewFit")
    Gui.runCommand("Draft_ToggleGrid")

    # load a scanned last to compare if available
    try: 
        Points.insert(Design456Init.NURBS_DATA_PATH+"shoe_last_scanned.asc","Shoe")
        App.ActiveDocument.shoe_last_scanned.ViewObject.ShapeColor=(1.0,.0,.0)
        App.ActiveDocument.shoe_last_scanned.ViewObject.PointSize=1
    except: 
        pass

    # create lofts from the creates curves
    if shoedata.showlofts:
        # flaechen erzeugen
        try: loft=App.ActiveDocument.MeridiansLoft
        except:loft=App.ActiveDocument.addObject('Part::Loft','MeridiansLoft')

        loft.Sections=App.ActiveDocument.Meridians.OutList

        try: loft=App.ActiveDocument.RibsLoft
        except:loft=App.ActiveDocument.addObject('Part::Loft','RibsLoft')

        loft.Sections=App.ActiveDocument.Ribs.OutList

    App.ActiveDocument.recompute()


    # hide all but some specials
    for i in App.ActiveDocument.Objects: i.ViewObject.hide()
    for obj in App.ActiveDocument.Sketch,App.ActiveDocument.Poles,App.ActiveDocument.shoe_last_scanned:
        obj.ViewObject.show()

    try: fa=App.ActiveDocument.Poles
    except: fa=App.ActiveDocument.addObject('Part::Spline','Poles')

    fa.ViewObject.Transparency=60

    # create inner and outer scale of the last to compare
    if shoedata.showscales:

        pc=Draft.clone(fa)
        pc.Scale.x=shoedata.scaleIn
        pc.Scale.y=shoedata.scaleIn
        pc.Scale.z=shoedata.scaleIn
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,1.0,.0)
        App.ActiveDocument.ActiveObject.Label="shoe " +str(shoedata.scaleIn)

        pc=Draft.clone(fa)
        pc.Scale.x=shoedata.scaleOut
        pc.Scale.y=shoedata.scaleOut
        pc.Scale.z=shoedata.scaleOut
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,.0,1.0)
        App.ActiveDocument.ActiveObject.Label="shoe " +str(shoedata.scaleOut)


    App.getDocument(dokname).saveAs(u"/tmp/shoe_v0.fcstd")

    # ein paar hilfslinien
    pts=np.array(fa.Shape.Face1.Surface.getPoles())
    comp=[]
    for yy in pts:
        pas=[App.Vector(tuple(p)) for p in yy]
        pol=Part.makePolygon(pas)
        cur=createSimpleBSC(pas)
        comp +=[pol,cur.toShape()]

    pts=pts.swapaxes(0,1)
    for yy in pts:
        pas=[App.Vector(tuple(p)) for p in yy]
        pol=Part.makePolygon(pas)
        cur=createSimpleBSC(pas)
        comp +=[pol,cur.toShape()]

    Part.show(Part.Compound(comp))
    App.ActiveDocument.ActiveObject.Label="Poles and Rib Splines"


    # ein paar hilfssegmente exemplarisch
    segment

    a=segment.createSegment()
    a.source=fa
    a.umax=-2
    a.umin=1
    a.vmax=-2
    a.vmin=1
    a.Label="Segment gesamt"

    a=segment.createFineSegment()
    a.source=fa
    a.umax=95
    a.umin=0
    a.vmax=98
    a.vmin=2
    a.Label="Fein Segment gesamt"

    # transform the poles array 
    s=segment.createNurbsTrafo()
    s.source=App.ActiveDocument.Poles

