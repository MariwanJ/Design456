
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

#print ("nurbs configuration file loaded")


# meta data for the actions
from PySide import QtGui
import FreeCAD as App
modes = {}


class MyWidget(QtGui.QLineEdit):

    def __init__(self, text, path):

        QtGui.QLineEdit.__init__(self)
        self.setText(text)
        self.path = path
        self.path = "BaseApp/Preferences/Mod/nurbswb/editor"
        self.name = "MyTestparam"
        self.textChanged.connect(self.ttChanged)

    def ttChanged(self, arg):
        print("!!", self)
        print(self.path)
        print("testprocessor")
        print(arg)
        print(self.text())

    def loadA(self):
        group = App.ParamGet("User parameter:"+self.path)
        rc = group.GetString(self.name)
        self.setText(rc)

    def save(self):
        group = App.ParamGet("User parameter:"+self.path)
        group.SetString(self.name, self.text())


if 0:
    w = MyWidget("AAA", "BBB")
    w.show()
    w.setText("TT")
    w.save()
    w.setText("huhu")
    w.loadA()


path = "BaseApp/Preferences/Mod/nurbswb/editor"


def setcf(name, value):
    group = App.ParamGet("User parameter:"+path)
    group.SetFloat(name, value)


def getcf(name):
    group = App.ParamGet("User parameter:"+path)
    return group.GetFloat(name)


def setcs(name, value):
    group = App.ParamGet("User parameter:"+path)
    group.SetString(name, value)


def getcs(name):
    group = App.ParamGet("User parameter:"+path)
    return group.GetString(name)


def setcb(name, value):
    group = App.ParamGet("User parameter:"+path)
    group.SetBool(name, value)


def getcb(name):
    group = App.ParamGet("User parameter:"+path)
    return group.GetBool(name)


def initialize():
    pass


setcb("mikidebug", False)
