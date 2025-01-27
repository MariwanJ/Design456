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

__updated__ = '2022-07-01 18:00:59'


def draw_DoubleSide2DdArrow(_Points=App.Vector(0, 0, 0),
                            color=FR_COLOR.FR_GOLD,
                            scale=[0.5, 0.5, 0.5],  opacity=0,
                            _rotation=[0.0, 0.0, 1.0, 0.0]):
    """[2D Arrow Double sided]

    Args:
        p1 ([App.Vector], optional): [Position of the arrow]. Defaults to App.Vector(0.0, 0.0, 0.0).
        color ((float,float,float)), optional): [RGB Value between 0 to 1]. Defaults to FR_COLOR.FR_GOLD.
        scale ((float,float,float)), optional): [Scale factor for each axis]. Defaults to (1,1,1).
        type (int, optional): [Arrow type. At the moment there are 2 types]. Defaults to 1.
        opacity (int, optional): [Opacity of the drawn arrow]. Defaults to 0.
        _rotation (list, optional): [Rotation of the arrow provided by three float and an angle (float) in degree]. Defaults to [1.0, 0.0, 0.0, 0.0].

    Returns:
        [SoSeparator]: [SoSeparator which hold the drawing. Add it to the scenegraph to show the arrow]
    """
    try:
        p1 = _Points
        root = coin.SoSeparator()
        transform = coin.SoTransform()

        trans = coin.SoTranslation()
        trans.translation.setValue(p1)

        transform.rotation.setValue(_rotation)
        transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))

        material = coin.SoMaterial()
        material.transparency.setValue(opacity)
        material.diffuseColor.setValue(coin.SbColor(color))
        material.ambientColor.setValue(coin.SbColor(color))
        material.emissiveColor.setValue(coin.SbColor(0.1, 0.1, 0.1))

        soSepArrow = coin.SoSeparator()   # drawing holder
        soIndexFace = coin.SoIndexedFaceSet()
        coordinate = coin.SoCoordinate3()
        vertexPositions = [(0.00,         8.68,        8.90),
                           (0.00,         8.68,        8.90),
                           (0.00,         8.66,        9.16),
                           (0.00,         7.89,        10.43),
                           (0.00,         8.21,        10.12),
                           (0.00,         8.46,        9.73),
                           (0.00,         8.59,        9.45),
                           (0.00,         5.49,        10.52),
                           (0.00,         5.88,        10.71),
                           (0.00,         6.29,        10.83),
                           (0.00,         6.70,        10.85),
                           (0.00,         7.12,        10.80),
                           (0.00,         7.52,        10.66),
                           (0.00,         3.62,        8.71),
                           (0.00,         1.91,        7.01),
                           (0.00,         1.91,        9.53),
                           (0.00,         1.91,        9.53),
                           (0.00,         1.91,        9.95),
                           (0.00,         1.91,        9.95),
                           (0.00,         1.91,        10.83),
                           (0.00,         1.91,        10.83),
                           (0.00,         1.91,        40.41),
                           (0.00,         1.91,        40.67),
                           (0.00,         3.61,        38.97),
                           (0.00,         5.47,        37.16),
                           (0.00,         6.62,        36.81),
                           (0.00,         6.22,        36.85),
                           (0.00,         5.84,        36.96),
                           (0.00,         8.58,        38.22),
                           (0.00,         8.39,        37.82),
                           (0.00,         8.14,        37.48),
                           (0.00,         7.83,        37.20),
                           (0.00,         7.46,        36.99),
                           (0.00,         7.06,        36.86),
                           (0.00,         8.35,        39.97),
                           (0.00,         8.57,        39.53),
                           (0.00,         8.67,        39.04),
                           (0.00,         8.67,        38.63),
                           (0.00,         1.17,        47.25),
                           (0.00,         0.51,        47.61),
                           (0.00,         0.82,        47.48),
                           (0.00,         0.99,        47.38),
                           (0.00,        -0.11,        47.69),
                           (0.00,         0.25,        47.68),
                           (0.00,        -0.72,        47.62),
                           (0.00,        -0.49,        47.67),
                           (0.00,        -0.33,        47.69),
                           (0.00,        -4.96,        43.74),
                           (0.00,        -1.75,        46.90),
                           (0.00,        -1.06,        47.48),
                           (0.00,        -0.89,        47.56),
                           (0.00,        -8.86,        39.54),
                           (0.00,        -8.75,        39.83),
                           (0.00,        -7.92,        40.78),
                           (0.00,        -8.95,        38.92),
                           (0.00,        -8.92,        39.26),
                           (0.00,        -8.96,        38.82),
                           (0.00,        -8.94,        38.56),
                           (0.00,        -8.17,        37.29),
                           (0.00,        -8.49,        37.60),
                           (0.00,        -8.74,        37.99),
                           (0.00,        -8.86,        38.27),
                           (0.00,        -5.77,        37.20),
                           (0.00,        -6.16,        37.00),
                           (0.00,        -6.57,        36.89),
                           (0.00,        -6.98,        36.86),
                           (0.00,        -7.40,        36.92),
                           (0.00,        -7.79,        37.06),
                           (0.00,        -3.89,        39.00),
                           (0.00,        -2.18,        40.69),
                           (0.00,        -2.19,        38.17),
                           (0.00,        -2.18,        38.17),
                           (0.00,        -2.18,        37.75),
                           (0.00,        -2.19,        37.75),
                           (0.00,        -2.19,        36.87),
                           (0.00,        -2.18,        36.87),
                           (0.00,        -2.18,        7.01),
                           (0.00,        -3.88,        8.71),
                           (0.00,        -5.75,        10.51),
                           (0.00,        -6.90,        10.85),
                           (0.00,        -6.50,        10.82),
                           (0.00,        -6.12,        10.70),
                           (0.00,        -8.85,        9.44),
                           (0.00,        -8.67,        9.84),
                           (0.00,        -8.42,        10.18),
                           (0.00,        -8.11,        10.46),
                           (0.00,        -7.74,        10.67),
                           (0.00,        -7.34,        10.81),
                           (0.00,        -8.62,        7.68),
                           (0.00,        -8.84,        8.13),
                           (0.00,        -8.94,        8.61),
                           (0.00,        -8.94,        9.03),
                           (0.00,        -1.41,        0.44),
                           (0.00,        -0.75,        0.08),
                           (0.00,        -1.06,        0.21),
                           (0.00,        -1.23,        0.31),
                           (0.00,        -0.13,        0.00),
                           (0.00,        -0.49,        0.01),
                           (0.00,         0.48,        0.08),
                           (0.00,         0.25,        0.02),
                           (0.00,         0.09,        0.00),
                           (0.00,         4.70,        3.97),
                           (0.00,         1.51,        0.80),
                           (0.00,         0.82,        0.22),
                           (0.00,         0.65,        0.14),
                           (0.00,         8.59,        8.18),
                           (0.00,         8.48,        7.89),
                           (0.00,         7.65,        6.94),
                           (0.00,         8.68,        8.81),
                           (0.00,         8.65,        8.47),
                           (0.00,         8.68,        8.90),
                           (0.00,         8.68,        8.81),
                           (0.00,         8.59,        8.18),
                           (0.00,         4.70,        3.97),
                           (0.00,         0.48,        0.08),
                           (0.00,        -0.13,        0.00),
                           (0.00,        -0.75,        0.08),
                           (0.00,        -1.41,        0.44),
                           (0.00,        -8.62,        7.68),
                           (0.00,        -8.85,        9.44),
                           (0.00,        -6.90,        10.85),
                           (0.00,        -5.75,        10.51),
                           (0.00,        -3.88,        8.71),
                           (0.00,        -2.18,        7.01),
                           (0.00,        -2.18,        36.87),
                           (0.00,        -2.19,        36.87),
                           (0.00,        -2.19,        37.75),
                           (0.00,        -2.18,        37.75),
                           (0.00,        -2.18,        38.17),
                           (0.00,        -2.19,        38.17),
                           (0.00,        -2.18,        40.69),
                           (0.00,        -3.89,        39.00),
                           (0.00,        -5.77,        37.20),
                           (0.00,        -8.17,        37.29),
                           (0.00,        -8.94,        38.56),
                           (0.00,        -8.96,        38.82),
                           (0.00,        -8.95,        38.92),
                           (0.00,        -8.86,        39.54),
                           (0.00,        -4.96,        43.74),
                           (0.00,        -0.72,        47.62),
                           (0.00,        -0.11,        47.69),
                           (0.00,         0.51,        47.61),
                           (0.00,         1.17,        47.25),
                           (0.00,         8.35,        39.97),
                           (0.00,         8.58,        38.22),
                           (0.00,         6.62,        36.81),
                           (0.00,         5.47,        37.16),
                           (0.00,         3.61,        38.97),
                           (0.00,         1.91,        40.67),
                           (0.00,         1.91,        40.41),
                           (0.00,         1.91,        10.83),
                           (0.00,         1.91,        10.83),
                           (0.00,         1.91,        9.95),
                           (0.00,         1.91,        9.95),
                           (0.00,         1.91,        9.53),
                           (0.00,         1.91,        9.53),
                           (0.00,         1.91,        7.01),
                           (0.00,         3.62,        8.71),
                           (0.00,         5.49,        10.52),
                           (0.00,         7.89,        10.43),
                           (0.00,         8.66,        9.16),
                           (0.00,         8.68,        8.90)]

        coordinate.point.setValues(0, 432, vertexPositions)
        indices = [104, 98, 103, -1, 99, 100, 98, -1,
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
                   72, 17, 75, -1, 75, 17, 76, -1]
        soIndexFace.coordIndex.setValues(0, len(indices), indices)
        soSepArrow.addChild(coordinate)
        soSepArrow.addChild(soIndexFace)

        # Finalize the drawing by adding color, pos, scale , opacity
        root.addChild(trans)
        root.addChild(transform)
        root.addChild(material)
        root.addChild(soSepArrow)
        return root

    except Exception as err:
        App.Console.PrintError("'draw_arrow2DDoublesided' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_RotationPad(p1=App.Vector(0.0, 0.0, 0.0), color=FR_COLOR.FR_GOLD,
                     scale=(1, 1, 1), opacity=0, _rotation=[0.0, 0.0, 0.0]):
    try:
        root = coin.SoSeparator()

        separatorX = coin.SoSeparator()
        separatorY = coin.SoSeparator()
        separatorZ = coin.SoSeparator()

        tempRX = coin.SbVec3f()
        tempRX.setValue(1, 0, 0)

        tempRY = coin.SbVec3f()
        tempRY.setValue(0, 1, 0)

        tempRZ = coin.SbVec3f()
        tempRZ.setValue(0, 0, 1)

        transformX = coin.SoTransform()
        transformY = coin.SoTransform()
        transformZ = coin.SoTransform()

        transformX.rotation.setValue(tempRY, math.radians(_rotation[0]))
        transformY.rotation.setValue(tempRX, math.radians(_rotation[1]))
        transformZ.rotation.setValue(tempRZ, math.radians(_rotation[2]))

        material = coin.SoMaterial()
        material.transparency.setValue(opacity)
        material.diffuseColor.setValue(coin.SbColor(color))
        Shapehint = coin.SoShapeHints()
        Shapehint.shapeType = coin.SoShapeHints.UNKNOWN_FACE_TYPE
        Shapehint.vertexOrdering = coin.SoShapeHints.CLOCKWISE
        Shapehint.faceType = coin.SoShapeHints.UNKNOWN_FACE_TYPE

        soIndexFace = coin.SoIndexedFaceSet()
        coordinate = coin.SoCoordinate3()
        vertexPositions = [(0,       0,    0.5),
                           (0.01,          0,       0.5),
                           (0.02,          0,       0.5),
                           (0.02,          0,       0.49),
                           (0.03,          0,       0.49),
                           (0.04,          0,       0.49),
                           (0.04,          0,       0.48),
                           (0.04,          0,       0.47),
                           (0.05,          0,       0.47),
                           (0.05,          0,       0.46),
                           (0.05,          0,       0.45),
                           (0,          0,        0.4),
                           (-0.01,           0,        0.4),
                           (-0.02,           0,        0.4),
                           (-0.02,           0,        0.41),
                           (-0.03,           0,        0.41),
                           (-0.04,           0,        0.41),
                           (-0.04,           0,        0.42),
                           (-0.04,           0,        0.43),
                           (-0.05,           0,        0.43),
                           (-0.05,           0,        0.44),
                           (-0.05,           0,        0.45),
                           (-0.05,           0,        0.46),
                           (-0.05,           0,        0.47),
                           (-0.04,           0,        0.47),
                           (-0.04,           0,        0.48),
                           (-0.04,           0,        0.49),
                           (-0.03,           0,        0.49),
                           (-0.02,           0,        0.49),
                           (-0.02,           0,        0.5),
                           (-0.01,           0,        0.5),
                           (0.05,          0,       0.44),
                           (0.05,          0,       0.43),
                           (0.04,          0,       0.43),
                           (0.04,          0,       0.42),
                           (0.04,          0,       0.41),
                           (0.03,          0,       0.41),
                           (0.02,          0,       0.41),
                           (0.02,          0,       0.4),
                           (0.01,          0,       0.4),
                           (-0.09,           0,        0.49),
                           (-0.17,           0,        0.47),
                           (-0.24,           0,        0.44),
                           (-0.31,           0,        0.39),
                           (-0.37,           0,        0.34),
                           (-0.42,           0,        0.27),
                           (-0.46,           0,        0.2),
                           (-0.48,           0,        0.13),
                           (-0.5,          0,       0.05),
                           (-0.5,          0,       -0.03),
                           (-0.49,           0,        -0.11),
                           (-0.46,           0,        -0.19),
                           (-0.43,           0,        -0.26),
                           (-0.38,           0,        -0.33),
                           (-0.32,           0,        -0.38),
                           (-0.25,           0,        -0.43),
                           (-0.18,           0,        -0.47),
                           (-0.1,          0,       -0.49),
                           (-0.02,           0,        -0.5),
                           (0.06,          0,       -0.5),
                           (0.14,          0,       -0.48),
                           (0.21,          0,       -0.45),
                           (0.28,          0,       -0.41),
                           (0.35,          0,       -0.36),
                           (0.4,         0,      -0.3),
                           (0.44,          0,       -0.23),
                           (0.47,          0,       -0.16),
                           (0.49,          0,       -0.08),
                           (0.5,         0,      0),
                           (0.49,          0,       0.08),
                           (0.48,          0,       0.15),
                           (0.45,          0,       0.22),
                           (0.41,          0,       0.29),
                           (0.36,          0,       0.35),
                           (0.3,         0,      0.4),
                           (0.24,          0,       0.44),
                           (0.17,          0,       0.47),
                           (0.09,          0,       0.49),
                           (0.1,         0,      0.48),
                           (0.1,         0,      0.46),
                           (0.1,         0,      0.45),
                           (0.1,         0,      0.43),
                           (0.09,          0,       0.41),
                           (0.08,          0,       0.39),
                           (0.4,         0,      0),
                           (0.39,          0,       0.07),
                           (0.38,          0,       0.13),
                           (0.35,          0,       0.2),
                           (0.31,          0,       0.25),
                           (0.26,          0,       0.3),
                           (0.21,          0,       0.34),
                           (0.15,          0,       0.37),
                           (-0.08,           0,        0.39),
                           (-0.15,           0,        0.37),
                           (-0.21,           0,        0.34),
                           (-0.27,           0,        0.29),
                           (-0.32,           0,        0.24),
                           (-0.36,           0,        0.18),
                           (-0.38,           0,        0.11),
                           (-0.4,          0,       0.04),
                           (-0.4,          0,       -0.03),
                           (-0.39,           0,        -0.1),
                           (-0.36,           0,        -0.17),
                           (-0.33,           0,        -0.23),
                           (-0.28,           0,        -0.29),
                           (-0.22,           0,        -0.33),
                           (-0.16,           0,        -0.37),
                           (-0.09,           0,        -0.39),
                           (-0.02,           0,        -0.4),
                           (0.05,          0,       -0.4),
                           (0.12,          0,       -0.38),
                           (0.19,          0,       -0.35),
                           (0.25,          0,       -0.31),
                           (0.3,         0,      -0.26),
                           (0.34,          0,       -0.21),
                           (0.37,          0,       -0.14),
                           (0.39,          0,       -0.07),
                           (-0.09,           0,        0.41),
                           (-0.1,          0,       0.43),
                           (-0.1,          0,       0.45),
                           (-0.1,          0,       0.47),
                           (0,          0,    0.5),
                           (0.05,          0,       0.45),
                           (0,           0,    0.4),
                           (-0.09,           0,        0.49),
                           (0.5,           0,      0),
                           (-0.08,           0,        0.39),
                           (0.4,         0,      0),
                           (0.08,          0,       0.39),
                           (0.1,         0,      0.45),
                           (0.09,          0,       0.49)]

        coordinate.point.setValues(0, 468, vertexPositions)
        indices = [5, 1, 0, -1, 5, 2, 1, -1,
                   5, 3, 2, -1, 5, 4, 3, -1,
                   5, 7, 6, -1, 5, 8, 7, -1,
                   5, 9, 8, -1, 5, 10, 9, -1,
                   5, 12, 11, -1, 5, 13, 12, -1,
                   5, 14, 13, -1, 5, 15, 14, -1,
                   5, 16, 15, -1, 5, 17, 16, -1,
                   5, 18, 17, -1, 5, 19, 18, -1,
                   5, 20, 19, -1, 5, 21, 20, -1,
                   5, 22, 21, -1, 5, 23, 22, -1,
                   5, 24, 23, -1, 5, 25, 24, -1,
                   5, 26, 25, -1, 5, 27, 26, -1,
                   5, 28, 27, -1, 5, 29, 28, -1,
                   5, 30, 29, -1, 5, 0, 30, -1,
                   5, 31, 10, -1, 5, 32, 31, -1,
                   5, 33, 32, -1, 5, 34, 33, -1,
                   5, 35, 34, -1, 5, 36, 35, -1,
                   5, 37, 36, -1, 5, 38, 37, -1,
                   5, 39, 38, -1, 5, 11, 39, -1,
                   104, 53, 54, -1, 103, 52, 53, -1,
                   103, 53, 104, -1, 105, 54, 55, -1,
                   105, 104, 54, -1, 102, 52, 103, -1,
                   102, 51, 52, -1, 106, 55, 56, -1,
                   106, 105, 55, -1, 101, 51, 102, -1,
                   101, 50, 51, -1, 107, 106, 56, -1,
                   107, 56, 57, -1, 100, 48, 49, -1,
                   100, 49, 50, -1, 100, 50, 101, -1,
                   108, 107, 57, -1, 108, 57, 58, -1,
                   108, 58, 59, -1, 99, 47, 48, -1,
                   99, 48, 100, -1, 109, 108, 59, -1,
                   60, 109, 59, -1, 98, 47, 99, -1,
                   110, 109, 60, -1, 46, 47, 98, -1,
                   61, 110, 60, -1, 97, 46, 98, -1,
                   111, 110, 61, -1, 45, 46, 97, -1,
                   62, 111, 61, -1, 96, 45, 97, -1,
                   112, 111, 62, -1, 44, 45, 96, -1,
                   63, 112, 62, -1, 95, 44, 96, -1,
                   113, 112, 63, -1, 43, 44, 95, -1,
                   64, 113, 63, -1, 94, 43, 95, -1,
                   114, 113, 64, -1, 42, 43, 94, -1,
                   65, 114, 64, -1, 93, 42, 94, -1,
                   115, 114, 65, -1, 41, 42, 93, -1,
                   66, 115, 65, -1, 117, 93, 92, -1,
                   116, 115, 66, -1, 118, 41, 93, -1,
                   118, 93, 117, -1, 119, 41, 118, -1,
                   120, 41, 119, -1, 40, 41, 120, -1,
                   67, 84, 116, -1, 67, 116, 66, -1,
                   68, 84, 67, -1, 91, 82, 83, -1,
                   81, 82, 91, -1, 69, 84, 68, -1,
                   69, 85, 84, -1, 70, 85, 69, -1,
                   70, 86, 85, -1, 76, 81, 91, -1,
                   76, 77, 78, -1, 76, 78, 79, -1,
                   76, 79, 80, -1, 76, 80, 81, -1,
                   71, 86, 70, -1, 71, 87, 86, -1,
                   75, 76, 91, -1, 75, 91, 90, -1,
                   72, 87, 71, -1, 72, 88, 87, -1,
                   74, 75, 90, -1, 74, 90, 89, -1,
                   73, 88, 72, -1, 73, 74, 89, -1,
                   73, 89, 88, -1
                   ]
        soIndexFace.coordIndex.setValues(0, len(indices), indices)
        separatorX.addChild(transformX)
        separatorX.addChild(Shapehint)
        separatorX.addChild(coordinate)
        separatorX.addChild(soIndexFace)

        separatorY.addChild(transformY)
        separatorY.addChild(separatorX)

        separatorZ.addChild(transformZ)
        separatorZ.addChild(separatorY)

        transform = coin.SoTransform()  # for scale only
        trans = coin.SoTranslation()
        trans.translation.setValue(p1)
        # Only for scale
        transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])

        root.addChild(trans)
        root.addChild(material)
        root.addChild(transform)
        root.addChild(separatorZ)
        return root
    except Exception as err:
        App.Console.PrintError("'draw draw_RotationPad' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)




class drawAlignmentBars:
    def __init__(self,_Boundary=None ,
                      color=[FR_COLOR.FR_RED, FR_COLOR.FR_GREEN, FR_COLOR.FR_BLUE],
                      scale=(1, 1, 1), opacity=0,
                      _rotation=[0.0, 0.0, 0.0], _type=0):

        # xAxis:
        if _Boundary is None: 
            raise ValueError ("Boundary cannot be None")
        
        self.vector = None
        self.separatorX = None
        self.separatorY = None
        self.separatorZ = None

        self.color = color
        self.Bartype = _type
        self.root = coin.SoSeparator()
        self.Boundary = _Boundary
        self.Average = (_Boundary.XLength+_Boundary.YLength+_Boundary.ZLength)/100
        self.barRadius =     self.Average
        self.ButtonRadius =  self.Average*2

        p1 = []
        p2 = []
        p3 = []
        _pStart = App.Vector(self.Boundary.XMin , self.Boundary.YMin, self.Boundary.ZMin)
        p1.append(App.Vector(_pStart.x, _pStart.y, _pStart.z))
        p1.append(App.Vector(_pStart.x, _pStart.y+self.Boundary.YLength/2, _pStart.z))
        p1.append(App.Vector(_pStart.x, _pStart.y+self.Boundary.YLength, _pStart.z))

        # yAxis:
        p2.append(App.Vector(_pStart.x, _pStart.y, _pStart.z))
        p2.append(App.Vector(_pStart.x+ self.Boundary.XLength/2, _pStart.y, _pStart.z))
        p2.append(App.Vector(_pStart.x+self.Boundary.XLength, _pStart.y, _pStart.z))

        # zAxis:
        p3.append(App.Vector(self.Boundary.XMax, _pStart.y, _pStart.z))
        p3.append(App.Vector(self.Boundary.XMax, _pStart.y, _pStart.z+ self.Boundary.ZLength/2))
        p3.append(App.Vector(self.Boundary.XMax, _pStart.y, _pStart.z+self.Boundary.ZLength))
        self.vector = [p1, p2, p3]

    def createABar(self, _vector, _color, _length, _rotation):
        color = coin.SoBaseColor()
        transform = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
        color.rgb = _color
        cylinder = coin.SoCylinder()
        cylinder.height = _length
        cylinder.radius = self.barRadius
        transBar = coin.SoTranslation()
        transBar.translation.setValue(_vector)
        barLine = coin.SoSeparator()
        barLine.addChild(color)
        barLine.addChild(transBar)
        barLine.addChild(transform)
        barLine.addChild(cylinder)
        return barLine

    def createAButton(self, _vector, _color, _rotation):
        color = coin.SoBaseColor()
        color.rgb = _color
        transform = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
        sphere = coin.SoSphere()
        sphere.radius = self.ButtonRadius
        transBar = coin.SoTranslation()
        transBar.translation.setValue(_vector)
        barLine = coin.SoSeparator()
        barLine.addChild(color)
        barLine.addChild(transBar)
        barLine.addChild(transform)
        barLine.addChild(sphere)
        return barLine

    def drawButtons(self):

        AllButtons = []
        # TODO FIXME: vectors are not correct

        # X button
        for i in range(0, 3):
            extraLength= App.Vector(0.0, self.Boundary.YLength/2, 0.0)
            extraLength = (self.vector[1][i]).sub(extraLength)

            AllButtons.append(self.createAButton(extraLength,
                       self.color[0], [0.0, 0.0, 0.0, 0.0]))

        # Y button
        for i in range(0, 3):
            extraLength=App.Vector(self.Boundary.XLength/2, 0.0, 0.0)
            extraLength=(self.vector[0][i]).sub( extraLength)
            AllButtons.append(self.createAButton(extraLength,
                       self.color[1],[0.0, 0.0, 1.0, 90.0]))

        # Z button
        for i in range(0, 3):
            extraLength=App.Vector(self.Boundary.XLength/2,0.0, 0)
            extraLength= (self.vector[2][i]).add(extraLength)
            AllButtons.append(self.createAButton(extraLength,
                       self.color[2], [0.0, 0.0, 1.0, 90.0]))

        return AllButtons  # a SoSeparator that contains all bars

    def drawBars(self):

        AllBars=coin.SoSeparator()

        # X bars
        for i in range(0, 3):
            AllBars.addChild(self.createABar(self.vector[1][i],
                       self.color[0],
                       self.Boundary.YLength,[0.0, 0.0, 0.0, 0.0]))

        # Y bars
        for i in range(0, 3):

            AllBars.addChild(self.createABar(self.vector[0][i],
                       self.color[1],
                       self.Boundary.XLength,[0.0, 0.0, -1.0, 90.0]))

        # Z bars
        for i in range(0, 3):
            AllBars.addChild(self.createABar(self.vector[2][i],
                       self.color[2],
                       self.Boundary.XLength,[0.0, 0.0, 1.0, 90.0]))

        return AllBars  # a SoSeparator that contains all bars

    def createWidget(self):
        base=[]
        buttons=[]

    def Activate(self):

        try:
            if self.Bartype == 0:
                pass

                self.barSoSeparator = self.drawBars()
                self.buttonSoSeparator = self.drawButtons()
                return(self.barSoSeparator,self.buttonSoSeparator)

            elif self.Bartype == 1:
                pass

        except Exception as err:
            App.Console.PrintError("'draw draw_RotationPad' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb=sys.exc_info()
            fname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
#*********************************************************
