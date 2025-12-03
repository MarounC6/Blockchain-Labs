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
    print("Public Key (n, e):", public_key)
    print("Private Key (n, d):", private_key)
    message = "Hello, RSA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print("Original message:", message)
    encrypted_msg = encrypt(message, public_key)
    print("Encrypted message:", encrypted_msg)
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print("Decrypted message:", decrypted_msg)