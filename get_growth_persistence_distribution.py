#!/usr/bin/env python3
#
# Analysis the distribution of growth persistence values by calculating
# statistics such as the weighted average and the average for each time
# step. Information is written to STDOUT and stored in gnuplot format.

from itertools import chain

import numpy
import sys

files  = sys.argv[1:]
header = ["file",\
    "average",
    "weighted_average",
    "q25",
    "created_mass",
    "created_mass_normalized",
]

print(" ".join(header))

for filename in files:
    values = dict()
    n      = 0
    with open(filename) as f:
        for line in f:
            line    = line.strip()
            _, _, p = line.split()
            p       = int(p) # growth persistence is an integer

            values[p] = values.get(p,0) + 1
            n         = n+1

    array                   = [ x for x in values ]
    weights                 = [ values[x] / n for x in values ] 
    average                 = numpy.average(array)
    weighted_average        = numpy.average(array, weights=weights)
    q25                     = numpy.percentile( list( chain.from_iterable( [ [x]*values[x] for x in values ] ) ), 25.0 )

    created_mass            = values.get(0,0) + values.get(1,0)
    created_mass_normalized = created_mass / n

    print("'%s' %f %f %f %d %f" % (filename,              \
                                   average,               \
                                   weighted_average,      \
                                   q25,                   \
                                   created_mass,          \
                                   created_mass_normalized))
