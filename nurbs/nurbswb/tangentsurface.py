# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create a parametric tangent surface
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------



import FreeCAD as App
import FreeCADGui as Gui



from PySide import QtGui
import Part,Mesh,Draft,Points


import numpy as np
import random

import os, nurbswb

global __dir__
__dir__ = os.path.dirname(nurbswb.__file__)
print __dir__


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


def createShape(obj,force=False):

    poles=obj.source.Shape.Face1.Surface.getPoles()
    pts2=np.array(poles).copy()
    pts=pts2.copy()

    du=3
    dv=3


    if 1:
        dd=2
        l=pts[0].copy()
        l2=pts[0].copy()

        if obj.westSeam:
            seam=obj.westSeam
            print ("Seam.....WEST........."
            print seam
            tvs=[]
            for i in range(30):
                n="t"+str(i)
                tvs.append(getattr(seam,n))
            # print tvs
            tvs=np.array(tvs)
            tvs *= obj.tangentFactor
            for i in range(l.shape[0]):
                print l[i]
                l[i,2] += tvs[i,2]
                l[i,0] += tvs[i,0]
                l[i,1] += tvs[i,1]
                l2[i,2] -= tvs[i,2]
                l2[i,0] -= tvs[i,0]
                l2[i,1] -= tvs[i,1]
                print l[i]

        r=pts[-1].copy()
        r2=pts[-1].copy()

        if obj.eastSeam:
            seam=obj.eastSeam
            print ("Seam.......EAST......."
            tvs=[]
            print l.shape
            for i in range(30):
                n="t"+str(i)
                tvs.append(getattr(seam,n))
            tvs=np.array(tvs)
            #tvs *= 10
            tvs *= obj.tangentFactor
            for i in range(l.shape[0]):
                r[i,2] += tvs[i,2]
                r[i,0] += tvs[i,0]
                r[i,1] += tvs[i,1]
                r2[i,2] -= tvs[i,2]
                r2[i,0] -= tvs[i,0]
                r2[i,1] -= tvs[i,1]

        pts2=np.concatenate([[l,pts[0],pts[0],pts[0],l2],pts[1:-1],[r,pts[-1],pts[-1],pts[-1],r2]])
        #pts2=np.concatenate([[l2,pts[0],pts[0],pts[0],l],pts[2:-1],[r,pts[-1],pts[-1],pts[-1],r2]])

    pts2=pts2.swapaxes(0,1)

    if 0 or obj.nordSeam!=None or  obj.southSeam!=None:
        #----------- nord und sued

        pts=pts2.copy()


        dd=2
        l=pts[0].copy()
        l2=pts[0].copy()


        if obj.nordSeam:
            seam=obj.nordSeam
            print ("Seam......NORD........"
            print seam
            tvs=[]
            for i in range(30):
                n="t"+str(i)
                tvs.append(getattr(seam,n))
            print tvs
            tvs=np.array(tvs)
            tvs *= obj.tangentFactor
            for i in range(l.shape[0]-8):
                print l[i+2]
                l[i+4,2] += tvs[i,2]
                l[i+4,0] += tvs[i,0]
                l[i+4,1] += tvs[i,1]
                l2[i+4,2] -= tvs[i,2]
                l2[i+4,1] -= tvs[i,1]
                l2[i+4,0] -= tvs[i,0]

                print (i,l[i+2])

        r=pts[-1].copy()
        r2=pts[-1].copy()

        if obj.southSeam:
            seam=obj.southSeam
            print ("Seam.......South......."
            tvs=[]
            for i in range(30):
                n="t"+str(i)
                tvs.append(getattr(seam,n))
            tvs=np.array(tvs)
            tvs *= obj.tangentFactor
            for i in range(l.shape[0]-8):
                r[i+4,2] += tvs[i,2]
                r[i+4,1] += tvs[i,1]
                r[i+4,0] += tvs[i,0]
                r2[i+4,2] -= tvs[i,2]
                r2[i+4,1] -= tvs[i,1]
                r2[i+4,0] -= tvs[i,0]

        pts2=np.concatenate([[l,pts[0],pts[0],pts[0],l2],pts[1:-1],[r,pts[-1],pts[-1],pts[-1],r2]])

        #--------------------------


    (cv,cu,_x) =pts2.shape

    print ("XXXXXXXXXXXXXXXXXXXXXXX shape",cv,cu)

    kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
    kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

    print  (len(kvs)
#    print  (len(kus)
#    kvs=[-1,-0.6,-0.4,-0.2]+ obj.source.Shape.Face1.Surface.getVKnots() +[1.2,1.4,1.6,1.8]
# knotenvektor stimmt nicht .#+#
    kvs=obj.source.Shape.Face1.Surface.getVKnots()
#    kus=[-1]+ obj.source.Shape.Face1.Surface.getUKnots() +[1.5]

    print  (len(kvs)
    print obj.source.Shape.Face1.Surface.getVKnots()


    mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
    mu=[du+1]+[1]*(cu-du-1)+[du+1]

    bs=Part.BSplineSurface()

    bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )


#    bs.segment(kvs[1],kvs[-2],kus[1],kus[-2])

#    bs.segment(kvs[1],kvs[-2],kus[2],kus[-2])

#ok    bs.segment(kvs[6],kvs[-7],kus[1],kus[-2])
#    bs.segment(kvs[4],kvs[-5],kus[1],kus[-2])

    bs.segment(0,1,kus[1],kus[-2])

#    try: fa=App.ActiveDocument.orig
#    except: fa=App.ActiveDocument.addObject('Part::Spline','orig')

#    fa=App.ActiveDocument.addObject('Part::Spline','orig')
#    fa.Shape=bs.toShape()
#    fa.ViewObject.ControlPoints=True


    if 0:
        print ("tangenten links"
        print pts[0]-l

        print ("kurve links"
        print pts[0]


        print ("tangenten rechts"
        print pts[-1]-r
        print ("kurve rechts"
        print pts[-1]



    if 0 and App.tangentsleft == [] and obj.tangentsleft==[] and force:
        print ("create tangents"
        for i in range(cu):
            t=Draft.makeWire([App.Vector(pts[0,i]),App.Vector(l[i])])
            t.ViewObject.LineColor=(1.0,1.,0.)
            t.ViewObject.LineWidth=10
            t.Label="Tangent left " + str(i+1)
            App.tangentsleft.append(t)
            t=Draft.makeWire([App.Vector(pts[-1,i]),App.Vector(r2[i])])
            t.ViewObject.LineColor=(1.0,1.,0.)
            t.ViewObject.LineWidth=10
            t.Label="Tangent right " + str(i+1)
    else:
        if obj.tangentsleft != []:
            print ("setze tvektoren neu"
            for i in range(cu):
                obj.tangentsleft[i].Start=App.Vector(pts[0,i])
                obj.tangentsleft[i].End=App.Vector(l[i])
                obj.tangentsleft[i].Proxy.execute(obj.tangentsleft[i])


    obj.Shape=bs.toShape()
    print ("tangenten linksAA"
    print obj.tangentsleft
    hp=App.ActiveDocument.getObject(obj.Name+"BS")
    print hp
    if hp == None:
        hp=App.ActiveDocument.addObject('Part::Spline',obj.Name+"BS")

    hp.Shape=bs.toShape()
    print ("2kkoay"



class TangentFace(PartFeature):
    def __init__(self, obj):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyVector","Size","Base").Size=App.Vector(300,-100,200)
        obj.addProperty("App::PropertyLink","source","Base")
        obj.addProperty("App::PropertyLink","westSeam","Base")
        obj.addProperty("App::PropertyLink","eastSeam","Base")
        obj.addProperty("App::PropertyLink","nordSeam","Base")
        obj.addProperty("App::PropertyLink","southSeam","Base")

        obj.addProperty("App::PropertyBool","flipWest","Base")
        obj.addProperty("App::PropertyBool","flipEast","Base")
        obj.addProperty("App::PropertyBool","flipNorth","Base")
        obj.addProperty("App::PropertyBool","flipSouth","Base")
        obj.addProperty("App::PropertyBool","flipNorthB","Base")
        obj.addProperty("App::PropertyBool","flipSouthB","Base")
        obj.addProperty("App::PropertyBool","swap","Base")
        
        obj.addProperty("App::PropertyLinkList","tangentsleft","Base")
        obj.addProperty("App::PropertyFloat","tangentFactor","Base").tangentFactor=1.0

        ViewProvider(obj.ViewObject)



    def xexecute(proxy,obj):
#        print("execute ")
#        if obj.noExecute: return
        try: 
            if proxy.lock: return
        except:
            print("except proxy lock")
        proxy.lock=True
#        print("myexecute")
        proxy.myexecute(obj)
        proxy.lock=False




    def execute(proxy,obj):
        print ("myexecute tanface"
        if hasattr(obj,"westSeam"):
            print ("run proxy seam"
            createShapeV2(obj)
        print ("done myex"

    def onChanged(self, obj, prop):
        if prop in ['factorA','factorB','displayShape','flipEast','flipWest']:
            self.execute(obj)


class Seam(PartFeature):
    def __init__(self, obj):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyLink","source","Base")
        obj.addProperty("App::PropertyBool","sourceSwap","Base")
        obj.addProperty("App::PropertyBool","sourceFlip","Base")
        obj.addProperty("App::PropertyBool","fillCorner","Base")
        obj.addProperty("App::PropertyBool","linear","Base")
        obj.addProperty("App::PropertyBool","reversecut","Base")
        
#        obj.addProperty("App::PropertyInteger","tCount","Base").tCount=30
#        obj.addProperty("App::PropertyInteger","index","Base").index=0
#        obj.addProperty("App::PropertyVector","V","Base").V.z=1
#        obj.addProperty("App::PropertyFloat","P","Base").P=1.8
        obj.addProperty("App::PropertyLink","endPlane","Base")
        obj.addProperty("App::PropertyInteger","factorA","Base").factorA=10
        obj.addProperty("App::PropertyInteger","factorB","Base").factorB=10
        obj.addProperty("App::PropertyInteger","factorC","Base").factorC=10
        obj.addProperty("App::PropertyEnumeration","displayShape","Base").displayShape=["Seam","OutSeam","InSeam","Curve","Tangent1","Tangent2"]
        obj.linear=True
        obj.displayShape="OutSeam"
        ViewProvider(obj.ViewObject)


    def onChanged(self, obj, prop):
        if prop in ['factorA','factorB','factorC','displayShape','sourceFlip','sourceSwap','linear','V','P']:
            self.execute(obj)
        if prop in ["vmin","vmax","umin","umax","source"]:
            pass

    def execute(proxy,obj):

        if obj.source!=None:
            print("execute ")
            try:
                sf=obj.source.Shape.Face1.Surface
                sf.getPoles
            except:
                print ("konvertiere zu nurbs"
                ff=obj.source.Shape.Face1.toNurbs()
                sf=ff.Face1.Surface

            weights=sf.getWeights()

            sf=sf.copy()

            if obj.sourceSwap:
                poles=np.array(sf.getPoles()).swapaxes(0,1)
            else:
                poles=np.array(sf.getPoles())

            if obj.sourceFlip:
                poles=np.flipud(poles)

            spols=np.array([
                poles[0]+(poles[0]-poles[1])*obj.factorB*0.1+(poles[1]-poles[2])*obj.factorC*0.1,
                poles[0]+(poles[0]-poles[1])*obj.factorA*0.1,
                poles[0],
                poles[0]+(poles[1]-poles[0])*obj.factorA*0.1,
                poles[0]+(poles[1]-poles[0])*obj.factorB*0.1+(poles[2]-poles[1])*obj.factorC*0.1
            ])

            if obj.linear:

                if obj.endPlane == None:
                    A,B=obj.factorA,obj.factorB
                else:
                    A,B=1,1000

                if obj.displayShape=="OutSeam" or obj.displayShape in ["Curve","Tangent1","Tangent2"]:
                    spols=np.array([
                        poles[0],
                        poles[0]+(poles[1]-poles[0])*A*0.1*-1,
                        poles[0]+(poles[1]-poles[0])*A*0.1*-2,
                        poles[0]+(poles[1]-poles[0])*B*0.1*-4
                    ])
                    wew=[weights[0]]*4

                if obj.displayShape=="InSeam":

                    spols=np.array([
                        poles[0],
                        poles[0]+(poles[1]-poles[0])*A*0.1*1,
                        poles[0]+(poles[1]-poles[0])*A*0.1*2,
                        poles[0]+(poles[1]-poles[0])*B*0.1*4
                    ])
                    wew=weights[0:4]

                if obj.displayShape=="Seam":
                    spols=np.array([
                        poles[0]+(poles[1]-poles[0])*B*0.1*4,
                        poles[0]+(poles[1]-poles[0])*A*0.1*1,
                        poles[0]+(poles[1]-poles[0])*A*0.1*2,
                        poles[0],
                        poles[0]+(poles[1]-poles[0])*A*0.1*-1,
                        poles[0]+(poles[1]-poles[0])*A*0.1*-2,
                        poles[0]+(poles[1]-poles[0])*B*0.1*-4
                    ])
                    wew=weights[0:4][::-1]+[weights[0]]*3


            if obj.fillCorner:
                # border add
                poles=spols.swapaxes(0,1)

                spolsA=np.concatenate([
                [
                    poles[0]+(poles[0]-poles[1])*obj.factorB*0.1+(poles[1]-poles[2])*obj.factorC*0.1,
#                    poles[0]+(poles[0]-poles[2])*obj.factorB*0.1,
                    poles[0]+(poles[0]-poles[1])*obj.factorA*0.1,
                    poles[0]],
                    poles,
                    [poles[-1],
                    poles[-1]-(poles[-2]-poles[-1])*obj.factorA*0.1,
                    poles[-1]-(poles[-2]-poles[-1])*obj.factorB*0.1-(poles[-3]-poles[-2])*obj.factorC*0.1
                ]
                ])

                spols=spolsA.swapaxes(0,1)

            if obj.sourceSwap:
                closed=sf.isUClosed()
            else:
                closed=sf.isVClosed()
            bs=machFlaeche(spols,ku=None,closed=closed,bs=sf,swap=obj.sourceSwap)
            #bs=machFlaeche(spols,ku=None,closed=closed)

            if closed:
                if obj.displayShape=="OutSeam":
                    uks=bs.getUKnots()
                    vks=bs.getVKnots()
                    bs.segment(uks[0],uks[1],vks[0],vks[-1])
                if obj.displayShape=="InSeam":
                    uks=bs.getUKnots()
                    vks=bs.getVKnots()
                    bs.segment(uks[-2],uks[-1],vks[0],vks[-1])

                if obj.displayShape=="Curve":
                    bs=bs.uIso(0.5)

            else:
                if obj.displayShape=="OutSeam":
                    if not obj.linear:
                        uks=bs.getUKnots()
                        bs.segment(uks[0],uks[1],0,1)
                if obj.displayShape=="InSeam":
                    if not obj.linear:
                        uks=bs.getUKnots()
                        bs.segment(uks[-2],uks[-1],0,1)
                if obj.displayShape=="Curve":
                    if not obj.linear:
                        bs=bs.uIso(0.5)
                    else:
                        bs=bs.uIso(0.)
                if obj.displayShape=="Tangent1":
                    bs=bs.vIso(0.)
                if obj.displayShape=="Tangent2":
                    bs=bs.vIso(bs.getVKnots()[-1])

            if obj.endPlane != None:

                shape=bs.toShape()
                pl=obj.endPlane

                V=pl.Placement.Rotation.multVec(App.Vector(0,0,1)).normalize()
                P=V.dot(pl.Placement.Base)
                ends=[]
                anz=spols.shape[1]

                for i in shape.slice(V,P):
                    ends=i.discretize(anz)
                    if obj.reversecut:
                        ends=ends[::-1]

                if len(ends) >=2:
                    spols2=np.array([spols[0],spols[1],spols[2],ends])
                    bs=machFlaeche(spols2,ku=None,closed=closed,bs=sf,swap=obj.sourceSwap)

            obj.Shape=bs.toShape()




def createTangentFace():
    b=App.activeDocument().addObject("Part::FeaturePython","MyTangentFace")
    bn=FilledFace(b)


if __name__=='__main__':


    #create the test faces

    cu=6
    cv=6
    du=3
    dv=3

    pts=np.zeros(cu*cv*3).reshape(cu,cv,3)
    for u in range(cu): pts[u,:,0]=10*u 
    for v in range(cv): pts[:,v,1]=10*v 

    pts[4,4,2]=40
    pts[1,2,2]=-80
    pts[1,3,2]=-80
    pts[1,4,2]=-80
    pts[3,1,2]=180

    kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
    kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

    mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
    mu=[du+1]+[1]*(cu-du-1)+[du+1]

    try: fa=App.ActiveDocument.source
    except: fa=App.ActiveDocument.addObject('Part::Spline','source')

    bs=Part.BSplineSurface()
    bs.buildFromPolesMultsKnots(pts,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )

    fa.Shape=bs.toShape()
    fa.ViewObject.ControlPoints=True
    fa.ViewObject.ShapeColor=(1.0,1.0,0.6)
    source=fa


    try: fa2=App.ActiveDocument.targetE
    except: fa2=App.ActiveDocument.addObject('Part::Spline','targetE')

    pts=np.zeros(cu*cv*3).reshape(cu,cv,3)
    for u in range(cu): pts[u,:,0]=10*u +50
    for v in range(cv): pts[:,v,1]=10*v 
    bs.buildFromPolesMultsKnots(pts,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )

    fa2.Shape=bs.toShape()
    fa2.ViewObject.ControlPoints=True
    fa2.ViewObject.ShapeColor=(1.0,.6,1.0)

    '''
    # some more testfaces
    try: fa3=App.ActiveDocument.targetN
    except: fa3=App.ActiveDocument.addObject('Part::Spline','targetN')

    pts=np.zeros(cu*cv*3).reshape(cu,cv,3)
    for u in range(cu): pts[u,:,0]=10*u 
    for v in range(cv): pts[:,v,1]=10*v +50
    bs.buildFromPolesMultsKnots(pts,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )

    fa3.Shape=bs.toShape()
    fa3.ViewObject.ControlPoints=True
    fa3.ViewObject.ShapeColor=(1.0,.6,1.0)

    try: fa4=App.ActiveDocument.targetW
    except: fa4=App.ActiveDocument.addObject('Part::Spline','targetW')
    pts=np.zeros(cu*cv*3).reshape(cu,cv,3)
    for u in range(cu): pts[u,:,0]=10*u -50
    for v in range(cv): pts[:,v,1]=10*v 
    bs.buildFromPolesMultsKnots(pts,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )

    fa4.Shape=bs.toShape()
    fa4.ViewObject.ControlPoints=True
    fa4.ViewObject.ShapeColor=(1.0,.6,1.0)
    '''



if __name__ == '__main__':
    # create the segment for tangents
    import nurbswb.segment
    ke= nurbswb.segment.createFineSegment()
    ke.source=App.ActiveDocument.source
    ke.Label="SeamBase E"
    ke.umax=100
    ke.umin=99

    kw= nurbswb.segment.createFineSegment()
    kw.source=App.ActiveDocument.source
    kw.Label="SeamBase W"
    kw.umax=1
    kw.umin=0

    kn= nurbswb.segment.createFineSegment()
    kn.source=App.ActiveDocument.source
    kn.Label="SeamBase N"
    kn.vmax=100
    kn.vmin=99


    ks= nurbswb.segment.createFineSegment()
    ks.source=App.ActiveDocument.source
    ks.Label="SeamBase S"
    ks.vmax=1
    ks.vmin=0

    #create the seam
    wseam=App.activeDocument().addObject("Part::FeaturePython","SeamW")
    Seam(wseam)

    eseam=App.activeDocument().addObject("Part::FeaturePython","SeamE")
    Seam(eseam)

    nseam=App.activeDocument().addObject("Part::FeaturePython","SeamN")
    Seam(nseam)

    sseam=App.activeDocument().addObject("Part::FeaturePython","SeamS")
    Seam(sseam)


    # seams aus streifen berechnen 
    poles=ke.Shape.Face1.Surface.getPoles()
    for i,p in enumerate(poles[0]):
        v=poles[0][i]-poles[1][i]
        setattr(wseam,"t"+str(i),v*5)


    poles=kw.Shape.Face1.Surface.getPoles()
    for i,p in enumerate(poles[0]):
        v=poles[0][i]-poles[1][i]
        setattr(eseam,"t"+str(i),v*5)

    poles=np.array(kn.Shape.Face1.Surface.getPoles()).swapaxes(0,1)
    for i,p in enumerate(poles[0]):
        v=poles[0][i]-poles[1][i]
        setattr(nseam,"t"+str(i),App.Vector(v)*5)

    poles=np.array(ks.Shape.Face1.Surface.getPoles()).swapaxes(0,1)
    for i,p in enumerate(poles[0]):
        v=poles[0][i]-poles[1][i]
        setattr(sseam,"t"+str(i),App.Vector(v)*5)


    # seams von segmenten abhaengig machen
    eseam.source=ke
    nseam.source=kn
    nseam.sourceSwap=True
    sseam.source=ks
    sseam.sourceSwap=True
    wseam.source=kw


    b=App.activeDocument().addObject("Part::FeaturePython","MyTangentialFace")
    bn=TangentFace(b)
    b.westSeam=wseam
    b.eastSeam=eseam
    b.nordSeam=nseam
    b.southSeam=sseam
    b.source=fa2
    createShape(b,force=True)



    # some placements to see the tangent effect
    if 0:
        b2=Draft.clone(b)
        b2.Placement.Base.x=-100

        b3=Draft.clone(b)
        b3.Placement.Base.x=-50
        b3.Placement.Base.y=50


        b3=Draft.clone(b)
        b3.Placement.Base.x=-50
        b3.Placement.Base.y=-50


        ss=Draft.clone(source)
        ss.Placement.Base.x=50
        ss.Placement.Base.y=50


        ss=Draft.clone(source)
        ss.Placement.Base.x=-50
        ss.Placement.Base.y=50


        ss=Draft.clone(source)
        ss.Placement.Base.x=50
        ss.Placement.Base.y=-50

        ss=Draft.clone(source)
        ss.Placement.Base.x=-50
        ss.Placement.Base.y=-50



    App.activeDocument().recompute()




    # quality check
    c1=App.ActiveDocument.source.Shape.Edge3.Curve
    c2=App.ActiveDocument.MyTangentialFace.Shape.Edge2.Curve

    a1=c1.discretize(100)
    a2=c2.discretize(100)

    for i,p in  enumerate(a1):
        assert (p-a2[i]).Length <1e-9





def runseam():

    source=None
    if len( Gui.Selection.getSelection())!=0:
        source=Gui.Selection.getSelection()[0]
    s=App.activeDocument().addObject("Part::FeaturePython","SeamW")
    Seam(s)
    s.source=source
    try:
        s.endPlane=Gui.Selection.getSelection()[1]
    except: pass


def runtangentsurface():

    source=None
    if len( Gui.Selection.getSelection())!=0:
        source=Gui.Selection.getSelection()[0]
    b=App.activeDocument().addObject("Part::FeaturePython","MyTangentialFace")
    TangentFace(b)
#    b.westSeam=App.ActiveDocument.SeamW007
#    b.eastSeam=App.ActiveDocument.SeamW006
#    b.nordSeam=App.ActiveDocument.SeamW005
#    b.southSeam=App.ActiveDocument.SeamW008
    b.source=source




import FreeCAD,Part
def machFlaeche(psta,ku=None,closed=False,bs=None,swap=False):
        NbVPoles,NbUPoles,_t1 =psta.shape
#        print psta.shape

        degree=3
        degree=3

        if 0:
            print ("bs-dump: v"
            print bs.VDegree
            print bs.getVMultiplicities()
            print bs.getVKnots()
            print bs.getWeights()[0:4][0:4]
            print bs.getPoles()[0:2][0:2]
            print np.array(bs.getPoles()).shape

        ps=[[App.Vector(psta[v,u,0],psta[v,u,1],psta[v,u,2]) for u in range(NbUPoles)] for v in range(NbVPoles)]

        kv=[1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
        if ku==None: ku=[1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]

#        mv=[4] +[1]*(NbVPoles-4) +[4]
#        mv=[vdegree+1] +[1]*(NbVPoles-vdegree-1) +[vdegree+1]
#        mv=[4,3,3,4]
#        mv=[4,1,1,1,1,1,1,4]
#        mv=[5,3,2,5]
#        print mv
#        print sum(mv)
#        print ("--------------"
#        kv=range(len(mv))

        mu=[4,4]
#        mu=[4]+[1]*(NbUPoles-4)+[4]
        ku=range(len(mu))


        if closed:
            ku=[1.0/(NbUPoles+1)*i for i in range(NbUPoles+1)]
            mu=[1]*(NbUPoles+1)

        
        if bs == None:
            pass
        else:
            ps=np.array(ps).swapaxes(0,1)
            if swap:
                vdegree=bs.UDegree
                mv= bs.getUMultiplicities()
                kv= bs.getUKnots()
                wew= np.array(bs.getWeights()).swapaxes(0,1)
                wew=[wew[0],wew[1],wew[2],wew[3]]
            else:
                vdegree=bs.VDegree
                mv= bs.getVMultiplicities()
                kv= bs.getVKnots()
                wew= bs.getWeights()[0:4]

        bs2=Part.BSplineSurface()
        if wew != None:
            bs2.buildFromPolesMultsKnots(ps, mv, mu, kv, ku,  False,closed ,vdegree,degree,wew)
        else:
            bs2.buildFromPolesMultsKnots(ps, mv, mu, kv, ku,  False,closed ,vdegree,degree)
        return bs2





import numpy as np

print ("temp module"

def createShapeV2(obj):
    if not obj.swap:
        if obj.westSeam!=None and obj.eastSeam != None:
            print obj.westSeam.Label
            sfw=obj.westSeam.Shape.Face1.Surface
            print sfw.NbVPoles
            print sfw.NbUPoles
            
            ptsw=sfw.getPoles()


            print obj.eastSeam.Label
            sfe=obj.eastSeam.Shape.Face1.Surface
            print sfe.NbVPoles
            print sfe.NbUPoles
            ptse=sfe.getPoles()
            
            if obj.flipWest:
                ptsw=np.flipud(ptsw)
            if obj.flipEast:
                ptse=np.flipud(ptse)

            poles=np.concatenate([ptsw,ptse])
            
            closed=sfw.isUClosed()
#            closed=True
            print ("-------------------------"
            bs=machFlaeche(poles,closed=closed)
            obj.Shape=bs.toShape()

    else:
        if obj.nordSeam!=None and obj.southSeam != None:
            sfw=obj.nordSeam.Shape.Face1.Surface
            print sfw.NbVPoles
            print sfw.NbUPoles

            ptsw=sfw.getPoles()


            sfe=obj.southSeam.Shape.Face1.Surface
            print sfe.NbVPoles
            print sfe.NbUPoles
            ptse=sfe.getPoles()
            
            if obj.flipNorth:
                ptsw=np.flipud(ptsw)
            if obj.flipSouth:
                ptse=np.flipud(ptse)

            if obj.flipNorthB:
                ptsw=np.fliplr(ptsw)
            if obj.flipSouthB:
                ptse=np.fliplr(ptse)


        poles=np.concatenate([ptsw,ptse])
        #losed=sfw.isClosed()
        closed=sfw.isUClosed()
#        closed=True
        bs=machFlaeche(poles,closed=closed)
        obj.Shape=bs.toShape()
    print ("fertig"


'''
def createShapeV2(obj):
    print obj.westSeam
    print obj.eastSeam
    import nurbswb.temp as ttt
    reload (nurbswb.temp)
    nurbswb.temp.run(obj)
'''




'''
surface wb erzeugen flaeche

App.ActiveDocument.addObject("Surface::Extend","Surface002")
App.ActiveDocument.Surface002.Face = (App.ActiveDocument.Fillet001,["Face3"])

'''
