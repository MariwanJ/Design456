# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- # kurven abwickeln
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui

from PySide import QtCore
from pivy import coin
import numpy as np

import Part,Draft


def unroll(mode):


	edge=Gui.Selection.getSelection()[0]
	face=Gui.Selection.getSelection()[1]


	# referenzflaeche
	# sf=App.ActiveDocument.Poles.Shape.Face1.Surface
	sf=face.Shape.Face1.Surface


	# pfad
	#e=App.ActiveDocument.map3D_for_Sketch001_on_Poles_by_MAP002_Spline.Shape.Edge1
	#e=App.ActiveDocument.map3D_for_map2D_for_Drawing_on_Poles__Face1_on_Poles_by_MAP_Spline.Shape.Edge1

	# wenn nicht bereits spline
	# fall eoinfacher wire
	# w=App.ActiveDocument.Drawing_on_Poles__Face1.Shape
	w=edge.Shape
	wpts=w.discretize(30)
	bb=Draft.makeBSpline(wpts)
	e=bb.Shape.Edge1



	c=e.Curve

	import numpy as np

	lenp=100
	
	el=e.Length/lenp

	pts=c.discretize(lenp)

	for p in pts:
		t=c.parameter(p)
		print c.tangent(t)
		(u,v)=sf.parameter(p)
		print sf.normal(u,v)


	tgs=[c.tangent(c.parameter(p))[0] for p in pts]
	nos=[]
	for p in pts:
		(u,v)=sf.parameter(p)
		nos += [sf.normal(u,v)]




	if mode=='yaw':
		pp=c.value(0)
		print  "Startpunkt",pp
		#bp=nos[0]
		#bp=FreeCAD.Vector(0,1,0)

	else:
		pp=FreeCAD.Vector()
		bp=FreeCAD.Vector(0,1,0)

	tp=FreeCAD.Vector(1,0,0)
#	tp=FreeCAD.Vector(1,0,0.3).normalize()
	tp=c.tangent(0)[0]
	print "-------------------"
	print "Startpunk",pp
	print "Tangente",tp

	if 1:
		pp=FreeCAD.Vector()
		tp=FreeCAD.Vector(1,0,0)
		bp=FreeCAD.Vector(0,1,0)



	# bp=FreeCAD.Vector(0,1,0)
	ptsn=[pp]

	for i in range(lenp-1):

		
		a=tgs[i+1]-tgs[i]
		if mode=='yaw':
			w=a.dot(nos[i].cross(tgs[i]))
			npa=FreeCAD.Vector(0,0,1).cross(tp)
		else:
			w=a.dot(nos[i])
			npa=FreeCAD.Vector(0,0,1)
			npa=tp.cross(bp)
		print (i,w)
		tpn=tp*np.cos(np.arcsin(w)) + npa*np.sin(np.arcsin(w))
		a=tpn.normalize()

		a *= el
		ppn=pp+ a 
		ptsn +=  [ppn]
		bp=tp.cross(tpn).normalize()
		tp=tpn.normalize()

		pp=ppn

	#Draft.makeWire(pts[:-2])
	#ptsn2=[p+FreeCAD.Vector(0,0,10) for p in ptsn]
	#ptsn=ptsn2
	
	if 1:
		res=Draft.makeBSpline(ptsn)
	else:
		res=App.activeDocument().addObject('Part::Feature','unroll')
		res.Shape=Part.makePolygon(ptsn)

	res.Label=mode + " for " + edge.Label + " on " + face.Label
	App.ActiveDocument.removeObject(bb.Name)







def unroll_yaw():
		unroll(mode='yaw')


def unroll_pitch():
		unroll(mode='pitch')



import Draft


def combineCT():

	objc=Gui.Selection.getSelection()[0]
	objt=Gui.Selection.getSelection()[1]


	#ec=App.ActiveDocument.BSpline001.Shape.Edge1
	ec=objc.Shape.Edge1
	kc=ec.Curve

	import numpy as np
	#et=App.ActiveDocument.BSpline002.Shape.Edge1
	et=objt.Shape.Edge1
	kt=et.Curve

	p=FreeCAD.Vector()
	start=FreeCAD.Vector()
	start=kc.value(0)
	print "start",start
	
	
	
	

	t=FreeCAD.Vector(1,0,0)
	t=FreeCAD.Vector(1,0,0.8).normalize()
	
	t=kc.tangent(0)[0]

	#-------------------
	start=FreeCAD.Vector (1000.0000000000025, -6.585502339306361e-13, -5.684341886080802e-14)
	t=FreeCAD.Vector (0.12085567006180127, 0.9814887436862094, -0.14857238313757795)
#	t=FreeCAD.Vector ( 0.9814887436862094, 0.12085567006180127,0.14857238313757795)
	
	#-------------------



	if 0:
		p=FreeCAD.Vector()
		start=FreeCAD.Vector()
		t=FreeCAD.Vector(1,0,0)

	nn=FreeCAD.Vector(0,0,1)
	b=t.cross(nn)
	print nn

	if 0:
		a=App.ActiveDocument.Drawing_on_Face__Face1_Spline.Shape.Edge1.Curve
		# p0=a.value(0)
		t=a.tangent(0)[0]
		nn=a.normal(0)
		b=t.cross(nn)
		start=a.value(0)

	ptt=FreeCAD.Placement(t,FreeCAD.Rotation())
	ptn=FreeCAD.Placement(nn,FreeCAD.Rotation())

	tpts=[p]

	n=200
	ptsc=kc.discretize(n)

	for i in range(0,n):
		r=App.Rotation(kc.tangent(ec.FirstParameter+1.0*i/n*(ec.LastParameter-ec.FirstParameter))[0],
		kc.tangent(ec.FirstParameter+1.0*(i-1)/n*(ec.LastParameter-ec.FirstParameter))[0])

		if r.Axis.y>0:
			rc=r.Angle
		else:
			rc=-r.Angle
		rc=r.Angle

		r2=App.Rotation(kt.tangent(et.FirstParameter+1.0*i/n*(et.LastParameter-et.FirstParameter))[0],
		kt.tangent(et.FirstParameter+1.0*(i-1)/n*(et.LastParameter-et.FirstParameter))[0])

		if r2.Axis.z>0:
			rt=r2.Angle
		else:
			rt=-r2.Angle
		#rt=r2.Angle

#		rt *= 1.3

#		rt *= 0.4
#		rt *= 0.1

	#	r3=App.Rotation(FreeCAD.Vector(0,0,1),rc)

		rX=App.Rotation(b,rc*180/np.pi)
	#	rX=App.Rotation(b,0)
		rY=App.Rotation(nn,rt*180/np.pi)

		#print (rc,rt)

		pc=FreeCAD.Placement(FreeCAD.Vector(),rX)
		pt=FreeCAD.Placement(FreeCAD.Vector(),rY)
	#	pc=FreeCAD.Placement()


		t9=pt.multiply(pc).multiply(ptt)
		t9=pc.multiply(pt).multiply(ptt)
		#t9=ptt.multiply(pc).multiply(pt)
		ptt=t9
		t=t9.Base
		#ptn=FreeCAD.Placement(nn,FreeCAD.Rotation())
		
		t8=pc.multiply(ptn)
		nn=t8.Base.normalize()
		ptn=t8
		
		b=t.cross(nn).normalize()
		p=p+t
	#	print "t ",t
		print "n ",nn
	#	print "b ",b
	#	print 
		tpts += [p]

	tpts2=[p*(1*ec.Length/n ) +start  for p in tpts]

	Draft.makeWire(tpts2)




if __name__ =='__main__':
	unroll_yaw()
	unroll_pitch()
