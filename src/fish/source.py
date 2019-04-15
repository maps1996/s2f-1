import numpy as np
import h5py


class Source_h5(object):
    def __init__(self, name, srclist):
        self.srcname = name
        self.srclist = srclist

    def export_h5(self, h5file):
        h5file['/source/' + self.srcname
               ] = np.array(self.srclist, dtype=np.float)
