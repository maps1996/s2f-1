import traceback
import os
from SalomePyQt import *
from qtsalome import *

# Get SALOME PyQt interface
sgPyQt = SalomePyQt()

from fish_GUI import *
import fish_GUI.fish_window_handler as fwh

global main
if os.getenv("already_initialized", "0") != "1":
    main = fwh.FishWindowHandler()

os.environ["already_initialized"] = "1"


################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################

class GUIcontext:

    # constructor
    def __init__(self):
        # Create 'fish' menu
        fish_mid = sgPyQt.createMenu("Fish", -1, -1, sgPyQt.defaultMenuGroup())
        # create toolbar
        fish_tid = sgPyQt.createTool("Fish")
        # about action
        about_id = sgPyQt.createAction(dict_actions["about_fish"],
                                       "About", "About", "software information", "about_fish.png")

        assign_mesh_id = sgPyQt.createAction(dict_actions["assign_mesh"],
                                             "Assign mesh", "Assign mesh", "software information", "assign_mesh.png")

        define_material_id = sgPyQt.createAction(dict_actions["define_material"],
                                                 "Define material", "Define material", "software information", "define_material.png")

        assign_material_id = sgPyQt.createAction(dict_actions["assign_material"],
                                                 "Assign material", "Assign material", "software information", "assign_material.png")

        set_solver_parameter_id = sgPyQt.createAction(dict_actions["set_solver_parameter"],
                                                      "Set solver parameter", "Set solver parameter", "software information", "set_solver_parameter.png")

        assign_boundary_condition_id = sgPyQt.createAction(dict_actions["assign_boundary_condition"],
                                                           "Assign boundary condition", "Assign boundary condition", "software information", "assign_boundary_condition.png")

        assign_source_id = sgPyQt.createAction(dict_actions["assign_source"],
                                               "Assign source", "Assign source", "software information", "assign_source.png")

        run_fish_id = sgPyQt.createAction(dict_actions["run_fish"],
                                          "Run fish", "Run fish", "software information", "run_fish.png")

        # Add actions in the menu 'Fish'
        sgPyQt.createMenu(assign_mesh_id, fish_mid)
        sgPyQt.createMenu(define_material_id, fish_mid)
        sgPyQt.createMenu(assign_material_id, fish_mid)
        sgPyQt.createMenu(assign_boundary_condition_id, fish_mid)
        sgPyQt.createMenu(set_solver_parameter_id, fish_mid)
        sgPyQt.createMenu(assign_source_id, fish_mid)
        sgPyQt.createMenu(run_fish_id, fish_mid)
        sgPyQt.createMenu(about_id, fish_mid)

        # Add actions in the tool 'Fish'

        sgPyQt.createTool(assign_mesh_id, fish_tid)
        sgPyQt.createTool(define_material_id, fish_tid)
        sgPyQt.createTool(assign_material_id, fish_tid)
        sgPyQt.createTool(assign_boundary_condition_id, fish_tid)
        sgPyQt.createTool(set_solver_parameter_id, fish_tid)
        sgPyQt.createTool(assign_source_id, fish_tid)
        sgPyQt.createTool(run_fish_id, fish_tid)
        sgPyQt.createTool(about_id, fish_tid)


def assign_mesh():
    global assign_mh
    assign_mh = assignMesh(sgPyQt.getDesktop(), 1)
    assign_mh.setMeshNames(mh.mesh_names)
    assign_mh.initUI()
    assign_mh.exec_()


def define_material():
    # create dialog box
    d = defineMaterial(sgPyQt.getDesktop(), 1)
    # show dialog box
    d.exec_()
    pass


def assign_material():
    global assign_mh, assign_src
    if(not mh.mesh_assigned):
        QMessageBox.information(sgPyQt.getDesktop(), "Error",
                                "The mesh has not been assigned")
    assign_mat = assignMat(sgPyQt.getDesktop(), 1)
    assign_mat.setRegionNames(assign_mh.domain_names)
    assign_mat.setSource(assign_src.SrcList1)
    assign_mat.initUI()
    assign_mat.exec_()


def assign_boundary_condition():
    global assign_mh
    if(not mh.mesh_assigned):
        QMessageBox.information(sgPyQt.getDesktop(), "Error",
                                "The mesh has not been assigned")

    assign_bc = assignBC(sgPyQt.getDesktop(), 1)
    assign_bc.setBoundaryNames(assign_mh.boundary_names)
    assign_bc.initUI()
    assign_bc.exec_()


def set_solver_parameter():
    assign_sp = setSP(sgPyQt.getDesktop(), 1)
    assign_sp.initUI()
    assign_sp.exec_()


def assign_source():
    global assign_src
    assign_src = assignSrc(sgPyQt.getDesktop(), 1)
    assign_src.initUI()
    assign_src.exec_()


def run_fish():
    QMessageBox.information(sgPyQt.getDesktop(), "Information",
                            "fish is a radiation shielding calculation program using finite element & spherical harmonics method")


def about_fish():
    main.about()


################################################
# verbosity level
__verbose__ = None

###
# Get verbose level
###


def verbose():
    global __verbose__
    if __verbose__ is None:
        try:
            __verbose__ = int(os.getenv('SALOME_VERBOSE', 0))
        except:
            __verbose__ = 0
            pass
        pass
    return __verbose__

# Create actions and menus


def initialize():
    if verbose():
        print("fish_appGUI::initialize()")
    return

# called when module is activated
# returns True if activating is successfull and False otherwise


def activate():
    if verbose():
        print("fish_appGUI.activate()")
    GUIcontext()
    return True

# called when module is deactivated


def deactivate():
    if verbose():
        print("fish_appGUI.deactivate()")
    pass

# Process GUI action


def OnGUIEvent(commandID):
    if verbose():
        print("fish_appGUI::OnGUIEvent : commandID = %d" % commandID)
    if commandID in dict_commands:
        try:
            dict_commands[commandID]()
        except:
            traceback.print_exc()
    else:
        if verbose():
            print("The command is not implemented: %d" % commandID)
    pass


# Define commands
dict_commands = {
    901: assign_mesh,
    902: define_material,
    903: assign_material,
    904: assign_boundary_condition,
    905: set_solver_parameter,
    906: assign_source,
    998: run_fish,
    999: about_fish,
}

# Define actions
dict_actions = {
    "assign_mesh": 901,
    "define_material": 902,
    "assign_material": 903,
    "assign_boundary_condition": 904,
    "set_solver_parameter": 905,
    "assign_source": 906,
    "run_fish": 998,
    "about_fish": 999,
}
