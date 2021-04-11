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

import random,time
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import scipy.linalg.lapack as sp
from numpy.linalg import inv

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import 

from .pyob import  FeaturePython,ViewProvider
from .say import *
reload (.pyob)

from FreeCAD import Vector
import Draft

from .tools import power,crossProduct,dotProduct,sign,sqrt,groupit
reload(.tools)


def drawConeA(name,i,bounds,apex,axis,alpha,trafo,pts):
    '''draw a Cone with helper points '''

    trafo=trafo.inverse()
    v=App.Vector(0,0,1)

    pss=[]

    [h1,h2]=bounds
    h2+=10
    h1-=10

    if alpha>np.pi/2: alpha= np.pi-alpha



    if h2>10:
        cc=Part.makeCone(0,abs(np.tan(alpha))*h2,h2)
        cc.Placement.Rotation=App.Rotation(v,axis)
        cc.Placement.Base=apex
        pss += [cc]

    if h1<-10:
        c2c=Part.makeCone(0,abs(np.tan(alpha))*-h1,-h1)
        c2c.Placement.Rotation=App.Rotation(-v,axis)
        c2c.Placement.Base=apex
        pss += [c2c]

    if 0:
        s=Part.makeSphere(3)
        s.Placement.Base=apex
        pss += [s]

    for p in pts:
        ps=Part.makeSphere(3)
        ps.Placement.Base=p
        ps.Placement=trafo.multiply(ps.Placement)
    #    pss += [ps]

    nn="__"+name+"_"+str(i)
    yy=App.ActiveDocument.getObject(nn)
    if yy==None:
        yy=App.ActiveDocument.addObject("Part::Feature",nn)
        yy.ViewObject.Transparency=10
        yy.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

    # nure fleache als nurbs
    ccokay=True
    
    if h2>10:
        nurbs=cc.toNurbs()
#        print ("---------NURBS -------", nurbs
        sf=nurbs.Face1.Surface.copy()
        us=[]
        vs=[]
        for p in pts:
            (u,v)=sf.parameter(p)
            if (sf.value(u,v)-p).Length>0.1:
                ccokay=False
            us += [u]
            vs += [v]
#        print us
#        print vs
        umi=min(us)
        uma=max(us)
        vmi=min(vs)
        vma=max(vs)
    else:
        ccokay=False

    if not ccokay:
        nurbs=c2c.toNurbs()
#        print ("---------NURBS -------", nurbs
        sf=nurbs.Face1.Surface.copy()
        us=[]
        vs=[]
        for p in pts:
            (u,v)=sf.parameter(p)
            if (sf.value(u,v)-p).Length>0.1:
                ccokay=False
            us += [u]
            vs += [v]
#        print us
#        print vs
        umi=min(us)
        uma=max(us)
        vmi=min(vs)
        vma=max(vs)

    if 0:
        try:
            sf.segment(umi,uma,vmi,vma)
            yy.Shape= sf.toShape()
        except:
            yy.Shape=Part.Compound(pss)
        if not ccokay:
            yy.Shape=Part.Compound(pss)
    else:
        yy.Shape=Part.Compound(pss)

    yy.Placement=trafo
    yy.purgeTouched()


def drawConeB(apex,axis,alpha,h,trafo,pts):

    trafo=trafo.inverse()
    axis=axis.normalize()
    lens=[(p-apex).dot(axis) for p in pts] #+ [-1,1]

    if 0: # display apex as ball
        s=Part.makeSphere(2)
        s.Placement.Base=apex
        pss=[s]
    else:
        pss=[]

    for p in pts:
        r=(p-apex).cross(axis).Length
        c=Part.makeCircle(r)
        c.Placement.Base=apex+axis*((p-apex).dot(axis))
        c.Placement.Rotation=App.Rotation(App.Vector(0,0,1),axis)
        pss += [c]

    mima=[min(lens),max(lens)]
#    print ("minma",mima
    mi = min(mima[0],10)
    ma = max(mima[1],10)

    pss += [Part.makePolygon([apex,apex+axis*ma*1.1,apex-axis*mi*1.1])]

    for p in pts:
        pss += [Part.makePolygon([apex,p])]

    for p in pts:
        s=Part.makeSphere(2)
        s.Placement.Base=p
        pss += [s]

    rc=Part.Compound(pss)
    rc.Placement=trafo

    return rc, mima


def run_conepnppp(name,trafo,displaynumber,displayFaces,p_1,p_2,p_3,p_4):

    N=6
    A_eigen =np.array([  
        0,  0,  0,  0,  -p_4[2]*power(p_2[2],3)*power(p_3[1],2)-power(p_2[2],2)*power(p_3[2],2)*power(p_4[1],2)+p_3[2]*power(p_2[2],3)*power(p_4[1],2)+power(p_2[2],2)*power(p_4[2],2)*power(p_3[1],2)-p_2[2]*power(p_4[2],2)*p_3[2]*power(p_2[1],2)+p_2[2]*power(p_3[2],2)*p_4[2]*power(p_2[1],2),
                                        -2*power(p_2[2],2)*power(p_4[2],2)*p_3[2]*p_2[0]+2*power(p_2[2],2)*power(p_4[2],2)*p_3[0]*p_3[2]-2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[2]+2*power(p_2[2],2)*power(p_3[2],2)*p_4[2]*p_2[0]-2*power(p_2[2],2)*power(p_3[2],2)*p_4[0]*p_4[2]+2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[2],
                    0,  0,  0,  0,  2*p_2[2]*p_4[0]*p_4[2]*p_3[2]*power(p_2[1],2)-2*p_2[2]*p_3[0]*p_3[2]*p_4[2]*power(p_2[1],2)+2*power(p_2[2],2)*power(p_3[2],2)*p_4[2]*p_2[0]+2*p_4[2]*p_2[0]*power(p_2[2],2)*power(p_3[1],2)-2*power(p_2[2],2)*power(p_3[2],2)*p_4[0]*p_4[2]-2*power(p_2[2],2)*p_4[0]*p_4[2]*power(p_3[1],2)+2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[2]-2*power(p_2[2],2)*power(p_4[2],2)*p_3[2]*p_2[0]-2*p_3[2]*p_2[0]*power(p_2[2],2)*power(p_4[1],2)+2*power(p_2[2],2)*power(p_4[2],2)*p_3[0]*p_3[2]+2*power(p_2[2],2)*p_3[0]*p_3[2]*power(p_4[1],2)-2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[2],
                                        -p_4[2]*power(p_2[2],3)*power(p_3[1],2)-power(p_2[2],2)*power(p_3[2],2)*power(p_4[1],2)+p_3[2]*power(p_2[2],3)*power(p_4[1],2)+power(p_2[2],2)*power(p_4[2],2)*power(p_3[1],2)-p_2[2]*power(p_4[2],2)*p_3[2]*power(p_2[1],2)+p_2[2]*power(p_3[2],2)*p_4[2]*power(p_2[1],2),
                    1,  0,  0,  0,  2*p_2[2]*p_4[1]*p_4[2]*p_3[2]*power(p_2[1],2)-2*p_2[2]*p_3[1]*p_3[2]*p_4[2]*power(p_2[1],2)-2*power(p_2[2],3)*p_3[1]*p_3[2]*p_4[2]+2*p_4[2]*p_2[1]*power(p_2[2],2)*power(p_3[2],2)+2*p_4[2]*p_2[1]*power(p_2[2],2)*power(p_3[1],2)-2*power(p_2[2],2)*p_4[1]*p_4[2]*power(p_3[2],2)-2*power(p_2[2],2)*p_4[1]*p_4[2]*power(p_3[1],2)+2*power(p_2[2],3)*p_4[1]*p_4[2]*p_3[2]-2*p_3[2]*p_2[1]*power(p_2[2],2)*power(p_4[2],2)-2*p_3[2]*p_2[1]*power(p_2[2],2)*power(p_4[1],2)+2*power(p_2[2],2)*p_3[1]*p_3[2]*power(p_4[2],2)+2*power(p_2[2],2)*p_3[1]*p_3[2]*power(p_4[1],2),
                                        4*p_4[2]*p_2[1]*power(p_2[2],2)*p_3[0]*p_3[2]+4*power(p_2[2],2)*p_4[1]*p_4[2]*p_3[2]*p_2[0]-4*power(p_2[2],2)*p_4[1]*p_4[2]*p_3[0]*p_3[2]-4*p_3[2]*p_2[1]*power(p_2[2],2)*p_4[0]*p_4[2]-4*power(p_2[2],2)*p_3[1]*p_3[2]*p_4[2]*p_2[0]+4*power(p_2[2],2)*p_3[1]*p_3[2]*p_4[0]*p_4[2]-2*p_2[2]*power(p_3[2],2)*p_4[2]*p_2[0]*p_2[1]+2*p_2[2]*power(p_4[2],2)*p_3[2]*p_2[0]*p_2[1]+2*power(p_3[2],2)*power(p_2[2],2)*p_4[0]*p_4[1]-2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[1]-2*power(p_4[2],2)*power(p_2[2],2)*p_3[0]*p_3[1]+2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[1],
                    0,  1,  0,  0,  -2*p_2[2]*power(p_3[2],2)*p_4[2]*p_2[0]*p_2[1]-2*p_4[2]*p_2[0]*p_2[1]*p_2[2]*power(p_3[1],2)-2*p_2[2]*p_4[0]*p_4[1]*p_3[2]*power(p_2[1],2)+2*p_2[2]*power(p_4[2],2)*p_3[2]*p_2[0]*p_2[1]+2*p_3[2]*p_2[0]*p_2[1]*p_2[2]*power(p_4[1],2)+2*p_2[2]*p_3[0]*p_3[1]*p_4[2]*power(p_2[1],2)+2*power(p_3[2],2)*power(p_2[2],2)*p_4[0]*p_4[1]+2*power(p_2[2],2)*p_4[0]*p_4[1]*power(p_3[1],2)-2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[1]-2*power(p_4[2],2)*power(p_2[2],2)*p_3[0]*p_3[1]-2*power(p_2[2],2)*p_3[0]*p_3[1]*power(p_4[1],2)+2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[1],
                                        2*p_2[2]*p_4[1]*p_4[2]*p_3[2]*power(p_2[1],2)-2*p_2[2]*p_3[1]*p_3[2]*p_4[2]*power(p_2[1],2)-2*power(p_2[2],3)*p_3[1]*p_3[2]*p_4[2]+2*p_4[2]*p_2[1]*power(p_2[2],2)*power(p_3[2],2)+2*p_4[2]*p_2[1]*power(p_2[2],2)*power(p_3[1],2)-2*power(p_2[2],2)*p_4[1]*p_4[2]*power(p_3[2],2)-2*power(p_2[2],2)*p_4[1]*p_4[2]*power(p_3[1],2)+2*power(p_2[2],3)*p_4[1]*p_4[2]*p_3[2]-2*p_3[2]*p_2[1]*power(p_2[2],2)*power(p_4[2],2)-2*p_3[2]*p_2[1]*power(p_2[2],2)*power(p_4[1],2)+2*power(p_2[2],2)*p_3[1]*p_3[2]*power(p_4[2],2)+2*power(p_2[2],2)*p_3[1]*p_3[2]*power(p_4[1],2),
                    0,  0,  1,  0,  -power(p_2[2],2)*power(p_4[0],2)*power(p_3[1],2)+power(p_2[2],3)*power(p_4[0],2)*p_3[2]+p_4[2]*power(p_2[2],3)*power(p_3[1],2)+power(p_2[2],2)*power(p_3[2],2)*power(p_4[1],2)+power(p_2[2],2)*power(p_3[0],2)*power(p_4[2],2)+power(p_2[2],2)*power(p_3[0],2)*power(p_4[1],2)-power(p_2[2],3)*power(p_3[0],2)*p_4[2]-p_3[2]*power(p_2[2],3)*power(p_4[1],2)-power(p_2[2],2)*power(p_4[2],2)*power(p_3[1],2)-power(p_2[2],2)*power(p_4[0],2)*power(p_3[2],2)+p_2[2]*power(p_4[2],2)*p_3[2]*power(p_2[1],2)+p_2[2]*power(p_4[0],2)*p_3[2]*power(p_2[1],2)+p_4[2]*power(p_2[0],2)*p_2[2]*power(p_3[2],2)+p_4[2]*power(p_2[0],2)*p_2[2]*power(p_3[1],2)-p_2[2]*power(p_3[2],2)*p_4[2]*power(p_2[1],2)-p_2[2]*power(p_3[0],2)*p_4[2]*power(p_2[1],2)-p_3[2]*power(p_2[0],2)*p_2[2]*power(p_4[2],2)-p_3[2]*power(p_2[0],2)*p_2[2]*power(p_4[1],2),
                                        2*p_4[2]*power(p_2[0],2)*p_2[2]*p_3[0]*p_3[2]-4*p_2[1]*p_4[2]*power(p_2[2],2)*p_3[0]*p_3[1]+4*power(p_2[2],2)*p_4[1]*p_4[2]*p_3[0]*p_3[1]-2*p_3[2]*power(p_2[0],2)*p_2[2]*p_4[0]*p_4[2]+4*p_2[1]*p_3[2]*power(p_2[2],2)*p_4[0]*p_4[1]-4*power(p_2[2],2)*p_3[1]*p_3[2]*p_4[0]*p_4[1]+2*power(p_2[2],2)*power(p_4[2],2)*p_3[2]*p_2[0]-2*power(p_2[2],2)*power(p_4[2],2)*p_3[0]*p_3[2]+2*power(p_2[2],2)*power(p_4[0],2)*p_3[2]*p_2[0]-2*power(p_2[2],2)*power(p_4[0],2)*p_3[0]*p_3[2]+2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[2]-2*power(p_2[2],2)*power(p_3[2],2)*p_4[2]*p_2[0]+2*power(p_2[2],2)*power(p_3[2],2)*p_4[0]*p_4[2]-2*power(p_2[2],2)*power(p_3[0],2)*p_4[2]*p_2[0]+2*power(p_2[2],2)*power(p_3[0],2)*p_4[0]*p_4[2]-2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[2]+4*p_2[2]*p_3[1]*p_3[2]*p_4[2]*p_2[0]*p_2[1]-4*p_2[2]*p_4[1]*p_4[2]*p_3[2]*p_2[0]*p_2[1],
                    0,  0,  0,  1,  0,  -power(p_2[2],2)*power(p_4[0],2)*power(p_3[1],2)+power(p_2[2],3)*power(p_4[0],2)*p_3[2]+p_4[2]*power(p_2[2],3)*power(p_3[1],2)+power(p_2[2],2)*power(p_3[2],2)*power(p_4[1],2)+power(p_2[2],2)*power(p_3[0],2)*power(p_4[2],2)+power(p_2[2],2)*power(p_3[0],2)*power(p_4[1],2)-power(p_2[2],3)*power(p_3[0],2)*p_4[2]-p_3[2]*power(p_2[2],3)*power(p_4[1],2)-power(p_2[2],2)*power(p_4[2],2)*power(p_3[1],2)-power(p_2[2],2)*power(p_4[0],2)*power(p_3[2],2)+p_2[2]*power(p_4[2],2)*p_3[2]*power(p_2[1],2)+p_2[2]*power(p_4[0],2)*p_3[2]*power(p_2[1],2)+p_4[2]*power(p_2[0],2)*p_2[2]*power(p_3[2],2)+p_4[2]*power(p_2[0],2)*p_2[2]*power(p_3[1],2)-p_2[2]*power(p_3[2],2)*p_4[2]*power(p_2[1],2)-p_2[2]*power(p_3[0],2)*p_4[2]*power(p_2[1],2)-p_3[2]*power(p_2[0],2)*p_2[2]*power(p_4[2],2)-p_3[2]*power(p_2[0],2)*p_2[2]*power(p_4[1],2)
    ])

    B_eigen = np.array([ 
        1,  0,  0,  0,  0,  0,
        0,  1,  0,  0,  0,  0,
        0,  0,  1,  0,  0,  0,
        0,  0,  0,  1,  0,  0,
        0,  0,  0,  0,  0,  2*p_2[2]*power(p_4[2],2)*p_3[2]*p_2[0]*p_2[1]+2*p_2[2]*power(p_4[0],2)*p_3[2]*p_2[0]*p_2[1]+2*p_4[2]*power(p_2[0],2)*p_2[2]*p_3[0]*p_3[1]-2*p_2[2]*power(p_3[2],2)*p_4[2]*p_2[0]*p_2[1]-2*p_2[2]*power(p_3[0],2)*p_4[2]*p_2[0]*p_2[1]-2*p_3[2]*power(p_2[0],2)*p_2[2]*p_4[0]*p_4[1]-2*power(p_4[2],2)*power(p_2[2],2)*p_3[0]*p_3[1]-2*power(p_2[2],2)*power(p_4[0],2)*p_3[0]*p_3[1]+2*p_4[2]*power(p_2[2],3)*p_3[0]*p_3[1]+2*power(p_3[2],2)*power(p_2[2],2)*p_4[0]*p_4[1]+2*power(p_2[2],2)*power(p_3[0],2)*p_4[0]*p_4[1]-2*p_3[2]*power(p_2[2],3)*p_4[0]*p_4[1],
        0,  0,  0,  0,  0,  0
    ])

    A= A_eigen.reshape(N,N)
    B= B_eigen.reshape(N,N)

    [alphar,alphai,beta,vi,vr,work,info] =sp.dggev(A,B,compute_vl=0,compute_vr=1,lwork=16*N    )

    vr2=vr.reshape(N*N)

    myList=[]
    cols=[]
    anz=0

    for i in range(N):
        # print ("found solution",i,beta[i],alphai[i])
        if beta[i]!=0 and alphai[i]==0:
            #print ("real solution ",i,anz,displaynumber)
            print ("found real solution",i,anz,displaynumber,"beta, alphai",beta[i],alphai[i])
            anz += 1
            if not (anz==displaynumber or displaynumber==0):
                continue

            a=vr[N-2,i]/vr[N-1,i];
            b=alphar[i]/beta[i];
            r=((a*a+b*b-1)*p_2[2]*p_2[2]+2*(a*p_2[0]+b*p_2[1])*p_2[2]+(b*p_2[0]-a*p_2[1])*(b*p_2[0]-a*p_2[1]))/(2*(a*a+b*b)*p_2[2]);
            q=App.Vector(0,0,r);

            apex=App.Vector(a*r,b*r,0);
            axis=(q-apex).normalize();

            print ("apex ",apex)
            print ("axis ",axis)

            sin_angle = (p_1-apex).dot(axis)/((p_1-apex).Length*axis.Length);
            cos_angle = ((p_1-apex).cross(axis)).Length/((p_1-apex).Length*axis.Length);
            
            r0 = np.arctan2(sin_angle , cos_angle);
            #alpha=np.pi/2-r0

            l1=min((p_1-apex).dot(axis),(p_2-apex).dot(axis));
            l2=max((p_1-apex).dot(axis),(p_2-apex).dot(axis));
            myList += [("Cone",apex,axis,r0,l1,l2)];

            pts=[apex,p_1,apex,p_2,apex,p_3,apex,p_4]

            if 0:
                print ("Laengen")
                print (axis.dot((apex-p_1).normalize()))
                print (axis.dot((apex-p_2).normalize()))
                print (axis.dot((apex-p_3).normalize()))
                print (axis.dot((apex-p_4).normalize()))

            h=500

            cmps=[]
            for p in [p_4,p_1,p_2,p_3,apex]:
                s=Part.makeSphere( 12)
                s.Placement.Base=p
                cmps += [s]

            alpha=np.pi/2-r0
            print ("alpha ",alpha*180/np.pi)

            [a,bounds]=    drawConeB(apex,axis,alpha,h,trafo,[p_4,p_1,p_2,p_3])
            cols += [a]

            if displayFaces:
                drawConeA(name,anz,bounds,apex,axis,alpha,trafo,[p_4,p_1,p_2,p_3]) # kegelflaeche zeigen 

    return cols


class PointFace(FeaturePython):
    '''a face reconstructed by some points and normales'''

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLink","L1")
        obj.addProperty("App::PropertyLink","L2")
        obj.addProperty("App::PropertyLink","L3")
        obj.addProperty("App::PropertyLink","L4")

        obj.addProperty("App::PropertyVector","P1").P1=App.Vector(50,0,0)
        obj.addProperty("App::PropertyVector","P2").P2=App.Vector(0,50,5)
        obj.addProperty("App::PropertyVector","P3").P3=App.Vector(-50,0,-1)
        obj.addProperty("App::PropertyVector","P4").P4=App.Vector(0,-50,-5)
        obj.addProperty("App::PropertyVector","P5").P5=App.Vector(0,-50,-5)
        obj.addProperty("App::PropertyVector","P6").P6=App.Vector(0,-50,-5)

        obj.addProperty("App::PropertyVector","N1").N1=App.Vector(10,0,10)
        obj.addProperty("App::PropertyVector","N2").N2=App.Vector(-5,0,10)
        obj.addProperty("App::PropertyVector","N3").N3=App.Vector(-5,0,10)
        obj.addProperty("App::PropertyVector","N4").N4=App.Vector(-5,0,10)

        
        obj.addProperty("App::PropertyInteger","number").number=0
        obj.addProperty("App::PropertyBool","displayPoints").displayPoints=1
        obj.addProperty("App::PropertyBool","displayFaces").displayFaces=1
        obj.addProperty("App::PropertyEnumeration","mode")
        obj.mode=['parameters','tripod','spheres and cones','vertexes']

        obj.addProperty("App::PropertyEnumeration","pattern")
        obj.pattern=['pnpn','pnppp','pnpnpnpn']
        obj.addProperty("App::PropertyEnumeration","target")
        obj.target=['Cone','Shpere','Cylinder','Torus','Plane']

        obj.addProperty("App::PropertyVector","apex",'~aux').apex=App.Vector(30,30,30)
        obj.addProperty("App::PropertyVector","axis",'~aux').axis=App.Vector(10,0,0)

        obj.setEditorMode('apex',2)
        obj.setEditorMode('axis',2)


    def myOnChanged(self,obj,prop):

        if prop in ["Shape","Label"]:
            return


        try: # start not before the last prop is created
            obj.axis
        except:
            return

        if prop=='pattern':
            if obj.pattern=='pnpn':
                for a in 'P3','P4','P5','P6','L3','L4','N3','N4':
                    obj.setEditorMode(a,2)
            if obj.pattern=='pnppp':
                for a in 'N2','P5','P6','N3','N4':
                    obj.setEditorMode(a,2)

        print ("---------prop          changed       ",prop)
        if prop not in ["_init_","number",'N1','N2','P1','P2','P3','P4','P5','P6']: return

        # generic testdata
        if obj.mode=='parameters':
            sp= [obj.P1,obj.P2,obj.P3,obj.P4]
            dirs=[obj.N1,obj.N2,obj.N3,obj.N4]

        # 1. Variante Tripod
        elif obj.mode=='tripod':
            sp=[]
            dirs=[]
            if obj.L1 != None: 
                sp += [obj.L1.Shape.Vertex1.Point]
                dirs += [obj.L1.Shape.Vertex6.Point-obj.L1.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P1]
                dirs += [obj.N1]
            if obj.L2 != None: 
                dirs += [obj.L2.Shape.Vertex6.Point-obj.L2.Shape.Vertex1.Point]
                sp += [obj.L2.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P2]
                dirs += [obj.N2]
            if obj.L3 != None: 
                sp += [obj.L3.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P3]
            if obj.L4 != None: 
                sp += [obj.L4.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P4]

        # 2. Variante Parts
        elif obj.mode== 'spheres and cones':
            sp=[]
            dirs=[]
            if obj.L1 != None: 
                sf=obj.L1.Shape.Face1.Surface
                if sf.__class__.__name__ =='Sphere':
                    sp += [obj.L1.Placement.Base]
                    dirs +=  [obj.N1]
                elif sf.__class__.__name__ =='Cone':
                    sp += [sf.Apex]
                    dirs += [sf.Axis]
                else:
                    sp += [obj.L1.Shape.Vertex1.Point]
                    dirs +=  [obj.N1]
            else: 
                sp += [ obj.P1]
                dirs +=  [obj.N1]

            if obj.L2 != None: 
                sf=obj.L2.Shape.Face1.Surface
                if sf.__class__.__name__ =='Sphere':
                    sp += [obj.L2.Placement.Base]
                    dirs +=  [obj.N1]
                elif sf.__class__.__name__ =='Cone':
                    sp += [ sf.Apex ]
                    dirs += [sf.Axis]
                else:
                    sp += [obj.L2.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P2]

            if obj.L3 != None: 
                sf=obj.L3.Shape.Face1.Surface
                if sf.__class__.__name__ =='Sphere':
                    sp += [obj.L3.Placement.Base]
                    dirs +=  [obj.N1]
                elif sf.__class__.__name__ =='Cone':
                    sp += [ sf.Apex ]
                    dirs += [sf.Axis]
                else:
                    sp += [obj.L3.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P3]

            if obj.L4 != None: 
                sf=obj.L4.Shape.Face1.Surface
                if sf.__class__.__name__ =='Sphere':
                    sp += [obj.L4.Placement.Base]
                    dirs +=  [obj.N1]
                elif sf.__class__.__name__ =='Cone':
                    sp += [ sf.Apex ]
                    dirs += [sf.Axis]
                else:
                    sp += [obj.L4.Shape.Vertex1.Point]
            else: 
                sp += [ obj.P4]

        print (dirs)
        dirsa=[App.Vector(p).normalize() for p in dirs]
        dirs=dirsa

        p1=sp[0]
        pma=App.Placement(-p1,App.Rotation())
        pmb=App.Placement(App.Vector(),App.Rotation(dirs[0],App.Vector(0,0,1)))
        trafo=pmb.multiply(pma)

        cmps=[]

        if obj.displayPoints:
            for p in sp[0:2]:
                    s=Part.makeSphere(2)
                    s.Placement.Base=p
                    cmps += [s]

        pts_norm=[trafo.multVec(p) for p in sp]
        dirs_norm=[pmb.multVec(p) for p in dirs]

        name=obj.Name

        if obj.pattern=='pnppp':
            rc=run_conepnppp(name,trafo,obj.number,obj.displayFaces,*pts_norm)

        elif obj.pattern=='pnpn':

            [p_1,p_2]=pts_norm[0:2]
            [n_1,n_2]=dirs_norm[0:2]

            rc=run_conepnpn(p_1,n_1,p_2,n_2,name,trafo,obj.number,obj.displayFaces)

        elif obj.pattern=='pnpnpnpn':

            [p_1,p_2,p_3,p_4]=pts_norm[0:4]
            [n_1,n_2,n_3,n_4]=dirs_norm[0:4]

            rc=run_4pn(p_1,n_1,p_2,n_2,p_3,n_3,p_4,n_4,name,trafo,obj.number,obj.displayFaces)

        obj.Shape= Part.Compound(rc +cmps)


    def myExecute(self,obj):
        self.onChanged(obj,"_init_")
        # print obj.Label," executed"



def PointstoConePNPPP():
    '''create a cone by point,normal and 3 points'''  

    sel=Gui.Selection.getSelection()
#    if len(sel) != 4:
#        print ("selection reicht nicht 4 "
#        return
    
    yy=App.ActiveDocument.addObject("Part::FeaturePython","PointFace")
    PointFace(yy)
    yy.pattern='pnppp'
    
    if len(sel)==4:
        # mode p n p p p

        y=sel[0]
        if y.TypeId == 'Part::Cone':
            yy.mode = 'spheres and cones'
        elif y.TypeId == 'Part::FeaturePython' and y.Proxy.__class__.__name__ =='Tripod':
            yy.mode = 'tripod'

        [yy.L1,yy.L2,yy.L3,yy.L4]=sel

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineColor=(.9,.9,0.)
    #yy.Proxy.myOnChanged(yy,"_init_")
    return yy


def PointstoConePNPN():
    '''create a cone by point,normal, point2.normal2'''

    sel=Gui.Selection.getSelection()
#    if len(sel) != 2:
#        print ("selection reicht nicht 4 "
#        return
    
    yy=App.ActiveDocument.addObject("Part::FeaturePython","PointFace")
    PointFace(yy)
    
#    yy.P1=App.Vector()
#    yy.P2=App.Vector(50,0,70)
#    yy.N1=App.Vector(0,0,1)
#    yy.N2=App.Vector(37,0,26)# .normalize()

    
    yy.pattern='pnpn'#,'pnppp']
    if len(sel)==4:
        # mode p n p p p

        y=sel[0]
        if y.TypeId == 'Part::Cone':
            yy.mode = 'spheres and cones'
        elif y.TypeId == 'Part::FeaturePython' and y.Proxy.__class__.__name__ =='Tripod':
            yy.mode = 'tripod'

        [yy.L1,yy.L2,yy.L3,yy.L4]=sel

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineColor=(.9,.9,0.)
    #yy.Proxy.myOnChanged(yy,"_init_")
    return yy


def PointstoBezierPNPNPNPN():
    '''create a cone by 4 point,normal,'''

    sel=Gui.Selection.getSelection()
#    if len(sel) != 2:
#        print ("selection reicht nicht 4 "
#        return
    
    yy=App.ActiveDocument.addObject("Part::FeaturePython","PointFace")
    PointFace(yy)
    
#    yy.P1=App.Vector()
#    yy.P2=App.Vector(50,0,70)
#    yy.N1=App.Vector(0,0,1)
#    yy.N2=App.Vector(37,0,26)# .normalize()

    
    yy.pattern='pnpnpnpn'
    if len(sel)==4:
        # mode p n p p p

        y=sel[0]
        if y.TypeId == 'Part::Cone':
            yy.mode = 'spheres and cones'
        elif y.TypeId == 'Part::FeaturePython' and y.Proxy.__class__.__name__ =='Tripod':
            yy.mode = 'tripod'

        [yy.L1,yy.L2,yy.L3,yy.L4]=sel

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineColor=(.9,.9,0.)
    #yy.Proxy.myOnChanged(yy,"_init_")
    return yy



def    run_conepnpn(p_1,n_1,p_2,n_2,name='PNPN_Test',trafo=None,displaynumber=0,displayFaces=True):
    '''2 points p1,p2 with normals n1,n2'''

    THRESHOLD=0.1
    cols=[]

    if displaynumber in  [0,1]:
        l_1=p_2.dot(n_2)/(n_2[2]+1);
        l_2=-p_2[2]/(1+n_2[2]);

        A1 = l_1 * n_1;
        A2 = l_2 * n_2 + p_2;


        if ((A2-A1).Length>THRESHOLD):

            axis = (A2-A1).normalize();
            apex=App.Vector(l_1*(n_2[0]*l_2+p_2[0])/(-l_2*n_2[2]+l_1-p_2[2]),
                          l_1*(n_2[1]*l_2+p_2[1])/(-l_2* n_2[2]+l_1-p_2[2]),
                          0);

        else:
            apex=App.Vector()
            axis= (A2X-A1X).normalize();
            
            axis = (A1-(p_1+p_2)/2).normalize();
            apex = App.Vector(l_1*p_2[0]/(2*l_1-p_2[2]),
                                l_1*p_2[0]/(2*l_1-p_2[2]),
                                0);


        print ("apex",apex)
        print ("axis",axis)

        if 0:
            print ("Laengen")
            print (axis.dot((apex-p_1).normalize()))
            print (axis.dot((apex-p_2).normalize()))

        sin_angle = (p_1-apex).dot(axis)/((p_1-apex).Length*axis.Length);
        cos_angle = ((p_1-apex).cross(axis)).Length/((p_1-apex).Length*axis.Length);
                
        r0 = np.arctan2(sin_angle , cos_angle);
        alpha=np.pi/2-r0
        print ("alpha",alpha)

        h=100
        pts=[p_1,p_2]
        #trafo=App.Placement()

        [a,bounds]=    drawConeB(apex,axis,alpha,h,trafo,pts)
        cols += [a]
        if displayFaces:
            drawConeA(name,0,bounds,apex,axis,alpha,trafo,pts) # kegelflaeche zeigen 


    if displaynumber  in [0,2]:
        #+# 2. Loesung noch dazu 

        l_1=p_2.dot(n_2)/(n_2[2]-1);
        l_2=p_2[2]/(1-n_2[2]);

        A1 = l_1 * n_1;
        A2 = l_2 * n_2 + p_2;

        if ((A2-A1).Length>THRESHOLD) :
            axis = (A2-A1).normalize();
            apex= App.Vector(    l_1*(n_2[0]*l_2+p_2[0])/(-l_2*n_2[2]+l_1-p_2[2]),
                            l_1*(n_2[1]*l_2+p_2[1])/(-l_2* n_2[2]+l_1-p_2[2]),
                            0);

        else :
            axis = (A1-(p_1+p_2)/2).normalize();
            apex = App.Vector(l_1*p_2[0]/(2*l_1-p_2[2]),
                l_1*p_2[1]/(2*l_1-p_2[2]),
                0);

        print ("apex",apex)
        print ("axis",axis)
        
        if 0:
            print ("Laengen")
            print (axis.dot((apex-p_1).normalize()))
            print (axis.dot((apex-p_2).normalize()))

        
        sin_angle = (p_1-apex).dot(axis)/((p_1-apex).Length*axis.Length);
        cos_angle = ((p_1-apex).cross(axis)).Length/((p_1-apex).Length*axis.Length);
                
        r0 = np.arctan2(sin_angle , cos_angle);
        alpha=np.pi/2-r0
        print ("alpha",alpha)
        h=100

        pts=[p_1,p_2]
        #trafo=App.Placement()

        [a,bounds]=    drawConeB(apex,axis,alpha,h,trafo,pts)
        cols += [a]
        if displayFaces:
            drawConeA(name,1,bounds,apex,axis,alpha,trafo,pts) # kegelflaeche zeigen 

    return cols


def run_bspline4pn(p_1,n_1,p_2,n_2,p_3,n_3,p_4,n_4,name,trafo,number,displayFaces):
    
    bs=Part.BSplineSurface()
    t1=(p_2-p_1).normalize()
    t2=(p_4-p_1).normalize()
    t1,t2=-n_1.cross(t2),n_1.cross(t1)
    
    k=30
    
    poles=np.array([
        p_1,p_1+k*t1,p_2-k*t1,p_2,
        p_1+k*t2,p_1+k*t1+k*t2,p_2-k*t1+k*t2,p_2+k*t2,
        p_4-k*t2,p_4+k*t1-k*t2,p_3-k*t1-k*t2,p_3-k*t2,
        p_4,p_4+k*t1,p_3-k*t1,p_3]).reshape(4,4,3)
    um=[4,4]
    uk=[0,1]

    bs.buildFromPolesMultsKnots(poles, 
                                um,um,range(len(um)),range(len(um)),False,False,3,3)
    return [bs.toShape()]



def run_cylinderpnpp(): 
    
    p_1=App.Vector()
    p_2=App.Vector(100,0,100)
    p_3=App.Vector(50,80,50)
    n1=App.Vector(0,0,1)
    p1=p_1

    a = (p_2[1]*p_2[1]+p_2[2]*p_2[2])*p_3[2] - (p_3[1]*p_3[1]+p_3[2]*p_3[2])*p_2[2];
    b = -2*(p_2[0]*p_2[1]*p_3[2] - p_3[0]*p_3[1]*p_2[2]);
    c = (p_2[0]*p_2[0]+p_2[2]*p_2[2])*p_3[2] - (p_3[0]*p_3[0]+p_3[2]*p_3[2])*p_2[2];

    if ((a == 0) and (b == 0) and (c == 0)):
        print  ("// Infinite solutions")
        return;

    cyls=[]
    # Different cases
    if (a == 0) :
        if ((c!=0)) :
            l=1;
            m=-b/c;
            v =App.Vector(l,m,0)
            if (p_2[2]!=0):
                r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                ## this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

            if (p_3[2]!=0):
                r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                ## this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
        l=1;
        m=0;
        
        v =App.Vector(l,m,0)

        if (p_2[2]!=0):
            r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
            r=abs(r);

            center=App.Vector(0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

        if (p_3[2]!=0):
            r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
            r=abs(r);

            center=App.Vector(0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

    elif (c == 0):
        m=1;
        l=-b/a;

        v =App.Vector(l,m,0)
        if (p_2[2]!=0):
            r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
            r=abs(r);

            center=App.Vector(0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

        if (p_3[2]!=0):
            r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
            r=abs(r);

            center=App.Vector(0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

        l=0;
        m=1;
        
        v =App.Vector(l,m,0)
        if (p_2[2]!=0):
            r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
            r=abs(r);

            (0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]

        if (p_3[2]!=0):
            r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
            r=abs(r);

            center=App.Vector(0,0,-r);
            l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
            # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
            cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
        
    else:
        delta = b*b-4*a*c;
        if (delta == 0):
            m = 1;
            l = -b/(2*a);
            
            v =App.Vector(l,m,0)
            if (p_2[2]!=0):
                r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
            elif (p_3[2]!=0):
                r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
        elif (delta > 0):
            m = 1;
            l = (- b + sqrt(delta)) / (2 * a);
            v =App.Vector(l,m,0)
            if (p_2[2]!=0):
                r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
            
            elif (p_3[2]!=0):
                r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
            
            l = (- b - sqrt(delta)) / (2 * a);
            v =App.Vector(l,m,0)
            if (p_2[2]!=0):
                r = 1/(2*p_2[2]) * (1/(l*l+m*m) * (-p_2[0]*m+p_2[1]*l) * (-p_2[0]*m+p_2[1]*l) + p_2[2]*p_2[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
            
            elif (p_3[2]!=0):
                r = 1/(2*p_3[2]) * (1/(l*l+m*m) * (-p_3[0]*m+p_3[1]*l) * (-p_3[0]*m+p_3[1]*l) + p_3[2]*p_3[2]);
                r=abs(r);

                center=App.Vector(0,0,-r);
                l1=min(dotProduct(p_1-center,v.normalize()),min(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                l2=max(dotProduct(p_1-center,v.normalize()),max(dotProduct(p_2-center,v.normalize()),dotProduct(p_3-center,v.normalize())));
                # this->list.push_back(Cylinder(p1+sign(p_2[2])*r*n1,Rotation*v,r,l1,l2));
                cyls += [(p1+sign(p_2[2])*r*n1,v,r,l1,l2)]
    for cyl in  cyls:
        print ("center",cyl[0],"axsi",cyl[1],"radius",cyl[3])
        Part.show(Part.makeCylinder(cyl[2],200,cyl[0],cyl[1]))
        App.ActiveDocument.ActiveObject.ViewObject.Transparency=60
        Part.show(Part.makeCylinder(cyl[2],200,cyl[0],-cyl[1]))
        App.ActiveDocument.ActiveObject.ViewObject.Transparency=60

    Part.show(Part.Compound([Part.makeSphere(5,p) for p in [p_1,p_2,p_3]]))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.,0.,0.)



def PointstoCylinderPNPP():
    '''create a cylinder by point,normal, point2, poimnt3'''


    run_cylinderpnpp()
    raise Exception("muss noch eingebettet werden")


    sel=Gui.Selection.getSelection()
#    if len(sel) != 2:
#        print ("selection reicht nicht 4 "
#        return
    
    yy=App.ActiveDocument.addObject("Part::FeaturePython","PointFace")
    PointFace(yy)
    
#    yy.P1=App.Vector()
#    yy.P2=App.Vector(50,0,70)
#    yy.N1=App.Vector(0,0,1)
#    yy.N2=App.Vector(37,0,26)# .normalize()

    
    yy.pattern='pnpp'#,'pnppp']
    
    if len(sel)==4:
        # mode p n p p p

        y=sel[0]
        if y.TypeId == 'Part::Cone':
            yy.mode = 'spheres and cones'
        elif y.TypeId == 'Part::FeaturePython' and y.Proxy.__class__.__name__ =='Tripod':
            yy.mode = 'tripod'

        [yy.L1,yy.L2,yy.L3,yy.L4]=sel

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineColor=(.9,.9,0.)
    #yy.Proxy.myOnChanged(yy,"_init_")
    return yy


def run_sphere4p(pts=None,display=0):

    # tesdaten hard  coded 
    if pts ==None:
        p1=App.Vector(0,-50,0)
        p2=App.Vector(0,140,0)
        p3=App.Vector(70,0,0)
        p4=App.Vector(0,0,60)
    else:
        [p1,p2,p3,p4]=pts


#    // Test if 2 points are equals
#   if (((p1-p2).norm() < THRESHOLD) || ((p1-p3).norm() < THRESHOLD) || ((p1-p4).norm() < THRESHOLD)|| ((p2-p3).norm() < #HRESHOLD)|| ((p2-p4).norm() < THRESHOLD)|| ((p3-p4).norm() < THRESHOLD)){
#        std::cerr<< "2 points are equals"<< endl;
#        return;
#    }
    A=np.array([(p2-p1), (p3-p2), (p4-p3)])

    b =App.Vector(
            0.5*(p2.Length**2-p1.Length**2),
            0.5*(p3.Length**2-p2.Length**2),
            0.5*(p4.Length**2-p3.Length**2),
        );

    center=App.Vector()
    AI=inv(A)
    for i in range(3):
        for j in range(3):
            center[i] += AI[i,j]*b[j]
    radius = (p1-center).Length;  

    auxshapes=[]
    if display>0:
        auxshapes += [Part.makeSphere(radius,center)]
        auxshapes += [Part.makeSphere(display,p) for p in [p1,p2,p3,p4]]

    return  (center,radius,auxshapes)

def run_plane3p(pts,display=0):
    
    [p1,p2,p3]=pts
    print ("run plan 3p")
    n=(p1-p2).cross(p1-p3).normalize()
    c=p1.dot(n)
    c2=p2.dot(n)
    center=c*n
    aux=Part.makeCircle(10,p1,n)
    print (c,c2) 
    print (center)
    print (n)
    return (center,n,aux)


def run_spherepnp(): # pn p 
#   // Test if the Normal is not 0 0 0
 #   if ((abs(N(0))<THRESHOLD) && (abs(N(1))<THRESHOLD) && (abs(N(2))<THRESHOLD)){
  #      std::cerr<< "Normal is undefined"<< endl;
   #     return;
   # }
   # // Test if 2 points are equals
   # if ((p1-p2).norm() < THRESHOLD) {
   #     std::cerr<< "2 points are equals"<< endl;
   #     return;
   # }
    p1=App.Vector(10,140,0)
    p2=App.Vector(-100,0,-100)
    N=App.Vector(0,0,-1).normalize()

    A =np.array([
        1, 0, 0, N[0],
        0, 1, 0, N[1],
        0, 0, 1, N[2],
        (p2-p1)[0], (p2-p1)[1], (p2-p1)[2], 0]).reshape(4,4)

    b = np.array([p1[0],p1[1],p1[2],0.5*(p2.Length**2-p1.Length**2)]);
    s=np.zeros(4)
    AI=inv(A)
    for i in range(4):
        for j in range(4):
            s[i] += AI[i,j]*b[j]

    center =App.Vector(s[0:3])
    radius = abs(s[3]);

    Part.show(Part.makeSphere(radius,center))
    Part.show(Part.Compound([Part.makeSphere(5,p) for p in [p1,p2]]))
    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.,0.,0.)

def run_cylinder5p(pts=None,display=True,pointsize=10,maxradius=100000):

    THRESHOLD = 0.001
    debug=False

    if pts == None:
        p1=App.Vector(100,0,0)
        p2=App.Vector(100,70,20)
        p3=App.Vector(-100,100,0)

        p4=p2+App.Vector(0,0,200)
        p5=p3+App.Vector(0,0,200)
    else:
        [p1,p2,p3,p4,p5]=pts

    nx = (p2-p1).normalize();
    ny = ((p3-p1)-(p3-p1).dot(nx)*nx).normalize();
    nz = nx.cross(ny).normalize();

    trafo=App.Rotation(
            nx.x,nx.y,nx.z,
            ny.x,ny.y,ny.z,
            nz.x,nz.y,nz.z,
        )

    ps=[]
    for p in [p1,p2,p3,p4,p5]:
        t=trafo.multVec(p-p1)
        ps += [t]

    [p_1,p_2,p_3,p_4,p_5]=ps


    if 0:
        # Five Points ##############################
        p_1=App.Vector(0,0,0)
        p_2=App.Vector(100,0,0)
        p_3=App.Vector(0,100,0)
        p_4=App.Vector(0,0,100)
        p_5=App.Vector(100,0,100) # eine loesung falsch
        
        p_5=App.Vector(100,100,100) # 5 fehler
        p_5=App.Vector(0,100,100) # 3 fehler
        p_4,p_5=p_5,p_4

        p_4=App.Vector(100,0,100)
        p_5=App.Vector(100,100,100)
        p_4,p_5=p_5,p_4


        p_1=App.Vector(0,0,0)
        p_2=App.Vector(100,0,0)
        p_3=App.Vector(-100,100,0)

        p_4=p_2+App.Vector(0,0,200)
        p_5=p_3+App.Vector(0,0,200)
        
        p_4=p_2+App.Vector(0,0,200)
        p_5=p_3+App.Vector(0,10,200)

        p_4=p_2+App.Vector(20,0,200)
        p_5=p_3+App.Vector(0,10,200)


    trafo.invert()


    if debug:
        print ("Points ...")
        for p in [p_1,p_2,p_3,p_4,p_5]:
            print (p)

    #    if ((abs(p_3(1)) < THRESHOLD) && (abs(p_3(0)) > THRESHOLD) ){ // p_1 p_2 p_3 are aligned so infinite or no cylinder
    #
     #       return;
      #  }        
    #
     #   if ((abs(p_4(2)) < THRESHOLD) && (abs(p_5(2)) < THRESHOLD)) {
    #
      #      return;
     #   }

#    if (abs(p_4[2]) < THRESHOLD): 
#        p_4,p_5 = p_5,p_4

    N = 12;
    A = np.array([
            0,  0,  0,  0,  0,  0,  0,  0,  -p_2[0]*p_3[1]*(-p_3[1]*p_4[1]+power(p_4[1],2)+power(p_4[2],2)),
                                                -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_4[0]*p_3[1]*p_4[2],
                                                    -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]+p_2[0]*power(p_3[1],2)*p_4[1]-p_2[0]*p_3[1]*power(p_4[1],2),
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  -p_2[0]*p_3[1]*(-p_3[1]*p_4[1]+power(p_4[1],2)+power(p_4[2],2)),
                                                    -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_4[0]*p_3[1]*p_4[2],
                                                        -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]+p_2[0]*power(p_3[1],2)*p_4[1]-p_2[0]*p_3[1]*power(p_4[1],2),
            0,  0,  0,  0,  0,  0,  0,  0,  power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                2*p_4[0]*p_3[1]*p_4[2]*p_5[2]-2*p_5[0]*p_3[1]*p_4[2]*p_5[2],
                                                    -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]+power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2],
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                    2*p_4[0]*p_3[1]*p_4[2]*p_5[2]-2*p_5[0]*p_3[1]*p_4[2]*p_5[2],
                                                        -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]+power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2],
            1,  0,  0,  0,  0,  0,  0,  0,  -p_4[2]*power(p_3[1],2)*p_2[0],
                                                -2*p_2[0]*p_3[0]*p_3[1]*p_4[1]+2*p_2[0]*p_4[0]*p_3[1]*p_4[1],
                                                    power(p_2[0],2)*p_3[0]*p_4[2]-p_2[0]*power(p_3[0],2)*p_4[2]-p_4[2]*power(p_3[1],2)*p_2[0]+2*p_2[0]*p_3[1]*p_4[1]*p_4[2],
                                                        0,
            0,  1,  0,  0,  0,  0,  0,  0,  0,  -p_4[2]*power(p_3[1],2)*p_2[0],
                                                    -2*p_2[0]*p_3[0]*p_3[1]*p_4[1]+2*p_2[0]*p_4[0]*p_3[1]*p_4[1],
                                                        power(p_2[0],2)*p_3[0]*p_4[2]-p_2[0]*power(p_3[0],2)*p_4[2]-p_4[2]*power(p_3[1],2)*p_2[0]+2*p_2[0]*p_3[1]*p_4[1]*p_4[2],
            0,  0,  1,  0,  0,  0,  0,  0,  0,  -2*p_3[0]*p_3[1]*p_4[1]*p_5[2]+2*p_3[0]*p_3[1]*p_5[1]*p_4[2]+2*p_4[0]*p_3[1]*p_4[1]*p_5[2]-2*p_5[0]*p_3[1]*p_5[1]*p_4[2],
                                                    2*p_3[1]*p_4[1]*p_4[2]*p_5[2]-2*p_3[1]*p_5[1]*p_4[2]*p_5[2],
                                                        0,
            0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  -2*p_3[0]*p_3[1]*p_4[1]*p_5[2]+2*p_3[0]*p_3[1]*p_5[1]*p_4[2]+2*p_4[0]*p_3[1]*p_4[1]*p_5[2]-2*p_5[0]*p_3[1]*p_5[1]*p_4[2],
                                                        2*p_3[1]*p_4[1]*p_4[2]*p_5[2]-2*p_3[1]*p_5[1]*p_4[2]*p_5[2],
            0,  0,  0,  0,  1,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_3[0]*p_3[1]*p_4[2],
                                                    -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]-p_2[0]*p_3[1]*power(p_4[2],2),
                                                        0,
            0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_3[0]*p_3[1]*p_4[2],
                                                        -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]-p_2[0]*p_3[1]*power(p_4[2],2),
            0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2)
            ]).reshape(N,N)

    B = np.array([
            1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  
                -power(p_2[0],2)*p_3[0]*p_4[2]+p_2[0]*power(p_3[0],2)*p_4[2],0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  
                -power(p_2[0],2)*p_3[0]*p_4[2]+p_2[0]*power(p_3[0],2)*p_4[2],
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            ]).reshape(N,N)

    #A=A.swapaxes(0,1)
    #B=B.swapaxes(0,1)

    [alphar,alphai,beta,vi,vr,work,info] =sp.dggev(A,B,compute_vl=1,compute_vr=1,lwork=16*N    )

    # vr2=vr.reshape(N*N)
    vr2=vr.swapaxes(0,1).reshape(N*N)

    if debug:
        print ("VR")
        print (np.round(vr,5))

    myList=[]
    cols=[]
    anz=0

    if debug:
        print ("beta")
        print (beta)
        print ("alphar")
        print (alphar)
        print ("alphai")
        print (alphai)
    
    cyls=[]
    cylsrc=[]
    # Generating the cones correspondinng to the real non-infinite eigenvalues
    for i in range(N):
#        if(beta[i]!=0 and alphai[i]==0):
        if(alphai[i]==0):
            if debug:
                print ("")
                print ("SSolution",i)
                print ("beta ",beta[i])
                print ("alphar[i]",alphar[i])
                print ("vr2",vr2[N-2+i*N],vr2[N-1+i*N])

            _ty=alphar[i]/beta[i]
            _t=vr2[N-2+i*N]/vr2[N-1+i*N]

            if beta[i]==0:
                _ty=100000

            if np.isnan(_t) or np.isinf(_t):
                print ("_t is nan------------------")
                _t=100000

            axis = App.Vector(_t,_ty,1).normalize();

            a = p_1 - p_1.dot(axis)*axis;
            b = p_2 - p_2.dot(axis)*axis;
            c = p_3 - p_3.dot(axis)*axis;

            la = (b-c).Length;
            lb = (c-a).Length;
            lc = (a-b).Length;
            sa = .5*(-la*la + lb*lb + lc*lc);
            sb = .5*( la*la - lb*lb + lc*lc);
            sc = .5*( la*la + lb*lb - lc*lc);

            center_bar = App.Vector(la*la*sa,lb*lb*sb,lc*lc*sc);
#            print ("center bar"
#            print center_bar

            center_bar = center_bar / (center_bar[0]+center_bar[1]+center_bar[2]);
#            print center_bar
            center = center_bar[0]*a + center_bar[1]*b + center_bar[2]*c;

            r0 = ((la*la*lb*lb*lc*lc)/ (4*power((crossProduct(b-a,c-a).Length),2)))**0.5;

            l1=min(dotProduct(p_1-center,axis),min(dotProduct(p_2-center,axis),min(dotProduct(p_3-center,axis),min(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));
            l2=max(dotProduct(p_1-center,axis),max(dotProduct(p_2-center,axis),max(dotProduct(p_3-center,axis),max(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));

            if debug:
                print ("center",center)
                print ("axis",axis)
                print ("r0",r0)

                print (l1,l2)

            if maxradius != 0 and r0> maxradius:
                print ("Fehler radius zu gross",round(r0,1),round(maxradius,1))
                continue

            cylsrc += [[trafo.multVec(center)+p1,trafo.multVec(axis),r0,l1,l2,i]]
            cyls += [[center,axis,r0,l1,l2,i]]


    aux=[]
    if display:
        if debug:
            print ()
            print ("create 3D objects---------------------------------------------")
        for cyl in  cyls:
                if cyl[2]>500:
#                    print ("radius zu gross"
                    continue
                if np.isnan(cyl[3]):
                    print ("nan cancellation")
                    continue
                if debug:
                    print ("center ",cyl[0])
                    print ("axis",cyl[1])
                    print ("radius",cyl[2])
                    print (cyl[3])
                    print (cyl[4])
                    print
                comps=[]
                comps += [Part.makeCylinder(cyl[2],200,cyl[0],cyl[1])]
                comps += [Part.makeCylinder(cyl[2],200,cyl[0],-cyl[1])]
                comps += [Part.makePolygon([cyl[0]-cyl[1]*200,cyl[0]+cyl[1]*200])]
                if 0:
                    Part.show(Part.Compound(comps))
                    App.ActiveDocument.ActiveObject.ViewObject.Transparency=60
                    App.ActiveDocument.ActiveObject.Label="Solution "+str(cyl[5])
                    App.ActiveDocument.ActiveObject.Placement=App.Placement(p1,trafo)
                else:
                    auxr=Part.Compound(comps)
                    auxr.Placement=App.Placement(p1,trafo)
                    aux += [auxr]

    if pointsize != 0:
        Part.show(Part.Compound([Part.makeSphere(pointsize,p) for ik,p in enumerate([p_1,p_2,p_3,p_4,p_5])]))
        App.ActiveDocument.ActiveObject.Placement=App.Placement(p1,trafo)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.,0.,0.)


    return (cylsrc,aux)



def run_cone6p():
    raise Exception("# geht noch nicht c++ quelle auch nicht.")

    p_1=App.Vector(0,0,0)
    p_2=App.Vector(10,0,0) #x!=0
    p_3=App.Vector(0,10,0) #y!=0
    p_4=App.Vector(0,0,20) #z!=0
    p_5=App.Vector(25,0,20) #z!=0
    p_6=App.Vector(0,25,20) 


    N = 12;



    A =np.array([
            0,  0,  0,  0,  0,  0,  0,  0,  -p_2[0]*p_3[1]*(-p_3[1]*p_4[1]+power(p_4[1],2)+power(p_4[2],2)),
                                                -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_4[0]*p_3[1]*p_4[2],
                                                    -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]+p_2[0]*power(p_3[1],2)*p_4[1]-p_2[0]*p_3[1]*power(p_4[1],2),
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  -p_2[0]*p_3[1]*(-p_3[1]*p_4[1]+power(p_4[1],2)+power(p_4[2],2)),
                                                    -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_4[0]*p_3[1]*p_4[2],
                                                        -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]+p_2[0]*power(p_3[1],2)*p_4[1]-p_2[0]*p_3[1]*power(p_4[1],2),
            0,  0,  0,  0,  0,  0,  0,  0,  power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                2*p_4[0]*p_3[1]*p_4[2]*p_5[2]-2*p_5[0]*p_3[1]*p_4[2]*p_5[2],
                                                    -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]+power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2],
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                    2*p_4[0]*p_3[1]*p_4[2]*p_5[2]-2*p_5[0]*p_3[1]*p_4[2]*p_5[2],
                                                        -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]+power(p_3[1],2)*p_4[1]*p_5[2]-power(p_3[1],2)*p_5[1]*p_4[2]-p_3[1]*power(p_4[1],2)*p_5[2]+p_3[1]*power(p_5[1],2)*p_4[2],
            1,  0,  0,  0,  0,  0,  0,  0,  -p_4[2]*power(p_3[1],2)*p_2[0],
                                                -2*p_2[0]*p_3[0]*p_3[1]*p_4[1]+2*p_2[0]*p_4[0]*p_3[1]*p_4[1],
                                                    power(p_2[0],2)*p_3[0]*p_4[2]-p_2[0]*power(p_3[0],2)*p_4[2]-p_4[2]*power(p_3[1],2)*p_2[0]+2*p_2[0]*p_3[1]*p_4[1]*p_4[2],
                                                        0,
            0,  1,  0,  0,  0,  0,  0,  0,  0,  -p_4[2]*power(p_3[1],2)*p_2[0],
                                                    -2*p_2[0]*p_3[0]*p_3[1]*p_4[1]+2*p_2[0]*p_4[0]*p_3[1]*p_4[1],
                                                        power(p_2[0],2)*p_3[0]*p_4[2]-p_2[0]*power(p_3[0],2)*p_4[2]-p_4[2]*power(p_3[1],2)*p_2[0]+2*p_2[0]*p_3[1]*p_4[1]*p_4[2],
            0,  0,  1,  0,  0,  0,  0,  0,  0,  -2*p_3[0]*p_3[1]*p_4[1]*p_5[2]+2*p_3[0]*p_3[1]*p_5[1]*p_4[2]+2*p_4[0]*p_3[1]*p_4[1]*p_5[2]-2*p_5[0]*p_3[1]*p_5[1]*p_4[2],
                                                    2*p_3[1]*p_4[1]*p_4[2]*p_5[2]-2*p_3[1]*p_5[1]*p_4[2]*p_5[2],
                                                        0,
            0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  -2*p_3[0]*p_3[1]*p_4[1]*p_5[2]+2*p_3[0]*p_3[1]*p_5[1]*p_4[2]+2*p_4[0]*p_3[1]*p_4[1]*p_5[2]-2*p_5[0]*p_3[1]*p_5[1]*p_4[2],
                                                        2*p_3[1]*p_4[1]*p_4[2]*p_5[2]-2*p_3[1]*p_5[1]*p_4[2]*p_5[2],
            0,  0,  0,  0,  1,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_3[0]*p_3[1]*p_4[2],
                                                    -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]-p_2[0]*p_3[1]*power(p_4[2],2),
                                                        0,
            0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[1]*p_4[2]+2*p_2[0]*p_3[0]*p_3[1]*p_4[2],
                                                        -power(p_2[0],2)*p_3[0]*p_4[1]+power(p_2[0],2)*p_4[0]*p_3[1]+p_2[0]*power(p_3[0],2)*p_4[1]-p_2[0]*power(p_4[0],2)*p_3[1]-p_2[0]*p_3[1]*power(p_4[2],2),
            0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2),
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  -p_2[0]*p_3[0]*p_4[1]*p_5[2]+p_2[0]*p_3[0]*p_5[1]*p_4[2]+p_2[0]*p_4[0]*p_3[1]*p_5[2]-p_2[0]*p_5[0]*p_3[1]*p_4[2]+power(p_3[0],2)*p_4[1]*p_5[2]-power(p_3[0],2)*p_5[1]*p_4[2]-power(p_4[0],2)*p_3[1]*p_5[2]+power(p_5[0],2)*p_3[1]*p_4[2]-p_3[1]*power(p_4[2],2)*p_5[2]+p_3[1]*p_4[2]*power(p_5[2],2)
            ]).reshape(N,N)

    B =np.array([
            1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[0]*p_4[2]+p_2[0]*power(p_3[0],2)*p_4[2],
                                                        0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  -power(p_2[0],2)*p_3[0]*p_4[2]+p_2[0]*power(p_3[0],2)*p_4[2],
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]).reshape(N,N)


    [alphar,alphai,beta,vi,vr,work,info] =sp.dggev(A,B,compute_vl=1,compute_vr=1,lwork=16*N    )

    # vr2=vr.reshape(N*N)
    vr2=vr.swapaxes(0,1).reshape(N*N)

    print ("VR")
    print (np.round(vr,5))

    myList=[]
    cols=[]
    anz=0

#-----------------------------------------------------------------

    cyls=[]
    cylsrc=[]
    # Generating the cones correspondinng to the real non-infinite eigenvalues
    for i in range(N):
#        if(beta[i]!=0 and alphai[i]==0):
        if(alphai[i]==0):
            print 
            print ("SSolution",i)
            print ("beta ",beta[i])
            print ("alphar[i]",alphar[i])
            print ("vr2",vr2[N-2+i*N],vr2[N-1+i*N])
            _ty=alphar[i]/beta[i]
            _t=vr2[N-2+i*N]/vr2[N-1+i*N]

            print ("Vektor komponenten")
            print(_t)
            print (alphar[i]/beta[i])

            if beta[i]==0:
                _ty=100000

            if np.isnan(_t) or np.isinf(_t):
                print ("_t is nan------------------")
                _t=100000

            axis = App.Vector(_t,_ty,1).normalize();

            # axis = App.Vector(vr2[N-1+i*N]/vr2[N-2+i*N],1.0/(alphar[i]/beta[i]),1).normalize();
            print ("axis",axis)


            a = p_1 - p_1.dot(axis)*axis;
            b = p_2 - p_2.dot(axis)*axis;
            c = p_3 - p_3.dot(axis)*axis;


            la = (b-c).Length;
            lb = (c-a).Length;
            lc = (a-b).Length;
            sa = .5*(-la*la + lb*lb + lc*lc);
            sb = .5*( la*la - lb*lb + lc*lc);
            sc = .5*( la*la + lb*lb - lc*lc);


            center_bar = App.Vector(la*la*sa,lb*lb*sb,lc*lc*sc);
            print ("center bar")
            print (center_bar)

            center_bar = center_bar / (center_bar[0]+center_bar[1]+center_bar[2]);
            print (center_bar)
            center = center_bar[0]*a + center_bar[1]*b + center_bar[2]*c;

            r0 = ((la*la*lb*lb*lc*lc)/ (4*power((crossProduct(b-a,c-a).Length),2)))**0.5;

            l1=min(dotProduct(p_1-center,axis),min(dotProduct(p_2-center,axis),min(dotProduct(p_3-center,axis),min(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));
            l2=max(dotProduct(p_1-center,axis),max(dotProduct(p_2-center,axis),max(dotProduct(p_3-center,axis),max(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));

#            double l1=min(dotProduct(p_1-center,axis),min(dotProduct(p_2-center,axis),min(dotProduct(p_3-center,axis),min(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));
#            double l2=max(dotProduct(p_1-center,axis),max(dotProduct(p_2-center,axis),max(dotProduct(p_3-center,axis),max(dotProduct(p_4-center,axis),dotProduct(p_5-center,axis)))));

#            this->list.push_back(Cone(p1+Rotation*center,Rotation*axis,r0,l1,l2));



            print ("center",center)
#            print ("axis",axis)
            print ("r0",r0)
            print (l1,l2)
            if r0> 10000:
                print ("Fehler radius zu gross")
                continue
            #cylsrc += [[trafo.multVec(center)+p1,trafo.multVec(axis),r0,l1,l2,i]]
            cyls += [[center,axis,r0,l1,l2,i]]


#------------------------------------------------------------------

            for c in cyls:
                print (np.round(center,2),np.round(axis,2))





#--------- massendaten auswerten

def discoverSpheres():
    ''' sphere mittelwert aus punktemenge finden'''

    a=time.time()

    pts= App.ActiveDocument.Mesh.Mesh.Topology[0]

    loops=1000
    l=len(pts)
    
    res=[]
    for i in range(loops):
#        print i
        sel=[pts[random.randint(0,l-1)]+App.Vector(0.5-random.random(),10*(0.5-random.random()),0.5-random.random()) for j in range(4)]
        res += [.points_to_face.run_sphere4p(sel,display=False) ]



    res=np.array(res).swapaxes(0,1)


    print (np.sum(res[0])/loops)
    print (np.mean(res[1]))
    print (np.std(res[1]))
    print (time.time()-a)

# findSphere()



def PointstoCylinder5P ():
    '''5 Punkte zu cylinder'''

    (cylsrc,aux)=run_cylinder5p()
    Part.show(Part.Compound(aux))


def PointstoSpherePNP ():
    run_spherepnp()

def PointstoSphere4P ():
    run_sphere4p()






#def AA():
#    '''5 Punkte zu cylinder'''
#    PointstoCylinder5P ()

#---------------------------


class ReconstructFace(FeaturePython):


    def __init__(self, obj):
        FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyLink", "A", "AX", "X", 8)# no impact recompute
        obj.addProperty("App::PropertyLink", "B", "AX", "X", 8)# no impact recompute

        obj.addProperty("App::PropertyLink","Source")
        obj.addProperty("App::PropertyLinkSubList","SourceFaces")

        obj.addProperty("App::PropertyInteger","number").number=0
#        obj.addProperty("App::PropertyBool","displayPoints").displayPoints=1
#        obj.addProperty("App::PropertyBool","displayFaces").displayFaces=1
        obj.addProperty("App::PropertyEnumeration","mode")
        obj.mode=['Cone','Sphere','Cylinder','Torus','Plane']

#        obj.addProperty("App::PropertyEnumeration","pattern")
#        obj.pattern=['pnpn','pnppp','pnpnpnpn']

        obj.addProperty("App::PropertyFloat","tol").tol=0.01
        obj.tol=1
        obj.addProperty("App::PropertyEnumeration","displayMode")
        obj.displayMode=['leftover','found','borders','aux']
        


#        obj.addProperty("App::PropertyVector","apex",'~aux').apex=App.Vector(30,30,30)

#        obj.setEditorMode('axis',2)





    def myOnChanged(self,obj,prop):

        if prop in ["Shape","Label","A","B","_noExecute"]:
            return


        try: # start not befor the last prop is created
            obj.displayMode
        except:
            return

        if obj.mode=='Cylinder' and prop=='number':
            print ("Select precomputed Face",obj.number)
            optimizeCylinder(obj,False)
            return



        # print ("changed ",prop
        if obj.mode=='Cylinder':
            findCylinder(obj)
            optimizeCylinder(obj)


        elif obj.mode == 'Sphere':
            findSphere(obj)


    def myExecute(self,obj):
        print ("start onchange init")
        self.onChanged(obj,"_init_")
        print (obj.Label," executed")

def splitShapeCylinder(shape,center,axis,r0,tol=0.01):
#    print ("splitshape --------------------------------------------"
    syes=[]
    sno=[]
    edges={}
    for f in shape.Faces:
        ok=True
#        print f
        for v in f.Vertexes:
            p=v.Point
            dd=abs((p-center).cross(axis).Length-r0)
            if dd >tol:
                ok=False
                sno += [f]
                break
        if ok:
            syes += [f]

    for f in syes:
        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            if 1:
                #dd=abs((ps[0]-center).Length-radius)
                #dd2=abs((ps[-1]-center).Length-radius)
                dd=abs((ps[0]-center).cross(axis).Length-r0)
                dd2=abs((ps[-1]-center).cross(axis).Length-r0)

                if dd <tol and dd2 < tol:
                    try:
                        edges[tuple(tt)] +=1 
                    except:
                        edges[tuple(tt)] =1 



#    print ("Edges--------------",len(edges)
#    for e in edges:
#        print edges[e]
#        if edges[e] == 1:
#            print ("border",e



    # delete islands
    syes2=[]

    for f in syes:
#        print ("!!",f
        fok=False
        for e in f.Edges:
#            print e
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            try:
                if edges[tuple(tt)]!=1:
                    fok=True
            except:
                print ("--------------------------------outside A")
                pass
        if fok:
            syes2+=[f]
        else:
            print ("--------------------------ISLAND-B",f)
            sno += [f]


    #print"compare face normals-----------------------------------------"
    found=0
    syes3=[]
    for f in syes2:
    #    print ("Face ",f
        [a,b,c]=f.Vertexes
        t=(a.Point-b.Point).cross(a.Point-c.Point).normalize()
        ff=0
        for v in f.Vertexes:
            t1=((v.Point-center).cross(axis)).normalize().cross(axis).normalize()
    #        print t.dot(t1)
            if abs(t.dot(t1))>0.5:
                ff+=1
    #    print ff
        if ff==3:
            found +=1
            syes3 += [f]
        else:
            sno += [f]
    print ("face normal reduction found",found,len(syes2))

    return (syes3,sno)




def splitShapeSphere(shape,center,radius,tol=0.01):

    syes=[]
    sno=[]
    for f in shape.Faces:
        ok=True
        for v in f.Vertexes:
            p=v.Point
            dd=abs((p-center).Length-radius)
            #print dd
            if dd > tol:
                ok=False
                sno += [f]
                break
        if ok:
            syes += [f]

    return (syes,sno)

def splitShapePlane(shape,center,normal,tol=0.01):

    syes=[]
    sno=[]
    for f in shape.Faces:
        ok=True
        for v in f.Vertexes:
            p=v.Point
            dd=abs((p-center).dot(normal))
            if dd >tol:
                ok=False
                sno += [f]
                break
        if ok:
            syes += [f]

    return (syes,sno)

print ("HUHU")

def borderPlane(shape,center,normal,tol=0.01):

    debug=False
    if debug: print ("borderplane",center,normal)
    syes=[]
    sno=[]
    edges={}
    for f in shape.Faces:
        # ist flaeche daei
        ok=True
#        print f
        for v in f.Vertexes:
            p=v.Point
            dd=abs((p-center).dot(normal))
            if dd >tol:
                ok=False
                sno += [f]
                break
        if not ok:
            continue

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            if 1:
                #dd=abs((ps[0]-center).Length-radius)
                #dd2=abs((ps[-1]-center).Length-radius)
                dd=abs((ps[0]-center).dot(normal))
                dd2=abs((ps[-1]-center).dot(normal))
                if dd <tol and dd2 < tol:
                    try:
                        edges[tuple(tt)] +=1 
                    except:
                        edges[tuple(tt)] =1 
    if debug: 
        print ("border")
        anz=0
        for e in edges:
            if edges[e]==1:
                print (np.round(e,1))
                anz += 1
        print (len(edges),anz)

    borders=[]
    for f in shape.Faces:

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            try:
                if edges[tuple(tt)] == 1:
                    borders += [e]
            except:
                pass #kante nicht dabei

    return borders





def borderSphere(shape,center,radius,tol=0.01):

    debug=False
    if debug: print ("bordersphere",center,radius)
    syes=[]
    sno=[]
    edges={}
    for f in shape.Faces:
        # ist flaeche daei
        ok=True
#        print f
        for v in f.Vertexes:
            p=v.Point
            dd=abs((p-center).Length-radius)
            if dd >tol:
                ok=False
                sno += [f]
                break
        if not ok:
            continue

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            if 1:
                dd=abs((ps[0]-center).Length-radius)
                dd2=abs((ps[-1]-center).Length-radius)
                if dd <tol and dd2 < tol:
                    try:
                        edges[tuple(tt)] +=1 
                    except:
                        edges[tuple(tt)] =1 
    if debug: 
        print ("border")
        anz=0
        for e in edges:
            if edges[e]==1:
                print (np.round(e,1))
                anz += 1
        print (len(edges),anz)

    borders=[]
    for f in shape.Faces:

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            try:
                if edges[tuple(tt)] == 1:
                    borders += [e]
            except:
                pass #kante nicht dabei

    return borders


def borderCylinder(shape,center,axis,r0,tol=0.01):

    debug=False

    if debug: print ("bordersphere",center,axis,r0)
    syes=[]
    sno=[]
    edges={}
    for f in shape.Faces:
        # ist flaeche daei
        ok=True
#        print f
        for v in f.Vertexes:
            p=v.Point
            #dd=abs((p-center).Length-radius)
            dd=abs((p-center).cross(axis).Length-r0)
            if dd >tol:
                ok=False
                sno += [f]
                break
        if not ok:
            continue

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            if 1:
                #dd=abs((ps[0]-center).Length-radius)
                #dd2=abs((ps[-1]-center).Length-radius)
                dd=abs((ps[0]-center).cross(axis).Length-r0)
                dd2=abs((ps[-1]-center).cross(axis).Length-r0)
                if dd <tol and dd2 < tol:
                    try:
                        edges[tuple(tt)] +=1 
                    except:
                        edges[tuple(tt)] =1 
    if debug: 
        print ("border")
        anz=0
        for e in edges:
            if edges[e]==1:
                print (np.round(e,1))
                anz += 1
        print (len(edges),anz)

    borders=[]
    for f in shape.Faces:

        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            try:
                if edges[tuple(tt)] == 1:
                    borders += [e]
            except:
                pass #kante nicht dabei

    return borders


def borderCylinderV2(shyes):

    debug=False

#    syes=[]
#    sno=[]
    edges={}
    for f in shyes:
        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            try:
                edges[tuple(tt)] +=1 
            except:
                edges[tuple(tt)] =1 

    borders=[]

    for f in shyes:
        for e in f.Edges:
            ps=[e.Vertexes[0].Point,e.CenterOfMass,e.Vertexes[-1].Point]
            tt=np.array(ps).reshape(9)
            if edges[tuple(tt)] == 1 and e not in borders:
                borders += [e]

    return borders



def findCylinder(obj):
        '''find faces which belong to a cylider by selected faces'''
        print("START FINDCYLINDER-----------------------")
        aaat=time.time()

        debug=False
        debug=obj._debug
        maxradius=obj.Source.Shape.BoundBox.DiagonalLength*0.5
        maxradius=0
        
        
        pts=[]
        for (sob,fns) in obj.SourceFaces:
            for fn in fns:
                f=getattr(sob.Shape,fn)
                for v in f.Vertexes:
                    if not v.Point in pts:
                        pts += [v.Point]

        l=len(pts)
        if debug:
            print ("find cylinder points in use ",l)

        res=[]
        auxs=[]
        display=1
        for i in range(l-5):
            pts5=pts[i:i+5]
            (rc,aux)=.points_to_face.run_cylinder5p(pts5,display=display,pointsize=0,maxradius=maxradius)
            res += rc
#            print (rc)
#            print ("!!",rc[2]
#            if rc[2]<5000:
#            print aux
            auxs += aux

        ptsa=[v.Point for v in obj.Source.Shape.Vertexes]
        l=len(ptsa)

        best=-1
        bestanz=-1
        sols=[]
        App.res=res
        res2=[]
        for ri,r in enumerate(res):

            [center,axis,r0,l1,l2,i]=r
            center=center - center.dot(axis)*axis
            
            # ignoriere entfernte
            if center.Length>1000 or r0>1000:
                if debug:
                    print ("zu gross ---center.Length---radius ---",center.Length,r0)
                continue

            anz=0 
            anz2=0
            dsum=0
            dds=0
            ptsok=[]
            ptserr=[] 
            for p in ptsa:
                dd=abs((p-center).cross(axis).Length-r0)
                
                if dd >obj.tol:
                    anz2 += 1
                    ptserr += [p]
                else:
                    anz +=1
                    dds += dd
                    ptsok +=  [p]
                dsum += dd

            if anz>bestanz:
                bestanz=anz
                best=i

            if anz >10:
                print(ri,anz,np.round(center,2),np.round(axis,2),round(r0,2) )
            else:
                if debug:
                    print ("small solution, not used index,count faces",ri,anz)

#            res2 += [[center,axis,r0,anz,obj.tol,ptsok,ptsa]]

            [center,axis,r0,l1,l2,i]=r


            if 1 or anz>10:
                if debug:
                    print ("centre",np.round(center,2))
                    print ("radius",round(r0,2))
                    print ("axis",np.round(axis,2))
                aata=time.time()
                (shyes,shno)=splitShapeCylinder(obj.Source.Shape,center,axis,r0,obj.tol)
                
                if len(shyes)>2:
                    res2 += [[center,axis,r0,anz,obj.tol,ptsok,ptsa]]

                if debug:
                    print ("Time split Shape",round(time.time()-aata,3))

                borders=[Part.Shape()]
                if 1: #+# border is time consuming improive
                    aata=time.time()
                    #borders=borderCylinder(obj.Source.Shape,center,axis,r0,obj.tol)
                    borders=borderCylinderV2(shyes)
                    print ("TimeXXAATA border",time.time()-aata)

                sols +=[[shyes,shno,borders]]


        App.res2=res2
        besta=-1
        ymax=-1

        if debug:
            print ("found solutions id,good faces, left over faces")
        for j,s in enumerate(sols):
                [y,n,b]=s
                if len(y)>ymax:
                    ymax=len(y)
                    besta=j

                if debug:
                    print (j,len(y),len(n))

        s=sols[besta]
        [y,n,b]=s
        print ("best solution:",besta,len(y),len(n))
        [shyes,shno,borders]=s

        if 1:

                obj.ViewObject.DisplayMode = "Flat Lines"
                if obj.displayMode=='found':
                    obj.Shape=Part.Compound(shyes)
                elif obj.displayMode=='leftover':
                    if len(shno)>0:
                        obj.Shape=Part.Compound(shno)
                    else:
                        obj.Shape=Part.Shape()
                elif obj.displayMode=='borders':
                    obj.Shape=Part.Compound(borders) 
                elif obj.displayMode=='aux':
                    obj.Shape=Part.Compound(auxs)
                    obj.ViewObject.Transparency=90
                    obj.ViewObject.ShapeColor=(0.7,1.,1.)
                    obj.ViewObject.DisplayMode = "Shaded"


                if obj.A== None:
                    _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_found_")
                    groupit(_t)
                    obj.A=_t
                    obj.A.ViewObject.ShapeColor=(0.,0.,1.)
                    #obj.A.ViewObject.hide()

                obj.A.Shape=Part.Compound(shyes)
                obj.A.purgeTouched()

                if obj.B== None:
                    _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_leftover_")
                    groupit(_t)
                    obj.B=_t
                    obj.B.ViewObject.ShapeColor=(1.,0.,0.)
                    #obj.B.ViewObject.hide()

                if len(shno)>0:
                    obj.B.Shape=Part.Compound(shno)
                else:
                    obj.B.Shape=Part.Shape()
                obj.B.purgeTouched()

                obj.ViewObject.hide()

                print ("FINDCYLINDER done solution",ri)

        print ("findCylinder time",time.time()-aaat)


def ReconstructCylinder():
    '''ReconstructrFace Cylinder'''

    sel=Gui.Selection.getSelection()
    s=Gui.Selection.getSelectionEx()[0]
    assert(len(s.SubElementNames)>1)

    yy=App.ActiveDocument.addObject("Part::FeaturePython","ReconstructFace")
    print (yy)
    ReconstructFace(yy)
    yy._noExecute=True
    yy.mode='Cylinder'
    yy.displayMode='borders'
    #yy.displayMode='found'
    yy.Source=sel[0]
    yy.Source.ViewObject.hide()

    for n in s.SubElementNames:
        yy.SourceFaces +=[(s.Object,n)]

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineWidth=5
    yy.ViewObject.LineColor=(.9,.9,0.0)

    yy._noExecute=False
    print ("########################################")
    # findCylinder(yy)
    return yy

def ReconstructPlane():
    '''ReconstructrFace Plane'''

    sel=Gui.Selection.getSelection()
    s=Gui.Selection.getSelectionEx()[0]
    assert(len(s.SubElementNames)>0)

    yy=App.ActiveDocument.addObject("Part::FeaturePython","ReconstructFace")
    ReconstructFace(yy)
    yy._noExecute=True
    yy.mode='Plane'
    yy.displayMode='borders'
    yy.Source=sel[0]
    yy.Source.ViewObject.hide()

    for n in s.SubElementNames:
        yy.SourceFaces +=[(s.Object,n)]

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineWidth=5
    yy.ViewObject.LineColor=(.9,.9,0.0)

    yy._noExecute=False
    #findPlane(yy)
    return yy



def findSphere(obj):
    '''find faces which belong to a Sphere by selected faces'''

    pts=[]
    for (sob,fns) in obj.SourceFaces:
        for fn in fns:
            f=getattr(sob.Shape,fn)
            for v in f.Vertexes:
                if not v.Point in pts:
                    pts += [v.Point]

    l=len(pts)
    if obj._debug:
        print ("find Sphere points in use",l)

    res=[]
    if obj.displayMode=='aux':
        display=1
    else: 
        display=0
    for i in range(l-4):
        (pp,ra,aux)=.points_to_face.run_sphere4p(pts[i:i+4],display=display)
        res += [(pp,ra)]

    res=np.array(res).swapaxes(0,1)

    if obj._debug:
        print ("Radius: ",np.round(np.mean(res[1]),2))
        print ("Center: ",np.round(np.sum(res[0])/(l-4),2))

    radius = np.mean(res[1])
    center = np.sum(res[0])/(l-4)

    (shyes,shno)=splitShapeSphere(obj.Source.Shape,center,radius,obj.tol)
    borders=borderSphere(obj.Source.Shape,center,radius,obj.tol)

    obj.ViewObject.DisplayMode = "Flat Lines"
    if obj.displayMode=='found':
        obj.Shape=Part.Compound(shyes)
    elif obj.displayMode=='leftover':
        if len(shno)>0:
            obj.Shape=Part.Compound(shno)
        else:
            obj.Shape=Part.Shape()
    elif obj.displayMode=='borders':
        obj.Shape=Part.Compound(borders)
    elif obj.displayMode=='aux':
        obj.Shape=Part.Compound(aux)
        obj.ViewObject.Transparency=60
        obj.ViewObject.ShapeColor=(0.9,0.,0.)
        obj.ViewObject.DisplayMode = "Shaded"


    if obj.A== None:
        _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_found_")
        groupit(_t)
        obj.A=_t
        obj.A.ViewObject.ShapeColor=(0.,0.,1.)

    obj.A.Shape=Part.Compound(shyes)
    obj.A.purgeTouched()

    if obj.B== None:
        _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_leftover_")
        groupit(_t)
        obj.B=_t
        obj.B.ViewObject.ShapeColor=(1.,0.,0.)

    if len(shno)>0:
        obj.B.Shape=Part.Compound(shno)
    else:
        obj.B.Shape=Part.Shape()
    obj.B.purgeTouched()


def findPlane(obj):
    '''find faces which belong to a Plane by selected faces'''

    obj._debug=True
    pts=[]
    for (sob,fns) in obj.SourceFaces:
        for fn in fns:
            f=getattr(sob.Shape,fn)
            for v in f.Vertexes:
                if not v.Point in pts:
                    pts += [v.Point]

    l=len(pts)
    if obj._debug:
        print ("find Sphere points in use",l)

    res=[]
    if obj.displayMode=='aux':
        display=1
    else: 
        display=0

    auxs=[]
    for i in range(l-2):
        (center,normal,aux)=.points_to_face.run_plane3p(pts[i:i+3],display=display)
        res += [(center,normal)]
        auxs += [aux]

#    res=np.array(res).swapaxes(0,1)

#    if obj._debug:
#        print ("Center: ",np.round(np.mean(res[0]),2)
#        print ("Normal: ",np.round(np.mean(res[1]),2)

    center=res[0][0]
    normal=res[0][1]

    if obj._debug:
        print ("Center: ",np.round(center,2))
        print ("Normal: ",np.round(normal,2))

    print( auxs)

    shyes=shno=[]
    borders=auxs
    shyes=auxs
    shno=auxs
    
    (shyes,shno)=splitShapePlane(obj.Source.Shape,center,normal,obj.tol)
    borders=borderPlane(obj.Source.Shape,center,normal,obj.tol)

    obj.ViewObject.DisplayMode = "Flat Lines"
    if obj.displayMode=='found':
        obj.Shape=Part.Compound(shyes)
    elif obj.displayMode=='leftover':
        if len(shno)>0:
            obj.Shape=Part.Compound(shno)
        else:
            obj.Shape=Part.Shape()
    elif obj.displayMode=='borders':
        obj.Shape=Part.Compound(borders)
    elif obj.displayMode=='aux':
        obj.Shape=Part.Compound(aux)
        obj.ViewObject.Transparency=60
        obj.ViewObject.ShapeColor=(0.9,0.,0.)
        obj.ViewObject.DisplayMode = "Shaded"


    if obj.A== None:
        _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_found_")
        groupit(_t)
        obj.A=_t
        obj.A.ViewObject.ShapeColor=(0.,0.,1.)

    obj.A.Shape=Part.Compound(shyes)
    obj.A.purgeTouched()

    if obj.B== None:
        _t=App.ActiveDocument.addObject("Part::Feature",obj.Name+"_leftover_")
        groupit(_t)
        obj.B=_t
        obj.B.ViewObject.ShapeColor=(1.,0.,0.)

    if len(shno)>0:
        obj.B.Shape=Part.Compound(shno)
    else:
        obj.B.Shape=Part.Shape()
    obj.B.purgeTouched()




def ReconstructSphere():
    '''Reconstruct Face Sphere select 2 faces/triangles '''

    sel=Gui.Selection.getSelection()
    s=Gui.Selection.getSelectionEx()[0]
    assert (len(s.SubElementNames)>1)

    yy=App.ActiveDocument.addObject("Part::FeaturePython","ReconstructFace")
    ReconstructFace(yy)
    yy._noExecute=True
    yy.mode='Sphere'
    yy.displayMode='borders'
    yy.Source=sel[0]
    yy.Source.ViewObject.hide()

    for n in s.SubElementNames:
        yy.SourceFaces +=[(s.Object,n)]

    ViewProvider(yy.ViewObject)
    yy.ViewObject.ShapeColor=(.9,.0,0.)
    yy.ViewObject.LineWidth=5
    yy.ViewObject.LineColor=(.9,.9,0.0)

    yy._noExecute=False
    findSphere(yy)
    return yy




def noisymesh():
    '''add some noise to a mesh and create a part of it'''

    import Mesh
    mesh=Gui.Selection.getSelection()[0]
    k=1.0 # noise factor in mm

    m=mesh.Mesh
    [ps,ts]=m.Topology
    ps2=[p+App.Vector(random.random(),random.random(),random.random())*k - App.Vector(1,1,1)*0.5*k for p in ps]
    m2=Mesh.Mesh((ps2,ts))

    tt=App.ActiveDocument.addObject("Part::Feature","M2")
    __shape__=Part.Shape()
    __shape__.makeShapeFromMesh(m2.Topology,0.100000)
    tt.Shape=__shape__
    tt.purgeTouched()


def findCluster():
    '''build groups of cylinders'''

    def dist(r,r2):

        [ce,ax,ra]=r[0:3]
        [ce2,ax2,ra2]=r2[0:3]

        dr=(ra/ra2+ra2/ra)*0.5 - 1
    #    print dr
        da=1- abs(ax.dot(ax2)) 
    #    print da
        
        try:
            dc=(ce-ce2).normalize().dot((ax+ax2)*0.5)
        except:
            dc=1
        dc=(ce-ce2).Length/(ce.Length+ce2.Length)
    #    print dc
        return (dr+da+dc,dr,da,dc)


    res=App.res2
    cr=len(res)

    cluster={}

    for i in range(cr):
        for j in range(cr):
    #        if i==j:
    #            continue
            r=res[i]
            r2=res[j]
            a=np.round(dist(r,r2),2)
            if a[0]<0.2:
                ran=min(r[3],r2[3])
                v=round(a[0]/ran*100000,2)
                if i<j:
                    print (i,j,v,a,r[3],r2[3])
                try:
                    cluster[i] += [j]
                except:
                    cluster[i] = [j]


    cluster2=[]
    for i in cluster:
#        print cluster[i]
        #if cluster[i] not in cluster2 and len(cluster[i])>1:
        if cluster[i] not in cluster2 :
            cluster2 += [cluster[i]]

    print ("cluster2")
    print (cluster2)
    # Berechne Mittelwerte
    for cl in cluster2:
        ces=App.Vector()
        axs=App.Vector()
        ras=0
        cll=len(cl)
        sanz=0
        for i in cl:
            [ce,ax,ra,anz]=res[i][0:4]
            ces += ce 
            axs += ax
            ras += ra
            sanz += anz
        ces /= cll
        axs=axs.normalize()
        ras /= cll
        sanz /= cll
        print (np.round(ces,2), np.round(axs,2),np.round(ras),sanz)

def AA():
    findCluster()



class MultiShape(FeaturePython):
    '''object with mutltiple shape to switch'''

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)

        obj.ViewObject.ShapeColor=(1.0,0.0,0.0)
        self.Shapes=[]
        obj.addProperty("App::PropertyInteger","number").number=0


    def myOnChanged(self,obj,prop):

        if prop in ["Shape","Label","_noExecute"]:
            return
        try: 
            obj.number
        except:
            return

        if len(self.Shapes)==0:
            return
        n=obj.number % len(self.Shapes)
        if n!=obj.number:
            obj.number=n
        obj.Shape=self.Shapes[n]



def optimizeCylinder(obj=None,needRecompute=True):

    aatt=time.time()

    debug=obj._debug

    if obj == None:
        raiseException("not implemented")
        ms=App.ActiveDocument.addObject("Part::FeaturePython","MS")
        MultiShape(ms)
        ViewProvider(ms.ViewObject) 
        shape=App.ActiveDocument.M2.Shape

    else:
        ms=obj.A
        shape=obj.Source.Shape

    if needRecompute:
        obj.Proxy.Shapes=[]
        obj.Proxy.ShapesNo=[]
        obj.Proxy.Borders=[]

        for solnr in range(len(App.res2)):
            [ce,ax,r,anz,tol,pts,ptsa]=App.res2[solnr]

            if 1 or debug:
                print ("Center",np.round(ce,2),"Radius",round(r,2))


            def modCe(ce,ax,r,pts):
                ''' optimize center'''

                fs=App.Vector()
                dr=0
                for p in pts:
                    k=(p-ce).cross(ax)
                    kn=App.Vector(k).normalize()
                    f=k -kn*r
                    dr += k.Length
                    fs+=f
                fs /= len(pts)
                fg= fs.cross(ax)
            #    print ("Force ",fs
            #    print ("Force ",fs.Length
            #    print ("DR ",dr,dr/len(pts))

                r2=dr/len(pts)
                return ce-fg,fg.Length


            if 0: # change the center
                print ("constant radius ->center force",np.round(ce,2))
                for i in range(10):
                    (ce2,f)=modCe(ce,ax,r,pts)
#                    print (i,np.round(ce2,2),round(f,2))
                    ce=ce2

            rmin=r
            fmin=10**10

            if 10:
                #print ("###fimnde besten radius#####llll#######################"
                for i in range(-20,20):
                    #print (i,"Radius",r+i)
                    (ce2,f)=modCe(ce,ax,r+i*0.1,pts)
                    if f<fmin:
                        fmin=f
                        rmin=r+i*0.1
                        cemin=ce2
                    # print (round(r+i,2),np.round(ce2,2),round(f,2))
                    # ce=ce2

            ce=cemin
            r=rmin

            if debug:
                print ("rmin,cmin",round(rmin,2),np.round(cemin,2))

            for i in range(10):
                (ce2,f)=modCe(ce,ax,r,pts)
                ce=ce2

            print ("solution",solnr,np.round(ce2,2),round(r,2),"force",round(f,4))

            anz=0
            ptsok=[]
            tolvs=[]

            for p in ptsa:
                dd=abs((p-ce).cross(ax).Length-r)
                if dd<2*tol:
                    tolvs += [dd]
                
                if dd < tol:
                    anz +=1
                    ptsok +=  [p]

            if debug:
                print ("Points in tol",anz,len(pts),len(ptsa))

            (shyes,shno)=splitShapeCylinder(shape,ce,ax,r,tol)
            borders=borderCylinderV2(shyes)
            
            print ("found and leftover faces for solution",solnr,len(shyes),len(shno))

            if debug:
                print("tol",tol,"Facesok",len(shyes))

            if len(shyes)>=0:
                obj.Proxy.Shapes  += [Part.Compound(shyes)]
            else:
                obj.Proxy.Shapes  += [ Part.makeSphere(10)]
            if len(shno)>=0:
                obj.Proxy.ShapesNo  += [Part.Compound(shno)]
            else:
                obj.Proxy.ShapesNo  += [ Part.makeSphere(10)]
            if len(borders)>=0:
                obj.Proxy.Borders += [Part.Compound(borders)]
            else:
                obj.Proxy.Borders += [Part.makeSphere(10)]
            if 0:
                n, bins, patches = plt.hist(tolvs,bins=int(round(tol*20)))
                plt.grid(True)
                plt.show()

    n=obj.number % len(obj.Proxy.Shapes)
    if n!=obj.number:
        obj.number=n

    print ("Display Solution",n)
    ms.Shape=obj.Proxy.Shapes[n]
    ms.purgeTouched()
    obj.B.Shape=obj.Proxy.ShapesNo[n]
    obj.B.purgeTouched()
    if obj.displayMode=='borders':
        obj.Shape=obj.Proxy.Borders[n]
    print ("Time optimize",round(time.time()-aatt,3))


def setSelection(obj,subels):
    '''set the selection subelements'''
    Gui.Selection.clearSelection()
    for f in subels:
        Gui.Selection.addSelection(obj,f)


import cProfile

def AA():
    '''testcase'''

    setSelection(App.ActiveDocument.M2,['Face560','Face628','Face623'])
    setSelection(App.ActiveDocument.M2,['Face560','Face628'])
    # cProfile.run(".points_to_face.ReconstructCylinder()")
    ReconstructCylinder()



'''
Idee fuer zurechtschneiden
f=App.ActiveDocument.Wire.Shape.Face1
e=App.ActiveDocument.Circle.Shape.Edge1
e=App.ActiveDocument.Wire001.Shape.Edge1
e2=App.ActiveDocument.Wire001.Shape.Edge2

e3=App.ActiveDocument.Wire002.Shape.Edge1
e4=App.ActiveDocument.Wire002.Shape.Edge2

yy=Part.makesplitShapeCylinder(f,[(e,f),(e2,f),(e3,f),(e4,f)])
for y in yy:
    Part.show(y[0])
'''
