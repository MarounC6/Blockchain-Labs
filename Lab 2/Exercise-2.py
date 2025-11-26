import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(bits=512):
    """Generate a prime number with specified bit length (default 512 for 1024-bit RSA)
    because when p and q are multiplied n will be 1024 bits and the generated keys
    will be 1024 bits long."""
    prime = random.randrange(2 ** (bits - 1) + 1, 2 ** bits, 2)  # odd numbers only
    while not is_prime(prime):
        prime = random.randrange(2 ** (bits - 1) + 1, 2 ** bits, 2)
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



def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
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