# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft  as _draft
import Part  as _part
from pivy import coin

from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide

def getDirectionAxis():
    try:
        s = Gui.Selection.getSelectionEx()
        if len(s)==0:
            return "" #nothing to do we cannot calculate the direction
        obj = s[0]
        if (hasattr(obj,"SubObjects")):
            if len(obj.SubObjects)!=0:
                faceSel = obj.SubObjects[0]
            else:
                faceSel=obj.Object.Shape.Faces[0] # Take the first face
        else:
            raise NotImplementedError
        try: 
            dir = faceSel.normalAt(0, 0)  #other faces needs 2 arguments
        except: 
            try: 
                dir= faceSel.normalAt(0) #Circle has not two arguments, only one
            except:
                f= findFacehasSelectedEdge()
                if f==None:
                    raise Exception ("Face not found")
                dir= f.normalAt(0, 0)
        
        if dir.z == 1:
            return "+z"
        elif dir.z==-1:
            return "-z"
        elif dir.y == 1:
            return "+y"
        elif dir.y==-1:
            return "-y"
        elif dir.x==1:
            return "+x"
        elif dir.x==-1:
            return "-x"
        else:
            return None 
    except Exception as err:
        App.Console.PrintError("'getDirectionAxis' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

class MousePosition:
    def __init__(self, view):
        self.view = view
        v = Gui.activeDocument().activeView()

    def getPosition(self, info):
        try:
            down = (info["State"] == "DOWN")
            pos = info["Position"]
            # if (down):
            App.Console.PrintMessage(
                "Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
            pnt = self.view.getPoint(pos)
            App.Console.PrintMessage(
                "World coordinates: " + str(pnt) + "\n")
            info = self.view.getObjectInfo(pos)
            App.Console.PrintMessage("Object info: " + str(info) + "\n")
            o = self.ViewObserver(self.v)
            c = self.v.addEventCallback("SoMouseButtonEvent", o.logPosition)
            return pnt
        except Exception as err:
            App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class mousePointMove:
    def __init__(self,obj,view):
        self.object = obj
        self.view = view
        self.callbackClicked = self.view.addEventCallbackPivy (coin.SoMouseButtonEvent.getClassTypeId(), self.mouseClick) #"SoLocation2Event"
        self.callbackMove = self.view.addEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(), self.mouseMove)
        StartMovePoint=0
        
    def convertToVector(self,pos):
        try:
            import Design456Init
            point=None
            tempPoint=self.view.getPoint(pos[0], pos[1])        
            if Design456Init.DefaultDirectionOfExtrusion=='x':        
                point= App.Vector(0.0,tempPoint[0],tempPoint[1]) 
            elif Design456Init.DefaultDirectionOfExtrusion=='y':
                point=App.Vector(tempPoint[0],0.0,tempPoint[1]) 
            elif Design456Init.DefaultDirectionOfExtrusion=='z':
                point=App.Vector(tempPoint[0],tempPoint[1],0.0)
            return point
        except Exception as err:
                App.Console.PrintError("'converToVector' Failed. "
                                       "{err}\n".format(err=str(err)))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
        

    def mouseMove(self,events):
        try:
            event = events.getEvent()
            pos = event.getPosition().getValue()
            point=self.convertToVector(pos)
            points=self.object.Object.Points
            #lastPoint=  point  
            self.object.Object.End=point
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Extend' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def mouseClick(self, events):
        try:
            import Design456Init
            event = events.getEvent()
            eventState= event.getState()
            getButton= event.getButton() 
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON1:
                pos=event.getPosition()
                point=self.convertToVector(pos)
                print('Mouse click \n')
                _point= self.object.Object.Points
                _point[len(_point)-1] = point
                #self.object.Object.End= point 
                App.ActiveDocument.recompute()
                self.remove_callbacks()
                
        except Exception as err:
            App.Console.PrintError("'converToVector' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        except Exception as err:
            App.Console.PrintError("'Mouse click ' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return None

    def remove_callbacks(self):
        try:
            print('Remove MouseClick callback')
            self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClicked)
            self.view.removeEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
            
        except Exception as err:
            App.Console.PrintError("'Mouse move point' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class PartMover:
    def __init__(self, view, obj, deleteOnEscape):
        self.obj = obj
        self.initialPosition = self.obj.Placement.Base
        self.view = view
        self.deleteOnEscape = deleteOnEscape
        self.callbackMove = self.view.addEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(), self.moveMouse)
        self.callbackClick = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.MouseClick)
        self.callbackKey = self.view.addEventCallbackPivy(coin.SoKeyboardEvent.getClassTypeId() , self.KeyboardEvent)
        self.objectToDelete = None  # object reference when pressing the escape key
        self.Direction =None
        
    def convertToVector(self,pos):
        try:
            import Design456Init
            
            tempPoint=self.view.getPoint(pos[0], pos[1])    
            if(self.Direction==None):
                if Design456Init.DefaultDirectionOfExtrusion=='x':        
                    point=( App.Vector(0.0,tempPoint[0],tempPoint[1]) )
                elif Design456Init.DefaultDirectionOfExtrusion=='y':
                    point=(App.Vector(tempPoint[0],0.0,tempPoint[1])) 
                elif Design456Init.DefaultDirectionOfExtrusion=='z':
                    point=(App.Vector(tempPoint[0],tempPoint[1],0.0))
            else:
                
                if (self.Direction=='X'):
                    point=( App.Vector(tempPoint[0],self.obj.Placement.Base.y,self.obj.Placement.Base.z))
                elif (self.Direction=='Y'):
                    point=( App.Vector(self.obj.Placement.Base.x,tempPoint[1],self.obj.Placement.Base.z))
                elif (self.Direction=='Z'):
                    point=( App.Vector(self.obj.Placement.Base.x,self.obj.Placement.Base.y,tempPoint[0]))
            return point     
            
        except Exception as err:
            App.Console.PrintError("'Mouse click error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
        
    def moveMouse(self, events):
        try:
            self.active=True
            event = events.getEvent()
            newPos = self.convertToVector(event.getPosition().getValue())
            self.obj.Placement.Base = newPos
            self.newPosition = newPos
        except Exception as err:
            App.Console.PrintError("'Mouse movements error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def remove_callbacks(self):
        try:
            print('Remove callback')
            self.view.removeEventCallbackPivy (coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
            self.view.removeEventCallbackPivy (coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
            self.view.removeEventCallbackPivy (coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)
            self.active = False
            self.info = None
            self.view = None
        except Exception as err:
            App.Console.PrintError("'remove callback error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def MouseClick(self, events):
        try:
            import Design456Init
            event = events.getEvent()
            eventState= event.getState()
            getButton= event.getButton() 
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON1:
                pos=event.getPosition()
                point=self.convertToVector(pos)
                newPos = point
                self.obj.Placement.Base = newPos
                self.obj = None
                App.ActiveDocument.recompute()
                self.remove_callbacks()
            return
        except Exception as err:
            App.Console.PrintError("'Mouse click error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def KeyboardEvent(self, events):
        try:
            event = events.getEvent()
            eventState=event.getState()
            if (type(event) == coin.SoKeyboardEvent):
                key = event.getKey()
            
            if key == coin.SoKeyboardEvent.X and eventState== coin.SoButtonEvent.UP:
                self.Direction='X'
            if key == coin.SoKeyboardEvent.Y and eventState== coin.SoButtonEvent.UP:
                self.Direction='Y'
            if key == coin.SoKeyboardEvent.Z and eventState== coin.SoButtonEvent.UP:
                self.Direction='Z'
                
            if key == coin.SoKeyboardEvent.ESCAPE and eventState== coin.SoButtonEvent.UP:
                self.remove_callbacks()
                if not self.deleteOnEscape:
                    self.obj.Placement.Base = self.initialPosition
                else:
                    # This can be asked by a timer in a calling func...
                    self.objectToDelete = self.obj
                App.ActiveDocument.removeObject(self.obj.Name)
                self.obj = None
                
        except Exception as err:
            App.Console.PrintError("'Keyboard error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
#TODO: This class must be updated to be able to move all kind of objects
#    Mariwan


""" This class will return back info about the selected
    face. Many options are available but
    I will put only what I need at the moment. 
    See the notes below for available info
    Give the class object Gui.Selection()[No] where No is the face you want to get info

"""


def getFaceName(sel):
    try:
        if(hasattr(sel,'SubElementNames')):
            Result = (sel.SubElementNames[0])
            return Result
        else:
            return None
    except Exception as err:
        App.Console.PrintError("'getFaceName' Failed. "
                               "{err}\n".format(err=str(err)))

#TODO Remove this.. not necessary. 
def getObjectFromFaceName(obj, face_name):
    try:
        faceName=face_name        
        if(obj.SubElementNames[0].startswith('Face')):
            faceNumber = int(faceName[4:]) -1
        return obj.Object.Shape.Faces[faceNumber]
    
    except Exception as err:
        App.Console.PrintError("'getObjectFromFaceName' Failed. "
                               "{err}\n".format(err=str(err)))        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def getObjectCenterOfMass(obj):
    try:
        Result = obj.SubObjects[0].CenterOfMass
        return Result
    except Exception as err:
        App.Console.PrintError("'getObjectCenterOfMass' Failed. "
                               "{err+}\n".format(err=str(err)))

def errorDialog( msg):
    # Create a simple dialog QMessageBox
    # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question}
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Error', msg)
    diag.setWindowModality(QtCore.Qt.ApplicationModal)
    diag.exec_()

# From Mario Macro_CenterCenterFace at
# https://wiki.freecadweb.org/Macro_CenterFace/fr
def objectRealPlacement3D(obj):    # search the real Placement
    try:
        objectPlacement = obj.Object.Shape.Placement
        objectPlacementBase = App.Vector(objectPlacement.Base)
        ####
        objectWorkCenter = objectPlacementBase
        ####
        if hasattr(obj, "getGlobalPlacement"):
            globalPlacement = obj.Object.getGlobalPlacement()
            globalPlacementBase = App.Vector(globalPlacement.Base)
            ####
            objectRealPlacement3D = globalPlacementBase.sub(
                objectWorkCenter)  # mode=0 adapte pour BBox + Centerpoints
            ####
        else:
            objectRealPlacement3D = objectWorkCenter
        return objectRealPlacement3D
    except Exception as err:
        App.Console.PrintError("'Magnet' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return getObjectCenterOfMass(obj)

#send object to this class you get back top-face's name  
class SelectTopFace: 
    def __init__(self, obj):
          self.obj = obj
          self.name_facename=""
          
    def Activated(self):
        try:
            if self.obj==None:
                return
            counter = 1
            centerofmass = None
            Highest = 0
            Result=0
            for fac in self.obj.Shape.Faces:
                if(fac.CenterOfMass.z > Highest):
                    Highest = fac.CenterOfMass.z
                    centerofmass = fac.CenterOfMass
                    Result = counter
                counter = counter+1
            self._facename = 'Face'+str(Result)
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(App.ActiveDocument.Name, self.obj.Name,self._facename, centerofmass.x, centerofmass.y, centerofmass.z)
            return self._facename
        except Exception as err:
            App.Console.PrintError("'SelectTopFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return self.obj.SubObjects[0].CenterOfMass

#TODO: Transparent dialog? how to? i.e. border less, only input widgets should be shown?
class GetInputValue:
    def __init__(self,defaultValue=0.0):
        self.value=defaultValue
        pass
    """
    get Input value from user. Either Text, INT or Float
    """
    def getIntValue(self):
        valueDouble,ok= (QtGui.QInputDialog.getInt(None, "Input new Value", "Change size:", self.value, -10000, 10000))
        if ok:
            return float(valueDouble)
        else:
            return None
        
    def getTextValue(self):
        text, ok = QtGui.QInputDialog.getText(None,'Input new Value', 'Change size:')
        if ok:
            return str(text)
        else:
            return None
            
    def getDoubleValue(self):
        valueDouble,ok= (QtGui.QInputDialog.getDouble(None, 'Input new Value', 'Change size:', self.value, -10000.0, 10000.0, 2))
        if ok:
            return float(valueDouble)
        else:
            return None
    
    def Activated(self):
        text, ok = QtGui.QInputDialog.getText(None,'Input new Value', 'Change size')
        if ok:
            return str(text)
        else:
            return None

#Visual progress indicator     
class StatusBarProgress:
    """
    Visual progress indicator. 
    Use this class to visually show the progress 
    of a process you are implementing. 
    Or it could be used also with Wizard widget
    as step indicator
    Use stop to stop the progress. 
    Use stepUp   to step Up   the progress indicator
    Use stepDown to step down the progress indicator
    """
    progress_bar=None
    def __init__(self,title="",Steps=10):
        self.ProgressTitle=title
        self.NoOfsteps=Steps
            
    def Activated(self):
        progress_bar = App.Base.ProgressIndicator()
         
    def start(self):
        self.progress_bar.start(self.ProgressTitle,9) 
    
    def stepUp(self):
        self.progress_bar.next()
    
    def stepDown(self):
        self.progress_bar.prev()
    def stopProgress(self):   
        self.progress_bar.stop() 
    
class createActionTab:
    def __init__(self,Title):
        self.title=Title
        self.mw=None
        self.dw=None
        self.dialog=None
    def Activated(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                self.mw=i    
        if self.mw==None:
            raise Exception("No main window found")
        dw=self.mw.findChildren(QtGui.QDockWidget)
        for i in dw:
            if str(i.objectName()) == "Combo View":
                self.tab= i.findChild(QtGui.QTabWidget)
            elif str(i.objectName()) == "Python Console":
                self.tab= i.findChild(QtGui.QTabWidget)
        if self.tab==None:
                raise Exception ("No tab widget found")
        self.dialog=QtGui.QDialog()
        oldsize=self.tab.count()
        self.tab.addTab(self.dialog,self.title)
        self.tab.setCurrentWidget(self.dialog)
        self.dialog.setWindowTitle(self.title)
        return (self.mw,self.dialog,self.tab)

def findFacehasSelectedEdge():
    """[Find Face that has the selected edge]
    Returns:
        [Face Object]: [Return the face has the selected edge or None if error occur]
    """
    obj=Gui.Selection.getSelectionEx()[0]
    edge=obj.SubObjects[0]
    Faces=obj.Object.Shape.Faces
    for fa in Faces: 
        for ed in fa.Edges:
            if edge.isEqual(ed):
            #if edge.isPartner(ed):
                return fa
    return None

def findFaceSHavingTheSameEdge():
    """[Find Faces that have the selected edge]
    Returns:
        [Face Objects]: [Return the faces have the selected edge or None if error occur]
    """
    s = Gui.Selection.getSelectionEx()[0]
    edge = s.SubObjects[0]
    shape = s.Object.Shape
    return shape.ancestorsOfType(edge, Part.Face)

def findnormalAtforEdge():
    """[Find Directions of an edge]

    Returns:
        [(float,float,float)]: [Returns the results of normalAt for the faces containing the edge.]
    """
    results=[]
    
    for f in findFacehasSelectedEdge():
        u0, u1, v0, v1 = f.ParameterRange
        results.append(f.normalAt(0.5 * (u0 + u1), 0.5 * (v0 + v1)))
    return results

def getDirectionOfFace():
    """[Find direction of a face]

    Returns:
        [Vector]: [Direction of the face]
    """
    selectedObj=Gui.Selection.getSelectionEx()[0]
    ss=None
    direction=None
    if hasattr(selectedObj,"SubObjects"):
        ss=selectedObj.SubObjects[0]
    else:
        #TODO: FIXME: WHAT SHOULD WE USE?
        print("failed")
    if ss!=None:
        # section direction
        yL = ss.CenterOfMass
        uv = ss.Surface.parameter(yL)
        nv = ss.normalAt(uv[0], uv[1])
        direction = yL.sub(nv + yL)
    return direction

def distanceBetweenTwoVectors(p1=App.Vector(0,0,0) , p2=App.Vector(10,10,10) ):
    """[summary]

    Args:
        p1 ([FreeCAD.Vector], optional): [description]. Defaults to App.Vector(0,0,0).
        p2 ([FreeCAD.Vector], Required): [description]. Defaults to App.Vector(10,10,10).

    Returns:
        [float]: [Deistance measured between the two vertices]
    """
    results = p1.distanceToPoint(p2)
    return results