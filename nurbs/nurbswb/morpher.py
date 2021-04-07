import numpy as np
import random

import nurbswb
from nurbswb.pyob import  FeaturePython,ViewProvider
from nurbswb.say import *
reload (nurbswb.pyob)

class Morpher(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLink","A")
        obj.addProperty("App::PropertyLink","B")
        obj.addProperty("App::PropertyFloat","factorA").factorA=10

    def myOnChanged(self,obj,prop):

        if prop in ["Shape"]:
            return

        try:
            obj.A.Shape,obj.B.Shape,obj.factorA
        except:
            return

        sfa=obj.A.Shape.Face1.Surface
        sfb=obj.B.Shape.Face1.Surface

        umsa,vmsa=sfa.getUMultiplicities(),sfa.getVMultiplicities()
        umsb,vmsb=sfb.getUMultiplicities(),sfb.getVMultiplicities()
        uksa,vksa=sfa.getUKnots(),sfa.getVKnots()
        uksb,vksb=sfb.getUKnots(),sfb.getVKnots()


        kbb=uksb[-1]
        kaa=uksa[-1]
        kbbv=vksb[-1]
        kaav=vksa[-1]

        # beide flaechen auf gleiche polanzahl bringen
        for (k,m) in zip(uksa,umsa)[1:-1]:
            kb=k*kbb/kaa
            sfb.insertUKnot(kb,m,0)

        for (k,m) in zip(vksa,vmsa)[1:-1]:
            kb=k*kbbv/kaav
            sfb.insertVKnot(kb,m,0)

        for (k,m) in zip(uksb,umsb)[1:-1]:
            kb=k*kaa/kbb
            sfa.insertUKnot(kb,m,0)

        for (k,m) in zip(vksb,vmsb)[1:-1]:
            kb=k*kaav/kbbv
            sfa.insertVKnot(kb,m,0)


        pa=np.array(sfa.getPoles())
        pb=np.array(sfb.getPoles())

        print pa.shape
        print pb.shape
        pb2=npb.copy()
        a,b=pb.shape[0:1]

        if 0:
            ppa=pa.swapaxes(0,1)
            ppa=ppa[::-1]
            pa=ppa.swapaxes(0,1)
            pb=pb[::-1] 
            print pa.shape
            print pb.shape
            print ("Ecken 0 0"
            print pa[0,0]
            print pb[0,0]
            print ("Eckebn -1 -1 "
            print pa[-1,-1]
            print pb[-1,-1]

            print ("Eckebn 0 1"
            print pa[0,-1]
            print pb[0,-1]
            print ("Eckebn 1 0"
            print pa[-1,0]
            print pb[-1,0]


        # pole morphen
        ka=obj.factorA
        kb=20-ka
        pc=(pa*ka+pb*kb)/20

        # spezielles addieren
        # pc[:,:,1] *= 2

        mu,mv=sfa.getUMultiplicities(),sfa.getVMultiplicities()
        bs=Part.BSplineSurface()

        bs.buildFromPolesMultsKnots(
                    pc,
                    mu,mv,range(len(mu)),range(len(mv)),
                    False,False,3,3)

        obj.Shape=bs.toShape()

    def myExecute(self,obj):
        print obj.Label," executed"


def createMorpher():
    '''create a moprhing between two bezier faces'''


    yy=App.ActiveDocument.addObject("Part::FeaturePython","Morpher")
    Morpher(yy)
    [yy.A,yy.B]=Gui.Selection.getSelection()
    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.6,.6,1.)
    yy.factorA=10
    return yy

# -----------curve morphed Face

class CurveMorpher(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLink","N","borders")
        obj.addProperty("App::PropertyLink","S","borders")
        obj.addProperty("App::PropertyLink","W","borders")
        obj.addProperty("App::PropertyLink","E","borders")
        obj.addProperty("App::PropertyLink","border","borders")
        obj.addProperty("App::PropertyBool","_showborders","borders")
        obj.addProperty("App::PropertyFloat","factorForce","config").factorForce=0
        obj.addProperty("App::PropertyFloat","factor2Force","config").factor2Force=0
        obj.addProperty("App::PropertyVector","pull","config").pull=App.Vector(0,0,0)  
        obj.addProperty("App::PropertyInteger","count","config").count=9
        obj.addProperty("App::PropertyInteger","degree","config").degree=3
        obj.addProperty("App::PropertyBool","curvesNS")
        obj.addProperty("App::PropertyBool","curvesWE")
        obj.addProperty("App::PropertyBool","faceNS")
        obj.addProperty("App::PropertyBool","faceWE")
        obj.addProperty("App::PropertyBool","flipA","config details")
        obj.addProperty("App::PropertyBool","flipB","config details")
        obj.addProperty("App::PropertyBool","flipAA","config details")
        obj.addProperty("App::PropertyBool","flipAB","config details")
        obj.addProperty("App::PropertyBool","flipBA","config details")
        obj.addProperty("App::PropertyBool","flipBB","config details")
        obj.addProperty("App::PropertyBool","_showconfigdetails","config details")
        obj.addProperty("App::PropertyBool","curveOnlyB","special")
        obj.addProperty("App::PropertyBool","curveOnlyA","special")
        obj.addProperty("App::PropertyFloat","curveAPosition","special").curveAPosition=50
        obj.addProperty("App::PropertyFloat","curveBPosition","special").curveBPosition=50
        
        obj.curvesNS=1
        obj.curvesWE=1
        obj.faceWE=0
        obj.curveOnlyA=0
        obj.flipB=1
        obj.flipAA=1
        obj.flipAB=1

        obj.addProperty("App::PropertyBool","_showspecial","special")
        obj._showspecial=False
        obj._showconfigdetails=False
        obj._showaux=False
        obj._showborders=False

    def myOnChangedA(self,obj,prop):

        if prop in ["Shape"]:
            return

        self.showprops(obj,prop)

        try:
            obj.factorForce,obj.curvesNS,obj.curvesWE,obj.faceNS,obj.faceWE
            obj.N.Shape,obj.S.Shape,obj.W.Shape,obj.E.Shape
            obj.curveAPosition,obj.curveBPosition,obj.pull
        except:
            return

        compsA=[]

        a=obj.S
        b=obj.N
        c=obj.W
        d=obj.E
        ca=a.Shape.Curve
        cb=b.Shape.Curve
        cc=c.Shape.Curve
        cd=d.Shape.Curve

        anz=obj.count

        ff=App

#        flip=0
#        if flip:
#            ca,cb,cc,cd=cc,cd,ca,cb

        def getmorph(A,B,ptsa,ptsb,u=0.5,ff=1.,helper=0,h2faktor=1):

            ptsa=np.array(ptsa)
            ptsb=np.array(ptsb)
            assert ptsa.shape == ptsb.shape    
            l=ptsa.shape[0]
            pts=u*ptsa+(1-u)*ptsb
            AA=pts[0].copy()
            BB=pts[-1].copy()
            ptsA=pts.copy()
            if helper:
                tname="helper"
                tt=App.ActiveDocument.getObject(tname)
                if tt==None:
                    tt=App.ActiveDocument.addObject('Part::Spline',tname)
                compsa=[]
                compsa +=[Part.makePolygon([App.Vector(p) for p in pts])]
                compsa +=[Part.makePolygon([App.Vector(AA),App.Vector(BB)])]

            h=(obj.factorForce+10)*0.1
            h2=-(obj.factor2Force)*0.1*h2faktor
            up=obj.pull*10

            for il in range(l):
                    D=(B*il+A*(l-1-il))/(l-1)
                    fa=((l-il-1.)/(l-1))**h if il!=l-1 else 0
                    fb=((il+0.)/(l-1))**h if il!=0 else 0
                    pts[il] -= (fa*(AA-A)  +fb*(BB-B))
                    if il!=l-1 and il !=0:
                        E=pts[il]-D
                        pts[il]=E*(1-h2)+D
                    pts[il] += up * il*(l-il-1)/l**2 * h2faktor

            if helper:
                compsa +=[Part.makePolygon([App.Vector(p) for p in pts])]
                tt.Shape=Part.Compound(compsa)

            # glaetten
            anz=(len(pts)-4)/2
            for i in range(anz):
                k=3*i+3
                p1=pts[k-1]
                p2=pts[k+1]
                p=pts[k]
                p1,p2= p +(p1-p2)/2,p +(p2-p1)/2
                pts[k-1],pts[k+1]=p1,p2

            return pts

        flipA=obj.flipAA
        flipB=obj.flipAB

        if obj.curveOnlyA:
            Arange=[0.01*obj.curveAPosition*anz]
        else:
            Arange=range(anz+1)

        for V in Arange:

            v=V/(anz+0.0)
            u=1-v
            ff=cc.getKnots()[-1]

            v=ff*V/(anz+0.0)
            u=1-V/(anz+0.0)

            ptsa=np.array(ca.getPoles())
            ptsb=np.array(cb.getPoles())

            if flipA:
                A=np.array(cc.value(ff-v))
            else:
                A=np.array(cc.value(v))
            if flipB:
                B=np.array(cd.value(ff-v))    
            else:
                B=np.array(cd.value(v))    

            if obj.flipA:
                A,B=B,A

            pts=getmorph(A,B,ptsa,ptsb,u,h2faktor=v*u)

            bc=Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(pts,ca.getMultiplicities(),ca.getKnots(),False,3)
            compsA += [bc.toShape()]

        ca,cb,cc,cd=cc,cd,ca,cb

        compsB=[]

        if obj.curveOnlyB:
            Brange=[0.01*obj.curveBPosition*anz]
        else:
            Brange=range(anz+1)

        flipA=obj.flipBA
        flipB=obj.flipBB

        
        for iV,V in enumerate(Brange):
            if not (obj.curvesWE or obj.faceWE):
                break

            ff=cc.getKnots()[-1]

            v=ff*V/(anz+0.0)
            u=1-V/(anz+0.0)

            ptsa=np.array(ca.getPoles())
            ptsb=np.array(cb.getPoles())

            if flipA:
                A=np.array(cc.value(ff-v))
            else:
                A=np.array(cc.value(v))
            if flipB:
                B=np.array(cd.value(ff-v))    
            else:
                B=np.array(cd.value(v))    

            if obj.flipB:
                A,B=B,A

            pts=getmorph(A,B,ptsa,ptsb,u,ff,h2faktor=v*u)

            bc=Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(pts,ca.getMultiplicities(),ca.getKnots(),False,3)
            compsB += [bc.toShape()]

        comps=[]
        if obj.curvesNS:
            comps  += compsA
        if obj.curvesWE:
            comps  += compsB
        if obj.faceNS:
            la=Part.makeLoft(compsA)
            comps += [la]
        if obj.faceWE or len(comps)==0:
            lb=Part.makeLoft(compsB)
            comps += [lb]

        obj.Shape=Part.Compound(comps)
#----------------------

    def myOnChangedBorder(self,obj,prop):

        if prop in ["Shape"]:
            return

        
        self.showprops(obj,prop)

#        try:
#            obj.factorForce,obj.curvesNS,obj.curvesWE,obj.faceNS,obj.faceWE
#            obj.N.Shape,obj.S.Shape,obj.W.Shape,obj.E.Shape
#            obj.curveAPosition,obj.curveBPosition,obj.pull
#        except:
#            return

        #faden in 4 teile zerlegen und dann daraus flaeche machen

        #sh=App.ActiveDocument.Sketch006.Shape
        sh=obj.border.Shape

        w=sh.Wires[0]
        pts=[v.Point for v in w.Vertexes]
#        print  (len(pts)


        # pts[0]=pts[-1]=(pts[0]+pts[-1])*0.5
        a=pts[0:4]
        b=pts[3:7]
        c=pts[6:10]
        d=pts[9:12]+[pts[0]]
#        for ps in [a,b,c,d]:
#            Part.show(Part.makePolygon(ps))

        import numpy  as np

        ptsarr=np.zeros(4*4*3).reshape(4,4,3)
        ptsarr[0]=a

        ptsarr[-1]=c[::-1]
        #ptsarr[-1]=c
        ptsarr=ptsarr.swapaxes(0,1)

#        print ptsarr[0,0]
#        print d[-1]
        ptsarr[0]=d[::-1]
#        print ptsarr[-1,0]
#        print b[0]

        ptsarr[-1]=b


        ptsarr[1,1:3]=(2*ptsarr[0,1:3]+ptsarr[3,1:3])/3
        ptsarr[2,1:3]=(ptsarr[0,1:3]+2*ptsarr[3,1:3])/3

        if 0:
            for ps in ptsarr:
                Part.show(Part.makePolygon([App.Vector(p) for p in ps]))

            ptsarr=ptsarr.swapaxes(0,1)

            for ps in ptsarr:
                Part.show(Part.makePolygon([App.Vector(p) for p in ps]))

        ptsarr[1:3,1:3] += obj.pull

        bs=Part.BSplineSurface()

        if obj.degree==1:
            bs.buildFromPolesMultsKnots(ptsarr,[2,1,1,2],[2,1,1,2],[0,1,2,3],[0,1,2,3],False,False,1,1)

        if obj.degree==2:
            bs.buildFromPolesMultsKnots(ptsarr,[3,1,3],[3,1,3],[0,1,2],[0,1,2],False,False,2,2)

        if obj.degree==3:
            bs.buildFromPolesMultsKnots(ptsarr,[4,4],[4,4],[0,1],[0,1],False,False,3,3)

        obj.Shape=bs.toShape()
        return

    def myOnChanged(self,obj,prop):
#        print prop
        if obj.border == None:
            self.myOnChangedA(obj,prop)
        else:
            self.myOnChangedBorder(obj,prop)
#----------------------

    def myExecute(self,obj):
        #return
        if not obj._noExecute:
            self.onChanged(obj,"__execute__")
        #print obj.Label," executed"

def curvemorphedFace():
    '''create a face by morphing boder curves'''
    yy=App.ActiveDocument.addObject("Part::FeaturePython","CurveMorpher")
    CurveMorpher(yy)

    curves=Gui.Selection.getSelection()
    if len(curves)==4:
        [yy.N,yy.S,yy.W,yy.E]=curves
    else:
        yy.border=curves[0]
    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.6,.6,1.)
    yy.ViewObject.LineColor=(.0,.6,0.)
    return yy


if __name__ == '__main__':
    #createMorpher()
    curvemorphedFace()





