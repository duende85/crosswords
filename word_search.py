# -*- coding: utf-8 -*-
"""
Created on Thu May 29 09:58:47 2025

@author: igorw
"""

# streamlit_app.py
import streamlit as st
import re

st.title("Word Pattern Matcher")

# Step 1: Get word length
word_length = st.number_input("Wpisz długosc slowa", min_value=3, max_value=30, step=1)

# Step 2: Build pattern input grid
st.markdown("### Wpisz znane litery")
letters = []
cols = st.columns(word_length)

for i in range(word_length):
    char = cols[i].text_input(f"{i+1}", max_chars=1, key=f"char_{i}")
    letters.append(char.upper() if char else "?")

# Step 3: Create regex
pattern = "".join(letters)
regex_pattern = "^" + pattern.replace("?", ".") + "$"
regex = re.compile(regex_pattern)

# Step 4: Load dictionary and match
try:
    with open("dictionary.txt", encoding="utf-8") as f:
        matches = [word.strip() for word in f if regex.match(word.strip().upper())]
except FileNotFoundError:
    st.error("dictionary.txt not found. Please place it in the same folder.")
    matches = []

# Step 5: Display results
if matches:
    st.success(f"{len(matches)} słów znaleziono:")
    for word in matches:
        st.write(word)
else:
    st.warning("Nic.")
