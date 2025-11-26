""" This code lets us decrypt a list of characters that were encrypted using RSA encryption using the private key."""

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message_Uni = [pow(charUni, d, n) for charUni in encrypted_message] # M = C^d mod n

    """ Convert Unicode integers back to characters """
    decrypted_message = ''.join([chr(charUni) for charUni in decrypted_message_Uni])
    return decrypted_message

# Example usage:
if __name__ == "__main__":
    print("=== RSA Decryption ===")
    
    # Get private key from user
    d = int(input("Please enter your private key d: "))
    n = int(input("Please enter your modulus n: "))
    private_key = (n, d)
    
    # Get encrypted message
    print("\nPlease enter the encrypted message (as a list of numbers):")
    print("Format: [num1, num2, num3, ...]")
    encrypted_input = input("Encrypted message: ")
    
    # Parse the encrypted message
    encrypted_msg = eval(encrypted_input)
    
    # Decrypt the message
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print("\nDecrypted message:", decrypted_msg)