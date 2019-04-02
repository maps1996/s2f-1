import numpy as np
import numpy as np

class SolverParameter(object):
    """docstring for SolverParameter."""
    def __init__(self):
        self.kmethod = np.string_('RGMRES ')
        self.ptype = np.string_('BJAC ')
        self.afmt  = np.string_('CSR ')
        self.itmax = 1000
        self.irst  = 100
        self.eps   = 1.0e-5
        self.istop = 2
        self.itrace= 0

    def export_h5(self, h5file):
        pref = 'solver'
        h5file[pref + '/kmethod'] = np.string_(self.kmethod+" ")
        h5file[pref + '/ptype'] = np.string_(self.ptype+" ")
        h5file[pref + '/afmt'] = np.string_(self.afmt+" ")
        h5file[pref + '/itmax'] = self.itmax
        h5file[pref + '/irst'] = self.irst
        h5file[pref + '/eps'] = self.eps
        h5file[pref + '/istop'] = self.istop
        h5file[pref + '/itrace'] = self.itrace
        print('Done exporting solver parameter information')
