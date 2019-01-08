app_name_=fish_app
salome_root_dir_=/home/maps/app/SALOME-8.5.0-UB16.04-SRC
salome_app_root_dir_=/home/maps/app/SALOME-8.5.0-UB16.04-SRC/app
salome_app_install_dir_=$salome_app_root_dir_/install

source $salome_root_dir_/env_launch.sh
export CONFIGURATION_ROOT_DIR=$salome_root_dir_/SOURCES/CONFIGURATION/

if [[ ! -d "./build/" ]]; then
  #statements
  mkdir build
else
  rm -rf build
  mkdir build
fi
cd build
cmake -DCMAKE_INSTALL_PREFIX=$salome_app_install_dir_/$app_name_ ..
make
make install
cd ..
rm -rf build
