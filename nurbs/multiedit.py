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

'''
multiple bspline faces editor
'''
# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- multiple bspline faces editor
#--
#-- microelly 2018
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


# pylint: disable=W0331
# pylint: disable=unused-import
# pylint: disable=invalid-name
# xpylint: disable=bare-except
# xpylint: disable=exec-used

'''
multiple bspline faces editor
'''

import FreeCAD,Part
import FreeCADGui as Gui 

import NURBSinit
import os

try:
    import numpy as np 
except ImportError:
    print("Numpy library is missing, please install it before using the library")
    
import time,random
App=FreeCAD

import configuration
#reload (.configuration)
from .configuration import getcf,getcb,getcs,setcb,setcf,setcs



# constraints
'''
obj=App.ActiveDocument.addObject('Part::FeaturePython','BePlane')
obj.addProperty("App::PropertyIntegerConstraint","u","huu").u=13
obj.u = (30,0,1000,100)

LowerBound    
UpperBound    
StepSize    

'''


faces=Gui.Selection.getSelectionEx()
print (faces)

 
import say


class Point(object):
    def __init__(self,point,sf,f):
        self.point=point
        self.sfs=[sf]
        self.fs=[f]

    def addsf(self,sf,f):
        self.sfs += [sf]
        self.fs += [f]

    def printFaces(self):
        print (self.point)
        for f in self.fs:
            print (f.Label," ",)
        print

def editcross(poles,u,v):
    '''create an object of curves to display the selected area u,v of the poles under focus of the editor'''
    comps=[]
    uu,vv=u,v

#    v -=1
#    print ("editcross------------------",u,v,poles.shape)
    uc,vc,_=poles.shape
    umi=max(u-3,0)
    uma=min(uc-1,u+3)
    vmi=max(v-3,0)
    vma=min(vc-1,v+3)
#    print  (umi,uma,vmi,vma)
    s=Part.Sphere()
#    s.Radius=20
    s.Radius=(App.Vector(poles[uma,vma])-App.Vector(poles[umi,vmi])).Length*0.01
    ss=s.toShape()
    ss.Placement.Base=App.Vector(poles[u,v])+App.Vector(11,11,11)
    comps += [ss]


    for u in range(umi,uma):
        if u%3==0:
            for v in range(vmi,vma+1):
                if v%3==0:
                    bc=Part.BSplineCurve()
                    bc.buildFromPolesMultsKnots(poles[u:u+4,v],[4,4],[0,1],False,3)
                    comps += [bc.toShape()]
    for u in range(umi,uma+1):
        if u%3==0:
            for v in range(vmi,vma):
                if v%3==0:
                    bc=Part.BSplineCurve()
                    bc.buildFromPolesMultsKnots(poles[u,v:v+4],[4,4],[0,1],False,3)
                    comps += [bc.toShape()]
    for u in range(umi,uma+1):
            for v in range(vmi,vma):
                    if uu==u and vv==v: continue
                    try:
                        ve=(App.Vector(poles[u,v])-App.Vector(poles[uu,vv])).normalize()*(-1)
                        v0=App.Vector(poles[uu,vv])
                        comps += [Part.makePolygon([v0+10*ve,v0+50*ve])]
                    except:
                        print ("problem editcross polygon")

    return comps


class Multiface(object):
    def __init__(self):
        self.faces=faces
        self.nameF="tmp_multiFace"
        self.nameP="tmp_poles"
        self.nameE="tmp_edit"
        self.createHelper()
        self.selection=[]
        self.compe=[]
        
    def createHelper(self):
        comp=[]

        obj2=App.ActiveDocument.getObject(self.nameP)
        if obj2==None:
            #obj2=App.ActiveDocument.addObject("Part::Compound","Compound")
            obj2=App.ActiveDocument.addObject('Part::Feature',self.nameP)

            obj2.Placement.Base=App.Vector(1,1,1)

            obj2.ViewObject.PointColor=(1.0,0.6,0.8)
            obj2.ViewObject.PointSize=6


        obj3=App.ActiveDocument.getObject(self.nameE)
        if obj3==None:
            #obj2=App.ActiveDocument.addObject("Part::Compound","Compound")
            obj3=App.ActiveDocument.addObject('Part::Feature',self.nameE)
            obj3.ViewObject.LineColor=(1.0,0.,0.)
            obj3.ViewObject.ShapeColor=(1.0,1.,0.)
            obj3.ViewObject.LineWidth=3



        obj=App.ActiveDocument.getObject(self.nameF)
        if obj==None:
            #obj=App.ActiveDocument.addObject("Part::Compound","Compound")
            #obj=App.ActiveDocument.addObject('Part::Feature',self.nameF)
            obj=App.ActiveDocument.addObject('Part::Spline',self.nameF)
            obj.ViewObject.Selectable=False
            obj.ViewObject.Transparency=70
            obj.ViewObject.ShapeColor=(1.0,0.3,0.2)
            for ff in self.faces:
                print (ff.Label)
                ff.ViewObject.hide()
                comp += ff.Shape.Faces
            obj.Shape=Part.Compound(comp)
        else:
            print ("!!!!!!!!!!!!###") #,obj.Shape.Faces
#            print App.ActiveDocument.tmp_multiFace.Shape.Faces
            for ff in obj.Shape.Faces:
                comp += [ff]
#                print comp
        self.faceobj=obj
        self.comp=comp
#        print comp
        print ("helper created")


    def getPoints(self):
        points={}
        for f in faces:
            sf=f.Shape.Face1.Surface
            poles=[v.Point for v in f.Shape.Vertexes]
            for p in poles:
                t=tuple(p)
                try: 
                    points[t].addsf(sf,f)
                except:
                    points[t]=Point(p,sf,f)
#        print ("getPoints",len(points)
        self.points=points

    def findPoint(self,vec):
        print ("findpoint ",vec)
        try: 
            t=tuple(vec)
            pp=self.points[t]
            pp.printFaces()
        except:
            print ("nicht gefunden")
        for i,p in enumerate(self.points):
            print (i,(vec-App.Vector(p)).Length)
            if (vec-App.Vector(p)).Length<0.1 :
                print ("gefunden ",i)
                return App.Vector(p)

    def movePoint(self,vec,mov,scanonly=False,params=None):
            points=self.points
            #print ("Move points........"


            ms=getcf("moveScale")
            if ms==0:
                setcf("moveScale",1.0)
                ms=1

            arc=50-random.random()*100
            arc=0

            comp=[]
            compe=self.compe
            pts=[]

            if params != None:
                mov=App.Vector(
                    params.root.ids['xdial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['ydial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['zdial'].value()*params.root.ids['scale'].value(),
                )
#            upn=int(self.root.ids['ux'].text())
#            vpn=int(self.root.ids['vx'].text())
                mov *= ms

            for sfi,sfa in enumerate(self.comp):
                try:
                #if 1:
                    ta=time.time()
                    sf=sfa.Surface
#                    print (self.faces[sfi].Label,"###################",sfi)
                    poles=np.array(sf.getPoles()).reshape(sf.NbUPoles*sf.NbVPoles,3)
                    found=-1
                    for i,p in enumerate(poles):
                        if vec != None  and (vec-App.Vector(p)).Length<0.1 :
#                            print ("gefunden ",i
                            found=i
                    if found == -1:
#                        print ("NICHT gefunden /kein Vector"
                        comp += [self.comp[sfi]]
                    else:
                        base=poles[found]
                        #poles[found]=vec+mov


                        vi=found % sf.NbVPoles
                        ui=found // sf.NbVPoles

                        self.selection += [(sfi,ui,vi,base.copy())]

                        pps=[(ui,vi)]
                        pps=[]
                        umi=max(ui-1,0)
                        uma=min(sf.NbUPoles-1,ui+1)
                        vmi=max(vi-1,0)
                        vma=min(sf.NbVPoles-1,vi+1)
                        
                        pps += [(uk,vk) for uk in range(umi,uma+1) for vk in range(vmi,vma+1)]

                        if 0:
                            if ui>0 and ui<sf.NbUPoles-1:
                                pps +=[(ui-1,vi),(ui+1,vi)]
                            if vi>0 and vi<sf.NbVPoles-1:
                                pps +=[(ui,vi-1),(ui,vi+1)]

                            if ui==0: 
        #                        print ("south"
                                pps +=[(ui+1,vi)]
                            if vi==0:
        #                        print ("west"
                                pps +=[(ui,vi+1)]
                            if ui==sf.NbUPoles-1:
        #                        print ("north"
                                pps +=[(ui-1,vi)]
                            if vi==sf.NbVPoles-1:
        #                        print ("east"
                                pps +=[(ui,vi-1)]

                        poles=poles.reshape(sf.NbUPoles,sf.NbVPoles,3)
    #                    print ("nachbarn ",pps
                        # nachbaren mitnehmen
                        
                        print ("tangent rotations !!!")
                        turot=params.root.ids['turot'].value()
                        tvrot=params.root.ids['tvrot'].value()
                        
                        print (turot,tvrot)
                        
                        for (u,v) in pps:
    #                        print (u,v)
                            
                            rot=App.Rotation(arc,0,0)
                            vv=App.Vector(poles[u,v]-base)
                            vv=rot.multVec(vv)
                            # vv *= 3.
                            poles[u,v] =base+vv+mov



                        compe += editcross(poles,ui,vi)

                        ptsa=[[3*uii,3*vii] for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                        if scanonly:
                            poles=np.array(sf.getPoles())


                        ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]

                        ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                        pts += [App.Vector(p) for p in ptsa]


                        bs=Part.BSplineSurface()
                        bs.buildFromPolesMultsKnots(poles,
                                sf.getUMultiplicities(),sf.getVMultiplicities(),
                                sf.getUKnots(),sf.getVKnots(),
                                False,False,sf.UDegree,sf.VDegree,sf.getWeights())

                        comp += [bs.toShape()]
#                    print ("Time step ",time.time()-ta
                except:
                #else:
                    print ("Problem bei ",sfi)
                    saysayexc("sfi-problem")
                    comp += [self.comp[sfi]]

                poles=np.array(sf.getPoles())

                ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                pts += [App.Vector(p) for p in ptsa]

                



            ta=time.time()
            obj=App.ActiveDocument.getObject(self.nameF)
            obj.Shape=Part.Compound(comp)

#            print ("Time compA  ",time.time()-ta
            ta=time.time()
            obj2=App.ActiveDocument.getObject(self.nameP)
            pm=obj2.Placement
            comp2=[Part.Vertex(App.Vector(p)) for p in pts]
            obj2.Shape=Part.Compound(comp2)
            obj2.Placement=pm

            obj3=App.ActiveDocument.getObject(self.nameE)
            if len(compe)!=0:
                obj3.Shape=Part.Compound(compe)
            else:
                obj3.Shape=Part.Shape()
            
            self.comp=comp


            print ("Time compB  ",time.time()-ta)

            if 0:
                ta=time.time()
                obj=App.ActiveDocument.getObject(self.nameF)
                for c in comp:
                    Part.show(c)
                print ("Time compC  ",time.time()-ta)


    # neue version ohne suchen
    def XmovePoint(self,vec,mov,scanonly=False,params=None,useselections=False):
            points=self.points
            print ("Move points...XXX.....")
#            print ("suche ", vec

            print ("useselections ",useselections)
            
            arc=50-random.random()*100
            arc=0

            comp=[]
            compe=self.compe
            pts=[]

            if params != None:
                mov=App.Vector(
                    params.root.ids['xdial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['ydial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['zdial'].value()*params.root.ids['scale'].value(),
                )
#            upn=int(self.root.ids['ux'].text())
#            vpn=int(self.root.ids['vx'].text())


            if not useselections:
                for sfi,sfa in enumerate(self.comp):
                    try:
                    #if 1:
                        ta=time.time()
                        sf=sfa.Surface
    #                    print (self.faces[sfi].Label,"###################",sfi)
                        poles=np.array(sf.getPoles()).reshape(sf.NbUPoles*sf.NbVPoles,3)
                        found=-1
                        for i,p in enumerate(poles):
                            if vec != None  and (vec-App.Vector(p)).Length<0.1 :
    #                            print ("gefunden ",i
                                found=i
                        if found == -1:
    #                        print ("NICHT gefunden /kein Vector"
                            comp += [self.comp[sfi]]
                        else:
                            base=poles[found]
                            #poles[found]=vec+mov


                            vi=found % sf.NbVPoles
                            ui=found // sf.NbVPoles

                            self.selection += [(sfi,ui,vi,base.copy())]

                            pps=[(ui,vi)]
                            pps=[]
                            umi=max(ui-1,0)
                            uma=min(sf.NbUPoles-1,ui+1)
                            vmi=max(vi-1,0)
                            vma=min(sf.NbVPoles-1,vi+1)
                            
                            pps += [(uk,vk) for uk in range(umi,uma+1) for vk in range(vmi,vma+1)]

                            if 0:
                                if ui>0 and ui<sf.NbUPoles-1:
                                    pps +=[(ui-1,vi),(ui+1,vi)]
                                if vi>0 and vi<sf.NbVPoles-1:
                                    pps +=[(ui,vi-1),(ui,vi+1)]

                                if ui==0: 
            #                        print ("south"
                                    pps +=[(ui+1,vi)]
                                if vi==0:
            #                        print ("west"
                                    pps +=[(ui,vi+1)]
                                if ui==sf.NbUPoles-1:
            #                        print ("north"
                                    pps +=[(ui-1,vi)]
                                if vi==sf.NbVPoles-1:
            #                        print ("east"
                                    pps +=[(ui,vi-1)]

                            poles=poles.reshape(sf.NbUPoles,sf.NbVPoles,3)
        #                    print ("nachbarn ",pps
                            # nachbaren mitnehmen
                            for (u,v) in pps:
        #                        print (u,v)
                                
                                rot=App.Rotation(arc,0,0)
                                vv=App.Vector(poles[u,v]-base)
                                vv=rot.multVec(vv)
                                # vv *= 3.
                                poles[u,v] =base+vv+mov



                            compe += editcross(poles,ui,vi)

                            ptsa=[[3*uii,3*vii] for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                            if scanonly:
                                poles=np.array(sf.getPoles())


                            ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]

                            ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                            pts += [App.Vector(p) for p in ptsa]


                            bs=Part.BSplineSurface()
                            bs.buildFromPolesMultsKnots(poles,
                                    sf.getUMultiplicities(),sf.getVMultiplicities(),
                                    sf.getUKnots(),sf.getVKnots(),
                                    False,False,sf.UDegree,sf.VDegree,sf.getWeights())

                            comp += [bs.toShape()]
    #                    print ("Time step ",time.time()-ta
                    except:
                    #else:
                        print ("Problem bei ",sfi)
                        saysayexc("sfi-problem")
                        comp += [self.comp[sfi]]

                    poles=np.array(sf.getPoles())

                    ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                    ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                    pts += [App.Vector(p) for p in ptsa]

            else:
                print ("useselections")
                print (self.selection)
            #--------------------------------------------
                for (sfi,ui,vi,p) in self.selection:
                        sf=self.comp[sfi].Surface
                        poles=np.array(sf.getPoles())
                        base=poles[ui,vi]

                        pps=[(ui,vi)]
                        pps=[]
                        umi=max(ui-1,0)
                        uma=min(sf.NbUPoles-1,ui+1)
                        vmi=max(vi-1,0)
                        vma=min(sf.NbVPoles-1,vi+1)

                        pps += [(uk,vk) for uk in range(umi,uma+1) for vk in range(vmi,vma+1)]

                        if 0:
                                if ui>0 and ui<sf.NbUPoles-1:
                                    pps +=[(ui-1,vi),(ui+1,vi)]
                                if vi>0 and vi<sf.NbVPoles-1:
                                    pps +=[(ui,vi-1),(ui,vi+1)]

                                if ui==0: 
            #                        print ("south"
                                    pps +=[(ui+1,vi)]
                                if vi==0:
            #                        print ("west"
                                    pps +=[(ui,vi+1)]
                                if ui==sf.NbUPoles-1:
            #                        print ("north"
                                    pps +=[(ui-1,vi)]
                                if vi==sf.NbVPoles-1:
            #                        print ("east"
                                    pps +=[(ui,vi-1)]

                        for (u,v) in pps:
                            rot=App.Rotation(arc,0,0)
                            vv=App.Vector(poles[u,v]-base)
                            vv=rot.multVec(vv)
                            poles[u,v] =base+vv+mov

                            compe += editcross(poles,ui,vi)

                            ptsa=[[3*uii,3*vii] for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                            if scanonly:
                                poles=np.array(sf.getPoles())

                            ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]

                            ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                            pts += [App.Vector(p) for p in ptsa]


                            bs=Part.BSplineSurface()
                            bs.buildFromPolesMultsKnots(poles,
                                    sf.getUMultiplicities(),sf.getVMultiplicities(),
                                    sf.getUKnots(),sf.getVKnots(),
                                    False,False,sf.UDegree,sf.VDegree,sf.getWeights())

                            comp += [bs.toShape()]

                        poles=np.array(sf.getPoles())

                        ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
                        ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                        pts += [App.Vector(p) for p in ptsa]


            #--------------------------------------------

            ta=time.time()
            obj=App.ActiveDocument.getObject(self.nameF)
            obj.Shape=Part.Compound(comp)

#            print ("Time compA  ",time.time()-ta
            ta=time.time()
            obj2=App.ActiveDocument.getObject(self.nameP)
            pm=obj2.Placement
            comp2=[Part.Vertex(App.Vector(p)) for p in pts]
            obj2.Shape=Part.Compound(comp2)
            obj2.Placement=pm


            obj3=App.ActiveDocument.getObject(self.nameE)
            obj3.Shape=Part.Compound(compe)

#            self.comp=comp


            print ("Time compB  ",time.time()-ta)

            if 0:
                ta=time.time()
                obj=App.ActiveDocument.getObject(self.nameF)
                for c in comp:
                    Part.show(c)
                print ("Time compC  ",time.time()-ta)


    def update(self,params,force):
        
        mov=App.Vector(
                    params.root.ids['xdial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['ydial'].value()*params.root.ids['scale'].value(),
                    params.root.ids['zdial'].value()*params.root.ids['scale'].value(),
                )

        rot=App.Rotation(
                    params.root.ids['xrot'].value(),
                    params.root.ids['yrot'].value(),
                    params.root.ids['zrot'].value(),
        )



        compe=[]
        comp=[c for c in self.comp]

        if params.root.ids['centerofmass'].isChecked():

            ps=App.Vector()
            for s in self.selection:
                print (s)
                [ci,ui,vi]=s[0:3]
                pp=comp[ci].Surface.getPoles()
                p=pp[ui][vi]
                ps +=p 
            ps *= 1.0/len(self.selection)
            com=ps




        print ("SELECTION LOOP")
        for sel in self.selection:
            si,ui,vi,p=sel
            print( si)
            print (comp[si])
            poles=np.array(comp[si].Surface.getPoles())
            print (poles[ui,vi])
            base=App.Vector(poles[ui,vi])
            print (p)
            print ("------------------")
        
            sf=comp[si].Surface
            print ("position",ui,vi)

            print (sf.getUKnots())
            print (sf.getVKnots())
            

            pps=[]
            umi=max(ui-1,0)
            uma=min(sf.NbUPoles-1,ui+1)
            vmi=max(vi-1,0)
            vma=min(sf.NbVPoles-1,vi+1)

            pps += [(uk,vk) for uk in range(umi,uma+1) for vk in range(vmi,vma+1)]

            try:
                (t1,t2)=sf.tangent(ui/3,vi/3)
                t1=t1.normalize()
                t2=t2.normalize()
                n=sf.normal(ui/3,vi/3)
                n=n.normalize()
                vectn=t1*params.root.ids['udial'].value()*params.root.ids['scale'].value()+\
                                t2*params.root.ids['vdial'].value()*params.root.ids['scale'].value()+\
                                n*params.root.ids['ndial'].value()*params.root.ids['scale'].value()
                print ("NORMAL/TAN", vectn)
            except:
                vectn=App.Vector()

            turot=params.root.ids['tvrot'].value()
            tvrot=params.root.ids['turot'].value()
            tuscale=params.root.ids['tuscale'].value()/30.
            tvscale=params.root.ids['tvscale'].value()/30.


#            t1=App.Vector(poles[ui,vi]-poles[ui+1,vi]).normalize()
#            t2=App.Vector(poles[ui,vi]-poles[ui,vi+1]).normalize()
#            n=t1.cross(t2)

            try:
#                (t1,t2)=sf.tangent(ui/3,vi/3)
#                t1=t1.normalize()
#                t2=t2.normalize()
                n=sf.normal(ui/3,vi/3)
                n=n.normalize()

                urot=App.Rotation(n,turot)
                vrot=App.Rotation(n,-tvrot)

            except:
                print ("KEINE NORMALE")
                n=None

            print ("center of mass", params.root.ids['centerofmass'].isChecked())

            if params.root.ids['centerofmass'].isChecked():

                base=com
                for (u,v) in pps:
                    vv=App.Vector(poles[u,v]-base)
                    vv=rot.multVec(vv)
                    print ("scalfactor val", params.root.ids['scale'].value())
                    print ("scalfactor", params.root.ids['scale'].value()*0.1)
                    vv *= params.root.ids['scale'].value()*0.1
                    poles[u,v] =base+vv+mov

            elif params.root.ids['referencepoint'].isChecked():

                base=App.ActiveDocument.getObject('tmp_referencePoint').Placement.Base
                for (u,v) in pps:
                    vv=App.Vector(poles[u,v]-base)
                    vv=rot.multVec(vv)
                    vv *= params.root.ids['scale'].value()*0.1
                    poles[u,v] =base+vv+mov
                


            else:
                for (u,v) in pps:
    #                rot=App.Rotation(arc,0,0)
                    vv=App.Vector(poles[u,v]-base)
                    # vv=rot.multVec(vv)
                    if n !=None:
                        if u==ui and (v==vi-1 or v==vi+1):
                            vv=urot.multVec(vv)
                            vv *= tuscale
                        if v==vi and (u==ui-1 or u==ui+1):
                            vv=vrot.multVec(vv)
                            vv *= tvscale

                    poles[u,v] =base+vv+mov+vectn

            compe += editcross(poles,ui,vi)
            #------------------

#            poles[ui,vi] += mov


            bs=Part.BSplineSurface()
            bs.buildFromPolesMultsKnots(poles,
                    sf.getUMultiplicities(),sf.getVMultiplicities(),
                    sf.getUKnots(),sf.getVKnots(),
                    False,False,sf.UDegree,sf.VDegree,sf.getWeights())
            comp[si]=bs.toShape()

        obj=App.ActiveDocument.getObject(self.nameF)
        obj.Shape=Part.Compound(comp)
        if force:
            print ("force")
            self.comp=comp
        else:
            print ("no force")

        # alle poles ausrechnen
        pts=[]
        for c in comp:
            sf=c.Surface
            poles=np.array(c.Surface.getPoles())
            ptsa=[App.Vector(poles[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]
            ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
            pts += [App.Vector(p) for p in ptsa]


        obj2=App.ActiveDocument.getObject(self.nameP)
        pm=obj2.Placement
        comp2=[Part.Vertex(App.Vector(p)) for p in pts]
        obj2.Shape=Part.Compound(comp2)
        obj2.Placement=pm

        obj3=App.ActiveDocument.getObject(self.nameE)
        obj3.Shape=Part.Compound(compe)




import FreeCADGui as Gui 

import NURBSinit





#----------------------------
# Gui
#---------------------------







def flattenRegion(selections):


    def flattenregion(bs,ua,ub,va,vb):


        poles=np.array(bs.getPoles())
        poles2=np.zeros(4*4*3).reshape(4,4,3)

        v=va
        u=ua

        poles2[0:2,0:2]=poles[u:u+2,v:v+2]
        u=ub

        poles2[2:4,0:2]=poles[u-1:u+1,v:v+2]


        v=vb
        u=ua
        poles2[0:2,2:4]=poles[u:u+2,v-1:v+1]
        u=ub
        poles2[2:4,2:4]=poles[u-1:u+1,v-1:v+1]


        bs2=Part.BSplineSurface()
        bs2.buildFromPolesMultsKnots(poles2, 
            [4,4],[4,4],
            [0,1],[0,1],
            False,False,3,3)

        Part.show(bs2.toShape())


        for u in range(ua,ub+1):
            for v in range(va,vb+1):
                (uu,vv)=bs2.parameter(App.Vector(poles[u,v]))
                pos=bs2.value(uu,vv)
                poles[u,v]=pos

        n=(ub-ua)/3
        for i in range(1,n):
            bs2.insertUKnot(1.0/n*i,3,0)

        n=(vb-va)/3
        for i in range(1,n):
            bs2.insertVKnot(1.0/n*i,3,0)

        Part.show(bs2.toShape())
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
        App.ActiveDocument.ActiveObject.ViewObject.Transparency=70
        App.ActiveDocument.BeGrid002.Source=App.ActiveDocument.ActiveObject

        poles2=np.array(bs2.getPoles())
        print (poles2.shape)
        
        #return bs2
        poles[ua:ub+1,va:vb+1]=poles2
        if 0:
            poles[ua-1,va+1:vb]=poles[ua,va+1:vb]*2-poles[ua+1,va+1:vb]
            poles[ub+1,va+1:vb]=poles[ub,va+1:vb]*2-poles[ub-1,va+1:vb]

            poles[ua+1:ub,va-1]=poles[ua+1:ub,va]*2-poles[ua+1:ub,va+1]
            poles[ua+1:ub,vb+1]=poles[ua+1:ub,vb]*2-poles[ua+1:ub,vb-1]


        poles[ua-1,va+2:vb-1]=poles[ua,va+2:vb-1]*2-poles[ua+1,va+2:vb-1]
        poles[ub+1,va+2:vb-1]=poles[ub,va+2:vb-1]*2-poles[ub-1,va+2:vb-1]

        poles[ua+2:ub-1,va-1]=poles[ua+2:ub-1,va]*2-poles[ua+2:ub-1,va+1]
        poles[ua+2:ub-1,vb+1]=poles[ua+2:ub-1,vb]*2-poles[ua+2:ub-1,vb-1]


        bs3=Part.BSplineSurface()
        bs3.buildFromPolesMultsKnots(poles, 
                        bs.getUMultiplicities(),
                        bs.getVMultiplicities(),
                        bs.getUKnots(),
                        bs.getVKnots(),
                        False,False,3,3,bs.getWeights())
        return bs3


    bs=App.ActiveDocument.BePlane.Shape.Face1.Surface
    print (selections)

    ua=selections[0][1]
    va=selections[0][2]
    ub=selections[1][1]
    vb=selections[1][2]
    
    try:
        App.ActiveDocument.ActiveObject.ViewObject.hide()
    except:
        pass

    bs=flattenregion(bs,ua,ub,va,vb)

    if 0: #repeat with multiple areas 
        ua,va=6,6
        ub,vb=12,15
        bs=flattenregion(bs,ua,ub,va,vb)

    Part.show(bs.toShape())
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
    App.ActiveDocument.BeGrid001.Source=App.ActiveDocument.ActiveObject





def SurfaceEditor():
    '''gui for the surface editor'''

    from .miki_g import createMikiGui2, MikiApp
    #reload( .miki_g)

    layout = '''
#MainWindow:
    MyTabWidget:
        tabname: "Editor"
        VerticalLayout:
            VerticalLayout:    
                QtGui.QLabel:
                    setText:"***   Multi Face Poles Editor   D E M O    V 0.9    ***"
        #            QtGui.QLineEdit:
        #                id: 'vx'
        #                setText:"1"
        #                textChanged.connect: app.relativeMode
                HorizontalGroup:
                    setTitle: "Position UV-tangential Normal"
                    QtGui.QDial:
                        id: 'udial'
                        setFocusPolicy: QtCore.Qt.StrongFocus
                        valueChanged.connect: app.relativeMode
                        setMinimum: -100
                        setMaximum: 100
                    QtGui.QDial:
                        id: 'vdial'
                        setMinimum: -100
                        setMaximum: 100
                        valueChanged.connect: app.relativeMode
                    QtGui.QDial:
                        id: 'ndial'
                        setMinimum: -100
                        setMaximum: 100
                        valueChanged.connect: app.relativeMode
                    QtGui.QPushButton:

                HorizontalGroup:
                    setTitle: "Position XYZ"
                    QtGui.QDial:
                        id: 'xdial'
                        setMinimum: -100
                        setMaximum: 100
                        #setValue: 90
                        setFocusPolicy: QtCore.Qt.StrongFocus
                        valueChanged.connect: app.update
                    QtGui.QDial:
                        id: 'ydial'
                        setMinimum: -100
                        setMaximum: 100
                        valueChanged.connect: app.update
                    QtGui.QDial:
                        id: 'zdial'
                        setMinimum: -100.
                        setMaximum: 100.
                        #setValue: 90.
                        valueChanged.connect: app.update
                    QtGui.QPushButton:


            HorizontalGroup:
                setTitle: "Transformation Center for Rotation/Scale"

                HorizontalLayout:
                    QtGui.QCheckBox:
                        id: 'centerofmass'
                        setText: 'center of mass'
                        stateChanged.connect: app.centerofmass
#                        valueChanged.connect: app.centerofmass
                        #setChecked: True

                HorizontalLayout:
                    QtGui.QCheckBox:
                        id: 'referencepoint'
                        setText: 'reference point'
                        stateChanged.connect: app.referencepoint
                        #setChecked: True





            setSpacer:


            HorizontalGroup:
                setTitle: "Command Line"
                QtGui.QLineEdit:
                    id: 'ux'
                    #setText:""
                    setPlaceholderText: "write command please"
                    textChanged.connect: app.textprocessor
#                returnPressed.connect: app.textprocessor2
                    editingFinished.connect: app.textprocessor3

                QtGui.QComboBox:
                    id: 'mode'
                    addItem: "FreeCAD"
                    addItem: "Blender"

            HorizontalGroup:
                setTitle: "grp 1"

                QtGui.QPushButton:
                    setText: "apply"
                    clicked.connect: app.apply

                QtGui.QPushButton:
                    setText: "apply and close"
                    clicked.connect: app.applyandclose

                QtGui.QPushButton:
                    setText: "cancel and close"
                    clicked.connect: app.myclose

                QtGui.QPushButton:
                    setText: "reset dialog"
                    clicked.connect: app.resetDialog


            HorizontalGroup:
                setTitle: "grp 2"

#                QtGui.QPushButton:
#                    setText: "init data"
#                    clicked.connect: app.initData

                QtGui.QPushButton:
                    setText: "clear selection"
                    clicked.connect: app.clearSelection

                QtGui.QPushButton:
                    setText: "add selection"
                    clicked.connect: app.addSelection

                QtGui.QPushButton:
                    setText: "set selection"
                    clicked.connect: app.setSelection




        tabname: "Extension"
        VerticalLayout:
            HorizontalGroup:
                setTitle: "Rotation Euler: Nick Roll Gier"
                QtGui.QDial:
                    id: 'xrot'
                    setMinimum: -100
                    setMaximum: 100
                    setFocusPolicy: QtCore.Qt.StrongFocus
                    valueChanged.connect: app.relativeMode
                QtGui.QDial:
                    id: 'yrot'
                    setMinimum: -100
                    setMaximum: 100
                    valueChanged.connect: app.relativeMode
                QtGui.QDial:
                    id: 'zrot'
                    setMinimum: -100.
                    setMaximum: 100.
                    valueChanged.connect: app.relativeMode




            HorizontalGroup:
                setTitle: "scale"
                QtGui.QSlider:
                    id: 'scale'
                    setMinimum: 1
                    setValue: 10.0
                    setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
                    valueChanged.connect: app.update


            HorizontalGroup:
                setTitle: "Rotation Tangents UV"
                QtGui.QDial:
                    id: 'turot'
                    setMinimum: -100
                    setMaximum: 100
                    setFocusPolicy: QtCore.Qt.StrongFocus
                    valueChanged.connect: app.relativeMode
                QtGui.QDial:
                    id: 'tvrot'
                    setMinimum: -100
                    setMaximum: 100
                    valueChanged.connect: app.relativeMode


            HorizontalGroup:
                setTitle: "scale Tangents UV"
                QtGui.QSlider:
                    id: 'tvscale'
                    setValue: 30.0
                    setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
                    valueChanged.connect: app.update
                QtGui.QSlider:
                    id: 'tuscale'
                    setValue: 30.0
                    setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
                    valueChanged.connect: app.update





            setSpacer:

        tabname: "Special Methods"
        VerticalLayout:

            HorizontalGroup:
                setTitle: ""

                QtGui.QPushButton:
                    setText: "update"
                    clicked.connect: app.update

                QtGui.QPushButton:
                    setText: "merge"
                    clicked.connect: app.merge

                QtGui.QPushButton:
                    setText: "flatten region"
                    clicked.connect: app.flattenregion

            QtGui.QPushButton:
                setText: "connect to selected point"
    #            clicked.connect: app.connectSelection


#            QtGui.QPushButton:
#                setText: 'Toggle Begrid'
#                clicked.connect: app.showbegrid
#                setChecked: True

#            QtGui.QPushButton:
#                setText: 'Toggle Map'
#                clicked.connect: app.showmap
#                setChecked: True


            setSpacer:


        tabname: "Configuration"
        VerticalLayout:

            HorizontalLayout:
                QtGui.QCheckBox:
                    id: 'showface'
                    setText: 'Show Face'
                    stateChanged.connect: app.relativeMode
                    setChecked: True

                QtGui.QCheckBox:
                    id: 'showtangents'
                    setText: 'Show Tangents'
                    stateChanged.connect: app.relativeMode
                    setChecked: True

                QtGui.QCheckBox:
                    id: 'showcurves'
                    setText: 'Show Curves'
                    stateChanged.connect: app.relativeMode
                    setChecked: True


    #            QtGui.QCheckBox:
    #                setText: 'Show Tangents'
    #                stateChanged.connect: app.relativeMode
    #                setChecked: True




    #        HorizontalGroup:
    #            setTitle: "Mode"
    #            QtGui.QComboBox:
    #                id: 'mode'
    #                addItem: "u"
    #                addItem: "v"
    #        QtGui.QPushButton:
    #            setText: "Run Action"
    #            clicked.connect: app.run

            setSpacer:


        tabname: "Develop"
        VerticalLayout:

            HorizontalLayout:
                QtGui.QCheckBox:
                    id: 'showface'
                    setText: 'Show Face'
                    stateChanged.connect: app.relativeMode
                    setChecked: True

            QtGui.QPushButton:
                setText: 'Set Selection 1,1 and 1,2'
                clicked.connect: app.setselection1
                setChecked: True



            setSpacer:

        setCurrentIndex: 0

        '''



    def edit(u,v,s=10):

        print ("u,v,scale",u,v,s)
        #fp=App.ActiveDocument.Seam_ProductFace001
        
        App.ActiveDocument.recompute()



    class EditorApp(MikiApp):

        def resetDialog(self):
            '''set all parameters of the dialog to default values'''

            for idx in  'udial','vdial','ndial','scale','xdial','ydial','zdial','xrot','yrot','zrot':
                if self.root.ids[idx].value()!=0:
                    self.root.ids[idx].setValue(0)

            self.root.ids['scale'].setValue(10)
            App.ActiveDocument.recompute()

        def setselection1(self):
            u=1
            v=2
            self.multiface.selection=[
                [0,3,3,App.Vector()],
                [0,3*u,3*v,App.Vector()],
                ]
            print ("set selection",u,v)


        def centerofmass(self):
            print ("display and use center of mass")
            ps=App.Vector()
            for s in self.multiface.selection:
                print (s)
                [ci,ui,vi]=s[0:3]
                pp=self.multiface.comp[ci].Surface.getPoles()
                p=pp[ui][vi]
                ps +=p 
            ps *= 1.0/len(self.multiface.selection)
            obj=App.ActiveDocument.getObject('tmp_CenterOfMass_Selection')
            if obj == None:
                obj=App.ActiveDocument.addObject("Part::Cone",'tmp_CenterOfMass_Selection')
                obj.ViewObject.ShapeColor=(1.,1.,0.)
                obj.Height=500
                obj.Radius2=50
            obj.Placement.Base=ps

        def referencepoint(self):
            obj=App.ActiveDocument.getObject('tmp_referencePoint')
            if obj == None:
                obj=App.ActiveDocument.addObject("Part::Cone",'tmp_referencePoint')
                obj.ViewObject.ShapeColor=(0.7,1.,0.7)
                obj.Height=500
                obj.Radius2=50








        def textprocessor(self):
            print ("TEXTPROZESSOR")
            print ("ux:",self.root.ids['ux'].text())

#        def textprocessor2(self):
#            print ("TEXTPROZESSOR 2"
#            print ("ux:",self.root.ids['ux'].text()

        def textprocessor3(self):
            '''command line execution after pressing enter in the command line '''
            print ("TEXTPROZESSOR 3")
            print ("ux:",self.root.ids['ux'].text())
            # anylize the text
            w=self.root.ids['ux'].text()
            # print w.split()
            cmds=w.split(';')
            cmdtab={ 'FreeCAD':    {
                            'x': 'xdial',
                            'y': 'ydial',
                            'z': 'zdial',
                            'u': 'udial',
                            'v': 'vdial',
                            'n': 'ndial',
                            's': 'scale',
                            'rn': 'xrot',
                            'rr': 'yrot',
                            'rg': 'zrot',

                        },
                    'Blender': {
                            'gx': 'xdial',
                            'gy': 'ydial',
                            'gz': 'zdial',
                            'u': 'udial',
                            'v': 'vdial',
                            'n': 'ndial',
                            's': 'scale',
                            'rx': 'xrot',
                            'ry': 'yrot',
                            'rz': 'zrot',
                        }
                    }

            mode=self.root.ids['mode'].currentText()
            print ("mode ",mode)
            for c in cmds:
                print (c.split())
                sp=c.split()
                if len(sp)==3:
                    [cmd,val1,val2]=sp
                    if cmd=='seladd':
                        print ("select add ring")
                        val1=int(val1)
                        val2=int(val2)
                        self.multiface.selection += [[0,3*val1,3*val2,None]]
                        print (self.multiface.selection)
                        self.update()

                if len(sp)==2:
                    [cmd,val]=sp
                    val=float(val)
                    print (val)
                    try:
                        if cmd=='s':val *= 10.
                        print ("scale command ------------",cmd,val)
                        self.root.ids[cmdtab[mode][cmd]].setValue(val)
                        self.update()

                    except:
                        print ("kann kommndo nicht ausfuehren")
                    
                    if cmd=='selu':
                        print ("select u ring")
                        self.multiface.selection=[]
                        val=int(val)
                        pp=self.multiface.comp[0].Surface.NbVPoles/3
                        
                        for v in range(pp+1):
                            self.multiface.selection += [[0,3*val,3*v,None]]
                        print (self.multiface.selection)
                        self.update()
                    if cmd=='selv':
                        print ("select v ring")
                        self.multiface.selection=[]
                        val=int(val)
                        pp=self.multiface.comp[0].Surface.NbUPoles/3
                        for u in range(pp+1):
                            self.multiface.selection += [[0,3*u,3*val,None]]
                        self.update()

                if len(sp)==0:
                    print ("Hide mode ..........")
                    print (self.last)
                    if self.last !='hide':
                        App.ActiveDocument.BeGrid.ViewObject.Visibility= not App.ActiveDocument.BeGrid.ViewObject.Visibility
                        self.last='hide'
                    else:
                        self.last=''
                    return

                if len(sp)==1:
                    cmd=sp[0]
                    if cmd=='a':
                        self.apply()
                    elif cmd=='1':
                        Gui.activeDocument().activeView().viewFront()
                    elif cmd=='2':
                        Gui.activeDocument().activeView().viewTop()
                    elif cmd=='3':
                        Gui.activeDocument().activeView().viewRight()
                    elif cmd=='4':
                        Gui.activeDocument().activeView().viewRear()
                    elif cmd=='5':
                        Gui.activeDocument().activeView().viewBottom()
                    elif cmd=='6':
                        Gui.activeDocument().activeView().viewLeft()
                    elif cmd=='0':
                        Gui.activeDocument().activeView().viewAxonometric()
                    elif cmd==',':
                        import workspace
                        import workspace.views
                        try: self.light
                        except: self.light=False
                        if self.light:
                            workspace.views.lightOff()
                        else:    
                            workspace.views.lightOn()
                        self.light = not self.light
                    elif cmd=='+':
                        Gui.ActiveDocument.ActiveView.zoomIn()
                    elif cmd=='-':
                        Gui.ActiveDocument.ActiveView.zoomOut()
                    elif cmd=='q':
                        self.close()

            self.last=''
            self.root.ids['ux'].setText('')


        def showbegrid(self):
            print ("showgrid")
            App.ActiveDocument.BeGrid.ViewObject.Visibility= not App.ActiveDocument.BeGrid.ViewObject.Visibility


        def showmap(self):
            print ("showmap")
            App.ActiveDocument.MAP.ViewObject.Visibility= not App.ActiveDocument.MAP.ViewObject.Visibility


        def flattenregion(self):
            for s in self.multiface.selection:
                print (s)

            flattenRegion(self.multiface.selection)

        def save(self):
            tt=time.time()
            try: obj=self.resultobj
            except:
                obj=App.ActiveDocument.addObject('Part::Spline','result')
                try:
                    App.ActiveDocument.removeObject(self.NameObj2)
                except:
                    pass
                try:
                    App.ActiveDocument.removeObject(self.NameObj)
                except:
                    pass
#            print ("savet ",time.time()-tt

            tt=time.time()
            obj.ViewObject.hide()
#            obj.Shape=self.Shape
#            print ("savetime hidden ",time.time()-tt
#            tt=time.time()
#            obj.ViewObject.show()

#            obj.Shape=self.Shape
            objA=App.ActiveDocument.getObject('tmp_multiFace')
            obj.Shape=objA.Shape
#            print ("savetime show ",time.time()-tt

#            tt=time.time()
#            z=self.Shape
#            z=self.Shape
#            print ("savetime intern ",time.time()-tt

            self.obj=obj
            self.resultobj=obj
#            print ("savetb ",time.time()-tt

        def applyandclose(self):
            self.save()
            try:
                App.ActiveDocument.removeObject(self.NameObj2)
                App.ActiveDocument.removeObject(self.NameObj)
            except:
                pass
            self.close()


        def myclose(self):
            try:
                App.ActiveDocument.removeObject(self.NameObj2)
                App.ActiveDocument.removeObject(self.NameObj)
            except:
                pass
            self.close()

        def run(self):
            print ("run")
            edit(
                self.root.ids['udial'].value(),
                self.root.ids['vdial'].value(),
                self.root.ids['scale'].value(),
            )




        def relativeMode(self):
            print ("relative mode called")
            self.update()

        def xyz_apply(self,save=True):
#            print ("apply  implemented"
            st=time.time()

            vec=App.Vector(
                        self.root.ids['xdial'].value()*self.root.ids['scale'].value(),
                        self.root.ids['ydial'].value()*self.root.ids['scale'].value(),
                        self.root.ids['zdial'].value()*self.root.ids['scale'].value()
                        )
            App.ActiveDocument.recompute()
            print ("Time C ",time.time()-st)

        def initData(self):
            print ("init data a")
            m=Multiface()
            m.getPoints()
            self.multiface=m
            self.multiface.movePoint(None,App.Vector(0,0,1000),True)
            # print ("comp anz", len(self.multiface.comp))
            self.multiface.selection = [
                (0,3,3,App.Vector()),
                (0,1,1,App.Vector()),
                (0,2,1,App.Vector()),
            ]


        def clearSelection(self):
            self.multiface.selection=[]


        def setSelection(self):
            print 
            selps=Gui.Selection.getSelectionEx()[0].PickedPoints
            self.multiface.compe=[]
            self.multiface.selection=[]
            for vt in selps:
                print (vt) 
                vt -= App.ActiveDocument.tmp_poles.Placement.Base
                self.multiface.movePoint(vt,App.Vector(0,0,2000),True,params=self)
            print ("SELECTIONS")
            for s in self.multiface.selection:
                print (s)
            App.ActiveDocument.recompute()
            App.ActiveDocument.getObject(self.multiface.nameE).ViewObject.show()

            self.root.ids['ux'].setFocus()
            self.last='hide2'

        def update(self):
            ta=time.time()
            if hasattr(self,'multiface'):
                self.multiface.update(params=self,force=False)
                App.ActiveDocument.recompute()
                print  (len(self.multiface.selection))
                print ("update ",time.time()-ta)

        def apply(self):
            ta=time.time()
            self.multiface.update(params=self,force=True)
            App.ActiveDocument.recompute()
            print  (len(self.multiface.selection))
            print ("update ",time.time()-ta)
            App.ActiveDocument.getObject(self.multiface.nameE).ViewObject.hide()
            App.ActiveDocument.recompute()



        def xyz_update(self):
            ta=time.time()
            
            print  (len(self.multiface.selection))
            selps=[App.Vector(p[3]) for p in self.multiface.selection]
            sels=self.multiface.selection
            self.multiface.selection=[]
            self.multiface.compe=[]
            for vt in selps:
                print ("X")
                self.multiface.movePoint(vt,App.Vector(0,0,2000),True,params=self,useselections=True)
            App.ActiveDocument.recompute()
            print  (len(self.multiface.selection))
            print ("update ",time.time()-ta)


        def addSelection(self):
            print 
            selps=Gui.Selection.getSelectionEx()[0].PickedPoints
            #self.multiface.compe=[]
            pres=self.multiface.selection
            for vt in selps:
                print (vt) 
                vt -= App.ActiveDocument.tmp_poles.Placement.Base
                self.multiface.movePoint(vt,App.Vector(0,0,2000),True)
            # self.multiface.selection += pres
            print ("SELECTIONS")
            for s in self.multiface.selection:
                print( s)
            
            self.update()
            App.ActiveDocument.recompute()
            App.ActiveDocument.getObject(self.multiface.nameE).ViewObject.show()

            self.root.ids['ux'].setFocus()
            self.last='hide2'


        def xyz_apply(self):
            print ("SELECTIONS pre")    
            for s in self.multiface.selection:
                print (s)
            selps=[App.Vector(p[3]) for p in self.multiface.selection]
#            for (s,u,v,p) in self.multiface.selection:
#                pp=self.multiface.comp[s].Surface.getPoles()
#                print pp[u][v]
#                print p
            
            self.multiface.selection=[]
            for vt in selps:
        #        vt -= App.ActiveDocument.tmp_poles.Placement.Base
                self.multiface.movePoint(vt,App.Vector(0,0,1500),False,params=self)

            print ("SELECTIONS post")    
            for s in self.multiface.selection:
                print (s)

            App.ActiveDocument.getObject(self.multiface.nameE).ViewObject.hide()
            App.ActiveDocument.recompute()


        def merge(self):
            print ("SELECTIONS")

            for s in self.multiface.selection:
                print (s)

            comp=[c for c in self.multiface.comp]
            compe=self.multiface.compe
            pts=[]

            for i in range(len(self.multiface.selection)/2):
                sa=self.multiface.selection[2*i]
                sb=self.multiface.selection[2*i+1]


                sia,uia,via,p=sa
                polesa=np.array(comp[sia].Surface.getPoles())
                print (polesa[uia,via])
                ma=polesa[uia,via]

                sib,uib,vib,p=sb
                polesb=np.array(comp[sib].Surface.getPoles())
                print (polesb[uib,vib])
                mb=polesb[uib,vib]

                #merge point
                mm=(ma+mb)*0.5

                sf=comp[sia].Surface
                pps=[]
                umia=max(uia-1,0)
                umaa=min(sf.NbUPoles-1,uia+1)
                vmia=max(via-1,0)
                vmaa=min(sf.NbVPoles-1,via+1)

                mova= mm-ma

                sf=comp[sib].Surface
                pps=[]
                umib=max(uib-1,0)
                umab=min(sf.NbUPoles-1,uib+1)
                vmib=max(vib-1,0)
                vmab=min(sf.NbVPoles-1,vib+1)

                movb= mm-mb
                print ("move b",movb)

                print ("Bereich a",umia,umaa,vmia,vmaa)
                pps=[]
                pps += [(uk,vk) for uk in range(umia,umaa+1) for vk in range(vmia,vmaa+1)]
                for (u,v) in pps:
#                            rot=App.Rotation(arc,0,0)
#                            vv=App.Vector(poles[u,v]-base)
#                            vv=rot.multVec(vv)
                    polesa[u,v] +=  mova 
                    print (u,v)
                print ("result a",polesa[uia,via])

                sf=comp[sib].Surface
                bs=Part.BSplineSurface()
                bs.buildFromPolesMultsKnots(polesa,
                                sf.getUMultiplicities(),sf.getVMultiplicities(),
                                sf.getUKnots(),sf.getVKnots(),
                                False,False,sf.UDegree,sf.VDegree,sf.getWeights())

                comp[sia] = bs.toShape()

                if sib != sia:
                    ptsa=[App.Vector(polesa[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]

                    ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                    pts += [App.Vector(p) for p in ptsa]

                print ("Xresult a",polesa[uia,via])
                if sib==sia:
                    polesb=polesa
                else:
                    polesb=np.array(comp[sib].Surface.getPoles())
                print ("result ab",polesb[uia,via])

                print ("Bereich b" ,umib,umab,vmib,vmab)
                pps=[]
                pps += [(uk,vk) for uk in range(umib,umab+1) for vk in range(vmib,vmab+1)]
                print ("ha----------")
                for (u,v) in pps:
#                            rot=App.Rotation(arc,0,0)
#                            vv=App.Vector(poles[u,v]-base)
#                            vv=rot.multVec(vv)
                    polesb[u,v] +=  movb 
                    print (u,v)
                    print ("result abb",polesb[uia,via])
                print ("hu-------------------")

                print ("result _b",polesb[uib,vib])
                print (uib,vib)
                print ("result aa",polesa[uia,via])
                print ("result a(b)",polesb[uia,via])
                print (uia,via)
                print 
                
                if sib == sia:
                    print ("!aaaa!!",sia,sib,uia,uib,via,vib)
                    if uia == uib:
                        print ("!ccc!!",sia,sib,uia,uib,via,vib)
                        mm=polesb[uia,via]
                        if via>vib: via,vib=vib,via
                        for v in range(via,vib+1):
                                print ("XX")
                                polesb[uia,v]=mm 
                                polesb[uia-1,v]=polesb[uia-1,via]
                                polesb[uia+1,v]=polesb[uia+1,via]
                    if via == vib:
                        print ("!ddd!!",sia,sib,uia,uib,via,vib)
                        mm=polesb[uia,via]
                        if uia>uib: uia,uib=uib,uia
                        for u in range(uia,uib+1):
                                print ("YYY")
                                polesb[u,via]=mm 
                                polesb[u,via-1]=polesb[uia,via-1]
                                polesb[u,via+1]=polesb[uia,via+1]
                else:
                    print ("!!!",sia,sib,uia,uib,via,vib)

    
                bs=Part.BSplineSurface()
                bs.buildFromPolesMultsKnots(polesb,
                                sf.getUMultiplicities(),sf.getVMultiplicities(),
                                sf.getUKnots(),sf.getVKnots(),
                                False,False,sf.UDegree,sf.VDegree,sf.getWeights())



                comp[sib] = bs.toShape()

                compe += editcross(polesa,uia,via)
                compe += editcross(polesb,uib,vib)

                ptsa=[App.Vector(polesb[3*uii,3*vii]) for uii in range(sf.NbUPoles/3+1) for vii in  range(sf.NbVPoles/3+1) ]

                ptsa = np.array(ptsa).reshape((sf.NbUPoles/3+1)*(sf.NbVPoles/3+1),3)
                pts += [App.Vector(p) for p in ptsa]





            obj=App.ActiveDocument.getObject(self.multiface.nameF)
            obj.Shape=Part.Compound(comp)

            obj3=App.ActiveDocument.getObject(self.multiface.nameE)
            obj3.Shape=Part.Compound(compe)

            self.multiface.comp=comp
            self.multiface.compe=compe


            obj2=App.ActiveDocument.getObject(self.multiface.nameP)
            pm=obj2.Placement
            print ("Poles placement -------")
            print (pm)
            
            comp2=[Part.Vertex(App.Vector(p)) for p in pts]
            obj2.Shape=Part.Compound(comp2)
            obj2.Placement=pm





    mikigui = createMikiGui2(layout, EditorApp)
    mikigui.initData()
    mikigui.last=''
    mikigui.light=False


class Nurbs_MultiEdit:
    def Activated(self):
        self.mmultiEdit()
    def multiEdit(self):
       SurfaceEditor()
        
    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_MultiEdit")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_MultiEdit"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_MultiEdit", Nurbs_MultiEdit())



class Nurbs_MultiEditAA:
    def Activated(self):
        self.AA()
    def AA(self):

        import berings
        #reload(berings)
        berings.createBeGrid()
        facedraw
        #reload(.facedraw)
        facedraw.createMap()
        
        if App.ActiveDocument.BeGrid.Source == None:
            App.ActiveDocument.BeGrid.Source=App.ActiveDocument.tmp_multiFace
            App.ActiveDocument.recompute()

        if App.ActiveDocument.MAP.faceObject == None:
            App.ActiveDocument.MAP.faceObject=App.ActiveDocument.tmp_multiFace
            App.ActiveDocument.recompute()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_MultiEditAA")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_MultiEditAA"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_MultiEditAA", Nurbs_MultiEditAA())

