#! /usr/bin/env python

n = 123456
n1 = (n - n % 10) / 10
n2 = (n // 10) % 10
n3 = (n % 100 - n % 10) / 10

print n, n1, n2, n3


def f(x):
    return  -5 * x ** 5 + 69 * x ** 2 - 47

print f(0), f(1), f(2), f(3)

print 3 * ((2 - 9) + 4) * (2 + (1 - 3))


my_number = 1
my-number = 1
