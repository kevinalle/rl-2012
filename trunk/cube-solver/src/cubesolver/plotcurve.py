#!/usr/bin/env python
import sys
if len(sys.argv) > 1:
    import matplotlib.pyplot
    from pylab import show
    f = open(sys.argv[1]).read().strip().split("\n")
    fs = [int(e.split()[2]) for e in f]
    if len(sys.argv) > 2:
        fs = fs[:int(sys.argv[2])]
    show(matplotlib.pyplot.plot(fs))
else:
    print "Need input file."

