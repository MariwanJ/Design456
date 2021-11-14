import os
import sys
from types import coroutine
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
from typing import List
from ThreeDWidgets.constant import FR_COLOR
# draw a line in 3D world
import math



def draw_2Darrow_DoubleSided(p1=App.Vector(0,0,0),
                             color=FR_COLOR.FR_GOLD,
                             scale=[0.5,0.5,0.5],type=0,opacity=0,
                             _rotation=[0.0, 0.0, 1.0, 0.0]):
    """[2D Arrow]

    Args:
        p1 ([App.Vector], optional): [Position of the arrow]. Defaults to App.Vector(0,0,0).
        color ((float,float,float)), optional): [RGB Value between 0 to 1]. Defaults to FR_COLOR.FR_GOLD.
        scale ((float,float,float)), optional): [Scale factor for each axis]. Defaults to (1,1,1).
        type (int, optional): [Arrow type. At the moment there are 2 types]. Defaults to 1.
        opacity (int, optional): [Opacity of the drawn arrow]. Defaults to 0.
        _rotation (list, optional): [Rotation of the arrow provided by three float and an angle (float) in degree]. Defaults to [1.0, 0.0, 0.0, 0.0].

    Returns:
        [SoSeparator]: [SoSeparator which hold the drawing. Add it to the scenegraph to show the arrow]
    """    
    try:
        root=coin.SoSeparator() 
        transform=coin.SoTransform()
        trans=coin.SoTranslation()
        trans.translation.setValue(p1)
        transform.rotation.setValue(_rotation)
        transform.translation.setValue(p1)
        transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
        material = coin.SoMaterial()
        material.transparency.setValue(opacity)
        material.diffuseColor.setValue(coin.SbColor(color))
        
        soSepArrow=coin.SoSeparator()   # drawing holder
        soIndexFace= coin.SoIndexedFaceSet()
        cordinate= coin.SoCoordinate3()
        vertexPositions=[
            
            
        ]
        
        cordinate.point.setValues(0, 61, vertexPositions)
        indices= [ 104, 98, 103, -1, 99, 100, 98, -1,
              103, 96, 102, -1, 98, 96, 103, -1,
              100, 96, 98, -1, 1, 2, 0, -1,
              97, 93, 96, -1, 108, 6, 1, -1,
              1, 6, 2, -1, 108, 5, 6, -1,
              93, 94, 96, -1, 94, 95, 96, -1,
              96, 92, 102, -1, 95, 92, 96, -1,
              108, 4, 5, -1, 4, 12, 3, -1,
              109, 12, 108, -1, 108, 12, 4, -1,
              109, 11, 12, -1, 11, 9, 10, -1,
              109, 9, 11, -1, 109, 8, 9, -1,
              106, 7, 105, -1, 107, 7, 106, -1,
              105, 7, 109, -1, 109, 7, 8, -1,
              101, 13, 107, -1, 107, 13, 7, -1,
              102, 14, 101, -1, 101, 14, 13, -1,
              14, 16, 15, -1, 17, 20, 18, -1,
              18, 20, 19, -1, 16, 76, 17, -1,
              92, 76, 102, -1, 102, 76, 14, -1,
              14, 76, 16, -1, 76, 88, 77, -1,
              77, 88, 78, -1, 92, 88, 76, -1,
              81, 79, 80, -1, 78, 79, 81, -1,
              89, 79, 88, -1, 88, 79, 78, -1,
              91, 82, 90, -1, 89, 83, 79, -1,
              82, 83, 90, -1, 79, 83, 87, -1,
              90, 83, 89, -1, 87, 85, 86, -1,
              83, 84, 87, -1, 87, 84, 85, -1,
              30, 33, 29, -1, 31, 33, 30, -1,
              32, 33, 31, -1, 33, 25, 29, -1,
              29, 36, 28, -1, 28, 36, 37, -1,
              25, 35, 29, -1, 29, 35, 36, -1,
              26, 27, 25, -1, 25, 34, 35, -1,
              27, 24, 25, -1, 25, 24, 34, -1,
              24, 23, 34, -1, 23, 22, 34, -1,
              75, 73, 72, -1, 74, 73, 75, -1,
              72, 71, 21, -1, 21, 69, 22, -1,
              71, 69, 21, -1, 70, 69, 71, -1,
              65, 66, 64, -1, 22, 38, 34, -1,
              58, 59, 67, -1, 57, 56, 61, -1,
              40, 42, 39, -1, 41, 42, 40, -1,
              38, 42, 41, -1, 39, 42, 43, -1,
              60, 54, 59, -1, 61, 54, 60, -1,
              56, 54, 61, -1, 54, 55, 59, -1,
              63, 55, 62, -1, 64, 55, 63, -1,
              67, 55, 66, -1, 59, 55, 67, -1,
              66, 55, 64, -1, 46, 44, 45, -1,
              42, 44, 46, -1, 55, 51, 62, -1,
              42, 49, 44, -1, 44, 49, 50, -1,
              51, 52, 62, -1, 42, 48, 49, -1,
              38, 48, 42, -1, 22, 48, 38, -1,
              69, 48, 22, -1, 69, 47, 48, -1,
              68, 47, 69, -1, 52, 53, 62, -1,
              68, 53, 47, -1, 62, 53, 68, -1,
              21, 20, 72, -1, 72, 20, 17, -1,
              72, 17, 75, -1, 75, 17, 76, -1 ]
        soIndexFace.coordIndex.setValues(0, len(indices), indices)
        soSepArrow.addChild(cordinate) 
        soSepArrow.addChild(soIndexFace)

        root.addChild(trans)
        root.addChild(material)
        root.addChild(transform)
        root.addChild(soSepArrow)
        #Finalize the drawing by adding color, pos, scale , opacity
        return root
    
    except Exception as err:
        App.Console.PrintError("'draw_arrow2DDoublesided' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)