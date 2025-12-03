""" This code lets us encrypt a list of characters using RSA encryption using the public key of a recipient and sign it using my private key."""

import random
import math

def sign_encrypt(message, my_private_key):
    n, d = my_private_key

    """ Convert the message to Unicode integers and encrypt each character """
    message_unicode = [ord(char) for char in message]

    encrypted_message = [pow(charUni, d, n) for charUni in message_unicode] # C = M^d mod n
    return encrypted_message

def encrypt(message, recipient_public_key):
    """Encrypt a message (list of integers) with recipient's public key."""
    n, e = recipient_public_key

    encrypted_message = [pow(charUni, e, n) for charUni in message] # C = M^e mod n
    return encrypted_message

if __name__ == "__main__":
    my_public_key = (int(input("my_public_key_n: ")), int(input("my_public_key_e: ")))
    my_private_key = (int(input("my_private_key_n: ")), int(input("my_private_key_d: ")))
    print("My Public Key (n, e):", my_public_key)
    print("My Private Key (n, d):", my_private_key)

    my_message = "Hello, Dear friend"
    print("Original message:", my_message)
    signed_encrypted_msg = sign_encrypt(my_message, my_private_key)
    print("Signed message:", signed_encrypted_msg)

    recipient_public_key = (int(input("recipient_public_key_n: ")), int(input("recipient_public_key_e: ")))

    final_encrypted_msg = encrypt(signed_encrypted_msg, recipient_public_key)
    print("Final Encrypted message for recipient:", final_encrypted_msg)
