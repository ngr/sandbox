#! /usr/bin/env python

def median ( q ):
    l = sorted( q )
    print l
    if len( l ) % 2 > 0:
        print "middle index: " + str( len(l)/2 )
        res = l[len(l)/2]
    else:
        res = float( l[len(l)/2-1] + l[len(l)/2] ) / 2
    return res
print "test" + str( 5//2 )
print median([4, 5, 7, 5, 4]) 
print median([4, 5, 5, 4])
print median([4])
print median([1, 34, 1, 6, 8, 0])

