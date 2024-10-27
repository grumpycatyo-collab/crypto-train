import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def analyze_frequency(text):
    # Numără doar literele
    letters = [c.lower() for c in text if c.isalpha()]
    freq = Counter(letters)

    # Sortează după frecvență
    sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

    # Calculează procentajele
    total = sum(freq.values())
    percentages = {k: (v / total) * 100 for k, v in sorted_freq.items()}

    return percentages


def create_substitution_dict():
    return {chr(i): chr(i) for i in range(97, 123)}  # a-z -> a-z


def apply_substitution(text, sub_dict):
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_lower = char.lower()
            new_char = sub_dict.get(char_lower, char_lower)
            result += new_char.upper() if is_upper else new_char
        else:
            result += char
    return result


# Streamlit interface
st.title("Analiză Frecvență și Decodare Text Criptat")

# Input text area
encrypted_text = st.text_area("Introduceți textul criptat:", height=200)

if encrypted_text:
    # Analyze frequency
    freq = analyze_frequency(encrypted_text)

    # Display frequency analysis
    st.subheader("Analiza Frecvenței")

    # Create DataFrame for better visualization
    df = pd.DataFrame(list(freq.items()), columns=['Litera', 'Frecvența (%)'])
    st.dataframe(df)

    # Plot frequency distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.bar(freq.keys(), freq.values())
    plt.title("Distribuția Frecvenței Literelor")
    plt.xlabel("Litere")
    plt.ylabel("Frecvența (%)")
    st.pyplot(fig)

    # Substitution interface
    st.subheader("Substituție")

    # Create two columns
    col1, col2 = st.columns(2)

    # Initialize substitution dictionary in session state
    if 'sub_dict' not in st.session_state:
        st.session_state.sub_dict = create_substitution_dict()

    # Create input fields for each letter
    with col1:
        st.write("Literă criptată -> Literă originală")
        for i in range(97, 110):  # a-m
            char = chr(i)
            new_char = st.text_input(f"{char} ->",
                                     value=st.session_state.sub_dict[char],
                                     key=char,
                                     max_chars=1)
            st.session_state.sub_dict[char] = new_char.lower() if new_char else char

    with col2:
        st.write("Literă criptată -> Literă originală")
        for i in range(110, 123):  # n-z
            char = chr(i)
            new_char = st.text_input(f"{char} ->",
                                     value=st.session_state.sub_dict[char],
                                     key=char,
                                     max_chars=1)
            st.session_state.sub_dict[char] = new_char.lower() if new_char else char

    # Apply substitution and show result
    if st.button("Aplică Substituția"):
        decoded_text = apply_substitution(encrypted_text, st.session_state.sub_dict)
        st.subheader("Text Decodat")
        st.text_area("Rezultat:", value=decoded_text, height=200)

    # Reset button
    if st.button("Resetează Substituția"):
        st.session_state.sub_dict = create_substitution_dict()
        st.experimental_rerun()