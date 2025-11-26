import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_keypair():
    p = 7919
    q = 1009

    if p == q or not is_prime(p) or not is_prime(q):
        raise ValueError("Both numbers must be distinct primes.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent e such that gcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi) # d=e^-1 mod phi
    return ((n, e), (n, d))



def encrypt(message, public_key):
    n, e = public_key

    """ Convert the message to Unicode integers and encrypt each character """
    message_unicode = [ord(char) for char in message]

    encrypted_message = [pow(charUni, e, n) for charUni in message_unicode] # C = M^e mod n
    return encrypted_message

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message_Uni = [pow(charUni, d, n) for charUni in encrypted_message] # M = C^d mod n

    """ Convert Unicode integers back to characters """
    decrypted_message = ''.join([chr(charUni) for charUni in decrypted_message_Uni])
    return decrypted_message


# Example usage:
if __name__ == "__main__":
    public_key, private_key = generate_keypair()
    message = "Hello, RSA!"
    print("Original message:", message)
    encrypted_msg = encrypt(message, public_key)
    print("Encrypted message:", encrypted_msg)
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print("Decrypted message:", decrypted_msg)