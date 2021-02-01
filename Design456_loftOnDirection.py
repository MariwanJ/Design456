#https://forum.freecadweb.org/viewtopic.php?f=22&t=46690&sid=18c0765424496ef734ce5b78914f7197
#https://forum.freecadweb.org/viewtopic.php?f=13&t=48276&p=413611#p413611
#https://forum.freecadweb.org/viewtopic.php?f=13&t=48276&p=414467#p414467
#https://forum.freecadweb.org/viewtopic.php?f=22&t=48425
# mario52
# 25/05/2020 03/07/2020 07/07/2020 15/07/2020
#
#Made to class and added to Design456 by Mariwan Jalal as requested by the Macro author (mario52)
#https://forum.freecadweb.org/viewtopic.php?f=8&t=54893&start=10

import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import BOPTools.SplitFeatures as SPLIT
from FreeCAD import Base
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide

class Design456_loftOnDirection_ui(object):
	
	def setupUi(self, loftOnDirection):
		loftOnDirection.setObjectName("Loft On Direction")
		#loftOnDirection.resize(243, 195)
		self.btnOK = QtGui.QPushButton(loftOnDirection)
		self.btnOK.setGeometry(QtCore.QRect(160, 130, 80, 25))
		self.btnOK.setDefault(True)
		#self.btnOK.setObjectName("btnOK")
		self.btnCancel = QtGui.QPushButton(loftOnDirection)
		self.btnCancel.setGeometry(QtCore.QRect(160, 160, 80, 25))
		#self.btnCancel.setObjectName("btnCancel")
		self.layoutWidget = QtGui.QWidget(loftOnDirection)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 136, 151))
		self.layoutWidget.setObjectName("layoutWidget")
		self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
		self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.label_5 = QtGui.QLabel(self.layoutWidget)
		self.label_5.setObjectName("label_5")
		self.verticalLayout_3.addWidget(self.label_5)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.lblLength = QtGui.QLabel(self.layoutWidget)
		self.lblLength.setObjectName("lblLength")
		self.verticalLayout.addWidget(self.lblLength)
		self.lblScaleX = QtGui.QLabel(self.layoutWidget)
		self.lblScaleX.setObjectName("lblScaleX")
		self.verticalLayout.addWidget(self.lblScaleX)
		self.lblScaleY = QtGui.QLabel(self.layoutWidget)
		self.lblScaleY.setObjectName("lblScaleY")
		self.verticalLayout.addWidget(self.lblScaleY)
		self.lblScaleZ = QtGui.QLabel(self.layoutWidget)
		self.lblScaleZ.setObjectName("lblScaleZ")
		self.verticalLayout.addWidget(self.lblScaleZ)
		self.horizontalLayout.addLayout(self.verticalLayout)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.inLength = QtGui.QDoubleSpinBox(self.layoutWidget)
		self.inLength.setRange(-100000.0, 100000.0);
		self.inLength.setObjectName("inLength")
		self.verticalLayout_2.addWidget(self.inLength)
		self.inScaleX = QtGui.QDoubleSpinBox(self.layoutWidget)
		self.inScaleX.setRange(-100000.0, 100000.0)		
		self.inScaleX.setObjectName("inScaleX")
		self.verticalLayout_2.addWidget(self.inScaleX)
		self.inScaleY = QtGui.QDoubleSpinBox(self.layoutWidget)
		self.inScaleY.setRange(-100000.0, 100000.0)
		self.inScaleY.setObjectName("inScaleY")
		self.verticalLayout_2.addWidget(self.inScaleY)
		self.inScaleZ = QtGui.QDoubleSpinBox(self.layoutWidget)
		self.inScaleZ.setRange(-100000.0, 100000.0)
		self.inScaleZ.setObjectName("inScaleZ")
		self.verticalLayout_2.addWidget(self.inScaleZ)
		self.horizontalLayout.addLayout(self.verticalLayout_2)
		self.verticalLayout_3.addLayout(self.horizontalLayout)
		self.retranslateUi(loftOnDirection)
		QtCore.QMetaObject.connectSlotsByName(loftOnDirection)
	def GetOut(self):
		loftOnDirection.hide()
		
	def retranslateUi(self, loftOnDirection):		
		_translate = QtCore.QCoreApplication.translate
		loftOnDirection.setWindowTitle(_translate("loftOnDirection", "Dialog"))
		self.btnCancel.setText(_translate("loftOnDirection", "Cancel"))
		self.label_5.setText(_translate("loftOnDirection", "Select Change variables"))
		loftOnDirection.setWindowTitle(_translate("loftOnDirection", "Dialog"))
		self.btnOK.setText(_translate("loftOnDirection", "OK"))
		self.btnCancel.setText(_translate("loftOnDirection", "Cancel"))
	
		self.lblLength.setText(_translate("loftOnDirection", "Length"))
		self.lblScaleX.setText(_translate("loftOnDirection", "ScaleX"))
		self.lblScaleY.setText(_translate("loftOnDirection", "ScaleY"))
		self.lblScaleZ.setText(_translate("loftOnDirection", "ScaleZ"))
		
		QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL("accepted()"), self.runClass)
		QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL("accepted()"), self.GetOut)
		QtCore.QObject.connect(self.btnOK,QtCore.SIGNAL("pressed()"),self.runClass)
		QtCore.QMetaObject.connectSlotsByName(loftOnDirection)
	
	def runClass(self):
		try:
			selectedEdge   = Gui.Selection.getSelectionEx()[0].SubObjects[0]	  # select one element
			SubElementName = Gui.Selection.getSelectionEx()[0].SubElementNames[0]
			sel			   = Gui.Selection.getSelection()
			
			#### configuration ####
			ValueLenght=(float)(self.inLength.value())	   
			ValueScaleX=(float)(self.inScaleX.value())
			ValueScaleY=(float)(self.inScaleY.value())
			ValueScaleZ=(float)(self.inScaleZ.value())
			
			####
			createAxis	= 0		   # 0 = not Axis, other = Axis
			createLoft	= 1		   # 0 = not loft, other = loft
			#### configuration ####
			
			if hasattr(selectedEdge,'Surface'):
				plr = plDirection = App.Placement()
			
				########## section direction
				yL = selectedEdge.CenterOfMass
				uv = selectedEdge.Surface.parameter(yL)
				nv = selectedEdge.normalAt(uv[0], uv[1])
				direction = yL.sub(nv + yL)
				r = App.Rotation(App.Vector(0,0,1),direction)
				plDirection.Rotation.Q = r.Q
				plDirection.Base = yL
				plr = plDirection
				print( "surface : ", sel[0].Name, " ", SubElementName,"	 ",direction)
				########## section direction
			
				########## section axis
				if createAxis != 0:
					########## section axis
					points=[FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Vector(0.0,0.0,(ValueLenght) )]
					centerX = Draft.makeWire(points,closed=False,face=False,support=None)
					centerX.Placement = plr
					centerX.Label = "Axis_" + SubElementName
					########## section axis
			
				#### section scale ####
				if createLoft != 0:
					#### section scale ####
					Part.show(selectedEdge.copy())
					firsFace = App.ActiveDocument.ActiveObject
					objClone = Draft.scale(App.ActiveDocument.ActiveObject,App.Vector(ValueScaleX, ValueScaleY, ValueScaleZ),center=App.Vector(plr.Base),copy=True)#False
				
					#### section placement face in length and direction
					objClone.Placement.Base = (App.Vector(direction).scale(ValueLenght, ValueLenght, ValueLenght))
				
					#### section loft
					App.activeDocument().addObject('Part::Loft','Loft')
					App.activeDocument().ActiveObject.Sections=[App.activeDocument().getObject(firsFace.Name), App.activeDocument().getObject(objClone.Name), ]
					App.activeDocument().ActiveObject.Solid = True
					####
				
					#### section hidden faces work
					firsFace.ViewObject.Visibility = False
					objClone.ViewObject.Visibility = False
					App.ActiveDocument.recompute()
					self.GetOut()
					#### section hidden faces work
			
		except ImportError as err:
				App.Console.PrintError("'Design456_loftOnDirection' Failed. "
							   "{err}\n".format(err=str(err)))		
class Design456_loftOnDirection():
	def __init__(self):
	  self.d = QtGui.QWidget()
	  self.ui = Design456_loftOnDirection_ui()
	  self.ui.setupUi(self.d)

	def Activated(self):
		self.d.show()	
	def GetResources(self):
		return{
			'Pixmap' :	Design456Init.ICON_PATH +  '/loftOnDirection.svg',
			'MenuText': 'loftOnDirection',
			'ToolTip':	'Loft On Direction'
		}
Gui.addCommand('Design456_loftOnDirection', Design456_loftOnDirection())			