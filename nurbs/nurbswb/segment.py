'''create a segment of s bspline surface'''

# -*- coding: utf-8 -*-
#-- microelly 2017 v 0.1
#-- GNU Lesser General Public License (LGPL)


##\cond

from say import *
import nurbswb.pyob


##\endcond

## Segment eines BSpline als parametrisches Part::FeaturePython


class Segment(nurbswb.pyob.FeaturePython):
	'''Segment einer bspline Flaeche oder Kurve
	Einschraenkung:
	es wird die erste Flaeche Face1 bzw. die erste Kante Edge1 verarbeitet
	'''

	##\cond
	def __init__(self, obj):
		nurbswb.pyob.FeaturePython.__init__(self, obj)

		obj.addProperty("App::PropertyLink", "source", "Base")
		obj.addProperty("App::PropertyInteger", "umin", "Base")
		obj.addProperty("App::PropertyInteger", "umax", "Base")
		obj.addProperty("App::PropertyInteger", "vmin", "Base")
		obj.addProperty("App::PropertyInteger", "vmax", "Base")
		obj.addProperty("App::PropertyBool", "closeV", "Base")

		obj.umax=-1
		obj.vmax=-1

		self.obj2=obj
		nurbswb.pyob.ViewProvider(obj.ViewObject)
	##\endcond

	## Die Properties umin, umax, vmin, vmax werden als Nummern der begrenzenden Knoten interpretiert
	# 


	def execute(self, obj):

		if  len(obj.source.Shape.Faces) >= 1:
			face=obj.source.Shape.Face1
			bs=face.Surface.copy()
			uks=bs.getUKnots()
			vks=bs.getVKnots()
			bs.segment(uks[obj.umin],uks[obj.umax],vks[obj.vmin],vks[obj.vmax])
		else:
			edge=obj.source.Shape.Edge1
			bs=edge.Curve.copy()
			ks=bs.getKnots()
			bs.segment(ks[obj.umin],ks[obj.umax])

		if obj.closeV:
			bs.setVPeriodic()

		obj.Shape=bs.toShape()


def createSegment(name="MySegment"):
	'''erzeugt ein Segment aus der source Flaeche oder Kurve
	Segmente sind nur fuer die gegebenen Knoten moeglich
	umin, ... vmax: Eingabe der Knotennummer
	'''

	ffobj = FreeCAD.activeDocument().addObject(
		"Part::FeaturePython", name)
	Segment(ffobj)
	return ffobj


## Modifikation eines BSpline als parametrisches Part::FeaturePython

class NurbsTrafo(nurbswb.pyob.FeaturePython):
	'''Rotieren des Pole-array, um die Naht zu verschieben'''

	##\cond
	def __init__(self, obj):
		nurbswb.pyob.FeaturePython.__init__(self, obj)

		obj.addProperty("App::PropertyLink", "source", "Base")
		obj.addProperty("App::PropertyInteger", "start", "Base")
		obj.addProperty("App::PropertyInteger", "umax", "Base")
		obj.addProperty("App::PropertyInteger", "vmin", "Base")
		obj.addProperty("App::PropertyInteger", "vmax", "Base")
		obj.addProperty("App::PropertyBool", "swapaxes", "Base").swapaxes=True


		obj.umax=-1
		obj.vmax=-1
		self.obj2=obj
		nurbswb.pyob.ViewProvider(obj.ViewObject)
	##\endcond

	def execute(proxy, obj):
		''' rotiert die Pole '''
		if  len(obj.source.Shape.Faces) >= 1:
			face=obj.source.Shape.Face1
			bs=face.Surface.copy()

			poles=bs.getPoles()
			ku=bs.getUKnots()
			kv=bs.getVKnots()
			mu=bs.getUMultiplicities()
			mv=bs.getVMultiplicities()
			perU=bs.isUPeriodic()
			perV=bs.isVPeriodic()

			k=obj.start
#			if not bs.isVPeriodic():
#				print "nicht vperiodic - kann nichts tun - Abbruch"
#				return

			if obj.swapaxes:
				y=np.array(poles).swapaxes(0,1)
				poles2=np.concatenate([y[k:],y[:k]]).swapaxes(0,1)
				poles2=np.concatenate([y[k:-1],y[:k+1]]).swapaxes(0,1)
			else:
				y=np.array(poles)
				poles2=np.concatenate([y[k:],y[:k]])

			print poles2
			FreeCAD.poles2=poles
			print ku
			print kv

			bs2=Part.BSplineSurface()
			bs2.buildFromPolesMultsKnots(poles2,
				mu,mv,
				ku,kv,
				perU,perV,3,3,)

			obj.Shape=bs2.toShape()

		else:
			bc=obj.source.Shape.Edge1.Curve.copy()
			pols=bc.getPoles()

			multies=bc.getMultiplicities()
			knots=bc.getKnots()
			deg=bc.Degree

			i=obj.start
			pols2=pols[i:] +pols[:i]
			bc.buildFromPolesMultsKnots(pols2,multies,knots,True,deg)

			obj.Shape=bc.toShape()



def createNurbsTrafo(name="MyNurbsTafo"):
	''' erzeugt ein NurbsTrafo Objekt '''

	ffobj = FreeCAD.activeDocument().addObject(
		"Part::FeaturePython", name)
	NurbsTrafo(ffobj)
	return ffobj

## Feines Segment eines BSpline als parametrisches Part::FeaturePython




class FineSegment(nurbswb.pyob.FeaturePython):
	''' erzeugt ein feines Segment, dass feienr ist als die normale Segmentierung des nurbs
	factor gibt die Anzahl der Abstufungen an
	die Zahlen umin, ... vmax sind ganzzahlige Anteile von factor
	'''

	##\cond
	def __init__(self, obj):
		nurbswb.pyob.FeaturePython.__init__(self, obj)

		obj.addProperty("App::PropertyLink", "source", "Base")
		obj.addProperty("App::PropertyInteger", "factor", "Base")
		obj.addProperty("App::PropertyInteger", "umin", "Base")
		obj.addProperty("App::PropertyInteger", "umax", "Base")
		obj.addProperty("App::PropertyInteger", "vmin", "Base")
		obj.addProperty("App::PropertyInteger", "vmax", "Base")

		obj.factor=100

		obj.umin=0
		obj.vmin=0
		obj.umax=obj.factor
		obj.vmax=obj.factor

		self.obj2=obj
		nurbswb.pyob.ViewProvider(obj.ViewObject)
	##\endcond

#	def execute(proxy, obj):
#		pass

	## Die Properties umin, umax, vmin, vmax werden durch factor geteilt
	# und dann als der begrenzenden Knoten interpretiert
	#
	# FineSegment kann bei einem grossen wert von *factor* sehr genau zuschneiden
	#


	def onChanged(self, obj, prop):
		if prop in ["vmin","vmax","umin","umax","source"]:

			if obj.source == None: return

			face=obj.source.Shape.Face1
			bs=face.Surface.copy()
#			bs.setUNotPeriodic()
#			bs.setVNotPeriodic()

			if obj.umin<0: obj.umin=0
			if obj.vmin<0: obj.vmin=0
			
			if obj.umax>obj.factor: obj.umax=obj.factor
			if obj.vmax>obj.factor: obj.vmax=obj.factor
			if obj.umin>obj.umax: obj.umin=obj.umax
			if obj.vmin>obj.vmax: obj.vmin=obj.vmax

			umin=1.0/obj.factor*obj.umin
			umax=1.0/obj.factor*obj.umax
			vmin=1.0/obj.factor*obj.vmin
			vmax=1.0/obj.factor*obj.vmax

			if bs.isVPeriodic() and not vmax< bs.getVKnots()[-1]:
				vmax=bs.getVKnots()[-1]
# geht so nicht: 
#				obj.vmax=int(round(vmax*obj.factor,0))

			if bs.isUPeriodic() and not umax< bs.getUKnots()[-1]:
				umax=bs.getUKnots()[-1]
#				obj.umax=int(round(umax*obj.factor,0))

#			print  bs.getUKnots()
#			print  bs.getVKnots()
#			print ("interval",umin,umax,vmin,vmax)

			if umin>0 and umin not in bs.getUKnots():
				bs.insertUKnot(umin,1,0)

			if umax<obj.factor and umax not in bs.getUKnots():
				bs.insertUKnot(umax,1,0)

			if vmin>0 and vmin not in bs.getVKnots():
				bs.insertVKnot(vmin,1,0)

			if vmax<obj.factor and vmax not in bs.getVKnots(): # and vmax< bs.getVKnots()[-1]:
				bs.insertVKnot(vmax,1,0)

			uks=bs.getUKnots()
			if umin<uks[0]: umin=uks[0]
			
#			print ("interval",umin,umax,vmin,vmax)
			bs.segment(umin,umax,vmin,vmax)
			obj.Shape=bs.toShape()



def createFineSegment(name="MyFineSegment"):
	''' erzeugt ein FineSegment Objekt '''

	ffobj = FreeCAD.activeDocument().addObject("Part::FeaturePython", name)
	FineSegment(ffobj)
	return ffobj



def runsegment():
	'''Anwendungsfall fuer die Gui.Selection wird ein Segment erzeugt'''

	source=None
	if len( Gui.Selection.getSelection())<>0:
		source=Gui.Selection.getSelection()[0]
	s=createSegment()
	s.source=source
	sm.umax=-2
	sm.umin=2

def runfinesegment():
	'''Anwendungsfall fuer die Gui.Selection wird ein FineSegement erzeugt'''

	source=None
	if len( Gui.Selection.getSelection())<>0:
		source=Gui.Selection.getSelection()[0]
	s=createFineSegment()
	s.source=source

def runnurbstrafo():
	'''Anwendungsfall fuer die Gui.Selection wird ein NurbsTrafo erzeugt'''

	source=None
	if len( Gui.Selection.getSelection())<>0:
		source=Gui.Selection.getSelection()[0]
	s=createNurbsTrafo()
	s.source=source




##\cond
if __name__ == '__main__':

	sm=createSegment()
	sm.source=App.ActiveDocument.Poles
	sm.umax=5

	k=createFineSegment()
	k.source=App.ActiveDocument.Poles


	s=createNurbsTrafo()
	s.source=App.ActiveDocument.Poles




##\endcond

