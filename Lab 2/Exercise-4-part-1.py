""" This code lets us encrypt a list of characters using RSA encryption using the public key of a recipient and sign it using my private key."""

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

def sign_encrypt(message, my_private_key):
    n, d = my_private_key

    """ Convert the message to Unicode integers and encrypt each character """
    message_unicode = [ord(char) for char in message]

    encrypted_message = [pow(charUni, d, n) for charUni in message_unicode] # C = M^d mod n
    return encrypted_message

def encrypt(message, recipient_public_key):
    n, e = recipient_public_key

    """ Convert the message to Unicode integers and encrypt each character """
    message_unicode = [ord(char) for char in message]

    encrypted_message = [pow(charUni, e, n) for charUni in message_unicode] # C = M^e mod n
    return encrypted_message

if __name__ == "__main__":
    my_public_key, my_private_key = generate_keypair()
    print("My Public Key (n, e):", my_public_key)
    print("My Private Key (n, d):", my_private_key)

    my_message = "Hello, Dear friend"
    print("Original message:", my_message)
    signed_encrypted_msg = sign_encrypt(my_message, my_private_key)
    print("Signed and Encrypted message:", signed_encrypted_msg)

    recipient_public_key = (int(input("recipient_public_key_n: ")), int(input("recipient_public_key_e: ")))

    final_encrypted_msg = encrypt(my_message, recipient_public_key)
    print("Final Encrypted message for recipient:", final_encrypted_msg)
