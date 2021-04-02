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

"""
This file will contain all event, handle, constants related to the interactive
part of the new widgets. It will keeps the events and translate them
to the desired standardized names.
Events will be defined here, mouse position will be saved here, last event..etc.
To understand how I think in making this widgets, please consider reading about
the FLTK toolkit. This is a flavour of https://www.fltk.org/.
Notice that we have two different windows system. One is for the Coin3D and 
the other is for QT Widget. 
That is why you will see different definitions here for each system.
"""
#Struct to keep the mouse position in both world
@dataclass
class mouseDimension:
    global Coin_x 
    global Coin_y 
    global Coin_z 
    global Qt_x   
    global Qt_y   
    global pos  
    
#get Object under mouse
def objectUMouse_Coin3d(self,win):
    pass
#get Object clicked in COIN3D

def objectCMouse_Coin3d():
    #This section is from DRAFT
    #It must help in finding the correct node 
    #which represent the widget.
    def __init__(self, mouse_pos):
        self.mouse_pos=mouse_pos

    def getEditNode(self):
        """Get edit node from given screen position."""
        node = self.sendRay()
        return node

    def sendRay(self):
        """Send a ray through the scene and return the nearest entity."""
        try:
            viewer = Gui.ActiveDocument.ActiveView.getViewer()
            render_manager = viewer.getSoRenderManager()
            ray_pick = coin.SoRayPickAction(render_manager.getViewportRegion())
            ray_pick.setPoint(coin.SbVec2s(*self.mouse_pos))
            ray_pick.setRadius(self.pick_radius)
            ray_pick.setPickAll(True)
            ray_pick.apply(render_manager.getSceneGraph())
            picked_point = ray_pick.getPickedPoint()
            return self.searchEditNode()

        except Exception as err:
            App.Console.PrintError("'SplitObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def searchEditNode(self):
        """Search edit node inside picked point list and return node ."""
        try:
            if self.picked_point !=None and self.picked_point!= 0: 
                path = self.picked_point.getPath()
                pickedNode = path.getTail()       
                return pickedNode
        except Exception as err:
            App.Console.PrintError("'SplitObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class root_handle():
    """
        The most critical part of the widgets. This will take care of 
        translating the events from COIN3D to our system.
        Bot QT and COIN3D windows will call this function.
        But they will be treated differently as they are different.
    """
    
    #Save last mouse event
    global lastEvent 
    #Save last keyboard event
    global lastKeyEvent
    
    # This should keep the mouse pointer position on the 3D view
    global lastEventXYZ 
    
    def __init__(self, events, WindowsType, window ):
        self.events=events
        self.WindowsType=WindowsType
        self.wind= window  
        self.lastEventXYZ = mouseDimension()    
    if self.WindowsType==COIN3D:
        try:    
            # write down all possible events.
            #First mouse move event
            get_event = self.events.getEvent()

            if(type(get_event)==coin.SoGestureEvent)             :
                """  represents a series of touch events  """
                raise NotImplementedError()     #will not be uses at least now 2021-04-02
            
            if(type(get_event)==coin.SoMotion3Event)             :
                """ represents 3D relative motion events in the 
                   Open Inventor event model.
                    sub functions: 
                    getTranslation()          # Gets the relative change in translation since the last translation event.
                    setRotation(SbRotation r) # Sets the relative change in rotation since the last rotation event.
                    setTranslation(SbVec3f t) # Sets the relative change in translation since the last translation event.
                    SbRotation getRotation()  #Gets the relative change in rotation since the last rotation event.
                """
                raise NotImplementedError()     #will not be uses at least now 2021-04-02
            
            if(type(get_event))==coin.SoTouchEvent               :
                """ A touch event typically represents a user finger action on a touch screen input device"""
                raise NotImplementedError()     #will not be uses at least now 2021-04-02
            
            if(type(get_event))==coin.SoTrackerEvent             :
                """ A "tracker" is any device whose position and orientation are dynamically tracked in 3D"""
                raise NotImplementedError()     #will not be uses at least now 2021-04-02
            
            if(type(get_event)==coin.SoLocation2Event)           :
                """ 2D location events. SoLocation2Event represents 2D location events, for example, mouse move events """
    
            if(type(get_event)==coin.SoMouseWheelEvent)          :
                """  Mouse wheel events. SoMouseWheelEvent represents a change in 
                mouse wheel rotation event in the Open Inventor event model. 
                
                """
                window.handle(fr.FR_MOUSEWHEEL)

                
            if(type(get_event)==coin.SoControllerButtonEvent)    :
                """
                Controller button press and release event. 
                SoControllerButtonEvent represents controller button press and
                release events in the Open Inventor event model.
                A controller device generally has associated 3D tracker information. 
                """
                raise NotImplementedError()     #will not be uses at least now 2021-04-02
            

            if(type(get_event)==coin.SoMouseButtonEvent)         :
                """
                Mouse button press and release events.
                SoMouseButtonEvent represents mouse button press and release
                events in the Open Inventor event model. 
                functions used with this: 
                - getButton()
                - isButtonDoubleClickEvent(SoEvent e, SoMouseButtonEvent.Buttons whichButton)
                - isButtonPressEvent(SoEvent e, SoMouseButtonEvent.Buttons whichButton)
                - isButtonReleaseEvent(SoEvent e, SoMouseButtonEvent.Buttons whichButton)
                - setButton(SoMouseButtonEvent.Buttons b)
                """
                eventState= get_event.getState()  # pressed down , or it is release
                getButton=  get_event.getButton()
                
                self.lastEvent=fr.FR_EVENTS.FR_NO_EVENT
                
                if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON1:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_LEFT_PUSH
                if eventState == coin.SoMouseButtonEvent.up and getButton ==coin.SoMouseButtonEvent.BUTTON1:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_LEFT_RELEASE
                    
                if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON2:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_RIGHT_PUSH
                if eventState == coin.SoMouseButtonEvent.UP and getButton ==coin.SoMouseButtonEvent.BUTTON2:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_RIGHT_RELEASE

                if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON3:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_MIDDLE_PUSH
                if eventState == coin.SoMouseButtonEvent.DOWN and getButton ==coin.SoMouseButtonEvent.BUTTON3:
                    self.lastEvent = constant.FR_EVENTS.MOUSE_MIDDLE_RELEASE
                self.wind.handle(self.lastEvent)



            if(type(get_event)==coin.SoKeyboardEvent)            :
    
            if(type(get_event)==coin.SoSpaceballButtonEvent)     :
                
            if(type(get_event)==coin.SoHandleEventAction)        :


            if(type(get_event)==coin.SoEventCallback)            :

            if(type(get_event)==coin.SoSelection)                :

            if(type(get_event)==coin.SoInteraction)              :

            if(type(get_event)==coin.SoWinDevice)                :

            if(type(get_event)==coin.SoWinRenderArea)            :

            if(type(get_event)==coin.SoGestureEvent)             :





            if(type(get_event)==coin.SoLocation2Event):
                self.lastEventXYZ.pos=get_event.getPosition()
                pos=self.lastEventXYZ.pos.getValue()
                pnt = self.view.getPoint(pos[0],pos[1])
                self.lastEventXYZ.Coin_x = pnt.x
                self.lastEventXYZ.Coin_y = pnt.y
                self.lastEventXYZ.Coin_z = pnt.z
                self.lastEventXYZ.Qt_x = pos[0]
                self.lastEventXYZ.Qt_y = pos[1]
            # Take care of Keyboard events
            elif (type(get_event) == coin.SoKeyboardEvent):
                key = ""
                try:
                    key = get_event.getKey()
                # Take care of CTRL,SHIFT,ALT
                    if (key == coin.SoKeyboardEvent.LEFT_CONTROL or coin.SoKeyboardEvent.RIGHT_CONTROL) and get_event.getState() == coin.SoButtonEvent.DOWN:
                        self.lastKeyEvent.append(key)
                    elif(key == coin.SoKeyboardEvent.LEFT_SHIFT or coin.SoKeyboardEvent.RIGHT_SHIFT) and get_event.getState() == coin.SoButtonEvent.DOWN:
                        self.lastKeyEvent.append(key)
                    elif(key == coin.SoKeyboardEvent.LEFT_ALT or coin.SoKeyboardEvent.RIGHT_ALT) and get_event.getState() == coin.SoButtonEvent.DOWN:
                        self.lastKeyEvent.append(key)
                    # Take care of all other keys.
                    if(get_event.getState() == coin.SoButtonEvent.UP):
                        self.lastKeyEvent.append(key)
                except ValueError:
                    # there is no character for this value
                    key = ""
        except Exception as err:
            App.Console.PrintError("'Extend' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    elif WindowsType==QTWINDOW:
        pass