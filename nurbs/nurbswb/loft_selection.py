
import FreeCAD
import FreeCADGui as Gui


from FreeCAD import Base
import Part
App=FreeCAD



# todo: parametric source
# flags 

def runOnEdges():
    '''version bei selektierten geschlossenen Kanten'''

    import FreeCADGui as Gui
    import Part
    wx=Gui.Selection.getSelectionEx()
    
    sls=[]
    for w in wx:
        sob=w.SubObjects[0]
        if  sob.__class__.__name__ == 'Face':
            sls += [w.SubObjects[0].Wires[0]]
        else:
            sls += [w.SubObjects[0]]


    l=Part.makeLoft(sls,True,True,False)

    Part.show(l)


def run():
    ribs=Gui.Selection.getSelection()

    l=App.ActiveDocument.addObject('Part::Loft','Loft')
    l.Ruled = True
    l.Sections=ribs
    App.activeDocument().recompute()


