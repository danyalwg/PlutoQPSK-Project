import numpy as np

def qpsk_demodulate(qpsk_signal, t, c1, c2, num_bits, sampling_rate=500):
    demod_binary = []

    for i in range(0, num_bits, 2):
        x1 = np.sum(c1 * qpsk_signal[i // 2])
        x2 = np.sum(c2 * qpsk_signal[i // 2])

        if x1 > 0 and x2 > 0:
            demod_binary.extend([1, 1])
        elif x1 > 0 and x2 < 0:
            demod_binary.extend([1, 0])
        elif x1 < 0 and x2 < 0:
            demod_binary.extend([0, 0])
        elif x1 < 0 and x2 > 0:
            demod_binary.extend([0, 1])

    return demod_binary
