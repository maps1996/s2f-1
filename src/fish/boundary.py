import h5py
import numpy as np


class Boundary(object):
    """assign material and source to region."""

    def __init__(self, mesh):
        self.name = mesh.get_boundary_group_names()
        self.num = len(self.name)
        self.idx = list(range(1, self.num + 1))
        self.cond_assigned = False
        self.type_assigned = False
        self.cond = None
        self.type = None

    def set_cond(self, cond):
        if(len(cond) != self.num):
            print ("ERROR: set boundary condition error!")
        self.cond = cond
        self.cond_assigned = True

    def set_type(self, type):
        if(len(type) != self.num):
            print ("ERROR: set boundary type error!")
        self.type = type
        self.type_assigned = True

    def export_h5(self, h5file):
        pref = 'bc'
        if pref in h5file.keys():
            h5file.__delitem__(pref)
        h5file[pref + '/group_index'] = self.idx
        h5file[pref + '/group_names'] = np.string_(self.name)
        h5file[pref + '/nb'] = self.num
        h5file[pref + '/cond'] = self.cond
        h5file[pref + '/type'] = self.type
        print('Done exporting boundary information')
