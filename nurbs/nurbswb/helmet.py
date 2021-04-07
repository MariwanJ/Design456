# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- helmlet with bezier border
#--
#-- microelly 2018 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD,FreeCADGui,Sketcher,Part
from say import *


App = FreeCAD
Gui = FreeCADGui

import numpy as np
import time

import nurbswb.pyob
from nurbswb.pyob import  FeaturePython,ViewProvider
reload (nurbswb.pyob)



class _VPH(ViewProvider):
	''' basic defs '''


	def setupContextMenu(self, obj, menu):
		menu.clear()
		action = menu.addAction("MyMethod #1")
		action.triggered.connect(lambda:self.methodA(obj.Object))
		action = menu.addAction("MyMethod #2")
		menu.addSeparator()
		action.triggered.connect(lambda:self.methodB(obj.Object))
		action = menu.addAction("Edit Sketch")
		action.triggered.connect(lambda:self.myedit(obj.Object))


	def myedit(self,obj):
		self.methodB(None)
		self.pm=obj.Placement
		Gui.activeDocument().setEdit(obj.Name)
		obj.ViewObject.show()
		run(obj)
		self.methodA(None)
		

	def methodA(self,obj):
		print "my Method A"
		FreeCAD.activeDocument().recompute()

	def methodB(self,obj):
		print "my method B"
		FreeCAD.activeDocument().recompute()

	def methodC(self,obj):
		print "my method C !!"
		print obj

		FreeCAD.activeDocument().recompute()
		run(obj)
		obj.Placement=self.pm

	def unsetEdit(self,vobj,mode=0):
		self.methodC(vobj.Object)
		vobj.Object.Placement=self.pm


	def doubleClicked(self,vobj):
		print "double clicked"
		self.myedit(vobj.Object)
		
		print "Ende double clicked"

#-------------------------------

def hideAllProps(obj,pns=None):
	if pns==None: pns=obj.PropertiesList
	for pn in pns:
		obj.setEditorMode(pn,2)

def readonlyProps(obj,pns=None):
	if pns==None: pns=obj.PropertiesList
	for pn in pns:
		try: obj.setEditorMode(pn,1)
		except: pass

def setWritableAllProps(obj,pns=None):
	if pns==None: pns=obj.PropertiesList
	for pn in pns:
		obj.setEditorMode(pn,0)

class Helmet(FeaturePython):
	def __init__(self, obj,patch=False,uc=5,vc=5):
		FeaturePython.__init__(self, obj)

		obj.addProperty("App::PropertyLink","equator")
		obj.addProperty("App::PropertyLink","meridian")
		obj.equator=createHelperSketch("Equator")
		obj.meridian=createHelperSketch("Meridian")


		obj.addProperty("App::PropertyBool","onlyFace")
		obj.addProperty("App::PropertyLink","sketch")
		obj.addProperty("App::PropertyFloat","height").height=100
		obj.addProperty("App::PropertyFloat","border").border=100
		obj.addProperty("App::PropertyVector","offset")
		obj.offset=FreeCAD.Vector(500,300,0)
#		try:
#			obj.equator=App.ActiveDocument.Sketch
#			obj.meridian=App.ActiveDocument.Sketch001
#		except:
			
#			print "keine Hilfskurven verfuegbar"


	def attach(self,vobj):
		print "attach -------------------------------------"
		self.Object = vobj.Object
		self.obj2 = vobj.Object

	def onChanged(self, fp, prop):
		#if not hasattr(fp,'onchange') or not fp.onchange : return
		print "########################## changed ",prop
		if prop =="height":
			print "change XXXX"
			print fp.height
			fp.equator.movePoint(1,2,FreeCAD.Vector(0,fp.height))
			fp.meridian.movePoint(1,2,FreeCAD.Vector(0,fp.height))
			fp.equator.solve()
			fp.meridian.solve()
			fp.equator.recompute()
			fp.meridian.recompute()
			fp.equator.purgeTouched()
			fp.meridian.purgeTouched()
			return

		if prop in ["sketch","height","border"]:
			try:  run(fp)
			except: 
				sayexc("fhelre run")
#		run(fp)

	def execute(self, fp):
		try: self.Lock
		except: self.Lock=False
		if not self.Lock:
			self.Lock=True
			try:
				fp.equator.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(1,0,0),90)
				fp.meridian.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(1,1,1),120)
				run(fp)
			except:
				sayexc('update error')
			self.Lock=False





def createSketch(sk):

	#sk=App.ActiveDocument.addObject('Sketcher::SketchObject','helmlet')

	# aussenring

	pts2= [
		(-200,0,0),(-200,-50,0),(-150,-75,0),(-100,-100,0),
		(0,-100,0),(100,-100,0),(150,-75,0),(200,-50,0),(200,0,0),
		(200,50,0),(150,75,0),(100,100,0),
		(0,100,0),(-100,100,0),(-150,75,0),(-200,50,0),(-200,0,0),
	]

	import Draft

	pts=[FreeCAD.Vector(p) for p in pts2]
	#Draft.makeWire(pts)


	for i in range(16):
		sk.addGeometry(Part.LineSegment(pts[i],pts[i+1]),False)

	for i in range(15):
		sk.addConstraint(Sketcher.Constraint('Coincident',i,2,i+1,1)) 

	sk.addConstraint(Sketcher.Constraint('Coincident',15,2,0,1)) 

	# innenring

	pts2=[(-50,-30,0),(50,-30,0),(50,30,0),(-50,30,0)]
	pts=[FreeCAD.Vector(p) for p in pts2]
	#Draft.makeWire(pts)

	for i in range(4):
		sk.addGeometry(Part.LineSegment(pts[i-1],pts[i]),False)

	for i in range(3):
		print "aa",i
		sk.addConstraint(Sketcher.Constraint('Coincident',16+i,2,16+i+1,1)) 

	sk.addConstraint(Sketcher.Constraint('Coincident',19,2,16,1)) 

	# parallele gruppen 

	sk.addConstraint(Sketcher.Constraint('Parallel',0,15)) 
	for i in range(7):
		sk.addConstraint(Sketcher.Constraint('Parallel',2*i+1,2*i+2)) 

	for i in [0,7,16,18]:
		print i
		sk.addConstraint(Sketcher.Constraint('Vertical',i)) 

	for i in [3,11,17,19]:
		sk.addConstraint(Sketcher.Constraint('Horizontal',i)) 
	
	for i,c in enumerate(sk.Constraints):
		sk.setVirtualSpace(i, True)

	sk.solve()
	sk.recompute()


def createHelperSketch(role):
	''' sketch for equator and meridian'''
	sk=App.ActiveDocument.addObject('Sketcher::SketchObject',role)
	for i in range(4):
		sk.addGeometry(Part.LineSegment(App.Vector(i*100,0,0),App.Vector((i+1)*100.,0,0)))
	for i in range(3):
		sk.addConstraint(Sketcher.Constraint('Coincident',i,2,i+1,1)) 
	sk.movePoint(1,2,FreeCAD.Vector(200,100))
	return sk






def createHelmet(obj=None):

	#a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","helmet")
	a=App.activeDocument().addObject('Sketcher::SketchObjectPython',"helmet")

	Helmet(a)
	a.onlyFace=True
	a.sketch=obj
	createSketch(a)
	a.recompute()

	_VPH(a.ViewObject,'freecad-nurbs/icons/createHelmet.svg')
	# a.ViewObject.Transparency=60
	a.ViewObject.ShapeColor=(0.3,0.6,0.3)
	if obj<>None:
		a.Label="Helmet for "+obj.Label


def run(fp):

	pts=[fp.getPoint(i,1) for i in range(16)]
	pts2=[fp.getPoint(i,1) for i in range(16,20)]

	ptsall=np.zeros(25*3).reshape(5,5,3)

	ptsall[0,2]=pts[0]
	ptsall[0,3]=pts[1]
	ptsall[0,4]=pts[2]
	ptsall[1,4]=pts[3]
	ptsall[2,4]=pts[4]
	ptsall[3,4]=pts[5]
	ptsall[4,4]=pts[6]
	ptsall[4,3]=pts[7]
	ptsall[4,2]=pts[8]
	ptsall[4,1]=pts[9]
	ptsall[4,0]=pts[10]
	ptsall[3,0]=pts[11]
	ptsall[2,0]=pts[12]
	ptsall[1,0]=pts[13]
	ptsall[0,0]=pts[14]
	ptsall[0,1]=pts[15]

	ptsall[1:4,3,1]=pts2[1].y
	ptsall[1:4,1,1]=pts2[3].y
	ptsall[3,1:4,0]=pts2[3].x
	ptsall[1,1:4,0]=pts2[1].x
	
	print "arquator"
	pa=fp.equator.getPoint(1,1)
	pb=fp.equator.getPoint(2,2)

	ptsall[3,1:4,0]=pb.x
	ptsall[1,1:4,0]=pa.x


	print "meridan"
	pa=fp.meridian.getPoint(1,1)
	pb=fp.meridian.getPoint(2,2)
	
	
	ptsall[1:4,3,1]=pa.x
	ptsall[1:4,1,1]=pb.x


	h=fp.equator.getPoint(1,2).y
	print ("HEights",h,fp.height)
	if h != fp.height:
		fp.height=h

	#fp.equator.movePoint(1,2,FreeCAD.Vector(0,fp.height))
	fp.equator.movePoint(0,1,fp.getPoint(0,1))
	fp.equator.movePoint(3,2,fp.getPoint(7,2))
	fp.equator.solve()
	fp.equator.purgeTouched()

	fp.meridian.movePoint(1,2,FreeCAD.Vector(0,fp.height))
	t=fp.getPoint(4,1)
	t2=fp.getPoint(12,1)
	fp.meridian.movePoint(0,1,FreeCAD.Vector(t.y,0,0))
	fp.meridian.movePoint(3,2,FreeCAD.Vector(t2.y,0,0))


	fp.meridian.solve()
	fp.meridian.purgeTouched()


	ptse =[ fp.equator.getPoint(0,1)+FreeCAD.Vector(0,-fp.border,0)]
	ptse +=[fp.equator.getPoint(i,1) for i in range(4)]
	ptse += [fp.equator.getPoint(3,2) ]
	ptse += [fp.equator.getPoint(3,2)+FreeCAD.Vector(0,-fp.border,0) ]

	ptsf =[ fp.meridian.getPoint(0,1)+FreeCAD.Vector(0,-fp.border,0)]
	ptsf +=[fp.meridian.getPoint(i,1) for i in range(4)]
	ptsf += [fp.meridian.getPoint(3,2) ]
	ptsf += [fp.meridian.getPoint(3,2)+FreeCAD.Vector(0,-fp.border,0) ]


	ptse2=[FreeCAD.Vector(p.x,0,p.y) for p in ptse]
	ptsf2=[FreeCAD.Vector(0,p.x,p.y) for p in ptsf]



	ptsall[1:4,1:4,2]=fp.height

	yy=np.array(ptsall)
	yy2=np.array([yy[0],yy[0],yy[1],yy[2],yy[3],yy[4],yy[4]])

	yy2[0,:,2]=-fp.border
	yy2[-1,:,2]=-fp.border

	yy=yy2.swapaxes(0,1)
	yy2=np.array([yy[0],yy[0],yy[1],yy[2],yy[3],yy[4],yy[4]])
	yy2[0,1:-1,2]=-fp.border
	yy2[-1,1:-1,2]=-fp.border

	af=Part.BSplineSurface()

	yy2a=np.array(yy2)
	yy3a=yy2a.swapaxes(0,1)

	print "!!",Gui.ActiveDocument.getInEdit(),"!!"

	vp=Gui.ActiveDocument.getInEdit()
	if vp != None and vp.Object==fp:
		yy2 +=fp.offset

#	af.buildFromPolesMultsKnots(yy2, 
#		[4,1,1,1,4],[4,1,1,1,4],
#		[0,1,2,3,4],[0,1,2,3,4],
#		False,False,3,3)

	af.buildFromPolesMultsKnots(yy2, 
		[4,3,4],[4,3,4],
		[0,1,2,],[0,1,2,],
		False,False,3,3)



	if fp.onlyFace:
		fp.Shape=af.toShape()
		return

	comps=[]
	comps += [af.toShape()]

	yy3=yy2.swapaxes(0,1)

	for yy in [yy2,yy3]:	
		for r in [0,3,6]:
			bc=Part.BSplineCurve()
			bc.buildFromPolesMultsKnots(yy[r], 
				[4,1,1,1,4],
				[0,1,2,3,4],
				False,3)
			comps += [bc.toShape()]

#	print "ptse23,",ptse2

	if 0:
		for yy in [yy2a,yy3a]:	
			for r in [0,6]:
				bc=Part.BSplineCurve()
				bc.buildFromPolesMultsKnots(yy[r], 
					[4,1,1,1,4],
					[0,1,2,3,4],
					False,3)
				comps += [bc.toShape()]

	for yy in [ptse2,ptsf2]:
			bc=Part.BSplineCurve()
			bc.buildFromPolesMultsKnots(yy, 
				[4,1,1,1,4],
				[0,1,2,3,4],
				False,3)
			comps += [bc.toShape()]

	# comps += [Part.makePolygon(ptse)]

	fp.Shape=Part.Compound(comps)



#sp=App.ActiveDocument.Sketch


#createHelmet()
#App.activeDocument().recompute()



def createTriangle():
	import numpy as np

	k=10
	rings=[
	[[-100,0,0],[-80,20,0],[-20,80,0],[0,100,0]],
	[[-80,0,0],[-50,20,40],[0,50,40],[20,80,0]],
	[[-20,0,-20+k],[0,20,20],[50,30,40],[80,20,0]],
	[[0,0,-20+k],[20,0,-20+k],[80,0,0],[100,0,0]],
	]
	rr=np.array(rings)

	bs=Part.BSplineSurface()
	bs.buildFromPolesMultsKnots(rr,
		[4,4],[4,4],
		[0,2],[0,2],
		False,False,3,3)
	if 0:
		bs.insertUKnot(1,3,0)
		bs.insertVKnot(1,3,0)

		bs.insertUKnot(1.5,3,0)

	sk=App.ActiveDocument.addObject('Part::Spline','adapter')
	sk.Shape=bs.toShape()



	rA=np.array([rr[0],rr[0]+[-30,30,30]])
	bs=Part.BSplineSurface()
	bs.buildFromPolesMultsKnots(rA,
		[2,2],[4,4],
		[0,2],[0,2],
		False,False,1,3)
	sk=App.ActiveDocument.addObject('Part::Spline','rA')
	sk.Shape=bs.toShape()

	rr[1]=rr[0]+rA[0]-rA[1]

	rrs=rr.swapaxes(0,1)
	rB=np.array([rrs[-1],rrs[-1]+[30,30,20]])
	bs=Part.BSplineSurface()
	bs.buildFromPolesMultsKnots(rB,
		[2,2],[4,4],
		[0,2],[0,2],
		False,False,1,3)
	sk=App.ActiveDocument.addObject('Part::Spline','rB')
	sk.Shape=bs.toShape()

	#rrs[-2][2:]=rrs[-1][2:]+rB[0][2:]-rB[1][2:]
	rrs[-2][1:]=rrs[-1][1:]+rB[0][1:]-rB[1][1:]

	rru=rrs.swapaxes(0,1)
	#rru=rings
	#rru=rr





	bs=Part.BSplineSurface()
	bs.buildFromPolesMultsKnots(rru,
		[4,4],[4,4],
		[0,2],[0,2],
		False,False,3,3)
	if 0:
		bs.insertUKnot(1,3,0)
		bs.insertVKnot(1,3,0)

		bs.insertUKnot(1.5,3,0)

	sk=App.ActiveDocument.addObject('Part::Spline','adapter')
	sk.Shape=bs.toShape()

	if 0:	
		comps=[]	
		bsa=bs.copy()
		bsa.segment(0,1,0,1)
		comps +=[bsa.toShape()]

		bsa=bs.copy()
		bsa.segment(0,1,1,2)
		comps +=[bsa.toShape()]

		bsa=bs.copy()
		bsa.segment(1,2,0,1)
		comps +=[bsa.toShape()]

		bsa=bs.copy()
		bsa.segment(1,2,1,2)
		comps +=[bsa.toShape()]

		sk=App.ActiveDocument.addObject('Part::Spline','split')
		sk.Shape=Part.Compound(comps)





