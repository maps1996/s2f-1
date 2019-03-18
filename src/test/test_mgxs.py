from fish.mgxs import *

transx_file = 'transx.out'
xs = MGXS(transx_file)
xs.export_h5()
