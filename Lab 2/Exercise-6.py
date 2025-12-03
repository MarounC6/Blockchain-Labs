import random
import math
import time

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
    print("=" * 70)
    print("RSA Performance Analysis for 1024-bit keys")
    print("=" * 70)
    
    # Generate keypair once
    public_key, private_key = generate_keypair()
    n, e = public_key
    print(f"\nPublic Key (n, e):")
    print(f"  n = {n}")
    print(f"  e = {e}")
    print(f"\nKey size: 1024 bits ({n.bit_length()} bits actual)")
    
    print("\n" + "=" * 70)
    print("Performance Test Results")
    print("=" * 70)
    print(f"{'Message Size':<15} {'Encryption Time':<20} {'Ciphertext Size':<20}")
    print(f"{'(bytes)':<15} {'(seconds)':<20} {'(bytes)':<20}")
    print("-" * 70)
    
    # Test for message sizes: 2^10, 2^11, 2^12, ..., 2^22 bytes
    for power in range(10, 23):
        message_size = 2 ** power
        
        # Generate a message of the specified size (using 'A' repeated)
        message = 'A' * message_size
        
        # Measure encryption time
        start_time = time.time()
        encrypted_msg = encrypt(message, public_key)
        end_time = time.time()
        
        encryption_time = end_time - start_time
        
        # Calculate ciphertext size
        # Each encrypted character is a large integer, stored in the list
        # Size in bytes = number of integers * bytes per integer
        # Each integer in the ciphertext is at most n, which is ~1024 bits = 128 bytes
        ciphertext_size_bytes = len(encrypted_msg) * 128  # Approximate size
        
        print(f"2^{power:<2} = {message_size:<8} {encryption_time:<20.6f} {ciphertext_size_bytes:<20}")
        
        # For very large messages, we might want to stop early to avoid memory issues
        if encryption_time > 120:  # If it takes more than 120 seconds
            print("\nStopping early due to long processing time...")
            break
    
    print("\n" + "=" * 70)
    print("Analysis Notes:")
    print("=" * 70)
    print("1. Encryption time grows linearly with message size")
    print("   (each character is encrypted independently)")
    print("2. Ciphertext size = message_length × 128 bytes")
    print("   (each character becomes a 1024-bit encrypted value)")
    print("3. Ciphertext expansion factor ≈ 128×")
    print("   (1 byte plaintext → 128 bytes ciphertext)")
    print("=" * 70)