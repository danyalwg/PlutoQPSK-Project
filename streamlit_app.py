import streamlit as st
import numpy as np
import time
from math import sqrt
from encoder_decoder import hamming_encode, hamming_decode
from modulation import qpsk_modulate
from demodulation import qpsk_demodulate
from utils import string_to_binary, binary_to_string
from plots import (
    get_carrier_signals_figure, get_qpsk_signal_figure, 
    get_constellation_figure, get_ber_vs_snr_figure,
    get_impulse_plot, get_encoded_data_plot,
    get_received_signal_figure  # Import the new function
)
from pluto import create_pluto_instance, transmit_and_receive, pll, apply_agc, low_pass_filter

def main():
    st.title('QPSK Modulation and Demodulation')
    
    # Input text
    phrase = st.text_input("Enter text to modulate:")
    
    if st.button("Start Modulation"):
        if not phrase:
            st.error("Please enter a phrase.")
        else:
            progress_bar = st.progress(0)
            task_placeholder = st.empty()
            progress = 0
            max_progress = 100  # Maximum value for progress bar
            progress_step = max_progress // 10  # Step for each task

            # Converting text to binary
            task_placeholder.write("Converting text to binary...")
            binary_data = string_to_binary(phrase)
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Adding parity bits
            task_placeholder.write("Adding parity bits...")
            encoded_data = hamming_encode(np.array(binary_data))
            parity_indices = [i for i in range(len(encoded_data)) if i % 7 >= 4]
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Performing QPSK modulation
            task_placeholder.write("Performing QPSK modulation...")
            bit_rate = 500e6  # 500 Mbps
            tb = 1 / bit_rate  # Symbol duration
            fc = 500e6  # Carrier frequency
            sampling_rate = 500  # Sampling rate
            qpsk_signal, t, constellation_points = qpsk_modulate(encoded_data, tb, fc, sampling_rate)
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Perform Transmission and Reception using ADALM-PLUTO
            task_placeholder.write("Transmitting using ADALM-PLUTO...")
            sdr = create_pluto_instance()
            received_data, transmitted_data = transmit_and_receive(sdr, len(qpsk_signal), fc, fs=sdr.sample_rate)
            task_placeholder.write("Receiving using ADALM-PLUTO...")
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))

            # Apply signal processing
            task_placeholder.write("Automatic gain control...")
            received_data = apply_agc(received_data)
            received_data_corrected, freq_estimate = pll(received_data, sdr.sample_rate)
            task_placeholder.write("Low pass filtering...")
            received_data_filtered = low_pass_filter(received_data_corrected, cutoff_freq=0.1 * (sdr.sample_rate / 2), fs=sdr.sample_rate)
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))

            # Demodulating with a Hamming window
            task_placeholder.write("Demodulating with a Hamming window...")
            demod_binary = qpsk_demodulate(
                qpsk_signal, t, sqrt(2/tb) * np.cos(2 * np.pi * fc * t), 
                sqrt(2/tb) * np.sin(2 * np.pi * fc * t), len(encoded_data), sampling_rate)
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Decoding and removing parity bits
            task_placeholder.write("Decoding and removing parity bits...")
            decoded_data = hamming_decode(np.array(demod_binary))
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Converting binary back to text
            task_placeholder.write("Converting binary back to text...")
            received_phrase = binary_to_string(decoded_data[:len(binary_data)])
            progress += progress_step
            progress_bar.progress(min(progress, max_progress))
            time.sleep(2)

            # Clear the progress bar and task list
            progress_bar.empty()
            task_placeholder.empty()

            # Calculate and print the error details
            errors = np.sum(np.array(binary_data) != decoded_data[:len(binary_data)])
            bit_error_prob = errors / len(binary_data)
            bit_error_percentage = bit_error_prob * 100

            # Store results in session state to persist data across button clicks
            st.session_state['binary_data'] = binary_data
            st.session_state['encoded_data'] = encoded_data
            st.session_state['demod_binary'] = demod_binary
            st.session_state['decoded_data'] = decoded_data
            st.session_state['bit_error_percentage'] = bit_error_percentage
            st.session_state['phrase'] = phrase
            st.session_state['received_phrase'] = received_phrase
            st.session_state['constellation_points'] = constellation_points
            st.session_state['qpsk_signal'] = qpsk_signal
            st.session_state['t'] = t
            st.session_state['c1'] = sqrt(2/tb) * np.cos(2 * np.pi * fc * t)
            st.session_state['c2'] = sqrt(2/tb) * np.sin(2 * np.pi * fc * t)
            st.session_state['tb'] = tb
            st.session_state['snr_values'] = np.arange(0, 21, 2)
            st.session_state['ber_values'] = []

            # Calculate BER for each SNR value
            for snr_db in st.session_state['snr_values']:
                snr_linear = 10**(snr_db/10)
                noise_std_dev = sqrt(1/(2*snr_linear))
                noisy_qpsk = qpsk_signal + noise_std_dev * np.random.randn(*qpsk_signal.shape)

                # QPSK Demodulation
                demod_binary_snr = qpsk_demodulate(noisy_qpsk, t, st.session_state['c1'], st.session_state['c2'], len(encoded_data), sampling_rate)

                # Hamming decode the demodulated binary data
                decoded_data_snr = hamming_decode(np.array(demod_binary_snr))

                # Calculate Bit Error Rate (BER)
                errors_snr = np.sum(np.array(binary_data) != decoded_data_snr[:len(binary_data)])
                bit_error_rate = errors_snr / len(binary_data)
                st.session_state['ber_values'].append(bit_error_rate)

            # Display results
            st.write(f"**Original Phrase:** {st.session_state['phrase']}")
            st.write(f"**Received Phrase:** {st.session_state['received_phrase']}")
            st.write(f"**Number of errors:** {errors}")
            st.write(f"**Bit Error Probability:** {st.session_state['bit_error_percentage']:.2f}%")

            st.write("**Original Binary Data:**")
            st.text(st.session_state['binary_data'])
        
            st.write("**Encoded Binary Data (Parity bits in red):**")
            st.markdown(color_code_parity(st.session_state['encoded_data']), unsafe_allow_html=True)
        
            st.write("**Demodulated Binary Data:**")
            st.text(st.session_state['demod_binary'])
        
            st.write("**Decoded Binary Data:**")
            st.text(st.session_state['decoded_data'])
        
            # Display plots within Streamlit
            st.subheader('Plots')

            # Message data, represented as an impulse plot of zeros and ones
            st.pyplot(get_impulse_plot(st.session_state['binary_data'], title="Message Data (Impulse Plot)"))

            # Encoded data with impulses of parity bits color-coded
            st.pyplot(get_encoded_data_plot(st.session_state['encoded_data'], parity_indices=parity_indices, title="Encoded Data with Parity Bits"))

            # Carrier signal
            st.pyplot(get_carrier_signals_figure(st.session_state['t'], st.session_state['c1'], st.session_state['c2']))

            # QPSK Modulated Signal
            st.pyplot(get_qpsk_signal_figure(st.session_state['qpsk_signal'], st.session_state['t'], st.session_state['tb'], len(st.session_state['encoded_data']) // 2))

            # **New Plot**: Received Signal from ADALM-Pluto
            st.pyplot(get_received_signal_figure(st.session_state['t'], received_data_filtered))

            # Demodulated data (should match the encoded data)
            st.pyplot(get_impulse_plot(st.session_state['demod_binary'], title="Demodulated Data"))

            # Decoded data as pulses
            st.pyplot(get_impulse_plot(st.session_state['decoded_data'], title="Decoded Data"))
            
            # Constellation Diagram
            st.pyplot(get_constellation_figure(st.session_state['constellation_points']))

def color_code_parity(encoded_data):
    colored_text = ""
    for i in range(len(encoded_data)):
        if i % 7 < 4:
            colored_text += str(encoded_data[i])
        else:
            colored_text += f'<span style="color:red;">{encoded_data[i]}</span>'
    return colored_text

if __name__ == "__main__":
    main()
