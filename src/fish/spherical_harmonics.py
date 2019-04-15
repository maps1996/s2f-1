
class SphericalHarmonics(object):
    """docstring for SphericalHarmonics."""

    def __init__(self, order):
        self.order = order
        self.type = 1

    def export_h5(self, h5file):
        pref = 'sh'
        if pref in h5file.keys():
            h5file.__delitem__(pref)
        h5file[pref + '/pn'] = self.order
        h5file[pref + '/type'] = self.type
