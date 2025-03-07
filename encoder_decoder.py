import numpy as np

def hamming_encode(data):
    # Pad the data if it's not a multiple of 4 bits
    if len(data) % 4 != 0:
        padding_length = 4 - (len(data) % 4)
        data = np.concatenate((data, np.zeros(padding_length, dtype=int)))
    
    G = np.array([[1, 0, 0, 0, 0, 1, 1],
                  [0, 1, 0, 0, 1, 0, 1],
                  [0, 0, 1, 0, 1, 1, 0],
                  [0, 0, 0, 1, 1, 1, 1]])
    
    encoded = np.dot(data.reshape(-1, 4), G) % 2
    return encoded.flatten()

def hamming_decode(encoded_data):
    H = np.array([[1, 0, 1, 0, 1, 0, 1], 
                  [0, 1, 1, 0, 0, 1, 1], 
                  [0, 0, 0, 1, 1, 1, 1]])
    
    decoded = []
    for i in range(0, len(encoded_data), 7):
        syndrome = np.dot(H, encoded_data[i:i+7]) % 2
        syndrome_decimal = int(''.join(map(str, syndrome)), 2)
        if syndrome_decimal != 0:
            encoded_data[i+syndrome_decimal-1] ^= 1
        decoded.extend([encoded_data[i], encoded_data[i+1], encoded_data[i+2], encoded_data[i+3]])
    return np.array(decoded)
