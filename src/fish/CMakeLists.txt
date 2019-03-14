
SET(_bin_SCRIPTS
  __init__.py
  mesh.py
  region.py
  boundary.py
  solver_parameter.py
)

# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_PYTHON}/fish)