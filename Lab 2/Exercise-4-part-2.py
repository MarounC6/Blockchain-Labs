""" This code lets us decrypt a list of characters using RSA encryption. The message was encrypted using my public key and signed using the recipient's private key.
    It will be decrypted using the recipient's public key to verify the signature authenticity, and then using my private key to get the original message.
"""

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
    """Decrypt a list of integers to a string.

    Handles the case where the decrypted integer is larger than a single
    Unicode code point by converting the integer to bytes and decoding.
    This prevents OverflowError when `chr()` can't accept very large ints.
    """
    n, d = my_private_key
    parts = []
    for char in encrypted_message:
        m = pow(char, d, n)
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

if __name__ == "__main__":
    my_public_key, my_private_key = generate_keypair()
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

    verified_msg = decrypt_verify_authenticity(encrypted_msg, recipient_public_key)
    print("\nVerified message after authenticity check:", verified_msg)
    final_decrypted_msg = decrypt_message(encrypted_msg, my_private_key)
    print("\nFinal Decrypted message:", final_decrypted_msg)