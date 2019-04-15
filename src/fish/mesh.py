import SMESH
from salome.smesh import smeshBuilder
import salome
import h5py
import numpy as np


class Mesh(object):
    """docstring for salome_mesh."""

    def __init__(self, mesh_name=None):
        self.meshs = list()
        self.mesh_names = []
        self.meshs_exist = False
        self.work_mesh = None
        self.mesh_assigned = False
        self.nd = 0
        self.domain = None
        self.boundary = None
        self.init_meshs()
        if mesh_name is not None:
            self.set_work_mesh(mesh_name)

    def init_meshs(self):
        "init meshs lists"
        smesh = smeshBuilder.New()
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
        "set which mesh to export"
        self.mesh_name = mesh_name
        smesh = smeshBuilder.New()
        mesh_path = "/Mesh/" + mesh_name
        obj = salome.myStudy.FindObjectByPath(mesh_path).GetObject()
        # print(type(obj))
        if obj:
            self.work_mesh = smesh.Mesh(obj)
            self.mesh_assigned = True
        if not self.mesh_assigned:
            print ("ERROR: there are no mesh named : " + mesh_name)
        # get mesh infomation
        self.nn = self.work_mesh.NbNodes()
        if(self.work_mesh.NbVolumes() > 0):
            self.nd = 3
            self.ne = self.work_mesh.NbVolumes()
            self.ne_b = self.work_mesh.NbFaces()
            self.domain = SMESH.VOLUME
            self.boundary = SMESH.FACE
        elif(self.work_mesh.NbFaces() > 0):
            self.nd = 2
            self.ne = self.work_mesh.NbFaces()
            self.ne_b = self.work_mesh.NbEdges()
            self.domain = SMESH.FACE
            self.boundary = SMESH.EDGE
        elif(self.work_mesh.NbEdges() > 0):
            self.nd = 1
            self.ne = self.work_mesh.NbEdges()
            self.ne_b = 2
            self.domain = SMESH.EDGE
            self.boundary = SMESH.NODE
        else:
            self.nd = 0

        #
    def get_dimension(self):
        return self.nd

    def get_domain_group_names(self):
        domain_group_names = []
        for grp in self.work_mesh.GetGroups(self.domain):
            domain_group_names.append(grp.GetName() + " ")
        return domain_group_names

    def get_boundary_group_names(self):
        boundary_group_names = []
        for grp in self.work_mesh.GetGroups(self.boundary):
            boundary_group_names.append(grp.GetName() + " ")
        return boundary_group_names

    def export_h5(self, h5file=None):
        if not self.mesh_assigned:
            print ("ERROR: mesh has not been assigned!")
        if h5file is None:
            h5file = h5py.File(self.mesh_name + '.h5', 'w')

        if self.nd == 3:
            ne = self.work_mesh.NbVolumes()
            ne_b = self.work_mesh.NbFaces()
            ne_e = self.work_mesh.NbEdges()
            ne_t = ne_b + ne_e
            enn = 4
            enn_b = 3
        elif self.nd == 2:
            ne = self.work_mesh.NbFaces()
            ne_b = self.work_mesh.NbEdges()
            ne_e = 0
            ne_t = ne_b
            enn = 3
            enn_b = 2
        elif self.nd == 1:
            ne = self.work_mesh.NbEdges()
            ne_b = 2
            ne_e = 0
            ne_t = ne_b
            enn = 2
            enn_b = 1
        # mesh.nodes
        nn = self.work_mesh.NbNodes()
        coo = np.zeros((nn, 3), dtype=np.float)
        nid = self.work_mesh.GetElementsByType(SMESH.NODE)
        n = 0
        for id in nid:
            coo[n, :] = self.work_mesh.GetNodeXYZ(id)
            n = n + 1
        # meshName = self.work_mesh.GetName()
        meshName = 'mesh'
        if meshName in h5file.keys():
            h5file.__delitem__(meshName)
        h5file[meshName + '/nodes/nd'] = self.nd
        h5file[meshName + '/nodes/nn'] = nn
        h5file[meshName + '/nodes/id'] = nid
        h5file[meshName + '/nodes/coo'] = coo

        # mesh.domain
        eni = np.zeros((ne, enn), dtype=np.int64)
        eid = self.work_mesh.GetElementsByType(self.domain)

        e = 0
        for el in eid:
            eni[e, :] = self.work_mesh.GetElemNodes(el)
            e = e + 1

        h5file[meshName + '/domain/ne'] = ne
        h5file[meshName + '/domain/enn'] = enn
        h5file[meshName + '/domain/eni'] = eni
        h5file[meshName + '/domain/id'] = eid
        h5file[meshName + '/domain/type'] = self.nd

        # ===========================================
        # domain group infomation
        er = np.zeros((ne), dtype=np.int64)

        groupID = 1
        for grp in self.work_mesh.GetGroups(self.domain):
            for el in grp.GetIDs():
                e = el - ne_t - 1
                er[e] = groupID
            groupID = groupID + 1
        h5file[meshName + '/domain/er'] = er
        # ===========================================
        # mesh boundary (the boundary element contains inner boundary)
        eni_b = np.zeros((ne_b, enn_b), dtype=np.int64)
        eid_b = self.work_mesh.GetElementsByType(self.boundary)

        e = 0
        for el in eid_b:
            eni_b[e, :] = self.work_mesh.GetElemNodes(el)
            e = e + 1

        h5file[meshName + '/boundary/ne'] = ne_b
        h5file[meshName + '/boundary/enn'] = enn_b
        h5file[meshName + '/boundary/eni'] = eni_b
        h5file[meshName + '/boundary/id'] = eid_b
        h5file[meshName + '/boundary/type'] = self.nd - 1
        # ===========================================
        # boundary group infomation ( the inner boundary ID is 0)
        er_b = np.zeros((ne_b), dtype=np.int64)

        groupID = 1
        for grp in self.work_mesh.GetGroups(self.boundary):
            for el in grp.GetIDs():
                e = el - ne_e - 1
                er_b[e] = groupID
            groupID = groupID + 1
        h5file[meshName + '/boundary/er'] = er_b

        h5file.close()
        print('Done exporting ' + self.mesh_name)
