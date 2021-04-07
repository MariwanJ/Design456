# -*- coding: utf-8 -*-
'''
#-------------------------------------------------
#--create curve/face pattern
#--
#-- microelly 2018  0.3
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''

##\cond

import networkx as nx
import numpy as np
import random

from nurbswb.say import *
import nurbswb.pyob
from nurbswb.pyob import  FeaturePython,ViewProvider
reload (nurbswb.pyob)
import nurbswb.lib as nl
reload(nurbswb.lib)


def vkey(vec):
    '''vector as key'''
    return tuple((round(vec[0],5),round(vec[1],5),round(vec[2],5)))

##\endcond

def splitEdges(obj=None,show=True):
    '''split edges on intersection points'''

    if obj==None:
        obj=Gui.Selection.getSelection()[0]
        shape=obj.Shape
    else:
        shape=obj

    es=shape.Edges
    g=nx.Graph()
    points={}
    vecs=[]

    # register all vertexes of the shape
    for vi,v in enumerate(shape.Vertexes):
        p=vkey(v.Point)
        points[tuple(p)]=vi
        vecs +=  [p]

    # register all edges of the shape
    for e in es:
        assert len(e.Vertexes)==2
        [p,q]=e.Vertexes
        kp=vkey(p.Point)
        kq=vkey(q.Point)
        g.add_edge(points[kp],points[kq],edge=e)

    # calculate the direction of the edges for each vertex
    for n in g.nodes():

        arcl={}
        for e in g.edges(n):
            fe=g.get_edge_data(*e)['edge']
            if (fe.valueAt(fe.FirstParameter)-App.Vector(vecs[n])).Length<0.0001:
                arc=np.arctan2(*fe.tangentAt(fe.FirstParameter)[0:2])
            else:
                vv=fe.tangentAt(fe.LastParameter)*(-1)
                arc=np.arctan2(*vv[0:2])

            arcl[arc]=e
            sk=np.sort(list(arcl.keys()))
            arcl2=[(arcl[k],k) for k in sk]
            g.node[n]['sortedEdges']=arcl2


    # Schnittpunkte

    pts=[]
    xyplane=Part.Plane()

    cuts=[]
    for c1i,c1 in enumerate(shape.Edges):
        (cmin,cmax)=c1.ParameterRange
        cuts += [[cmin,cmax]]

    cuts2=[]
    for c1i,c1 in enumerate(shape.Edges):
        (cmin,cmax)=c1.ParameterRange
        cuts2 += [[cmin,cmax]]

    for c1i,c1 in enumerate(shape.Edges):
        for c2i,c2 in enumerate(shape.Edges):
            c1=c1.toNurbs().Edge1
            c2=c2.toNurbs().Edge1
            if c1i<c2i:
                ips=c1.Curve.intersect2d(c2.Curve,xyplane)
                for p in ips:
                    try:
                        _ = points[vkey([p[0],p[1],0.0])]
                    except:
                        # liegt Punkt innen?
                        pp=App.Vector(p[0],p[1],0.0)
                        (cmin,cmax)=c1.ParameterRange
                        cp1=c1.Curve.parameter(pp)
                        if cmin<cp1 and cp1<cmax:
                            (cmin,cmax)=c2.ParameterRange
                            cp=c2.Curve.parameter(pp)
                            if (cmin<cp and cp<cmax):
                                pts+=[App.Vector(p[0],p[1])]
                                cuts[c1i] += [cp1]
                                cuts2[c2i] += [cp]
                                print(("schnitt",c1i,c2i,cp1,cp))

    # use the cutpoints to split all edges
    newedges=[]
    oldedges=[]

    displayEdges=False
    for cus,cus2,e in zip(cuts,cuts2,shape.Edges):

        if len(cus)>2 and len(cus2)>2:
            cus=cus+cus2[2:]
        elif len(cus2)>2:
            cus=cus2

        if len(cus)>2:
            cus.sort()
            e=e.toNurbs().Edge1
            for i in range(len(cus)-1):
                c=e.Curve.copy()
                try:
                    c.segment(cus[i],cus[i+1])
                except:
                    print(("fehler c.segment(cus[i],cus[i+1])",i))
                    continue
                #display the segment
                if displayEdges:
                    Part.show(c.toShape())
                    #App.ActiveDocument.ActiveObject.ViewObject.hide()
                    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(
                            random.random(),random.random(),random.random())
                newedges+= [c.toShape()]
        else:
            oldedges += [e]

    if displayEdges:
        for e in oldedges:
                Part.show(e)
                        #App.ActiveDocument.ActiveObject.ViewObject.hide()
                App.ActiveDocument.ActiveObject.ViewObject.LineColor=(
                                random.random(),random.random(),random.random())

    if show:
        # compound of all splitted edges
        Part.show(Part.Compound(newedges+oldedges))
        App.ActiveDocument.ActiveObject.ViewObject.PointColor=(1.,0.,0.)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,1.,1.)
        App.ActiveDocument.ActiveObject.ViewObject.PointSize=6
        obj=App.ActiveDocument.ActiveObject
        obj.Label="split Edge"

    return newedges+oldedges



def createPattern(obj=None,rx=3,ry=2,sx=200,sy=100,all_faces=None):
    '''create pattern subobjects'''

    if obj==None:
        obj=Gui.Selection.getSelection()[0]
        comp=obj.Shape
    else:
        comp=obj

    # size of the pattern:
    sizex,sizey=3000,2000
    sizex,sizey=sx,sy
    # repeats of the pattern rx,ry

    es=comp.Edges
    points={}
    vecs=[]
    g=nx.Graph()

    for vi,v in enumerate(comp.Vertexes):
        p=vkey(v.Point)
        points[tuple(p)]=vi
        vecs +=  [p]

    for e in es:
        [p,q]=e.Vertexes
        kp=vkey(p.Point)
        kq=vkey(q.Point)
        g.add_edge(points[kp],points[kq],edge=e)


    for n in g.nodes():
        arcl={}
        for e in g.edges(n):
            fe=g.get_edge_data(*e)['edge']
            if (fe.valueAt(fe.FirstParameter)-App.Vector(vecs[n])).Length<0.001:
                arc=np.arctan2(*fe.tangentAt(fe.FirstParameter)[0:2])
            else:
                vv=fe.tangentAt(fe.LastParameter)*(-1)
                arc=np.arctan2(*vv[0:2])

            arcl[arc]=e

        sk=np.sort(list(arcl.keys()))
        arcl2=[(arcl[k],k) for k in sk]
        g.node[n]['sortedEdges']=arcl2



    def find_segment_step(n,alt,*a):
        '''find the next edge/vertex of a area segment'''
        se=g.node[n]['sortedEdges']
        pol=[n,alt]+ list(a)


        for i,(e,arc) in enumerate(se):
            (n1,n2)=e
            if n2==alt:
                (e,arc)=se[i-1]
                (n1,n2)=e
                pol =[n2] + pol
                if n1==n:
                    return n2

        return None



    def show(pol):
        '''display the segment pattern'''

        print(("display figure",pol))
        tz=App.ActiveDocument.addObject("Part::Feature","tracks")
        tz.ViewObject.LineColor=(random.random(),random.random(),random.random())
        tz.ViewObject.ShapeColor=tz.ViewObject.LineColor
        tz.ViewObject.LineWidth=3

        if 0: # display simplified polygon only
            pts=[App.Vector(vecs[p]) for p in pol]
            tz.Shape=Part.makePolygon(pts)

        comps=[]
        for j in range(len(pol)-1):
            comps += [ g.get_edge_data(pol[j],pol[j+1])['edge']]

        if 10: # display curves compound
            tz.Shape=Part.Compound(comps)

        # display faces
        s1=Part.makeFilledFace(Part.__sortEdges__(comps))
        if s1.isNull(): raise RuntimeError('Failed to create face')
        col=[]

        for xc in range(rx):
            for yc in range(ry):
                sn=s1.copy()
                sn.Placement.Base.x=sizex*xc
                sn.Placement.Base.y=sizey*yc
                col +=[sn]

        tz.Shape=Part.Compound(col+comps)
        tz.Placement.Base.z=random.random()-tz.Shape.Area*0.00001

        return tz


    def find_all_segments():
        '''find all closed areas'''

        tracks=[]
        lg=max(g.nodes())+1
        used=np.zeros(lg*lg).reshape(lg,lg)

        for n in g.nodes():
            for n2 in g.nodes():
                liste=[n,n2]
                start=liste[0]
                liste2=liste
                rc=-1

                while rc!=None and rc not in liste:

                    liste=liste2
                    rc=find_segment_step(*liste)
                    try:
                        [rc1,rc2]=rc
                        liste2 = [rc1,rc2]+liste
                        rc=rc1
                    except:
                        liste2 = [rc]+liste

                if (liste2[0]==liste2[-1] or liste2[1]==liste2[-1]) and len(liste2)>3 :

                    if liste2[1]==liste2[-1]:
                        liste2=liste2[1:]
                    if not used[liste2[0],liste2[1]] and not used[liste2[1],liste2[2]] :
                        rc=show(liste2)
                        tracks += [rc]
                    for i in range(len(liste2)):
                        used[liste2[i-1],liste2[i]]=1

                Gui.updateGui()

        return tracks

    tracks=find_all_segments()
    sw=all_faces

    sw.Links=tracks
    for t in tracks:
        t.purgeTouched()
    sw.recompute()
    sw.purgeTouched()

#erzeugt einzelnes Muster bestehend aus Flächen

def createSinglePattern():
    '''create a simple pattern with faces without repetitions'''
    createPattern(obj=None,rx=1,ry=1)



def _createArray(show=True,obj=None):
    ''' array aus edges machen'''

    edges=[]

    pm=App.Placement(App.Vector(0,0,0),    App.Rotation(App.Vector(0,0,1),0))
    pms=[pm]

    if obj.modeX=='mirror':
        pm2=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),180))
        pms += [pm2]

    if obj.modeY=='mirror':
        pm2=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),180))
        pms += [pm2]

    if obj.modeY=='rotate':
        pm2=App.Placement(App.Vector(0,obj.sizeY,0),App.Rotation(App.Vector(0,0,1),180))
        pms += [pm2]

    if obj.modeX=='rotate':
        pm2=App.Placement(App.Vector(obj.sizeX,0,0),App.Rotation(App.Vector(0,0,1),180))
        pms += [pm2]

    if obj.modeX=='mirror' and obj.modeY=='mirror':
        pm2=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
        pms += [pm2]

    if obj.modeX=='rotate' and obj.modeY=='rotate':
        pm2=App.Placement(App.Vector(-obj.sizeX,-obj.sizeY,0),App.Rotation(App.Vector(0,0,1),0))
        pms += [pm2]


    if obj.modeX=='rotate' and obj.modeY=='mirror':
        pm2=App.Placement(App.Vector(-obj.sizeX,0,0),App.Rotation(App.Vector(1,0,0),180))
        pms += [pm2]

    if obj.modeX=='mirror' and obj.modeY=='rotate':
        pm2=App.Placement(App.Vector(0,-obj.sizeY,0),App.Rotation(App.Vector(0,1,0),180))
        pms += [pm2]



    if obj==None:
        for obj in Gui.Selection.getSelection():
            edges += obj.Shape.Edges
    else:
            edges = obj.obj.Shape.Edges

    es2=[]
    xc=1
    yc=1
    for xi in range(xc):
        for yi in range(yc):
            for e in edges:
                for pm in pms:
                    e2=e.copy()
                    e2.Placement.Base.x += 1000*xi
                    e2.Placement.Base.y += 1000*yi
                    sh2=e2.copy()
                    sh2.Placement=pm.multiply(e2.Placement)
                    es2 +=[sh2]

    if obj.createBorder:
        a=App.Vector(0,0)
        b=App.Vector(xc*obj.sizeX,0)
        d=App.Vector(0,yc*obj.sizeY)
        c=App.Vector(xc*obj.sizeX,yc*obj.sizeY)
        sh=Part.makePolygon([a,b,c,d,a])

        for pm in pms:
            sh2=sh.copy()
            sh2.Placement=pm
            es2 +=[sh2]

    if show:
        Part.show(Part.Compound(es2))
        App.ActiveDocument.ActiveObject.Label="Array from generic pattern"
        return App.ActiveDocument.ActiveObject
    else:
        return (es2)




def removeEdges():
    '''remove selected edges from collection'''

    sel=Gui.Selection.getSelectionEx()[0]

    todelete=[]
    for sun in sel.SubElementNames:
        en=int(sun[4:])-1
        todelete += [en]

    eds=sel.Object.Shape.Edges
    eds2=[]
    for i,e in enumerate(eds):
        if i not in todelete:
            eds2+= [e]

    Part.show(Part.Compound(eds2))

    if 0:
        sel.Object.ViewObject.hide()
    else:
        sel.Object.ViewObject.LineWidth=1
        sel.Object.ViewObject.LineColor=(1.,1.,1.)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=(0.,0.,1.)
        App.ActiveDocument.ActiveObject.ViewObject.LineWidth=10


## Das Pattern Objekt erzeugt aus den Kanten des **obj** ein
# Compound mit Kanten, welche in den Parametern eingestellte Symmetrien
# bilden
#
# Das Ergebnis ist planar in xy oder auf eine Targetfläche abgebildet
#

class Pattern(FeaturePython):
    ''' parametric pattern object'''
##\cond
    def __init__(self, obj,uc=5,vc=5):
        FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyFloat","sizeX","Base","size of the border").sizeX=800
        obj.addProperty("App::PropertyFloat","sizeY","Base","Size of the border").sizeY=600
        obj.addProperty("App::PropertyBool","createBorder","Base","add border rectangle to pattern").createBorder=False
        obj.addProperty("App::PropertyEnumeration","modeX","Base").modeX=['simple','mirror','rotate']
        obj.addProperty("App::PropertyEnumeration","modeY","Base").modeY=['simple','mirror','rotate']
        obj.addProperty("App::PropertyLink","obj","Base","shape with pattern geometry")
        obj.addProperty("App::PropertyBool","splitEdges","post","")
        obj.addProperty("App::PropertyLink","target","target","target face to map ")
        obj.addProperty("App::PropertyBool","mapToTarget","target","").mapToTarget=True
        obj.addProperty("App::PropertyInteger","repeatX","target","how often to repeat pattern in u/x direction").repeatX=1
        obj.addProperty("App::PropertyInteger","repeatY","target","how often to repeat iny/v direction").repeatY=2

        obj.addProperty("App::PropertyBool","createPlanarPattern","postPlane","").createPlanarPattern=True
        obj.addProperty("App::PropertyFloat","sizePlanarX","postPlane","").sizePlanarX=800
        obj.addProperty("App::PropertyFloat","sizePlanarY","postPlane","").sizePlanarY=600
        obj.addProperty("App::PropertyInteger","repeatPlanarX","postPlane","").repeatPlanarX=2
        obj.addProperty("App::PropertyInteger","repeatPlanarY","postPlane","").repeatPlanarY=3
##\endcond


    def myExecute(self, fp):
        '''split Edges, optional map curves to a target surface'''

        col=_createArray(show=False,obj=fp)
        if fp.splitEdges:
            col=splitEdges(Part.makeCompound(col),show=False)

        fp.Shape=Part.makeCompound(col)

        if fp.mapToTarget and fp.target != None:
            col2=[]
            border=Part.makeCompound(col)
            for c in col:
                if c.Edge1.Curve.__class__.__name__=='BSplineCurve':
                    col2 += mapcurve(c.Edge1.discretize(10),border,fp.target,fp.repeatX,fp.repeatY)
                else:
                    col2 += mapcurve([v.Point for v in c.Vertexes],border,fp.target,fp.repeatX,fp.repeatY)
            fp.Shape=Part.makeCompound(col2)

        if fp.createPlanarPattern:

            sx=fp.sizePlanarX
            sy=fp.sizePlanarY
            if fp.modeX!='simple':
                sy *=2
            if fp.modeY!='simple':
                sx *=2

            try:
                self.all_faces.ViewObject.hide()
            except: pass

            self.all_faces=App.ActiveDocument.addObject("Part::Compound","All_Faces")

            col=splitEdges(Part.makeCompound(col),show=False)
            createPattern(Part.makeCompound(col),
                rx=fp.repeatPlanarX,ry=fp.repeatPlanarY,
                sx=sx,sy=sy,
                all_faces=self.all_faces,
                )


def createPatternV3(obj=None,target=None,createPlanarPattern=False):
    '''create a pattern object'''


    a=App.ActiveDocument.addObject("Part::FeaturePython","Pattern")
    Pattern(a)
    ViewProvider(a.ViewObject)
    a.createPlanarPattern=createPlanarPattern
#    a.modeY='mirror'
#    a.modeX='rotate'
    a.createPlanarPattern=True

    a.repeatX=5
    a.repeatY=5
    a.obj=obj
    a.target=target
    a.Label="Pre Pattern for "+obj.Label
    return a



def patternV3():
    '''call from WB Gui'''
    s=Gui.Selection.getSelection()
    print s
    obj=s[0]
#    if len(s)>1:
#        target=s[1]
#    else:
#        target=None
#    print obj.Label,target.Label

    createPatternV3(obj)

## bildet eine Folge von Punkten **points** auf die Fläche1 des Objektes
# **target**.
# Die Größe wird angepasst und das Muster **repeatX** / **repeatY** mal wiederholt.


import matplotlib.pyplot as plt
from scipy import interpolate



def mapv(vvals,face):

    f=face
    sf=f.Surface

    (umi,uma,vmi,vma)=f.ParameterRange

    anz=11
    bc=sf.uIso(umi)
    pts=bc.discretize(anz)
    vs=[bc.parameter(p) for p in pts]
    vr=[vmi+(vma-vmi)/(anz-1)*a for a in range(anz)]

    f = interpolate.interp1d(vr, vs)
    ynew = f(vvals)
    #plt.plot(vr, vs, 'o', xnew, ynew, '-')
    #plt.show()

    return ynew

def mapu(uuvals,face):

    f=face
    sf=f.Surface

    (umi,uma,vmi,vma)=f.ParameterRange

    anz=11
    bc=sf.vIso(vmi)
    pts=bc.discretize(anz)
    vs=[bc.parameter(p) for p in pts]
    ur=[umi+(uma-umi)/(anz-1)*a for a in range(anz)]

    f = interpolate.interp1d(ur, vs)
    ynew = f(uuvals)

    return ynew


#vvals=[0.1,0.5,1.2,1.7]
#mapv(vvals)




def mapcurve(points,border,target,repeatX,repeatY):
    '''maps a curve to a surface - stretch,repeat over the whole area'''


    f=target.Shape.Face1
    (umi,uma,vmi,vma)=f.ParameterRange

    f2=border

    xl=f2.BoundBox.XLength
    yl=f2.BoundBox.YLength
    xmi=f2.BoundBox.XMin
    ymi=f2.BoundBox.YMin

    es=[]
    for ix in range(repeatX):
        for iy in range(repeatY):
            bs2d = Part.Geom2d.BSplineCurve2d()
            pts2d=[]
            uss=[umi+(p.x-xmi)*(uma-umi)/xl/repeatX+(uma-umi)/repeatX*ix for p in points]
            vss=[vmi+(p.y-ymi)*(vma-vmi)/yl/repeatY+(vma-vmi)/repeatY*iy for p in points]
            vss2=mapv(vss,f)
            uss2=mapu(uss,f)

            pts2d +=[App.Base.Vector2d(u,v) for u,v in zip(uss2,vss2)]

            #geschlossen
            #bs2d.buildFromPolesMultsKnots(pts2d,[1]*(len(pts2d)+1),list(range(len(pts2d)+1)),True,1)

            bs2d.buildFromPolesMultsKnots(pts2d,[2]+[1]*(len(pts2d)-2)+[2],list(range(len(pts2d)-0)),False,1)

            e = bs2d.toShape(f.Surface)
            es +=[e]

    return es



def testcase():
    '''simple run'''
    nl.load("pattern/pattern_1")
    createPatternV3(App.ActiveDocument.Sketch,App.ActiveDocument.BePlane)
#    createPatternV3(App.ActiveDocument.Sketch,App.ActiveDocument.BeTube)
#    createPatternV3(App.ActiveDocument.Sketch,None,True)

def patternalltests():
    testcase()



#--------
