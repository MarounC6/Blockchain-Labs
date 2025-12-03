""" This code lets us decrypt a list of characters using RSA encryption. The message was encrypted using my public key and signed using the recipient's private key.
    It will be decrypted using the recipient's public key to verify the signature authenticity, and then using my private key to get the original message.
"""

import random
import math

def decrypt_verify_authenticity(encrypted_message, recipient_public_key):
    """Decrypt a list of integers to a string.

    Handles the case where the decrypted integer is larger than a single
    Unicode code point by converting the integer to bytes and decoding.
    This prevents OverflowError when `chr()` can't accept very large ints.
    """
    n, e = recipient_public_key
    parts = []
    for char in encrypted_message:
        m = pow(char, e, n)
        try:
            parts.append(chr(m))
        except (OverflowError, ValueError):
            # Convert integer to minimal big-endian byte sequence
            length = (m.bit_length() + 7) // 8
            if length == 0:
                parts.append('')
                continue
            b = m.to_bytes(length, byteorder='big')
            # Try UTF-8 first, fall back to latin-1 to preserve bytes
            try:
                parts.append(b.decode('utf-8'))
            except UnicodeDecodeError:
                parts.append(b.decode('latin-1'))

    decrypted_message = ''.join(parts)
    return decrypted_message

def decrypt_message(encrypted_message, my_private_key):
    """Decrypt a list of integers and return a list of integers (not converted to characters).
    
    This is used for the first decryption step where we need to preserve
    the integer values for subsequent signature verification.
    """
    n, d = my_private_key
    decrypted_integers = []
    for char in encrypted_message:
        m = pow(char, d, n)
        decrypted_integers.append(m)
    
    return decrypted_integers

if __name__ == "__main__":
    my_public_key = (int(input("my_public_key_n: ")), int(input("my_public_key_e: ")))
    my_private_key = (int(input("my_private_key_n: ")), int(input("my_private_key_d: ")))
    print("My Public Key (n, e):", my_public_key)
    print("My Private Key (n, d):", my_private_key)

    n=int(input("recipient_public_key_n: "))
    e=int(input("recipient_public_key_e: "))
    recipient_public_key = (n, e)

    # Get encrypted message
    print("\nPlease enter the encrypted message (as a list of numbers):")
    print("Format: [num1, num2, num3, ...]")
    encrypted_input = input("Encrypted message: ")
    
    # Parse the encrypted message
    encrypted_msg = eval(encrypted_input)

    print("\nStep 1: Decrypt using my private key to get the message signed by recipient.")
    print("Note: We should do the steps in this order because when a person sends a message, they first sign it with their private key and then encrypt it with the recipient's public key.")

    Decrypted_signed_msg = decrypt_message(encrypted_msg, my_private_key)
    print("\nMessage after Decryption:", Decrypted_signed_msg)

    print("\nStep 2: Verify authenticity using recipient's public key.")
    final_decrypted_msg = decrypt_verify_authenticity(Decrypted_signed_msg, recipient_public_key)
    print("\nFinal Decrypted message:", final_decrypted_msg)