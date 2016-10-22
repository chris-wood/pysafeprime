from nose.tools import *

import math

import pysafeprime
from pysafeprime import is_prime
from pysafeprime import random_prime
from pysafeprime import safe_prime

def bit_length(n):
    return int(math.log(n, 2)) + 1

def test_is_prime_small():
    assert is_prime(15) == False
    assert is_prime(23) == True
    assert is_prime(2) == True

def test_random_prime_512():
    p = random_prime(512)
    assert bit_length(p) == 512

#def test_random_prime_1024():
#    p = random_prime(1024)
#    assert bit_length(p) == 1024

#def test_random_prime_2048():
#    p = random_prime(2048)
#    assert bit_length(p) == 2048

#def test_random_prime_4096():
#    p = random_prime(4096)
#    assert bit_length(p) == 4096

def check_safe_prime(p):
    assert is_prime(p)
    assert is_prime((p - 1) / 2)

def test_safe_prime_512():
    p = safe_prime(512)
    check_safe_prime(p)

#def test_safe_prime_1024():
#    p = safe_prime(1024)
#    check_safe_prime(p)

#def test_safe_prime_2048():
#    p = safe_prime(2048)
#    check_safe_prime(p)

#def test_safe_prime_4096():
#    p = safe_prime(4096)
#    check_safe_prime(p)
