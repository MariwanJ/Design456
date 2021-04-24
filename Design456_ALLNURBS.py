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

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init

class Design456_Nurbs_List0Group:

    """Design456 Nurbs list 0 toolbars"""
    def __init__(self):
        return

    """Nurbs commands."""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_AnalyseLoadTest1",
                "Nurbs_AnalyseLoadTest2",
                "Nurbs_AnalyseTest3"    ,
                "Nurbs_AnalyseTest4"    ,
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
                "Nurbs_RibstoFace"

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List0.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List0Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List0Group", Design456_Nurbs_List0Group())

class Design456_Nurbs_List1Group:
    """Design456 Nurbs list 1 toolbars"""
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_CreateBeFaceFromSelBering",
                "Nurbs_TestCaseBeringTest",
                "Nurbs_FixCorner",
                "Nurbs_createProduct",
                "Nurbs_CreateSeam",
                "Nurbs_createDatumPlane",
                "Nurbs_createDatumLine",
                "Nurbs_CreateBeGrid",
                "Nurbs_CreateSketchSpline_Runall",
                "Nurbs_CreateSketchSpline_runsub",
                "Nurbs_BSplineToBezierCurve1",
                "Nurbs_BSplineToBezierCurve2",
                "Nurbs_BSplineToBezierSurface",
                "Nurbs_SurfaceEditor",
                "Nurbs_connectFaces"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List1.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List1Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List1Group", Design456_Nurbs_List1Group())

class Design456_Nurbs_List2Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
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
                "Nurbs_createTangentHelpersGUI",
                "NurbsTangentSurfaceRUN",
                "Nurbs_TangentMainFunction",
                "Nurbs_TangentSurfaceAnotherMain",
                "NurbsTangentSurfaceRUNSEAM",
                "Nurbs_CreateBorderGUI"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List2.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List2Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List2Group", Design456_Nurbs_List2Group())


class Design456_Nurbs_List3Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_createApprox",
                "Nurbs_CreateSheelANDsolid",
                "Nurbs_FlattenTheWire",
                "Nurbs_ParametricGridModifiable",
                "Nurbs_CreateGenericPane",
                "Nurbs_ControlPanelCreateFunction",
                "Nurbs_ControlPanelHU",
                "Nurbs_ControlPanelAdd",
                "Nurbs_CreateBtimap",
                "Nurbs_CreateCloverLeaf",
                "Nurbs_CurveDistance",
                "Nurbs_SoleWithBorder",
                "Nurbs_DrawCurves2Face"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List3.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List3Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List3Group", Design456_Nurbs_List3Group())



class Design456_Nurbs_List4Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_DataTool",
                "Nurbs_DraftBSplineEditorR1",
                "Nurbs_DraftBSplineEditorR2",
                "Nurbs_createSketchSpline",
                "Nurbs_DynamicOffsetMain",
                "Nurbs_DynamicOffsetRu",
                "Nurbs_FeedBackSketch",
                "Nurbs_FaceDrawSegments",
                "Nurbs_Drawoversegments"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List4.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List4Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List4Group", Design456_Nurbs_List4Group())


class Design456_Nurbs_List5Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_CreateMapToFace",
                "Nurbs_CreateGridToFace",
                "Nurbs_EventFilter",
                "Nurbs_DrawIsoFace",
                "Nurbs_FaceDraw",
                "Nurbs_FemEdgeLengthMesh",
                "Nurbs_FEM_EdgeLengthMeshExampl",
                "Nurbs_CreateFiledFace",
                "Nurbs_FoldingRu",
                "Nurbs_GenRandomDa",
                "Nurbs_geodesicMapPatchToFace",
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List5.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List5Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List5Group", Design456_Nurbs_List5Group())


class Design456_Nurbs_List6Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_AppendGeodesic",
                "Nurbs_createCurvatureStar",
                "Nurbs_createGeodesicA",
                "Nurbs_creategeodesicbunch",
                "Nurbs_geodesicDistance",
                "Nurbs_CreateMarker",
                "Nurbs_FindGeodesicToTarget",
                "Nurbs_CreateShoeMarkers",
                "Nurbs_CreateShoeMarkers",
                "Nurbs_commandCreateHelmet",
                "Nurbs_HelmetCreateTriange",
                "Nurbs_MakeHelperSel",
                "Nurbs_HelperTes"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List6.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List6Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List6Group", Design456_Nurbs_List6Group())

class Design456_Nurbs_List7Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_extractWires",
                "Nurbs_Holes",
                "Nurbs_IsoDrawtestE",
                "Nurbs_IsoDrawtestD",
                "Nurbs_IsoDrawtestC",
                "Nurbs_ISOmap2Dto3D",
                "Nurbs_ISOmap3Dto2D",
                "Nurbs_ISOdrawTestB",
                "Nurbs_ISOdrawTestA",
                "Nurbs_IsodrawTestF",
                "Nurbs_IsoMapMai",
                "Nurbs_DisplayKontsandPolseForCurv",
                "Nurbs_LoftSelectionEdge"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List7.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List7Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List7Group", Design456_Nurbs_List7Group())



class Design456_Nurbs_List8Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_LoftSelection",
                "Nurbs_MeshGenModTest",
                "Nurbs_MeshGenTest",
                "Nurbs_MikiTestMe",
                "Nurbs_miki_gTestDialog",
                "Nurbs_miki_gTestDialog_1",
                "Nurbs_miki_gTestDialog_2",
                "Nurbs_miki_gTestDialog_3",
                "Nurbs_miki_gTestDialog_4",
                "Nurbs_MonitorMain",
                "Nurbs_MoinitorForce",
                "Nurbs_Monitor_Mymonito"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List8.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List8Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List8Group", Design456_Nurbs_List8Group())

class Design456_Nurbs_List9Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_createMorpher",
                "Nurbs_MultiEditAA",
                "Nurbs_MultiEdi",
                "Nurbs_NeedleMain",
                "Nurbs_NeedleChangeModel",
                "Nurbs_NeedlecmdAdd",
                "Nurbs_NeedlecmdDel",
                "Nurbs_Needle_ListModels",
                "newTestNeedleFunctionWasMain",
                "Nurbs_CreateWSLink",
                "Nurbs_CreateWorkspace"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List9.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List9Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List9Group", Design456_Nurbs_List9Group())


class Design456_Nurbs_List10Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_main",
                "Nurbs_NurbsTest2",
                "Nurbs_NurbsTest",
                "Nurbs_NurbsRandomTours",
                "Nurbs_PointsRUNA",
                "Nurbs_PointsRUNC",
                "Nurbs_PointsRUND",
                "Nurbs_PointsRUNE",
                "Nurbs_PointsRUNE",
                "Nurbs_PointsRUND",
                "Nurbs_PointsRUNC",
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List10.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List10Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List10Group", Design456_Nurbs_List10Group())

class Design456_Nurbs_List11Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_RemoveKnots",
                "Nurbs_MainScanCut",
                "Nurbs_CulpterEventStarter",
                "Nurbs_CreateShoeRib",
                "Nurbs_CreateShoeribTest",
                "Nurbs_CreateLinkToSvg",
                "Nurbs_FeedBackSketchTestB",
                "Nurbs_FeedBAckSketch_RevConstrain",
                "FeedBackSketchTest2Clients",
                "Nurbs_LoadHeightProfileFromFile",
                "Nurbs_LoadSoleProfile"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List11.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List11Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List11Group", Design456_Nurbs_List11Group())



class Design456_Nurbs_List12Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                "Nurbs_CreateOrUpdateSoleEnvironmentSheet",
                "Nurbs_PrototypeCreateHELL",
                "Nurbs_CreateTripod",
                "Nurbs_CreateTripodSketch",
                "Nurbs_CreateSweep",
                "Nurbs_CreateLoft",
                "Nurbs_CreateCompound",
                "Nurbs_CreatePatternV2",
                "Nurbs_CreateSinglePattern",
                "Nurbs_runPatternV3",
                "Nurbs_WeightEditor"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List12.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List12Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List12Group", Design456_Nurbs_List12Group())


class Design456_Nurbs_List13Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (
                'Nurbs_CreateQuadview',
                'Nurbs_CreateH2',
                'Nurbs_CreateDarkRoom',
                'Nurbs_LightON',
                'Nurbs_LightOFF',           
                "Nurbs_UVGRIDgenRunSel",
                "Nurbs_unrollCurveMain",
                "Nurbs_UnrollCurve"
                
                
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List13.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List13Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List13Group", Design456_Nurbs_List13Group())




class Design456_Nurbs_List14Group:
    def __init__(self):
        return

    """Nurbs commands"""

    def GetCommands(self):
        """Nurbs commands."""
        import nurbs
        return (              
                "Nurbs_UVGRIDgenRunSel",
                "Nurbs_unrollCurveMain",
                "Nurbs_UnrollCurve",
                "Nurbs_UnrollCurve_yaw",
                "Nurbs_UnrollCurve_pitch",
                "Nurbs_TransformSplinRun"

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH+ 'Nurbs_List14.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_List14Group"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_List14Group", Design456_Nurbs_List14Group())