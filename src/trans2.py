#======================================================================
# FUNCTION:
#   Read the transx ouput file and then transform
#   the cross section to the FISH input file(hdf5) and
#   multi-group MCNP cs file.
#======================================================================
# DEVELOP:
#   Name    : Tran2
#   Version : 0.1.0
#   Author  : c.fang, gczhang, zzheng jianxin.miao
#   email   : xiyanfc@gmail.com
#   qq      : 419881977
#   Date    : 2018/12/4
#======================================================================
# USAGE:
#   python path/Trans2 -a[-b][-c] -inp inpfile -oup oupfile
#   generate hdf5 file for fish directly
#   parameter: -a   write the detail xs information to the file
#              -b   write the basic xs information to the file
#                   including Extra xs sigma_t and sigma_s, and
#                   there are only data without commet
#                   this file is used for FISH!
#              -c   write the cs information fo multi-group MCNP
#              -inp if -a[-b] the inpfile only contains transx output
#                   if -c the first inpfile is transx ouput,the second
#                   file is energy boundary point, from max to min
#              -oup if -a[-b] the oupfile is mat information,including
#                   material name extra xs name ..., used for FISH
#                   if -c the oupfile is used for MCNP cards.
#======================================================================
# EXAMPLE:
#   python ./trans2.py -c
#   python ./trans2.py -a
#   python ./trans2.py
#======================================================================

import sys
import h5py
import numpy as np
import os

matlist = []
nm = 0
ng = 0
nps = 0
nup = 0
ned = 0
exslist = []


class material:

    #======================================================================
    def __init__(self, name):

        global nm, ng, nps, nup, ned, matlist, exslist

        self.name = name
        self.chi = [0] * ng
        self.nftot = [0] * ng
        self.abss = [0] * ng
        self.nusigf = [0] * ng
        self.tots = [0] * ng
        self.arr1 = np.array([], float)
        self.arr1 = [0] * ng
        self.scatt = [0] * ng

        self.exs = [['0.000E+00'] * (ng) for i in range(ned)]
        self.p0 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p1 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p2 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p3 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p4 = [['0.000E+00'] * (ng) for i in range(ng + nup)]
        self.p5 = [['0.000E+00'] * (ng) for i in range(ng + nup)]

        self.p0_c = [[0.0] * ng for i in range(ng)]
        self.p1_c = [[0.0] * ng for i in range(ng)]
        self.p2_c = [[0.0] * ng for i in range(ng)]
        self.p3_c = [[0.0] * ng for i in range(ng)]
        self.p4_c = [[0.0] * ng for i in range(ng)]
        self.p5_c = [[0.0] * ng for i in range(ng)]

        self.nxs = [0] * 16
        self.jxs = [0] * 32
        self.xss = []
        self.nusigft = 0

    #======================================================================
    def read_xs(self, fname):

        global nm, ng, nps, nup, ned, matlist, exslist

        print(self.name + ' is reading cross-sections...')

        inp = open(fname, 'r')
        done = False

        if ng >= 9:
            lg = 9
        else:
            lg = ng

        while True:
            linelist = inp.readline().split()
            if len(linelist) < 1:
                continue
            if linelist[0] == '**' and linelist[1] == self.name:
                for i in range(nps + 1):
                    head = 0
                    num = 0
                    tail = 0
                    while True:
                        if done:
                            break
                        if tail == ng:
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
                                if i == 0:
                                    if llist1[1] in exslist:
                                        ii = exslist.index(llist1[1])
                                        self.exs[ii][head:tail] = llist1[2:]
                                        if llist1[1] == 'chi':
                                            self.chi.extend(
                                                map(float, llist1[2:]))
                                        if llist1[1] == 'nftot':
                                            self.nftot.extend(
                                                map(float, llist1[2:]))
                                        continue
                                    if llist1[1] == 'abs':
                                        self.abss[head:tail] = map(
                                            float, llist1[2:])
                                        continue
                                    if llist1[1] == 'nusigf':
                                        self.nusigf[head:tail] = map(
                                            float, llist1[2:])
                                        continue
                                    if llist1[1] == 'total':
                                        self.tots[head:tail] = map(
                                            float, llist1[2:])
                                        self.arr1[head:tail] = self.tots[head:tail]
                                        basenum = int(llist1[0])
                                        continue
                                else:
                                    if llist1[1] == 'total':
                                        basenum = int(llist1[0])
                                        continue
                                # print 'basenum','%s'%(basenum)
                                group = int(llist1[0])
                                if group == basenum + nup + 1:
                                    tmp = llist1[2:]
                                else:
                                    tmp = llist1[1:]
                                # read scatter cross section matrix
                                # P0 ---> P5
                                # if last segment, i.e. tail>=ngroup, tail=ngroup
                                if (tail + 1) > ng:
                                    tail = ng
                                if i == 0:
                                    self.p0[group - basenum -
                                            1][head:tail] = tmp
                                elif i == 1:
                                    self.p1[group - basenum -
                                            1][head:tail] = tmp
                                elif i == 2:
                                    self.p2[group - basenum -
                                            1][head:tail] = tmp
                                elif i == 3:
                                    self.p3[group - basenum -
                                            1][head:tail] = tmp
                                elif i == 4:
                                    self.p4[group - basenum -
                                            1][head:tail] = tmp
                                elif i == 5:
                                    self.p5[group - basenum -
                                            1][head:tail] = tmp
                            num = num + 1

                for ig in range(0, ng):
                    self.nusigft = self.nusigft + self.nusigf[ig]
                inp.close()
                if(self.nusigft != 0):
                    self.nutot = [0] * ng
                    for ig in range(0, ng):
                        if self.nftot[ig] != 0:
                            self.nutot[ig] = self.nusigf[ig] / self.nftot[ig]
                # print 'Reading cross-sections Done!'
                break

    #======================================================================
    def converse(self):
        # rearrange the scatter matrix to normal, i.e. i-->j;
        # There may be some wasting of memories, for perhaps not all the 5
        # moments are read from the library.

        print(self.name + ' is conversing the matrix...')

        global ng, nup

        for i in range(ng):
            for j in range(ng):
                self.p0_c[j][i] = float(self.p0[j + nup - i][j])
                self.p1_c[j][i] = float(self.p1[j + nup - i][j])
                self.p2_c[j][i] = float(self.p2[j + nup - i][j])
                self.p3_c[j][i] = float(self.p3[j + nup - i][j])
                self.p4_c[j][i] = float(self.p4[j + nup - i][j])
                self.p5_c[j][i] = float(self.p5[j + nup - i][j])
        for i in range(ng):
            self.scatt[i] = sum(self.p0_c[i][:])

        print('Converting Done!')

    #======================================================================
    def write_xs(self, fname):
        # output the cross sections to  the output file.
        print (self.name + ' is output the detail cross-sections to the file...')

        global nm, ng, nps, nup, ned, matlist, exslist

        oup = open(fname, 'w')
        oup.write('  position  ')
        #-----write group i------
        for i in range(1, ng + 1):
            gstr = 'group' + str(i)
            oup.write('   %s' % (gstr.center(9)))
        #-----write extra edit cross-sections------
        for i in range(ned):
            oup.write('%s%s' % ('\n', exslist[i].center(12)))
            #         for j in range(self.ngroup):
            #            outf.write('  %10.3E'%(self.extEdi[i][j]))
            for value in self.exs[i][:]:
                oup.write('  %s' % (value.rjust(10)))

        #----write absorption cross section------
        namstr = 'abs'
        oup.write('%s%s' % ('\n', namstr.center(12)))
        for i in range(ng):
            oup.write('  %10.3E' % (self.abss[i]))
        #-----write neutron production cross section------
        if(self.nusigft != 0):
            namstr = 'nusigf'
            oup.write('%s%s' % ('\n', namstr.center(12)))
            for i in range(ng):
                oup.write('  %10.3E' % (self.nusigf[i]))
        #----write total cross section-----
        namstr = 'total'
        oup.write('%s%s' % ('\n', namstr.center(12)))
        for i in range(ng):
            oup.write('  %10.3E' % (self.tots[i]))
        #----write scattering ratio-----
        namstr = 'scat ratio'
        oup.write('%s%s' % ('\n', namstr.center(12)))
        for i in range(ng):
            oup.write('  %10.3E' % (self.scatt[i] / self.tots[i]))
        #----write scatT cross: total scatt of one group--
        namstr = 'scatT'
        oup.write('%s%s' % ('\n', namstr.center(12)))
        for value in self.scatt:
            oup.write('  %10.3E' % (value))

        #----PN scatter cross sections matrix---
        pl = 0
        namstr = 'scattP0'
        tmp = self.p0_c
        while True:
            for i in range(ng):
                if i == 0:
                    oup.write('%s%s' % ('\n', namstr.center(12)))
                else:
                    oup.write('%s' % (str(i + 1).center(12)))
                for value in tmp[i][:]:
                    #   fvalue = float(value)
                    #   print value
                    #   oup.write('  %s'%(value.rjust(10)))
                    oup.write('  %10.3E' % (value))
                oup.write('\n')

            pl = pl + 1
            if pl <= (nps):
                if pl == 1:
                    namstr = 'scattP1'
                    tmp = self.p1_c
                    #----write scatT cross: total scatt of one group--
                    for i in range(ng):
                        self.scatt.append(sum(self.p1_c[i][:]))
                    namstr1 = 'scatT'
                    oup.write('%s%s' % ('\n', namstr1.center(12)))
                    for i in range(ng, 2 * ng):
                        oup.write('  %10.3E' % (self.scatt[i]))
                    continue
                if pl == 2:
                    namstr = 'scattP2'
                    tmp = self.p2_c
                    #----write scatT cross: total scatt of one group--
                    for i in range(ng):
                        self.scatt.append(sum(self.p2_c[i][:]))
                    namstr1 = 'scatT'
                    oup.write('%s%s' % ('\n', namstr1.center(12)))
                    for i in range(2 * ng, 3 * ng):
                        oup.write('  %10.3E' % (self.scatt[i]))
                    continue
                if pl == 3:
                    namstr = 'scattP3'
                    tmp = self.p3_c
                    #----write scatT cross: total scatt of one group--
                    for i in range(ng):
                        self.scatt.append(sum(self.p3_c[i][:]))
                    namstr1 = 'scatT'
                    oup.write('%s%s' % ('\n', namstr1.center(12)))
                    for i in range(3 * ng, 4 * ng):
                        oup.write('  %10.3E' % (self.scatt[i]))
                    continue
                if pl == 4:
                    namstr = 'scattP4'
                    tmp = self.p4_c
                    #----write scatT cross: total scatt of one group--
                    for i in range(ng):
                        self.scatt.append(sum(self.p4_c[i][:]))
                    namstr1 = 'scatT'
                    oup.write('%s%s' % ('\n', namstr1.center(12)))
                    for i in range(4 * ng, 5 * ng):
                        oup.write('  %10.3E' % (self.scatt[i]))
                    continue
                if pl == 5:
                    namstr = 'scattP5'
                    tmp = self.p5_c
                    #----write scatT cross: total scatt of one group--
                    for i in range(ng):
                        self.scatt.append(sum(self.p5_c[i][:]))
                    namstr1 = 'scatT'
                    oup.write('%s%s' % ('\n', namstr1.center(12)))
                    for i in range(5 * ng, 6 * ng):
                        oup.write('  %10.3E' % (self.scatt[i]))
                    continue
            else:
                oup.close()
                break
        print('Done!')

    #======================================================================
    def write_xs_simple(self, fname):
        # output the cross sections to  the output file.
        print (self.name + ' is output the simple cross-sections to the file...')

        global nm, ng, nps, nup, ned, matlist, exslist

        oup = open(fname, 'w')
        #-----write extra edit cross-sections------
        for i in range(ned):
            for value in self.exs[i][:]:
                oup.write('  %s' % (value.rjust(10)))
            oup.write('\n')

        #----write total cross section-----
        for i in range(ng):
            oup.write('  %10.3E' % (self.tots[i]))
        oup.write('\n')

        #----PN scatter cross sections matrix---
        pl = 0
        while True:
            for i in range(ng):
                for value in self.p0_c[i][:]:
                    oup.write('  %10.3E' % (value))
                oup.write('\n')

            pl = pl + 1
            if pl <= (nps):
                if pl == 1:
                    for i in range(ng):
                        for value in self.p1_c[i][:]:
                            oup.write('  %10.3E' % (value))
                        oup.write('\n')

                if pl == 2:
                    for i in range(ng):
                        for value in self.p2_c[i][:]:
                            oup.write('  %10.3E' % (value))
                        oup.write('\n')

                if pl == 3:
                    for i in range(ng):
                        for value in self.p3_c[i][:]:
                            oup.write('  %10.3E' % (value))
                        oup.write('\n')

                if pl == 4:
                    for i in range(ng):
                        for value in self.p4_c[i][:]:
                            oup.write('  %10.3E' % (value))
                        oup.write('\n')

                if pl == 5:
                    for i in range(ng):
                        for value in self.p5_c[i][:]:
                            oup.write('  %10.3E' % (value))
                        oup.write('\n')
            else:
                oup.close()
                break
        print('Done!')

    #=========================================================
    # Initialize the MCNP arguments and the cross-sections
    #=========================================================
    def mcnp_init(self, fname):
        # 1: Only P0 scatter Matrix...
        # 2: Fission material cross-section can be converted.

        global ng
        energy = []

        if (self.nusigft == 0):  # no fission

            self.nxs[0] = ng * ng + 4 * ng + 1
            self.nxs[1] = 99999
            self.nxs[4] = ng     # Number of groups
            self.nxs[5] = ng - 1  # Number of upscatter groups
            self.nxs[6] = ng - 1  # Number of downscatter groups
            self.nxs[11] = 1     # neutrons; NO photons.
            self.jxs[0] = 1
            self.jxs[1] = 2 * ng + 1
            self.jxs[5] = 3 * ng + 1
            self.jxs[12] = 4 * ng + 1

            inp = open(fname, 'r')
            for line in inp:
                energy.extend(map(float, line.split()))
            inp.close()

            if len(energy) < (ng + 1):
                sys.exit('ERROR: The number of the bounderies are less than\
                equal to %d !\n       The execution is TERMINATED!\n       Please \
                check the group-boundary file.' % (ng + 1))
            for i in range(ng):
                self.xss.append((energy[i] + energy[i + 1]) / 2.0)

            for i in range(ng, 2 * ng):
                self.xss.append(energy[i - ng] - energy[i - ng + 1])

            for i in range(2 * ng, 3 * ng):
                self.xss.append(self.tots[i - 2 * ng])

            for i in range(3 * ng, 4 * ng):
                if(len(self.abss) == 0):
                    self.xss.append(0.0)
                else:
                    self.xss.append(self.abss[i - 3 * ng])

            self.xss.append(4 * ng + 2)

            for i in range(ng):
                self.xss.extend(self.p0_c[i][:])

        else:  # with fission

            self.nxs[0] = ng * ng + 7 * ng + 1
            self.nxs[1] = 99999
            self.nxs[4] = ng     # Number of groups
            self.nxs[5] = ng - 1  # Number of upscatter groups
            self.nxs[6] = ng - 1  # Number of downscatter groups
            self.nxs[9] = 1      # Number of nubars given
            self.nxs[11] = 1     # neutrons; NO photons.
            self.jxs[0] = 1
            self.jxs[1] = 2 * ng + 1
            self.jxs[2] = 3 * ng + 1  # Location of fission cross sections
            self.jxs[3] = 4 * ng + 1  # Location of nubar data
            self.jxs[4] = 5 * ng + 1  # Location of fission chi data
            self.jxs[5] = 6 * ng + 1  # Location of absorption cross sections
            self.jxs[12] = 7 * ng + 1  # Location of P0 locators

            inp = open(fname, 'r')
            for line in inp:
                energy.extend(map(float, line.split()))
            inp.close()

            if len(energy) < (ng + 1):
                sys.exit('ERROR: The number of the bounderies are less than\
                equal to %d !\n       The execution is TERMINATED!\n       Please \
                check the group-boundary file.' % (ng + 1))
            for i in range(ng):
                self.xss.append((energy[i] + energy[i + 1]) / 2.0)

            for i in range(ng, 2 * ng):
                self.xss.append(energy[i - ng] - energy[i - ng + 1])

            for i in range(2 * ng, 3 * ng):
                self.xss.append(self.tots[i - 2 * ng])

            for i in range(3 * ng, 4 * ng):
                self.xss.append(self.nftot[i - 3 * ng])

            for i in range(4 * ng, 5 * ng):
                self.xss.append(self.nutot[i - 4 * ng])

            for i in range(5 * ng, 6 * ng):
                self.xss.append(self.chi[i - 5 * ng])

            for i in range(6 * ng, 7 * ng):
                self.xss.append(self.abss[i - 6 * ng])

            self.xss.append(7 * ng + 2)

            for i in range(ng):
                self.xss.extend(self.p0_c[i][:])

    #======================================================================
    def write_mcnp(self, fname, k):
        # output the MCNP type cross-sections
        oup = open(fname, 'w')
        if k <= 9:
            tmpstr = ' 99999.0' + str(k) + 'm' + '   999    0.00000E+00  '
        else:
            tmpstr = ' 99999.' + str(k) + 'm' + '   999    0.00000E+00  '
        oup.write('%s%s' % (tmpstr, '\n'))
        oup.write('%s%s' % (self.name, '\n'))
        tmpstr = \
            '      0   0.000000      0   0.000000      0   0.000000      0   0.000000\n\
        0   0.000000      0   0.000000      0   0.000000      0   0.000000\n\
        0   0.000000      0   0.000000      0   0.000000      0   0.000000\n\
        0   0.000000      0   0.000000      0   0.000000      0   0.000000'
        oup.write('%s%s' % (tmpstr, '\n'))
        for i in range(0, len(self.nxs), 8):
            for j in range(i, i + 8):
                oup.write('%9d' % (self.nxs[j]))
            oup.write('\n')

        for i in range(0, len(self.jxs), 8):
            for j in range(i, i + 8):
                oup.write('%9d' % (self.jxs[j]))
            oup.write('\n')

        for i in range(0, len(self.xss), 4):
            head = i
            if (i + 3) >= (len(self.xss) - 1):
                tail = len(self.xss)
            else:
                tail = i + 4
            for j in range(head, tail):
                oup.write('%20.12E' % (self.xss[j]))
            oup.write('\n')

    #======================================================================
    def write_matcrd(self, k, kmix, fname):
        # output material cards
        global ng

        if k == 1:
            oup = open(fname, 'wt')
            oup.close()

        oup = open(fname, 'a')

        tmpstr = 'm' + str(k)
        if k == 1:
            oup.write('%s' % (tmpstr))
        else:
            oup.write('%s%s' % ('\n', tmpstr))
        if k <= 9:
            tmpstr = '     99999.0' + str(k) + 'm' + ' 1.0'
        else:
            tmpstr = '    99999.' + str(k) + 'm' + ' 1.0'
        oup.write('%s%s' % (tmpstr, '\n'))
        tmpstr = 'xs' + str(k)
        oup.write(tmpstr)
        if k <= 9:
            tmpstr = '    99999.0' + str(k) + 'm' + ' 1.0'
        else:
            tmpstr = '   99999.' + str(k) + 'm' + ' 1.0'
        oup.write(tmpstr)
        tmpstr = ' cs' + str(k)
        oup.write(tmpstr)
        tmpstr = ' 0 1 1 '
        oup.write(tmpstr)
        tmpstr = self.nxs[0]
        oup.write('%s' % (tmpstr))
        if k == kmix:
            tmpstr = 'mgopt f '
            oup.write('%s%s' % ('\n', tmpstr))
            tmpstr = str(ng)
            oup.write(tmpstr)

    #======================================================================
    def write_hdf5(self, fname):
        print (self.name + ' is output the detail cross-sections to the hdf5 file...')
        global nm, ng, nps, nup, ned, exslist, hdf5file
        temp = [0] * ng

        hdf5file['/xs/' + self.name + '/xs_t'] = self.arr1

        hdf5file['/xs/' + self.name + '/xs_s0'] = self.p0_c
        pl = 0
        while True:
            pl = pl + 1
            if pl <= (nps):
                if pl == 1:
                    hdf5file['/xs/' + self.name + '/xs_s1'] = self.p1_c
                    continue
                if pl == 2:
                    hdf5file['/xs/' + self.name + '/xs_s2'] = self.p2_c
                    continue
                if pl == 3:
                    hdf5file['/xs/' + self.name + '/xs_s3'] = self.p3_c
                    continue
                if pl == 4:
                    hdf5file['/xs/' + self.name + '/xs_s4'] = self.p4_c
                    continue
                if pl == 5:
                    hdf5file['/xs/' + self.name + '/xs_s5'] = self.p5_c
                    continue
            else:
                break

        for j in range(ned):
            for k in range(ng):
                temp[k] = float(self.exs[j][k])
            hdf5file['/xs/' + self.name + '/' + exslist[j]] = temp

#======================================================================


def init_matlist(fname):

    global nm, ng, nps, nup, ned, matlist, exslist

    inp = open(fname, 'r')

    while True:
        linelist = inp.readline().split()
        if len(linelist) == 0:
            continue
        if linelist[0] == 'ngroup':
            ng = int(linelist[1])
        if linelist[0] == 'nl':
            nps = int(linelist[1]) - 1
        if linelist[0] == 'nup':
            nup = int(linelist[1])
        if linelist[0] == 'nmix':
            nm = int(linelist[1])
        if linelist[0] == 'ned':
            ned = int(linelist[1])
        if linelist[0] == 'mix'and linelist[1] == 'names':
            break

# read material name
    inp.readline()
    for i in range(nm):
        linelist = inp.readline().split()
        matlist.append(material(linelist[1]))

    while True:
        linelist = inp.readline().split()
        if len(linelist) == 0:
            continue
        if linelist[0] == 'edit'and linelist[1] == 'names':

            # read extra xs name
            inp.readline()
            for i in range(ned):
                linelist = inp.readline().split()
                exslist.append(linelist[1])
        if linelist[0] == 'input':
            break

    inp.close()

#======================================================================


def write_matinfo(fname):

    global nm, ng, nps, nup, ned, matlist, exslist

    oup = open(fname, 'w')
    oup.write('%s   %s   %s   %s   %s%s' %
              ('! nm', 'ng', 'nps', 'nup', 'ned', '\n'))
    oup.write('%i     %i      %i     %i     %i' % (nm, ng, nps, nup, ned))

    oup.write('\n' + '! material names')
    for mat in matlist:
        oup.write('\n' + mat.name)
    oup.write('\n' + '! extra xs names')
    for exs in exslist:
        oup.write('\n' + exs)


#======================================================================

# main program
def export_mat():
    global hdf5file
    trx_file = './transx.out'
    mat_file = './matinfo.dat'
    erg_file = './inp/ergbdy.inp'
    mcg_file = './cxs/mcard.dat'

    xs_path = './bxs/'
    axs_path = './axs/'
    cs_path = './cxs/'
    hdf5_path = './hdf5/'

    if os.path.exists('./transx.out'):
        # init_matlist(trx_file)
        write_matinfo(mat_file)
        fname = 'fish.h5'
        hdf5file = h5py.File(fname, 'r+')
        hdf5file['/xs/nm'] = nm
        hdf5file['/xs/ng'] = ng
        hdf5file['/xs/nl'] = nps + 1
        hdf5file['/xs/nu'] = nup
        hdf5file['/xs/ne'] = ned
        for exs in exslist:
            hdf5file['/xs/' + exs] = 0
        for mat in matlist:
            mat.read_xs(trx_file)
            mat.converse()
            mat.write_hdf5(fname)
        hdf5file.close()
    else:
        hdf5file = h5py.File('fish.h5', 'r+')
        hdf5file['/xs/nm'] = 1
        hdf5file['/xs/ng'] = 1
        hdf5file['/xs/nu'] = 0
        hdf5file['/xs/nl'] = 1
        hdf5file['/xs/ne'] = 0
        hdf5file['/xs/m1/xs_s0'] = 0.19
        hdf5file['/xs/m1/xs_t'] = 0.2
        hdf5file.close()
        """
        i=1
        for mat in matlist:
            mat.read_xs(trx_file)
            mat.converse()

            xsfile =xs_path + mat.name + '.xs'
            mat.write_xs_simple(xsfile)

        if '-a' in sys.argv:
            xsfile =axs_path + mat.name + '.xs'
            mat.write_xs(xsfile)

        if '-c' in sys.argv:
            csfile = cs_path + 'cs' + str(i)
            mat.mcnp_init(erg_file)
            mat.write_mcnp(csfile,i)
            mat.write_matcrd(i,nm,mcg_file)
        i = i + 1
        """
