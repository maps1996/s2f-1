import h5py 

class Region(object):
    """assign material and source to region."""
    def __init__(self, mesh):
        self.name = mesh.get_domain_group_names()
        self.num  = len(self.name)
        self.idx  = list(range(1,self.num+1))
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
        
    def export_h5(self, h5file=None):
        if not (self.mat_assigned and self.source_assigned):
            print ("ERROR: region material and source has not been assigned!")
        if h5file is None:
            h5file = h5py.File('region.h5','w')
        pref = 'region'
        h5file[pref + '/group_index'] = self.idx 
        h5file[pref + '/group_names'] = self.name
        h5file[pref + '/nr'] = self.num
        h5file[pref + '/m_idx'] = self.m_idx
        h5file[pref + '/s_idx'] = self.s_idx
        h5file.close()
        print('Done exporting region information')
        
        
        