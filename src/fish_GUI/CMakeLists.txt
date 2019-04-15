
SET(_bin_SCRIPTS
  __init__.py
  fish_window_handler.py
  make_transx_input.py
  defineMaterial.py
  assignMesh.py
  assignBC.py
  assignMat.py
  setSP.py
  assignSource.py
  combobox.py
)

# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_PYTHON}/fish_GUI)
