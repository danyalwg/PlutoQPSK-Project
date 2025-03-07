import numpy as np
from math import sqrt

def qpsk_modulate(encoded_data, tb, fc=500e6, sampling_rate=500):
    t = np.linspace(0, tb, sampling_rate)
    c1 = sqrt(2/tb) * np.cos(2 * np.pi * fc * t)  # Cosine carrier (in-phase)
    c2 = sqrt(2/tb) * np.sin(2 * np.pi * fc * t)  # Sine carrier (quadrature)
    
    num_bits = len(encoded_data)
    qpsk = np.zeros((num_bits // 2, sampling_rate))
    constellation_points = []

    for i in range(0, num_bits, 2):
        m_s1 = np.ones(sampling_rate) if encoded_data[i] == 1 else -np.ones(sampling_rate)
        m_s2 = np.ones(sampling_rate) if encoded_data[i+1] == 1 else -np.ones(sampling_rate)

        qpsk[i // 2] = c1 * m_s1 + c2 * m_s2  # QPSK modulated signal
        constellation_points.append([m_s1[0], m_s2[0]])

    return qpsk, t, constellation_points
