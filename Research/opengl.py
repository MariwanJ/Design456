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
from OpenGL.GL import *
from OpenGL.GLU import *
import PySide2
import FreeCADGui as Gui
#from PyQt4 import QtGui
#from PyQt4.QtOpenGL import *

import pivy.coin as coin
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide2.QtOpenGL import * #as QtOPENGL
from OpenGL.WGL import *


"""
Class to retrieve all OpenGL related objects

Returns:
    _type_: _description_
"""
class myOPENGL(PySide2.QtWidgets.QGraphicsView):
    #def __init__(self):
    #    pos={  -0.5,-0.5,0.0,0.0, 0.5,-0.5 }
    
    def setDefaultT(self):
        self= self.GetQuarterWidget()[0]
    # wglGetCurrentContext and wglGetCurrentDC, 
    
    def getCurrentContext(self):
        #http://stackoverflow.com/questions/17532033/qglwidget-get-gl-contextes-for-windows
        return wglGetCurrentContext()  # or return OpenGL.WGL.wglGetCurrentContext()
    
    def makeCurrentContext(self,context):
        glfwMakeContextCurrent(context)
    
    def getQuarterContext(self):
        qt=self.GetQuarterWidget()[0]
        return qt.context()
        
    def getCurrentDC(self):
        return wglGetCurrentDC() # or return OpenGL.WGL.wglGetCurrentDC()
    
    def getPaintEngine(self):
        
        v=self.GetQuarterWidget()[0]
        #return PySide2.QtGui.QPaintEngine object
        return v.paintEngine
    
    def getBuffer(self):
        buf=0
        glGenBuffers(1,buf)
        glBindBuffer(GL_ARRAY_BUFFER,buf)
        glBufferData(GL_ARRAY_BUFFER,6*size(float),pos,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,size(float)*2,8)
        
    def GetQuarterWidget(self):
        views = []
        self.mainWindow=Gui.getMainWindow()
        for w in self.mainWindow.findChild(QtGui.QMdiArea).findChildren(QtGui.QWidget):
            if w.inherits("SIM::Coin3D::Quarter::QuarterWidget"):
                views.append(w)
        return views
    
    def getContext(self):
        """ Get OpenGL Context

        Returns:
            _type_: _description_
        """
        return getViewPort().context()

    def getViewPort(self):
        """Get View Port of the OpenGL window

        Returns:
            _type_: _description_
        """
        #return GetQuarterWidget()[0].viewport()
        # or 
        return Gui.ActiveDocument.ActiveView
    def getMdiWindow(self):
        mw = Gui.getMainWindow()
        mdi = mw.findChild(PySide2.QtWidgets.QMdiArea)
        #w = MyNewMainWindow()
        #w.setCentralWidget(mdi)
        #w.show()
        mw.hide()
        mw.show()
        
    def draw(self):
        glDrawArrays(GL_TRIANGLES, self.getBuffer(),0,3)
        
    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-2.5, 0.5, -6.0)
        glColor3f( 1.0, 1.5, 0.0 )
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        glVertex3f(2.0,-1.2,0.0)
        glVertex3f(2.6,0.0,0.0)
        glVertex3f(2.9,-1.2,0.0)
        glEnd()
            

    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    
        gluPerspective(45.0,1.33,0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)



f=myOPENGL()
g=f.getCurrentContext()
c=f.getQuarterContext()
f.makeCurrentContext(g)
f.initializeGL()
f.paintGL()

