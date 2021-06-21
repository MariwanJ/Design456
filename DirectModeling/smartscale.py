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
from pivy import coin
import FACE_D as faced
import math as _math
from PySide.QtCore import QT_TRANSLATE_NOOP
import ThreeDWidgets.fr_line_widget as wlin
import ThreeDWidgets.fr_coinwindow  as win
from typing import List
import time 
import Design456Init

def smartLinecallback(smartLine,obj,parentlink):
    """
        Calback when line is clicked
    """    
    print("callback")   
    
def smartlbl_callback(smartLine,obj,parentlink):
    """
        callback when label is double clicked
    """
    print("smartline lbl callback") 
    print(obj)  
    print(parentlink)
    #clone the object
    p1=smartLine.w_vector[0]
    p2=smartLine.w_vector[1]
    deltaX=p2.x-p1.x
    deltaY= p2.y-p1.y
    deltaZ=p2.z-p1.z
    side=None
    oldv=0.0
    if deltaX==0 and deltaZ==0:
        side= 'y'
        oldv=deltaY
        print("scale y axis")
    elif deltaY==0.0 and deltaZ==0.0:
        side='x'
        oldv=deltaX
        print("scale x axis")
    elif deltaY==0.0 and deltaX==0.0 and deltaZ!=0.0:
        side='z'
        oldv=deltaZ
        print("scale z axis")

    newValue=0
    
    #all lines has a 4 mm more size due to the way we calculate them. Remove that
    newValue=faced.GetInputValue(oldv).getDoubleValue()
    if newValue==0:
        #User canceled the value
        return

    if obj==None:
        # Only one object must be selected
        errMessage = "Select an object to scale"
        faced.getInfo().errorDialog(errMessage)
        return
    print("object=",obj)
    print("objectname=",obj.Name)
    cloneObj = Draft.clone(obj, forcedraft=True)
    #scaled_list = scale(objectslist, scale=Vector(1,1,1), center=Vector(0,0,0), copy=False)
    scaleX=1
    scaleY=1
    scaleZ=1    

    if side=='y':
        scaleY=newValue/deltaY
        smartLine.w_vector[1].y=smartLine.w_vector[1].y+(newValue-deltaY)
    elif side=='x':
        scaleX=newValue/deltaX
        smartLine.w_vector[1].x=smartLine.w_vector[1].x+(newValue-deltaX)
    elif side=='z':
        scaleZ=newValue/deltaZ
        smartLine.w_vector[1].z=smartLine.w_vector[1].z+(newValue-deltaZ)
    else : 
        print("error")
    smartLine.changeLabelfloat(newValue)
    try:
        cloneObj.Scale=App.Vector(scaleX,scaleY,scaleZ)
        cloneObj.Placement=obj.Placement

        obj.Visibility=False
        App.ActiveDocument.recompute()
        _name=obj.Label
        obj.Label=obj.Label+"old"
        __shape = Part.getShape(cloneObj,'',needSubElement=False,refine=False)
        _simpleCopy=App.ActiveDocument.addObject('Part::Feature',_name)
        _simpleCopy.Shape=__shape
        App.ActiveDocument.recompute()
        App.ActiveDocument.removeObject(obj.Name)
        App.ActiveDocument.removeObject(cloneObj.Name)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(_simpleCopy)
        #All objects must get link to the new targeted object
        for i in parentlink.smartInd:
            i.set_target(_simpleCopy)
        App.ActiveDocument.recompute()
        smartLine.redraw()        #Update the vertices here 
        
           
    except Exception as err:
        App.Console.PrintError("'Design456_SmartScale' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


class smartLines(wlin.Fr_Line_Widget):
    """
        A subclass of fr_line_widget used to show 
        the length,width and height of the selected
        object for scaling. 
    """
    def __init__(self, vectors: List[App.Vector] = [], label: str = "", lineWidth=1,linkToParent=None):
        super().__init__(vectors, label,lineWidth)     #Must be done first as described in fr_line_widget
        self.w_lbl_calback_=smartlbl_callback
        self.w_callback_=smartLinecallback
        self.targetObject=None
        self._parentLink=linkToParent  #this hold the command class. used to reproduce the whole object.
 
    def do_callback(self):
        """ Do widget callback"""
        self.w_callback_(self,self.targetObject,self._parentLink)
        
    def do_lblcallback(self):
        """ Do label callaback"""
        self.w_lbl_calback_(self,self.targetObject,self._parentLink)

    def set_target(self,target):
        """ Set target object"""
        self.targetObject=target

class Design456_SmartScale:
    _mywin=None
    smartInd=[]
    
    def getXYZdimOfSelectedObject(self,selected):
        print("create smart lines with xyz calculation")
        try:
            #Max object length in all directions        
            lengthX =selected.Shape.BoundBox.XLength
            lengthY =selected.Shape.BoundBox.YLength
            lengthZ =selected.Shape.BoundBox.ZLength

            #Make the end 10 mm longer/after the object
            NewX= selected.Shape.BoundBox.XMax+2
            NewY= selected.Shape.BoundBox.YMax+2
            NewZ= selected.Shape.BoundBox.ZMax+4

            #Make the start 10 mm before the object is placed
            startX= selected.Shape.BoundBox.XMin-2
            startY= selected.Shape.BoundBox.YMin-2
            startZ= selected.Shape.BoundBox.ZMin

            if self._mywin!=None :
                try: 
                    del self._mywin
                    self._mywin=None
                except:
                    self._mywin=None

            self._mywin=win.Fr_CoinWindow()
            Xvectors: List[App.Vector] = []
            Yvectors: List[App.Vector] = []
            Zvectors: List[App.Vector] = []

            Yvectors.append(App.Vector(startX,NewY,0))
            Yvectors.append(App.Vector(NewX,NewY,0))
    
            Xvectors.append(App.Vector(NewX,startY,0))
            Xvectors.append(App.Vector(NewX,NewY,0))

            Zvectors.append(App.Vector(NewX,NewY,startZ))
            Zvectors.append(App.Vector(NewX,NewY,NewZ))

            #Create the lines
            self.smartInd.append(smartLines(Xvectors,"{0:.2f}".format(lengthX),5,self))
            self.smartInd.append(smartLines(Yvectors,"{0:.2f}".format(lengthY),5,self))
            self.smartInd.append(smartLines(Zvectors,"{0:.2f}".format(lengthZ),5,self))

            for i in self.smartInd:
                i.set_target(selected)

            #set selected object to each smartline 
            print( "Selected object is ")
            print(selected.Name)

            self._mywin.addWidget(self.smartInd)
            
            self._mywin.show()     

        except Exception as err:
            App.Console.PrintError("'Design456_SmartScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        try:
            select = Gui.Selection.getSelection()
            if len(select) != 1:
                # Only one object must be selected
                errMessage = "Select one object to scale"
                faced.getInfo().errorDialog(errMessage)
                return
            self.getXYZdimOfSelectedObject(select[0])
            wait=faced.Ui_WaitForOK()
            resu=wait.Activated()
            #while resu.isVisible:
            #    time.sleep(0.1)
        # we have a selected object. Try to show the dimensions. 
        except Exception as err:
            App.Console.PrintError("'Design456_SmartScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """ 
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        try:
            for i in self.smartInd:
                i.hide()
                i.__del__()
                del i  # call destructor 
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
            'Pixmap': Design456Init.ICON_PATH +'smartscale.svg',
            'MenuText': 'SmartScale',
                        'ToolTip':  'Smart Scale'
        }

Gui.addCommand('Design456_SmartScale', Design456_SmartScale())

class Design456_DirectScale:

    def Activated(self):
        try:
            sel = Gui.Selection.getSelection()
            if len(sel) != 1:
                # Only one object must be selected
                errMessage = "Select one object to scale"
                faced.getInfo().errorDialog(errMessage)
                return 
                
        # we have a selected object. Try to show the dimensions. 
        except Exception as err:
            App.Console.PrintError("'Design456_DirectScale' Failed. "
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