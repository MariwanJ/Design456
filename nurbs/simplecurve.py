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
#-- convert a draft wire to a sketcher bspline
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import random
import Draft,Part

import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from scipy.signal import argrelextrema
import os

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
#import matplotlib.pyplot as plt

from PySide import QtGui
import sys,traceback,random


def showdialog(title="Fehler",text="Schau in den ReportView fuer mehr Details",detail=None):
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(title)
    if detail!=None:   msg.setDetailedText(detail)
    msg.exec_()


def sayexc(title='Fehler',mess=''):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
    lls=eval(ttt)
    l=len(lls)
    l2=lls[(l-3):]
    App.Console.PrintError(mess + "\n" +"-->  ".join(l2))
    showdialog(title,text=mess,detail="--> ".join(l2))


def simplecurve(wire,ct=20,plotit=False,offset=0,debug=False):

    try:
        pts=wire.Points
    except:
        bc=wire.Shape.Edge1.Curve
        pts=bc.discretize(20)

    for kshift in [0,1,2,4]:
        pts=pts[kshift:]+pts[:kshift]


        off=App.Vector(0,0,offset)




        bc=Part.BSplineCurve()
        bc.approximate(pts,DegMax=3,Tolerance=0.5)
        bc.setPeriodic()
        sc=bc.toShape()
        print ("--------",ct,len(bc.getPoles()))

        if debug:
            sp=App.ActiveDocument.addObject("Part::Spline","approx Spline")
            sp.Shape=sc
        App.sc=sc
        App.bc=bc
        
        # calculate the interpolation points
        x=np.array(range(ct+1))
        vps=np.array([bc.value(1.0/ct*i)+off for i in x])
    #    y=np.array([sc.curvatureAt(1.0/ct*i) for i in x])

        y=[]
        for i in x:
            jj=1.0/ct*i
            v2=(bc.centerOfCurvature(jj)-bc.value(jj))
            v1=App.sc.tangentAt(jj)
            v=v1.cross(v2)
            if v.z>0: ff=1 
            else: ff=-1
            y.append(ff*sc.curvatureAt(jj))

        y=np.array(y)


        # find extrema for the poles
        z=argrelextrema(y, np.greater)
        z2=argrelextrema(y, np.less)
        z=z[0]
        z2=z2[0]

        mm=y[z]
        mm2=y[z2]

#        print z
#        print z2

        zc=np.concatenate([z,z2,[0,ct]])
        zc.sort()
        
    #
    #   hier feinheiten regeln 
    #

        th=0.013
        th=0.01

    #
    # kleine aenderungen ueberspringen
    #
        if th!=0:
            nn=[zc[0]]
            #for v in zc[1:-2]:
            for v in range(len(zc)-2):
#                print v
                if  abs(y[zc[v]]-y[zc[v+1]])<th and  abs(y[zc[v+1]]-y[zc[v+2]])<th:
#                    print ("skip ",v
                    pass
                else: nn.append(zc[v+1])
            nn.append(zc[-1])
        else: nn=zc

        mm3=y[nn]
        
        exps=vps[nn]


        #plotit=False
        if plotit: # display for debugging
            plt.plot(x,y, 'r-')

            plt.plot(z,mm,'bx')
            plt.plot(z2,mm2,'gx')
            plt.plot(nn,mm3,"ro")
            plt.show()

        print ("Approx !! points: ",len(nn))
        #return

    #    exps=vps[zc]


        ps=[tuple(p) for p in exps]



    #    Draft.makeBSpline(ps,closed=True,face=False)
    #
    #    App.ActiveDocument.ActiveObject.Label="simple " +str(ct) 
    #    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
    #    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.0,1.0,0.0)
    #    App.ActiveDocument.ActiveObject.ViewObject.LineWidth=6
    #    App.ActiveDocument.recompute()
    #    App.ActiveDocument.recompute()

    #    if debug:
    #        sh=App.ActiveDocument.ActiveObject.Shape.Edge1.Curve.toShape()
    #        sp=App.ActiveDocument.addObject("Part::Spline","simple Spline")
    #        sp.Shape=sh
    #
    #    if debug:
            #sh=App.ActiveDocument.ActiveObject.Shape.Edge1.Curve.toShape()
            
        bc=Part.BSplineCurve()
        bc.setPeriodic()
        bc.interpolate(ps)

        #    Draft.makeWire(ps,closed=True,face=False)

        bc.setPeriodic()
        sh=bc.toShape()
        
        sp=App.ActiveDocument.addObject("Part::Spline","Spline " +str(ct))
        sp.Label=wire.Label
        sp.Shape=sh




    #    zc=np.concatenate([z,z2,[0,ct]])
        zc=np.concatenate([z,[0,ct]])

        zc.sort()
        exps=vps[zc]

        ps=[tuple(p) for p in exps]

    #    Draft.makeBSpline(ps,closed=True,face=False)
    #
    #    App.ActiveDocument.ActiveObject.Label="simpleMax " +str(ct) 
    #    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
    #    App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.0,1.0,0.0)
    #    App.ActiveDocument.ActiveObject.ViewObject.LineWidth=6
    #    App.ActiveDocument.recompute()
    #    App.ActiveDocument.recompute()
    #



    #    if debug:
            #sh=App.ActiveDocument.ActiveObject.Shape.Edge1.Curve.toShape()
            
        bc=Part.BSplineCurve()
        bc.setPeriodic()
        bc.interpolate(ps)
        bc.setPeriodic()
        sh=bc.toShape()

        if 0:
            sp=App.ActiveDocument.addObject("Part::Spline","Max Spline " + str(ct))
            sp.Shape=sh


        Gui.updateGui()



def ThousandsOfRunWhatShouldIdo():

    if len( Gui.Selection.getSelectionEx())==0:
        showdialog('Oops','nothing selected - nothing to do for me','Plese select a Draft Wire or a Draft BSpline')

    for obj in Gui.Selection.getSelectionEx():

        #default parameters
        p={
            "splitcount":[10,'Integer'],
            "splits":['6,10,20','String'],
            "showplot":[False,'Boolean'],
            "test":[False,'Boolean'],
            "debug":[False,'Boolean'],
        }

        # parameter -----------------
        t=App.ParamGet('User parameter:Plugins/nurbs/'+'simplecurve')
        l=t.GetContents()
        if l==None: l=[]
        for k in l: p[k[1]]=k[2]
        for k in p:
            if p[k].__class__.__name__=='list':
                typ=p[k][1]
                if typ=='Integer':t.SetInt(k,p[k][0]);
                if typ=='Boolean':t.SetBool(k,p[k][0])
                if typ=='String':t.SetString(k,p[k][0])
                if typ=='Float':t.SetFloat(k,p[k][0])
                p[k]=p[k][0]
        #--------------------

        ct=p["splitcount"]
        splits=eval(p["splits"])
        plotit=p["showplot"]


        plotit=True
        
        print (ct,splits,plotit)
        splits=[8,16,32,64]
        splits=[20]
        for s in splits:
            #simplecurve(obj,s,plotit,offset=0,debug=p['debug'])
            simplecurve(obj,s,plotit,offset=0,debug=False)
