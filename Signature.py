import hashlib
import random
import os

def calculate_hash(data, q):
    count_1s = sum(bin(byte).count('1') for byte in data)
    h = count_1s % q
    if h == 0:
        h = 1
    return h

def hash_message(message, q):
    hash_code = hashlib.sha256(message.encode()).hexdigest()
    hash_int = int(hash_code, 16) % q
    return hash_int if hash_int != 0 else 1

def generate_signature(data, private_key, a, p, q):
    h_m = calculate_hash(data, q)
    while True:
        k = random.randint(1, q - 1)
        r = pow(a, k, p)
        r1 = r % q
        if r1 == 0:
            continue

        s = (private_key * r1 + k * h_m) % q
        if 0 < s < q: 
            break

    return r1, s

def verify_signature(data, r1, s, public_key, a, p, q):
    if not (0 < r1 < q and 0 < s < q):
        return False

    h_m = calculate_hash(data, q)
    v = pow(h_m, q - 2, q)  
    z1 = (s * v) % q
    z2 = (q - r1) * v % q
    u = (pow(a, z1, p) * pow(public_key, z2, p) % p) % q
    return u == r1

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def save_hash_count(file_path, hash_count):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Number of 1's in binary representation: {hash_count}\n")

p, q = 227, 307
       
a = 3  
while pow(a, q, p) != 1:
        a += 1
    
private_key = random.randint(1, q - 1) 
public_key = pow(a, private_key, p) 

print(f"Initial parameters:\n"
    f"Modulus (p): {p}, q: {q}, Parameter (a): {a}\n"
    f"Private key (x): {private_key}, Public key (y): {public_key}")

file_path = input("Enter the path to the file: ")
data = read_file(file_path)
    
hash_count = calculate_hash(data, q)

r1, s = generate_signature(data, private_key, a, p, q)
print(f"Generated signature:\n r1 = {r1}, s = {s}")

is_valid = verify_signature(data, r1, s, public_key, a, p, q)
print(f"Signature valid: {is_valid}")

altered_r1 = r1 + random.randint(0, 10)  
altered_s = s + random.randint(0, 10)   
print(f"Altered signature:\n r1 = {altered_r1}, s = {altered_s}")

is_valid_after_change = verify_signature(data, altered_r1, altered_s, public_key, a, p, q)
print(f"Signature valid after alteration: {is_valid_after_change}")

directory_file = file_path.split('\\')[:-1]
directory = '\\'.join(directory_file)
if not os.path.exists(directory):
    os.makedirs(directory)

result_file_path = os.path.join(directory, 'signature_results.txt')
result_content = (
    f"Signature (r1, s): {r1, s}\n"
    f"Signature (altered r1, altered s): {altered_r1, altered_s}\n"
    f"Signature authenticity after alteration: {is_valid_after_change}\n"
)
write_file(result_file_path, result_content)

hash_count_file_path = os.path.join(directory, 'hash_count.txt')
save_hash_count(hash_count_file_path, hash_count)

print(f"The results are recorded in a file {result_file_path}")
print(f"The hash count is recorded in a file {hash_count_file_path}")
