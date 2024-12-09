# ElGamal encryption and decryption

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, p):
    g, x, _ = extended_gcd(a, p)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % p

def elgamal_encrypt(message, p, g, y, k):
    c1 = pow(g, k, p)  # c1 = g^k % p
    c2 = (message * pow(y, k, p)) % p  # c2 = m * y^k % p
    return c1, c2

def elgamal_decrypt(c1, c2, p, x):
    # Decrypt the message m = c2 * (c1^x)^(-1) % p
    c1_x = pow(c1, x, p)  # c1^x % p
    c1_x_inv = mod_inverse(c1_x, p)  # Inverse of c1^x mod p
    message = (c2 * c1_x_inv) % p  # m = c2 * (c1^x)^(-1) % p
    return message

# Given values
p = 281
g = 3 #alpha
message = 'A' # m
x = 57  # random and private key
y = pow(g, x, p)  # Public key y = g^x % p
print(y)
k = 49  # session key

public_key = (p, g, y)
print(f"Public key: (p, g, y) = {public_key}")
# Encrypting the message
c1, c2 = elgamal_encrypt(ord(message), p, g, y, k)
print(f"Ciphertext: (c1, c2) = ({c1}, {c2})")

# Decrypting the message
decrypted_message = elgamal_decrypt(c1, c2, p, x)
print(f"Decrypted message: {chr(decrypted_message)}")