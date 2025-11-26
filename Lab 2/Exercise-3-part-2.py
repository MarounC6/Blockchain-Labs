""" This code lets us decrypt a list of characters using my private key. The message was encrypted using my public key."""

def decrypt(encrypted_message, private_key):
    """Decrypt a list of integers to a string.

    Handles the case where the decrypted integer is larger than a single
    Unicode code point by converting the integer to bytes and decoding.
    This prevents OverflowError when `chr()` can't accept very large ints.
    """
    n, d = private_key
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

# Example usage:
if __name__ == "__main__":
    print("=== RSA Decryption ===")
    
    # Get private key from user
    d = int(input("Please enter your private key d: "))
    n = int(input("Please enter your modulus n: "))
    my_private_key = (n, d)
    
    # Get encrypted message
    print("\nPlease enter the encrypted message (as a list of numbers):")
    print("Format: [num1, num2, num3, ...]")
    encrypted_input = input("Encrypted message: ")
    
    # Parse the encrypted message
    encrypted_msg = eval(encrypted_input)
    
    # Decrypt the message
    decrypted_msg = decrypt(encrypted_msg, my_private_key)
    print("\nDecrypted message:", decrypted_msg)
