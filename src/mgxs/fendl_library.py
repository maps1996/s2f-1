
import os
from distutils import spawn
import numpy as np

# global Parameters
default_fendl_path = './fendl'
default_matxs_path = './matxs'
default_fendl_url  = 'https://www-nds.iaea.org/fendl/data/neutron/fendl31b-neutron-matxs.zip'

fendl_neutron_group_structure = np.array(
[5.50000E+07,5.40000E+07,5.30000E+07,5.20000E+07,5.10000E+07
,5.00000E+07,4.90000E+07,4.80000E+07,4.70000E+07,4.60000E+07,4.50000E+07
,4.40000E+07,4.30000E+07,4.20000E+07,4.10000E+07,4.00000E+07,3.90000E+07
,3.80000E+07,3.70000E+07,3.60000E+07,3.50000E+07,3.40000E+07,3.30000E+07
,3.20000E+07,3.10000E+07,3.00000E+07,2.90000E+07,2.80000E+07,2.70000E+07
,2.60000E+07,2.50000E+07,2.40000E+07,2.30000E+07,2.20000E+07,2.10000E+07
,2.00000E+07,1.96403E+07,1.73325E+07,1.69046E+07,1.64872E+07,1.56831E+07
,1.49182E+07,1.45499E+07,1.41907E+07,1.38403E+07,1.34986E+07,1.28403E+07
,1.25232E+07,1.22140E+07,1.16183E+07,1.10517E+07,1.05127E+07,1.00000E+07
,9.51229E+06,9.04837E+06,8.60708E+06,8.18731E+06,7.78801E+06,7.40818E+06
,7.04688E+06,6.70320E+06,6.59241E+06,6.37628E+06,6.06531E+06,5.76950E+06
,5.48812E+06,5.22046E+06,4.96585E+06,4.72367E+06,4.49329E+06,4.06570E+06
,3.67879E+06,3.32871E+06,3.16637E+06,3.01194E+06,2.86505E+06,2.72532E+06
,2.59240E+06,2.46597E+06,2.38513E+06,2.36533E+06,2.34570E+06,2.30693E+06
,2.23130E+06,2.12248E+06,2.01897E+06,1.92050E+06,1.82684E+06,1.73774E+06
,1.65299E+06,1.57237E+06,1.49569E+06,1.42274E+06,1.35335E+06,1.28735E+06
,1.22456E+06,1.16484E+06,1.10803E+06,1.00259E+06,9.61672E+05,9.07180E+05
,8.62936E+05,8.20850E+05,7.80817E+05,7.42736E+05,7.06512E+05,6.72055E+05
,6.39279E+05,6.08101E+05,5.78443E+05,5.50232E+05,5.23397E+05,4.97871E+05
,4.50492E+05,4.07622E+05,3.87742E+05,3.68832E+05,3.33733E+05,3.01974E+05
,2.98491E+05,2.97211E+05,2.94518E+05,2.87246E+05,2.73237E+05,2.47235E+05
,2.35177E+05,2.23708E+05,2.12797E+05,2.02419E+05,1.92547E+05,1.83156E+05
,1.74224E+05,1.65727E+05,1.57644E+05,1.49956E+05,1.42642E+05,1.35686E+05
,1.29068E+05,1.22773E+05,1.16786E+05,1.11090E+05,9.80365E+04,8.65170E+04
,8.25034E+04,7.94987E+04,7.20245E+04,6.73795E+04,5.65622E+04,5.24752E+04
,4.63092E+04,4.08677E+04,3.43067E+04,3.18278E+04,2.85011E+04,2.70001E+04
,2.60584E+04,2.47875E+04,2.41755E+04,2.35786E+04,2.18749E+04,1.93045E+04
,1.50344E+04,1.17088E+04,1.05946E+04,9.11882E+03,7.10174E+03,5.53084E+03
,4.30742E+03,3.70744E+03,3.35463E+03,3.03539E+03,2.74654E+03,2.61259E+03
,2.48517E+03,2.24867E+03,2.03468E+03,1.58461E+03,1.23410E+03,9.61117E+02
,7.48518E+02,5.82947E+02,4.53999E+02,3.53575E+02,2.75364E+02,2.14454E+02
,1.67017E+02,1.30073E+02,1.01301E+02,7.88932E+01,6.14421E+01,4.78512E+01
,3.72665E+01,2.90232E+01,2.26033E+01,1.76035E+01,1.37096E+01,1.06770E+01
,8.31529E+00,6.47595E+00,5.04348E+00,3.92786E+00,3.05902E+00,2.38237E+00
,1.85539E+00,1.44000E+00,1.12300E+00,8.76425E-01,6.82560E-01,5.31579E-01
,4.13994E-01,1.00001E-01,1.00001E-05])

fendl_gamma_group_structure = np.array(
[5.00000E+07,3.00000E+07,2.00000E+07,1.40000E+07,1.20000E+07
,1.00000E+07,8.00000E+06,7.50000E+06,7.00000E+06,6.50000E+06,6.00000E+06
,5.50000E+06,5.00000E+06,4.50000E+06,4.00000E+06,3.50000E+06,3.00000E+06
,2.50000E+06,2.00000E+06,1.66000E+06,1.50000E+06,1.34000E+06,1.33000E+06
,1.00000E+06,8.00000E+05,7.00000E+05,6.00000E+05,5.12000E+05,5.10000E+05
,4.50000E+05,4.00000E+05,3.00000E+05,2.00000E+05,1.50000E+05,1.00000E+05
,7.50000E+04,7.00000E+04,6.00000E+04,4.50000E+04,3.00000E+04,2.00000E+04
,1.00000E+04,1.00000E+03])


class fendl_library(object):
    """fendl library."""
    def __init__(self, fendl_path = None, matxs_path = None):
        self._fendl_path = default_fendl_path
        self._matxs_path = default_matxs_path
        self._nuclide_list = []
        if fendl_path is not None:
            self._fendl_path = fendl_path
        if matxs_path is not None:
            self._matxs_path = matxs_path
        #get nuclide_list from matxs_path
        self._nuclide_list = sorted(os.listdir(self._matxs_path))

    def download(self):
        """
        download Fendl 3.1b
        """
        print('Downloading Fendl 3.1b data to '+self._fendl_path)
        os.system("wget "+default_fendl_url)
        print('Extracting Data')
        os.system("unzip fendl31b-neutron-matxs.zip -d {}".format(self.fendl_path))
        os.system("rm fendl31b-neutron-matxs.zip")

    def make_matxs(self):
        """
        make matxs by bbc
        """
        bbcinput = open("bbcinput",'w')
        bbcinput.write('-1 1 0 0 1')
        bbcinput.close()
        xsfiles = sorted(os.listdir(self._fendl_path))
        for filename in xsfiles:
            # move the text file to current directory and call it text
            path = '{}/{}'.format(self._fendl_path, filename)
            os.system("cp {} text".format(path))
            # get name of nuclide to call new matxs file
            f = open("text", 'r')
            line = f.readline()
            name = line.split('*')[1][9:].strip()
            f.close()
            # run bbc to get matx file
            if spawn.find_executable('bbc') == None:
                print("No bbc executable found.")
            os.system("bbc")
            # move matx file to new name
            os.system("mv matxs {}/{}".format(self._matxs_path,name))
            # remove extra files created
            os.system("rm index text")

    def neutron_group(self):
        "neutron group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[0])
        f.close()
        return ng

    def gamma_group(self):
        "gamma group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[1])
        f.close()
        return ng

    def group_number(self):
        "energy group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[1]) + int(line.split()[0])
        f.close()
        return ng

    def nuclide_number(self):
        nn = len(self._nuclide_list)
        return nn

    def neutron_group_structure(self):
        "neutron energy group structure"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        lines = ''
        for i in range(9, 44):
            line = f.readline()
            lines = lines + line
        ngs = map(eval,lines.split()[1:])
        f.close()
        return ngs

    def gamma_group_structure(self):
        "gama energy group structure"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 44):
            line = f.readline()
        lines = ''
        for i in range(45, 52):
            line = f.readline()
            lines = lines + line
        ggs = map(eval,lines.split()[1:])
        f.close()
        return ggs

    def print_information(self):
        "print fendl "
        print('nuclide number:',self.nuclide_number())
        print("neutron group number",self.neutron_group())
        print("neutron group structure",self.neutron_group_structure())
        print("gamma group number",self.gamma_group())
        print("gamma group structure",self.gamma_group_structure())
        print("group number",self.group_number())
        print('nuclides:',self._nuclide_list)
