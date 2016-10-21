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

def is_prime_rabin(n, probability = 0.01):
    """Miller-Rabin primality test. 
    
    This code is implemented using algorithm 4.24 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).
    
    Args:
        n: The integer whose primality is in question.
        probability: The probability that the result is incorrect.

    Returns:
        True if n is prime prob. (1 - probability).
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

def random_prime(k, probability = 0.01, num_trials = 0):
    """Generate a random k-bit prime.

    Create a random prime according to algorithm 4.44 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).

    Args:
        k: The number of bits in the prime.
        probability: The probability that the number is composite.

    Returns:
        An integer that is prime with probability (1 - probability)
    """
    
    block = num_trials == 0
    trial = 0
    while trial < num_trials or block:
        n = _random_bit_integer(k)
        if is_prime_rabin(n, probability):
            return n
        trial += 1

    raise Exception("Could not generate a random prime")

def random_prime_with_filter(k, condition, probability = 0.01):
    """Return a random k-bit prime that meets some criteria.

    Use a condition function to filter the prime result. For example,
    the function might be 
        lambda p : p % 4 == 3
    to check that the prime p = 3 mod 4. 

    Args:
        k: The number of bits in the prime.
        condition: The function to filter the prime result
        probability: The probability that the number is composite.

    Returns:
        An integer n that is prime with prob. (1 - probability) and meets the condition function. 
    """

    num_trials = 1000

    trial = 0
    while trial < num_trials:
        p = random_prime(k, probability)
        if condition(p):
            return p
        trial += 1
    raise Exception("Could not generate a random prime that meets the criteria")

def safe_prime(k, probability = 0.01):
    """Generate a 2k-bit prime.

    Generate a safe prime using algorithm 4.53 from the HAC (http://cacr.uwaterloo.ca/hac/about/chap4.pdf).

    Args:
        k: Half the number of bits in the result.
        probability: The probability that the result is composite.

    Returns:
        A safe prime of length 2k bits that is incorrect with the given probability.
    """

    s = random_prime(k, probability)
    t = random_prime(k, probability)

    i = 1
    q = 0
    while q == 0:
        qt = (2 * i * t) + 1
        if is_prime_rabin(qt, probability):
            q = qt
        i += 1

    r = q

    p0 = (2 * (pow(s, r - 2, r)) * s) - 1

    j = 1
    q = 0
    while q == 0:
        qt = p0 + (2 * j * r * s)
        if is_prime_rabin(qt, probability):
            q = qt
        j += 1

    p = q

    return p

def fast_safe_prime(k, probability = 0.01):
    """ Quickly generate a k-bit safe prime.

    Quickly generate safe primes using the method of:
        https://eprint.iacr.org/2003/175.pdf
    This function will block until it finds a suitable prime.

    Args:
        k: The number of bits in the result.
        probability: The probability that the result is composite.

    Returns: 
        A safe prime of length k bits that is incorrect with the given probability.
    """
    def prime_filter(p):
        return p % 4 == 3
    while True:
        p = random_prime_with_filter(k, prime_filter, probability)
        
        if is_prime_rabin((2 * p) + 1, probability) or is_prime((p - 1) / 2, probability):
            return p

def fast_safe_prime_2(k, probability = 0.01):
    """Quickly generate a safe prime.

    Use the algorithm outlined in https://eprint.iacr.org/2003/186.pdf.

    Args:
        k: The number of bits in the result.
        probability: The probability that the result is composite.

    Returns: 
        A safe prime of length k bits that is incorrect with the given probability.
    """
    pass
