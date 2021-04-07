# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- geodesics and patches
#--
#-- microelly 2018 v 0.3
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


# from say import *
# import nurbswb.pyob
#------------------------------

# https://dl.acm.org/citation.cfm?id=1654774
# chinese whispers

import FreeCAD,FreeCADGui,Sketcher,Part
import Draft


App = FreeCAD
Gui = FreeCADGui

import numpy as np
import time
from pivy import coin

import nurbswb.pyob
from nurbswb.pyob import  FeaturePython,ViewProvider
reload (nurbswb.pyob)


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

class Geodesic(FeaturePython):
	def __init__(self, obj,patch=False,uc=5,vc=5):
		FeaturePython.__init__(self, obj)

		obj.addProperty("App::PropertyBool","onchange","", "calculate all 4 directions")
		obj.addProperty("App::PropertyBool","flipNormals","", "calculate all 4 directions")
		obj.addProperty("App::PropertyBool","createSweep")
		
		obj.addProperty("App::PropertyBool","geodesicTorsion")
		obj.addProperty("App::PropertyEnumeration","mode","Base").mode=["geodesic","curvature","patch","distance"]
		obj.addProperty("App::PropertyLink","obj","","surface object")
		obj.addProperty("App::PropertyInteger","facenumber","", "number of the face")
		obj.addProperty("App::PropertyFloat","sega","Source", "u coord start point of geodesic").sega=0
		obj.addProperty("App::PropertyFloat","segb","Source", "u coord start point of geodesic").segb=100
		obj.addProperty("App::PropertyFloat","tolerance2","Source", "tolerance for curve on face").tolerance2=10
		obj.addProperty("App::PropertyFloat","tolerance","Source", "tolerance for geodesic apporx").tolerance=0.5
		obj.addProperty("App::PropertyFloat","volume","Source", "u coord start point of geodesic").volume=10

		obj.addProperty("App::PropertyFloat","thresholdForce")
		obj.addProperty("App::PropertyBool","relativeForce")

		if not patch:
			obj.addProperty("App::PropertyInteger","gridsize","", "size of a grid cell").gridsize=20
			obj.addProperty("App::PropertyInteger","forcesize","", "size of a grid cell").forcesize=100

			obj.addProperty("App::PropertyFloat","u","A", "u coord start point of geodesic").u=50
			obj.addProperty("App::PropertyFloat","v","A", "v coord start point of geodesic").v=50

			obj.addProperty("App::PropertyFloat","ue","_calculated", "calculated u coord endpoint of geodesic")
			obj.addProperty("App::PropertyFloat","ve","_calculated", "calculated coord endpoint of geodesic")

			obj.addProperty("App::PropertyFloat","ut","Target", "u coord target point of geodesic").ut=60
			obj.addProperty("App::PropertyFloat","vt","Target", "u coord target point of geodesic").vt=60
			obj.addProperty("App::PropertyBool","target","Target", "u coord target point of geodesic").target=True

			obj.addProperty("App::PropertyInteger","lang","A", "size of cell in u direction").lang=24
			obj.addProperty("App::PropertyInteger","lang2","Generator", "size of cell in v direction").lang2=3
			obj.addProperty("App::PropertyInteger","lang3","Generator", "size of cell in -u direction").lang3=6
			obj.addProperty("App::PropertyInteger","lang4","Generator", "size of cell in -v direction").lang4=10

			obj.addProperty("App::PropertyFloat","direction","A", "direction of backbone geodesic")
			obj.direction=0
			obj.addProperty("App::PropertyFloat","directione","_calculated", "calculated direction of backbone geodesic")
			obj.directione=0

			obj.addProperty("App::PropertyFloat","directionrib","Generator", "direction of rib geodesics")
			obj.directionrib=90



			obj.addProperty("App::PropertyBool","flip","Star", "flip the curvature direction")
			obj.addProperty("App::PropertyBool","redirect","Star", "flip the curvature direction")
			obj.addProperty("App::PropertyBool","star","Star", "calculate all 4 directions")

			obj.addProperty("App::PropertyFloat","dist","_calculated","calculated distance of endpoint (ue,ve) to target (ut,vt)")
			obj.addProperty("App::PropertyLink","pre","XYZ","")

			obj.addProperty("App::PropertyFloatList","uvdarray","_storage","storage data uvd for geodesic field")
			obj.addProperty("App::PropertyInteger","uvdUdim","_storage","u dimension of uvdarray")
			obj.addProperty("App::PropertyInteger","uvdVdim","_storage","v dimension of uvdarray")

			obj.addProperty("App::PropertyLink","geogrid","geodesic","")
			obj.addProperty("App::PropertyLink","geoborder","geodesic","")
			obj.addProperty("App::PropertyLink","geobone","geodesic","")

		if patch:
			obj.addProperty("App::PropertyBool","patch","patch", ).patch=True
#			obj.addProperty("App::PropertyLink","track","patch","")
#			obj.addProperty("App::PropertyLink","face","patch","")
			obj.addProperty("App::PropertyLink","wire","patch","")

			obj.addProperty("App::PropertyEnumeration","form","patch","layout for the 3D curve").form=["polygon","bspline1","bspline3",'facecurve','face']
			obj.form='polygon'
			obj.addProperty("App::PropertyFloat","tolerance","patch").tolerance=2.0
			obj.addProperty("App::PropertyBool","closed","patch")
			obj.addProperty("App::PropertyBool","reverse","patch")
#			obj.addProperty("App::PropertyInteger","ind1Face","patch","v dimension of uvdarray").ind1Face=0
#			obj.addProperty("App::PropertyInteger","ind2Face","patch","v dimension of uvdarray").ind2Face=0


		readonlyProps(obj,['mode','pre','directionrib','directione','dist','ue','ve'])
		if obj.mode=='patch':
			obj.Shape=updatePatch(obj)



	def attach(self,vobj):
		print "attach -------------------------------------"
		self.Object = vobj.Object
		self.obj2 = vobj.Object

	def onChanged(self, fp, prop):
		if not hasattr(fp,'onchange') or not fp.onchange : return
		if prop=="direction" or prop=="lang":
			try:  self.execute(fp)
			except: pass


	def execute(self, fp):

		if fp.mode=="patch":
			fp.Shape=updatePatch(fp)
			if fp.form=='face':
				fp.Placement=fp.obj.obj.Placement
			else:
				fp.Placement=FreeCAD.Placement()

		if fp.mode=="geodesic":
			fp.Shape=updateGeodesic(fp)
		if fp.mode=="curvature":
			fp.Shape=updateCurvature(fp)
		if fp.mode=="distance":
			fp.Shape=updateDistance(fp)





def createGeodesicA(obj=None):
	'''create a geodesic from the default psoition 50 50 and direction for testing'''

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Geodesic")

	Geodesic(a)
	a.obj=obj
	ViewProvider(a.ViewObject)
	if obj<>None:
		a.Label="Geodesic for "+obj.Label

	a.mode="geodesic"

	a.lang=50
	a.lang2=50
	a.lang3=50
	a.direction=30
	
	a.lang2=1
	a.lang4=1
	a.lang3=0


	a.lang3=50
	a.lang2=20
	a.lang4=-1

#	hideAllProps(a,['patch'])
	return a


def createPatch(obj=None,wire=None):
	'''create a patch on obj with borderdata from wire'''

	# reorder if the selection order is false
	try: _=obj.uvdUdim
	except: obj,wire=wire,obj

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Patch")

	Geodesic(a,True)
	a.obj=obj
	a.wire=wire

	ViewProvider(a.ViewObject)
	if obj<>None:
		a.Label="Patch for "+obj.Label
	a.mode="patch"
	
	#a.reverse=True
	a.closed=True
	a.form="facecurve"
	a.tolerance=1.
	a.form="bspline3"
#	a.form="face"
	
#	hideAllProps(a)
	return a






def createCurvature(obj=None):
	'''create a curvature object'''

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Curvature")

	Geodesic(a)
	a.obj=obj
	a.u=10
	a.v=55
	ViewProvider(a.ViewObject)
	a.Label="Curvature for "+obj.Label
	a.mode="curvature"
	a.star=True
	a.lang=120
	a.direction=-60
	return a





def colorPath(pts,color='0 1 0',name=None):
	'''create a colored LineSet for points pts with colorstring color '''

	def ivPts(pts):
		'''  points to iv format '''
		s=''
		for p in pts:
			s +=  "{} {} {}, ".format(p.x,p.y,p.z) 
		return s

	buf='''
	#Inventor V2.1 ascii
	  Separator {
		 Transform { translation %s }
		 Material { diffuseColor %s specularColor 1 1 1 shininess 0.9 }
#		 Shuttle { translation0 -1 0 -1 translation1 1 0 1 speed 0.3 on TRUE }
		 Coordinate3 { point [ %s ] }
		 LineSet { 
			#numVertices [ 7 ]
		 }
	  }
	'''

	if name <> None:
		iv=App.ActiveDocument.getObject(name)
		if iv==None:iv=App.ActiveDocument.addObject("App::InventorObject",name)
		iv.Buffer=buf % ('0 0 0',color,ivPts(pts))
	else: 
		return buf % ('0 0 0',color,ivPts(pts))



def genRibForGeodesic(fp,u,v,d,lang,ribflag,color='0 1 1'):
		''' erzeugt eine rippe fuer color grid '''

		pts=[]
		uvs=[(u,v)]

		obj=fp.obj
		f=obj.Shape.Faces[fp.facenumber]
		sf=f.Surface
		umin,umax,vmin,vmax=f.ParameterRange

		(t1,t2)=sf.tangent(u,v)
		t=FreeCAD.Vector(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2)

		lang=int(round(lang))
		#print "loops genrib",lang
		for i in range(lang):
			pot=sf.value(u,v)
			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)
			pts += [pot]

			# local axis cross creation
			if ribflag:
				pts += [pot+ sf.normal(u,v)*0.5*fp.gridsize*0.1,pot]
				pts += [pot+ sf.normal(u,v).cross(t)*2.5*fp.gridsize*0.1,pot]
				pts += [pot+ sf.normal(u,v).cross(t)*-2.5*fp.gridsize*0.1,pot]

			last=sf.value(u,v)
			p2=last+t*fp.gridsize*0.1
			(u1,v1)=sf.parameter(p2)
			(u,v)=(u1,v1)

			#restrict to area inside the Face
			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			uvs += [(u,v)]

			if u<umin or v<vmin or u>umax or v>vmax:
				print "Abbruch!"
				break

			p=sf.value(u,v)
			pts += [p]

			#compute the further direction of the geodesic
			(t1,t2)=sf.tangent(u,v)
			t=p-last
			t.normalize()


		if ribflag:
			try: cps=colorPath(pts,color=color,name=None)
			except: 
				cps=None
				shape=None
		else: 
			cps=None
			shape=None

		return (cps,(u,v),uvs)




def getface_old(count=10):
	'''outdated: for update patch old '''

	faceobj=App.ActiveDocument.BSpline
	bs=faceobj.Shape.Face1
	track=App.ActiveDocument.Line.Shape

	ptsa=[]
	ptsb=[]

	try: curve=track.Curve
	except: curve=track.Edges[0].Curve


	#print track.Edges

	cc=int(round(track.Length))
	tps=track.discretize(cc)

	col2=[]
	for p in tps:
			v=curve.parameter(p)
			t=curve.tangent(v)
			n=t[0].cross(FreeCAD.Vector(0,0,1))
			polg=Part.makePolygon([p+10000*n,p-10000*n])
			col2 += [polg]
			
			ss=bs.makeParallelProjection(polg,FreeCAD.Vector(0,0,1))
			sps=[v.Point for v in ss.Vertexes]
			#print sps
			if len(sps) == 2:
				ptsa += [sps[0]]
				ptsb += [sps[1]]
			if len(sps) == 1:
				ptsa += [sps[0]]
				ptsb += [sps[0]]

	ppsa=[]
	ppsb=[]

	segments=App.ActiveDocument.getObject("Segments")
	if segments==None:
		segments=App.ActiveDocument.addObject("Part::Feature","Segments")

	pls=[]
	nls=[]
	comp=[]
	f=0.4
	f=count/track.Length
	f=1
	for i,p in enumerate(ptsa):
		if ptsa[i]<>ptsb[i]:
			pol=Part.makePolygon([ptsa[i],ptsb[i]])
			comp.append(pol)
#			print(i, (ptsa[i]-tps[i]).Length,(ptsb[i]-tps[i]).Length)

			pls += [(ptsa[i]-tps[i]).Length*f]
			nls += [(ptsb[i]-tps[i]).Length*f]
	segments.Shape=Part.Compound(comp)
	return track.Length, pls,nls



def drawColorLines(fp,name,ivs):
	'''create a inventor presentation of a inventor scene ivs'''

	iv=App.ActiveDocument.getObject(fp.Name+"_"+name)
	if iv==None:iv=App.ActiveDocument.addObject("App::InventorObject",fp.Name+"_"+name)
	iv.Label=name + " for " +fp.Label
	iv.Buffer=ivs


def updateGeodesic(fp):
		print "run updateStarG"

		gridon=True

		ta=time.time()
		d=fp.direction
		d2=fp.directionrib
		u=fp.u
		v=fp.v
		obj=fp.obj
		d0=d


		ak=1

		if fp.pre<>None:
			obj=fp.pre.obj
			d=fp.pre.directionrib
			d=fp.pre.directione+fp.pre.directionrib
			
			u=fp.pre.ue
			v=fp.pre.ve
			if fp.obj<>obj: fp.obj=obj
			if fp.u<>u: fp.u=u
			if fp.v<>v: fp.v=v
			if fp.direction<>d:	
				fp.direction=d


		u *= 0.01
		v *= 0.01

		pts=[]
		ptsbb=[]

		f=obj.Shape.Faces[fp.facenumber]
		sf=f.Surface
		#print (f,sf,fp.facenumber,obj.Shape.Faces)
		umin,umax,vmin,vmax=f.ParameterRange

		# print (umin,umax)

		u0,v0=u,v
		d0=d

		u=umin + (umax-umin)*u
		v=vmin + (vmax-vmin)*v

		#u0,v0=u,v

		pstart=sf.value(u,v)

		(t1,t2)=sf.tangent(u,v)
		nn=f.normalAt(u,v)
		t2=t1.cross(nn)
		t2.normalize()
		#if ak:
		#	t2 *= -1
		#d=60-d

		#t=FreeCAD.Vector(np.cos(np.pi*d/180)*t1*-1+np.sin(-np.pi*-d/180)*t2*-1)
		t=FreeCAD.Vector(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2)
		t *= -1


		shapas=''
		puvs=[(u,v)]
		nuvs=[(u,v)]

		puvs=[]
		nuvs=[]
		uvsarr=[]

		lang3=int(round(10.0*fp.lang3/fp.gridsize))
		lang=int(round(10*fp.lang/fp.gridsize))
		lang2=int(round(10*fp.lang2/fp.gridsize))
		if fp.lang4==-1: lang4=lang2
		else: lang4=int(round(10*fp.lang4/fp.gridsize))

		#rueckwaerts
		ribb=''
		riba=''

		for i in range(lang3+1):
			taa=time.time()
			if 1 or i % 2 == 0 or i==fp.lang:
				ribflag= i%5 == 0 and gridon
				if i==lang3: ribflag=True
				
#				print ("erzeuge ribbe",i)
				a=t.dot(t1)
				b=t.dot(t2)
				a,b=b,a
				de=180./np.pi*np.arctan2(b,a)
				
				if i==lang3 : color='0 1 0'
				#else: color='0 1 1'
				else: color='1 1 0'

				r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de-90,lang2,ribflag,color)
				r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de+90,lang4,ribflag,color)

				if ak:
					r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de,lang2,ribflag,color)
					r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de+180,lang4,ribflag,color)



#				r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de+90+2*d,lang2,ribflag,color)
#				r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de+90-2*d,lang2,ribflag,color)

				nuvs += [(u1,v1)]
				puvs += [(u2,v2)]
				uvs2.reverse()
				if i<>0:
					#uvsarr += [uvs2[:-1]+uvs1]
					ttu=uvs2[:-1]+uvs1
					ttu.reverse()
					uvsarr += [ttu]
					
				if ribflag:
					if i<>0:
						shapas += r1 + r2
				if i==0:
					ribm=r1+r2
				if i==lang3:
					ribb=r1+r2

			pot=sf.value(u,v)
			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)
			pts += [pot]

			pts += [sf.value(u,v)+ sf.normal(u,v)*2,sf.value(u,v)]

			# ribs
			if 1:
				rib=FreeCAD.Vector(np.cos(np.pi*d2/180)*t+np.sin(np.pi*d2/180)*sf.normal(u,v).cross(t))
				pts += [sf.value(u,v)+ rib*-2,sf.value(u,v)]
				pts += [sf.value(u,v)+ rib*2,sf.value(u,v)]


			last=sf.value(u,v)
			p2=last+t*0.1*fp.gridsize
			(u1,v1)=sf.parameter(p2)
			
#			print ("pot",i,u,v,t,fp.gridsize,last,p2)
			(u,v)=(u1,v1)
			
			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax


			if u<umin or v<vmin or u>umax or v>vmax:
				print "qaBBruch!"
			
				break
			p=sf.value(u,v)

			pts += [ p]
			(t1,t2)=sf.tangent(u,v)
			nn=f.normalAt(u,v)
			t2=t1.cross(nn)
			
			#t2 *= -1

			t=p-last
			t.normalize()
			tbb=time.time()
			# print ("time aa bb,loop",tbb-taa,i,(tbb-taa)/fp.lang*1000000/lang2)

		#-------------------------------------

		# vorwaerts rictung

		geto=[]

		d=d0
		u=umin + (umax-umin)*u0
		v=vmin + (vmax-vmin)*v0

		(t1,t2)=sf.tangent(u,v)

		nn=f.normalAt(u,v)
		t2=t1.cross(nn)
		t2.normalize()

		t=FreeCAD.Vector(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2)

		puvs.reverse()
		nuvs.reverse()
		aa=[]
		for j in range(len(uvsarr)):
			a= uvsarr[-1-j]
			a.reverse()
			aa += [a]
		uvsarr=aa

		for i in range(lang+1):
			taa=time.time()
			if 1 or i % 2 == 0 or i==lang:
				ribflag= i%5 == 0 and gridon
				if i==lang: ribflag=True
				
#				print ("erzeuge ribbe",i)
				a=t.dot(t1)
				b=t.dot(t2)
				a,b=b,a
				de=180./np.pi*np.arctan2(b,a)
				
				if i==lang: color='1 0 0'
				else: color='1 1 0'
#				r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de+90-2*d,lang2,ribflag,color)
#				r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de-90-2*d,lang2,ribflag,color)

				r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de+180,lang2,ribflag,color)
				r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de+0,lang4,ribflag,color)



				if 1:
					puvs += [(u1,v1)]
					nuvs += [(u2,v2)]
				uvs2.reverse()
				uvsarr += [uvs2[:-1]+uvs1]
				if ribflag:
					shapas += r1 + r2
#				if i==0:
#					riba=r1+r2
				if i==lang:
					riba=r1+r2

			pot=sf.value(u,v)
			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)
			pts += [pot]
			ptsbb += [pot]
			
			(ct1,ct2)=sf.curvatureDirections(u,v)
			kmax=sf.curvature(u,v,"Max")
			kmin=sf.curvature(u,v,"Min")
			aa1=ct1.dot(t)
			aa2=ct2.dot(t)
			
			if fp.flipNormals:nfa=-1 
			else: nfa=1

			geto +=[pot,pot +  nfa*sf.normal(u,v)*abs(aa1*aa2*(kmax-kmin))*10*fp.forcesize,
					pot]


			pts += [sf.value(u,v)+ sf.normal(u,v)*2,sf.value(u,v)]

			# ribs
			if 1:
				rib=FreeCAD.Vector(np.cos(np.pi*d2/180)*t+np.sin(np.pi*d2/180)*sf.normal(u,v).cross(t))
				pts += [sf.value(u,v)+ rib*-2,sf.value(u,v)]
				pts += [sf.value(u,v)+ rib*2,sf.value(u,v)]
				if i==0:
					poly=Part.makePolygon([sf.value(u,v)+ rib*(-1)*(lang2+1),
						sf.value(u,v),sf.value(u,v)+ rib*(1.0)*(lang4+1)])
					
					if fp.volume:
						poly=Part.makePolygon([
							sf.value(u,v)+ rib*(-1)*(lang2+1),
							sf.value(u,v),
							sf.value(u,v)+ rib*(1.0)*(lang4+1),

							sf.value(u,v)+ rib*(1.0)*(lang4+1) + fp.volume*sf.normal(u,v),
							sf.value(u,v)+ fp.volume*sf.normal(u,v),
							sf.value(u,v)+ rib*(-1)*(lang2+1)+ fp.volume*sf.normal(u,v),
							sf.value(u,v)+ rib*(-1)*(lang2+1),
						])


					if fp.createSweep:
						cyy=App.ActiveDocument.getObject(fp.Name+'_MyBSC')
						if cyy== None:
							cyy=App.ActiveDocument.addObject('Part::Feature',fp.Name+'_MyBSC')
						cyy.Shape=poly





			last=sf.value(u,v)
			p2=last+t*fp.gridsize*0.1
			(u1,v1)=sf.parameter(p2)
#			print ("bpot",i,u,v,t,fp.gridsize,last,p2)
#			print ("bpot",i,u,v,last)
			(u,v)=(u1,v1)

			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			if u<umin or v<vmin or u>umax or v>vmax:
				print "qaBBruch!"
				break


			ua=umin + (umax-umin)*u
			va=vmin + (vmax-vmin)*v


			p=sf.value(u,v)

			pts += [ p]
			(t1,t2)=sf.tangent(u,v)
			nn=f.normalAt(u,v)
			t2=t1.cross(nn)

			t=p-last
			t.normalize()
			tbb=time.time()
			# print ("time aa bb,loop",tbb-taa,i,(tbb-taa)/fp.lang*1000000/lang2)


#		FreeCAD.uvsarr=np.array(uvsarr)
#		FreeCAD.sf=sf
#		print "size uvs arr",FreeCAD.uvsarr.shape
#		print (fp.lang,lang2)

		ar=np.array(uvsarr)
		(a,b,c)=ar.shape
		fp.uvdarray=list(ar.reshape(a*b*c))
		fp.uvdUdim=a
		fp.uvdVdim=b

		puvs+=[(u,v)]
		nuvs+=[(u,v)]

		shape=Part.makePolygon(pts)
		cp1=colorPath(pts,color='1 1 0',name=None)
		
		ppts=[sf.value(u,v) for (u,v) in puvs]
		pshape=Part.makePolygon(ppts)
		cp2=colorPath(ppts[:-1],color='0 0 1',name=None)

		npts=[sf.value(u,v) for (u,v) in nuvs]
		nshape=Part.makePolygon(npts)
		cp3=colorPath(npts[:-1],color='0 0 1',name=None)


		name="VBound"
		drawColorLines(fp,name,cp1+cp2+cp3)

		tb=time.time()
		print ("time a - b:",tb-ta)

		ut=fp.ut*0.01
		vt=fp.vt*0.01
#		pt=Part.Point(sf.value(ut,vt))
#		print "Abstand"
#		print pt
#		print shape.distToShape(pt.toShape())
#		print (pt,shape.distToShape(pt.toShape())[0])

		ut=umin + (umax-umin)*ut
		vt=vmin + (vmax-vmin)*vt





		pend=sf.value(ut,vt)
		pt=Part.Point(sf.value(ut,vt))
		fp.dist= shape.distToShape(pt.toShape())[0]

#		print ("Abstand",pts[-1],pend,shape.distToShape(pt.toShape())[0],(pts[-1]-pend).Length)
#		print (u,v)

		fp.ue=u2*100
		fp.ve=v2*100

		a=t.dot(t1)
		b=t.dot(t2)
		fp.directione=180./np.pi*np.arctan2(b,a)

		if fp.target:
			shape2=Part.Compound([
						shape,
						Part.makePolygon([
							pend,pend+FreeCAD.Vector(0,10,0),
							pend,pend+FreeCAD.Vector(0,-10,0),
							pend,pend+FreeCAD.Vector(10,0,0),
							pend,pend+FreeCAD.Vector(-10,0,0),
							pend,pend+FreeCAD.Vector(0,0,10),
							pend,pend+FreeCAD.Vector(0,0,-10),
						]),
						Part.makePolygon([
							pstart,pstart+FreeCAD.Vector(0,10,0),
							pstart,pstart+FreeCAD.Vector(0,-10,0),
							pstart,pstart+FreeCAD.Vector(10,0,0),
							pstart,pstart+FreeCAD.Vector(-10,0,0),
							pstart,pstart+FreeCAD.Vector(0,0,10),
							pstart,pstart+FreeCAD.Vector(0,0,-10),
						])

					])

		else:
			shape2=shape

		if gridon:
			name="Grid"
			drawColorLines(fp,name,shapas)

			name="UBound"
			drawColorLines(fp,name,riba+ribm+ribb)

		bc=Part.BSplineCurve()
		FreeCAD.ptsbb=ptsbb
		if fp.tolerance==0:
			bc.interpolate(ptsbb)
		else:
			bc.approximate(ptsbb,DegMax=3,Tolerance=fp.tolerance)
#		return bc.toShape()

		if fp.createSweep:
			yaas=App.ActiveDocument.getObject(fp.Name+'_geodes')
			if yaas == None:
				yaas=App.ActiveDocument.addObject('Part::Feature',fp.Name+'_geodes')

			yaas.Shape=bc.toShape()

			ys=App.ActiveDocument.getObject(fp.Name+'_Sweep')
			if ys == None:
				ys=App.ActiveDocument.addObject('Part::Sweep',fp.Name+'_Sweep')
			ys.Sections=[cyy, ]
			ys.Spine=(yaas,["Edge1"])
			if fp.volume: ys.Solid=True


		if fp.geodesicTorsion:
				polygt=Part.makePolygon(geto)

				cygt=App.ActiveDocument.getObject(fp.Name+'_geodesicTorsion')
				if cygt== None:
					cygt=App.ActiveDocument.addObject('Part::Feature',fp.Name+'_geodesicTorsion')
					cygt.ViewObject.LineColor=(1.0,0.,0.)
				cygt.Shape=polygt




		return shape2


def updatePatch_old(fp):
		print "run update Patch"

		gridon=True

		d=fp.direction
		d2=fp.directionrib
		u=fp.u
		v=fp.v
		obj=fp.obj

		if fp.pre<>None:
			obj=fp.pre.obj
			d=fp.pre.directionrib
			d=fp.pre.directione+fp.pre.directionrib
			
			u=fp.pre.ue
			v=fp.pre.ve
			if fp.obj<>obj: fp.obj=obj
			if fp.u<>u: fp.u=u
			if fp.v<>v: fp.v=v
			if fp.direction<>d:	
				fp.direction=d


		u *= 0.01
		v *= 0.01

		pts=[]

		f=obj.Shape.Faces[fp.facenumber]
		sf=f.Surface
		umin,umax,vmin,vmax=f.ParameterRange

		u=umin + (umax-umin)*u
		v=vmin + (vmax-vmin)*v

		(t1,t2)=sf.tangent(u,v)
		t=FreeCAD.Vector(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2)

		shapas=''
		puvs=[(u,v)]
		nuvs=[(u,v)]

		lang,ptsa,ntsa=getface_old(2+fp.lang+1)

		pds=[4+p for p in ptsa]
		nds=[4+p for p in ntsa]

		uvsp=[]

		for i in range(fp.lang+1):

			if i % 2 == 0 or i==fp.lang:
				ribflag= i%5 == 0 and gridon
				if i==fp.lang: ribflag=True
 
#				print ("erzeuge ribbe",i)
				a=t.dot(t1)
				b=t.dot(t2)
				de=180./np.pi*np.arctan2(b,a)
				r1,(u1,v1),uvs1 = genRibForGeodesic(fp,u,v,de+90,ptsa[i],ribflag)
				r2,(u2,v2),uvs2 = genRibForGeodesic(fp,u,v,de-90,ntsa[i],ribflag)
				puvs += [(u1,v1)]
				nuvs += [(u2,v2)]
				uvsp += [uvs1]
				if ribflag:
					shapas += r1 + r2
				if i==0:
					riba=r1+r2
				if i==fp.lang:
					ribb=r1+r2


			pot=sf.value(u,v)
			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)
			pts += [pot]

			pts += [sf.value(u,v)+ sf.normal(u,v)*2,sf.value(u,v)]

			# ribs
			if 1:
				rib=FreeCAD.Vector(np.cos(np.pi*d2/180)*t+np.sin(np.pi*d2/180)*sf.normal(u,v).cross(t))
				pts += [sf.value(u,v)+ rib*-3,sf.value(u,v)]
				pts += [sf.value(u,v)+ rib*3,sf.value(u,v)]

			last=sf.value(u,v)
			p2=last+t*1
			(u1,v1)=sf.parameter(p2)
			(u,v)=(u1,v1)

			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			if u<umin or v<vmin or u>umax or v>vmax:
				print "qaBBruch!"
				break
			p=sf.value(u,v)

			pts += [ p]
			(t1,t2)=sf.tangent(u,v)
			t=p-last
			t.normalize()


		FreeCAD.uvsp=uvsp
		FreeCAD.sf=sf
#		if hasattr(obj,"uvdarray"):
#		fp.uvdarray=list(np.array(uvsp).reshape(lang*lang2*2))

		puvs+=[(u,v)]
		nuvs+=[(u,v)]




		shape=Part.makePolygon(pts)
		cp1=colorPath(pts,color='1 0 0',name=None)
		
		ppts=[sf.value(u,v) for (u,v) in puvs[1:-1]]
		pshape=Part.makePolygon(ppts)
		cp2=colorPath(ppts,color='0 1 0',name=None)
		
		npts=[sf.value(u,v) for (u,v) in nuvs[1:-1]]
		nshape=Part.makePolygon(npts)
		cp3=colorPath(npts,color='0 0 1',name=None)


		name="geodesicBorder"
		drawColorLines(name,cp1+cp2+cp3)




		ut=fp.ut*0.01
		vt=fp.vt*0.01
#		pt=Part.Point(sf.value(ut,vt))
#		print "Abstand"
#		print pt
#		print shape.distToShape(pt.toShape())
#		print (pt,shape.distToShape(pt.toShape())[0])


		pend=sf.value(ut,vt)
		pt=Part.Point(sf.value(ut,vt))
#		print "Abstand"
#		print pt
#		print shape.distToShape(pt.toShape())
		fp.dist= shape.distToShape(pt.toShape())[0]

#		print ("Abstand",pts[-1],pend,shape.distToShape(pt.toShape())[0],(pts[-1]-pend).Length)
#		print (u,v)
		fp.ue=u2*100
		fp.ve=v2*100

		a=t.dot(t1)
		b=t.dot(t2)
		fp.directione=180./np.pi*np.arctan2(b,a)

		shape2=Part.Compound([shape,Part.makePolygon([
				pend,pend+FreeCAD.Vector(0,10,0),
				pend,pend+FreeCAD.Vector(0,-10,0),
				pend,pend+FreeCAD.Vector(10,0,0),
				pend,pend+FreeCAD.Vector(-10,0,0),
				pend,pend+FreeCAD.Vector(0,0,10),
				pend,pend+FreeCAD.Vector(0,0,-10),
				])]+[pshape] )

		shape2=Part.Compound([shape,pshape,nshape])

		if gridon:

			name="geodesicGrid"
			drawColorLines(name,shapas)

			name="borders"
			drawColorLines(name,riba+ribb)

		return shape2




def updateCurvaturePath(fp,redirect,flip):

		d=fp.direction
		u=fp.u
		v=fp.v
		obj=fp.obj
		u *= 0.01
		v *= 0.01

		pts=[]
		pts2=[]

		f=obj.Shape.Faces[fp.facenumber]
		sf=f.Surface
		print (f,sf,fp.facenumber,obj.Shape.Faces)
		umin,umax,vmin,vmax=f.ParameterRange

		u=umin + (umax-umin)*u
		v=vmin + (vmax-vmin)*v

#		(t1,t2)=sf.tangent(u,v)
		tsa=sf.curvatureDirections(u,v)
		
		if flip: t=tsa[1]
		else: t=tsa[0]
		if redirect:
			t *= -1

		for i in range(fp.lang):

			pts += [sf.value(u,v)]

			last=sf.value(u,v)
			p2=last+t*1
			(u1,v1)=sf.parameter(p2)
			(u,v)=(u1,v1)
			
			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			if u<umin or v<vmin or u>umax or v>vmax:
				print "qaBBruch!"
				break
			p=sf.value(u,v)
			
			pts += [ p]
			# (t1,t2)=sf.tangent(u,v)
			(t1,t2)=sf.curvatureDirections(u,v)
#			print "---------t ",t
#			print t1
#			print t2
			print (round(t.dot(t1)*100),round(t.dot(t2)*100))
			dt1=t.dot(t1)
			dt2=t.dot(t2)
			pts += [p+t1,p,p+t2,p]
			if abs(dt1)<0.82 and abs(dt2)<0.82:
				print "worry "
				pts += [p+t1,p,p+t2,p]
#			else:

			if abs(dt1)>abs(dt2):
				t=t1
			else: 
				t=t2

			if (p-last).Length>(p+t-last).Length:
				t *= -1

			t.normalize()

		shape=Part.makePolygon(pts)

		ut=fp.ut*0.01
		vt=fp.vt*0.01
		pend=sf.value(ut,vt)
		pt=Part.Point(sf.value(ut,vt))
		print "Abstand"
		print pt
		print shape.distToShape(pt.toShape())
		t= shape.distToShape(pt.toShape())
		print t
		print t[0]
		fp.dist=t[0]

		return shape


def updateCurvature(fp):
	if fp.star:
		rc=Part.Compound([
			updateCurvaturePath(fp,False,False),
			updateCurvaturePath(fp,False,True),
			updateCurvaturePath(fp,True,False),
			updateCurvaturePath(fp,True,True)
		])
	else:
		rc=updateCurvaturePath(fp,fp.redirect,fp.flip)
	return rc




def runtest1():
	'''testfall fuer grundflaechen'''
	a=createGeodesic(obj=App.ActiveDocument.Poles)
	b=createGeodesic(obj=App.ActiveDocument.Cylinder)
	d=createGeodesic(obj=App.ActiveDocument.Cone)
	d=createGeodesic(obj=App.ActiveDocument.Sphere)


def createGeodesic():
	'''geodesic auf koerper erzeugen'''
	a=createGeodesicA(obj=Gui.Selection.getSelection()[0])


def geodesicMapPatchToFace():
	'''pfad(e) $2 auf geodesic $1 auflegen'''
	a=createPatch(obj=Gui.Selection.getSelection()[0],
	wire=Gui.Selection.getSelection()[1])
	App.activeDocument().recompute()
	App.activeDocument().recompute()


def appendGeodesic():
	'''geodesic erzeugen, die an eine geodesic andockt'''
	a=createGeodesicA()
	a.pre=Gui.Selection.getSelection()[0]


def createCurvatureStar():
	a=createCurvature(obj=Gui.Selection.getSelection()[0])


def	creategeodesicbunch():
	for j in range(36):
		a=createGeodesicA(obj=Gui.Selection.getSelection()[0])
		a.direction=j*10



# http://cyberware.com/wb-vrml/index.html

def  wireToPolygon(w):
	pts=[]
	yy=0.2
	for e in w.Edges:
		print (e, e.Length)
		if e.Length>1:
			zz=e.discretize(int(round(e.Length)+1))
			zz[0],zz[0]+yy*(zz[1]-zz[0])
			pts += [zz[0],zz[0]+yy*(zz[1]-zz[0])]+zz[1:-1]+ [zz[-1]+yy*(zz[-2]-zz[-1]),zz[-1]]
	#pol=Part.makePolygon(pts)
	return pts





def updatePatch(fp):


	gd=fp.obj

	try:
		udim=gd.uvdUdim
		vdim=gd.uvdVdim
	except:
		return Part.Shape()

	usvarr=np.array(gd.uvdarray).reshape(udim,vdim,2)
	sf=gd.obj.Shape.Face1.Surface

	# bound box fuer rahmen
	print fp.wire.Shape.BoundBox
	bb=fp.wire.Shape.BoundBox
	l3=-bb.XMin
	if l3<0: l3=0
	l=bb.XMax
	l2=max(abs(bb.YMax),abs(bb.YMin))
	print (l,l2,l3)
	
	needupd=False
	if gd.lang<l: gd.lang=int(round(l))+1;needupd=True
	if gd.lang2<l2:	
		gd.lang2=int(round(l2))+1;needupd=True
		gd.lang4=int(round(l2))+1;needupd=True
	
	if gd.lang3<l3:	gd.lang3=int(round(l3))+1;needupd=True
	
	if needupd:
		gd.Proxy.execute(gd.obj)


	# erster fall nur ein wire #+#
	try: ws= fp.wire.Shape.Wires
	except: ws=None
	
	if ws <> None: ws2=ws
	else: ws2=[fp.wire.Shape]

	print ws
	print ws2
	ress=[]
	for w in ws2:
		print ("loop",w,ress)
		pts=w.discretize(1000)

		# anderer weg der zerlegnung
		pts=wireToPolygon(w)

		uvs=[]
		ul,vl=(-10000,-10000)
		


		for p in pts:
			(u,v) = int(round(p.x*10.0/gd.gridsize)),int(round(p.y*10.0/gd.gridsize))
			print (u,v)

#			u += gd.lang3
#			v += gd.lang2

			u += int(round(gd.lang3*10.0/gd.gridsize))
			v += int(round(gd.lang2*10.0/gd.gridsize))


			if u>=udim: u=udim-1
			if v>=vdim: v=vdim-1


			if (u,v) <>(ul,vl):
				uvs += [(u,v)]
				ul,vl=u,v

		# ausgangskurve 2D
		pts2=[FreeCAD.Vector(u,v,0) for (u,v) in uvs]

		# berechne 3D Kurve ..
		pts=[]
		print usvarr.shape
		print "A"
		
		for up,vp in uvs:
			print (up,vp)
			(u,v)=usvarr[up,vp]
			print (up,vp,u,v,sf.value(u,v))
			pts += [sf.value(u,v)]

#		pts=pts[:-1]
		if fp.closed:
			pts=pts[5:]+pts[1:6]


		#---------------------
		if fp.form=='facecurve':
			t=sf
			pts2da=[sf.parameter(p) for p in pts[1:]]
			pts2da=[sf.parameter(p) for p in pts]
			pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da]

			bs2d = Part.Geom2d.BSplineCurve2d()
			bs2d.setPeriodic()

#			bs2d.interpolate(pts2d)

			bs2d.setPeriodic()
			bs2d.approximate(pts2d,DegMax=3,Tolerance=fp.tolerance2*0.001)

#			bs2d.approximate(pts2d[30:-2]+pts2d[:30],DegMax=3,Tolerance=fp.tolerance)
#			bs2d.setPeriodic()
			bs2d.segment(0.01*fp.sega,0.01*fp.segb)


			e1 = bs2d.toShape(t)
			print len(pts2d)
			print "huhwu"
			return e1
		#----------------------

		if fp.form=='face':
			t=sf
			pts2da=[sf.parameter(p) for p in pts[1:]]
			pts2d=[FreeCAD.Base.Vector2d(p[0],p[1]) for p in pts2da]

			bs2d = Part.Geom2d.BSplineCurve2d()
			bs2d.setPeriodic()
			bs2d.approximate(pts2d,DegMax=3,Tolerance=fp.tolerance2*0.001)

			ptsa2d=bs2d.discretize(len(pts2da)+1)

			bs2d = Part.Geom2d.BSplineCurve2d()
			bs2d.setPeriodic()

			bs2d.interpolate(ptsa2d)
			bs2d.setPeriodic()


			e1 = bs2d.toShape(t)
			FreeCAD.e1=e1

			if fp.reverse:
				e1.reverse()

			face=gd.obj.Shape.Face1
			splita=[(e1,face)]
			r=Part.makeSplitShape(face, splita)
			rc=r[0][0]
#			rc.Placement=gd.obj.Placement
			return rc


		if fp.form=='polygon':
			shape=Part.makePolygon(pts)
			if ws <> None: ress += [shape]
			else:
				return shape

		if fp.form=='bspline1':
			bc=Part.BSplineCurve()
			bc.approximate(pts,DegMin=1,DegMax=1,Tolerance=fp.tolerance)
			#if fp.closed: bc.setPeriodic()
			if ws <> None: ress += [bc.toShape()]
			else:
				return bc.toShape()

		if fp.form=='bspline3':
			bc=Part.BSplineCurve()
			bc.approximate(pts,DegMax=3,Tolerance=fp.tolerance)
			#if fp.closed: bc.setPeriodic()
			if ws <> None: ress += [bc.toShape()]
			else:
				return bc.toShape()

	comp=Part.Compound(ress)
	return comp



'''
def approx_step():
	

	a=App.ActiveDocument.Geodesic

	ds=a.dist
	a.direction += 1
	App.activeDocument().recompute()
	dsa=a.dist

	better=True
	print (ds,dsa)
	if ds<dsa:
		print "wird nicht besser A"
		a.direction -= 1
		App.activeDocument().recompute()
		ds=a.dist
		a.direction -= 1
		App.activeDocument().recompute()
		dsa=a.dist

		print (ds,dsa)
		if ds<dsa:
			print "wird nicht besser B"
			a.direction += 1
			App.activeDocument().recompute()
			better=False

	if better: return better
	
	better=True

	ds=a.dist
	a.lang -= 1
	App.activeDocument().recompute()
	dsa=a.dist

	print (ds,dsa)
	if ds<=dsa:
		print "wird nicht besser C"
		a.lang += 1
		App.activeDocument().recompute()

		ds=a.dist
		a.lang += 1
		App.activeDocument().recompute()
		dsa=a.dist

		print (ds,dsa)
		if ds<=dsa:
			print "wird nicht besser D"
			a.lang -= 1
			App.activeDocument().recompute()
			better=False
	print "a lang ",a.lang
	print "hah ", better
	return better


def approx_geodesic(n=10):
	for i in range(n): 
		print "------------step ",i
		rc=approx_step()
		print "----------result ",rc
		if not rc: break
'''





def genRibForUpdateDistance(f,u=50,v=50,d=0,lang=30,gridsize=20):
		''' erzeugt eine rippe fuer color grid fuer kreis geodesics'''

		pts=[]
		norms=[]
		tans=[]
		uvs=[(u,v)]

		sf=f.Surface
		umin,umax,vmin,vmax=f.ParameterRange

#		pts = [sf.value(v*0.01,u*0.01)]
		u=umin-(umin-umax)*u/100
		v=vmin-(vmin-vmax)*v/100


#		print ("uv neu xx",u,v)

		(t1,t2)=sf.tangent(u,v)
		nn=f.normalAt(u,v)

		t2=t1.cross(nn)
		t2.normalize()


		a=np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2
#		print a
		t=FreeCAD.Vector(tuple(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2))

		lang=int(round(lang))

		for i in range(lang+1):
			pot=sf.value(u,v)
			nn=f.normalAt(u,v)

			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)


			pts += [pot]
			norms += [nn]
			tans += [t]

			last=sf.value(u,v)
			p2=last+t*gridsize*0.1
			#print ("apot",i,u,v,last)
			(u1,v1)=sf.parameter(p2)
			(u,v)=(u1,v1)



#			last=sf.value(u,v)
#			p2=last+t*fp.gridsize*0.1
#			(u1,v1)=sf.parameter(p2)
#			(u,v)=(u1,v1)




			#restrict to area inside the Face
			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			uvs += [(u,v)]

			p=sf.value(u,v)

			(t1,t2)=sf.tangent(u,v)

			ta=p-last
			try: 
				ta.normalize()
				t=ta
			except:
				pass

		pts=np.array(pts)
		norms=np.array(norms)

		return pts,norms,tans


def genrib_outdated(f,u=50,v=50,d=0,lang=30,gridsize=20):
		''' erzeugt eine rippe fuer color grid fuer kreis geodesics'''

		pts=[]
		norms=[]
		tans=[]
		uvs=[(u,v)]

		sf=f.Surface
		umin,umax,vmin,vmax=f.ParameterRange


		u=u*0.01
		v=v*0.01
#		print ("uv neu",u,v)

		(t1,t2)=sf.tangent(u,v)
		nn=f.normalAt(u,v)

		a=np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2
#		print a
		t=FreeCAD.Vector(tuple(np.cos(np.pi*d/180)*t1+np.sin(np.pi*d/180)*t2))

		lang=int(round(lang))

		for i in range(lang+1):
			pot=sf.value(u,v)
			nn=f.normalAt(u,v)

			u2=(u-umin)/(umax-umin)
			v2=(v-vmin)/(vmax-vmin)

			pts += [pot]
			norms += [nn]
			tans += [t]

			last=sf.value(u,v)
			p2=last+t*gridsize*0.1
			(u1,v1)=sf.parameter(p2)
			(u,v)=(u1,v1)

			#restrict to area inside the Face
			if u<umin:u=umin
			if v<vmin:v=vmin
			if u>umax:u=umax
			if v>vmax:v=vmax

			uvs += [(u,v)]

			p=sf.value(u,v)

			(t1,t2)=sf.tangent(u,v)

			ta=p-last
			try: 
				ta.normalize()
				t=ta
			except:
				pass

		pts=np.array(pts)
		norms=np.array(norms)

		return pts,norms,tans



def updateDistance(fp):

	print "update distance"
	try:
		obj=fp.obj
		lang=fp.lang
		u=fp.u
		v=fp.v
	except:
		print "still not ready"
		return Part.Shape()

	f=obj.Shape.Faces[0]
	sf=f.Surface

	star=[]
	startans=[]
	starnorms=[]

	dr=24
	lang=int(round(lang/(0.1*fp.gridsize)))

	comp=[]

	for d in range(dr):
		pts,norms,tans=genRibForUpdateDistance(f,u=u,v=v,d=360/dr*d,lang=lang,gridsize=fp.gridsize)
		comp += [Part.makePolygon([FreeCAD.Vector(p) for p in pts])]

		star += [pts]
		startans += [tans]
		starnorms += [norms]


	dists=[]

	for d in range (dr):
		distd=[]
		#for i in range(lang):
		for i in range(lang+1):
			d2 = d+1 if d+1<dr else 0

			dd=FreeCAD.Vector(star[d][i]-star[d-1][i]).Length + FreeCAD.Vector(star[d][i]-star[d2][i]).Length -4*i*np.sin(0.5*np.pi/180*360/dr)

			dd=FreeCAD.Vector(star[d][i]-star[d-1][i]).Length + FreeCAD.Vector(star[d][i]-star[d2][i]).Length -4*i*np.sin(0.5*np.pi/180*360/dr)*0.1*fp.gridsize


			if fp.relativeForce:
				dd=dd/(2*i*np.sin(np.pi/180*360/dr))

			if fp.thresholdForce>0:
				if abs(dd)<fp.thresholdForce*0.01:
					dd=0
			# generelle schwelle
			if abs(dd)<0.1: dd=0

			distd += [dd]

		dists += [distd]
		h=i*np.sin(np.pi/180*360/dr)

	factor=fp.forcesize

	dists=np.array(dists)*factor
	rstar=np.array(star).swapaxes(0,1)
	rstarnorms=np.array(starnorms).swapaxes(0,1)

	cp =''
	if fp.flipNormals: nf=-1
	else: nf=1  
	for i in range(1,lang+1):
		if i %5 == 0:
			pts=[FreeCAD.Vector(tuple(p))  for p in rstar[i]]
			norms=[FreeCAD.Vector(tuple(p))  for p in rstarnorms[i]]
			pps=[]
			for j in range(len(pts))+[0]:
				#pps += [ rstar[i,j],rstar[i,j]-dists[j,i]*1*rstarnorms[i,j],rstar[i,j]]
				pps += [ rstar[i,j] ]
				
				if dists[j,i]>0:
					cp += colorPath([
						FreeCAD.Vector(rstar[i,j]),
						FreeCAD.Vector(rstar[i,j]+dists[j,i]*nf*rstarnorms[i,j])],
						color='1 1 0',name=None)


				else:
					cp += colorPath([
						FreeCAD.Vector(rstar[i,j]),
						FreeCAD.Vector(rstar[i,j]-dists[j,i]*nf*rstarnorms[i,j])],
						color='1 0 0',name=None)

				if j==dr-1: j2=0
				else: j2=j+1
				if j<dr and i>0:
					dxd=FreeCAD.Vector(0.02,0.02,0.02)

					if dists[j,i]>0: color='1 1 0'
					else: color='1 0 0'

					cp += colorPath([
							FreeCAD.Vector(star[j][i])+FreeCAD.Vector(star[j][i]-star[j2][i]).normalize()*(-1)*i*np.sin(0.5*np.pi/180*360/dr)*0.1*fp.gridsize,
							FreeCAD.Vector(star[j2][i])+FreeCAD.Vector(star[j2][i]-star[j][i]).normalize()*(-1)*i*np.sin(0.5*np.pi/180*360/dr)*0.1*fp.gridsize
							],
							color=color,name=None)

					if 1:
						cp += colorPath([
								FreeCAD.Vector(star[j][i])+dxd,
								FreeCAD.Vector(star[j][i])+dxd+FreeCAD.Vector(star[j][i]-star[j-1][i]).normalize()*(-1)*i*np.sin(0.5*np.pi/180*360/dr)*0.1*fp.gridsize
								],
								color='0 0.3 0',name=None)
						cp += colorPath([
								FreeCAD.Vector(star[j][i])+FreeCAD.Vector(star[j][i]-star[j2][i]).normalize()*(-1)*i*np.sin(0.5*np.pi/180*360/dr)*0.1*fp.gridsize,
								FreeCAD.Vector(star[j][i]),
								],
								color='0 0.4 0.',name=None)



				if 0 and i==lang:
					print ("dists absolut a promille,",j,
						round(dists[j,i]/factor,2),
						round(1000.*dists[j,i]/(i*np.pi/dr)/factor,2),i)

			comp += [Part.makePolygon([FreeCAD.Vector(p) for p in pps])]


	name="Pull_and_Press"
	drawColorLines(fp,name,cp)

	return Part.Compound(comp)

def geodesicDistance():

	obj=Gui.Selection.getSelection()[0]

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","distance")

	Geodesic(a,False)
	a.obj=obj

	# werte fuer random cylinder
	a.u=48
	a.v=45
	a.gridsize=200


	a.u=50
	a.v=50
	a.lang=100
	a.gridsize=20
	a.forcesize=10

	a.flipNormals=True

	ViewProvider(a.ViewObject)
	if obj<>None:
		a.Label="Distance for "+obj.Label
	a.mode="distance"
	
	return a

#-------------------------------
# aus Draft.py

if FreeCAD.GuiUp:
	from PySide import QtCore
	from PySide.QtCore import QT_TRANSLATE_NOOP
	gui = True

class MyDraftLabel:
	
	"The Draft Label object"
	
	def __init__(self,obj):
		obj.Proxy = self
		obj.addProperty("App::PropertyPlacement","Placement","Base",QT_TRANSLATE_NOOP("App::Property","The placement of this object"))
		obj.addProperty("App::PropertyDistance","StraightDistance","Base",QT_TRANSLATE_NOOP("App::Property","The length of the straight segment"))
		obj.addProperty("App::PropertyVector","TargetPoint","Base",QT_TRANSLATE_NOOP("App::Property","The point indicated by this label"))
		obj.addProperty("App::PropertyVectorList","Points","Base",QT_TRANSLATE_NOOP("App::Property","The points defining the label polyline"))
		obj.addProperty("App::PropertyEnumeration","StraightDirection","Base",QT_TRANSLATE_NOOP("App::Property","The direction of the straight segment")).StraightDirection = ["Horizontal","Vertical","Custom"]
		obj.addProperty("App::PropertyEnumeration","LabelType","Base",QT_TRANSLATE_NOOP("App::Property","The type of information shown by this label"))
		obj.LabelType = ["Custom","Name","Label","Position","Length","Area","Volume","Tag","Material"]
		obj.addProperty("App::PropertyLinkSub","Target","Base",QT_TRANSLATE_NOOP("App::Property","The target object of this label"))
		obj.addProperty("App::PropertyStringList","CustomText","Base",QT_TRANSLATE_NOOP("App::Property","The text to display when type is set to custom"))
		obj.addProperty("App::PropertyStringList","Text","Base",QT_TRANSLATE_NOOP("App::Property","The text displayed by this label"))

		obj.addProperty("App::PropertyLink","obj","Source","surface object")
		obj.addProperty("App::PropertyInteger","facenumber","Source", "number of the face")
		obj.addProperty("App::PropertyFloat","u","Source", "u coord start point of geodesic").u=50
		obj.addProperty("App::PropertyFloat","v","Source", "v coord start point of geodesic").v=50



		obj.setEditorMode("Text",1)
		obj.StraightDistance = 15
		obj.TargetPoint = FreeCAD.Vector(2,-1,0)
		obj.CustomText = "Label"
		self.Type = "Label"


	def execute(self,obj):
		if obj.StraightDirection != "Custom":
			p1 = obj.Placement.Base
			if obj.StraightDirection == "Horizontal":
				p2 = FreeCAD.Vector(obj.StraightDistance.Value,0,0)
			else:
				p2 = FreeCAD.Vector(0,obj.StraightDistance.Value,0)
			p2 = obj.Placement.multVec(p2)
			# p3 = obj.Placement.multVec(obj.TargetPoint)
			p3 = obj.TargetPoint
			obj.Points = [p1,p2,p3]
		if obj.LabelType == "Custom":
			if obj.CustomText:
				obj.Text = obj.CustomText
		elif obj.Target:
			if obj.LabelType == "Name":
				obj.Text = [obj.Target[0].Name]
			elif obj.LabelType == "Label":
				obj.Text = [obj.Target[0].Label]
			elif obj.LabelType == "Tag":
				if hasattr(obj.Target[0],"Tag"):
					obj.Text = [obj.Target[0].Tag]
			elif obj.LabelType == "Material":
				if hasattr(obj.Target[0],"Material"):
					if hasattr(obj.Target[0].Material,"Label"):
						obj.Text = [obj.Target[0].Material.Label]
			elif obj.LabelType == "Position":
				p = obj.Target[0].Placement.Base
				if obj.Target[1]:
					if "Vertex" in obj.Target[1][0]:
						p = obj.Target[0].Shape.Vertexes[int(obj.Target[1][0][6:])-1].Point
				obj.Text = [FreeCAD.Units.Quantity(x,FreeCAD.Units.Length).UserString for x in tuple(p)]
			elif obj.LabelType == "Length":
				if obj.Target[0].isDerivedFrom("Part::Feature"):
					if hasattr(obj.Target[0].Shape,"Length"):
						obj.Text = [FreeCAD.Units.Quantity(obj.Target[0].Shape.Length,FreeCAD.Units.Length).UserString]
					if "Edge" in obj.Target[1][0]:
						obj.Text = [FreeCAD.Units.Quantity(obj.Target[0].Shape.Edges[int(obj.Target[1][0][4:])-1].Length,FreeCAD.Units.Length).UserString]
			elif obj.LabelType == "Area":
				if obj.Target[0].isDerivedFrom("Part::Feature"):
					if hasattr(obj.Target[0].Shape,"Area"):
						obj.Text = [FreeCAD.Units.Quantity(obj.Target[0].Shape.Area,FreeCAD.Units.Area).UserString]
					if "Face" in obj.Target[1][0]:
						obj.Text = [FreeCAD.Units.Quantity(obj.Target[0].Shape.Faces[int(obj.Target[1][0][4:])-1].Area,FreeCAD.Units.Area).UserString]
			elif obj.LabelType == "Volume":
				if obj.Target[0].isDerivedFrom("Part::Feature"):
					if hasattr(obj.Target[0].Shape,"Volume"):
						obj.Text = [FreeCAD.Units.Quantity(obj.Target[0].Shape.Volume,FreeCAD.Units.Volume).UserString]

		try: _=obj.obj.Shape
		except: return
		
		try:
			f=obj.obj.Shape.Faces[obj.facenumber]
			sf=f.Surface
			umin,umax,vmin,vmax=f.ParameterRange

			u=umin-(umin-umax)*obj.u/100
			v=vmin-(vmin-vmax)*obj.v/100
	#		print ("uv neu  aa",u,v)
			obj.TargetPoint=obj.obj.Shape.Faces[obj.facenumber].Surface.value(u,v)

		except:
			f=obj.obj.Shape.Edges[obj.facenumber]
			sf=f.Curve
			umin,umax=f.ParameterRange

			u=umin-(umin-umax)*obj.u/100
#			v=vmin-(vmin-vmax)*obj.v/100
			print ("u neu  aa",u)
			obj.TargetPoint=obj.obj.Shape.Edges[obj.facenumber].Curve.value(u)


		obj.CustomText=[obj.Label,str((round(obj.TargetPoint.x,1),round(obj.TargetPoint.y,1),round(obj.TargetPoint.z,1))),str((obj.u,obj.v))]
		obj.CustomText=[obj.Label]

	def onChanged(self,obj,prop):
		if prop in ['u','v','Label']:
			self.execute(obj)
		pass

	def __getstate__(self):
		return self.Type

	def __setstate__(self,state):
		if state:
			self.Type = state


class MyViewProviderDraftLabel:

	"A View Provider for the Draft Label"

	def __init__(self,vobj):
		vobj.addProperty("App::PropertyLength","TextSize","Base",QT_TRANSLATE_NOOP("App::Property","The size of the text"))
		vobj.addProperty("App::PropertyFont","TextFont","Base",QT_TRANSLATE_NOOP("App::Property","The font of the text"))
		vobj.addProperty("App::PropertyLength","ArrowSize","Base",QT_TRANSLATE_NOOP("App::Property","The size of the arrow"))
		vobj.addProperty("App::PropertyEnumeration","TextAlignment","Base",QT_TRANSLATE_NOOP("App::Property","The vertical alignment of the text"))
		vobj.addProperty("App::PropertyEnumeration","ArrowType","Base",QT_TRANSLATE_NOOP("App::Property","The type of arrow of this label"))
		vobj.addProperty("App::PropertyEnumeration","Frame","Base",QT_TRANSLATE_NOOP("App::Property","The type of frame around the text of this object"))
		vobj.addProperty("App::PropertyFloat","LineWidth","Base",QT_TRANSLATE_NOOP("App::Property","Line width"))
		vobj.addProperty("App::PropertyColor","LineColor","Base",QT_TRANSLATE_NOOP("App::Property","Line color"))
		vobj.addProperty("App::PropertyColor","TextColor","Base",QT_TRANSLATE_NOOP("App::Property","Text color"))
		vobj.addProperty("App::PropertyInteger","MaxChars","Base",QT_TRANSLATE_NOOP("App::Property","The maximum number of characters on each line of the text box"))
		vobj.Proxy = self
		self.Object = vobj.Object
		vobj.TextAlignment = ["Top","Middle","Bottom"]
		vobj.TextAlignment = "Middle"
		vobj.LineWidth = 1#getParam("linewidth",1)
		#vobj.TextFont = getParam("textfont")
		vobj.TextSize = 10 #getParam("textheight",1)
		vobj.ArrowSize = 1 # getParam("arrowsize",1)
		# vobj.ArrowType = arrowtypes
		# vobj.ArrowType = arrowtypes[getParam("dimsymbol")]
		vobj.Frame = ["None","Rectangle"]

	def getIcon(self):
		import Draft_rc
#		try: 
#			if self.upd: return ":/icons/DraftWorkbench.svg"
#1		except: pass
		return ":/icons/Draft_Label.svg"



	def claimChildren(self):
		return []

	def attach(self,vobj):
		self.arrow = coin.SoSeparator()
		self.arrowpos = coin.SoTransform()
		self.arrow.addChild(self.arrowpos)
		self.matline = coin.SoMaterial()
		self.drawstyle = coin.SoDrawStyle()
		self.drawstyle.style = coin.SoDrawStyle.LINES
		self.lcoords = coin.SoCoordinate3()
		self.line = coin.SoType.fromName("SoBrepEdgeSet").createInstance()
		self.mattext = coin.SoMaterial()
		textdrawstyle = coin.SoDrawStyle()
		textdrawstyle.style = coin.SoDrawStyle.FILLED
		self.textpos = coin.SoTransform()
		self.font = coin.SoFont()
		self.text2d = coin.SoText2()
		self.text3d = coin.SoAsciiText()
		self.text2d.string = self.text3d.string = "Label" # need to init with something, otherwise, crash!
		self.text2d.justification = coin.SoText2.RIGHT
		self.text3d.justification = coin.SoAsciiText.RIGHT
		self.fcoords = coin.SoCoordinate3()
		self.frame = coin.SoType.fromName("SoBrepEdgeSet").createInstance()
		self.node2d = coin.SoGroup()
		self.node2d.addChild(self.matline)
		self.node2d.addChild(self.arrow)
		self.node2d.addChild(self.drawstyle)
		self.node2d.addChild(self.lcoords)
		self.node2d.addChild(self.line)
		self.node2d.addChild(self.arrow)
		self.node2d.addChild(self.mattext)
		self.node2d.addChild(textdrawstyle)
		self.node2d.addChild(self.textpos)
		self.node2d.addChild(self.font)
		self.node2d.addChild(self.text2d)
		self.node2d.addChild(self.fcoords)
		self.node2d.addChild(self.frame)
		self.node3d = coin.SoGroup()
		self.node3d.addChild(self.matline)
		self.node3d.addChild(self.arrow)
		self.node3d.addChild(self.drawstyle)
		self.node3d.addChild(self.lcoords)
		self.node3d.addChild(self.line)
		self.node3d.addChild(self.arrow)
		self.node3d.addChild(self.mattext)
		self.node3d.addChild(textdrawstyle)
		self.node3d.addChild(self.textpos)
		self.node3d.addChild(self.font)
		self.node3d.addChild(self.text3d)
		self.node3d.addChild(self.fcoords)
		self.node3d.addChild(self.frame)
		vobj.addDisplayMode(self.node2d,"2D text")
		vobj.addDisplayMode(self.node3d,"3D text")
		self.onChanged(vobj,"LineColor")
		self.onChanged(vobj,"TextColor")
		self.onChanged(vobj,"ArrowSize")

	def getDisplayModes(self,vobj):
		return ["2D text","3D text"]

	def getDefaultDisplayMode(self):
		return "2D text"

	def setDisplayMode(self,mode):
		return mode

	def updateData(self,obj,prop):

		try: self.upd
		except: self.upd=True
		self.upd=not self.upd

		if prop == "Points":
			if len(obj.Points) >= 2:
				self.line.coordIndex.deleteValues(0)
				self.lcoords.point.setValues(obj.Points)
				self.line.coordIndex.setValues(0,len(obj.Points),range(len(obj.Points)))
				self.onChanged(obj.ViewObject,"TextSize")
				self.onChanged(obj.ViewObject,"ArrowType")
			if obj.StraightDistance > 0:
				self.text2d.justification = coin.SoText2.RIGHT
				self.text3d.justification = coin.SoAsciiText.RIGHT
			else:
				self.text2d.justification = coin.SoText2.LEFT
				self.text3d.justification = coin.SoAsciiText.LEFT
		elif prop == "Text":
			if obj.Text:
				self.text2d.string.setValues([l.encode("utf8") for l in obj.Text if l])
				self.text3d.string.setValues([l.encode("utf8") for l in obj.Text if l])
				self.onChanged(obj.ViewObject,"TextAlignment")

	def getTextSize(self,vobj):
		if vobj.DisplayMode == "3D text":
			text = self.text3d
		else:
			text = self.text2d
		v = FreeCADGui.ActiveDocument.ActiveView.getViewer().getSoRenderManager().getViewportRegion()
		b = coin.SoGetBoundingBoxAction(v)
		text.getBoundingBox(b)
		return b.getBoundingBox().getSize().getValue()

	def onChanged(self,vobj,prop):
		if prop == "LineColor":
			if hasattr(vobj,"LineColor"):
				l = vobj.LineColor
				self.matline.diffuseColor.setValue([l[0],l[1],l[2]])
		elif prop == "TextColor":
			if hasattr(vobj,"TextColor"):
				l = vobj.TextColor
				self.mattext.diffuseColor.setValue([l[0],l[1],l[2]])
		elif prop == "LineWidth":
			if hasattr(vobj,"LineWidth"):
				self.drawstyle.lineWidth = vobj.LineWidth
		elif (prop == "TextFont"):
			if hasattr(vobj,"TextFont"):
				self.font.name = vobj.TextFont.encode("utf8")
		elif prop in ["TextSize","TextAlignment"]:
			if hasattr(vobj,"TextSize") and hasattr(vobj,"TextAlignment"):
				self.font.size = vobj.TextSize.Value
				v = FreeCAD.Vector(1,0,0)
				if vobj.Object.StraightDistance > 0:
					v = v.negative()
				v.multiply(vobj.TextSize/10)
				tsize = self.getTextSize(vobj)
				if len(vobj.Object.Text) > 1:
					v = v.add(FreeCAD.Vector(0,(tsize[1]-1)*2,0))
				if vobj.TextAlignment == "Top":
					v = v.add(FreeCAD.Vector(0,-tsize[1]*2,0))
				elif vobj.TextAlignment == "Middle":
					v = v.add(FreeCAD.Vector(0,-tsize[1],0))
				v = vobj.Object.Placement.Rotation.multVec(v)
				pos = vobj.Object.Placement.Base.add(v)
				self.textpos.translation.setValue(pos)
				self.textpos.rotation.setValue(vobj.Object.Placement.Rotation.Q)
		elif prop == "ArrowType":
			if hasattr(vobj,"ArrowType"):
				if len(vobj.Object.Points) > 1:
					if hasattr(self,"symbol"):
						if self.arrow.findChild(self.symbol) != -1:
								self.arrow.removeChild(self.symbol)
					s = arrowtypes.index(vobj.ArrowType)
					self.symbol = dimSymbol(s)
					self.arrow.addChild(self.symbol)
					self.arrowpos.translation.setValue(vobj.Object.Points[-1])
					v1 = vobj.Object.Points[-2].sub(vobj.Object.Points[-1])
					if not DraftVecUtils.isNull(v1):
						v1.normalize()
						import DraftGeomUtils
						v2 = FreeCAD.Vector(0,0,1)
						if round(v2.getAngle(v1),4) in [0,round(math.pi,4)]:
							v2 = FreeCAD.Vector(0,1,0)
						v3 = v1.cross(v2).negative()
						q = FreeCAD.Placement(DraftVecUtils.getPlaneRotation(v1,v3,v2)).Rotation.Q
						self.arrowpos.rotation.setValue((q[0],q[1],q[2],q[3]))
		elif prop == "ArrowSize":
			if hasattr(vobj,"ArrowSize"):
				s = vobj.ArrowSize.Value
				if s:
					self.arrowpos.scaleFactor.setValue((s,s,s))
		elif prop == "Frame":
			if hasattr(vobj,"Frame"):
				self.frame.coordIndex.deleteValues(0)
				if vobj.Frame == "Rectangle":
					tsize = self.getTextSize(vobj)
					pts = []
					base = vobj.Object.Placement.Base.sub(FreeCAD.Vector(self.textpos.translation.getValue().getValue()))
					pts.append(base.add(FreeCAD.Vector(0,tsize[1]*3,0)))
					pts.append(pts[-1].add(FreeCAD.Vector(-tsize[0]*6,0,0)))
					pts.append(pts[-1].add(FreeCAD.Vector(0,-tsize[1]*6,0)))
					pts.append(pts[-1].add(FreeCAD.Vector(tsize[0]*6,0,0)))
					pts.append(pts[0])
					self.fcoords.point.setValues(pts)
					self.frame.coordIndex.setValues(0,len(pts),range(len(pts)))

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None




def makeLabel(targetpoint=None,target=None,direction=None,distance=None,labeltype=None,placement=None):
	obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython","MyLabel")
	MyDraftLabel(obj)
	if FreeCAD.GuiUp:
		MyViewProviderDraftLabel(obj.ViewObject)
	if targetpoint:
		obj.TargetPoint = targetpoint
	if target:
		obj.Target = target
	if direction:
		obj.StraightDirection = direction
	if distance:
		obj.StraightDistance = distance
	if labeltype:
		obj.LabelType = labeltype
	if placement:
		obj.Placement = placement
	FreeCAD.ActiveDocument.recompute()
	return obj






# fuer messpunkte zum andocken
def createMarker(u=20,v=50):
	'''create Label'''

	l = makeLabel(direction='Horizontal',labeltype='Position')
	l.obj=Gui.Selection.getSelection()[0]
	l.LabelType = u"Custom"
	l.Label="MyMarker"
	l.ViewObject.DisplayMode = u"2D text"
	l.ViewObject.TextSize = '15 mm'
	App.activeDocument().recompute()
	l.u=u
	l.v=v
	try:
		l.TargetPoint=l.obj.Shape.Faces[0].Surface.value(l.u*0.01,l.v*0.01)
	except:
		l.TargetPoint=l.obj.Shape.Edges[0].Curve.value(l.u*0.01)
	hideAllProps(l,pns=['Text','CustomText','LabelType'])
	return l








def findGeodesicToTarget(start=None,target=None,d=10):

	print 
	print "step"

	if start==None:
		start=Gui.Selection.getSelection()[0]
	if target==None:
		target=Gui.Selection.getSelection()[1]

	assert start.obj == target.obj
	assert start.facenumber == target.facenumber

	f=start.obj.Shape.Faces[start.facenumber]

	pt=target.TargetPoint
	u=start.u
	v=start.v

	sf=f.Surface

	print "Start:",start.TargetPoint
	print "Ziel:",target.TargetPoint
	print ("----------",u,v)
 
	lang=30
	minl=10**10

	def runfak(lang,d,fak,anz,minl):
		for i in range(anz):
			if i==0: minp=[lang,d]
			print ("------------",i,minp, minl)
			print 
			ta=time.time()
			found=False
			faktor=fak
			for dd in [-1,0,1]:
				for dl in [-1,0,1]:
						if lang+faktor*dl <=0: continue
						pts,norms,tans=genRibForUpdateDistance(f,u=u,v=v,d=d+faktor*dd,lang=lang+faktor*dl,gridsize=10)
						ptsa=[FreeCAD.Vector(tuple(p)) for p in pts]
						la=(pt-ptsa[-1]).Length
						if la<minl:
							minl=la
							minp=[lang+faktor*dl,d+faktor*dd]
							print ("wechsel ",minp)
							found=True

						cp=colorPath(ptsa,color='0 1 0',name=None)
						name="A_"+str(lang+faktor*dl)+"_"+str(d+faktor*dd)
						name="A_"
						drawColorLines(start.obj,name,cp)

			[lang,d]=minp
			[lange,de]=minp
			Gui.updateGui()
			dti=time.time()-ta
			print ("Loop time ",dti,len(pts),dti/len(pts))
			if not found: 
				print "nichts mehr gefunden"
				break

		print (lange,de)

		pts,norms,tans=genRibForUpdateDistance(f,u=u,v=v,d=de,lang=lange,gridsize=10)

		#display the current path
		ptsa=[FreeCAD.Vector(tuple(p)) for p in pts]
		cp2=colorPath(ptsa,color='1 0 0',name=None)
		name="A_"
		drawColorLines(start.obj,name,cp2)

		return [lange,de,minl]

	if 10:
		anz=20
		fak=10
		[lang,d,minl]=runfak(lang,d,fak,anz,minl)
		print (lang,d,"distance",minl)

	if 10:
		anz=14
		fak=1
		[lang,d,minl]=runfak(lang,d,fak,anz,minl)
		print
		print ("lang,direction:",lang,d,"distance:",minl)






	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Geodesic")

	Geodesic(a)
	a.obj=start.obj
	ViewProvider(a.ViewObject)

	a.Label="Geodesic on " + a.obj.Label + " from "+start.Label +  " to " + target.Label
	a.mode="geodesic"

	a.lang=lang
	a.lang2=0
	a.lang3=0
	a.direction=d
	a.ut=target.u
	a.vt=target.v
	a.u=start.u
	a.v=start.v
	





def createShoeMarkers():

	markers=[

	'A2',4,76,
	'A',4,50.5,
	'A1',4,26,
	
	'J',20,50.4,
	'J1',22,26,
	'J2',20,76,

	'I1',30.9,26,
	'I2',30.9,76,

	'E',51.54,50.6,
	'G',30.9,50.6,

	# Ferse
	'HF1',98.,29.,
	'HF2',98.,70.,

	'H1',98.,40.,
	'H2',98.,60.,


	# Knoechel
	'K2', 70.,60.,
	'K1', 70.,40.,


	'KF2', 70.,70.,
	'KF1', 70.,30.,

	
	
	]
	da=3
	db=len(markers)/da
	markers=np.array(markers).reshape(db,da)# [:3]


	for m in markers:
		print "!",m

		l = makeLabel(
			targetpoint=FreeCAD.Vector (0.0, -18.226360321044922, 53.260826110839844),
			direction='Horizontal',
			labeltype='Position',
		)
		l.obj=App.ActiveDocument.Poles
		l.LabelType = u"Custom"
		l.Label=m[0]
		l.ViewObject.DisplayMode = u"2D text"
		l.ViewObject.TextSize = '15 mm'
		l.u,l.v=float(m[1]),float(m[2])
		App.activeDocument().recompute()
		App.activeDocument().recompute()
		l.Placement.Base=FreeCAD.Vector(l.TargetPoint.x,l.TargetPoint.y*3,l.TargetPoint.z+30)
		l.ViewObject.LineColor=(1.0,.6,0.)
		l.ViewObject.LineWidth=4.
		App.activeDocument().recompute()



def connectMarkers():

	connList=[
				('A2','A'),	('J2','J'),	('I2','G'),
				('A','J'), ('J','G'),
				('J2','A2'),('I2','J2'),
				('G','E'),('E','K2'),('KF2','K2'),('KF2','I2'),
				('HF2','KF2'),
				('H2','HF2'),
				('K2','H2'),
			]

	for a,b in connList:

		al=App.ActiveDocument.getObjectsByLabel(a)
		aob=al[0]
		bl=App.ActiveDocument.getObjectsByLabel(b)
		bob=bl[0]
		if a=='HF2' and b=='KF2':connectMarkers(aob,bob,d=190)
		elif a=='H2' and b=='HF2':connectMarkers(aob,bob,d=190)
		else:connectMarkers(aob,bob)
		App.activeDocument().recompute()
