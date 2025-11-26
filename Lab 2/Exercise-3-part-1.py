""" This code lets us encrypt a list of characters using RSA encryption using the public key of a recipient."""

def encrypt(message, recipient_public_key):
    n, e = recipient_public_key

    """ Convert the message to Unicode integers and encrypt each character """
    message_unicode = [ord(char) for char in message]

    encrypted_message = [pow(charUni, e, n) for charUni in message_unicode] # C = M^e mod n
    return encrypted_message

# Example usage:
if __name__ == "__main__":
    print("=== RSA Encryption ===")
    
    # Get public key from user
    e = int(input("Please enter the recipient's public key e: "))
    n = int(input("Please enter the recipient's modulus n: "))
    recipient_public_key = (n, e)
    
    # Get encrypted message
    print("\nPlease enter the message to encrypt:")
    message = input("Message: ")
    
    # Parse the encrypted message
    encrypted_msg = encrypt(message, recipient_public_key)
    
    print("\nEncrypted message:", encrypted_msg)