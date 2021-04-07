
import FreeCADGui as Gui
import FreeCAD,Part,Sketcher
App=FreeCAD

import Draft
import numpy as np

from PySide import QtGui
import sys,traceback,random


def showdialog(title="Fehler",text="Schau in den ReportView fuer mehr Details",detail=None):
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Warning)
	msg.setText(text)
	msg.setWindowTitle(title)
	if detail<>None:   msg.setDetailedText(detail)
	msg.exec_()


def sayexc(title='Fehler',mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))
	showdialog(title,text=mess,detail="--> ".join(l2))


import numpy as np

def run():
	label="cloverleaf"
	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	sk=App.activeDocument().addObject('Sketcher::SketchObject','cloverleaf')
	sk.Label=label
	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	pts=None

	if pts==None: # some test data
		anz=16
		r=100
		pts= [FreeCAD.Vector(r*np.sin(2*np.pi/anz*i),r*np.cos(2*np.pi/anz*i),0) for i in range(anz)]

	for i,p in enumerate(pts):
		sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		if 0:
			#if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000)) 
			if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i)) 
		else:
			radius=2.0
			sk.addConstraint(Sketcher.Constraint('Radius',i,radius)) 
			sk.renameConstraint(i, 'Weight ' +str(i+1))


	k=i+1

	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]

	if 0:
		# open spline
		sk.addGeometry(Part.BSplineCurve(l,None,None,False,3,None,False),False)

	else:
		# periodic spline
		sk.addGeometry(Part.BSplineCurve(l,None,None,True,3,None,False),False)

	conList = []
	for i,p in enumerate(pts):
		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i,3,k,i))
	sk.addConstraint(conList)

	App.activeDocument().recompute()


	App.activeDocument().recompute()
	
	sk.addConstraint(Sketcher.Constraint('Symmetric',0,3,2,3,1,3)) 
	App.activeDocument().recompute()


	sk.addConstraint(Sketcher.Constraint('Symmetric',4,3,6,3,5,3)) 
	App.activeDocument().recompute()


	sk.addConstraint(Sketcher.Constraint('Symmetric',8,3,10,3,9,3)) 
	App.activeDocument().recompute()


	sk.addConstraint(Sketcher.Constraint('Symmetric',12,3,14,3,13,3)) 
	App.activeDocument().recompute()


	la=sk.addGeometry(Part.LineSegment(App.Vector(-100,-100,0),App.Vector(100,-100,0)),False)
	lb=sk.addGeometry(Part.LineSegment(App.Vector(100,-100,0),App.Vector(100,100,0)),False)
	lc=sk.addGeometry(Part.LineSegment(App.Vector(100,100,0),App.Vector(-100,100,0)),False)
	ld=sk.addGeometry(Part.LineSegment(App.Vector(-100,100,0),App.Vector(-100,-100,0)),False)
	 
	 
	sk.addConstraint(Sketcher.Constraint('Coincident',la,2,lb,1)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',lb,2,lc,1)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',lc,2,ld,1)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',ld,2,la,1)) 

	for l in [la,lb,lc,ld]:
		sk.toggleConstruction(l) 

	sk.addConstraint(Sketcher.Constraint('Coincident',1,3,lc,1))
	sk.addConstraint(Sketcher.Constraint('Coincident',5,3,lb,1))
	sk.addConstraint(Sketcher.Constraint('Coincident',9,3,la,1))
	sk.addConstraint(Sketcher.Constraint('Coincident',13,3,ld,1))


	print ("curve length",sk.Shape.Edge1.Length)



	sk.addGeometry(Part.LineSegment(App.Vector(-100,-100,0),App.Vector(100,-100,0)),False)
	sk.addConstraint(Sketcher.Constraint('Coincident',21,1,10,3)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',21,2,8,3)) 
	sk.toggleConstruction(21) 

	sk.addGeometry(Part.LineSegment(App.Vector(100,-100,0),App.Vector(100,100,0)),False)
	sk.addConstraint(Sketcher.Constraint('Coincident',22,1,6,3)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',22,2,4,3)) 
	sk.toggleConstruction(22) 

	sk.addGeometry(Part.LineSegment(App.Vector(100,100,0),App.Vector(-100,100,0)),False)
	sk.addConstraint(Sketcher.Constraint('Coincident',23,1,0,3)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',23,2,2,3)) 
	sk.toggleConstruction(23) 




	sk.addGeometry(Part.LineSegment(App.Vector(-100,100,0),App.Vector(-100,-100,0)),False)
	sk.addConstraint(Sketcher.Constraint('Coincident',24,1,14,3)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',24,2,12,3)) 
	sk.toggleConstruction(24) 





