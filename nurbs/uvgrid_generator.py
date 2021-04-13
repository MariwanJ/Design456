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
#-- uvgrid_generator.py
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

# generates 
# point clouds for curvature in u/v-direction
# face uv grid
# group with uv - unfolder and isoline grid 


from say import *
import Points


# test data
# /home/thomas/Dokumente/freecad_buch/b149_unfold/m09_uvgrid_generator.fcstd"

'''
import FreeCAD
App.open(u"/home/thomas/Dokumente/freecad_buch/b149_unfold/m09_uvgrid_generator.fcstd")
App.setActiveDocument("m09_uvgrid_generator")
App.ActiveDocument=App.getDocument("m09_uvgrid_generator")
Gui.ActiveDocument=Gui.getDocument("m09_uvgrid_generator")
'''

import nurbs_tools
#reload (nurbs_tools)
from .nurbs_tools import kruemmung



def uvmap(edges,sf,debug):


    try: uvgrp=App.ActiveDocument.UV
    except: uvgrp=App.ActiveDocument.addObject("App::DocumentObjectGroup","UV")

    ll=edges

    got=[0] * len(ll)

    ll2=[ll[0]]
    got[0]=1
    found=0

    for i in range(len(ll)):
        e=ll2[found]
        ps0= e.valueAt(e.FirstParameter)
        pe0= e.valueAt(e.LastParameter)
        for j in range(len(ll)):
            if got[j]: continue
            e=ll[j]
            ps1= e.valueAt(e.FirstParameter)
            pe1= e.valueAt(e.LastParameter)
            if ps1 in [ps0,pe0] or pe1 in [ps0,pe0]:
                ll2.append(e)
                found += 1
                got[j]=1
#                print (i,j,len(ll2))
                break
    assert(len(ll)==len(ll2))
    ll=ll2

    psa=None
    pea=None

    # genauigkeit
    anz=10
    
    pts=[]
    direct=[0] * len(ll)
    e=ll[0]
    ps0= e.valueAt(e.FirstParameter)
    pe0= e.valueAt(e.LastParameter)
    e=ll[1]
    ps1= e.valueAt(e.FirstParameter)
    pe1= e.valueAt(e.LastParameter)


    if pe0==pe1:
        # umdrehen
        direct[1]=1

    elif ps0==pe1:
        direct[1]=1
        direct[0]=1

    elif ps0==ps1:
        direct[0]=1
    else:
        assert(pe0==ps1)

    for i in range(1,len(ll)):
        e=ll[i-1]
        ps0= e.valueAt(e.FirstParameter)
        pe0= e.valueAt(e.LastParameter)
        e=ll[i]
        ps1= e.valueAt(e.FirstParameter)
        pe1= e.valueAt(e.LastParameter)
        if direct[i-1]:
            if pe1==ps0:
                direct[i]=1
            else:
                assert(ps0==ps1)
        else:
            if pe1==pe0:
                direct[i]=1
            else:
                assert(pe0==ps1)

    umin=1e+10
    vmin=umin
    umax=-1e+10
    vmax=umax


    for i,e in enumerate(ll):
    #        print (i,e.Curve)
            ps= e.valueAt(e.FirstParameter)
            pe= e.valueAt(e.LastParameter)
            #xprint (e.FirstParameter,e.LastParameter)
            #xprint (ps,pe)
            #xprint 
            
            pl=e.discretize(anz)
    #        Part.show(e)
            (u,v)=sf.parameter(e.Vertexes[0].Point)
            #xprint ("Start",u,v)
            vmax=max(vmax,v)
            umax=max(umax,u)
            vmin=min(vmin,v)
            umin=min(umin,u)


            (u,v)=sf.parameter(e.Vertexes[1].Point)
            #xprint ("Ende",u,v)
            vmax=max(vmax,v)
            umax=max(umax,u)
            vmin=min(vmin,v)
            umin=min(umin,u)

            ptst=[]
            kupts=[]
            kvpts=[]
            for p in pl:
                (u,v)=sf.parameter(p)
                ptst.append(App.Vector(u,v,0))
##                u=1*round(u,1)
##                v=1*round(v,1)

            if direct[i]:
                ptst.reverse()
            pts += ptst
            # Draft.makeWire(pts)


    poly=Part.Face(Part.makePolygon(pts,True))

    if debug: 
        Part.show(poly)
        # uvgrp.addObject(App.ActiveDocument.ActiveObject)

    for i,v in enumerate(pts):
        #xif i%5 == 0: print
        #xprint v
        pass

    return poly,umin,umax,vmin,vmax





def genVgrid(face,sf,gridfac=10,debug=False):
    poly=face
    if poly == None: return 

    try: uvgrp=App.ActiveDocument.UV
    except: uvgrp=App.ActiveDocument.addObject("App::DocumentObjectGroup","UV")


    sps=[]

    ust=18
    start=poly.BoundBox.YMin
    ende=poly.BoundBox.YMax
    ust=gridfac*int(round(poly.BoundBox.YMax-poly.BoundBox.YMin))+2

    mind=30
    if ust <mind: ust=mind 


    yl=[]
#    yl.append(start+0.001)
    for i in range(ust):
        yl.append(start+(ende-start)*i/ust)

#    yl.append(ende-0.001)

    rc=[]
    kupts=[]
    kvpts=[]

    vst=19

    anz1=vst
    
    kval=[]
    kual=[]
    
    for y in yl:
        vl=Part.makeLine((poly.BoundBox.XMin-1,y,0),(poly.BoundBox.XMax+1,y,0))
        if debug: 
            Part.show(vl)
            uvgrp.addObject(App.ActiveDocument.ActiveObject)


        start=poly.BoundBox.XMin
        ende=poly.BoundBox.XMax


        kul=[]
        kvl=[]
        for i in range(vst+1):
            v=y; u= start +(ende-start)*i/vst
            ku,kv=kruemmung(sf,u,v)
            kupts.append(App.Vector(u,v,10*ku))
            kvpts.append(App.Vector(u,v,10*kv))
            kul.append(App.Vector(u,v,10*ku))
            kvl.append(App.Vector(u,v,10*kv))
        kval.append(kvl)
        kual.append(kul)


        a=vl.distToShape(poly)
        #xprint y,a
        if a[0]>0.01 or  len(a[1])<2:
            #yprint ("keine schnittpunkte y ",y,a)
            pass
        else:
            anz1 += 1
            
            #xprint a[1]
            start=a[1][0][0][0]
            ende=a[1][-1][0][0]
##            print (start,ende)
            pts=[]

            for i in range(vst+1):
                pts.append(sf.value(start+(ende-start)*i/vst,y))

##            print pts
            spline = Part.BSplineCurve()
            spline.interpolate(pts, False)
            rc.append(spline.toShape())

    '''
    p=Points.Points(kupts)
    Points.show(p)
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,.0,1.0)
    App.ActiveDocument.ActiveObject.Label="U Curvature Map"

    p=Points.Points(kvpts)
    Points.show(p)
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,1.0,1.0)
    App.ActiveDocument.ActiveObject.Label="V Curvature Map"
    '''

    if 0:
        tt=Part.BSplineSurface()
        tt.interpolate(kual)
        sha=tt.toShape()
        Part.show(sha)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,.0,1.0)
        App.ActiveDocument.ActiveObject.Label="V Curvature Map"

        tt=Part.BSplineSurface()
        tt.interpolate(kval)
        sha=tt.toShape()
        Part.show(sha)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,1.0,1.0)
        App.ActiveDocument.ActiveObject.Label="U Curvature Map"

    return rc



def genUgrid(face,sf,gridfac=10,debug=False):
    ''' create u isolines '''
    poly=face
    if poly == None: return 

    try: uvgrp=App.ActiveDocument.UV
    except: uvgrp=App.ActiveDocument.addObject("App::DocumentObjectGroup","UV")

    sps=[]

    ust=gridfac*int(round(poly.BoundBox.XMax-poly.BoundBox.XMin))+2
    mind=30
    if ust <mind: ust=mind 
    print ("ust",ust)
    start=poly.BoundBox.XMin
    ende=poly.BoundBox.XMax
    yl=[]

    for i in range(ust):
        yl.append(start+(ende-start)*i/ust)

    rc=[]
    kupts=[]
    kvpts=[]

    for ix,x in enumerate(yl):
        vl=Part.makeLine((x,poly.BoundBox.YMin-1,0),(x,poly.BoundBox.YMax+1,0))

        if debug: 
            Part.show(vl)
            uvgrp.addObject(App.ActiveDocument.ActiveObject)


        a=vl.distToShape(poly)
        #xprint x,a

        start=poly.BoundBox.XMin
        ende=poly.BoundBox.XMax
        vst=19

        for i in range(vst+1):
            u=x; v= start +(ende-start)*i/vst
            ku,kv=kruemmung(sf,u,v)
    #                    if i >-10  :
    #                        if ku!=-1 and kv !=-1: 
#            print (u,v,ku,kv)
            if 0: # nicht fast ebenene Flaechen
                kupts.append(App.Vector(u,v,10*ku))
                kvpts.append(App.Vector(u,v,10*kv))
            else:
                p=sf.value(u,v)
                kupts.append(App.Vector(p.x,p.y,10000*ku))
                kvpts.append(App.Vector(p.x,p.y,10000*kv))
            


        if a[0]>0.01 or  len(a[1])<2:
            #yprint ("keine/zuviel  schnittpunkte x ",ix,x,len(a[1]),a[0],a)
            if len(a[1])>2:
                print 
                for p in a[1]:
                    print (p[0])
                print
        else:
                start=a[1][0][0][1]
                ende=a[1][-1][0][1]
                pts=[]

                for i in range(vst+1):
                    pts.append(sf.value(x,start+(ende-start)*i/vst))


                spline = Part.BSplineCurve()
                spline.interpolate(pts, False)
                ##Part.show(spline.toShape())
                ##App.ActiveDocument.ActiveObject.Label="huhu" + str(x)
                rc.append(spline.toShape())


#    p=Points.Points(kupts)
#    Points.show(p)
#    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,.0,1.0)

    print (len(kupts),len(kupts)/(vst+1))
    gengrid(kupts,vst+1,1)
    gengrid(kvpts,vst+1,2)

#    p=Points.Points(kvpts)
#    Points.show(p)
#    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,1.0,1.0)

    return rc

def piep(mess=None):
    if mess == None:
        mess=time.time()
    App.Console.PrintWarning(str(mess) +"\n")
    Gui.updateGui()

#----------------------
def genKgrid(face,umin,umax,vmin,vmax,mode,sf,gridfac=10,obj=None,debug=False):
    ''' create rectangles with curvature '''

    ts=time.time()

    poly=face
    if poly == None: return 

    gridz=20

    sps=[]

    ust=gridfac*int(round(poly.BoundBox.XMax-poly.BoundBox.XMin))+2
    
    mind=gridz
    if ust <mind: ust=mind 

    ust=gridz
    vst=gridz
    print ("ust",ust)


#    startx=poly.BoundBox.XMin
#    endex=poly.BoundBox.XMax

    startx=umin
    endex=umax

    start=vmin
    ende=vmax

    yl=[]

    for i in range(ust):
        yl.append(startx+(endex-startx)*i/ust)

    rc=[]
    kupts=[]
    kvpts=[]

    faces=[]
    colors=[]
    kvals=[]

    cmap = matplotlib.cm.get_cmap('jet')

    for ix,x in enumerate(yl):
        piep(("ix,x: ",ix,x))

        for i in range(vst+1):
            u=x; v= start +(ende-start)*i/vst
            ku,kv=kruemmung(sf,u,v)

            if mode =='v':
                kvals.append(10*kv)

            if mode == 'u':
                kvals.append(10*ku)

            if mode=='gauss':
                # zeigt gut die lage der pole
                # gausssche kruemmung
                kvals.append(10*ku*kv)

            if mode == 'sumabs':
                # mittlere Krümmung oder ist das ku+kv anstatt der abs ???
                kvals.append(10*(abs(ku)+abs(kv)))

            if mode == 'mean':
                kvals.append(10*(ku+kv))


            eu=(endex-startx)/ust/2
            ev=(ende-start)/vst/2


            p1=sf.value(u-eu,v-ev)
            p2=sf.value(u-eu,v+ev)
            p3=sf.value(u+eu,v+ev)
            p4=sf.value(u+eu,v-ev)

            pg2=Part.makePolygon([p1,p2,p3],True)
            fa=Part.Face(pg2)
            pg2=Part.makePolygon([p1,p3,p4],True)
            fa2=Part.Face(pg2)
            faces += [fa,fa2]

    Part.show(Part.makeSolid(Part.makeShell(faces)))

    kval2= [] + kvals
    kval2.sort()

    for c in kvals:
        ci=kval2.index(c)
        t=float(ci)/(len(kval2)-1)

        if mode == 'sumabs':
            t=0.5*(1+t)

        (r,g,b,a)=cmap(t)
        cc=(r,g,b)
        colors += [cc,cc]

    App.ActiveDocument.ActiveObject.ViewObject.DiffuseColor=colors
    App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = "Shaded"

    te=time.time()
    print ("color time ",round(te-ts,2))


def gengrid(pts,lena,direct=2):
    ''' creates a polygon grid for a point grid'''

    lenb=len(pts)//lena
    print ("erzeuge gitter",lena,"x",lenb,"punkte",len(pts)) 
    assert(lenb*lena==len(pts))
    pols=[]

    limit=3000

    if (direct==2):
        for u in range(lenb):
            uline=[]
            for v in range(lena):
                if abs(pts[u*lena+v].z) < limit:
                    uline.append(pts[u*lena+v])
                else:
                    p=pts[u*lena+v]
                    p.z=0
                    uline.append(p)

    if (direct==1):
        for v in range(lena):
            uline=[]
                # Feler am Rand
            if abs(pts[u*lena+v].z) < limit:
                    uline.append(pts[u*lena+v])
            else:
                    p=pts[u*lena+v]
                    p.z=0
                    uline.append(p)

    pol=Part.makePolygon(uline)
    pols.append(pol)

    com=Part.makeCompound(pols)
    Part.show(com)



def runobj(obj,fac=5):
    ''' run for one complete object over all of its faces'''

    ts=time.time()
    el=[]
    debug=1

    for f in obj.Shape.Faces:
        try:
            poly,umin,umax,vmin,vmax = uvmap(f.Edges,f.Surface,debug)
            print ("genkgrid" )
            mode= 'sumabs' # 'u','v', 'sumabs','gauss', 'mean'
            genKgrid(poly,umin,umax,vmin,vmax,mode ,f.Surface,fac,obj,debug)
            print ("DONE stop here - no grid generation")
            return
            l1=genVgrid(poly,f.Surface,fac,debug)
            l2=genUgrid(poly,f.Surface,fac,debug)
            el += l1 
            el += l2
        except:
            sayexc()

    for e in f.Edges:
        if e.Curve.__class__.__name__ == "GeomLineSegment":
            e=e.Curve.toShape()
        el.append(e)


    comp=Part.makeCompound(el)
    te=time.time()
    print ("Creation time ",round(te-ts,2))

    ts=time.time()
    Part.show(comp)
    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(random.random(),random.random(),random.random())
    te=time.time()
    print ("Part.show time ",round(te-ts,2))


def runsub(f,fac=5,label="NoLAB"):

    ts=time.time()

    el=[]
    debug=1

    try:
        poly=uvmap(f.Edges,f.Surface,debug)
        l2=[]
        l1=[]
        l1=genVgrid(poly,f.Surface,fac,debug)
        l2=genUgrid(poly,f.Surface,fac,debug)
        el += l1 
        el += l2
    except:
        sayexc()

    for e in f.Edges:
        if e.Curve.__class__.__name__ == "GeomLineSegment":
            e=e.Curve.toShape()
        el.append(e)

    App.ActiveDocument.recompute()
    
    comp=Part.makeCompound(el)
    te=time.time()
    print ("Creation time ",round(te-ts,2))

    ts=time.time()
    Part.show(comp)
    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(random.random(),random.random(),random.random())
    App.ActiveDocument.ActiveObject.Label=label
    te=time.time()
    print ("Part.show time ",round(te-ts,2))



def runSel(fac=3):
    ''' create the xxx for some selected faces or all faces of a selected part'''

    if len(Gui.Selection.getSelectionEx())>0:
        for ss in Gui.Selection.getSelectionEx():
            subn=ss.SubElementNames
            if len(subn)>0:
                for i,obj in enumerate(ss.SubObjects):
                    label=ss.ObjectName + " " + subn[i] + " UVGrid "
                    print ("create  ",label, "for ",obj.Surface)
                    runsub(obj,fac,label)
                    
            else:
                print("create for all faces of the object",ss.Object.Label)
                obj=ss.Object
                runobj(obj,fac)


def run():
    runSel()
