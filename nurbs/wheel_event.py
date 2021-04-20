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
#-- event filter for nurbs-needle editor 
#--
#-- microelly 2016
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''eventfilter for the nurbs-needle editor


'''

from PySide import QtGui,QtCore
from say import *

import FreeCAD as App
import sys,time

import NURBSinit

'''
# parameter
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MovePageStep",50)
App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveCursorStep",10)

'''



class EventFilter(QtCore.QObject):

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.mouseWheel=0
        self.enterleave=False
        self.enterleave=True
        self.keyPressed2=False
        self.editmode=False
        self.key='x'
        self.posx=-1
        self.posy=-1
        self.lasttime=time.time()
        self.lastkey='#'


    def eventFilter(self, o, e):

        z=str(e.type())

        event=e

        if event.type() == QtCore.QEvent.ContextMenu : return True

        # not used events
        if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
                z == 'PySide.QtCore.QEvent.Type.ChildRemoved'or \
                z == 'PySide.QtCore.QEvent.Type.User'  or \
                z == 'PySide.QtCore.QEvent.Type.Paint' or \
                z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
                z == 'PySide.QtCore.QEvent.Type.UpdateRequest'   :
            return QtGui.QWidget.eventFilter(self, o, e)

        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = event.pos()
                x=pos.x()
                y=pos.y()
                # print ("mous pos ",x,y)


        if z == 'PySide.QtCore.QEvent.Type.KeyPress':
            # http://doc.qt.io/qt-4.8/qkeyevent.html

            # ignore editors
            try:
                if self.editmode:
                    return QtGui.QWidget.eventFilter(self, o, e)
            except: pass
            
            # only first time key pressed
            if not self.keyPressed2:
                self.keyPressed2=True
                time2=time.time()
                ee=e.text()

                if time2-self.lasttime<0.01 and len(ee)>0 and ee[0]==self.lastkey:
                    self.lasttime=time2
                    return False

                try:
                    # only two function keys implemented, no modifieres
                    if e.key()== QtCore.Qt.Key_F2:
                        say("------------F2-- show mode and moddata---------------")
                        print (self.mode)
                        return False
                    elif e.key()== QtCore.Qt.Key_Escape:
                        say("------------Escape-----------------")
                        stop()

                    elif e.key()== QtCore.Qt.Key_F3 :
                        say("------------F3-----------------")
                        stop()


                    elif e.key()== QtCore.Qt.Key_Enter or e.key()== QtCore.Qt.Key_Return:
#                        say("------------Enter-----------------")
                        self.update()
                    elif e.key() == QtCore.Qt.Key_Right :
                        if self.dialog.dial.value()==self.dialog.dial.maximum(): val=0
                        else: val=self.dialog.dial.value()+1
                        self.dialog.dial.setValue(val)
                        return True
                    elif e.key() == QtCore.Qt.Key_Left :
                        if self.dialog.dial.value()== 0: val=self.dialog.dial.maximum()
                        else: val=self.dialog.dial.value()-1
                        self.dialog.dial.setValue(val)
                        return True
                    elif e.key() == QtCore.Qt.Key_Up :
                        self.mouseWheel += App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveCursorStep",10)
                        self.dialog.ef_action("up",self,self.mouseWheel) 
                        return True
                    elif e.key() == QtCore.Qt.Key_Down :
                        self.mouseWheel -= App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveCursorStep",10) 
                        self.dialog.ef_action("down",self,self.mouseWheel)
                        return True
                    elif e.key() == QtCore.Qt.Key_PageUp :
                        self.mouseWheel += App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MovePageStep",50)
                        self.dialog.ef_action("up!",self,self.mouseWheel)
                        return True
                    elif e.key() == QtCore.Qt.Key_PageDown :
                        self.mouseWheel -= App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MovePageStep",50)
                        self.dialog.ef_action("down!",self,self.mouseWheel)
                        return True
                    else: # letter key pressed
                        ee=e.text()
                        if len(ee)>0: 
                            r=ee[0]
                            
                        else: r="key:"+ str(e.key())
                        #say("-------action for key ----!!------" + r)
                        self.lastkey=e.text()
                        if r=='+':
                            Gui.activeDocument().ActiveView.zoomIn()
                            return True
                        if r=='-':
                            Gui.activeDocument().ActiveView.zoomOut()
                            return True
                        if r=='*':
                            Gui.activeDocument().ActiveView.fitAll()
                            return True
                        if r in ['l','r','h','x','y','z','n','t','b']:
                            self.key=str(r)
                            self.mode=str(r)
                            App.ParamGet('User parameter:Plugins/nurbs').SetString("editorKey",self.key)
                            self.dialog.ef_action(r,self)
                            self.dialog.modelab.setText("Direction: "+ r)
                        if r == '0':
                            self.mouseWheel = 0
                            self.mode='0'

                except:
                    sayexc()

        # end of a single key pressed
        if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
            self.lasttime=time.time()
            self.keyPressed2=False

        # enter and leave a widget - editor widgets
        if z == 'PySide.QtCore.QEvent.Type.Enter' or z == 'PySide.QtCore.QEvent.Type.Leave':
            pass

        # deactivate keys in editors context
        if z == 'PySide.QtCore.QEvent.Type.Enter' and \
            (o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
            self.editmode=True
        elif z == 'PySide.QtCore.QEvent.Type.Leave' and \
            (o.__class__ == QtGui.QPlainTextEdit or o.__class__ == QtGui.QTextEdit):
            self.editmode=False

        # mouse movement only leaves and enters
        if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
            pass



        event=e
        try:

            if event.type() == QtCore.QEvent.ContextMenu : #and o.__class__ == QtGui.QWidget:
                    # hier contextmenue rechte maus auschalten
                    App.Console.PrintMessage('!! cancel -------------------------------------context-----------\n')
                    return False
                    pass

            # wheel rotation
            if event.type()== QtCore.QEvent.Type.Wheel:

                self.mouseWheel += e.delta()/120
                pos=e.pos()
                self.posx=pos.x()
                self.posy=pos.y()

                ##App.Console.PrintMessage("wheel: " + str(self.mouseWheel) + " pos: " +str(e.pos())+ "\n")
                #self.modedat[self.mode]=self.mouseWheel
                self.dialog.ef_action("wheel",self,self.mouseWheel)

                noDefaultWheel = self.mode!='n'
                
                if noDefaultWheel:
                    return True 
                else:
                    return False

            # mouse clicks
            if event.type() == QtCore.QEvent.MouseButtonPress or \
                    event.type() == QtCore.QEvent.MouseButtonRelease or\
                    event.type() == QtCore.QEvent.MouseButtonDblClick:

#                App.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')

                if event.button() == QtCore.Qt.MidButton or  event.button() == QtCore.Qt.MiddleButton:
#                    App.Console.PrintMessage('!-------------------------------------!!  X middle \n')
                    return False

                if event.button() == QtCore.Qt.LeftButton:
#                    App.Console.PrintMessage('!! X one left\n')
                    return False

                elif event.button() == QtCore.Qt.RightButton:
#                    App.Console.PrintMessage('!! X one right\n')
                    return False

        except:
            sayexc()
        return QtGui.QWidget.eventFilter(self, o, e)


    def update(self):
        self.dialog.commit_noclose()




def focus():
    '''get preselected pole sets'''

    try:
        s=Gui.Selection.getSelection()[0]

        s.Object.Label
    #    print s.Object.Name
    #    print s.SubElementNames


        needle=s.Object.InList[0]
        needle.Label

        for sen in s.SubElementNames:
            print (sen[4:])
            if s.Object.Name[0:4]=='Ribs':
                return (needle,"rib",int(sen[4:]))
            if s.Object.Name[0:9]=='Meridians':
                return(needle,"meridian",int(sen[4:]))
    except:
        return (None,None,-1)


def liposs(liste,start,ende):
    ''' index of an interval in a list '''
    try: l=len(liste)
    except: l=liste.shape[0]
    lix=[p%l for p in range(start,ende+1)]
    print ("liposs l-s-e ix",l,start,ende,lix)
    return lix




class MyWidget(QtGui.QWidget):
    '''edit pole mastre dialog'''

    def getNeedle(self): 
        source=self.getsource()
        needle=source.InList[0]
        return needle


    def commit_noclose(self):

        self.update()
        hd=self.helperDok()
        poles=hd.BSpline.Shape.Edge1.Curve.getPoles()
        
        pos=self.dial.value()
        source=self.getsource()
        needle=source.InList[0]
        curve,bb,scaler,twister= needle.Proxy.Model()
        self.twister=twister
        self.scaler=scaler
        if self.source=='Backbone': 
            bb=poles
            (rx,ry,rz)=twister[pos]
            twister[pos]=[self.dialx.value(),self.dialy.value(),self.dialz.value()]
        elif self.source=='Rib_template': curve=poles

        needle.Proxy.updateSS(curve,bb,scaler,twister)

# geht nicht #+# warumn?
#        App.getDocument("Unnamed").Spreadsheet.touch()
#        App.getDocument("Unnamed").recompute()

        docname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
        App.ActiveDocument=App.getDocument(docname)
        Gui.ActiveDocument=Gui.getDocument(docname)
        App.ActiveDocument.Spreadsheet.touch()
        App.ActiveDocument.recompute()
        self.setSelection(pos)

    def commit(self):
        ''' commit data and close dialog '''
        self.commit_noclose()
        self.closeHelperDok()
        stop()

    def cancel(self):
        self.closeHelperDok()
        stop()

    def getsource(self):
        docname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
        return App.getDocument(docname).getObject(self.source)

    def update(self):
        mode=self.imode
        print ("focus",focus())
        ef=self.ef
        print ("val,x,y,k",ef.mouseWheel,ef.posx,ef.posy,ef.key)
        #hilfsfenster 
        hd=self.helperDok()


        # move-mode
        if mode==0 or mode==-1:
            try: 
                bb=App.ActiveDocument.BSpline
                pos=self.dial.value()

                try:
                    t=hd.Target.Shape.Vertex1.Point
                except:
                    t=App.Vector()
                print ("Target",t)
                pp=bb.Shape.Edge1.Curve.getPoles()
                points=pp
                if pos>0:
                    pp2=pp[:pos]+[t]+pp[pos+1:]
                else:
                    pp2=[t]+pp[pos+1:]

                bs=bb.Shape.Edge1.Curve.copy()
                bs.setPole(pos+1,App.Vector(t))
                bb.Shape=bs.toShape()
                points=pp2

            except:
                print ("ExCEPT - need to create helper BSpline")
                src=self.getsource()
                points=src.Shape.Edge1.Curve.getPoles()
                mybsc=App.ActiveDocument.addObject('Part::Feature','BSpline')
                mybsc.Shape=src.Shape
                mybsc.ViewObject.Selectable=False

                Gui.activeDocument().activeView().viewAxonometric()
                Gui.SendMsgToActiveView("ViewFit")
                bb=App.ActiveDocument.ActiveObject

            Gui.Selection.addSelection(bb)

            self.points=points
            self.setcursor()
            #reset diff
            self.ef.mouseWheel=0
            self.settarget()
            return

        if mode==1:
            bb=App.ActiveDocument.BSpline
            pos=self.dial.value()

#            try:
#                t=hd.Target.Shape.Point
#            except:
#                t=App.Vector()

            t1=hd.Target.Shape.Vertex1.Point
            t=hd.Target.Shape.Vertex2.Point
            t2=hd.Target.Shape.Vertex3.Point


            pp=bb.Shape.Edge1.Curve.getPoles()
            points=pp
            [pi1,pi,pi2]=liposs(points,pos-1,pos+1)
            pp2=pp
            pp2[pi1]=t1
            pp2[pi2]=t2
            pp2[pi]=t

            print ("len pp, pp2",len(pp),len(pp2))

            bs=bb.Shape.Edge1.Curve.copy()
            bs.setPole(pi1+1,App.Vector(t1))
            bs.setPole(pi+1,App.Vector(t))
            bs.setPole(pi2+1,App.Vector(t2))

            bb=hd.TargetCurve
            bb.Shape=bs.toShape()
            points=pp2

            Gui.Selection.addSelection(bb)

            self.points=points
            self.setcursor()
            #reset diff
            self.ef.mouseWheel=0
            self.settarget()
            return

#-----------------------
        elif mode==2:
            faktor=self.dials.value()
            self.dials.setValue(0)
            
            print ("sharpen.",faktor)
            pos=self.dial.value()
            dok=self.helperDok()
            
            pp=self.points

            t1=pp[pos-1]*(1-0.01*faktor)+pp[pos]*0.01*faktor
            if pos==len(pp)-1:
                t2=pp[0]*(1-0.01*faktor)+pp[pos]*0.01*faktor
            else:
                t2=pp[pos+1]*(1-0.01*faktor)+pp[pos]*0.01*faktor

            if pos==len(pp)-1:
                pp2=pp[1:pos-1]+[t1,pp[pos],t2] # +pp[pos+2:]
            elif pos>0: pp2=pp[:pos-1]+[t1,pp[pos],t2]+pp[pos+2:]
            else: pp2=[t1,pp[pos],t2]+pp[2:-1]

            bb=dok.TargetCurve

            # bspline curve
            bs=dok.BSpline.Shape.Edge1.Curve.copy()
            if pos==0: posa =len(pp)
            else: posa= pos
            bs.setPole(posa,App.Vector(t1))
            if pos==len(pp)-1: posb =1
            else: posb= pos+2

            bs.setPole(posb,App.Vector(t2))
            dok.BSpline.Shape=bs.toShape()

            pol=Part.makePolygon(pp2+[pp2[0]])
            bb.Shape=Part.Compound([pol])


            points=pp2

        elif mode==4:
            print ("rotate NEIOGHJHGJH")
            
#-----------------------
        elif mode==3:
            # colinear neighbors
            faktor=self.dials.value()
            #faktor= 100
            self.dials.setValue(0)
            
            print ("update sharpen.",faktor)
            pos=self.dial.value()
            dok=self.helperDok()
            
            pp=self.points

            if pos==len(pp)-1:
                t2=pp[pos]+(pp[0]-pp[pos-1])*(1-0.01*faktor)
                t1=pp[pos]-(pp[0]-pp[pos-1])*(1-0.01*faktor)
            else:
                t2=pp[pos]+(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)
                t1=pp[pos]-(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)


#            if pos==len(pp)-1:
#                t2=pp[0]*(1-0.01*faktor)+pp[pos]*0.01*faktor
#            else:
#                t2=pp[pos]+(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)
#                t1=pp[pos]-(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)

            if pos==len(pp)-1:
                pp2=pp[1:pos-1]+[t1,pp[pos],t2] # +pp[pos+2:]
            elif pos>0: pp2=pp[:pos-1]+[t1,pp[pos],t2]+pp[pos+2:]
            else: pp2=[t1,pp[pos],t2]+pp[2:-1]

            bb=dok.TargetCurve

            # bspline curve
            bs=dok.BSpline.Shape.Edge1.Curve.copy()
            if pos==0: posa =len(pp)
            else: posa= pos
            bs.setPole(posa,App.Vector(t1))
            if pos==len(pp)-1: posb =1
            else: posb= pos+2

            bs.setPole(posb,App.Vector(t2))
            dok.BSpline.Shape=bs.toShape()

            pol=Part.makePolygon(pp2+[pp2[0]])
            bb.Shape=Part.Compound([pol])


            points=pp2


#----------------------

            Gui.Selection.addSelection(bb)

            self.points=points
            self.setcursor()
            #reset diff
            self.ef.mouseWheel=0
            self.settarget()
            return



        else:
            print ("!!!!!!!!!!!!!! no imp for this mode!!")



    def ef_action(self,*args):
        # aufruf durch ef.dialog.ef_action()
        self.settarget()


    def helperDok(self):
        '''get or create helper document'''
        try: hd=App.getDocument("Aux")
        except:
            App.newDocument("Aux")
            hd=App.getDocument("Aux")


        App.setActiveDocument("Aux")
        App.ActiveDocument=App.getDocument("Aux")
        Gui.ActiveDocument=Gui.getDocument("Aux")
        return hd

    def closeHelperDok(self):
        '''close helper document'''
        try: App.closeDocument("Aux")
        except: pass

    def cursor(self,dok,cords=(0,0,0),restore=False):
        '''pointer to the selected pole/coords as a red quad'''
        v=Part.Point(App.Vector(cords)).toShape()
        try: curs=dok.Cursor
        except: 
            curs=dok.addObject('Part::Feature','Cursor')
            curs.ViewObject.Selectable=False
        curs.Shape=v
        dok.recompute()
        curs.ViewObject.PointSize=10
        curs.ViewObject.PointColor=(1.0,1.,0.)
        self.settarget()
        obj=self.getNeedle()
        curve,bb,scaler,twister= obj.Proxy.Model()
        pos=self.dial.value()
        if restore and hasattr(self,'dialx'):
            self.dialx.setValue(twister[pos][0])
            self.dialy.setValue(twister[pos][1])
            self.dialz.setValue(twister[pos][2])


    def setcursor(self):
        ''' set cursor to the dialer selecterd pole'''
        hd=self.helperDok()
        pl=len(self.points)
        self.cursor(hd,self.points[self.dial.value()%pl],False)
        self.dial.setMaximum(pl-1)

    def setcursor2(self,p):
        ''' set cursor as dialer backcall'''
        hd=self.helperDok()
        self.cursor(hd,self.points[p],True)
        App.ParamGet('User parameter:Plugins/nurbs').SetInt("Cursor",p)
        self.setSelection(p)


    def setSelection(self,pos):
        obj=self.getNeedle()

        if self.source=='Backbone':
            obj.Proxy.showRib(pos)
        else:
            obj.Proxy.showMeridian(pos)

    def setrotx(self,rx):
        self.rotx=rx
        self.settarget()

    def setroty(self,r):
        self.roty=r
        self.settarget()

    def setrotz(self,r):
        self.rotz=r
        self.settarget()

    def setsharp(self,v):
        if self.imode==3:
            print ("mode 3")
            self.setsharp3(v)
            return
        
        faktor=v
        print ("sharpen.",faktor)
        pos=self.dial.value()
        dok=self.helperDok()
        
        pp=self.points

        t1=pp[pos-1]*(1-0.01*faktor)+pp[pos]*0.01*faktor
        if pos==len(pp)-1:
            t2=pp[0]*(1-0.01*faktor)+pp[pos]*0.01*faktor
        else:
            t2=pp[pos+1]*(1-0.01*faktor)+pp[pos]*0.01*faktor

        if pos==len(pp)-1:
            pp2=pp[1:pos-1]+[t1,pp[pos],t2] # +pp[pos+2:]
        elif pos>0: pp2=pp[:pos-1]+[t1,pp[pos],t2]+pp[pos+2:]
        else: pp2=[t1,pp[pos],t2]+pp[2:-1]

        bb=dok.TargetCurve

        # bspline curve
        bs=dok.BSpline.Shape.Edge1.Curve.copy()
        if pos==0: posa =len(pp)
        else: posa= pos
        bs.setPole(posa,App.Vector(t1))
        if pos==len(pp)-1: posb =1
        else: posb= pos+2

        bs.setPole(posb,App.Vector(t2))
        dok.BSpline.Shape=bs.toShape()

        pol=Part.makePolygon(pp2+[pp2[0]])
        bb.Shape=Part.Compound([pol])


    def setsharp3(self,v,run=True):
        
        faktor=v
        print ("3 sharpen.",faktor)
        pos=self.dial.value()
        dok=self.helperDok()
        
        pp=self.points

        if pos==len(pp)-1:
            t2=pp[pos]+(pp[0]-pp[pos-1])*(1-0.01*faktor)
            t1=pp[pos]-(pp[0]-pp[pos-1])*(1-0.01*faktor)
        else:
            t2=pp[pos]+(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)
            t1=pp[pos]-(pp[pos+1]-pp[pos-1])*(1-0.01*faktor)

#        t1=pp[pos-1]*(1-0.01*faktor)+pp[pos]*0.01*faktor
#
#        if pos==len(pp)-1:
#            t2=pp[0]*(1-0.01*faktor)+pp[pos]*0.01*faktor
#        else:
#            t2=pp[pos+1]*(1-0.01*faktor)+pp[pos]*0.01*faktor


        if pos==len(pp)-1:
            pp2=pp[1:pos-1]+[t1,pp[pos],t2] # +pp[pos+2:]
        elif pos>0: pp2=pp[:pos-1]+[t1,pp[pos],t2]+pp[pos+2:]
        else: pp2=[t1,pp[pos],t2]+pp[2:-1]

        bb=dok.TargetCurve

        # bspline curve
        bs=dok.BSpline.Shape.Edge1.Curve.copy()
        if pos==0: posa =len(pp)
        else: posa= pos
        bs.setPole(posa,App.Vector(t1))
        if pos==len(pp)-1: posb =1
        else: posb= pos+2

        bs.setPole(posb,App.Vector(t2))
        dok.BSpline.Shape=bs.toShape()

        pol=Part.makePolygon(pp2+[pp2[0]])
        bb.Shape=Part.Compound([pol])

        #hier backbone anpassen
        self.dials.setValue(0)



    def target_old(self,dok,cords=(0,0,0)):
        ''' set changed pole to '''
        v=Part.Point(App.Vector(cords)).toShape()
        try: curs=dok.Target
        except: 
            curs=dok.addObject('Part::Feature','Target')
            curs.ViewObject.Selectable=False
        curs.Shape=v
        dok.recompute()
        curs.ViewObject.PointSize=10
        curs.ViewObject.PointColor=(.0,0.,1.)

    def target(self,dok,cords=(0,0,0),coordlist=[]):
        ''' set changed pole to '''
        if len(coordlist)>1 and coordlist[0]!=coordlist[1]:
            col=Part.makePolygon(coordlist)
            v=Part.makeCompound([col])
        else:
            if len(coordlist)==1: cords=coordlist[0]
            v=Part.Point(App.Vector(cords)).toShape()

        try: curs=dok.Target
        except: 
            curs=dok.addObject('Part::Feature','Target')
            curs.ViewObject.Selectable=False
        curs.Shape=v
        dok.recompute()
        curs.ViewObject.PointSize=20
        curs.ViewObject.PointColor=(.0,0.,1.)


    def settarget(self):
        '''set the target depending on the mouse wheel roll and mode key'''
        if self.imode==3:
            print ("SET IMODE 3")
            ef=self.ef


            self.dials.setValue(min(ef.mouseWheel,99))
            self.setsharp3(min(ef.mouseWheel,99))
            #return

        if self.imode==4:
            print ("SET IMODE 4")
            self.settarget4()
            return

        
        dok=self.helperDok()
        pl=len(self.points)
        self.dial.setMaximum(pl-1)
        pos=self.dial.value()

        if pos==0: lpos=pl-1
        else: lpos=pos-1

        if pos==pl-1: rpos=0
        else: rpos=pos+1
#        print ('pl,pos,lpos,rpos',pl,pos,lpos,rpos)


        if  self.imode!=3:
            diff=App.Vector()
            ef=self.ef
            if ef.key in  ['x','y','z']:
                kx,ky,kz=0,0,0
                if ef.key=='x': kx=ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)
                if ef.key=='y': ky=ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)
                if ef.key=='z': kz=ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)

                #changed point 
                diff=App.Vector(kx,ky,kz)
                t=self.points[pos] + diff
            elif  ef.key=='t':
                a=App.Vector(self.points[lpos])-App.Vector(self.points[rpos])
                a.normalize()
                diff=a.multiply(ef.mouseWheel *App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1))
                t=self.points[pos] + diff 
            elif  ef.key=='n' or  ef.key=='b':
                a=App.Vector(self.points[lpos])-App.Vector(self.points[rpos])
                b=App.Vector(self.points[lpos])-App.Vector(self.points[pos])
                c=a.cross(b)
                if  ef.key=='n': d=c.cross(a)
                else: d=c
                d.normalize()
                diff=d.multiply(ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1))
                t=self.points[pos] + diff 
            elif  ef.key=='r':
                d=App.Vector(self.points[pos][0],self.points[pos][1],0).normalize()
                diff=d.multiply(ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1))
                t=self.points[pos] + diff 
            else:
                print ("mode not implemented ",ef.key)
                t=self.points[pos]

            #self.target(dok, t)
            print ("settarget cc imode", self.imode)
            print ("diff",diff)
            if self.imode==1:
                self.target(dok,coordlist=[self.points[pos-1]+diff,t,self.points[pos+1]+diff]) 
            else:
                self.target(dok,coordlist=[t]) 

    #        try: dok.Sphere
    #        except:
    #            s=dok.addObject("Part::Sphere","Sphere")
    #            s.Radius=10000000
    #            s.ViewObject.Selectable=False
    #            s.ViewObject.ShapeColor=(1.,1.,1.)
    #            s.ViewObject.DisplayMode = u"Shaded"
    #            s.ViewObject.DisplayMode = u"Shaded"

            # create or get traget curve

            pp=self.points

            if pos>0: pp2=pp[:pos]+[t]+pp[pos+1:]
            else: pp2=[t]+pp[pos+1:]

            # bspline curve
            bs=dok.BSpline.Shape.Edge1.Curve.copy()
            bs.setPole(pos+1,App.Vector(t))
            if self.imode==1:
                bs.setPole(pos,self.points[pos-1]+diff)
                bs.setPole(pos+2,self.points[pos+1]+diff)
            dok.BSpline.Shape=bs.toShape()
            pol=Part.makePolygon(pp2 + [pp2[0]])

        else:
            pp2=self.points

            # pole polygon
            pol=Part.makePolygon(pp2 + [pp2[0]])
    #        bb.Shape=pol

            bs=dok.BSpline.Shape.Edge1.Curve.copy()


        try: 
            bb=dok.TargetCurve
            bax=dok.TargetExtra
        
        except: 
            bb=dok.addObject('Part::Feature','TargetCurve')
            bax=dok.addObject('Part::Feature','TargetExtra')
            
        bax.ViewObject.LineColor=(1.0,1.0,0.0)


        pp3=[]
        ppax=[]

        if self.source=='Backbone':
            print ("recompute Backbone #########################################")
            xV=App.Vector(100,0,0)
            yV=App.Vector(0,100,0)
            zV=App.Vector(0,0,141)

            source=self.getsource()
            needle=source.InList[0]
            curvea,bba,scaler,twister= needle.Proxy.Model()


            for i,p in enumerate(pp2):
                # print (i,twister[i],scaler[i])
                [xa,ya,za]=twister[i]

                if pos  == i :
                    xa += self.rotx
                    ya += self.roty
                    za += self.rotz

                if pos  == i :
                    xa = self.rotx
                    ya = self.roty
                    za = self.rotz



                p2=App.Placement()
                p2.Rotation=App.Rotation(App.Vector(0,0,1),za).multiply(App.Rotation(App.Vector(0,1,0),ya).multiply(App.Rotation(App.Vector(1,0,0),xa)))

                ph=App.Placement()
                ph.Base=xV
                xR=p2.multiply(ph).Base
                ph=App.Placement()
                ph.Base=yV
                yR=p2.multiply(ph).Base
                ph=App.Placement()
                ph.Base=zV
                zR=p2.multiply(ph).Base

                p=App.Vector(p)

                if 1:
                    pp=Part.makePolygon([p,p+xR,p+xR+yR,p])
                    ps=Part.Face(pp)
                    ppax.append(ps)
                    pp=Part.makePolygon([p,p+yR,p+xR+yR,p])
                    ppax.append(Part.Face(pp))
                    pp=Part.makePolygon([p,p+zR,p+xR+yR,p])
                    ppax.append(Part.Face(pp))


        # all together 
        bb.Shape=Part.Compound([pol])
        if ppax!=[]:
            bax.Shape=Part.Compound(ppax + [bs.toShape()])

        dok.recompute()

        bb.ViewObject.LineColor=(1.0,0.6,.0)
        bb.ViewObject.LineWidth=1
        bb.ViewObject.PointColor=(.8,0.4,.0)
        bb.ViewObject.PointSize=8
        bax.ViewObject.Selectable=False

        col=[]
        for i in range(len(bax.Shape.Faces)):
            tt=i%3
            if tt==0: col.append((1.,0.,0.))
            elif tt==1: col.append((0.,1.,0.))
            else: col.append((0.,0.,1.))
        # bax.ViewObject.DiffuseColor=col
        bax.ViewObject.LineColor=(1.0,0.0,0.0)



    def settarget4(self):
        '''rotate neighbors'''

        print ("settarget 4")

        dok=self.helperDok()
        pl=len(self.points)
        self.dial.setMaximum(pl-1)
        pos=self.dial.value()

        if pos==0: lpos=pl-1
        else: lpos=pos-1

        if pos==pl-1: rpos=0
        else: rpos=pos+1
#        print ('pl,pos,lpos,rpos',pl,pos,lpos,rpos)

        t=self.points[pos]
        t1=self.points[pos-1]
        t2=self.points[pos+1]
        
        dt1=t1-t
        dt2=t2-t
        print (dt1,dt2)
        
        # rotation
        p2=App.Placement()
        #p2.Rotation=App.Rotation(App.Vector(0,0,1),za).multiply(App.Rotation(App.Vector(0,1,0),ya).multiply(App.Rotation(App.Vector(1,0,0),xa)))
        ef=self.ef
        kr=ef.mouseWheel * App.ParamGet('User parameter:Plugins/nurbs').GetFloat("MoveWheelStep",1)
        p2.Rotation=App.Rotation(App.Vector(0,0,1),kr)
        
        print (t1,t2)
        ph=App.Placement()
        ph.Base=dt1
        drt1=p2.multiply(ph).Base
        t1=t+drt1

        ph=App.Placement()
        ph.Base=dt2
        drt2=p2.multiply(ph).Base
        t2=t+drt2

        print (t1,t2)
        print ("kilo")
        self.target(dok,coordlist=[t1,t,t2]) 

#        try: dok.Sphere
#        except:
#            s=dok.addObject("Part::Sphere","Sphere")
#            s.Radius=10000000
#            s.ViewObject.Selectable=False
#            s.ViewObject.ShapeColor=(1.,1.,1.)
#            s.ViewObject.DisplayMode = u"Shaded"
#            s.ViewObject.DisplayMode = u"Shaded"

        # create or get traget curve
        try: 
            bb=dok.TargetCurve
            bax=dok.TargetExtra
        
        except: 
            bb=dok.addObject('Part::Feature','TargetCurve')
            bax=dok.addObject('Part::Feature','TargetExtra')
        
        bax.ViewObject.LineColor=(1.0,1.0,0.0)


        pp=self.points

        pp2=pp[:pos-1]+[t1,t,t2]+pp[pos+2:]
        print ("lnes",len(pp),len(pp2))

        # bspline curve
        bs=dok.BSpline.Shape.Edge1.Curve.copy()
        bs.setPole(pos,App.Vector(t1))
        bs.setPole(pos+1,App.Vector(t))
        bs.setPole(pos+2,App.Vector(t2))
        dok.BSpline.Shape=bs.toShape()
        sss=bs.toShape()

        # pole polygon
        pol=Part.makePolygon(pp2 + [pp2[0]])
#        bb.Shape=pol



        pp3=[]
        ppax=[]
        
        print ("wwww")

        if self.source=='Backbone':
            xV=App.Vector(100,0,0)
            yV=App.Vector(0,100,0)
            zV=App.Vector(0,0,141)

            source=self.getsource()
            needle=source.InList[0]
            curvea,bba,scaler,twister= needle.Proxy.Model()


            for i,p in enumerate(pp2):
                # print (i,twister[i],scaler[i])
                [xa,ya,za]=twister[i]

                if pos  == i :
                    xa += self.rotx
                    ya += self.roty
                    za += self.rotz

                if pos  == i :
                    xa = self.rotx
                    ya = self.roty
                    za = self.rotz



                p2=App.Placement()
                p2.Rotation=App.Rotation(App.Vector(0,0,1),za).multiply(App.Rotation(App.Vector(0,1,0),ya).multiply(App.Rotation(App.Vector(1,0,0),xa)))

                ph=App.Placement()
                ph.Base=xV
                xR=p2.multiply(ph).Base
                ph=App.Placement()
                ph.Base=yV
                yR=p2.multiply(ph).Base
                ph=App.Placement()
                ph.Base=zV
                zR=p2.multiply(ph).Base

                p=App.Vector(p)

                if 1:
                    pp=Part.makePolygon([p,p+xR,p+xR+yR,p])
                    ps=Part.Face(pp)
                    ppax.append(ps)
                    pp=Part.makePolygon([p,p+yR,p+xR+yR,p])
                    ppax.append(Part.Face(pp))
                    pp=Part.makePolygon([p,p+zR,p+xR+yR,p])
                    ppax.append(Part.Face(pp))


        # all together 
        bb.Shape=Part.Compound([pol])
        if ppax!=[]:
            bax.Shape=Part.Compound(ppax + [bs.toShape(),sss])

        dok.recompute()

        bb.ViewObject.LineColor=(1.0,0.6,.0)
        bb.ViewObject.LineWidth=1
        bb.ViewObject.PointColor=(.8,0.4,.0)
        bb.ViewObject.PointSize=8
        bax.ViewObject.Selectable=False

        col=[]
        for i in range(len(bax.Shape.Faces)):
            tt=i%3
            if tt==0: col.append((1.,0.,0.))
            elif tt==1: col.append((0.,1.,0.))
            else: col.append((0.,0.,1.))
        bax.ViewObject.DiffuseColor=col

    def settarget2(self,p):
        '''set target as dialer callback'''
        dok=self.helperDok()
        #self.target(dok,self.points[p])
        self.target(dok,coordlist=self.points[p-1:p+1])

    def setmode(self,index):
        '''callback from list'''
        self.imode=index
        print (self.mode.currentText())
        App.ParamGet('User parameter:Plugins/nurbs').SetString("editorMode",str(self.mode.currentText()))
        if index not in [2,3]:
            self.rotsl.hide()
            self.dials.hide()
        else:
            self.rotsl.show()
            self.dials.show()



def dialog(source):
    ''' create dialog widget'''

    
    w=MyWidget()
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    w.source=source
    w.imode=-1
    w.ef="no eventfilter defined"


    try:
        n=w.getNeedle()
        n.RibTemplate.ViewObject.hide()
        n.Backbone.ViewObject.hide()
    except:
        pass


    mode=QtGui.QComboBox()
    mode.addItem("move pole") #0
    mode.addItem("move pole and neighbors") #1
    mode.addItem("sharpen/smooth edge") #2
    mode.addItem("colinear neighbors") #3
    mode.addItem("rotate neighbors") #4
    #App.ParamGet('User parameter:Plugins/nurbs').SetString("editorMode","move pole and neighbors")
    
    
    mode.currentIndexChanged.connect(w.setmode)
    w.mode=mode
    

    editorkey=App.ParamGet('User parameter:Plugins/nurbs').GetString("editorKey","h")
    lab=QtGui.QLabel("Direction: " + editorkey)
    w.key=editorkey
    w.modelab=lab

    btn=QtGui.QPushButton("Cancel")
    btn.clicked.connect(w.cancel)

    cobtn=QtGui.QPushButton("Commit and stop")
    cobtn.clicked.connect(w.commit)

    conbtn=QtGui.QPushButton("Commit and continue")
    conbtn.clicked.connect(w.commit_noclose)

    cbtn=QtGui.QPushButton("Stop Dialog (preserve Aux)")
    cbtn.clicked.connect(stop)

    poll=QtGui.QLabel("Selected  Pole:")

    dial=QtGui.QDial() 
    dial.setNotchesVisible(True)
    dial.setValue(App.ParamGet('User parameter:Plugins/nurbs').GetInt("Cursor",0))
    dial.valueChanged.connect(w.setcursor2)
    w.dial=dial
    



    if source == 'Backbone':
        rotxl=QtGui.QLabel("Rotation X:")

        dialx=QtGui.QDial() 
        dialx.setNotchesVisible(True)
        dialx.setMinimum(-90)
        dialx.setMaximum(90)
        dialx.setValue(0)
        dialx.setSingleStep(15)
        dialx.valueChanged.connect(w.setrotx)
        w.dialx=dialx

        rotyl=QtGui.QLabel("Rotation Y:")

        dialy=QtGui.QDial() 
        dialy.setNotchesVisible(True)
        dialy.setMinimum(-90)
        dialy.setMaximum(90)
        dialy.setValue(0)
        dialy.setSingleStep(15)

        dialy.valueChanged.connect(w.setroty)
        w.dialy=dialy

        rotzl=QtGui.QLabel("Rotation Z:")

        dialz=QtGui.QDial() 
        dialz.setNotchesVisible(True)
        dialz.setMinimum(-90)
        dialz.setMaximum(90)
        dialz.setValue(0)
        dialz.setSingleStep(15)

        dialz.valueChanged.connect(w.setrotz)
        w.dialz=dialz
        
        rots=[rotxl,dialx,rotyl,dialy,rotzl,dialz]
    else:
        rots=[]


    if 1:
        rotsl=QtGui.QLabel("Sharpen Smooth Factor:")
        w.rotsl=rotsl

        dials=QtGui.QDial() 
        dials.setNotchesVisible(True)
        dials.setMinimum(-99)
        dials.setMaximum(99)
        dials.setValue(0)
        dials.setSingleStep(10)
        dials.valueChanged.connect(w.setsharp)
        w.dials=dials



    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    
    for ww in [mode,lab,btn,cobtn,conbtn,cbtn,poll,dial] + rots + [rotsl,dials]:
        box.addWidget(ww)

    rotsl.hide()
    dials.hide()
    
    
    return w

class SelObserver:
    def setPreselection(self,doc,obj,sub):
        pass# Preselection object
        # App.Console.PrintMessage("Pre! " +str(sub)+ "\n")          # The part of the object name

    def addSelection(self,doc,obj,sub,pnt):               # Selection object
        #App.Console.PrintMessage("addSelection"+ "\n")
        #App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # App.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
        if str(doc) != 'Aux': return
        if str(obj) != 'TargetCurve': return
        sel=str(sub)
        if sel.startswith('Vertex'):
            nr=sel[6:]
            App.eventfilter.dialog.dial.setValue(int(nr)-1)
        else:
            print ("no vertext")
            return


    def removeSelection(self,doc,obj,sub):
        pass                # Delete the selected object
        #App.Console.PrintMessage("removeSelection"+ "\n")

    def setSelection(self,doc):                           # Selection in ComboView
        pass
        #App.Console.PrintMessage("setSelection"+ "\n")

    def clearSelection(self,doc): 
        pass                        # If click on the screen, clear the selection
        #App.Console.PrintMessage("clearSelection"+ "\n")  # If click on another object, clear the previous object

                # Uninstall the resident function 


def start(source):
    '''create and initialize the event filter'''

    ef=EventFilter()
    ef.mouseWheel=0
    ef.mode='r'

    s =SelObserver()
    Gui.Selection.addObserver(s)                       # install the function mode resident
    ef.selObserver=s

    App.eventfilter=ef

    mw=QtGui.qApp
    mw.installEventFilter(ef)
    ef.keyPressed2=False

    ef.dialog=dialog(source)
    #ef.dialog.source=source
    ef.dialog.ef=ef
    ef.dialog.rotx=0
    ef.dialog.roty=0
    ef.dialog.rotz=0
    ef.dialog.update()
    if source=='Backbone':
            Gui.activeDocument().activeView().viewFront()
    else:
            Gui.activeDocument().activeView().viewTop()


    Gui.SendMsgToActiveView("ViewFit")

    ef.dialog.show()
    
    editorMode=App.ParamGet('User parameter:Plugins/nurbs').GetString("editorMode","move pole")
    ef.dialog.mode.setCurrentIndex(ef.dialog.mode.findText(editorMode))
    tt=Gui.activeDocument().activeView()
    tt.stopAnimating()

    mw=Gui.getMainWindow()
    mdiarea=mw.findChild(QtGui.QMdiArea)
    mdiarea.tileSubWindows()



def delo(label):
    ''' delete object by given label'''
    try:
        c=App.ActiveDocument.getObjectsByLabel(label)[0]
        App.ActiveDocument.removeObject(c.Name)
    except: pass

def stop():
    ''' stop eventserver'''

    mw=QtGui.qApp
    ef=App.eventfilter
    mw.removeEventFilter(ef)
    ef.keyPressed2=False
    ef.dialog.hide()
    
    s=ef.selObserver
    Gui.Selection.removeObserver(s)   

#    for l in ("Cursor","Target","TargetCurve"):
#        delo(l)
#        pass




def undock(label='Spreadsheet'):
    ''' open the data spreadsheet as top level window'''

    try:
        #activate eventmanager for ss
        a=App.ActiveDocument.MyNeedle
        a.Proxy.startssevents()
    except:
        print ("cannot active eventmanager")

    mw=Gui.getMainWindow()
    mdiarea=mw.findChild(QtGui.QMdiArea)

    sws=mdiarea.subWindowList()
    print ("windows ...")
    for w2 in sws:
        print (str(w2.windowTitle()))
        if str(w2.windowTitle()).startswith(label):
            sw=w2
            bl=w2.children()[3]
            blcc=bl.children()[2].children()

            w=QtGui.QWidget()
            w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

            box = QtGui.QVBoxLayout()
            w.setLayout(box)
            ss=blcc[3]
            box.addWidget(ss)
            # ss.setParent(w)
            w.setGeometry(50, 30, 1650, 350)
            w.show()
            sw.close()
            App.ss=w
            return w




try: stop()
except: pass

'''


'''
