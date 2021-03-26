#add new widget to the main windows
'''
The FreeCAD 3D visualization basically works like this:

    There is a general rectangular Area in which everything is rendered with OpenGL.
     This is what you see as 3D view. This are is a QT widget called QGraphicsView.
      The widget is embedded in the overall UI, and allows to render all kinds of opengl stuff in it.
    One thing that is rendered onto the QGraphicsView is the Coin3D scene graph. 
    Hence in this step, everything thats in the scene graph is put onto the render area
    Other things can than be rendered on top of that. There are some spare examples around over freeCAD, 
    for example the FEM postprocessing scales. Basically anything OpenGL can be drawn

This means for your idea you have 2 options: First to add everything you need to the scenegraph,
 and use coin to achieve your functionality. Or second, use OpenGL to draw everything ontop afterwards.

The second step is made very easy by the fact, that a QGraphicsView allows to add default QtWidgets to it which are than rendered via opengl. here is a simple example (works when you have a document open): 
'''
from PySide2 import QtWidgets

def findInChildren(obj, searched):
	for child in obj.children():
		if isinstance(child, searched):
			return child
		else: 
			res = findInChildren(child, searched)
			if res:
				return res

	return None

view = findInChildren(Gui.getMainWindow(), QtWidgets.QGraphicsView)
widget = QtWidgets.QLineEdit()

proxy = view.scene().addWidget(widget)

