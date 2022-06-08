# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - App.      *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************

from PySide.QtCore import QT_TRANSLATE_NOOP
import Draft_rc
import FreeCAD as App
import FreeCADGui as Gui

__updated__ = '2022-05-17 20:29:36'

__title__ = "FreeCAD Design456 Workbench - Init file"
__author__ = "Yorik van Havre <yorik@uncreated.net> DRAFT PART / Mariwan Jalal <mariwan.jalal@gmail.com> for Design456"
__url__ = "https://www.freecadweb.org"



class Design456 (Gui.Workbench):
    "Design456 Workbench object"

    def __init__(self):
        import Design456Init
        self.__class__.Icon = Design456Init.ICON_PATH + 'WorkbenchIcon.svg'
        self.__class__.MenuText = "Design456"
        self.__class__.ToolTip = "Direct Modeling Workbench"
        self.runOnce = True
        self.planeShow = None
        self.myDocObserver = None
        Design456Init.pToWorkbench=self


    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import BOPTools  # as bop
        import Design456Part as designPart
        import Design456_2Ddrawing as TwoDDraw
        import Design456Part_Tools as _tools
        import Design456_Alignment as _alignment
        import Design456_SelectionGate as SelGate
        import DirectModeling.directModelingCommands as dModeling
        import DefeaturingWB.DefeaturingTools
        import DefeaturingWB.DefeaturingCMD  
        import DefeaturingWB.FuzzyTools
        import Design456Init
        from Design456Pref import Design456Preferences
        import Design456_Segmented as _segmented
        import Design456_ICONPanel  #Side panel for ICONS
        import Design456_Grid as _grid

        # from Part import CommandShapes     #Tube  not working
        Gui.runCommand('Std_PerspectiveCamera', 1)

        self.appendToolbar("Design456Part", designPart.Design456Part.list)
        self.appendToolbar("Design456 2Ddrawing",
                           TwoDDraw.Design456_2Ddrawing.list)
        self.appendToolbar("Design456_Segmented",_segmented.Design456_Segmented.list)
        
        self.appendToolbar("Design456 Tools", _tools.Design456Part_Tools.list)
        self.appendToolbar("Design456 Alignment", _alignment.Design456_Alignment_Tools.list)
        self.appendToolbar(
            "Selection Mode", SelGate.Design456_SelectionGate.list)
        self.appendToolbar("Direct Modeling",
                           dModeling.Design456_DirectModeling.list)
        self.appendToolbar ("GridSize",_grid.Design456_GridSize.list)

        self.appendMenu("Design456Part", designPart.Design456Part.list)
        self.appendMenu("Design456_2Ddrawing",
                        TwoDDraw.Design456_2Ddrawing.list)
        self.appendMenu("Design456 Tools", _tools.Design456Part_Tools.list)
        self.appendMenu("Design456 Alignment", _alignment.Design456_Alignment_Tools.list)
        
        # Defeaturing WB  added to Design456 
        self.appendToolbar("Defeaturing Tools", ["DF_SelectLoop","refineFeatureTool","DefeatShapeFeature"])
        #self.appendMenu("ksu Tools", ["ksuTools","ksuToolsEdit"])
        self.appendMenu("Defeaturing Tools", ["refineFeatureTool","DF_SelectLoop"])
        self.appendToolbar("Fuzzy Tools", ["FuzzyCut","FuzzyUnion","FuzzyCommon"])
        self.appendMenu("Fuzzy Tools", ["FuzzyCut","FuzzyUnion","FuzzyCommon"])
        Gui.addIconPath(Design456Init.ICON_PATH)

        # Design456Part
        # self.appendMenu(QT_TRANSLATE_NOOP("Draft", "&Drafting"), self.drawing_commands)

        # Design456Part
        # DRAFT
        def QT_TRANSLATE_NOOP(context, text):
            return text

        # Run self-tests
        dependencies_OK = False
        try:
            from pivy import coin
            if FreeCADGui.getSoDBVersion() != coin.SoDB.getVersion():
                raise AssertionError("FreeCAD and Pivy use different versions "
                                     "of Coin. "
                                     "This will lead to unexpected behaviour.")
        except AssertionError:
            FreeCAD.Console.PrintWarning("Error: FreeCAD and Pivy "
                                         "use different versions of Coin. "
                                         "This will lead to unexpected "
                                         "behaviour.\n")
        except ImportError:
            FreeCAD.Console.PrintWarning("Error: Pivy not found, "
                                         "Draft Workbench will be disabled.\n")
        except Exception:
            FreeCAD.Console.PrintWarning("Error: Unknown error "
                                         "while trying to load Pivy.\n")
        else:
            dependencies_OK = True

        if not dependencies_OK:
            return

        # Import Draft tools, icons
        try:
            import Draft_rc
            import DraftTools
            import DraftGui
            import DraftFillet
            Gui.addLanguagePath(":/translations")
            Gui.addIconPath(":/icons")
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Initializing one or more "
                                       "of the Draft modules failed, "
                                       "Draft will not work as expected.\n")

        # Set up command lists
        import draftutils.init_tools as it
        self.drawing_commands = it.get_draft_drawing_commands()
        self.annotation_commands = it.get_draft_annotation_commands()
        self.modification_commands = it.get_draft_modification_commands()
        self.utility_commands_menu = it.get_draft_utility_commands_menu()
        self.utility_commands_toolbar = it.get_draft_utility_commands_toolbar()
        self.context_commands = it.get_draft_context_commands()

        # Set up toolbars
        it.init_toolbar(self,
                        QT_TRANSLATE_NOOP("Draft", "Draft creation tools"),
                        self.drawing_commands)
        it.init_toolbar(self,
                        QT_TRANSLATE_NOOP("Draft", "Draft annotation tools"),
                        self.annotation_commands)
        it.init_toolbar(self,
                        QT_TRANSLATE_NOOP("Draft", "Draft modification tools"),
                        self.modification_commands)
        it.init_toolbar(self,
                        QT_TRANSLATE_NOOP("Draft", "Draft utility tools"),
                        self.utility_commands_toolbar)

        # Set up menus
        it.init_menu(self,
                     [QT_TRANSLATE_NOOP("Draft", "&Drafting")],
                     self.drawing_commands)
        it.init_menu(self,
                     [QT_TRANSLATE_NOOP("Draft", "&Annotation")],
                     self.annotation_commands)
        it.init_menu(self,
                     [QT_TRANSLATE_NOOP("Draft", "&Modification")],
                     self.modification_commands)
        it.init_menu(self,
                     [QT_TRANSLATE_NOOP("Draft", "&Utilities")],
                     self.utility_commands_menu)

        # Set up preferences pages
        if hasattr(Gui, "draftToolBar"):
            if not hasattr(Gui.draftToolBar, "loadedPreferences"):
                Gui.addPreferencePage(":/ui/preferences-draft.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                Gui.addPreferencePage(":/ui/preferences-draftinterface.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                Gui.addPreferencePage(":/ui/preferences-draftsnap.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                Gui.addPreferencePage(":/ui/preferences-draftvisual.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                Gui.addPreferencePage(":/ui/preferences-drafttexts.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                Gui.draftToolBar.loadedPreferences = True

        App.Console.PrintLog('Loading Draft workbench, done.\n')

    def Activated(self):
        try:
            import WorkingPlane
            from plane import Grid as gr
            from plane import DocObserver
            from Design456Pref import Design456pref_var
            import Design456Pref            
            import draftutils
            
            #retrieve preferences from user.cfg
            Design456Pref.Design456Preferences().loadSettings()
            Design456pref_var.PlaneGridEnabled=Design456Pref.getPlaneGrid()
            Design456pref_var.PlaneGridSize=Design456Pref.getPlaneGridSize()
            Design456pref_var.Simplified==Design456Pref.getSimplified()
            Design456pref_var.MouseStepSize=Design456Pref.getMouseStepSize()
            Design456pref_var.BKGColor = Design456Pref.getBKGColor()
            Design456pref_var.pickSize=Design456Pref.getPickSize()         
             
            if (self.myDocObserver is None):
                self.myDocObserver = DocObserver()
                self.myDocObserver.setLink(self)
            App.addDocumentObserver(self.myDocObserver)
            if not(App.ActiveDocument):
                App.newDocument()
                Gui.ActiveDocument.ActiveView.setCameraType("Perspective")
                
            # FROM DRAFT
            if hasattr(Gui, "draftToolBar"):
                Gui.draftToolBar.Activated()
            if hasattr(Gui, "Snapper"):
                Gui.Snapper.show()
                import draftutils.init_draft_statusbar as dsb
                dsb.show_draft_statusbar()
            # Fix the view of the grid make it as 123D Design
            App.DraftWorkingPlane.alignToPointAndAxis(
                App.Vector(0.0, 0.0, 0.0), App.Vector(0, 0, 1), 0.0)
            # Show the Grid always
            # g=gridTracker()
            _view = Gui.ActiveDocument.ActiveView
            # New plane axis 2021-03-22
            if (self.planeShow is None):
                self.planeShow = gr(_view)
                self.planeShow.Activated()
            # g.ff()                #draft Grid  --> I will try to remove it in the future Mariwan 2021-03-22
            # Show Top view - Isometric always
            if self.runOnce == True:
                _view.viewTop()
                _view.viewIsometric()
                # Gui.SendMsgToActiveView("ViewFit")
                for TT in range(1, 10):
                    _view.zoomOut()
                self.runOnce = False
            App.Console.PrintLog(
                "Draft workbench activated Inside Design456.\n")
            # Turn OFF grid          #TODO:Make This permanent
            Gui.Snapper.grid.off()
            App.Console.PrintMessage('Design456 workbench loaded\n')
            return

        except Exception as err:
            App.Console.PrintError("'Error: Design456 activation' Failed.\n"
                                   "Design456 will not work as expected.\n "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Deactivated(self):
        from plane import Grid as gr
        # from plane import DocObserver
        try:
            "workbench deactivated"
            if hasattr(Gui, "draftToolBar"):
                Gui.draftToolBar.Deactivated()
            if hasattr(Gui, "Snapper"):
                Gui.Snapper.hide()
                import draftutils.init_draft_statusbar as dsb
                dsb.hide_draft_statusbar()
            App.Console.PrintLog(
                "Design456/Draft workbench deactivated.\n")
            # gr.removeGarbage(gr)
            self.planeShow.removeGarbage()
            del self.planeShow
            self.planeShow = None
            App.removeDocumentObserver(self.myDocObserver)
            self.myDocObserver = None
            return
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Draft deactivation failed\n")

    def ContextMenu(self, recipient):
        "right-clicks on screen"
        try:
            import BOPTools  # as bop
            import Design456Part as designPart
            import Design456Part_Tools as pTools
            import Design456_2Ddrawing as TwoDDraw
            import Design456_Alignment as _alignment
            import Design456_Grid as _grid

            self.appendContextMenu(
                "Design456Part", designPart.Design456Part.list)
            self.appendContextMenu("Design456_2Ddrawing",
                                   TwoDDraw.Design456_2Ddrawing.list)
            self.appendContextMenu(
                "Design456 Tools", pTools.Design456Part_Tools.list)
            self.appendContextMenu("Design456 Alignment", 
                                        _alignment.Design456_Alignment_Tools.list)
            # from Design456Part
            self.appendContextMenu(
                "Design456Part", designPart.Design456Part.list)
            
            self.appendContextMenu ("GridSize",_grid.Design456_GridSize.list)
           
            # from DRAFT
            """Define an optional custom context menu."""
            from DraftGui import translate
            if recipient == "View":
                if App.activeDraftCommand is None:
                    if Gui.Selection.getSelectionEx():
                        self.appendContextMenu(
                            "Draft", self.drawing_commands + self.modification_commands)
                        self.appendContextMenu(
                            "Utilities", self.context_commands)
                    else:
                        self.appendContextMenu("Draft", self.drawing_commands)
            else:
                if Gui.Selection.getSelectionEx():
                    self.appendContextMenu("Utilities", self.context_commands)
            # END DRAFT
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Draft ContexMenu "
                                   "failed, "
                                   "Design456 will not work as expected.\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(Design456())
# FROM DRAFT
# Preference pages for importing and exporting various file formats
# are independent of the loading of the workbench and can be loaded at startup
Gui.addPreferencePage(
    ":/ui/preferences-dxf.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-dwg.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-svg.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-oca.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))

App.__unit_test__ += ["TestDraftGui"]