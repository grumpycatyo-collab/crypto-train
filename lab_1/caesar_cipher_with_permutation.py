def create_permuted_alphabet(key2):
    key2 = ''.join(dict.fromkeys(key2.upper()))
    remaining_letters = ''.join([c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c not in key2])
    print(key2 + remaining_letters)
    print((key2 + remaining_letters).lower())
    return key2 + remaining_letters


def caesar_cipher_with_permutation(text, key1, key2, mode):
    permuted_alphabet = create_permuted_alphabet(key2)
    result = ""
    text = text.upper().replace(" ", "")

    for char in text:
        if char.isalpha():
            index = permuted_alphabet.index(char)
            new_index = 0
            if mode == "encrypt":
                new_index = (index + key1) % 26
            elif mode == "decrypt":
                new_index = (index - key1) % 26
            result += permuted_alphabet[new_index]
        else:
            result += char

    return result


# Main program
while True:
    mode = input("Enter 'encrypt' or 'decrypt': ").lower()
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
        continue

    key1 = input("Enter the first key (1-25): ")
    if not key1.isdigit() or int(key1) < 1 or int(key1) > 25:
        print("Invalid key. Please enter a number between 1 and 25.")
        continue
    key1 = int(key1)

    key2 = input("Enter the second key (at least 7 letters): ")
    if len(key2) < 7 or not key2.isalpha():
        print("Invalid second key. Please enter at least 7 letters.")
        continue

    message = input("Enter the message: ")
    if not all(c.isalpha() or c.isspace() for c in message):
        print("Invalid message. Please use only letters and spaces.")
        continue

    result = caesar_cipher_with_permutation(message, key1, key2, mode)
    print(f"Result: {result}")