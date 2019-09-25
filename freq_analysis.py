# freq_analysis.py
# Generates frequency analysis graphs

from ciphertexts import CIPHERTEXTS
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

FILE_PREFIX = "freq_analysis"
ASCII_UPPERCASE = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

for idx, ciphertext in enumerate(CIPHERTEXTS):
    freq_analysis = defaultdict(int)
    for c in ciphertext.value:
        freq_analysis[c] += 1
    x = np.array(ASCII_UPPERCASE)
    y = np.array([freq_analysis[c] for c in x])
    fig, ax = plt.subplots()
    ax.bar(x, y)
    plt.xlabel("Letter")
    plt.ylabel("Frequency")
    plt.title("Frequency Analysis for Ciphertext %d" % (idx + 1))
    plt_file = "%s_ciphertext%d.png" % (FILE_PREFIX, idx + 1)
    plt.savefig(plt_file)
    print("Saved plot to %s." % plt_file)
