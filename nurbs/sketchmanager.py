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

''' save sketches into a sketch lib, load sketches into models ''' 
from say import *

import Design456Init

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
import pyob

import time
import glob

import FreeCAD as App
import FreeCADGui as Gui
import PySide
from PySide import  QtGui,QtCore



def getNamedConstraint(sketch,name):
    '''get the index of a constraint name'''
    for i,c in enumerate (sketch.Constraints):
        if c.Name==name: return i
    print ('Constraint name "'+name+'" not in ' +sketch.Label)
    raise Exception ('Constraint name "'+name+'" not in ' + sketch.Label)


def run(w):
    print ("I'm run")
    print (w)
    print (w.obj)
    print ("-------------")
    App.oo=w.obj
    sk=w.obj.Object #.Object
    print (sk.Label)
    print (sk.Name)

def hideAllConstraints(w,show=False):
    App.wob=w.obj
    sk=w.obj.Object
    c=sk.Constraints
    for i in range(len(c)):
        sk.setVirtualSpace(i, not show)

def showEndPoints(w,show=False):
    sk=w.obj.Object
    cs=[getNamedConstraint(sk,l) for l in ['p_0_x','p_0_y','p_1_x','p_1_y']]
    for i in cs:
        sk.setVirtualSpace(i, not show)

def showArcs(w,show=False):
    sk=w.obj.Object
    for l in ['tangent_AB','tangent_BC','tangent_CD']:
        try:
            cs=getNamedConstraint(sk,l) 
            sk.setVirtualSpace(cs, not show)
        except: pass


def setEndpoints(w,show=None):
    sk=w.obj.Object

    for i in [13,14,15,16,22]:
        sk.toggleDriving(i)

    posa=App.Vector(-250000,40000,0)
    posb=App.Vector(800000,50000,0)
    l=(posa-posb).Length
    #posa
    sk.setDatum(13,posa.x)
    sk.setDatum(14,posa.y)
    #posb
    sk.setDatum(15,posb.x)
    sk.setDatum(16,posb.y)
    # laenge tangentialabsc.
    sk.setDatum(19,0.3*l)
    sk.setDatum(20,0.3*l)
    sk.setDatum(22,posb.x-0.1*l)
    #sk.setDatum(11,0.3*l)

    sk.setDatum(17,0.04*l)
    sk.setDatum(18,0.02*l)

    for i in [13,14,15,16,22]:
        sk.toggleDriving(i)


def lockEndpoints(w,mode=0):
    sk=w.obj.Object
    if mode==1:
        print ("toggle 1")
        sk.toggleDriving(13)
        sk.toggleDriving(14)
    if mode==2:
        print ("toggle 2")
        sk.toggleDriving(15)
        sk.toggleDriving(16)
    sk.solve()







import Sketcher
def runSelection(w,mode=None):
        sk=w.obj.Object
        s=Gui.Selection.getSelectionEx()[0]
        for el in s.SubElementNames:
            el=int(el.replace("Edge",""))
            try:
                cs=getNamedConstraint(sk,'block edge ' + str(el)) 
                sk.delConstraint(cs)
            except:
                c=sk.addConstraint(Sketcher.Constraint('Block',el-1)) 
                sk.renameConstraint(c, u'block edge ' + str(el) )
                if sk.solve()!=0:
                    print ("kann block nicht ausfuehren")
                    sk.delConstraint(c)
                    sk.solve()


def dialog(obj):

    w=QtGui.QWidget()
    w.obj=obj

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    w.l=QtGui.QLabel("Sketcher Dialog Extension" )
    box.addWidget(w.l)

    w.r=QtGui.QPushButton("run")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :run(w))

    w.r=QtGui.QPushButton("hide All Constraints")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :hideAllConstraints(w,False))

    w.r=QtGui.QPushButton("show All Constraints")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :hideAllConstraints(w,True))

    w.r=QtGui.QPushButton("show Endpoint coordinates")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :showEndPoints(w,True))

    w.r=QtGui.QPushButton("hide Endpoint coordinates")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :showEndPoints(w,False))

    w.r=QtGui.QPushButton("show Arc dimensions")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :showArcs(w,True))

    w.r=QtGui.QPushButton("hide Arc dimensions")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :showArcs(w,False))

    w.r=QtGui.QPushButton("block or unblock selections")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :runSelection(w,None))


    w.r=QtGui.QPushButton("set endpoints")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :setEndpoints(w,None))

    w.r=QtGui.QPushButton("toggle startpoint")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :lockEndpoints(w,1))

    w.r=QtGui.QPushButton("toggle endpoint")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :lockEndpoints(w,2))



    w=ComboViewShowWidget(w)

    box.addItem(QtGui.QSpacerItem(
            10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))


    return w

#--------------


def getMainWindow():
    '''returns the main window'''
    toplevel = QtGui.qApp.topLevelWidgets()
    for i in toplevel:
        if i.metaObject().className() == "Gui::MainWindow":
            return i
    raise Exception("No main window found")


def getComboView(mw):
    '''returns the Combo View widget'''
    dw = mw.findChildren(QtGui.QDockWidget)
    for i in dw:
        if str(i.objectName()) == "Combo View":
            return i.findChild(QtGui.QTabWidget)
        elif str(i.objectName()) == "Python Console":
            return i.findChild(QtGui.QTabWidget)
    raise Exception("No tab widget found")


def ComboViewShowWidget(widget, tabMode=True):
    '''create a tab widget inside the combo view'''

    widget.tabname="Transportation Sketcher"
    # stop to default
    if not tabMode:
        widget.show()
        return widget

    mw = getMainWindow()
    tab = getComboView(mw)

    c = tab.count()

    # clear the combo  window
    for i in range(c - 1, 1, -1):
        tab.removeTab(i)

    # start the requested tab
    tab.addTab(widget, widget.tabname)
    tab.setCurrentIndex(2)

    print ("ComboViewShowWidget done.")
    widget.tab = tab
    return widget





#-------------











#\cond
class _ViewProvider(pyob.ViewProvider):
    ''' base class view provider '''

    def __init__(self, vobj):
        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        return Design456Init.NURBS_ICON_PATH+'sketchdriver.svg'

    def setupContextMenu(self, obj, menu):
        menu.clear()
        action = menu.addAction("MyMethod #1")
        action.triggered.connect(lambda:self.methodA(obj.Object))
        action = menu.addAction("MyMethod #2")
        menu.addSeparator()
        action.triggered.connect(lambda:self.methodB(obj.Object))
        action = menu.addAction("Edit Sketch")
        action.triggered.connect(lambda:self.myedit(obj.Object))


    def myedit(self,obj):
        self.methodB(None)
        App.oo2=obj
        self.Object=obj
        Gui.activeDocument().setEdit(obj.Name)
        self.methodA(None)

    def methodA(self,obj):
#        print ("my Method A Finisher")
#        Gui.activateWorkbench("DraftWorkbench")
        App.ActiveDocument.recompute()

    def methodB(self,obj):
        print ("my method B Starter")
        # test starting an extra dialog
        App.d=dialog(self)
        App.d.show()
        App.ActiveDocument.recompute()

    def methodC(self,obj):
        print ("my method C After Edit finished")
        Gui.activateWorkbench("NurbsWorkbench")
        print ("kl")
#        App.d.hide()
#        App.d.deleteLater()
        print ("ha")
        App.ActiveDocument.recompute()
        print ("hu")
        mw = getMainWindow()
        tab = getComboView(mw)
        c = tab.count()
        print ("count ",c)
        c = tab.count()

        # clear the combo  window
        for i in range(c - 1, 1, -1):
            tab.removeTab(i)



        tab.setCurrentIndex(0)
        tab.setCurrentIndex(0)
        print ("set tab domne")



    def unsetEdit(self,vobj,mode=0):
        self.methodC(None)


    def doubleClicked(self,vobj):
        print ("double clicked")
        self.myedit(vobj.Object)
        print ("Ende double clicked")



#\endcond


def copySketch(sketch,name):
    '''kopiert sketch in sketchobjectpython'''
    sb=sketch
    gs=sb.Geometry
    cs=sb.Constraints

    sk=App.ActiveDocument.addObject('Sketcher::SketchObjectPython',name)
    _ViewProvider(sk.ViewObject)

    for g in gs:
        rc=sk.addGeometry(g)
        sk.setConstruction(rc,g.Construction)
    #    sk.solve()

    for c in cs:
        rc=sk.addConstraint(c)
    #    sk.solve()

    sk.solve()
    sk.recompute()
    App.ActiveDocument.recompute()


def replaceSketch(sketch,name):
    '''kopiert sketch in sketchobjectpython'''
    sb=sketch
    gs=sb.Geometry
    cs=sb.Constraints

    sk=App.ActiveDocument.getObject(name)
    if sk == None or name=='ufo':
        sk=App.ActiveDocument.addObject('Sketcher::SketchObjectPython',name)
        _ViewProvider(sk.ViewObject)
    rr=range(len(sk.Geometry))
    rr.reverse()

    sk.deleteAllGeometry()

    for g in gs:
#        print (g)
        rc=sk.addGeometry(g)
        sk.setConstruction(rc,g.Construction)

#    print ("Constraints ...")
    for c in cs:
#        print (c)
        rc=sk.addConstraint(c)

    sk.solve()
    sk.recompute()
    App.ActiveDocument.recompute()
    return sk




def loadSketch(fn,sourcename='Sketch',targetname='Sketch'):
    '''load sketch from file into sketcher object with name'''

    ad=App.ActiveDocument
    if ad==None:
        ad=App.newDocument("Unnamed")

    rc=App.open(fn)
    print ("read ",fn)
    print ("active document",ad,ad.Label,ad.Name)

    for obj in rc.Objects:
        print (obj.Name,obj.Label,obj.ViewObject.Visibility)
        if obj.ViewObject.Visibility:
            print ("found")
            sb=obj
            break

    #sb=rc.getObject(sourcename)
    assert sb is not None


    # App.setActiveDocument(ad.Label)
    App.setActiveDocument(ad.Name)
    App.ActiveDocument=ad

    sk=replaceSketch(sb,targetname)
    
    sk.Label="Copy of "+sourcename+"@"+fn
    App.closeDocument(rc.Label)





def getfiles():
    '''list sketcher files library''' 
    files=glob.glob(App.ConfigGet("UserAppData") +'sketchlib/'+'*_sk.fcstd')
    files.sort()
    return files



def saveSketch(w=None):
    '''save Gui.Selection  sketch into a file inside the sketch lib directory'''

    sel=Gui.Selection.getSelection()[0]
    fn=App.ConfigGet("UserAppData") +'sketchlib/'+sel.Name+"_"+str(int(round(time.time())))+"_sk.fcstd"
    nd=App.newDocument("XYZ")
    App.ActiveDocument=nd
    copySketch(sel,"Sketch")
    print (sel.Label+" - speichere als " + fn)
    App.ActiveDocument.saveAs(fn)
    App.closeDocument("XYZ")



#\cond
def srun(w):
    a=w.target
    lm=getfiles()

    model=lm[w.m.currentIndex()]

    sketchmanager
    #reload(.sketchmanager)

    target='ufo'

    s=Gui.Selection.getSelection()
    if s != []: 
        target=s[0].Name
    print ("target is: ",target)

    cmd=".sketchmanager.loadSketch('" + model +"','Sketch',target)"
    print ("Run command:",cmd)
    eval(cmd)
    Gui.SendMsgToActiveView("ViewFit")
    w.hide()
    w.deleteLater()
#\endcond


def MyLoadDialog(target=None):
    '''widget for load sketch from file into a sketch object''' 

    lm=getfiles()
    w=QtGui.QWidget()
    w.target=target

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    l=QtGui.QLabel("Select the model" )
    box.addWidget(l)

    combo = QtGui.QComboBox()
    for item in lm:
        combo.addItem(str(item))
    w.m=combo
    combo.activated.connect(lambda:srun(w))  
    box.addWidget(combo)

#    w.r=QtGui.QPushButton("save selected sketch as file")
#    box.addWidget(w.r)
#    w.r.pressed.connect(lambda :saveSketch(w))

    w.show()
    return w


# hier names dialog einbauen
def MySaveDialog(target=None):
    '''widget for save sketch into a file''' 

    lm=getfiles()
    w=QtGui.QWidget()
    w.target=target

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


    w.r=QtGui.QPushButton("save selected sketch as file")
    box.addWidget(w.r)
    w.r.pressed.connect(lambda :saveSketch(w))

    w.show()
    return w




def runLoadSketch():
    '''method called from Gui menu'''
    #[target]=FreeCADGui.Selection.getSelection()
    target=None
    return MyLoadDialog(target)

def runSaveSketch():
    '''method saveSketch called from Gui menu'''
    #[target]=FreeCADGui.Selection.getSelection()
#    target=None
#    return MySaveDialog(target)
    saveSketch()

def runSketchLib():
    '''method called from Gui menu'''
    sayexc2("Ups","Noch nicht implementiert")


def setDatum(sk,datname,datvalue):
    
    c=getNamedConstraint(sk,datname)
    #c=
    cc=sk.Constraints[c]
    print ("---------",c,cc.Value)
    print (cc.Driving)
    cd=cc.Driving
    sk.setDriving(c,True)
    sk.setDatum(c,datvalue)
    sk.setDriving(c,cd)
    print ("rc solve",sk.solve())
    

def reportSketch(sk):
    ''' report constraints of a sketch'''
    #sk=App.ActiveDocument.ufo
    cs=sk.Constraints
    datumtypes=['Radius','DistanceX','DistanceY','Distance']

    for ci,c in enumerate(cs):
        # only datums
        if c.Type in datumtypes:
            print (ci,c.Name,c.Type,c.Value,c.Driving,c.InVirtualSpace,[c.First,c.FirstPos])

    print ("nameless datum ------------------")
    for ci,c in enumerate(cs):
        # only datums
        if c.Type in datumtypes and c.Name=='':
            print (ci,c.Name,c.Type,c.Value,c.Driving,c.InVirtualSpace,[c.First,c.FirstPos])

    return
    for v in [30,0,40]:
        try:
            setDatum(sk,'line_A',v)
        except:
            print ("kann nicht ",v )

def createConstraint(sk,line,name,value,blue=False):
        rc=sk.addConstraint(Sketcher.Constraint('Distance',line,value)) 
        sk.renameConstraint(rc, name)
        if blue: 
            sk.toggleDriving(rc) 
        return rc



def connectAll(sk):
        '''connect all matching geometries'''
        for i,c in enumerate(sk.Geometry):
            for i2,c2 in enumerate(sk.Geometry):
                if i<i2:
                    for j in [1,2]:
                        for j2 in [1,2]:
                            if sk.getPoint(i,j)==sk.getPoint(i2,j2):
                                cc=sk.addConstraint(Sketcher.Constraint('Coincident',i,j,i2,j2)) 
                                if sk.solve()!=0:
                                    sk.delConstraint(cc)


def genQuadrangle():
        name="Viereck"
        sk=App.ActiveDocument.addObject('Sketcher::SketchObjectPython',name)
        _ViewProvider(sk.ViewObject)
        A=App.Vector(-100,-50,0)
        B=App.Vector(100,-50,0)
        C=App.Vector(100,50,0)
        D=App.Vector(-100,50,0)

        a=sk.addGeometry(Part.LineSegment(A,B),False)
        b=sk.addGeometry(Part.LineSegment(B,C),False)
        c=sk.addGeometry(Part.LineSegment(C,D),False)
        d=sk.addGeometry(Part.LineSegment(D,A),False)
        e=sk.addGeometry(Part.LineSegment(A,C),True)
        f=sk.addGeometry(Part.LineSegment(B,D),True)

#        c1=sk.addConstraint(Sketcher.Constraint('Block',a)) 
#        c2=sk.addConstraint(Sketcher.Constraint('Block',c)) 

        connectAll(sk)

        if 1:
            length_a=createConstraint(sk,a,'length_a',300)
            length_b=createConstraint(sk,b,'length_b',200)
            length_c=createConstraint(sk,c,'length_c',300)
            length_d=createConstraint(sk,d,'length_d',300)

            length_e=createConstraint(sk,e,'length_e',300,blue=True)
            length_f=createConstraint(sk,f,'length_f',300,blue=True)
            

        sk.solve()
        App.ActiveDocument.recompute()
        print ("done")
        reportSketch(sk)

        App.ActiveDocument.openTransaction("set length_c 105")
        sk.setDatum(length_c,105)
        reportSketch(sk)
        App.ActiveDocument.commitTransaction()

        # Fehler erkennen
        App.ActiveDocument.openTransaction("set length_c 1205")
        try:
            sk.setDatum(length_c,1200)
            App.ActiveDocument.commitTransaction()
        except:
            print ("Fehler gemacht")
            reportSketch(sk)
            print ("roll back")
            #App.ActiveDocument.abortTransaction()
        reportSketch(sk)
        App.ActiveDocument.recompute()
        
        

        





def hahahaMainAgain():
         runLoadSketch()
    pass




