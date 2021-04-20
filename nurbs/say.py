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

'''package ausgabe von programmablaufinformationen, importieren der wichtigsten module'''

# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- (c) microelly 2017 v 0.4
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


# \cond
import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit

import os,sys 

# \endcond

import PySide
from PySide import QtCore, QtGui
import Draft
import Part
import random
import time
import traceback
import inspect

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    

# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import cm

##
#
# <A HREF="http://www.freecadbuch.de/doku.php?id=blog">FreeCAD Buch 2</A>
#
# @author microelly
# @warning works only on linux, writes to /tmp/log.txt
#
# @param[in] s String to log
# @param[in] logon is logging on (False)
#
# @image html plane.svg
#
# .


def log(s, logon=False):
    '''write to a logfile'''
    if logon:
        f = open('/tmp/log.txt', 'a')
        f.write(str(s) + '\n')
        f.close()


def sayd(s):
    '''print information if debug mode'''
    if hasattr(FreeCAD, 'animation_debug'):
        log(str(s))
        App.Console.PrintMessage(str(s)+"\n")


def say(s):
    '''print information to console'''
    log(str(s))
    App.Console.PrintMessage(str(s)+"\n")


def sayErr(s):
    '''print information as error'''
    log(str(s))
    App.Console.PrintError(str(s)+"\n")


def sayW(s):
    '''print information as warning'''
    log(str(s))
    App.Console.PrintWarning(str(s)+"\n")


def errorDialog(msg):
    ''' pop up an error QMessageBox'''
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical, u"Error Message", msg)
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


def sayexc(mess=''):
    ''' print message with traceback'''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    ttt = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    lls = eval(ttt)
    l = len(lls)
    l2 = lls[(l-3):]
    App.Console.PrintError(mess + "\n" + "-->  ".join(l2))

    l = len(inspect.stack())
    print(inspect.stack()[1][3], " @ ", inspect.stack()
          [1][1], " line: ", inspect.stack()[1][2])
    if l > 3:
        print(inspect.stack()[2][3], " @ ", inspect.stack()
              [2][1], " line: ", inspect.stack()[2][2])
    if l > 3 and inspect.stack()[3][3] != '<module>':
        print(inspect.stack()[3][1], " line ", inspect.stack()[3][2])
        print(inspect.stack()[3][3])


def showdialog(title="Fehler",
               text="Schau in den ReportView fuer mehr Details", detail=None):
    '''display a window with: title,text and detail'''

    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(title)
    if detail != None:
        msg.setDetailedText(detail)
    msg.exec_()


def sayexc2(title='Fehler', mess=''):
    '''display exception trace in Console
    and pop up a window with title, message'''

    exc_type, exc_value, exc_traceback = sys.exc_info()
    ttt = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    lls = eval(ttt)
    laa = len(lls)
    la2 = lls[(laa - 3):]
    App.Console.PrintError(mess + "\n" + "-->  ".join(la2))
    showdialog(title, text=mess, detail="--> ".join(la2))

    l = len(inspect.stack())
    print(inspect.stack()[1][3], " @ ", inspect.stack()
          [1][1], " line: ", inspect.stack()[1][2])
    if l > 3:
        print(inspect.stack()[2][3], " @ ", inspect.stack()
              [2][1], " line: ", inspect.stack()[2][2])
    if l > 4 and inspect.stack()[3][3] != '<module>':
        print(inspect.stack()[3][1], " line ", inspect.stack()[2][2])
        print(inspect.stack()[3][3])
