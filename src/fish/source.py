import numpy as np 

class Source(object):
    def __init__(self, ns, ng):
        self.ns = ns
        self.ng = ng
        self.density = np.zeros(ng,ns)
        
        
    def set_density(self, source, density):
        
        