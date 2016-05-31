from nose.tools import *

import math

import pysafeprime
from pysafeprime import is_prime
from pysafeprime import random_prime
from pysafeprime import safe_prime

def test_is_prime_small():
    assert is_prime(15) == False
    assert is_prime(23) == True
    assert is_prime(2) == True

def test_is_prime_large():
    pass

def test_random_prime():
    def bit_length(n):
        return int(math.log(n, 2)) + 1
        
    p = random_prime(1024)
    assert bit_length(p) == 1024

def test_safe_prime():
    p = safe_prime(1024)
    assert is_prime(p)
    assert is_prime((p - 1) / 2)
