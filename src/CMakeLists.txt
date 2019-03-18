
INCLUDE(UseQtExt)

# additional include directories
INCLUDE_DIRECTORIES(
  ${QT_INCLUDES}
)
##
# Common packages
##

# --- scripts ---

# scripts / static
SET(_bin_SCRIPTS
  fish_appGUI.py
  salome2fish.py
  fish_window_handler.py
  make_transx_input.py
  defineMaterial.py
  assignMesh.py
  assignBC.py
  assignMat.py
  setSP.py
  assignSource.py
)

# --- resources ---
# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_SCRIPT_PYTHON})

SET(SUBDIRS
fish
)

FOREACH(dir ${SUBDIRS})
 ADD_SUBDIRECTORY(${dir})
ENDFOREACH(dir ${SUBDIRS})
