'''package ausgabe von programmablaufinformationen, importieren der wichtigsten module'''

# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- (c) microelly 2017 v 0.4
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------



##\cond
import FreeCAD
import FreeCADGui

App=FreeCAD
Gui=FreeCADGui

##\endcond

import PySide
from PySide import QtCore, QtGui

import Draft, Part

import numpy as np

#import matplotlib
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import cm 

import os,random,time,sys,traceback
import inspect


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



def log(s,logon=False):
    '''write to a logfile'''
    if logon:
        f = open('/tmp/log.txt', 'a')
        f.write(str(s) +'\n')
        f.close()

def sayd(s):
    '''print information if debug mode'''
    if hasattr(FreeCAD,'animation_debug'):
        log(str(s))
        FreeCAD.Console.PrintMessage(str(s)+"\n")

def say(s):
    '''print information to console''' 
    log(str(s))
    FreeCAD.Console.PrintMessage(str(s)+"\n")

def sayErr(s):
    '''print information as error'''
    log(str(s))
    FreeCAD.Console.PrintError(str(s)+"\n")


def sayW(s):
    '''print information as warning'''
    log(str(s))
    FreeCAD.Console.PrintWarning(str(s)+"\n")


def errorDialog(msg):
    ''' pop up an error QMessageBox'''
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


def sayexc(mess=''):
    ''' print message with traceback''' 
    exc_type, exc_value, exc_traceback = sys.exc_info()
    ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
    lls=eval(ttt)
    l=len(lls)
    l2=lls[(l-3):]
    FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

    l=len(inspect.stack())
    print inspect.stack()[1][3]," @ ",inspect.stack()[1][1]," line: ",inspect.stack()[1][2]
    if l>3: print inspect.stack()[2][3]," @ ",inspect.stack()[2][1]," line: ",inspect.stack()[2][2]
    if  l>3 and inspect.stack()[3][3] <>'<module>':        
        print inspect.stack()[3][1]," line ",inspect.stack()[3][2]
        print inspect.stack()[3][3]



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
    FreeCAD.Console.PrintError(mess + "\n" + "-->  ".join(la2))
    showdialog(title, text=mess, detail="--> ".join(la2))

    l=len(inspect.stack())
    print inspect.stack()[1][3]," @ ",inspect.stack()[1][1]," line: ",inspect.stack()[1][2]
    if l>3: print inspect.stack()[2][3]," @ ",inspect.stack()[2][1]," line: ",inspect.stack()[2][2]
    if l>4 and inspect.stack()[3][3] <>'<module>':
        print inspect.stack()[3][1]," line ",inspect.stack()[2][2]
        print inspect.stack()[3][3]
