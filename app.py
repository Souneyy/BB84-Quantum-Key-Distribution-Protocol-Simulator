import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from bb84_simulation import BB84Simulator
import numpy as np
import traceback

def plot_transmission(df, title):
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Alice's bits and bases
        ax.scatter(df['step'], [0.8] * len(df), marker='s', c=['red' if b == 1 else 'blue' for b in df['alice_bits']], 
                  label='Alice Bits', s=100)
        
        # Plot Bob's bits and bases
        ax.scatter(df['step'], [0.2] * len(df), marker='s', c=['red' if b == 1 else 'blue' for b in df['bob_bits']], 
                  label='Bob Bits', s=100)
        
        # Plot bases as symbols
        for i, (alice_base, bob_base) in enumerate(zip(df['alice_bases'], df['bob_bases'])):
            if alice_base == '+':
                ax.plot([i, i], [0.7, 0.9], 'k-', alpha=0.5)
                ax.plot([i-0.2, i+0.2], [0.8, 0.8], 'k-', alpha=0.5)
            else:
                ax.plot([i-0.2, i+0.2], [0.7, 0.9], 'k-', alpha=0.5)
                ax.plot([i+0.2, i-0.2], [0.7, 0.9], 'k-', alpha=0.5)
            
            if bob_base == '+':
                ax.plot([i, i], [0.1, 0.3], 'k-', alpha=0.5)
                ax.plot([i-0.2, i+0.2], [0.2, 0.2], 'k-', alpha=0.5)
            else:
                ax.plot([i-0.2, i+0.2], [0.1, 0.3], 'k-', alpha=0.5)
                ax.plot([i+0.2, i-0.2], [0.1, 0.3], 'k-', alpha=0.5)
        
        # Highlight matching bases
        for i, matched in enumerate(df['matched']):
            if matched:
                ax.axvspan(i-0.4, i+0.4, color='green', alpha=0.1)
        
        ax.set_ylim(0, 1)
        ax.set_xlim(-1, len(df))
        ax.set_yticks([0.2, 0.8])
        ax.set_yticklabels(['Bob', 'Alice'])
        ax.set_xlabel('Qubit Number')
        ax.set_title(title)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='Bit 0'),
            Patch(facecolor='red', label='Bit 1'),
            Patch(facecolor='green', alpha=0.1, label='Matching Bases')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="BB84 Quantum Key Distribution Simulator",
        page_icon="🔐",
        layout="wide"
    )
    
    st.title("BB84 Quantum Key Distribution Protocol Simulator")
    st.write("""
    This simulator demonstrates the BB84 quantum key distribution protocol, showing how 
    quantum properties can be used to generate a secure encryption key between two parties.
    """)
    
    # Add explanation
    with st.expander("How does BB84 work?"):
        st.write("""
        1. **Alice** generates random bits and encodes them in random bases (+ or x)
        2. **Bob** measures the qubits in random bases
        3. They compare bases and keep only matching ones (sifting)
        4. They check for errors to detect eavesdropping
        5. If secure, they use the remaining bits as a key
        """)
    
    # Simulation parameters
    col1, col2 = st.columns(2)
    with col1:
        num_qubits = st.slider("Number of Qubits", 10, 2000, 1000)
    with col2:
        eavesdropping = st.checkbox("Enable Eavesdropping (Eve)")
    
    if st.button("Run Simulation", type="primary"):
        try:
            with st.spinner("Running simulation..."):
                # Run simulation
                simulator = BB84Simulator(num_qubits=num_qubits, eavesdropping=eavesdropping)
                results = simulator.simulate()
            
            # Display results
            st.header("Simulation Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Qubits", results['total_qubits'])
            with col2:
                st.metric("Sifted Bits", results['sifted_bits'])
            with col3:
                st.metric("Error Rate", f"{results['error_rate']:.2%}")
            
            # Display security status
            if results['secure']:
                st.success("🔒 Key Exchange Successful - Channel appears secure!")
            else:
                st.error("⚠️ Warning: High error rate detected! Possible eavesdropping!")
            
            # Show visualization
            st.header("Protocol Visualization")
            st.write("This visualization shows the first 20 qubits of the transmission:")
            df = simulator.get_visualization_data()
            fig = plot_transmission(df, "BB84 Protocol Transmission Visualization")
            if fig:
                st.pyplot(fig)
            
            # Display final key if secure
            if results['secure'] and results['final_key']:
                st.header("Final Key")
                key_display = results['final_key'][:64] + "..." if len(results['final_key']) > 64 else results['final_key']
                st.code(key_display)
                st.write(f"Final key length: {results['final_key_length']} bits")
                
                # Add key statistics
                st.subheader("Key Statistics")
                key_bits = [int(b) for b in results['final_key']]
                zeros = sum(1 for b in key_bits if b == 0)
                ones = sum(1 for b in key_bits if b == 1)
                st.write(f"Zeros: {zeros} ({zeros/len(key_bits):.1%})")
                st.write(f"Ones: {ones} ({ones/len(key_bits):.1%})")
        
        except Exception as e:
            st.error(f"Error during simulation: {str(e)}")
            st.error("Stack trace:")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main() 