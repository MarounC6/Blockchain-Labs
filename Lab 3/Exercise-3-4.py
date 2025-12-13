# import necessary modules to time the function
import time

# --- SHA-512 CONSTANTS ---

# Modulo mask for 64-bit operations (2^64)
MASK_64 = 0xFFFFFFFFFFFFFFFF

# Initial Hash Values (H) - Fractional parts of the square roots of the first 8 primes
H = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
]

# Round Constants (K) - Fractional parts of the cube roots of the first 80 primes
K = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 
                  0xe9b5dba58189dbbc, 0x3956c25bf348b538, 0x59f111f1b605d019,
                  0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242,
                  0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
                  0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
                  0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
                  0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275,
                  0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
                  0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f,
                  0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
                  0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc,
                  0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
                  0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6,
                  0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
                  0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
                  0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
                  0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99,
                  0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
                  0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc,
                  0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
                  0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915,
                  0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
                  0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba,
                  0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
                  0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
                  0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
                  0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

# --- UTILITY BITWISE FUNCTIONS ---

def ROTR(x, n):
    """Rotate Right (64-bit)"""
    # Uses MASK_64 to ensure 64-bit behavior
    return ((x >> n) | (x << (64 - n))) & MASK_64

def SHR(x, n):
    """Shift Right (64-bit)"""
    return (x >> n)

# Compression Function Utilities
def Ch(x, y, z):
    """Choice function: (x AND y) XOR (NOT x AND z)"""
    return (x & y) ^ (~x & z) & MASK_64

def Maj(x, y, z):
    """Majority function: (x AND y) XOR (x AND z) XOR (y AND z)"""
    return (x & y) ^ (x & z) ^ (y & z)

def Sigma0(x):
    """SHA-512 Big Sigma 0 (Rotation constants: 28, 34, 39)"""
    return ROTR(x, 28) ^ ROTR(x, 34) ^ ROTR(x, 39)

def Sigma1(x):
    """SHA-512 Big Sigma 1 (Rotation constants: 14, 18, 41)"""
    return ROTR(x, 14) ^ ROTR(x, 18) ^ ROTR(x, 41)

# Message Scheduling Utilities
def sigma0(x):
    """SHA-512 Little Sigma 0 (Rotation/Shift constants: 1, 8, 7)"""
    return ROTR(x, 1) ^ ROTR(x, 8) ^ SHR(x, 7)

def sigma1(x):
    """SHA-512 Little Sigma 1 (Rotation/Shift constants: 19, 61, 6)"""
    return ROTR(x, 19) ^ ROTR(x, 61) ^ SHR(x, 6)

def padding(data: bytes) -> bytearray:
    """Pads the input byte string according to SHA-512 standard."""
    data_len_bits = len(data) * 8
    
    # 1. Append '1' bit (0x80 byte)
    padded_data = bytearray(data)
    padded_data.append(0x80)
    
    # 2. Append '0' bits until the length is 896 mod 1024
    # Block size is 128 bytes (1024 bits). Length field is 16 bytes (128 bits).
    # We pad until (L' * 8) % 1024 = 896
    
    # Calculate the number of zero bytes needed
    # (len(padded_data) * 8) is the current length in bits
    # We want 1024 - 128 = 896 bits before the length.
    # We need to reach the next L such that L % 128 = 112 (128 - 16)
    
    while (len(padded_data) * 8) % 1024 != 896:
        padded_data.append(0x00)
    
    # 3. Append original length (128 bits / 16 bytes) in big-endian format
    padded_data.extend(data_len_bits.to_bytes(16, byteorder='big'))
    
    return padded_data

def sha512_hash(data: bytes) -> str:
    """The main SHA-512 implementation function."""
    
    # 1. Initialize hash values
    h = list(H)
    
    # 2. Pre-processing: Padding
    padded_data = padding(data)
    
    # 3. Process the message in 1024-bit (128-byte) chunks
    for i in range(0, len(padded_data), 128):
        block = padded_data[i:i + 128]
        
        # a. Message Schedule (W): 80 64-bit words
        W = [0] * 80
        
        # The first 16 words (W[0] through W[15]) are from the current block
        for t in range(16):
            # Big-endian conversion of 8 bytes (64 bits)
            W[t] = int.from_bytes(block[t * 8: (t + 1) * 8], byteorder='big')
            
        # The remaining 64 words (W[16] through W[79]) are generated
        for t in range(16, 80):
            s0 = sigma0(W[t - 15])
            s1 = sigma1(W[t - 2])
            
            # W[t] = W[t-16] + s0 + W[t-7] + s1 (mod 2^64)
            W[t] = (W[t - 16] + s0 + W[t - 7] + s1) & MASK_64

        # b. Initialize the eight working variables (a, b, c, d, e, f, g, h_var)
        # Using a tuple/list to simulate the register bank
        a, b, c, d, e, f, g, h_var = h
        
        # c. Main Loop: 80 Rounds
        for t in range(80):
            # Step 1: Calculate T1
            # T1 = h_var + Sigma1(e) + Ch(e, f, g) + K[t] + W[t] (mod 2^64)
            T1 = (h_var + Sigma1(e) + Ch(e, f, g) + K[t] + W[t]) & MASK_64
            
            # Step 2: Calculate T2
            # T2 = Sigma0(a) + Maj(a, b, c) (mod 2^64)
            T2 = (Sigma0(a) + Maj(a, b, c)) & MASK_64
            
            # Step 3: Update variables (the eight registers shift)
            h_var = g
            g = f
            f = e
            e = (d + T1) & MASK_64
            d = c
            c = b
            b = a
            a = (T1 + T2) & MASK_64
        
        # d. Update the intermediate hash value (H)
        h[0] = (h[0] + a) & MASK_64
        h[1] = (h[1] + b) & MASK_64
        h[2] = (h[2] + c) & MASK_64
        h[3] = (h[3] + d) & MASK_64
        h[4] = (h[4] + e) & MASK_64
        h[5] = (h[5] + f) & MASK_64
        h[6] = (h[6] + g) & MASK_64
        h[7] = (h[7] + h_var) & MASK_64

    # 4. Final Hash Output (512 bits)
    final_hash = b''
    for val in h:
        final_hash += val.to_bytes(8, byteorder='big')
        
    return final_hash.hex()

#Exercise 3 :

""" def concatenate_bytes(id, x):
    Concatenates two strings"
    result = b''
    result += id
    result += x
    return result
 """

def concatenate_bytes(id, nonce):
    """Concatenates id and a fixed-width nonce (x: int -> bytes)."""
    # x is now an integer nonce; encode to fixed-width bytes (8 bytes here)
    return id + nonce.to_bytes(8, byteorder='big')

def time_to_find_leading_zero(num_zeros=1):
    """Finds a value x such that sha512_hash(id || x) starts with num_zeros '0's"""
    id = b'random'
    nonce = 0#x = b''
    target = '0' * num_zeros     
    time_start = time.time()

    while True:    
        
        #nonce_bytes = nonce.to_bytes(8, byteorder='big')
        h = sha512_hash(concatenate_bytes(id, nonce))   # compute once
        if h.startswith(target):         # found a hash with leading '0's
            time_end = time.time()
            break
        #print(h)                      # optional: show attempts
        nonce += 1
        if time.time() - time_start > 600:  # avoid long runs in testing:
            time_end = time.time()
            print(f'Timeout reached after {round(time_end - time_start, 2)} seconds. No value found.\n\n')
            return round(time_end - time_start, 2)
        if nonce >= 1 << (8 * 8):  # 8 bytes nonce space
            raise OverflowError("Nonce space exhausted; increase nonce_width or use extra-nonce")                     # try next candidate

    print(f'Valeur de x trouvée : {nonce}, hash: {h}, temps écoulé: {round(time_end - time_start, 2)} secondes\n\n')
    return round(time_end - time_start, 2)

""" for i in range(1, 7):
    print(f'--- Recherche pour {i} zéros initiaux ---')
    time_to_find_leading_zero(i) """

#Exercise 4 :
# need to store the time taken for each number of leading zeros and make a small analysis of the results and a graphic representation (e.g., using matplotlib)
data = []
for i in range(1, 10):
    print(f'--- Recherche pour {i} zéros initiaux ---')
    time_values = time_to_find_leading_zero(i)
    data.append((i, time_values))

# need to store the values in a csv file
import csv

# Store data
with open('sha512_leading_zeros_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Leading Zeros', 'Time (seconds)'])
    for row in data:
        writer.writerow(row)

# Extract data with error handling
leading_zeros = []
times = []

try:
    with open('sha512_leading_zeros_results.csv', mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader for named columns
        for row in reader:
            leading_zeros.append(int(row['Leading Zeros']))
            times.append(float(row['Time (seconds)']))
except FileNotFoundError:
    print("CSV file not found. Run the data collection first.")

#Pltotting the results
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(leading_zeros, times, marker='o')
plt.title('Time to Find SHA-512 Hash with Leading Zeros')
plt.xlabel('Number of Leading Zeros')
plt.ylabel('Time (seconds)')
plt.yscale('log')  # Logarithmic scale for better visualization
plt.grid(True, which="both", ls="--")
plt.show()