#! /usr/bin/env python

def count( sequence, item ):
    cnt = 0
    l = len(item)
    for i in sequence:
        if i == item:
            cnt += 1
    return cnt

print count( [1.23,2,4,[112,"ab","a"], "a", "aa"], "a")
