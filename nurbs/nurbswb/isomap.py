# -*- coding: utf-8 -*-
'''
#-------------------------------------------------
#-- isomap calculation
#--
#-- microelly 2017 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''

##\cond

from nurbswb.say import *

import FreeCAD as App
import FreeCADGui as Gui




import Part,Mesh,Draft,Points

import numpy as np
import scipy
from scipy import interpolate


# altes interface
# def getmap(mapobj,obj, mpv=0.5, mpu=0.5, fx=-1, fy=-1, vc=30, uc=30 ):

##\endcond

raise Exception("getmap, get,map3 moverd to isodraw")



##\cond

def run_fulltest(obj, mpv=0.5, mpu=0.5, fx=-1, fy=-1, vc=30, uc=30 ):
	'''testmethode'''

	'''  Hilfsobjekte zeichnen   
	mittelpunkt in uv: mpv, mpu
	skalierung/lage der xy-Ebene: fx,fy 
	anzahl der gitterlinien: vc,uc
	'''

	#fx,fy=1,1

	bs=obj.Shape.Face1.Surface
	refpos=bs.value(mpv,mpu)

	if 1: # display centers
		s=App.ActiveDocument.addObject("Part::Sphere","Center Face")
		s.Placement.Base=bs.value(mpv,mpu)

		s=App.ActiveDocument.addObject("Part::Sphere","Center Map")



	if 1: # display grids
		comps=[]
		ptsa=[]

		ba=bs.uIso(mpu)
		comps += [ba.toShape()]

		for v in range(vc+1):
			pts=[]
			vm=1.0/vc*v

			ky=ba.length(vm,mpv)

			if vm<mpv: ky =-ky
			bbc=bs.vIso(vm)

			comps += [bbc.toShape()]

			ptsk=[]
			for u in range(uc+1):
				uv=1.0/uc*u
				ba=bs.uIso(uv)

				ky=ba.length(vm,mpv)
				if vm<mpv: ky =-ky


				kx=bbc.length(mpu,uv)
				if uv<mpu: kx =-kx
				ptsk.append(bs.value(vm,uv))

				pts.append([kx,ky,0])
			ptsa.append(pts)

			comps += [ Part.makePolygon(ptsk)]

		Part.show(Part.Compound(comps))
		App.ActiveDocument.ActiveObject.Label="Grid"


		if 1:
			comps=[]

			for pts in ptsa:
				comps += [ Part.makePolygon([App.Vector(fx*p[0],fy*p[1],0) for p in pts]) ]

			ptsa=np.array(ptsa).swapaxes(0,1)
			for pts in ptsa:
				comps += [ Part.makePolygon([App.Vector(fx*p[0],fy*p[1],0) for p in pts]) ]

			Part.show(Part.Compound(comps))

			# App.ActiveDocument.ActiveObject.Placement.Base=refpos

			App.ActiveDocument.ActiveObject.Label="planar Map of Grid"



	[uv2x,uv2y,xy2u,xy2v]=getmap(obj)


	if 0:
		# display 2 curves
		run_test_1(obj,bs,uv2x,uv2y,fx,fy,refpos)
		# display square grid
		run_test2_2(obj,bs,xy2u,xy2v,fx,fy,refpos)

	if 0:
		#display grid of circles 
		bs=obj.Shape.Face1.Surface
		run_test_circle(bs,xy2u,xy2v)




def run_test_1(obj,bs,uv2x,uv2y,fx,fy,refpos):
	'''testmethode'''
	
	ptss=[]
	ptsk=[]

	for a in range(21):

		um=1./20*a
		vm=0.7/20*a
		y=uv2y(vm,um)
		x=uv2x(vm,um)
		ptss.append(App.Vector(fx*x,fy*y,0))
		ptsk.append(bs.value(um,vm))

	w1=Draft.makeWire(ptss)
	w1.Placement.Base=refpos
	w1.Label="Map uv-line"
	w1.ViewObject.LineColor=(1.,0.,1.)

	w2=Draft.makeWire(ptsk)
	w2.Label="uv-line"
	w2.ViewObject.LineColor=(1.,0.,1.)


	ptss=[]
	ptsk=[]


	for a in range(21):
		um=0.7+ 0.3*np.sin(2*np.pi*a/20)
		vm=0.5+ 0.5*np.cos(2*np.pi*a/20)

		y=uv2y(vm,um)
		x=uv2x(vm,um)
		ptss.append(App.Vector(fx*x,fy*y,0))
		ptsk.append(bs.value(um,vm))

	w1=Draft.makeWire(ptss)
	w1.Label="Map uv-circle"
	w1.Placement.Base=refpos
	w1.ViewObject.LineColor=(1.,0.,0.)

	w2=Draft.makeWire(ptsk)
	w2.Label="uv-circle"
	w2.ViewObject.LineColor=(1.,0.,0.)




def run_test_2(obj,bs,xy2u,xy2v,fx,fy,refpos):
	'''testmethode'''

	col=[]
	col2=[]

	for m in range(-2,20):
		for n in range(2,24):
			ptsk=[]
			ptss=[]
			r=10

			xm=-100+10*m
			ym=-130+10*n
			u=xy2u(xm,ym)
			v=xy2v(xm,ym)
			
			zp=bs.value(u,v)

			#ost
			xm=-100+10*m+r
			ym=-130+10*n
			u=xy2u(xm,ym)
			v=xy2v(xm,ym)
			ze=bs.value(u,v)

			xm=-100+10*m-r
			ym=-130+10*n
			u=xy2u(xm,ym)
			v=xy2v(xm,ym)
			zw=bs.value(u,v)

			xm=-100+10*m
			ym=-130+10*n+r
			u=xy2u(xm,ym)
			v=xy2v(xm,ym)
			zn=bs.value(u,v)

			xm=-100+10*m
			ym=-130+10*n-r
			u=xy2u(xm,ym)
			v=xy2v(xm,ym)
			zs=bs.value(u,v)

			d=np.array([(zp-ze).Length,(zp-zn).Length,(zp-zw).Length,(zp-zs).Length])
			
			d *= 100/r
			d -= 100
			try:
				#if np.abs(d).max()>10:
				if np.abs(d).mean()>5:
					col2 += [Part.makePolygon([ze,zn,zw,zs,ze])]
				else:
					col += [Part.makePolygon([ze,zn,zw,zs,ze])]
			except:
				print ("error polxygon"


#			print(m-10,n-13,"!", np.round(d,1))

	Part.show(Part.Compound(col))
	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(0.,0.,1.)

	Part.show(Part.Compound(col2))
	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,0.,0.)


# drawcircle2
def run_test_circle(bs,xy2u,xy2v,RM=15,uc=10,vc=10):
	''' zeichnet Kreise auf die Flaeche bs '''

	col=[]

	for m in range(-10,10):
		for n in range(-10,10):
			ptsk=[]
			ptss=[]

			xm=10*m
			ym=10*n
			um=xy2u(xm,ym)
			vm=xy2v(xm,ym)

			pss=[]
			pm=bs.value(um,vm)

			for a in range(17):
				r=0.03
				try:
					for i in range(5):
						pa=bs.value(um+r*np.cos(np.pi*a/8),vm+r*np.sin(np.pi*a/8))
#						print ((pa-pm).Length, RM/(pa-pm).Length)
						r=r*RM/(pa-pm).Length
						pa=bs.value(um+r*np.cos(np.pi*a/8),vm+r*np.sin(np.pi*a/8))
					#print ((pa-pm).Length, RM/(pa-pm).Length)
					#print
					l=(pa-pm).Length
					pss.append(pa)
				except:
					print ("error circle2 line near 408"
			try:
				col +=[Part.makePolygon(pss+[pm])]
			except:
				print ("error 412"

	Part.show(Part.Compound(col))
	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,1.,0.)


def run():
	''' main test'''


	[source]=Gui.Selection.getSelection()

	mapa=App.ActiveDocument.MAP
	[uv2x,uv2y,xy2u,xy2v]=getmap(mapa,source)
	
	bs=source.Shape.Face1.Surface

	run_test_circle(bs,xy2u,xy2v,RM=5,uc=10,vc=10)



#run()
##\endcond
