# PlutoQPSK-Project

## Overview

PlutoQPSK-Project is an advanced digital communications repository that demonstrates the complete QPSK (Quadrature Phase Shift Keying) signal chain using ADALM-PLUTO SDR hardware. This project walks you through every step—from converting plain text into binary, applying Hamming error correction, modulating the binary data using QPSK, transmitting and receiving signals via the PlutoSDR, and finally demodulating and decoding the data back into text. With extensive visualization and an interactive web interface powered by Streamlit, this repository serves as both an educational resource and a testbed for modern wireless communication systems.

## Background

### QPSK Modulation
Quadrature Phase Shift Keying (QPSK) is a widely used modulation scheme that conveys data by changing the phase of a carrier wave. In QPSK, two bits are represented by one symbol, allowing for efficient use of bandwidth. The modulation process involves:
- Mapping binary data to specific phase shifts.
- Generating two carrier signals (in-phase and quadrature components).
- Combining these carriers to produce the modulated signal.

### Hamming Error Correction
Hamming codes are a class of error-correcting codes that add parity bits to the data to detect and correct single-bit errors. In this project:
- The input binary data is padded and encoded with extra parity bits.
- The decoding process identifies and corrects errors, ensuring the integrity of the transmitted message.

### ADALM-PLUTO SDR Integration
ADALM-PLUTO is a versatile and cost-effective software-defined radio (SDR) platform. In this project:
- The PlutoSDR is used for real-time transmission and reception of modulated signals.
- Advanced signal processing techniques, such as Automatic Gain Control (AGC) and Phase-Locked Loop (PLL), are employed to enhance signal quality.

## Features

- **Text to Binary Conversion:**  
  Convert text input into binary form and revert it back to text after processing.

- **Hamming Encoding & Decoding:**  
  Integrate Hamming error correction to add redundancy and improve transmission reliability.

- **QPSK Modulation & Demodulation:**  
  Modulate binary data using QPSK, transmit using PlutoSDR, and demodulate the received signal to recover the data.

- **Advanced Visualization:**  
  Generate detailed plots including carrier signal waveforms, QPSK modulated signal, impulse plots, constellation diagrams, and BER vs. SNR graphs.

- **Interactive Web Interface:**  
  A full-featured Streamlit application lets you input text, visualize signal processing steps, and see real-time performance metrics.

- **SDR Device Detection:**  
  Quickly scan and identify available PlutoSDR devices for seamless integration.

## Directory Structure

The repository is organized to separate different functionalities and ensure modularity:

- **utils.py:**  
  Utility functions for binary conversion, saving plots, and other general-purpose tasks.

- **demodulation.py:**  
  Functions to perform QPSK demodulation, processing the received signal to extract binary data.

- **encoder_decoder.py:**  
  Implements Hamming encoding and decoding to provide error correction capabilities.

- **find_address.py:**  
  A script to scan for and display available PlutoSDR devices, ensuring proper connectivity.

- **modulation.py:**  
  Contains the QPSK modulation functions that map binary data to phase-modulated signals.

- **plots.py:**  
  Provides a suite of functions to create various plots for analysis and debugging, including impulse plots and constellation diagrams.

- **pluto.py:**  
  Sets up and configures the PlutoSDR instance, handling the basics of transmission and reception.

- **pluto_plots.py:**  
  An enhanced version of PlutoSDR interfacing with additional signal processing and plotting capabilities.

- **streamlit_app.py:**  
  An interactive Streamlit application that demonstrates the entire signal chain from modulation to demodulation with real-time visualization.

## Installation Instructions

### Cloning the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/danyalwg/PlutoQPSK-Project.git
```

Then navigate into the project directory:

```bash
cd PlutoQPSK-Project
```

### Installing Dependencies

Install the necessary Python packages using pip3. This project depends on:

- numpy
- matplotlib
- scipy
- streamlit
- adi

Run the following command:

```bash
pip3 install numpy matplotlib scipy streamlit adi
```

*Tip:* If you encounter any issues with pip3, ensure your pip3 is updated:

```bash
pip3 install --upgrade pip
```

## Usage Instructions

### Running the Streamlit Application

The interactive Streamlit app offers a step-by-step demonstration of the modulation and demodulation process:

```bash
streamlit run streamlit_app.py
```

Upon launching, the app will open in your default browser. Follow the on-screen instructions to input your text, initiate modulation, and observe the various signal processing steps through dynamic plots.

### Running Individual Scripts

Explore specific functionalities by running the following scripts:

- **Modulation Demonstration:**

  To test QPSK modulation independently, run:

  ```bash
  python3 modulation.py
  ```

- **PlutoSDR Device Detection:**

  To check for connected PlutoSDR devices, run:

  ```bash
  python3 find_address.py
  ```

- **PlutoSDR Transmission/Reception:**

  For a full demonstration of signal transmission and reception using PlutoSDR, execute:

  ```bash
  python3 pluto.py
  ```

  Alternatively, for an enhanced version with detailed plotting:

  ```bash
  python3 pluto_plots.py
  ```

## Detailed Project Explanation

### Signal Processing Chain

1. **Text Conversion:**  
   The process begins with converting your input text into binary format using functions defined in `utils.py`. Each character is represented by its ASCII binary code.

2. **Hamming Encoding:**  
   Before modulation, the binary data is encoded with Hamming codes (via `encoder_decoder.py`) to introduce redundancy. This allows the system to detect and correct single-bit errors during transmission.

3. **QPSK Modulation:**  
   The binary data is grouped into pairs of bits, and each pair is mapped to a unique phase. The `modulation.py` script generates two carrier signals (cosine and sine) to represent the in-phase and quadrature components. These are combined to form the QPSK modulated signal.

4. **Transmission & Reception:**  
   The modulated signal is transmitted using the ADALM-PLUTO SDR as configured in `pluto.py` and `pluto_plots.py`. The received signal undergoes:
   - **Automatic Gain Control (AGC):** Normalizes the signal amplitude.
   - **Phase-Locked Loop (PLL):** Corrects any phase offsets introduced during transmission.
   - **Low-Pass Filtering:** Removes high-frequency noise.

5. **Demodulation & Decoding:**  
   The `demodulation.py` script processes the received signal by correlating it with the known carrier signals, thereby retrieving the original binary data. The Hamming decoding step in `encoder_decoder.py` then corrects any detected errors before converting the binary data back to text.

### Visualization & Analysis

- **Carrier and Signal Plots:**  
  Visualizations generated by `plots.py` illustrate the carrier waveforms, modulated signals, and the resulting constellation diagram, offering insights into the modulation process.

- **Impulse & Error Analysis:**  
  Impulse plots display binary data at various stages (original, encoded, demodulated, and decoded), making it easy to spot discrepancies and assess the effectiveness of error correction.

- **BER vs. SNR Analysis:**  
  The Streamlit app computes the Bit Error Rate (BER) across a range of Signal-to-Noise Ratio (SNR) values, demonstrating the system’s robustness under different noise conditions.

## Troubleshooting

- **Device Connectivity:**  
  If PlutoSDR devices are not detected, verify that the hardware is correctly connected. Use `find_address.py` to ensure that the devices are recognized by your system.

- **Dependency Issues:**  
  Module import errors usually indicate missing packages. Confirm that all dependencies are installed with the command provided above.

- **Signal Quality Problems:**  
  Adjust filtering and gain parameters in `pluto.py` or `pluto_plots.py` if the received signal quality is suboptimal. Experiment with different settings to optimize performance.

## Future Improvements

- **Enhanced Error Correction:**  
  Investigate the integration of more robust error-correcting codes beyond Hamming.

- **Advanced Signal Processing:**  
  Implement adaptive equalization and improved noise reduction techniques to further enhance signal quality.

- **Hardware Expansion:**  
  Extend support for additional SDR platforms and hardware configurations.

- **UI Enhancements:**  
  Enrich the Streamlit interface with real-time plotting updates, additional control elements, and detailed logging for improved user experience.

## Conclusion

PlutoQPSK-Project is a complete, detailed framework for exploring digital communications using QPSK modulation and ADALM-PLUTO SDR hardware. It provides both theoretical background and practical implementations, making it an excellent resource for students, hobbyists, and professionals in the field. Contributions, issues, and suggestions are welcome to continually improve the project.

Happy coding and exploring the intricacies of digital communications!
