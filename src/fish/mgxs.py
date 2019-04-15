import numpy as np
import h5py


class MGXS(object):
    """docstring for mgxs."""

    def __init__(self, transx_file):
        self.nm = 0
        self.ng = 0
        self.nl = 0
        self.nup = 0
        self.ned = 0
        self.matlist = list()
        self.matnames = list()
        self.exsnames = list()
        self.matnames1 = list()
        self.exsnames1 = list()
        self.read_transx(transx_file)

    def read_transx(self, filename):
        inp = open(filename, 'r')
        while True:
            linelist = inp.readline().split()
            if len(linelist) == 0:
                continue
            if linelist[0] == 'ngroup':
                self.ng = int(linelist[1])
            if linelist[0] == 'nl':
                self.nl = int(linelist[1])
            if linelist[0] == 'nup':
                self.nup = int(linelist[1])
            if linelist[0] == 'nmix':
                self.nm = int(linelist[1])
            if linelist[0] == 'ned':
                self.ned = int(linelist[1])
            if linelist[0] == 'mix'and linelist[1] == 'names':
                break

        # read material name
        inp.readline()
        for i in range(self.nm):
            linelist = inp.readline().split()
            matname = linelist[1]
            self.matnames.append(matname)

        # read exs names
        while True:
            linelist = inp.readline().split()
            if len(linelist) == 0:
                continue
            if linelist[0] == 'edit'and linelist[1] == 'names':
                # read extra xs name
                inp.readline()
                for i in range(self.ned):
                    linelist = inp.readline().split()
                    exsname = linelist[1]
                    self.exsnames.append(exsname)
            if linelist[0] == 'input':
                break

        inp.close()

        for i in range(self.nm):
            imat = Material(self.matnames[i], self.ng,
                            self.nl, self.nup, self.exsnames)
            imat.read_transx_xs(filename)
            self.matlist.append(imat)

    def export_h5(self, h5file=None):
        if h5file is None:
            h5file = h5py.File('xs.h5', 'w')
        for matstr in self.matnames:
            self.matnames1.append(matstr.encode('utf8').decode('utf8') + ' ')
        for exsstr in self.exsnames:
            self.exsnames1.append(exsstr.encode('utf8').decode('utf8') + ' ')
        h5file['/xs/nm'] = self.nm
        h5file['/xs/ng'] = self.ng
        h5file['/xs/nl'] = self.nl
        h5file['/xs/nu'] = self.nup
        h5file['/xs/ne'] = self.ned
        h5file['xs/matnames'] = np.string_(self.matnames1)
        h5file['xs/exsnames'] = np.string_(self.exsnames1)
        for mat in self.matlist:
            mat.export_h5(h5file)
        h5file.close()


class Material(object):
    """docstring for material."""

    def __init__(self, name, ng, nl, nup, exsnames):
        self.name = name
        self.ng = ng
        self.nl = nl
        self.nup = nup
        self.exsnames = exsnames
        self.ned = len(exsnames)

        self.xs_t = [0.0] * ng
        self.xs_a = [0.0] * ng
        self.xs_s = [0.0] * ng
        self.xs_p = [0.0] * ng
        self.xs_f = [0.0] * ng
        self.chi = [0.0] * ng

        self.xs_e = [[0.0] * self.ned for i in range(ng)]
        self.xs_s0 = [[0.0] * ng for i in range(ng)]
        self.xs_s1 = [[0.0] * ng for i in range(ng)]
        self.xs_s2 = [[0.0] * ng for i in range(ng)]
        self.xs_s3 = [[0.0] * ng for i in range(ng)]
        self.xs_s4 = [[0.0] * ng for i in range(ng)]
        self.xs_s5 = [[0.0] * ng for i in range(ng)]

        # >> temp data store transx xs_s, xs_e
        self.exs = [['0.000E+00'] * (ng) for i in range(self.ned)]
        self.p0 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p1 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p2 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p3 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p4 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p5 = [['0.000E+00'] * (ng) for i in range(ng + nup)]

    def read_transx_xs(self, filename):
        print(self.name + ' is reading cross-sections...')

        inp = open(filename, 'r')
        done = False
        if self.ng >= 9:
            lg = 9
        else:
            lg = self.ng

        while True:
            linelist = inp.readline().split()
            if len(linelist) < 1:
                continue
            if linelist[0] == '**' and linelist[1] == self.name:
                for il in range(self.nl):
                    head = 0
                    num = 0
                    tail = 0
                    basenum = 0
                    while True:
                        if done:
                            break
                        if tail == self.ng:
                            break
                        llist = inp.readline().split()
                        if len(llist) < 1:
                            continue
                        if llist[0] == 'position':
                            head = num * lg
                            tail = head + lg
                            line = inp.readline()
                            while True:
                                llist1 = inp.readline().split()
                                # End of file. '1'
                                if len(llist1) == 1 and llist1[0] == '1':
                                    done = True
                                    break
                                if len(llist1) == 0:
                                    break
                                # extra xs
                                if il == 0:
                                    if llist1[1] in self.exsnames:
                                        ii = self.exsnames.index(llist1[1])
                                        self.exs[ii][head:tail] = llist1[2:]
                                    if llist1[1] == 'abs':
                                        self.xs_a[head:tail] = map(
                                            float, llist1[2:])
                                        continue
                                    if llist1[1] == 'nusigf':
                                        self.xs_p[head:tail] = map(
                                            float, llist1[2:])
                                        continue
                                    if llist1[1] == 'total':
                                        self.xs_t[head:tail] = map(
                                            float, llist1[2:])
                                        basenum = int(llist1[0])
                                        continue
                                else:
                                    if llist1[1] == 'total':
                                        basenum = int(llist1[0])
                                        continue

                                group = int(llist1[0])
                                if group == basenum + self.nup + 1:
                                    tmp = llist1[2:]
                                else:
                                    tmp = llist1[1:]
                                # read scatter cross section matrix
                                # P0 ---> P5
                                # if last segment, i.e. tail>=ngroup, tail=ngroup
                                if (tail + 1) > self.ng:
                                    tail = self.ng
                                if il == 0:
                                    self.p0[group - basenum -
                                            1][head:tail] = tmp
                                elif il == 1:
                                    self.p1[group - basenum -
                                            1][head:tail] = tmp
                                elif il == 2:
                                    self.p2[group - basenum -
                                            1][head:tail] = tmp
                                elif il == 3:
                                    self.p3[group - basenum -
                                            1][head:tail] = tmp
                                elif il == 4:
                                    self.p4[group - basenum -
                                            1][head:tail] = tmp
                                elif il == 5:
                                    self.p5[group - basenum -
                                            1][head:tail] = tmp
                            num = num + 1

                # print(self.name + " reading cross-sections Done!")
                break

        inp.close()

        for i in range(self.ng):
            for j in range(self.ng):
                self.xs_s0[j][i] = float(self.p0[j + self.nup - i][j])
                self.xs_s1[j][i] = float(self.p1[j + self.nup - i][j])
                self.xs_s2[j][i] = float(self.p2[j + self.nup - i][j])
                self.xs_s3[j][i] = float(self.p3[j + self.nup - i][j])
                self.xs_s4[j][i] = float(self.p4[j + self.nup - i][j])
                self.xs_s5[j][i] = float(self.p5[j + self.nup - i][j])

        for i in range(self.ng):
            for j in range(self.ned):
                self.xs_e[i][j] = float(self.exs[j][i])

    #======================================================================
    def export_h5(self, h5file):
        # print (self.name + ' export cross-sections to the hdf5 file...')
        pref = '/xs/' + self.name
        h5file[pref + '/xs_t'] = self.xs_t
        if self.nl >= 1:
            h5file[pref + '/xs_s0'] = self.xs_s0
        if self.nl >= 2:
            h5file[pref + '/xs_s1'] = self.xs_s1
        if self.nl >= 3:
            h5file[pref + '/xs_s2'] = self.xs_s2
        if self.nl >= 4:
            h5file[pref + '/xs_s3'] = self.xs_s3
        if self.nl >= 5:
            h5file[pref + '/xs_s4'] = self.xs_s4
        if self.nl >= 6:
            h5file[pref + '/xs_s5'] = self.xs_s5
        if(self.ned >= 1):
            h5file[pref + '/xs_e'] = self.xs_e
