ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def caesar_cipher(text, key, mode):
    n = len(ALPHABET)
    result = ""
    text = text.upper().replace(" ", "")

    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            new_index = 0

            if mode == "encrypt":
                new_index = (index + key) % n
            elif mode == "decrypt":
                new_index = (index - key) % n

            result += ALPHABET[new_index]
        else:
            result += char

    return result


while True:
    mode = input("Enter 'encrypt' or 'decrypt': ").lower()
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
        continue

    key = input("Enter the key (1-25): ")
    if not key.isdigit() or int(key) < 1 or int(key) > 25:
        print("Invalid key. Please enter a number between 1 and 25.")
        continue
    key = int(key)

    message = input("Enter the message: ")
    if not all(c.isalpha() or c.isspace() for c in message):
        print("Invalid message. Please use only letters and spaces.")
        continue

    result = caesar_cipher(message, key, mode)
    print(f"Result: {result}")

    if input("Do you want to continue? (y/n): ").lower() != 'y':
        break