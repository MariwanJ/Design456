'''convert a draft bspline to a sketcher bspline'''
# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- microelly 2017 v 0.1
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *
from scipy.signal import argrelextrema
import Sketcher

##creates a BSpline Curve approximation Sketch for a list of points
#


def createSketchSpline(pts=None,label="BSpline Sketch",periodic=True):
	'''createSketchSpline(pts=None,label="BSpline Sketch",periodic=True)'''

	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	sk=App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
	sk.Label=label
	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	if pts==None: # some test data
		pts=[App.Vector(a) for a in [(10,20,30), (30,60,30), (20,50,40),(50,80,90)]]

	for i,p in enumerate(pts):
		sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		#if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000)) 
		#if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i)) 

		radius=2.0
		sk.addConstraint(Sketcher.Constraint('Radius',i,radius)) 
		sk.renameConstraint(i, 'Weight ' +str(i+1))

		#i=5; App.ActiveDocument.Sketch016.setDatum(i,40))

	k=i+1
	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]

	if not periodic:
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,False,3,None,False),False)
	else:
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,True,3,None,False),False)

	conList = []
	for i,p in enumerate(pts):
		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i,3,k,i))
	sk.addConstraint(conList)

	App.activeDocument().recompute()

 	sk.Placement = App.Placement(App.Vector(0,0,p.z),App.Rotation(App.Vector(1,0,0),0))
	sk.ViewObject.LineColor=(random.random(),random.random(),random.random())
	App.activeDocument().recompute()
	return sk


def mergeSketchSpline(pts=None,label="BSpline Sketch",periodic=True,name="Sketch"):
	'''createSketchSpline(pts=None,label="BSpline Sketch",periodic=True)'''

	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	sk=App.activeDocument().getObject(name)
	if sk== None:
		sk=App.activeDocument().addObject('Sketcher::SketchObject',name)

	sk.Label=label
	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	if pts==None: # some test data
		pts=[App.Vector(a) for a in [(10,20,30), (30,60,30), (20,50,40),(50,80,90)]]

	js=[]
	for i,p in enumerate(pts):
		j=sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		sk
		
		# wenn schon was da ist,verbinden
		if i==0 and int(sk.GeometryCount)>=2:
			sk.addConstraint(Sketcher.Constraint('Coincident',j-2,3,j,3)) 
		
		j=int(sk.GeometryCount)-1
		js.append(j)
		#if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000)) 
		#if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i)) 

		radius=2.0
		cj=sk.addConstraint(Sketcher.Constraint('Radius',j,radius)) 
		print ("Constraint ",cj)
		sk.renameConstraint(cj, 'Weight ' +str(cj+1))

		#i=5; App.ActiveDocument.Sketch016.setDatum(i,40))

	

	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]

	if not periodic:
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,False,3,None,False),False)
	else:
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,True,3,None,False),False)

	k=int(sk.GeometryCount)-1

	rc=sk.solve()
	conList = []
	for i,j in enumerate(js):

		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',j,3,k,i))
		print ("okay")

	sk.addConstraint(conList)

	App.activeDocument().recompute()

 	sk.Placement = App.Placement(App.Vector(0,0,p.z),App.Rotation(App.Vector(1,0,0),0))
	sk.ViewObject.LineColor=(random.random(),random.random(),random.random())
	App.activeDocument().recompute()
	return sk


def closecurve(sk):
	j=int(sk.GeometryCount)-2
	sk.addConstraint(Sketcher.Constraint('Coincident',0,3,j,3)) 

def runobj(obj,label=None):
	''' erzeugt fuer ein objekt den SketchSpline'''

	sk=createSketchSpline(obj.Shape.Edge1.Curve.getPoles(),str(obj.Label) + " Sketch" )
	if label !=None: sk.Label=label
	return sk

def runsubs():
	''' erzeugt sketche fuer mehrere subkanten''' 
	sx=Gui.Selection.getSelectionEx()
	s=sx[0]
	for so in s.SubObjects:
		try:
			bc=so.Curve
			pts=bc.getPoles()
			l=s.Object.Label
			print (l,len(pts))
			periodic=bc.isPeriodic()
			createSketchSpline(pts,str(l) + " Sketch" ,periodic)
		except:
			sayexc2(title='Error',mess='somethinq wrong with ' + obj.Label)

def runall():
	''' erzeugt sketche fuer mehrere subkanten''' 
	sx=Gui.Selection.getSelection()
	s=sx[0]
	name="mergeS_"+s.Name
	for so in s.Shape.Edges:
		print (so)
		try:
			bc=so.Curve
			print (bc)
			pts=bc.getPoles()
			print (pts)
			l=s.Label
			print  (l)
			print (l,len(pts))
			periodic=bc.isPeriodic()
			# createSketchSpline(pts,str(l) + " Sketch" ,periodic)
			rc=mergeSketchSpline(pts,str(l) + " Sketch" ,periodic,name)
			name=rc.Name
		except:
			sayexc2(title='Error',mess='somethinq wrong with ' + s.Label)
	closecurve(rc)

def run():
	''' erzeugt fuer jedes selektierte Objekte aus Edge1 einen Sketch'''

	if len( Gui.Selection.getSelection())==0:
		showdialog('Oops','nothing selected - nothing to do for me','Plese select a Draft Bspline or Draft Wire')

	for obj in Gui.Selection.getSelection():
		try:
			bc=obj.Shape.Edge1.Curve
			pts=bc.getPoles()
			l=obj.Label
			print (l,len(pts))
			periodic=bc.isPeriodic()
			createSketchSpline(pts,str(l) + " Sketch" ,periodic)
		except:
			sayexc2(title='Error',mess='somethinq wrong with ' + obj.Label)
