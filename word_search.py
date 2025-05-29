# -*- coding: utf-8 -*-
import streamlit as st
import re
from collections import Counter

st.title("Wyszukiwarka słów")

# Step 1: Get word length
word_length = st.number_input("Wpisz długość słowa", min_value=3, max_value=30, step=1)

# Step 2: Build pattern input grid
st.markdown("### Wpisz znane litery (pozostaw puste jeśli nieznana)")
letters = []
cols = st.columns(word_length)

for i in range(word_length):
    char = cols[i].text_input(f"{i+1}", max_chars=1, key=f"char_{i}")
    letters.append(char.upper() if char else "?")

# Step 3: Additional filters
include_letters = st.text_input("Musi zawierać litery (np. atn, aatt)").upper().strip()
exclude_letters = st.text_input("Nie może zawierać liter (np. xyz)").upper().strip()

# Step 4: Create regex
pattern = "".join(letters)
regex_pattern = "^" + pattern.replace("?", ".") + "$"
regex = re.compile(regex_pattern)

# Step 5: Load dictionary and match
try:
    with open("dictionary.txt", encoding="utf-8") as f:
        words = [word.strip().upper() for word in f if len(word.strip()) == word_length]
except FileNotFoundError:
    st.error("dictionary.txt not found. Please place it in the same folder.")
    words = []

# Step 6: Apply filters
matches = []
include_counter = Counter(include_letters)

for word in words:
    if not regex.match(word):
        continue
    # Must include exact number of letters
    word_counter = Counter(word)
    if any(word_counter[char] < count for char, count in include_counter.items()):
        continue
    # Must exclude these letters
    if any(char in word for char in exclude_letters):
        continue
    matches.append(word)

# Step 7: Display results
if matches:
    st.success(f"{len(matches)} słów znaleziono:")
    st.text(", ".join(matches))  # Single line, easy to copy
else:
    st.warning("Nic nie znaleziono.")
