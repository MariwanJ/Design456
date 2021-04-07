# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- scan cut --- shoe last - get cut wires from a scan
#--
#-- microelly 2017v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
import FreeCAD as App
import FreeCADGui as Gui
import Points,Part,Draft
import numpy as np
import random
import scipy as sp
from scipy import signal

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


def run1(z0,mesh,plane,showpointsmap=True,showmedianfilter=True):
    print ("run1 ",z0)

    color=(random.random(),random.random(),random.random())

    
    pl=plane.Placement
    plst=" Base:" + str(pl.Base) +" Rot Euler:" + str(pl.Rotation.toEuler())
    plinv=pl.inverse()

    #stl=App.ActiveDocument.LastDIA.Mesh
    stl=mesh
    pts=stl.Topology[0]


    pts2=[plinv.multVec(p) for p in pts]
    #pts2=[App.Vector(round(p.x),round(p.y),round(p.z)) for p in pts2]

    zmax=0.5
    zmin=-zmax

    #pts2a=[App.Vector(p.x,p.y,0) for p in pts2 if zmin<=p.z and p.z<=zmax]

    pts2a=[App.Vector(round(p.x),round(p.y),round(p.z)) for p in pts2 if round(p.z)==z0]
    
    if len(pts2a)==0: return

    p2=Points.Points(pts2a)
    if showpointsmap:
        Points.show(p2)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
        App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
        App.ActiveDocument.ActiveObject.Label="Points Map xy " +plst



    # create a wire from a central projection
    (px,py,pz)=np.array(pts2a).swapaxes(0,1)
    mymean=App.Vector(px.mean(),py.mean(),pz.mean())
    aps={}
    for v in pts2a:
        vm=v-mymean
    #    print np.arctan2(vm.x,vm.y)
        aps[np.arctan2(vm.x,vm.y)]=v

    kaps=aps.keys()
    kaps.sort()
    ptss=[aps[k] for k in kaps]
    print ("lens ",len(ptss),len(pts2a))

    l4=ptss

    # window size for smoothing
    f=5
    path=np.array([l4[0]] * f + l4 + [l4[-1]]*f)
    tt=path.swapaxes(0,1)
    y1 = sp.signal.medfilt(tt[1],f)
    y0 = sp.signal.medfilt(tt[0],f)
    #l5=[App.Vector(p) for p in np.array([tt[0],y1,tt[2]]).swapaxes(0,1)] 
    l5=[App.Vector(p) for p in np.array([y0,y1,tt[2]]).swapaxes(0,1)] 

    if 0 and showmedianfilter:
        Draft.makeWire(l5)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
        App.ActiveDocument.ActiveObject.Label="Median filter " + str(f)  + " " + plst


    # place the wire back into the shoe
    if 0:
        invmin=[pl.multVec(p) for p in l5]
        Draft.makeWire(invmin)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
        App.ActiveDocument.ActiveObject.Label="Wire "+ plst
    if 0:
        # diusplay the used points inside the shoe
        sels=[pl.multVec(p) for p in pts2a]
        s2=Points.Points(sels)
        Points.show(s2)
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
        App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
        App.ActiveDocument.ActiveObject.Label="Points " +plst



def run():

#    if len( Gui.Selection.getSelection())==0:
#        showdialog('Oops','nothing selected - nothing to do for me','Plese select a Draft Wire or a Draft BSpline')

    #default parameters
    p={
        "showmedianfilter":[False,'Boolean'],
        "showpointsmap":[False,'Boolean'],
    }

    # parameter -----------------
    t=App.ParamGet('User parameter:Plugins/nurbs/'+'scancut')
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


    try:
        plane=App.ActiveDocument.Plane
        mesh=App.ActiveDocument.LastDIA.Mesh
    except:
        sayexc(title='Error',mess='something wrong with the mesh and the helper plane ' )
        return

    for z0 in range(0,3):
        pass

    for z0 in range(-15,10):
        #run1(10*z0,mesh,plane,p['showpointsmap'],p['showmedianfilter'])
        run1(10*z0,mesh,plane,True,True)

if __name__ == '__main__':
    run()
