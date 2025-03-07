import matplotlib.pyplot as plt
import numpy as np

def get_carrier_signals_figure(t, c1, c2):
    fig, ax = plt.subplots()
    ax.plot(t, c1, label='Cosine Carrier (In-phase)')
    ax.plot(t, c2, label='Sine Carrier (Quadrature)')
    ax.set_title('Carrier Signals')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()
    return fig

def get_qpsk_signal_figure(qpsk_signal, t, tb, num_symbols):
    fig, ax = plt.subplots()
    for i in range(num_symbols):
        ax.plot(t + i * tb, qpsk_signal[i])
    ax.set_title('QPSK Modulated Signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    return fig

def get_constellation_figure(constellation_points):
    fig, ax = plt.subplots()
    constellation_points = np.array(constellation_points)
    ax.scatter(constellation_points[:, 0], constellation_points[:, 1], color='blue')
    
    # Adding the plus sign to divide the diagram into 4 quadrants and changing its color to red
    ax.axhline(0, color='red', lw=1)  # Horizontal line at y=0
    ax.axvline(0, color='red', lw=1)  # Vertical line at x=0

    ax.set_title('QPSK Constellation Diagram')
    ax.set_xlabel('In-phase')
    ax.set_ylabel('Quadrature')
    ax.grid(True)
    return fig

def get_ber_vs_snr_figure(snr_values, ber_values):
    fig, ax = plt.subplots()
    ax.plot(snr_values, ber_values, marker='o')
    ax.set_title('BER vs. SNR')
    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('Bit Error Rate (BER)')
    ax.grid(True)
    return fig

def get_impulse_plot(binary_data, parity_indices=None, title="Impulse Plot"):
    fig, ax = plt.subplots()
    if parity_indices is None:
        parity_indices = []
    for i in range(len(binary_data)):
        color = 'r' if i in parity_indices else 'b'  # 'r' for red, 'b' for blue
        ax.stem([i], [binary_data[i]], linefmt=color+'-', markerfmt=color+'o', basefmt=" ")
    ax.set_title(title)
    ax.set_xlabel('Bit Index')
    ax.set_ylabel('Bit Value')
    ax.grid(True)
    return fig

def get_received_signal_figure(t, received_data_filtered):
    fig, ax = plt.subplots()
    common_length = min(len(t), len(received_data_filtered))
    ax.plot(t[:common_length], 20 * np.log10(np.abs(received_data_filtered[:common_length]) + 1e-12), label="Received Signal", linestyle='--')
    ax.set_title('Received Signal from ADALM-Pluto')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [dB]')
    ax.grid(True)
    ax.legend()
    return fig


def get_encoded_data_plot(encoded_data, parity_indices=None, title="Encoded Data with Parity Bits"):
    return get_impulse_plot(encoded_data, parity_indices=parity_indices, title=title)
