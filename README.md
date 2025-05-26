# BB84-Quantum-Key-Distribution-Protocol-Simulator

# BB84 Quantum Key Distribution Protocol Simulator

This project provides an interactive simulation of the BB84 quantum key distribution protocol, demonstrating how quantum properties can be used to generate a secure encryption key between two parties (Alice and Bob), and how an eavesdropper (Eve) can be detected.

## Features

- Interactive web interface built with Streamlit
- Visual representation of qubit transmission and measurement
- Simulation of eavesdropping scenarios
- Real-time error rate calculation
- Dynamic key generation and validation
- Beautiful visualization of the quantum states and bases

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the interface to:
   - Adjust the number of qubits to simulate
   - Toggle eavesdropping on/off
   - Run the simulation and view results
   - Analyze the visualization of the quantum transmission
   - View the generated key (if secure)

## Understanding the Visualization

The visualization shows:
- Blue squares: represent bit value 0
- Red squares: represent bit value 1
- Plus (+) symbols: rectilinear basis
- Cross (x) symbols: diagonal basis
- Green highlighted areas: matching bases between Alice and Bob
- Top row: Alice's bits and bases
- Bottom row: Bob's bits and bases

## Protocol Steps

1. Alice generates random bits and random bases
2. Alice encodes each bit in its corresponding basis
3. Bob randomly chooses measurement bases
4. Bob measures each received qubit
5. Alice and Bob compare bases (sifting)
6. Error rate calculation on a sample
7. Final key generation if the channel is secure

## Security Features

- Automatic detection of eavesdropping through error rate analysis
- Threshold-based security validation (default 15% error rate)
- Secure key generation only when the channel is deemed secure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
