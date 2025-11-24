import random

# Function to generate a random binary key of given length
def rand_key(length):
    return "".join(str(random.randint(0, 1)) for _ in range(length))

# Function to perform XOR between two binary strings
def xor(a, b):
    return "".join("0" if a[i] == b[i] else "1" for i in range(len(a)))

def F_function(right, key):
    return xor(right, key)

# Feistel round function
def feistel_round(left, right, key):
    f = F_function(right, key)
    new_left = right
    new_right = xor(left, f)
    return new_left, new_right

# Encryption function
def feistel_encrypt(plain_text, rounds=2):
    # Convert plaintext to binary (8 bits for each character)
    pt_bin = "".join(format(ord(c), "08b") for c in plain_text)

    # Split into two halves
    n = len(pt_bin) // 2
    left, right = pt_bin[:n], pt_bin[n:]

    key = rand_key(len(right)) # we generate the key inside of the function, so each encryption will get a different key

    # Apply Feistel rounds
    for i in range(rounds):
        left, right = feistel_round(left, right, key)
    # Final ciphertext in binary
    cipher_bin = left + right

    # Convert binary to string
    cipher_text = ""
    for i in range(0, len(cipher_bin), 8):
        byte = cipher_bin[i:i+8]
        cipher_text += chr(int(byte, 2))

    return cipher_text, key, rounds

# Decryption function
def feistel_decrypt(cipher_text, key, rounds):
    # Convert ciphertext to binary
    ct_bin = "".join(format(ord(c), "08b") for c in cipher_text)

    # Split into two halves
    n = len(ct_bin) // 2
    left, right = ct_bin[:n], ct_bin[n:]

    # Apply Feistel rounds in reverse
    for i in range(rounds):
        right, left = feistel_round(right, left, key)

    # Final plaintext in binary
    plain_bin = left + right

    # Convert binary back to string
    plain_text = ""
    for i in range(0, len(plain_bin), 8):
        byte = plain_bin[i:i+8]
        plain_text += chr(int(byte, 2))

    return plain_text