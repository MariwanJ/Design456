'''
display knots and poles of a selected curve
'''

import FreeCAD as App
import FreeCADGui as Gui

import Draft

def run():
	''' for all selected curves two wires are created
	one displays all poles and the other all knotes
	the created objects are not parametric
	'''

	sx=Gui.Selection.getSelectionEx()
	for s in sx:
		print (s,s.SubObjects)
		for i,e in enumerate(s.SubObjects):
			edge=e
			name=s.SubElementNames[i]

			bc=e.Curve
			pts=e.Curve.getPoles()
			print "Poles", len(pts)
			_t=Draft.makeWire(pts,closed=True,face=False)
			App.ActiveDocument.ActiveObject.Label="Poles of "+s.Object.Label + " " + name
			App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
			App.ActiveDocument.ActiveObject.ViewObject.PointColor=(1.,0.,1.)
			App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,0.,1.)

			pts2=[bc.value(k) for k in bc.getKnots()]
			print "Knots:",len(pts2)
			_t=Draft.makeWire(pts2,closed=True,face=False)
			App.ActiveDocument.ActiveObject.Label="Knotes of "+s.Object.Label +   " " + name
			App.ActiveDocument.ActiveObject.ViewObject.PointSize=10
			App.ActiveDocument.ActiveObject.ViewObject.PointColor=(0.,1.,1.)
			App.ActiveDocument.ActiveObject.ViewObject.LineColor=(0.,1.,1.)




run()
