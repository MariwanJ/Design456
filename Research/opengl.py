from OpenGL.GL import *
from OpenGL.GLU import *
#from PyQt4 import QtGui
#from PyQt4.QtOpenGL import *

import pivy.coin as coin
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide2.QtOpenGL import * #as QtOPENGL


class myOPENGL:
    def __init__(self):
        self=self.GetQuarterWidget()
        pass
        
    def GetQuarterWidget(self):

        views = []
        mainWindow=Gui.getMainWindow()
        for w in mainWindow.findChild(QtGui.QMdiArea).findChildren(QtGui.QWidget):
            if w.inherits("SIM::Coin3D::Quarter::QuarterWidget"):
                views.append(w)
        return views
    
    def paintGL(self):
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
        glFlush()

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
f.initializeGL()
f.paintGL()

