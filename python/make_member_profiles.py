import numpy as np
import collections
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## Command line arguments
parser = argparse.ArgumentParser(
    description='Find archived data in the LSST  data Catalog. These include CCD test stand and vendor data files.')

##   The following are 'convenience options' which could also be specified in the filter string
parser.add_argument('-f', '--dataFile', default="", help="name of data file (default=%(default)s)")
args = parser.parse_args()

dateData = collections.OrderedDict()

with open(args.dataFile) as f:
    for line in f:
        (year, id, kind, mdy, timestamp, active) = line.split()
        dateDataList = dateData.setdefault(year, [])

        if 'full' not in kind:
            continue
        values = dateData.values()
        if  not (id in [x for v in values for x in v if type(v) == list] or id in values):
            dateDataList.append(id)

integral = collections.OrderedDict()
roll = 0

for yr in dateData:
    num_in_year = len(dateData[yr])
    print yr, num_in_year
    integral[yr] = roll + num_in_year
    roll += num_in_year

print integral

with PdfPages('out.pdf') as pdf:

    fig1=plt.figure(1)
    plt.bar(range(len(integral)), integral.values(), align='center')
    plt.xticks(range(len(integral)), integral.keys())
    plt.xlabel('year')
    plt.suptitle(' DESC Membership Integral by Year' )
    pdf.savefig()
    plt.close()
