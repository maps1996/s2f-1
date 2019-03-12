
INCLUDE(UseQtExt)

# additional include directories
INCLUDE_DIRECTORIES(
  ${QT_INCLUDES}
)

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
  fish.py
  trans2.py
  mgxs/fendl_library.py
  mesh.py
)

# --- resources ---

# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_SCRIPT_PYTHON})
