import numpy as np
import matplotlib.pyplot as plt
import os

def string_to_binary(phrase):
    binary_string = ''.join(format(ord(char), '08b') for char in phrase)
    return [int(bit) for bit in binary_string]

def binary_to_string(binary_data):
    binary_string = ''.join(str(bit) for bit in binary_data)
    chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
    return ''.join(chars)

def save_plot(fig, filename):
    if not os.path.exists('plots'):
        os.makedirs('plots')
    fig.savefig(f'plots/{filename}.png')
    plt.show()
