import SMESH
from salome.smesh import smeshBuilder
import salome
import h5py
import numpy as np
import time


class salome2fish():

    """docstring for salome2fish."""

    def __init__(self):
        # file
        self.filename = 'fish.h5'
        self.h5file = []

        # mesh
        self.meshs = list()
        self.mesh_names = []
        self.meshs_exist = False
        self.work_mesh = []
        self.mesh_assigned = False

        # material index
        self.domain_group_number = 0
        self.domain_group_index = []
        self.domain_group_names = []
        self.domain_group_material = []
        self.domain_group_source = []
        self.material_assigned = False
        self.source_assigned = False

        # boundary condition
        self.boundary_group_number = 0
        self.boundary_group_index = []
        self.boundary_group_names = []
        self.boundary_group_condition = []
        self.boundary_group_type = []
        self.bc_assigned = False
        self.btype_assigned = False

        # solver parameter
        self.solver_kmethod = np.string_('RGMRES ')
        self.solver_ptype = np.string_('BJAC ')
        self.solver_afmt = np.string_('CSR ')
        self.solver_itmax = 1000
        self.solver_irst = 100
        self.solver_eps = 1.0e-5
        self.solver_istop = 2
        self.solver_itrace = 0

        # material

        # source
        #self.num_source = 1

        # spherical harmonics
        self.sh_pn = 1
        self.sh_type = 1

    def open_h5(self):
        self.h5file = h5py.File(self.filename, 'w')

    def close_h5(self):
        self.h5file.close()

    ##
    def list_meshs(self):
        smesh = smeshBuilder.New()
        self.mesh_names = []
        self.meshs_exist = False
        smeshComp = salome.myStudy.FindComponent("SMESH")
        if smeshComp:
            iterater = salome.myStudy.NewChildIterator(smeshComp)
            while iterater.More():
                sobj = iterater.Value()
                iterater.Next()
                if not hasattr(sobj.GetObject(), "NbNodes"):
                    continue
                mesh = smesh.Mesh(sobj.GetObject())
                self.meshs_exist = True
                self.meshs.append(mesh)
                self.mesh_names.append(mesh.GetName())
        if not self.meshs_exist:
            print ("ERROR: there are no meshs")

    def set_work_mesh(self, mesh_name):
        smesh = smeshBuilder.New()
        mesh_path = "/Mesh/" + mesh_name
        obj = salome.myStudy.FindObjectByPath(mesh_path).GetObject()
        self.mesh_assigned = False
        if obj:
            self.work_mesh = smesh.Mesh(obj)
            self.mesh_assigned = True
        if not self.mesh_assigned:
            print ("ERROR: there are no mesh named : " + mesh_name)

    #
    def list_groups(self):
        if not self.mesh_assigned:
            print ("ERROR: the work mesh has not been seted ")
        if self.work_mesh.NbVolumes() > 0:
            domain = SMESH.VOLUME
            boundary = SMESH.FACE
        else:
            domain = SMESH.FACE
            boundary = SMESH.EDGE

        #>> domain group information
        gid = 0
        for grp in self.work_mesh.GetGroups(domain):
            gid = gid + 1
            self.domain_group_names.append(grp.GetName())
            self.domain_group_index.append(gid)
        self.domain_group_number = gid
        #>> boundary group infomation
        gid = 0
        for grp in self.work_mesh.GetGroups(boundary):
            gid = gid + 1
            self.boundary_group_names.append(grp.GetName())
            self.boundary_group_index.append(gid)
        self.boundary_group_number = gid

    def set_domain_group_material(self, mat_idx):
        if(len(mat_idx) != self.domain_group_number):
            print ("ERROR: set region material error!")
        self.domain_group_material = mat_idx
        self.material_assigned = True

    def set_domain_group_source(self, src_idx):
        if(len(src_idx) != self.domain_group_number):
            print ("ERROR: set region source error!")
        self.domain_group_source = src_idx
        self.source_assigned = True

    def set_boundary_group_type(self, bc_type):
        if(len(bc_type) != self.boundary_group_number):
            print ("ERROR: set boundary condition error!")
        self.boundary_group_type = bc_type
        self.btype_assigned = True

    def set_boundary_group_condition(self, bc_idx):
        if(len(bc_idx) != self.boundary_group_number):
            print ("ERROR: set boundary condition error!")
        self.boundary_group_condition = bc_idx
        self.bc_assigned = True

    def set_source_group(self, nsrc):
        self.num_source = nsrc

    def export_h5(self):
        if not self.mesh_assigned:
            print ("ERROR: mesh has not been assigned!")
        if not self.material_assigned:
            print ("ERROR: material has not been assigned!")
        if not self.source_assigned:
            print ("ERROR: source has not been assigned!")
        if not self.btype_assigned:
            print ("ERROR: boundary type has not been assigned!")
        if not self.bc_assigned:
            print ("ERROR: bc has not been assigned!")

        if self.work_mesh.NbVolumes() > 0:
            nd = 3
            domain = SMESH.VOLUME
            boundary = SMESH.FACE
            ne = self.work_mesh.NbVolumes()
            ne_b = self.work_mesh.NbFaces()
            ne_e = self.work_mesh.NbEdges()
            ne_t = ne_b + ne_e
            enn = 4
            enn_b = 3
        else:
            nd = 2
            domain = SMESH.FACE
            boundary = SMESH.EDGE
            ne = self.work_mesh.NbFaces()
            ne_b = self.work_mesh.NbEdges()
            ne_e = 0
            ne_t = ne_b
            enn = 3
            enn_b = 2

        self.open_h5()
        # mesh header
        # ===========================================

        # mesh nodes
        # ===========================================
        nn = self.work_mesh.NbNodes()
        coo = np.zeros((nn, 3), dtype=np.float)
        nid = self.work_mesh.GetElementsByType(SMESH.NODE)
        n = 0
        for id in nid:
            coo[n, :] = self.work_mesh.GetNodeXYZ(id)
            n = n + 1

        # meshName = self.work_mesh.GetName()
        meshName = 'mesh'
        self.h5file[meshName + '/nodes/nd'] = nd
        self.h5file[meshName + '/nodes/nn'] = nn
        self.h5file[meshName + '/nodes/id'] = nid
        self.h5file[meshName + '/nodes/coo'] = coo
        # ===========================================
        # mesh domain
        eni = np.zeros((ne, enn), dtype=np.int64)
        eid = self.work_mesh.GetElementsByType(domain)

        e = 0
        for el in eid:
            eni[e, :] = self.work_mesh.GetElemNodes(el)
            e = e + 1

        self.h5file[meshName + '/domain/ne'] = ne
        self.h5file[meshName + '/domain/enn'] = enn
        self.h5file[meshName + '/domain/eni'] = eni
        self.h5file[meshName + '/domain/id'] = eid
        self.h5file[meshName + '/domain/type'] = nd
        # ===========================================
        # domain group infomation
        er = np.zeros((ne), dtype=np.int64)

        groupID = 1
        for grp in self.work_mesh.GetGroups(domain):
            for el in grp.GetIDs():
                e = el - ne_t - 1
                er[e] = groupID
            groupID = groupID + 1
        self.h5file[meshName + '/domain/er'] = er
        # ===========================================
        # mesh boundary (the boundary element contains inner boundary)
        eni_b = np.zeros((ne_b, enn_b), dtype=np.int64)
        eid_b = self.work_mesh.GetElementsByType(boundary)

        e = 0
        for el in eid_b:
            eni_b[e, :] = self.work_mesh.GetElemNodes(el)
            e = e + 1

        self.h5file[meshName + '/boundary/ne'] = ne_b
        self.h5file[meshName + '/boundary/enn'] = enn_b
        self.h5file[meshName + '/boundary/eni'] = eni_b
        self.h5file[meshName + '/boundary/id'] = eid_b
        self.h5file[meshName + '/boundary/type'] = nd - 1
        # ===========================================
        # boundary group infomation ( the inner boundary ID is 0)
        er_b = np.zeros((ne_b), dtype=np.int64)

        groupID = 1
        for grp in self.work_mesh.GetGroups(boundary):
            for el in grp.GetIDs():
                e = el - ne_e - 1
                er_b[e] = groupID
            groupID = groupID + 1
        self.h5file[meshName + '/boundary/er'] = er_b

        #===========================================
        # region
        dgn_encode = list()
        for dg_names in self.domain_group_names:
            dgn_encode.append(dg_names.encode())
        self.h5file['/region/group_index'] = self.domain_group_index
        self.h5file['/region/group_names'] = dgn_encode
        self.h5file['/region/nr'] = self.domain_group_number
        self.h5file['/region/m_idx'] = self.domain_group_material
        self.h5file['/region/s_idx'] = self.domain_group_source

        #===========================================
        # boundary condition
        bgn_encode = list()
        for bg_names in self.boundary_group_names:
            bgn_encode.append(bg_names.encode())
        self.h5file['/bc/group_index'] = self.boundary_group_index
        self.h5file['/bc/group_names'] = bgn_encode
        self.h5file['/bc/nb'] = self.boundary_group_number
        self.h5file['/bc/type'] = self.boundary_group_type
        self.h5file['/bc/cond'] = self.boundary_group_condition
        #===========================================
        # solver
        self.h5file['/solver/kmethod'] = self.solver_kmethod
        self.h5file['/solver/ptype'] = self.solver_ptype
        self.h5file['/solver/afmt'] = self.solver_afmt
        self.h5file['/solver/itmax'] = self.solver_itmax
        self.h5file['/solver/irst'] = self.solver_irst
        self.h5file['/solver/eps'] = self.solver_eps
        self.h5file['/solver/istop'] = self.solver_istop
        self.h5file['/solver/itrace'] = self.solver_itrace

        #===========================================
        # material

        #===========================================
        # source
        self.h5file['/source/ns'] = self.num_source
        #self.h5file['/source/s1'] = np.array([1.0], dtype=np.float)

        #===========================================
        # spherical harmonics
        self.h5file['/sh/pn'] = self.sh_pn
        self.h5file['/sh/type'] = self.sh_type

        #===========================================
        # attribute
        self.h5file.attrs['auther'] = 'fang chao'
        self.h5file.attrs['date'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        self.h5file.attrs['problem'] = '2d 2 region problem'
        self.h5file.attrs['description'] = 'the hdf5 input file for fish created by salome2fish'

        # self.close_h5()
