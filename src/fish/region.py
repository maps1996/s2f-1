import h5py
import numpy as np


class Region(object):
    """assign material and source to region."""

    def __init__(self, mesh):
        self.name = mesh.get_domain_group_names()
        self.num = len(self.name)
        self.idx = list(range(1, self.num + 1))
        self.mat_assigned = False
        self.source_assigned = False
        self.m_idx = None
        self.s_idx = None

    def set_midx(self, midx):
        if(len(midx) != self.num):
            print ("ERROR: set region material error!")
        self.m_idx = midx
        self.mat_assigned = True

    def set_sidx(self, sidx):
        if(len(sidx) != self.num):
            print ("ERROR: set region source error!")
        self.s_idx = sidx
        self.source_assigned = True

    def export_h5(self, h5file):
        pref = 'region'
        if pref in h5file.keys():
            h5file.__delitem__(pref)
        h5file[pref + '/group_index'] = self.idx
        h5file[pref + '/group_names'] = np.string_(self.name)
        h5file[pref + '/nr'] = self.num
        h5file[pref + '/m_idx'] = self.m_idx
        h5file[pref + '/s_idx'] = self.s_idx
        print('Done exporting region information')
