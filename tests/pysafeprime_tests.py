from nose.tools import *

import pysafeprime
from pysafeprime import is_prime
from pysafeprime import random_prime
from pysafeprime import safe_prime

# def setup():
#     pass
#
# def teardown():
#     pass

def test_stub():
    print is_prime(15, 0.01)
    print is_prime(23, 0.01)
    print random_prime(100, 0.01)
    print safe_prime(100, 0.01)
    pass
