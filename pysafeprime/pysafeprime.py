import sys
import os
import math
import struct

def _random_in_range(low, high):
    num_bytes = (int(math.log(high, 2)) / 8) + 1
    n = int(os.urandom(num_bytes).encode('hex'), 16)
    while n < low or n > high:
        n = int(os.urandom(num_bytes).encode('hex'), 16)
    return n

def _random_bit_integer(bits):
    low = (2 ** bits) + 1
    high = (2 ** (bits + 1)) - 1
    return _random_in_range(low, high)

def is_prime(n, probability = 0.01):
    '''
    Miller-Rabin primality test algorithm 4.24 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''

    if n % 2 == 0:
        return False

    nn = n - 1
    s = 0
    while nn % 2 == 0:
        s += 1
        nn /= 2
    r = nn

    assert((2 ** s) * r == (n - 1))

    num_trials = int(math.log((1 / probability), 4))
    for i in range(num_trials):
        a = _random_in_range(2, n - 2)
        y = pow(a, r, n)
        if y != 1 and y != (n - 1):
            j = 1
            while j <= s - 1 and y != (n - 1):
                y = pow(y, y, n)
                if y == 1:
                    return False
                j = j + 1
            if y != (n - 1):
                return False

    return True

def random_prime(k, probability = 0.01):
    '''
    Random prime generation algorithm 4.44 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''
    
    num_trials = 1000

    trial = 0
    while trial < num_trials:
        n = _random_bit_integer(k)
        if is_prime(n, probability):
            return n
        trial += 1

    raise "Could not generate a random prime"

def random_prime_with_filter(k, condition, probability = 0.01):
    '''
    Return a random prime p that satisfies some condition, e.g., p = 3 mod 4
    '''

    num_trials = 1000

    trial = 0
    while trial < num_trials:
        p = random_prime(k, probability)
        if condition(p):
            return p
        trial += 1
    raise "Could not generate a random prime that meets the criteria"

def safe_prime(k, probability = 0.01):
    '''
    Safe prime generation algorithm 4.53 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    '''

    s = random_prime(k, probability)
    t = random_prime(k, probability)

    i = 1
    q = 0
    while q == 0:
        qt = (2 * i * t) + 1
        if is_prime(qt, probability):
            q = qt
        i += 1

    r = q

    p0 = (2 * (pow(s, r - 2, r)) * s) - 1

    j = 1
    q = 0
    while q == 0:
        qt = p0 + (2 * j * r * s)
        if is_prime(qt, probability):
            q = qt
        j += 1

    p = q

    return p

def fast_safe_prime(k, probability = 0.01):
    ''' 
    Quickly generate safe primes using the method of:
        https://eprint.iacr.org/2003/175.pdf
    This function will block until it finds a suitable prime.
    '''
    def prime_filter(p):
        return p % 4 == 3
    while True:
        p = random_prime_with_filter(k, prime_filter, probability)
        
        if is_prime((2 * p) + 1, probability) or is_prime((p - 1) / 2, probability):
            return p

# TODO: translate t parameter into probability
# test passes with probability at most (1/4^t) on a composite number

print is_prime(15, 0.01)
print is_prime(23, 0.01)
print random_prime(100, 0.01)
print safe_prime(100, 0.01)
print fast_safe_prime(100, 0.01)
