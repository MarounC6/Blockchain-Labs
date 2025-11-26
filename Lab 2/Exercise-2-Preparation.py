""" This code let us generate two distinct prime numbers p and q of 512 bits each to create a 1024-bit RSA keypair.
The rest of the code can be found in the Exercise-2.py file. """

import secrets
import math

def is_probable_prime(n, k=40):
    if n <= 1:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        p = secrets.randbits(bits)
        p |= (1 << (bits - 1)) | 1  # ensure top bit and odd
        if is_probable_prime(p):
            return p

if __name__ == "__main__":
    p = generate_prime(512)
    q = generate_prime(512)
    print("Generated primes p and q:")
    print("p =", p)
    print("q =", q)
