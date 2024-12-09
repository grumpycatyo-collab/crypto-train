# RSA encryption
def rsa_encrypt(message, p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Encrypt the message
    ciphertext = pow(message, e, n)
    return ciphertext

# Given values
p = 5
q = 13
message = 3
e = 11

# Encrypting the message
ciphertext = rsa_encrypt(message, p, q, e)
print(f"Encrypted message: {ciphertext}")

# RSA decryption
def rsa_decrypt(ciphertext, p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Calculate the decryption key
    d = pow(e, -1, phi_n)

    # Decrypt the message
    decrypted_message = pow(ciphertext, d, n)
    return decrypted_message

print(f"Decrypted message: {rsa_decrypt(ciphertext, p, q, e)}")
