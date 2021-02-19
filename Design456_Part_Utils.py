# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		    *
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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init
import FACE_D as faced
import Design456_MakeFaceArray


class Design456_Part_Utils:
	list = ["Design456_CommonFace",
			"Design456_MakeFaceArray"
			]

	"""Design456 Part Utils"""

	def GetResources(self):
		return{
			'Pixmap':	Design456Init.ICON_PATH + '/Part_Utils.svg',
			'MenuText': 'Box',
						'ToolTip': 'Box'
		}

	def IsActive(self):
		if App.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		self.appendToolbar("Design456_Part_Utils", Design456_Part_Utils())

class GenCommandForPartUtils:
    def __init__(self, object, typeOfCommand):
        self.obj = object
    def DoCommand(self):
        if(typeOfCommand==1):  #Common
            tempResult = App.ActiveDocument.addObject("Part::MultiCommon", "tempWire") 
        elif(typeOfCommand==1):# join or fusion
                App.getDocument('Unnamed').getObject('Fusion').ViewObject.ShapeColor=getattr(App.getDocument('Unnamed').getObject('Cylinder').getLinkedObject(True).ViewObject,'ShapeColor',App.getDocument('Unnamed').getObject('Fusion').ViewObject.ShapeColor)
                
class Design456_CommonFace:
	def Activated(self):
		selection = Gui.Selection.getSelectionEx()
		# Two object must be selected
		if(len(selection) < 2 or len(selection) > 2):
			errMessage = "Select two objects to use Common 2D Tool"
			faced.getInfo(selection).errorDialog(errMessage)
		else:
			nObjects = []
			nObjects.clear()
			GlobalPlacement=App.activeDocument().getObject(selection[1].Object.Name).Placement
			for a2dobj in selection:
				m = App.activeDocument().getObject(a2dobj.Object.Name)
				f = App.activeDocument().addObject('Part::Extrusion', 'ExtrudeOriginal')
				f.Base = App.activeDocument().getObject(m.Name)
				f.DirMode = "Normal"
				f.DirLink = a2dobj.Object
				f.LengthFwd = 1.00
				f.LengthRev = 0.0
				f.Solid = True
				f.Reversed = False
				f.Symmetric = False
				f.TaperAngle = 0.0
				f.TaperAngleRev = 0.0
				App.ActiveDocument.recompute()

				# Make a simple copy of the object
				newShape = Part.getShape(f, '', needSubElement=False, refine=True)
				newObj = App.ActiveDocument.addObject('Part::Feature', 'Extrude')
				newObj.Shape = newShape
				App.ActiveDocument.recompute()
				App.ActiveDocument.ActiveObject.Label = f.Label
				App.ActiveDocument.recompute()
				App.ActiveDocument.removeObject(f.Name)
				App.ActiveDocument.removeObject(m.Name)
				App.ActiveDocument.recompute()
				nObjects.append(newObj)
			tempResult = App.ActiveDocument.addObject("Part::MultiCommon", "tempWire") #Change this line to get other options.
			tempResult.Shapes =nObjects
			App.ActiveDocument.recompute()
			newShape=Part.getShape(tempResult,'', needSubElement=False, refine=True)
			Result=App.ActiveDocument.addObject('Part::Feature','Shape')
			Result.Shape=newShape
			for name in nObjects:
				App.ActiveDocument.removeObject(name.Name)	
			App.ActiveDocument.removeObject(tempResult.Name)
			Gui.Selection.clearSelection()
			App.ActiveDocument.recompute()
			Gui.Selection.addSelection(App.ActiveDocument.Name,Result.Name)
			s=Gui.Selection.getSelectionEx()[0]
			obFace=faced.getInfo(s)
			faceName=obFace.SelectTopFace()
			# Extract the face
			sh = Result.Shape.copy()
			sh.Placement = GlobalPlacement# Result.Placement
			sh.Placement.Base.z=-1
			newobj = Result.Document.addObject("Part::Feature", "Common2DShape")
			newobj.Shape = sh.getElement(faceName)
			App.ActiveDocument.removeObject(Result.Name)
			App.ActiveDocument.recompute()
		
		# extract code here 

	def GetResources(self):
			return{
			'Pixmap':	Design456Init.ICON_PATH + '/CommonFace.svg',
			'MenuText': 'CommonFace',
			'ToolTip':	'CommonFace between 2-2D shapes'
		}

Gui.addCommand('Design456_CommonFace', Design456_CommonFace())
