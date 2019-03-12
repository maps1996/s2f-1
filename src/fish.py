
from salome2fish import salome2fish
import numpy as np
import time
from trans2 import *
# from assignBC import *
# from assign_mat import *
# from setSP import *
# from assignSource import *
from fish_appGUI import assign_mat
from fish_appGUI import assign_bc
from fish_appGUI import assign_sp
from fish_appGUI import assign_src
from fish_appGUI import assign_mh

tstart = time.time()

data = salome2fish()
data.list_meshs()

# assign mesh
data.set_work_mesh(assign_mh.work_mesh)
data.list_groups()

# sh
data.sh_pn = assign_sp.sph_pn

# solver
data.solver_eps = assign_sp.eps
data.solver_irst = assign_sp.irst

# assign material& source index
mat_idx = np.array(assign_mat.mat_idx, dtype=np.int64)
src_idx = np.array(assign_mat.src_idx, dtype=np.int64)
if mat_idx.size != data.domain_group_number:
    print ("ERROR: mat_idx.size != data.domain_group_number")

data.set_domain_group_material(mat_idx)
data.set_domain_group_source(src_idx)
data.set_source_group(assign_mat.nsrc)

# assign bc
bt_idx = np.array(assign_bc.bt_idx, dtype=np.int64)
bc_idx = np.array(assign_bc.bc_idx, dtype=np.int64)

if bc_idx.size != data.boundary_group_number:
    print ("ERROR: bc_idx.size != data.boundary_group_number")

data.set_boundary_group_type(bt_idx)
data.set_boundary_group_condition(bc_idx)

# material


data.export_h5()

# source
for i in range(assign_mat.nsrc):
    data.h5file['/source/' + assign_src.SrcList1[i]
                ] = np.array(assign_src.SrcList[i].list, dtype=np.float)
data.close_h5()

# xs
export_mat()
print ("Done exporting!\n")
print ("Total time: %0.f s\n" % (time.time() - tstart))
