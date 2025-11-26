import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime():
    prime = random.randrange(2 ** 8 + 1, 2 ** 16, 2)  # odd numbers only
    while not is_prime(prime):
        prime = random.randrange(2 ** 8 + 1, 2 ** 16, 2)
    return prime

def generate_keypair():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent e such that gcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi) # d=e^-1 mod phi
    return ((n, e), (n, d))
