""" This code lets us decrypt a list of characters that were encrypted using RSA encryption using the private key."""

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message_Uni = [pow(charUni, d, n) for charUni in encrypted_message] # M = C^d mod n

    """ Convert Unicode integers back to characters """
    decrypted_message = ''.join([chr(charUni) for charUni in decrypted_message_Uni])
    return decrypted_message

# Example usage:
if __name__ == "__main__":
    