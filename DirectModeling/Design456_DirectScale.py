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
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
from ThreeDWidgets import fr_arrow_widget
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
import ThreeDWidgets.fr_line_widget as wlin
import ThreeDWidgets.fr_coinwindow  as win
from ThreeDWidgets import fr_coin3d
from typing import ItemsView, List
import Design456Init
from PySide import QtGui,QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
import math
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR

SCALE_FACTOR=10.0 # This will be used to convert mouse movement to scale factor.

def ResizeObject(ArrowObject,linktocaller,startVector,EndVector):
    try:
        scaleX=scaleY=scaleZ=1.0
        deltaX=EndVector.x-startVector.x
        deltaY=EndVector.y-startVector.y
        deltaZ=EndVector.z-startVector.z

        (lengthX,lengthY,lengthZ)=linktocaller.getObjectLength()
        uniformValue=1.0
        oldLength=0.0
        print(linktocaller.b1.text())
        if (linktocaller.b1.text()=='Uniform'):
            #We maximize all of them regardles the change in which axis made
            if ArrowObject.w_color==FR_COLOR.FR_OLIVEDRAB:
                uniformValue=deltaY
            elif ArrowObject.w_color==FR_COLOR.FR_RED:
                uniformValue=deltaX
            elif ArrowObject.w_color==FR_COLOR.FR_BLUE:
                uniformValue=deltaZ
            else:
                # This shouldn't happen
                errMessage = "Unknown error occurred. Arrow's Color not find"
                faced.getInfo().errorDialog(errMessage)
                return 
            
            scaleX=scaleY=scaleZ=1+(uniformValue)/SCALE_FACTOR
            linktocaller.scaleLBL.setText("scale= "+str(scaleX))
        else:
            scaleX=1
            scaleY=1
            scaleZ=1
            if ArrowObject.w_color==FR_COLOR.FR_OLIVEDRAB:
                #y-direction moved
                scaleY=1+deltaY/SCALE_FACTOR
                linktocaller.scaleLBL.setText("scale= "+str(scaleY))
            elif ArrowObject.w_color==FR_COLOR.FR_RED:
                #x-direction moved
                scaleX=1+deltaX/SCALE_FACTOR
                linktocaller.scaleLBL.setText("scale= "+str(scaleX))
            elif ArrowObject.w_color==FR_COLOR.FR_BLUE:
                #z-direction moved
                scaleZ=1+deltaZ/SCALE_FACTOR
                linktocaller.scaleLBL.setText("scale= "+str(scaleZ))
        #Clone the object
        cloneObj = Draft.clone(linktocaller.selectedObj, forcedraft=True)
        #Scale the object
        cloneObj.Scale=App.Vector(scaleX,scaleY,scaleZ)

        linktocaller.selectedObj.Visibility=False
        App.ActiveDocument.recompute()
        _name=linktocaller.selectedObj.Label
        linktocaller.selectedObj.Label=linktocaller.selectedObj.Label+"old"
        __shape = Part.getShape(cloneObj,'',needSubElement=False,refine=False)
        _simpleCopy=App.ActiveDocument.addObject('Part::Feature',_name)
        _simpleCopy.Shape=__shape
        App.ActiveDocument.recompute()
        App.ActiveDocument.removeObject(linktocaller.selectedObj.Name)
        App.ActiveDocument.removeObject(cloneObj.Name)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(_simpleCopy)
        _simpleCopy.Label = _name        
        App.ActiveDocument.recompute()
        #All objects must get link to the new targeted object
        linktocaller.selectedObj=_simpleCopy

    except Exception as err:
        App.Console.PrintError("'Resize' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def callback_release(userData:fr_arrow_widget.userDataObject=None):
 
    try:    
        ArrowObject= userData.ArrowObj
        events=userData.events
        linktocaller= userData.callerObject  

        #Avoid activating this part several times,
        if (linktocaller.startVector==None): 
            return
        
        print("mouse release")
        ArrowObject.remove_focus()
        linktocaller.run_Once=False 
        linktocaller.endVector=App.Vector(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                              ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                              ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        
        ResizeObject(ArrowObject,linktocaller,linktocaller.startVector,linktocaller.endVector)
        linktocaller.startVector=None
        userData=None
        linktocaller.mouseToArrowDiff=0.0
        linktocaller.scaleLBL.setText("scale= ")
        #TODO : We should redraw the arrows here. 
        linktocaller.resizeArrowWidgets()

        return 1  #we eat the event no more widgets should get it 
     
    except Exception as err:
        App.Console.PrintError("'callback release' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def callback_move(userData:fr_arrow_widget.userDataObject=None):
    try:
        if userData==None : 
            return # Nothing to do here - shouldn't be None 
    
        ArrowObject= userData.ArrowObj
        events=userData.events
        linktocaller= userData.callerObject
        if type(events)!=int:
            return    
        
        clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                          ArrowObject.w_pick_radius, ArrowObject.w_widgetSoNodes)
        clickwdglblNode = fr_coin3d.objectMouseClick_Coin3d(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                           ArrowObject.w_pick_radius, ArrowObject.w_widgetlblSoNodes) 
        linktocaller.endVector=App.Vector(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                              ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                              ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        if clickwdgdNode == None and clickwdglblNode==None:
            if linktocaller.run_Once==False:
                return 0  # nothing to do 
                
        if linktocaller.run_Once==False:
            linktocaller.run_Once=True
            if ArrowObject.w_color== FR_COLOR.FR_OLIVEDRAB:
                linktocaller.mouseToArrowDiff=ArrowObject.w_vector.y-linktocaller.endVector.y
            elif ArrowObject.w_color== FR_COLOR.FR_RED:
                linktocaller.mouseToArrowDiff=ArrowObject.w_vector.y-linktocaller.endVector.x
            elif ArrowObject.w_color== FR_COLOR.FR_RED:
                linktocaller.mouseToArrowDiff=ArrowObject.w_vector.z-linktocaller.endVector.z
            
            
            linktocaller.startVector=linktocaller.endVector # Keep the old value only first time when drag start
            if not ArrowObject.has_focus():
                ArrowObject.take_focus()

        scale=1.0
        newPos=App.Vector(0.0,0.0,0.0)
        
        if ArrowObject.w_color==FR_COLOR.FR_OLIVEDRAB:
            #x direction only
            ArrowObject.w_vector.y=linktocaller.endVector.y-linktocaller.mouseToArrowDiff
            scale=linktocaller.endVector.y-linktocaller.startVector.y
        elif ArrowObject.w_color==FR_COLOR.FR_RED:
            ArrowObject.w_vector.x=linktocaller.endVector.x-linktocaller.mouseToArrowDiff
            scale=linktocaller.endVector.x-linktocaller.startVector.x
        elif ArrowObject.w_color==FR_COLOR.FR_BLUE:
            ArrowObject.w_vector.z=linktocaller.endVector.z-linktocaller.mouseToArrowDiff
            scale=linktocaller.endVector.z-linktocaller.startVector.z

        linktocaller.scaleLBL.setText("scale= "+str(1+(scale)/SCALE_FACTOR))

        linktocaller.smartInd[0].redraw()
        linktocaller.smartInd[1].redraw()
        linktocaller.smartInd[2].redraw()
        return 1 #we eat the event no more widgets should get it

    except Exception as err:
        App.Console.PrintError("'callback' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

class Design456_DirectScale:
    """
    Direct scaling of any 3D Object by draging either uniform arrow or
    un-uniform arrows.
    """
    mw=None
    dialog=None
    tab=None
    smartInd=[]
    _mywin=None
    b1=None
    scaleLBL=None
    run_Once=False 
    endVector=None
    startVector=None
    selectedObj=None
    mouseToArrowDiff=0.0
    
    def getObjectLength(self):
        return(self.selectedObj.Shape.BoundBox.XLength,
               self.selectedObj.Shape.BoundBox.YLength,
               self.selectedObj.Shape.BoundBox.ZLength)
        
    def returnVectorsFromBoundaryBox(self):
        try:
            #Max object length in all directions        
            (lengthX,lengthY,lengthZ)= self.getObjectLength()

            #Make the start 2 mm before the object is placed
            startX= self.selectedObj.Shape.BoundBox.XMin
            startY= self.selectedObj.Shape.BoundBox.YMin
            startZ= self.selectedObj.Shape.BoundBox.ZMin
            EndX=self.selectedObj.Shape.BoundBox.XMax
            EndY=self.selectedObj.Shape.BoundBox.YMax
            EndZ=self.selectedObj.Shape.BoundBox.ZMax
            p1: App.Vector=None
            p2: App.Vector=None
            _vectors: List[App.Vector] = []

            leng=[]
            leng.append(lengthX)
            leng.append(lengthY)
            leng.append(lengthZ)
            
            p1=App.Vector(startX+lengthX/2,EndY+lengthY,startZ+lengthZ/2)
            p2=App.Vector(EndX+lengthX,startY+lengthY/2,startZ+lengthZ/2)
            p3=App.Vector(startX+lengthX/2,startY+lengthY/2,EndZ+lengthZ)
            
            _vectors.append(p1)
            _vectors.append(p2)
            _vectors.append(p3)
            return (_vectors,leng)

        # we have a self.selectedObj object. Try to show the dimensions. 
        except Exception as err:
            App.Console.PrintError("'Design456_DirectScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def createArrows(self):
        try:    
            (_vec, length)=self.returnVectorsFromBoundaryBox()

            self.smartInd.clear()

            rotation=(0.0,0.0,0.0,0.0)
            self.smartInd.append(Fr_Arrow_Widget(_vec[0],"X-Axis",1,FR_COLOR.FR_OLIVEDRAB,rotation))
            self.smartInd[0].w_callback_= callback_release
            self.smartInd[0].w_move_callback_=callback_move      #External function
            self.smartInd[0].w_userData.callerObject=self

            rotation=(0.0,0.0,-1.0,math.radians(57))
            self.smartInd.append(Fr_Arrow_Widget(_vec[1],"Y-Axis",1,FR_COLOR.FR_RED,rotation))
            self.smartInd[1].w_callback_=callback_release
            self.smartInd[1].w_move_callback_=callback_move
            self.smartInd[1].w_userData.callerObject=self
            
            rotation=(1.0,0.0 ,0.0,math.radians(57))
            self.smartInd.append(Fr_Arrow_Widget(_vec[2],"Z-Axis",1,FR_COLOR.FR_BLUE,rotation))
            self.smartInd[2].w_callback_=callback_release
            self.smartInd[2].w_move_callback_=callback_move
            self.smartInd[2].w_userData.callerObject=self

        # we have a self.selectedObj object. Try to show the dimensions. 
        except Exception as err:
            App.Console.PrintError("'Design456_DirectScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

                    
    def Activated(self):
        try:
            sel = Gui.Selection.getSelection()
            if len(sel) != 1:
                # Only one object must be self.selectedObj
                errMessage = "Select one object to scale"
                faced.getInfo().errorDialog(errMessage)
                return 
            self.selectedObj=sel[0]
            if not hasattr(self.selectedObj,'Shape'):
                # Only one object must be self.selectedObj
                errMessage = "self.selectedObj object has no Shape,\n please make a simple copy of the object"
                faced.getInfo().errorDialog(errMessage)
                return 
            
            (self.mw,self.dialog, self.tab)=faced.createActionTab("Direct Scale").Activated()
            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("(Direct Scale)\nFor quicker\nresizing any\n3D Objects")
            self.scaleLBL= QtGui.QLabel("Scale=")
            commentFont=QtGui.QFont("Times",12,True)
            self.b1 = QtGui.QPushButton("Uniform")
            BUTTON_SIZE = QtCore.QSize(100, 100)
            self.b1.setMinimumSize(BUTTON_SIZE)
            self.b1.setStyleSheet("background: orange;")
            self.b1.setCheckable(True)
            self.b1.toggle()
            self.b1.clicked.connect(lambda:self.whichbtn(self.b1))
            self.b1.clicked.connect(self.btnState)
            la.addWidget(self.b1)
            e1.setFont(commentFont)
            self.scaleLBL.setFont(commentFont)
            la.addWidget(e1)
            la.addWidget(self.scaleLBL)
            self.okbox = QtGui.QDialogButtonBox(self.dialog)
            self.okbox.setOrientation(QtCore.Qt.Horizontal)
            self.okbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
            la.addWidget(self.okbox)
            QtCore.QObject.connect(self.okbox, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QObject.connect(self.okbox, QtCore.SIGNAL("rejected()"), self.hide)
                        
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            
            self.createArrows()
            
            #set self.selectedObj object to each smartArrow 
            if self._mywin==None :
                self._mywin=win.Fr_CoinWindow()
            self._mywin.addWidget(self.smartInd)
            self._mywin.show()

        # we have a self.selectedObj object. Try to show the dimensions. 
        except Exception as err:
            App.Console.PrintError("'Design456_DirectScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        self.dialog.hide()
        del self.dialog
        dw=self.mw.findChildren(QtGui.QDockWidget)
        newsize=self.tab.count()    #Todo : Should we do that?
        self.tab.removeTab(newsize-1) # it is 0,1,2,3 ..etc    
        self.__del__()  # Remove all smart scale 3dCOIN widgets

    def  btnState(self):
        if self.b1.isChecked():
            self.b1.setText("Uniform")
            print ("button pressed")
        else:
            self.b1.setText("None Uniform")
            print ("button released")
            
    def whichbtn(self,b1):
        if b1.text()=='Uniform':
            b1.setStyleSheet("background: yellow;");
        else: 
            b1.setStyleSheet("background: orange;");
    
    def resizeArrowWidgets(self):
        """
        Reposition the arrows by recalculating the boundary box
        and updating the vectors inside each fr_arrow_widget
        """
        (_vec, length)=self.returnVectorsFromBoundaryBox()
        self.smartInd[0].w_vector=_vec[0]
        self.smartInd[1].w_vector=_vec[1]
        self.smartInd[0].w_vector=_vec[2]
        for wdg in self.smartInd:
            wdg.redraw()
        return
    def __del__(self):
        """
        Remove all widget from Fr_CoinWindow and from the senegraph
        """
        try:
            if type(self.smartInd)==list:
                for i in self.smartInd:
                    i.hide()
                    i.__del__()
                    del i  # call destructor
            else:
                self.smartInd.hide()
                self.smartInd.__del__()
                del self.smartInd
                
            if self._mywin!=None:
                self._mywin.hide()
                del self._mywin
                self._mywin=None
                
        except Exception as err:
            App.Console.PrintError("'Design456_SmartScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)    
    
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH +'DirectScale.svg',
            'MenuText': 'Direct Scale',
                        'ToolTip':  'Direct Scale'
        }

Gui.addCommand('Design456_DirectScale', Design456_DirectScale())