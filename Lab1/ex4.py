import random
import time
import statistics
import csv
import argparse
import sys

# Keep deterministic for reproducible benchmarks
random.seed(0)


# Function to generate a random binary key of given length
def rand_key(length):
    return "".join(str(random.randint(0, 1)) for _ in range(length))


# Function to perform XOR between two binary strings
def xor(a, b):
    return "".join("0" if a[i] == b[i] else "1" for i in range(len(a)))


def F_function(right, key):
    # Expansion D-box: Expanding the 32 bits data into 48 bits
    exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
             6, 7, 8, 9, 8, 9, 10, 11,
             12, 13, 12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21, 20, 21,
             22, 23, 24, 25, 24, 25, 26, 27,
             28, 29, 28, 29, 30, 31, 32, 1]

    # Expand right from 32 bits to 48 bits
    right_expanded = "".join(right[exp_d[i] - 1] for i in range(48))

    # XOR with round key
    xor_x = xor(right_expanded, key)

    # S-boxes: 8 S-boxes, each takes 6 bits input and produces 4 bits output
    sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    # Apply S-boxes
    sbox_str = ""
    for j in range(8):
        i_start = j * 6
        row = int(xor_x[i_start] + xor_x[i_start + 5], 2)
        col = int(xor_x[i_start + 1:i_start + 5], 2)
        val = sbox[j][row][col]
        sbox_str += format(val, "04b")

    # Straight D-box (P-box): Permutation after S-boxes
    per = [16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25]

    # Apply permutation
    sbox_str = "".join(sbox_str[per[i] - 1] for i in range(32))

    return sbox_str


# DES round function
def DES_round(left, right, key):
    # Apply F function to right half
    f_result = F_function(right, key)

    # XOR left with F result
    new_right = xor(left, f_result)

    # Right becomes new left (swap happens in main loop)
    return new_right, right


def DES_create_keys(length=64):
    # Fixed block size of 64 bits and key size of 64 bits

    main_key = rand_key(length)
    # Skip every 8th bit to create effective key (removes parity bits)
    effective_key = "".join(main_key[i] for i in range(len(main_key)) if (i + 1) % 8 != 0)

    keys = [0] * 16

    # Number of bit shifts
    shift_table = [1, 1, 2, 2,
                   2, 2, 2, 2,
                   1, 2, 2, 2,
                   2, 2, 2, 1]

    # Key- Compression Table : Compression of key from 56 bits to 48 bits
    key_comp = [14, 17, 11, 24, 1, 5,
                3, 28, 15, 6, 21, 10,
                23, 19, 12, 4, 26, 8,
                16, 7, 27, 20, 13, 2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32]

    left = effective_key[0:28]
    right = effective_key[28:56]
    for i in range(16):
        # Shifting the bits by nth shifts by checking from shift table
        left = left[shift_table[i]:] + left[:shift_table[i]]
        right = right[shift_table[i]:] + right[:shift_table[i]]

        # Combination of left and right string
        combine_str = left + right

        # Compression of key from 56 to 48 bits
        round_key = "".join(combine_str[key_comp[j] - 1] for j in range(48))

        keys[i] = round_key

    return keys


# Encryption function for a single 8-char block
def DES_encrypt(plain_text, keys):
    # plain_text must be exactly 8 characters (64 bits)
    if len(plain_text) != 8:
        raise ValueError("DES_encrypt expects an 8-character block")

    # Convert plaintext to binary (8 bits for each character)
    pt_bin = "".join(format(ord(c), "08b") for c in plain_text)

    initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7]

    # Apply initial permutation
    permutated_bin = ['0'] * len(initial_perm)
    for i in range(len(initial_perm)):
        permutated_bin[i] = pt_bin[initial_perm[i] - 1]
    pt_bin = "".join(permutated_bin)

    # Split into two halves the plaintext
    n = len(pt_bin) // 2
    left, right = pt_bin[:n], pt_bin[n:]

    # Apply DES rounds (16 rounds for full DES)
    for i in range(16):
        # Apply DES round function
        new_right, new_left = DES_round(left, right, keys[i])

        # Swap for next round (except last round)
        if i != 15:
            left, right = new_left, new_right
        else:
            left, right = new_right, new_left

    # Final ciphertext in binary
    cipher_bin = left + right

    final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
                  39, 7, 47, 15, 55, 23, 63, 31,
                  38, 6, 46, 14, 54, 22, 62, 30,
                  37, 5, 45, 13, 53, 21, 61, 29,
                  36, 4, 44, 12, 52, 20, 60, 28,
                  35, 3, 43, 11, 51, 19, 59, 27,
                  34, 2, 42, 10, 50, 18, 58, 26,
                  33, 1, 41, 9, 49, 17, 57, 25]

    # Apply final permutation
    cipher_bin = "".join(cipher_bin[final_perm[i] - 1] for i in range(64))

    # Convert binary to string (8 chars)
    cipher_text = ""
    for i in range(0, len(cipher_bin), 8):
        byte = cipher_bin[i:i + 8]
        cipher_text += chr(int(byte, 2))

    return cipher_text


# Decryption function for a single 8-char block
def DES_decrypt(cipher_text, keys):
    # Convert ciphertext to binary
    ct_bin = "".join(format(ord(c), "08b") for c in cipher_text)

    initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7]

    # Apply initial permutation
    permutated_bin = ['0'] * len(initial_perm)
    for i in range(len(initial_perm)):
        permutated_bin[i] = ct_bin[initial_perm[i] - 1]
    ct_bin = "".join(permutated_bin)

    # Split into two halves
    n = len(ct_bin) // 2
    left, right = ct_bin[:n], ct_bin[n:]

    # Apply DES rounds in reverse
    for i in reversed(range(16)):
        # Apply DES round function in reverse
        new_right, new_left = DES_round(left, right, keys[i])

        # Swap for next round (except last round)
        if i != 0:
            left, right = new_left, new_right
        else:
            left, right = new_right, new_left

    # Final plaintext in binary
    plain_bin = left + right

    final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
                  39, 7, 47, 15, 55, 23, 63, 31,
                  38, 6, 46, 14, 54, 22, 62, 30,
                  37, 5, 45, 13, 53, 21, 61, 29,
                  36, 4, 44, 12, 52, 20, 60, 28,
                  35, 3, 43, 11, 51, 19, 59, 27,
                  34, 2, 42, 10, 50, 18, 58, 26,
                  33, 1, 41, 9, 49, 17, 57, 25]

    # Apply final permutation
    plain_bin = "".join(plain_bin[final_perm[i] - 1] for i in range(64))

    # Convert binary back to string
    plain_text = ""
    for i in range(0, len(plain_bin), 8):
        byte = plain_bin[i:i + 8]
        plain_text += chr(int(byte, 2))

    return plain_text


def generate_random_message_bytes(size):
    """
    Generate a random bytes object of given size.
    Uses random.randbytes when available (Python 3.9+), otherwise fallback.
    """
    if hasattr(random, "randbytes"):
        return random.randbytes(size)
    # fallback for older or other Python versions
    return bytes(random.getrandbits(8) for _ in range(size))


def bytes_to_str_latin1(b):
    """
    Convert bytes to Python str using latin-1 (one-to-one mapping 0..255)
    so ord() on resulting string gives original byte values.
    """
    return b.decode("latin-1")


def encrypt_message(message_str, keys):
    """
    Encrypt an arbitrary-length message (str) by splitting into 8-char blocks.
    Returns the concatenated cipher blocks as a str (latin-1 bytes).
    """
    # Pad with null bytes to multiple of 8 chars
    if len(message_str) % 8 != 0:
        message_str = message_str.ljust((len(message_str) // 8 + 1) * 8, "\x00")

    cipher_blocks = []
    for i in range(0, len(message_str), 8):
        block = message_str[i:i + 8]
        cipher_blocks.append(DES_encrypt(block, keys))
    return "".join(cipher_blocks)


def benchmark_des(min_exp=10, max_exp=26, trials=3, out_csv=None):
    """
    Benchmark encryption time for message sizes 2^min_exp ... 2^max_exp bytes.
    trials: number of repetitions per size (to average).
    out_csv: filename to write CSV results, if provided.
    """
    # Create DES round keys once and reuse for all trials for fairness
    round_keys = DES_create_keys()

    results = []
    print(f"Benchmarking DES encryption from 2^{min_exp} to 2^{max_exp} bytes (inclusive)")
    print(f"Trials per size: {trials}")
    print("Size (B)\tAvg time (s)\tStd dev (s)\tThroughput (MB/s)")
    try:
        for exp in range(min_exp, max_exp + 1):
            size = 2 ** exp
            trial_times = []
            for t in range(trials):
                # Generate a new random message for each trial
                msg_bytes = generate_random_message_bytes(size)
                msg_str = bytes_to_str_latin1(msg_bytes)

                # Measure encryption time only
                t0 = time.perf_counter()
                _ = encrypt_message(msg_str, round_keys)
                t1 = time.perf_counter()
                elapsed = t1 - t0
                trial_times.append(elapsed)

            avg_t = statistics.mean(trial_times)
            std_t = statistics.stdev(trial_times) if trials > 1 else 0.0
            throughput_mb_s = (size / (1024 * 1024)) / avg_t if avg_t > 0 else float("inf")
            print(f"{size}\t{avg_t:.6f}\t{std_t:.6f}\t{throughput_mb_s:.3f}")

            results.append({
                "exp": exp,
                "size_bytes": size,
                "avg_time_s": avg_t,
                "std_time_s": std_t,
                "throughput_MB_s": throughput_mb_s
            })
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user.", file=sys.stderr)

    if out_csv:
        with open(out_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["exp", "size_bytes", "avg_time_s", "std_time_s", "throughput_MB_s"])
            for r in results:
                writer.writerow([r["exp"], r["size_bytes"], r["avg_time_s"], r["std_time_s"], r["throughput_MB_s"]])
        print(f"Results written to {out_csv}")

    return results


# Quick smoke test to validate correctness of encrypt/decrypt for one block
def smoke_test():
    round_keys = DES_create_keys()
    block = "ABCDEFGH"
    cipher = DES_encrypt(block, round_keys)
    plain = DES_decrypt(cipher, round_keys)
    assert plain == block, f"DES encrypt/decrypt smoke test failed: got {repr(plain)}"
    print("Smoke test passed (single block encrypt/decrypt)")


# Driver Code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DES implementation with benchmarking for varying message sizes.")
    parser.add_argument("--min-exp", type=int, default=10, help="Minimum exponent (2^min_exp bytes). Default 10.")
    parser.add_argument("--max-exp", type=int, default=26, help="Maximum exponent (2^max_exp bytes). Default 26.")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials per size. Default 3.")
    parser.add_argument("--csv", type=str, default="des_benchmark_results.csv", help="CSV output filename. Default des_benchmark_results.csv")
    parser.add_argument("--no-smoke", action="store_true", help="Skip the smoke test.")
    args = parser.parse_args()

    if not args.no_smoke:
        smoke_test()

    results = benchmark_des(min_exp=args.min_exp, max_exp=args.max_exp, trials=args.trials, out_csv=args.csv)

    # Print a short summary
    print("\nSummary:")
    for r in results:
        print(f"2^{r['exp']} ({r['size_bytes']} B): avg {r['avg_time_s']:.6f} s, {r['throughput_MB_s']:.3f} MB/s")