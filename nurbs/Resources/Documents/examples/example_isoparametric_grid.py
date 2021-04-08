import nurbswb

reload(nurbswb.nurbs_tools)
from nurbswb.nurbs_tools import *


bs=App.ActiveDocument.Nurbs.Shape.Surface

for u in range(11):
    showIsoparametricUCurve(bs,1.0/10*u)

for v in range(11):
    showIsoparametricVCurve(bs,1.0/10*v)

