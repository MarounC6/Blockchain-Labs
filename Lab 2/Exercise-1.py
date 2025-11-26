import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime():
    while True:
        prime = random.randint(2 ** 8, 2 ** 16)
        if is_prime(prime):
            return prime

def generate_keypair():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi)
        if math.gcd(e, phi) == 1:
            break

    d = pow(e, -1, phi)
    return ((n, e), (n, d))
