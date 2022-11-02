# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from typing import List
import FACE_D as faced
from dataclasses import dataclass
from ThreeDWidgets.fr_draw import draw_2Darrow
from ThreeDWidgets import fr_label_draw
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_draw1 import draw_RotationPad
import math

__updated__ = '2022-07-02 20:24:38'


"""
Example how to use this widget.

# show the window and it's widgets.
import ThreeDWidgets.fr_one_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR

class test:
        global runOunce
        def __init__(self):
                self.runOunce = None

        def callback_move(self,userData : wd.userDataObject = None):
     
             PadObj = userData.PadObj  # Arrow object
             click=App.Vector(PadObj.w_parent.w_lastEventXYZ.Coin_x,
                                            PadObj.w_parent.w_lastEventXYZ.Coin_y,
                                            PadObj.w_parent.w_lastEventXYZ.Coin_z)
             if self.runOunce is None:
                   self.runOunce = click.sub(PadObj.w_vector[0])

             PadObj.w_vector[0]=click.sub(self.runOunce)
             
             PadObj.redraw()

             print(self.runOunce,"self.runOunce")

        def runme(self):
                mywin = wnn.Fr_CoinWindow()
                vectors=[App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 0.0)] 
                rot=[0,0,0,0]
                root=wd.Fr_OneArrow_Widget(vectors, "X-Axis")
                root.w_move_callback_=self.callback_move
                root.enableDisc()
                mywin.addWidget(root)
                mywin.show()

a=test()
a.runme()
a=test()

OR another example :

import ThreeDWidgets.fr_one_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR



mywin = wnn.Fr_CoinWindow()
v1=[App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 0.0)] 
v2=[App.Vector(20,0,0), App.Vector(0.0, 0.0, 0.0)] 
r1=wd.Fr_OneArrow_Widget(v1, "X-Axis")
r1.enableDisc()
r2=wd.Fr_OneArrow_Widget(v2, "y-Axis")
r1.enableDisc()
r2.enableDisc()

mywin.addWidget(r1)
mywin.addWidget(r2)
mywin.show()

"""


@dataclass
class userDataObject:
    __slots__ = ['discObj', 'events', 'callerObject', 'Axis_cb',
                 'Disc_cb']

    def __init__(self):
        self.discObj      =   None    # Class/Tool uses
        self.events       =   None    # events - save handle events here
        self.callerObject =   None    # 
        self.Axis_cb       =   False   # Disallow running callback - Arrows
        self.Disc_cb       =   False   # Disallow running callback - discs.
# *******************************CALLBACKS - DEMO *****************************


def callback1(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy XAxis callback")


def callback2(userData: userDataObject = None):
    """
        This function executes when the rotary disc
        angel changed event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy angle changed callback", userData.discObj.w_discAngle)


def callback(userData: userDataObject = None):
    """
        This function executes when lblCallbak 
        or general widget callback occurs
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy callback")

# *************************************************************


class Fr_OneArrow_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a one Degrees disc
    This will be used later to create 3D disc.
    Or it can be used as a single rotate/move widget
    """
    __slots__ =["w_lbluserData",
                "w_widgetType",
                "w_callback_",
                "w_lbl_calback_",
                "w_KB_callback_",
                "w_ArrowAxis_cb_",
                "w_rotary_cb_",
                "Opacity",
                "DrawingType",
                "distanceBetweenThem",
                "axisType",
                "w_wdgsoSwitch",
                "w_ArrowsSeparator",
                "w_discSeparator",
                "w_color",
                "w_rotaryDisc_color",
                "w_selColor",
                "w_Scale",
                "w_inactiveColor",
                "w_userData",
                "w_discAngle",
                "oldAngle",
                "rotationDirection",
                "w_WidgetDiskRotation",
                "w_rotation",
                "w_discEnabled",
                "releaseDragAxis",
                "releaseDragDisc",
                "run_Once",
                "startVector",
                "endVector"]

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]],
                 _axisType: str = 'X',  # Default is X axis and RED color
                 _lblColor=FR_COLOR.FR_WHITE,
                 _axisColor=FR_COLOR.FR_RED,
                 # User controlled rotation.
                 # Face position-direction controlled rotation at creation.
                 # Whole widget rotation
                 _rotation: List[float] = [0.0, 0.0, 0.0, 0.0],
                 _scale: List[float] = [3, 3, 3],
                 _type: int = 1,
                 _opacity: float = 0.0,
                 _distanceBetweenThem: float = 5.0):
        super().__init__(vectors, label)

        self.w_lbluserData = fr_widget.propertyValues()
        self.w_widgetType = constant.FR_WidgetType.FR_ONE_DISC
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard
        # Dummy callback Axis
        self.w_ArrowAxis_cb_ = callback1

        # Dummy callback          disc
        self.w_rotary_cb_ = callback2

        self.Opacity = _opacity
        self.DrawingType = _type
        # Use this to separate the arrows/lbl from the origin of the widget
        self.distanceBetweenThem = _distanceBetweenThem
        self.axisType = _axisType  # X, Y or Z

        self.w_wdgsoSwitch = coin.SoSwitch()
        self.w_ArrowsSeparator = None
        self.w_discSeparator = None

        self.w_color = _axisColor
        self.w_rotaryDisc_color = _axisColor
        self.w_selColor = [i * 1.2 for i in self.w_color]
        self.w_Scale = _scale
        self.w_inactiveColor = [i * 0.7 for i in self.w_selColor]

        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.discObj = self
        self.w_discAngle = 0.0      # Only disc rotation.
        self.oldAngle = 0.0
        self.rotationDirection = 1   # +1 CCW , -1 ACCW

        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.vectors = self.w_vector

        # We must make it higher or it will intersect the object and won't be visible
        # TODO:Check if this works always?
        self.w_lbluserData.vectors[0].x = self.w_lbluserData.vectors[0].x + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].y = self.w_lbluserData.vectors[0].y + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].z = self.w_lbluserData.vectors[0].z + \
            self.distanceBetweenThem
        self.w_lbluserData.labelcolor = _lblColor

        # Use this to save rotation degree of the disk which is the whole widget angle.
        self.w_WidgetDiskRotation = 0.0

        self.w_rotation = _rotation       # Whole onearrow object Rotation

        self.w_discEnabled = False
        self.releaseDragAxis = -1  # Used to avoid running drag code while it is in drag mode
        # -1 no click, 0 mouse clicked, 1 mouse dragging
        self.releaseDragDisc = -1  # Used to avoid running drag code while it is in drag mode
        # -1 no click, 0 mouse clicked, 1 mouse dragging
        self.run_Once = False
        self.startVector=0.0
        self.endVector=0.0

    def handle(self, event):
        """
        This function is responsible for taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """

        self.w_userData.events = event  # Keep the event always here
        if type(event) == int:
            if event == FR_EVENTS.FR_NO_EVENT:
                return 1  # we treat this event. Nothing to do

        # This is for the widgets label - Not the axes label - be aware.
        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)

        # In this widget, we have 2 coin drawings that we need to capture event for them
        clickwdgdNode = []
        # 0 =     Axis movement
        # 1 =     disc Rotation

        clickwdgdNode = [False, False]

        if(self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                 self.w_pick_radius, self.w_ArrowsSeparator) is not None):
            clickwdgdNode[0] = True

        if self.w_discEnabled is True:
            if (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                      self.w_pick_radius, self.w_discSeparator) is not None):
                clickwdgdNode[1] = True

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            # disc's part
            if clickwdgdNode[1] is True:
                # When the discs rotates, we don't accept
                # the arrow dragging. Disk rotation has priority
                if self.releaseDragDisc == 1 or self.releaseDragDisc == 0:
                    self.releaseDragDisc = -1
                    # Release callback should be activated
                    self.do_callbacks(0)
                    return 1
                # Axis's part
            elif clickwdgdNode[0] is True:
                if self.releaseDragAxis == 1 or self.releaseDragAxis == 0:
                    self.releaseDragAxis = -1
                    self.do_callbacks(1)
                    return 1
            else:  # None of them -- remove the focus
                self.remove_focus()
                return 0
        # Mouse first click and then mouse with movement is here
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            # DISC
            if((clickwdgdNode[1] is True) and (self.releaseDragDisc == -1)):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.releaseDragDisc = 0
                self.releaseDragAxis = -1
                self.take_focus()
                return 1
            # DISC
            elif ((clickwdgdNode[1] is True) and (self.releaseDragDisc == 0)):
                self.releaseDragDisc = 1  # Rotation will continue it will be a drag always
                self.releaseDragAxis = -1
                self.take_focus()
                self.cb_discRotate()
                self.do_callbacks(2)  # disc callback
                return 1

            # DISC
            elif self.releaseDragDisc == 1 and (clickwdgdNode[1] is True):
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.cb_discRotate()
                self.do_callbacks(2)        # We use the same callback,
                return 1

            # Axis
            elif ((((clickwdglblNode is not None)
                    or (clickwdgdNode[0] is True))
                   and (self.releaseDragAxis == -1))):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.releaseDragAxis = 0
                self.releaseDragDisc = -1  # Not possible to have rotation while arrow is active
                self.take_focus()
                return 1
            # Axis
            elif (((clickwdgdNode[0] is True) or (clickwdglblNode is not None))
                  and (self.releaseDragAxis == 0)) :
                self.releaseDragAxis = 1  # Drag  will continue, it will be a drag always
                self.releaseDragDisc = -1
                self.take_focus()
                self.do_callbacks(1)
                return 1
            # Axis
            elif self.releaseDragAxis == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_callbacks(1)        # We use the same callback,
                print (self.axisType,"..")
                return 1
        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible for creating the node,
        and draw the disc on the screen. It creates a node for each 
        element and for each disc.
        """
        try:

            if (len(self.w_vector) < 2):
                raise ValueError('Must be 2 vector at least')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that already ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            # TODO: FIXME:
            preRotVal = None
            distance = [0.0, 0.0, 0.0]
            if self.is_visible():
                if self.axisType == 'X':  # XAxis default   RED
                    preRotVal = [0.0, 90.0, 0.0]  # pre-Rotation
                    distance = [self.distanceBetweenThem, 0.0, 0.0]
                elif self.axisType == 'Y':  # YAxis default GREEN
                    preRotVal = [0.0, 90.0, 90.0]  # pre-Rotation
                    distance = [0.0, self.distanceBetweenThem, 0.0]
                elif self.axisType == 'Z':
                    preRotVal = [0.0, 0.0, 0.0]
                    distance = [0.0, 0.0, self.distanceBetweenThem]
                self.w_ArrowsSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x +
                                                                 distance[0],
                                                                 self.w_vector[0].y +
                                                                 distance[1],
                                                                 self.w_vector[0].z + distance[2]),
                                                      # default FR_COLOR.FR_RED
                                                      self.w_color, self.w_Scale,
                                                      self.DrawingType, self.Opacity,
                                                      preRotVal)

                if self.w_discEnabled:
                    preRotValdisc = [self.w_discAngle, 0.0, 90.0]
                    if self.axisType == 'X':  # Xdisc default   RED
                        preRotValdisc = [self.w_discAngle, 0.0, 90.0]
                    elif self.axisType == 'Y':  # YAxis default GREEN
                        preRotValdisc = [self.w_discAngle, 0.0, 0.0]
                    elif self.axisType == 'Z':
                        preRotValdisc = [0.0, 270.0, (-1*self.w_discAngle)]
                    # Hint: def draw_RotationPad(p1=App.Vector(0.0, 0.0, 0.0), color=FR_COLOR.FR_GOLD,
                    # scale=(1, 1, 1), opacity=0, _rotation=[0.0, 0.0, 0.0]):
                    self.w_discSeparator = draw_RotationPad(self.w_vector[0],
                                                            self.w_rotaryDisc_color,
                                                            self.w_Scale, self.Opacity,
                                                            preRotValdisc)  # RED
                    # self.w_userData.RotaryDisc = self.w_discSeparator

                CollectThemAllRot = coin.SoTransform()
                CollectThemAll = coin.SoSeparator()
                tR = coin.SbVec3f()
                tR.setValue(
                    self.w_rotation[0], self.w_rotation[1], self.w_rotation[2])
                CollectThemAllRot.rotation.setValue(
                    tR, math.radians(self.w_rotation[3]))

                CollectThemAll.addChild(CollectThemAllRot)
                CollectThemAll.addChild(self.w_ArrowsSeparator)

                if self.w_discEnabled:
                    CollectThemAll.addChild(self.w_discSeparator)
                self.draw_label()
                self.saveSoNodesToWidget(CollectThemAll)

                # add SoSeparator to the switch
                # We can put them in a tuple but it is better not doing so
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'draw Fr_one_Arrow_widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self):
        """[Draw 3D text in the scenegraph]

        Returns:
            [type]: [Use w_lbluserData variable to setup the label shape, size, font ..etc

            w_lebluserData is of type  propertyValues

            @dataclass
            class propertyValues:
                '''
                Property-holder class for drawing labels
                '''
                __slots__ = ['vectors', 'linewidth', 'fontName', 'fontsize',
                            'labelcolor', 'alignment', 'rotation', setupRotation,
                            'scale']
                vectors: VECTOR  # List[App.Vector] two vectors must be provided
                linewidth: int
                fontName: str
                fontsize: int
                labelcolor: tuple
                alignment: int  # This will not be used .. not good
                rotation: tuple    # three float value and an angle 
                setupRotation: Three angle values for the xyz axis
                scale: tuple  # Three float numbers for scaling
            ]
        """
        if self.axisType == 'X':
            self.w_lbluserData.SetupRotation = App.Vector(0, 0, 0)
        elif self.axisType == 'Y':
            self.w_lbluserData.SetupRotation = App.Vector(0, 0, 90)
        elif self.axisType == 'Z':
            self.w_lbluserData.SetupRotation = App.Vector(0, -90, 180)
        self.w_lbluserData.labelcolor = self.w_color
        lbl = fr_label_draw.draw_newlabel(self.w_label, self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def move(self, newVecPos=App.Vector(0, 0, 0)):
        """[Move the widget to a new location referenced by the 
            left-top corner of the object. Or the start of the disc
            if it is an disc.]

        Args:
            newVecPos ([App.Vector], optional): [Move the label to a new position]. Defaults to App.Vector(0.0, 0.0, 0.0).
        """
        self.w_lbluserData.vectors = [newVecPos, ]

    def show(self):
        """[This function will show the widget. But it doesn't draw it. ]
        """
        self.w_visible = 1
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.w_hasFocus == 1:
            return  # nothing to do here
        self.w_hasFocus = 1
        self.redraw()

    def activate(self):
        """[Activate the widget so it can take events]

        """
        if self.w_active:
            return  # nothing to do
        self.w_active = 1
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        self.w_active = 0

    def ChangeScale(self, newScale=[1, 1, 1]):
        """[Scale the whole widget default is no scaling ]

        Args:
            newScale (list, optional): [New scale to apply to the widget]. Defaults to [1.0,1.0,1.0].
        """
        self.w_Scale = newScale

    def __del__(self):
        """
        Class Destructor.
        This will remove the widget totally.
        """
        self.hide()
        try:
            if self.w_parent is not None:
                # Parent should be the windows widget.
                self.w_parent.removeWidget(self)

            if self.w_parent is not None:
                self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)

            self.removeSoNodeFromSoSwitch()
            self.removeSoNodes()
            self.removeSoSwitch()

        except Exception as err:
            App.Console.PrintError("'del Fr_disc_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """[Hide the widget - but the widget is not destroyed]

        Returns:
            [type]: [description]
        """
        if self.w_visible == 0:
            return  # nothing to do
        self.w_visible = 0
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        if self.w_hasFocus == 0:
            return  # nothing to do
        else:
            self.w_hasFocus = 0
            self.redraw()

    def resize(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """Resize the widget by using the new vectors"""
        self.w_Scale = _scale
        self.redraw()

    def size(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """[Scale the widget for the three directions]

        Args:
            _scale (tuple, Three float values): [Scale the widget using three float values for x,y,z axis]. 
            Defaults to [1.0, 1.0, 1.0].
        """
        self.resize(_scale)

    def label(self, newlabel):
        self.w_label = newlabel

    # Keep in mind you must run lblRedraw
    def label_font(self, name="sans"):
        """[Change Label Font]

        Args:
            name (str, optional): [Change label font]. Defaults to "sans".
        """
        self.w_lbluserData.fontName = name

    # Keep in mind you must run lblRedraw
    def label_scale(self, newsize: tuple = [1.0, 1.0, 1.0]):
        """[Scale the font using three float values. This is not the font size.
        You must redraw the label to get this scaling done.
        ]

        Args:
            newsize (int, optional): [Change font label ]. Defaults to 1.
        """
        self.w_lbluserData.scale = newsize

    # Keep in mind you must run lblRedraw
    def label_fontsize(self, newsize=1):
        """[Change label font size ]

        Args:
            newsize (int, optional): [Change fontsize of the label ]. Defaults to 1.
        """
        self.w_lbluserData.fontsize = newsize

    # Must be App.Vector
    def label_move(self, newPos=App.Vector(0.0, 0.0, 0.0)):
        """[Move location of the label]

        Args:
            newPos ([App.Vector], optional): [Change placement of the label]. Defaults to App.Vector(0.0, 0.0, 0.0).
        """
        self.w_lbluserData.vectors = [newPos, ]

    def setRotationAngle(self, axis_and_angle):
        ''' 
        Set the rotation axis and the angle. This is for the whole widget.
        Axis is coin.SbVec3f((x,y,z)
        angle=float number
        '''
        self.w_rotation = axis_and_angle

    def enableDisc(self):
        """[Enable rotation disc. You need to redraw the widget]
        """
        self.w_discEnabled = True

    def setDistanceBetweenThem(self, newvalue):
        """[Change distance between the arrows to the origin of the widget. ]

        Args:
            newvalue ([float]): [new distance in mm]
        """
        self.distanceBetweenThem = newvalue

    def disableDisc(self):
        """[Disable rotation disc. You need to redraw the widget]
        """
        self.w_discEnabled = False

    # def calculateMouseAngle(self, val1, val2):
    #     """[Calculate Angle of two coordinates ( xy, yz or xz).
    #         This function is useful to calculate mouse position
    #         in Angle depending on the mouse position.
    #     ]

    #     Args:
    #         val1 ([Horizontal coordinate]): [x, y]
    #         val2 ([Vertical coordinate ]): [y or z]

    #     Returns:
    #         [int]: [Calculated value in degrees]
    #     """
    #     if(val2 == 0):
    #         return None  # divide by zero
    #     result = 0
    #     if (val1 > 0 and val2 > 0):
    #         result = int(math.degrees(math.atan2(float(val1),
    #                                              float(val2))))
    #     if (val1 < 0 and val2 > 0):
    #         result = int(math.degrees(math.atan2(float(val1),
    #                                              float(val2))))+360
    #     if (val1 > 0 and val2 < 0):
    #         result = int(math.degrees(math.atan2(float(val1),
    #                                              float(val2))))
    #     if (val1 < 0 and val2 < 0):
    #         result = int(math.degrees(math.atan2(float(val1),
    #                                              float(val2))))+360
    #     return result

    def cb_discRotate(self, userData: userDataObject = None):
        """
        Internal callback function, runs when the disc
        rotation event happens.
        self.w_discEnabled must be True
        """
        boundary = self.getWidgetsBoundary(self.w_discSeparator)
        center = self.getWidgetsCenter(self.w_discSeparator)
        try:

            self.endVector = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                        self.w_parent.w_lastEventXYZ.Coin_y,
                                        self.w_parent.w_lastEventXYZ.Coin_z)
            if self.run_Once is False:
                self.run_Once = True
                self.startVector = self.endVector

            # Keep the old value only first time when drag start
                self.startVector = self.endVector
                if not self.has_focus():
                    self.take_focus()
            newValue = self.endVector

            print(center, "center")
            mx = my = mz = 0.0

            if self.axisType == 'X':                                                     # Right
                # It means that we have changes in Z and Y only
                # If the mouse moves at the >center in Z direction :
                # Z++  means   -Angel, Z--  means  +Angle    --> When Y is +                   ^
                # Z++  means   +Angel, Z--  means  -Angle    --> When Y is -                   v
                # Y++  means   +Angel, Y--  means  -Angel    -->  when Z is +
                # Y++  means   -Angel, Y--  means  +Angel    -->  when Z is -
                my = (newValue.y - center.y)
                mz = (newValue.z - center.z)
                if (mz == 0):
                    return  # Invalid
                self.w_discAngle = faced.calculateMouseAngle(my, mz)

            if self.axisType == 'Y':                                                      # Front
                # It means that we have changes in Z and X only
                # Z++  means   -Angel, Z--  means  +Angle    -->  When X is +                   ^
                # Z++  means   +Angel, Z--  means  -Angle    -->  When X is -                   v
                # X++  means   -Angel, x--  means  +Angel    -->  when Z is +
                # X++  means   +Angel, x--  means  -Angel    -->  when Z is -
                mx = (newValue.x - center.x)
                mz = (newValue.z - center.z)
                if (mz == 0):
                    return  # Invalid
                self.w_discAngle = faced.calculateMouseAngle(mx, mz)

            if self.axisType == 'Z':
                # It means that we have changes in X and Y only
                # Y++  means   -Angel, Y--  means  +Angle    -->  When X is +                   ^
                # Y++  means   +Angel, Y--  means  -Angle    -->  When X is -                   v
                # x++  means   -Angel, X--  means  +Angel    -->  when Y is +
                # x++  means   +Angel, X--  means  -Angel    -->  when Y is -
                mx = (newValue.x - center.x)
                my = (newValue.y - center.y)
                if (my == 0):
                    return  # Invalid
                self.w_discAngle = faced.calculateMouseAngle(mx, my)
            if (self.w_discAngle == 360):
                self.w_discAngle = 0
            if (self.oldAngle < 45 and self.oldAngle >= 0) and (self.w_discAngle > 270):
                self.rotationDirection = -1
                self.w_discAngle = self.w_discAngle-360

            elif(self.rotationDirection == -1
                 and self.w_discAngle > 0
                 and self.w_discAngle < 45
                 and self.oldAngle < -270):
                self.rotationDirection = 1

            # we don't accept an angel grater or smaller than 360 degrees
            if(self.rotationDirection < 0):
                self.w_discAngle = self.w_discAngle-360

            if(self.w_discAngle > 359):
                self.w_discAngle = 359
            elif(self.w_discAngle < -359):
                self.w_discAngle = -359
            if self.w_discAngle == -360:
                self.w_discAngle = 0
            self.oldAngle = self.w_discAngle
            print("Angle=", self.w_discAngle)
            self.redraw()

        except Exception as err:
            App.Console.PrintError("'disc Callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    @property
    def getAngle(self):
        return self.w_discAngle

    def do_callbacks(self, callbackType=-1):
        """[summarize the call of the callbacks]

        Args:
            callbackType (int, optional): 
            [Call specific callback depending on the callback type]. Defaults to -1.
            userData will hold the direction dependently.
            Axis   : holds the axis name ('X','Y' or 'Z') as letter
            _rotaryDisc: holds the discs (wheel) rotation axis ('X','Y' or 'Z') 
            as letters.  
        """
        if(callbackType == 0):
            # normal callback This represent the whole widget.
            # Use this to finalize the action.
            self.do_callback(self.w_userData)

        # Move callback - Axis
        elif(callbackType == 1):
            self.w_userData.Axis_cb = True
            self.w_userData.Disc_cb = False
            self.w_ArrowAxis_cb_(self.w_userData)
        elif(callbackType == 2):
            # Rotate callback
            if self.w_discEnabled:
                # Rotation callback - Disc
                self.w_userData.Axis_cb = False
                self.w_userData.Disc_cb = True
                self.w_rotary_cb_(self.w_userData)
    
    def setAxisType(self,_ntype = 'X'):
        """[summary]

        Args:
            _ntype (str, optional): [setter for axis type]. Defaults to 'X'.
        """
        self.axisType = _ntype
