# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a apart of the Open Source Design456 Workbench - FreeCAD. *
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
import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from draftutils.translate import translate   #for translate

#There are several preferences that must be registered somewhere
#For example simplecopy of extruded object, chamfer,..etc
#Originally I wanted to simplify everything. But there are users don't like that.
#This is a start of the preferences pages. Not finished yet. 
#TODO : FIXME:

__updated__ = '2022-02-08 20:28:39'

from PySide import QtGui

def Design456_preferences():
    return Gui.ParamGet("User parameter:BaseApp/Preferences/Mod/Design456")

def setGrid(enabled=True):
    pref = Design456_preferences()
    pref.SetBool("GridEnabled", enabled)

def setSimplified(enabled=False):
    pref = Design456_preferences()
    pref.SetBool("Simplified", enabled)

class Design456Preferences:
    def __init__(self, parent=None):
        self.form = Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')

    def saveSettings(self):
        Design456_preferences().setPreferencesAdvanced(
                self.form.chkDisableGrid.isChecked(),
                self.form.chkSimplify.isChecked()
                )

    def loadSettings(self):
        self.form.chkDisableGrid.setChecked(Design456Init.PATH_PREF.chkDisableGrid())
        self.form.chkSimplify.setChecked(Design456Init.PATH_PREF.chkSimplify())
        self.updateSelection()

    def updateSelection(self, state=None):
        pass

Gui.addPreferencePage(Design456Preferences,"Design456")