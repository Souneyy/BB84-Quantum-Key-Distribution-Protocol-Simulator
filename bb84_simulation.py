import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from typing import List, Tuple, Dict
import random

class BB84Simulator:
    def __init__(self, num_qubits: int = 1000, eavesdropping: bool = False):
        # Input validation
        if num_qubits < 10:
            raise ValueError("Number of qubits must be at least 10")
        if not isinstance(num_qubits, int):
            raise TypeError("Number of qubits must be an integer")
        if not isinstance(eavesdropping, bool):
            raise TypeError("Eavesdropping must be a boolean value")

        self.num_qubits = num_qubits
        self.eavesdropping = eavesdropping
        self.bases = ['+', 'x']  # Rectilinear and diagonal bases
        
        # Initialize data structures
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_measurements = []
        self.eve_bases = []
        self.eve_measurements = []
        self.final_key = []
        self.error_rate = 0.0
        self.sifted_indices = []
        
        # History for visualization
        self.history = {
            'step': [],
            'description': [],
            'alice_bits': [],
            'alice_bases': [],
            'bob_bases': [],
            'bob_bits': [],
            'matched': []
        }

    def generate_random_bits(self, size: int) -> List[int]:
        try:
            return [random.randint(0, 1) for _ in range(size)]
        except Exception as e:
            raise RuntimeError(f"Error generating random bits: {str(e)}")

    def generate_random_bases(self, size: int) -> List[str]:
        try:
            return [random.choice(self.bases) for _ in range(size)]
        except Exception as e:
            raise RuntimeError(f"Error generating random bases: {str(e)}")

    def measure_qubit(self, bit: int, send_basis: str, measure_basis: str) -> int:
        # Input validation
        if bit not in [0, 1]:
            raise ValueError("Bit value must be 0 or 1")
        if send_basis not in self.bases or measure_basis not in self.bases:
            raise ValueError("Invalid basis")

        if send_basis == measure_basis:
            # If measuring in the correct basis, we get the correct bit
            return bit
        else:
            # If measuring in the wrong basis, we get a random result
            return random.randint(0, 1)

    def simulate(self):
        try:
            # Step 1: Alice generates random bits and bases
            self.alice_bits = self.generate_random_bits(self.num_qubits)
            self.alice_bases = self.generate_random_bases(self.num_qubits)
            
            # Step 2: Bob chooses random bases
            self.bob_bases = self.generate_random_bases(self.num_qubits)
            
            # Step 3: Simulate transmission and measurement
            if self.eavesdropping:
                # Eve intercepts and measures
                self.eve_bases = self.generate_random_bases(self.num_qubits)
                self.eve_measurements = []
                eve_resend_bits = []  # The bits Eve will resend to Bob
                
                # Eve's measurements and resending
                for i in range(self.num_qubits):
                    # Eve measures Alice's qubit
                    eve_measurement = self.measure_qubit(
                        self.alice_bits[i],
                        self.alice_bases[i],
                        self.eve_bases[i]
                    )
                    self.eve_measurements.append(eve_measurement)
                    
                    # Eve resends the qubit in her basis
                    # This is crucial: Eve must resend in HER basis, not Alice's
                    # This is what causes the errors even when Bob measures in Alice's basis
                    eve_resend_bits.append(eve_measurement)
                
                # Bob measures Eve's forwarded qubits
                self.bob_measurements = [
                    self.measure_qubit(eve_bit, eve_basis, bob_basis)
                    for eve_bit, eve_basis, bob_basis in zip(eve_resend_bits, self.eve_bases, self.bob_bases)
                ]
            else:
                # Direct transmission to Bob
                self.bob_measurements = [
                    self.measure_qubit(bit, alice_basis, bob_basis)
                    for bit, alice_basis, bob_basis in zip(self.alice_bits, self.alice_bases, self.bob_bases)
                ]
            
            # Record state for visualization
            self._record_state()
            
            # Step 4: Sifting - Keep only bits where bases match
            self.sifted_indices = [
                i for i in range(self.num_qubits)
                if self.alice_bases[i] == self.bob_bases[i]
            ]
            
            if not self.sifted_indices:
                raise RuntimeError("No matching bases found after sifting")
            
            self.sifted_key_alice = [self.alice_bits[i] for i in self.sifted_indices]
            self.sifted_key_bob = [self.bob_measurements[i] for i in self.sifted_indices]
            
            # Step 5: Error detection (using 25% of bits)
            sample_size = max(1, len(self.sifted_indices) // 4)
            sample_indices = random.sample(range(len(self.sifted_indices)), sample_size)
            
            errors = sum(
                self.sifted_key_alice[i] != self.sifted_key_bob[i]
                for i in sample_indices
            )
            
            self.error_rate = errors / sample_size if sample_size > 0 else 1.0
            
            # Remove sampled bits from final key
            final_key_indices = [i for i in range(len(self.sifted_indices)) if i not in sample_indices]
            self.final_key = [self.sifted_key_alice[i] for i in final_key_indices]
            
            return {
                'total_qubits': self.num_qubits,
                'sifted_bits': len(self.sifted_indices),
                'error_rate': self.error_rate,
                'final_key_length': len(self.final_key),
                'final_key': ''.join(map(str, self.final_key)) if self.error_rate < 0.15 else None,
                'secure': self.error_rate < 0.15
            }
        except Exception as e:
            raise RuntimeError(f"Error during simulation: {str(e)}")

    def _record_state(self):
        """Record the current state for visualization"""
        try:
            for i in range(min(20, self.num_qubits)):  # Record first 20 qubits for visualization
                self.history['step'].append(i)
                self.history['description'].append(f'Qubit {i+1}')
                self.history['alice_bits'].append(self.alice_bits[i])
                self.history['alice_bases'].append(self.alice_bases[i])
                self.history['bob_bases'].append(self.bob_bases[i])
                self.history['bob_bits'].append(self.bob_measurements[i])
                self.history['matched'].append(self.alice_bases[i] == self.bob_bases[i])
        except Exception as e:
            raise RuntimeError(f"Error recording state: {str(e)}")

    def get_visualization_data(self) -> pd.DataFrame:
        """Return the history as a pandas DataFrame for visualization"""
        try:
            return pd.DataFrame(self.history)
        except Exception as e:
            raise RuntimeError(f"Error creating visualization data: {str(e)}") 