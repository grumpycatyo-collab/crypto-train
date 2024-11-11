import streamlit as st
import sys


def validate_input(text):
    return all(c.isalpha() or c.isspace() for c in text)


def prepare_text(text):
    return ''.join(c.upper() for c in text if not c.isspace())


def validate_key(key):
    if len(key) < 7:
        return False
    return all(c.isalpha() for c in key)


def char_to_number(char):
    romanian_alphabet = {
        'A': 0, 'Ă': 1, 'Â': 2, 'B': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7,
        'G': 8, 'H': 9, 'I': 10, 'Î': 11, 'J': 12, 'K': 13, 'L': 14, 'M': 15,
        'N': 16, 'O': 17, 'P': 18, 'Q': 19, 'R': 20, 'S': 21, 'Ș': 22, 'T': 23,
        'Ț': 24, 'U': 25, 'V': 26, 'W': 27, 'X': 28, 'Y': 29, 'Z': 30
    }
    return romanian_alphabet[char.upper()]


def number_to_char(num):
    romanian_alphabet = [
        'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'Î', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Ș', 'T', 'Ț', 'U',
        'V', 'W', 'X', 'Y', 'Z'
    ]
    return romanian_alphabet[num]


def vigenere_cipher(text, key, encrypt=True):
    if not validate_input(text):
        return "Eroare: Textul poate conține doar litere și spații!"

    if not validate_key(key):
        return "Eroare: Cheia trebuie să aibă cel puțin 7 caractere și să conțină doar litere!"

    text = prepare_text(text)
    key = prepare_text(key)
    result = ""

    for i in range(len(text)):
        text_num = char_to_number(text[i])
        key_num = char_to_number(key[i % len(key)])

        if encrypt:
            new_num = (text_num + key_num) % 31
        else:
            new_num = (text_num - key_num + 31) % 31

        result += number_to_char(new_num)

    return result


st.title("Algoritmul Vigenere pentru limba română (31 litere)")


tab1, tab2 = st.tabs(["Criptare", "Decriptare"])

with tab1:
    st.header("Criptare")


    key_encrypt = st.text_input("Introduceți cheia (minim 7 caractere):", key="key_encrypt")
    text_encrypt = st.text_area("Introduceți textul pentru criptare:", key="text_encrypt")

    if st.button("Criptează", key="encrypt_button"):
        if key_encrypt and text_encrypt:
            result = vigenere_cipher(text_encrypt, key_encrypt, True)
            st.success(f"Text criptat: {result}")
        else:
            st.error("Vă rugăm să completați toate câmpurile!")

with tab2:
    st.header("Decriptare")

    key_decrypt = st.text_input("Introduceți cheia (minim 7 caractere):", key="key_decrypt")
    text_decrypt = st.text_area("Introduceți textul pentru decriptare:", key="text_decrypt")

    if st.button("Decriptează", key="decrypt_button"):
        if key_decrypt and text_decrypt:
            result = vigenere_cipher(text_decrypt, key_decrypt, False)
            st.success(f"Text decriptat: {result}")
        else:
            st.error("Vă rugăm să completați toate câmpurile!")

with st.expander("Vezi alfabetul românesc utilizat"):
    st.write("""
    Alfabetul românesc folosit (31 litere):
    A, Ă, Â, B, C, D, E, F, G, H, I, Î, J, K, L, M, N, O, P, Q, R, S, Ș, T, Ț, U, V, W, X, Y, Z
    """)

# Add footer
st.markdown("---")
st.markdown("Creat pentru criptarea și decriptarea textelor în limba română")