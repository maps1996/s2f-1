
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
)

# --- resources ---
# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_SCRIPT_PYTHON})

SET(SUBDIRS
fish
fish_GUI
)


FOREACH(dir ${SUBDIRS})
 ADD_SUBDIRECTORY(${dir})
ENDFOREACH(dir ${SUBDIRS})
