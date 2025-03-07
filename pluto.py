
import os
import time
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal.windows import hamming
from scipy.signal import lfilter, welch
import matplotlib.pyplot as plt
import adi

def pll(input_signal, fs, loop_bandwidth=0.01):
    phase_estimate = 0.0
    output_signal = np.zeros_like(input_signal, dtype=complex)
    freq_estimate = 0.0
    Kp = 2 * np.pi * loop_bandwidth
    Ki = (Kp ** 2) / 4
    integrator = 0.0
    
    for i in range(len(input_signal)):
        phase_error = np.angle(input_signal[i] * np.exp(-1j * phase_estimate))
        integrator += Ki * phase_error
        freq_estimate = integrator + Kp * phase_error
        phase_estimate += freq_estimate / fs
        output_signal[i] = input_signal[i] * np.exp(-1j * phase_estimate)
    
    return output_signal, freq_estimate

def low_pass_filter(data, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def apply_agc(signal, target_level=0.1):
    max_val = np.max(np.abs(signal))
    gain = target_level / max_val
    return signal * gain

def create_pluto_instance(uri="usb:1.5.5"):
    sdr = adi.Pluto(uri=uri)
    sdr.rx_rf_bandwidth = 4000000
    sdr.sample_rate = 6000000
    sdr.rx_lo = 500000000  # 500 MHz Local Oscillator
    sdr.tx_lo = 500000000  # 500 MHz Local Oscillator
    sdr.tx_cyclic_buffer = True
    sdr.tx_hardwaregain_chan0 = -10
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = 50

    sdr.rx_enabled_channels = [0]
    sdr.tx_enabled_channels = [0]
    return sdr

def transmit_and_receive(sdr, N, fc, fs):
    ts = 1 / float(fs)
    t = np.arange(0, N * ts, ts)  # 1 second worth of time steps
    sine_wave = np.cos(2 * np.pi * fc * t) * 2**14 * hamming(N)
    iq = sine_wave + 1j * sine_wave

    print(f"Transmitting {fc / 1e6} MHz Sine waveform for 1 second...")
    sdr.tx(iq)

    # Allow signal to stabilize
    time.sleep(1)

    # Receive data
    received_data = sdr.rx()

    # Stop transmission
    sdr.tx_destroy_buffer()

    return received_data, iq[:len(received_data)]
