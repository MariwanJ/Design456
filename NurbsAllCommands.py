# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
import nurbs


# Sort commands by file names
# The command are many and must be used together
# so I sort them out by filenames

class Design456_Nurbs_Analyse:

    """Nurbs Analyse"""

    def GetCommands(self):
        """3D Modifying Tools."""
        return ("Nurbs_AnalyseTest3",
                "Nurbs_AnalyseTest4",
                "Nurbs_AnalyseLoadTest1",
                "Nurbs_AnalyseLoadTest2"

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Analyse")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Analyse"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Analyse", Design456_Nurbs_Analyse())


class Design456_Nurbs_Approximation:

    """Nurbs Approximation"""

    def GetCommands(self):
        return (
            "Nurbs_smoothPointcloudGUI",
            "Nurbs_loadPointcloudfromImageGUI",
            "Nurbs_LoadCylinderfacefromImageGUI",
            "Nurbs_BumpFacefromImageGUI",
            "Nurbs_minimumLengthBezier",
            "Nurbs_CreateMyMinAGUI",
            "Nurbs_createMyMinSoftGUI",
            "Nurbs_nearconstantCurvatureBezier",
            "Nurbs_createBezierPolesFramefromribsGUI",
            "Nurbs_DontKnowWhatThisDo_B",
            "Nurbs_RibstoFace",
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Approximation")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Approximation"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Approximation",
               Design456_Nurbs_Approximation())


class Design456_Nurbs_Bering:

    """Nurbs Bering"""

    def GetCommands(self):
        return (
            "Nurbs_CreateBeFaceFromSelBering",
            "Nurbs_TestCaseBeringTest",
            "Nurbs_FixCorner",
            "Nurbs_createProduct",
            "Nurbs_CreateSeam",
            "Nurbs_createDatumPlane",
            "Nurbs_createDatumLine",
            "Nurbs_CreateBeGrid",
            "Nurbs_CreateSketchSpline_Runall"
            "Nurbs_CreateSketchSpline_runsubs"
            "Nurbs_BSplineToBezierCurve1",
            "Nurbs_BSplineToBezierCurve2",
            "Nurbs_BSplineToBezierSurface",
            "Nurbs_SurfaceEditor",
            "Nurbs_connectFaces",
            "Nurbs_CreateBEplane",
            "Nurbs_CreateBETube",
            "Nurbs_createPlaneTubeConnector",
            "Nurbs_createHelmetTubeConnector",
            "Nurbs_createTriangle",
            "Nurbs_SplitInToCells",
            "Nurbs_createTangentStripes",
            "Nurbs_CreateCELL",
            "Nurbs_CreateQuadPlacement",
            "Nurbs_FaceToBezierSurface",
            "Nurbs_Stretchandbend",
            "Nurbs_CreateSketchCircle",
            "Nurbs_CreateHOLEGUI",
            "Nurbs_polishG1GUI",
            "Nurbs_createTangentHelpers",
            "Nurbs_CreateBorderGUI",
            "Nurbs_createApprox",
            "Nurbs_CreateSheelANDsolid",
            "Nurbs_FlattenTheWire",


        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Bering")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Bering"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Bering", Design456_Nurbs_Bering())


class Design456_Nurbs_BlenderGrid:

    """Nurbs BlenderGrid"""

    def GetCommands(self):
        return (
            "Nurbs_ParametricGridModifiable"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs BlenderGrid")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs BlenderGrid"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_BlenderGrid", Design456_Nurbs_BlenderGrid())


class Design456_Nurbs_ControlPanel:

    """Nurbs Configuration"""

    def GetCommands(self):
        return (
            "Nurbs_CreateGenericPanel"
            "Nurbs_ControlPanelCreateFunction",
            "Nurbs_ControlPanelHU",
            "Nurbs_ControlPanelAdd",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs ControlPanel")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs ControlPanel"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_ControlPanel", Design456_Nurbs_ControlPanel())


class Design456_Nurbs_CreateBitmap:

    """Nurbs CreateBitmap"""

    def GetCommands(self):
        return (
            "Nurbs_CreateBtimap",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs CreateBitmap")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs CreateBitmap"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_CreateBitmap", Design456_Nurbs_CreateBitmap())


class Design456_Nurbs_CreateCloverLeaf:

    """Nurbs CreateCloverLeaf"""

    def GetCommands(self):
        return (
            "Nurbs_CreateCloverLeaf",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs CreateCloverLeaf")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs CreateCloverLeaf"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_CreateCloverLeaf",
               Design456_Nurbs_CreateCloverLeaf())


class Design456_Nurbs_Curve:

    """Nurbs curvDistance, Curve, simplecurve and unroll_curve """

    def GetCommands(self):
        return (
            "Nurbs_CurveDistance",
            "Nurbs_SoleWithBorder",
            "Nurbs_DrawCurves2Face",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs curvDistance, Curve, simplecurve and unroll_curve")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "curvDistance, Curve, simplecurve and unroll_curve"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Curve", Design456_Nurbs_Curve())


class Design456_Nurbs_dataTools:

    """Nurbs dataTools"""

    def GetCommands(self):
        return (
            "Nurbs_DataTools"

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs dataTools")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs dataTools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_dataTools", Design456_Nurbs_dataTools())


class Design456_Nurbs_DraftBSplineEditor:

    """Nurbs DraftBSplineEditor, param_bspline, CreateSketchSpline, transformspline"""

    def GetCommands(self):
        return (

            "Nurbs_DraftBSplineEditorR1",
            "Nurbs_DraftBSplineEditorR2",
            "Nurbs_createSketchSpline",



        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = (
            "Nurbs  DraftBSplineEditor, param_bspline, CreateSketchSpline, transformspline")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs  DraftBSplineEditor, param_bspline, CreateSketchSpline, transformspline"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_DraftBSplineEditor",
               Design456_Nurbs_DraftBSplineEditor())


class Design456_Nurbs_DynamicOffset:

    """Nurbs DynamicOffset"""

    def GetCommands(self):
        return ("Nurbs_DynamicOffsetMain",
                "Nurbs_DynamicOffsetRun"

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs DynamicOffset")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs DynamicOffset"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_DynamicOffset",
               Design456_Nurbs_DynamicOffset())


class Design456_Nurbs_FeedBackSketch:

    """Nurbs FeedBackSketch"""

    def GetCommands(self):
        return (
            "Nurbs_FeedBackSketch",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs FeedBackSketch")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs  FeedBackSketch"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_FeedBackSketch",
               Design456_Nurbs_FeedBackSketch())


class Design456_Nurbs_FaceDraw:

    """Nurbs FaceDraw and FAceDraw segments"""

    def GetCommands(self):
        return ("Nurbs_FaceDrawSegments",
                "Nurbs_Drawoversegments",
                "Nurbs_CreateMapToFace",
                "Nurbs_CreateGridToFace",
                "Nurbs_EventFilter",
                "Nurbs_DrawIsoFace",
                "Nurbs_FaceDraw",








                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs  FaceDraw and FAceDraw segments")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs  FaceDraw and FAceDraw segments"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_FaceDraw", Design456_Nurbs_FaceDraw())


class Design456_Nurbs_FemEdgeLengthMesh:

    """Nurbs FemEdgeLengthMesh"""

    def GetCommands(self):
        return ("Nurbs_FemEdgeLengthMesh",
                "Nurbs_FEM_EdgeLengthMeshExample"


                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs  FemEdgeLengthMesh")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs  FemEdgeLengthMesh"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_FemEdgeLengthMesh",
               Design456_Nurbs_FemEdgeLengthMesh())


class Design456_Nurbs_FilledFace:

    """Nurbs FilledFace"""

    def GetCommands(self):
        return (
            "Nurbs_CreateFiledFace",


        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs FilledFace")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs FilledFace"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_FilledFace", Design456_Nurbs_FilledFace())


class Design456_Nurbs_Folding:

    """Nurbs Folding"""

    def GetCommands(self):
        return (
            "Nurbs_FoldingRun"

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Folding")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Folding"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Folding", Design456_Nurbs_Folding())


class Design456_Nurbs_GenRandomNumber:

    """Nurbs GenRandomNumber"""

    def GetCommands(self):
        return ("Nurbs_GenRandomDat"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs GenRandomNumber")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs GenRandomNumber"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_GenRandomNumber",
               Design456_Nurbs_GenRandomNumber())


class Design456_Nurbs_Geodesic_Line:

    """Nurbs Geodesic_Line"""

    def GetCommands(self):
        return (
            "Nurbs_geodesicMapPatchToFace",
            "Nurbs_AppendGeodesic",
            "Nurbs_createCurvatureStar",
            "Nurbs_createGeodesicA",
            "Nurbs_creategeodesicbunch",
            "Nurbs_geodesicDistance",
            "Nurbs_CreateMarker",
            "Nurbs_FindGeodesicToTarget",
            "Nurbs_CreateShoeMarkers",
            "Nurbs_CreateShoeMarkers",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Geodesic_Line")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Geodesic_Line"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Geodesic_Line",
               Design456_Nurbs_Geodesic_Line())


class Design456_Nurbs_Helmet:

    """Nurbs Helmet"""

    def GetCommands(self):
        return (
            "Nurbs_commandCreateHelmet",
            "Nurbs_HelmetCreateTriangel"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Helmet")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Helmet"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Helmet", Design456_Nurbs_Helmet())


class Design456_Nurbs_Helper:

    """Nurbs Helper"""

    def GetCommands(self):
        return (
            "Nurbs_MakeHelperSel",
            "Nurbs_HelperTest"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Helper")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Helper"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Helper", Design456_Nurbs_Helper())


class Design456_Nurbs_Holes:

    """Nurbs Holes"""

    def GetCommands(self):
        return ("Nurbs_extractWires",
                "Nurbs_Holes"





                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Holes")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs Holes"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Holes", Design456_Nurbs_Holes())


class Design456_Nurbs_ISODraw:

    """Nurbs ISODraw isomap"""

    def GetCommands(self):
        return (
            "Nurbs_IsoDrawtestE",
            "Nurbs_IsoDrawtestD",
            "Nurbs_IsoDrawtestC",
            "Nurbs_ISOmap2Dto3D",
            "Nurbs_ISOmap3Dto2D",
            "Nurbs_ISOdrawTestB",
            "Nurbs_ISOdrawTestA",
            "Nurbs_IsodrawTestF",
            "Nurbs_IsoMapMain"

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs ISODraw isomap")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs ISODraw"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_ISODraw", Design456_Nurbs_ISODraw())


class Design456_Nurbs_KontsandPolseForCurve:

    """Nurbs KontsandPolseForCurve"""

    def GetCommands(self):
        return (
            "Nurbs_DisplayKontsandPolseForCurve"

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs KontsandPolseForCurve")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs KontsandPolseForCurve"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_KontsandPolseForCurve",
               Design456_Nurbs_KontsandPolseForCurve())


class Design456_Nurbs_LoftSelection:

    """Nurbs LoftSelection """

    def GetCommands(self):
        return (
            "Nurbs_LoftSelectionEdge",
            "Nurb_LoftSelection"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs LoftSelection")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsLoftSelection"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_LoftSelection",
               Design456_Nurbs_LoftSelection())


class Design456_Nurbs_MeshGenerator:

    """Nurbs MeshGenerator"""

    def GetCommands(self):
        return (
            "Nurbs_MeshGenModTest",
            "Nurbs_MeshGenTest"

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs MeshGenerator")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "MeshGenerator"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_MeshGenerator",
               Design456_Nurbs_MeshGenerator())


class Design456_Nurbs_MIKI:

    """Nurbs MIKI"""

    def GetCommands(self):
        return (
            "Nurbs_MikiTestMe",
            "Nurbs_miki_gTestDialog",
            "Nurbs_miki_gTestDialog_1",
            "Nurbs_miki_gTestDialog_2",
            "Nurbs_miki_gTestDialog_3",
            "Nurbs_miki_gTestDialog_4",


        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs MIKI")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "MIKI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_MIKI", Design456_Nurbs_MIKI())


class Design456_Nurbs_Monitor:

    """Nurbs Monitor"""

    def GetCommands(self):
        return ("Nurbs_MonitorMain",
                "Nurbs_MoinitorForce",
                "Nurbs_Monitor_Mymonitor"





                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Monitor")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Monitor"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Monitor", Design456_Nurbs_Monitor())


class Design456_Nurbs_Morpher:

    """Nurbs Morpher"""

    def GetCommands(self):
        return (
            "Nurbs_createMorpher",



        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Morpher")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Morpher"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Morpher", Design456_Nurbs_Morpher())


class Design456_Nurbs_MoveAlongCurve:

    """Nurbs MoveAlongCurve"""

    def GetCommands(self):
        return (
            "Nurbs_MoveAlongCurve"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs MoveAlongCurve")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "MoveAlongCurve"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_MoveAlongCurve",
               Design456_Nurbs_MoveAlongCurve())


class Design456_Nurbs_Multiedit:

    """Nurbs Multiedit"""

    def GetCommands(self):
        return (
            "Nurbs_MultiEditAA",
            "Nurbs_MultiEdit"
        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Multiedit")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Multiedit"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Multiedit", Design456_Nurbs_Multiedit())


class Design456_Nurbs_Needle:

    """Nurbs Needle, neele_models,needle_cmds, needle_change_model"""

    def GetCommands(self):
        return (
            "Nurbs_NeedleMain",
            "Nurbs_NeedleChangeModel",
            "Nurbs_NeedlecmdAdd",
            "Nurbs_NeedlecmdDel",
            "Nurbs_Needle_ListModels",
            "newTestNeedleFunctionWasMain",
            ""




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = (
            "Nurbs Needle, neele_models,needle_cmds, needle_change_model")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Needle, neele_models,needle_cmds, needle_change_model"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Needle", Design456_Nurbs_Needle())


class Design456_Nurbs_Nurbs:

    """Nurbs nurbs,nurbs_dialog,nurbs_tools,nurbsGUI"""

    def GetCommands(self):
        return (
            "Nurbs_CreateWSLink",
            "Nurbs_CreateWorkspace",
            "Nurbs_main",
            "Nurbs_NurbsTest2",
            "Nurbs_NurbsTest",
            "Nurbs_NurbsRandomTours",






        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs nurbs,nurbs_dialog,nurbs_tools,nurbsGUI")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "nurbs,nurbs_dialog,nurbs_tools,nurbsGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Nurbs", Design456_Nurbs_Nurbs())


class Design456_Nurbs_Points:

    """Nurbs OrderPoints, Points, Points_to_face"""

    def GetCommands(self):
        return (
            "Nurbs_PointsRUNA",
            "Nurbs_PointsRUNC",
            "Nurbs_PointsRUND",
            "Nurbs_PointsRUNE",
            # TODO  :THERE ARE MORE COMMANDS




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs OrderPoints, Points, Points_to_face")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "OrderPoints, Points, Points_to_face"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Points", Design456_Nurbs_Points())


class Design456_Nurbs_Points:

    """Nurbs OrderPoints, Points, Points_to_face"""

    def GetCommands(self):
        return (
            "Nurbs_PointsRUNE",
            "Nurbs_PointsRUND",
            "Nurbs_PointsRUNC",
            "Nurbs_PointsRUNA"




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs OrderPoints, Points, Points_to_face")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "OrderPoints, Points, Points_to_face"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Points", Design456_Nurbs_Points())


class Design456_Nurbs_RemoveKnot:

    """Nurbs RemoveKnot"""

    def GetCommands(self):
        return (

            "Nurbs_RemoveKnots",

        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs RemoveKnot")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "RemoveKnot"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_RemoveKnot", Design456_Nurbs_RemoveKnot())

class Design456_Nurbs_ScanBackBoneCut:

    """Nurbs ScanBackBoneCut"""

    def GetCommands(self):
        return (
            "Nurbs_MainScanCut",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs ScanBackBoneCut")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "ScanBackBoneCut"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_ScanBackBoneCut",
               Design456_Nurbs_ScanBackBoneCut())


class Design456_Nurbs_Scancut:

    """Nurbs Scancut"""

    def GetCommands(self):
        return (
            ""




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Scancut")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Scancut"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Scancut", Design456_Nurbs_Scancut())


class Design456_Nurbs_Sculpter:

    """Nurbs Sculpter"""

    def GetCommands(self):
        return (
            "Nurbs_CulpterEventStarter",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Sculpter")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Sculpter"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Sculpter", Design456_Nurbs_Sculpter())


class Design456_Nurbs_Shoe:

    """Nurbs CreateSHOErib,ImportSVG, shoe, shoedata,"""

    def GetCommands(self):
        return (
            "Nurbs_CreateShoeRib",
            "Nurbs_CreateShoeribTest",
            "Nurbs_CreateLinkToSvg",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs CreateSHOErib,ImportSVG, shoe, shoedata,")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "CreateSHOErib,ImportSVG, shoe, shoedata,"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Shoe", Design456_Nurbs_Shoe())


class Design456_Nurbs_sketcher:

    """Nurbs sketcher, skdriver, sketch_to_bezier,sketchclone,sketcher_grids,sketchmanager"""

    def GetCommands(self):
        return (
            "Nurbs_FeedBackSketchTestB",
            "Nurbs_FeedBAckSketch_RevConstrain",
            "FeedBackSketchTest2Clients",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = (
            "Nurbs Nurbs sketcher, skdriver, sketch_to_bezier,sketchclone,sketcher_grids,sketchmanager")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs sketcher, skdriver, sketch_to_bezier,sketchclone,sketcher_grids,sketchmanager"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_sketcher", Design456_Nurbs_sketcher())


class Design456_Nurbs_Sole:

    """Nurbs LoadSoleProfile height & width, sole_change_model, sole_:models,sole """

    def GetCommands(self):
        return (
            "Nurbs_LoadHeightProfileFromFile",
            "Nurbs_LoadSoleProfile",
            "Nurbs_CreateOrUpdateSoleEnvironmentSheet",
            "Nurbs_PrototypeCreateHELL",
            "Design456_Nurbs_Soel",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = (
            "Nurbs LoadSoleProfile height & width, sole_change_model, sole_:models,sole")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs LoadSoleProfile height & width, sole_change_model, sole_:models,sole"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Sole", Design456_Nurbs_Sole())


class Design456_Nurbs_TRIPOD2:

    """Nurbs TRIPOD2"""

    def GetCommands(self):
        return (
            "Nurbs_CreateTripod",
            "Nurbs_CreateTripodSketch",
            "Nurbs_CreateSweep",
            "Nurbs_CreateLoft",
            "Nurbs_CreateCompound",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs TRIPOD2")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "TRIPOD2"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_TRIPOD2", Design456_Nurbs_TRIPOD2())


class Design456_Nurbs_Patternv2:

    """Nurbs Pattern v2"""

    def GetCommands(self):
        return (
            "Nurbs_CreatePatternV2",
            "Nurbs_CreateSinglePattern",
            "Nurbs_runPatternV3",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Pattern v2")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Pattern v2"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Patternv2", Design456_Nurbs_Patternv2())


class Design456_Nurbs_WeightEditor:

    """Nurbs WeightEditor"""

    def GetCommands(self):
        return (
            "Nurbs_WeightEditor",





        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs WeightEditor")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "WeightEditor"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_WeightEditor", Design456_Nurbs_WeightEditor())


class Design456_Nurbs_Wheel_Event:

    """Nurbs Wheel_Event"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Wheel_Event")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Wheel_Event"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Wheel_Event", Design456_Nurbs_Wheel_Event())


class Design456_Nurbs_ProjectEdge2Face:

    """Nurbs ProjectEdge2Face"""

    def GetCommands(self):
        return (
            ""




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs ProjectEdge2Face")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "ProjectEdge2Face"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_ProjectEdge2Face",
               Design456_Nurbs_ProjectEdge2Face())


class Design456_Nurbs_pyob:

    """Nurbs pyob"""

    def GetCommands(self):
        return (
            ""




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs pyob")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "pyob"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_pyob", Design456_Nurbs_pyob())


class Design456_Nurbs_TangetSurface:

    """Nurbs TangetSurface"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs TangetSurface")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "TangetSurface"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_TangetSurface",
               Design456_Nurbs_TangetSurface())


class Design456_Nurbs_Smooth:

    """Nurbs Smooth"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Smooth")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Smooth"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Smooth", Design456_Nurbs_Smooth())


class Design456_Nurbs_simpleHood:

    """Nurbs simpleHood"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs simpleHood")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "simpleHood"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_simpleHood", Design456_Nurbs_simpleHood())


class Design456_Nurbs_Segment:

    """Nurbs Segment"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Segment")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Segment"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Segment", Design456_Nurbs_Segment())


class Design456_Nurbs_Smooth:

    """Nurbs Smooth"""

    def GetCommands(self):
        return (
            "",




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Smooth")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Smooth"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Smooth", Design456_Nurbs_Smooth())


class Design456_Nurbs_Say:

    """Nurbs Say"""

    def GetCommands(self):
        return (
            ""




        )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Say")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Say"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Nurbs_Say", Design456_Nurbs_Say())

