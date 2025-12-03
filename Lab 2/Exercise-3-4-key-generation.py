import random
import math

def generate_keypair():
    p = 13056932318856843310644448299628916969227702961492332334730418406353218124606901311070668633265361798062241273296993366781912657899804766080546303633545241
    q = 11947512567685455735662913327603978387598921209168609052543969200310400962078773834003499670567840328714778672972828472123409156785174642040732775461639329

    '''
    if p == q or not is_prime(p) or not is_prime(q):
        raise ValueError("Both numbers must be distinct primes.")
    '''

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent e such that gcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi) # d=e^-1 mod phi
    return ((n, e), (n, d))

if __name__ == "__main__":
    public_key, private_key = generate_keypair()
    print("Public Key (n, e):", public_key)
    print("Private Key (n, d):", private_key)