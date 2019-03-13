app_name_=fish_app
user_name_=superfun/fc
salome_version_=SALOME-9.2.0-UB18.04-SRC
salome_root_dir_=/home/$user_name_/app/$salome_version_
salome_app_root_dir_=/home/$user_name_/salome_app
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
