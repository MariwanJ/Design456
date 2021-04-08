'''
shoe sole creation

'''


# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create a shoe sole
#--
#-- microelly 2017 v 0.8
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
#\cond

__version__ = '0.12'

from say import  *

import Part,Mesh,Draft,Points


import random

import os, nurbswb

global __dir__
__dir__ = os.path.dirname(nurbswb.__file__)
print ( __dir__)
import numpy as np
#\endcond

# 12 divisions 

import nurbswb.spreadsheet_lib
reload (nurbswb.spreadsheet_lib)
from nurbswb.spreadsheet_lib import ssa2npa, npa2ssa, cellname


def runA(model=None):
    '''
    create or update a sole environment:
    spreadsheet, 
    
    
    '''


    # von andre daten 30.04.

    import Part,Draft

    points_list = [       
                   [0,0,18],
                   [-22,12,17],

                   [-28,44,16],
                   [-30,66,15],

                   [-32,88,11],
                   [-33,95,10],           

                   [-34,110,8],
                   [-39,132,5],

                   [-43,163,0],
                   [-42,196,2],
                   [-37,218,5],
                   [-24,240,9],
                   [ 9,258,14],

                   [36,240,9],
                   [42,218,5],
                   [45,196,2],
                   [43,174,1],
                   [32,147,2],
                   [28,132,5],
                   [23,110,8],
                   [22,95,10],
                   [20,88,11],
                   [22,66,15],
                   [25,44,16],
                   [26,22,17],
                   [22,12,17],
                   
               ]




    try: 
        try:
            [ss]=FreeCADGui.Selection.getSelection()
            print ("Selection",ss.Label)
            if ss.__class__.__name__ !='Sheet':
                print ("not a spreadsheet")
                raise Exception("selection is not a spreadsheet")
        except:
            ss=App.ActiveDocument.Spreadsheet
    except: 
        ss=App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')


        App.activeDocument().recompute()

        import nurbswb.sole_models
        reload(nurbswb.sole_models)
        model=nurbswb.sole_models.model()

    if 0: # "punktelisten anzeigen"
        p=Draft.makeWire([App.Vector(p[0],-p[1],p[2]) for p in points_list])
        p.Placement.Rotation.Angle=np.pi/2



    ss.set("A1","Sohle")
    ss.set("C1","LL")
    ss.set("A8","Divisionen")
    npa2ssa(np.arange(1,13).reshape(1,12),ss,2,8)
    ss.set("A18","Spitze")
    ss.set("A19","  length -LL")
    ss.set("A20","  left/right")
    ss.set("A21","  height")
    ss.set("A23","Ferse")
    ss.set("A24","  length")
    ss.set("A25","  left/right")
    ss.set("A26","  height")
    ss.set("A9","Height A")
    ss.set("A10","Length")
    ss.set("A14","Width right")
    ss.set("A15","Width left")

    highd=[0]*13
    highe=[0]*7

    if model!=None:
        print ("load model -------------------------")
        print (model)
        LL=model.LL
        LS=model.LS
        div12=model.div12
        tt=np.array(model.tt)

        print ("Fehler dubug ...")
        App._debug_LL=LL
        App._debug_tt=tt
        print (LL)
        print (tt[0,:,0])
        print ("End debug")

        tt[0,:,0] += LL

        tf=model.tf

        weia=model.weia
        weib=model.weib

        higha=model.higha
        highb=model.highb
        highc=model.highc
        highd=model.highd
        highe=model.highe

        ss.set("D1",str(LL))
        npa2ssa(np.array(tt[0]).swapaxes(0,1),ss,2,19)
        npa2ssa(np.array(tf[0]).swapaxes(0,1),ss,2,24)
        npa2ssa(np.array(higha).reshape(1,13),ss,2,9)
        print (np.array(weia).shape)
        print (np.array(weib).shape)
        npa2ssa(np.array(weia).reshape(1,13),ss,2,14)
        npa2ssa(np.array(weib).reshape(1,13),ss,2,15)
        npa2ssa(np.array(div12).reshape(1,12),ss,2,10)

    else:
        print (" load from spreadsheet---------------------")
        LL=244.0
        LS=LL+30
        div12=[round(LL/11*i,1) for i in range(12)]

        highb=[17,17,16,15,11,10,8,4,2,1,2,5,9,14]
        highc=[17,17,16,15,25,35,35,15,5,1,2,5,9,14]

        App.activeDocument().recompute()

        tf=[ssa2npa(ss,2,24,8,26,default=None).swapaxes(0,1)]
        tt=np.array([ssa2npa(ss,2,19,8,21,default=None).swapaxes(0,1)])
        
        print ("tt,LL",tt,LL)
        # tt[0,:,0] += LL
        # print ("LL,",LL

        higha=ssa2npa(ss,2,9,2+12,9,default=None)[0]
        weia=ssa2npa(ss,2,14,2+12,14,default=None)[0]
        weib=ssa2npa(ss,2,15,2+12,15,default=None)[0]

    App.activeDocument().recompute()

    rand=True
    bh=0 # randhoehe
    bw=0.1 # randbreite


    sh=5 # sohlenhoehe

#    bh=400
#    sh=10
    bw=0.0


    # prgramm parameter
    # grad der flaechen
    du=3
    dv=3
    drawisolines=False
    drawwires=False

    #-----------------------------------------------------------------------------

    # hilfslinien
    la=[[div12[i],-100,higha[i]] for i in range(12)]
    lb=[[div12[i],100,highb[i]] for i in range(12)]
    lc=[[div12[i],80,highc[i]] for i in range(12)]

#    try: App.getDocument("Unnamed")
#    except: App.newDocument("Unnamed")
#    
#    App.setActiveDocument("Unnamed")
#    App.ActiveDocument=App.getDocument("Unnamed")
#    Gui.ActiveDocument=Gui.getDocument("Unnamed")

    if drawwires:
        import Draft
        wa=Draft.makeWire([App.Vector(tuple(p)) for p in la])
        wa.ViewObject.LineColor=(.0,1.,.0)

        wb=Draft.makeWire([App.Vector(tuple(p)) for p in lb])
        wb.ViewObject.LineColor=(1.,0.,.0)

        wc=Draft.makeWire([App.Vector(tuple(p)) for p in lc])
        wc.ViewObject.LineColor=(1.,1.,.0)

    # siehe auch https://forum.freecadweb.org/viewtopic.php?f=3&t=20525&start=70#p165214


    pts2=[]
#    print ("Koordianten ..."
#    print highd
    for i in range(13):
        if i!=12:
            x=div12[i]
            h=higha[i]
            hc=highc[i]
            
        if i == 0:
            # fersenform
            #tf=[[[16,26,h],[8,18,h],[4,9,h],[0,0,h],[4,-7,h],[8,-14,h],[18,-22,h]]]
            pts2 += tf 
#            print (i,tf)
        elif i == 12:
            # Spitze
            # spitzenform
            #tt=[[[LS-15,35,h],[LS-8,28,h],[LS-5,14,h],[LS,0,h],[LS-5,-15,h],[LS-8,-20,h],[LS-15,-35,h]]]
            # pts2 += tt 
            pts2.append(tt[0])
#            print ("XX",i,tt)
        else:
            # mit innengewoelbe
            # pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6,h if j!=0 else hc] for j in range(7)]]
            
            pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6,h ] for j in range(7)]]
            
            
            # spielerei mit tiefer legen
            #pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6,h if  j not in [3,4] else h+highd[i]*highe[j] ] for j in range(7)]]
            #pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6, h+highd[i]*highe[j] ] for j in range(7)]]


#            print (i,round(x,1),h,weib[i],weia[i])


    pts2=np.array(pts2)
#    print ("--------------", pts2.shape

    cv=len(pts2)
    cu=len(pts2[0])
    #print pts2.round()
#    print (cv,cu)

    kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
    kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

    mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
    mu=[du+1]+[1]*(cu-du-1)+[du+1]

    bs=Part.BSplineSurface()

    bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )

    try: fa=App.ActiveDocument.orig
    except: fa=App.ActiveDocument.addObject('Part::Spline','orig')

    fa.Shape=bs.toShape()
    fa.ViewObject.ControlPoints=True




    if rand:

        pts0=np.array(pts2).swapaxes(0,1)

        l=np.array(pts0[0])
        l[1:-1,1] += bw
        l[1:-1,2] += bh

        r=np.array(pts0[-1])
        r[1:-1,1] -= bw
        r[1:-1,2] += bh

        pts2=np.concatenate([[l],[pts0[0]],pts0[1:],[r]])



        pts0=np.array(pts2).swapaxes(0,1)

        l=np.array(pts0[0])
        l[:,0] -= bw
        l[:,2] += bh

        pts0[0,0,2] += bh
        pts0[0,0,0] -= bw

        pts0[0,-1,2] += bh
        pts0[0,-1,0] -= bw

        r=np.array(pts0[-1])

        r[:,0] += bw
        r[:,2] += bh

        pts0[-1,0,2] += bh
        pts0[-1,0,0] += bw

        pts0[-1,-1,2] += bh
        pts0[-1,-1,0] += bw

        pts2=np.concatenate([[l],[pts0[0]],pts0[1:],[r]])




    cv=len(pts2)
    cu=len(pts2[0])

    kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
    kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

    mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
    mu=[du+1]+[1]*(cu-du-1)+[du+1]

    bs=Part.BSplineSurface()


    pts2[:,0,2]=100
    pts2[:,-1,2]=100
    pts2[0,:,2]=100
    pts2[-1,:,2]=100
    


    bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
                False,False,
                dv,du,
            )



    if 1:
        try: fa= App.ActiveDocument.up
        except: fa=App.ActiveDocument.addObject('Part::Spline','up')

        fa.Shape=bs.toShape()
        # fa.ViewObject.ControlPoints=True


    if drawisolines:
        for k in kus:
            Part.show(bs.vIso(k).toShape())

        for k in kvs:
            Part.show(bs.uIso(k).toShape())


    coll=[]
    for pts in pts2:
        coll += [Part.makePolygon([App.Vector(p) for p in pts])]

    Part.show(Part.Compound(coll))
    
    
#    print ("cancellation HIER"
#    return



    if 1:


        pts2[:,:,2] -= sh

        pts3=pts2

        # fuess gewoelbe wieder runter
        '''
        pts3[4,-1,2]=14
        pts3[4,-2,2]=14

        pts3[5,-1,2]=10
        pts3[5,-2,2]=10

        pts3[6,-1,2]=6
        pts3[6,-2,2]=6
        '''


        cv=len(pts2)
        cu=len(pts2[0])

        kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
        kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

        mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
        mu=[du+1]+[1]*(cu-du-1)+[du+1]

        bs=Part.BSplineSurface()

        bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
                    False,False,
                    dv,du,
                )



        try: fb= App.ActiveDocument.inner
        except: fb=App.ActiveDocument.addObject('Part::Spline','inner')

        fb.Shape=bs.toShape()
        # fb.ViewObject.ControlPoints=True

        try:  loft=App.ActiveDocument.sole
        except: loft=App.ActiveDocument.addObject('Part::Loft','sole')

        loft.Sections=[fa,fb]
        loft.Solid=True
        loft.ViewObject.ShapeColor=(.0,1.,.0)
        App.activeDocument().recompute()

        for f in loft.Sections:
            f.ViewObject.hide()


## prototype create a heel
# absatz ninten und vorne, erste experimente

def createheel():

        points=[App.Vector(30.0, 11.0, 0.0), App.Vector (65., 5., 0.0), 
            App.Vector (60., -10., 0.0), App.Vector (19., -13., 0.0)]
        spline = Draft.makeBSpline(points,closed=True,face=True,support=None)


        s=spline.Shape.Edge1
        f=App.ActiveDocument.orig.Shape.Face1

        p=f.makeParallelProjection(s, App.Vector(0,0,1))
        Part.show(p)
        proj=App.ActiveDocument.ActiveObject

        clone=Draft.clone(spline)
        clone.Placement.Base.z=-100
        clone.Scale=(0.4,0.5,1.)


        loft=App.ActiveDocument.addObject('Part::Loft','Loft')
        loft.Sections=[proj,clone]


        points = [App.Vector(165.,-7.,-00.0),App.Vector(208.,-25.,-00.0),App.Vector(233.,20.,-00.0)]
        spline = Draft.makeBSpline(points,closed=True,face=True,support=None)


        s=spline.Shape.Edge1
        f=App.ActiveDocument.orig.Shape.Face1

        p=f.makeParallelProjection(s, App.Vector(0,0,1))
        Part.show(p)
        proj=App.ActiveDocument.ActiveObject

        clone=Draft.clone(spline)
        clone.Placement.Base.z=-100

        loft=App.ActiveDocument.addObject('Part::Loft','Loft')
        loft.Sections=[proj,clone]


        App.activeDocument().recompute()
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.SendMsgToActiveView("ViewFit")


        print ("okay")


## create sole and infrastructure models
def run():
    runA()
#    createheel()



if __name__=='__main__':
    run()

