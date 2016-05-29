from nose.tools import *

import math

import pysafeprime
from pysafeprime import is_prime
from pysafeprime import random_prime
from pysafeprime import safe_prime

def test_is_prime_small():
    assert is_prime(15) == False
    assert is_prime(23) == True
    assert is_prime(2) == False

def test_is_prime_large():
    pass

def test_random_prime():
    def bit_length(n):
        return int(math.log(n, 2)) + 1
        
    for i in range(1024, 4096, 1024):
        p = random_prime(i)
        print p, i, bit_length(p)
        assert bit_length(p) == i

def test_safe_prime():
    for i in range(1024, 4096, 1024):
        p = safe_prime(i)
        assert is_prime(p)
        assert is_prime((p - 1) / 2)
