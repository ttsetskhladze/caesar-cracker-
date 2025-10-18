#!/usr/bin/env python3
"""
caesar_crack.py
Brute-force + frequency-analysis helper for Caesar cipher.
Usage: python3 caesar_crack.py
"""

import string
from collections import Counter

CIPHER = "Hvs Eiwqy Pfckb Tcl Xiadg Cjsf Hvs Zonm Rcu."  # change if needed

ENGLISH_FREQ_ORDER = "etaoinshrdlcumwfgypbvkjxqz"

def caesar_shift(text, shift):
    out = []
    for ch in text:
        if ch.isalpha():
            alpha = string.ascii_lowercase if ch.islower() else string.ascii_uppercase
            idx = alpha.index(ch)
            out.append(alpha[(idx + shift) % 26])
        else:
            out.append(ch)
    return "".join(out)

def brute_force(cipher):
    return [(s, caesar_shift(cipher, s)) for s in range(26)]

def score_text_by_freq_and_words(text):
    text_l = text.lower()
    letters = [c for c in text_l if c.isalpha()]
    if not letters:
        return 0
    freq = Counter(letters)
    most_common = [p[0] for p in freq.most_common(10)]
    score = 0
    for i, ch in enumerate(most_common):
        if ch in ENGLISH_FREQ_ORDER[:10]:
            score += (11 - i)
    for w, pts in [(" the ", 40), (" and ", 20), (" of ", 15), (" to ", 10), (" is ", 10)]:
        if w in text_l:
            score += pts
    if text and text[0].isupper():
        score += 5
    return score

def find_best(cipher, top_n=5):
    candidates = brute_force(cipher)
    scored = [(shift, txt, score_text_by_freq_and_words(txt)) for shift, txt in candidates]
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:top_n]

def main():
    print("Ciphertext:\n", CIPHER, "\n")
    print("Brute-force results (shift -> plaintext):\n")
    for shift, plaintext in brute_force(CIPHER):
        print(f"shift={shift:2d}: {plaintext}")
    print("\nTop candidates by scoring:\n")
    for shift, txt, score in find_best(CIPHER, top_n=6):
        print(f"shift={shift:2d} (score={score:3d}): {txt}")
    best = find_best(CIPHER, top_n=1)[0]
    print("\nBest guess:")
    print(f"shift = {best[0]} -> {best[1]}")

if __name__ == "__main__":
    main()
