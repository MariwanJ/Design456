import FreeCAD as App

try:
        App.closeDocument("Unnamed")
except:
        pass

try:
        App.newDocument("Unnamed")
        App.setActiveDocument("Unnamed")
        App.ActiveDocument=App.getDocument("Unnamed")
        Gui.ActiveDocument=Gui.getDocument("Unnamed")
except:
        pass


helper
#reload(helper)

nurbs
#reload(nurbs)

nurbs.testRandomB()
hp=helper.makeHelper()

hp.source=App.ActiveDocument.Nurbs

hp.mode="isoGrid"
hp.Proxy.create_knotes_shape2()

hp.mode='poleGrid'
hp.Placement.Base.x=1200


hp.mode='Surface'
hp.Placement.Base.x=1200



