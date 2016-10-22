import sys
import os
import math
import struct

def _random_in_range(low, high):
    """Generate a random integer within some finite range.

    Args:
        low: The minimum value in the range.
        high: The maximum value in the range.

    Returns:
        A random integer in the range [low, high].
    """

    num_bytes = (int(math.log(high, 2)) / 8) + 1
    n = int(os.urandom(num_bytes).encode('hex'), 16)
    while n < low or n > high:
        n = int(os.urandom(num_bytes).encode('hex'), 16)
    return n

def _random_bit_integer(k):
    """Generate a random k-bit integer.
    
    Args:
        k: The number of bits in the integer.
    Returns:
        A random k-bit integer.
    """

    low = (2 ** (k - 1)) + 1
    high = (2 ** k) - 1
    return _random_in_range(low, high)

def is_prime_rabin(n, t = 40):
    """Miller-Rabin primality test. 
    
    This code is implemented using algorithm 4.24 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).

    XXX: provide a better explanation of that value
    
    Args:
        n: The integer whose primality is in question.
        t: The security parameter. 

    Returns:
        True if n is deemed prime upon t iterations of the core algorithm.
        False otherwise.
    """

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    nn = n - 1
    s = 0
    while nn % 2 == 0:
        s += 1
        nn /= 2
    r = nn

    assert((2 ** s) * r == (n - 1))

    #num_trials = int(math.log((1 / probability), 4))
    for i in range(t):
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

def is_prime(p):
    return is_prime_rabin(p)

def random_prime_with_filter(k, condition, block = False):
    """Return a random k-bit prime that meets some criteria.

    Use a condition function to filter the prime result. For example,
    the function might be 
        lambda p : p % 4 == 3
    to check that the prime p = 3 mod 4. 

    We bound the number of iterations by 100k since we expect to find
    approximately one in every 0.7k numbers is prime. The constant 100
    gives us a large enough cushion to make this correct with overwhelming
    probability. For example, if k = 4096, then one in every ~2,867 numbers 
    is prime, and between 2^k and 2^{k+1} - 1 (inclusive) there is a *massive*
    amount of numbers.

    If block = true, then this will block until it definitely finds a prime. 

    Args:
        k: The number of bits in the prime.
        condition: The function to filter the prime result.
        block: A flag to indicate that the iteration bound should not be used.

    Returns:
        An integer n that is (probabilistically) prime and satisfies the given condition.
    """

    trial = 0
    num_trials = 100 * k
    while trial < num_trials or block:
        p = _random_bit_integer(k)
        if is_prime_rabin(p) and condition(p):
            return p
        trial += 1

    raise Exception("Could not generate a random prime that meets the criteria")

def random_prime(k, block = False):
    """Generate a random k-bit prime.

    Create a random prime according to algorithm 4.44 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).


    Args:
        k: The number of bits in the prime.
        block: A flag to indicate that the iteration bound should not be used.

    Returns:
        An integer that is probabilistically prime. 
    """
    
    return random_prime_with_filter(k, lambda p : True, block)


def safe_prime(k):
    """Generate a 2k-bit prime using Gordon's algorithm.

    Generate a safe prime using algorithm 4.53 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).

    Args:
        k: Half the number of bits in the result.

    Returns:
        A safe prime of length 2k bits that is incorrect with the given probability.
    """

    s = random_prime(k)
    t = random_prime(k)

    i = 1
    q = 0
    while q == 0:
        qt = (2 * i * t) + 1
        if is_prime_rabin(qt):
            q = qt
        i += 1
    r = q

    p0 = (2 * (pow(s, r - 2, r)) * s) - 1

    j = 1
    q = 0
    while q == 0:
        qt = p0 + (2 * j * r * s)
        if is_prime_rabin(qt):
            q = qt
        j += 1
    p = q

    return p

def fast_safe_prime(k):
    """ Quickly generate a k-bit safe prime.

    Quickly generate safe primes using the method of:
        https://eprint.iacr.org/2003/175.pdf
    This function will block until it finds a suitable prime.

    Args:
        k: The number of bits in the result.

    Returns: 
        A safe prime of length k bits that is incorrect with the given probability.
    """
    prime_filter = lambda p : p % 4 == 3

    while True:
        p = random_prime_with_filter(k, prime_filter)
        
        if is_prime_rabin((2 * p) + 1): 
            return p

def fast_safe_prime_2(k):
    """Quickly generate a safe prime.

    Use the algorithm outlined in https://eprint.iacr.org/2003/186.pdf.

    Args:
        k: The number of bits in the result.

    Returns: 
        A safe prime of length k bits that is incorrect with the given probability.
    """
    pass
