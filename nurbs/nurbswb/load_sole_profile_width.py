
'''
load width information for a sole from a sketcher file
filename is 'User parameter:Plugins/shoe').GetString("width profile")
there must be one sketch in it with constraints  l1-l12, r1-r12
'''


import FreeCAD
import FreeCADGui

import os
import nurbswb

import nurbswb.spreadsheet_lib
reload(nurbswb.spreadsheet_lib)
import nurbswb.sole
reload(nurbswb.sole)


from nurbswb.spreadsheet_lib import cellname

# from nurbswb.errors import sayexc
from nurbswb.say import *


def runa():
	''' load the data from the first sketch in file fn
	writes the data into the spreadsheet 
	and recomputes the sole
	'''

#	raise Exception("test fehler")
	aktiv = App.ActiveDocument

	fna = App.ParamGet(
		'User parameter:Plugins/shoe').GetString("width profile")
	if fna == '':
		__dir__ = os.path.dirname(nurbswb.__file__)
		fna = __dir__ + "/../testdata/breitev3.fcstd"
		App.ParamGet('User parameter:Plugins/shoe').SetString(
			"width profile", fna)

	dok = App.open(fna)
	sss = dok.findObjects("Sketcher::SketchObject")
	s = sss[0]

	# werte aus sketch holen
	rs = []
	ls = []
	for i in range(1, 12):
		rs += [s.getDatum('r' + str(i)).Value]
		ls += [s.getDatum('l' + str(i)).Value]

	App.closeDocument(dok.Name)

	# eigentliche Arbeitsdatei
	dok2 = aktiv
	App.setActiveDocument(dok2.Name)

	sss = dok2.findObjects("Sketcher::SketchObject")
#	print sss,dok2.Name
	ss = dok2.Spreadsheet

	# daten ins spreadsheet
	for s in range(1, 12):
		cn = cellname(s + 1, 14)
		ss.set(cn, str(rs[s - 1]))
		cn = cellname(s + 1, 15)
		ss.set(cn, str(ls[s - 1]))

	# aktualisieren
	dok2.recompute()
	nurbswb.sole.run()
	dok2.recompute()


def run():
	''' run with error handling'''
	try:
		runa()
	except:
		sayexc2(
			__name__, "was ist los--------------------------------------------------------------------")
