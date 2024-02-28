"""Tests for `qimp` module."""
from qimp.ImageEncoding.Encodings import hadamard
from typing import Generator
import numpy as np
import pytest
import qiskit

def test_hadamard():
    """Test the hadamard function."""
    # Create a test circuit
    circ = qiskit.QuantumCircuit(3)
    n = [0, 1, 2]

    # Apply the hadamard gate
    hadamard(circ, n)

    # Check if the gates were applied correctly
    assert str(circ) == "     ┌───┐\nq_0: ┤ H ├\n     ├───┤\nq_1: ┤ H ├\n     ├───┤\nq_2: ┤ H ├\n     └───┘"

    # Add more assertions if needed

from qimp.ImageEncoding.Encodings import FRQI
from qimp.ImageEncoding.QuantumImage import QuantumImage,generate_example_image

def test_FRQI():
    # Create a QuantumImage object for testing
    req_qubits = 6
    total_qubits = 7
    depth = 128


    quantumimage = QuantumImage(generate_example_image(8))
    # Call the xyfrqi function
    FRQI(quantumimage)


    # Add assertions to check the expected behavior of the function
    assert quantumimage.required_qubits == req_qubits
    assert quantumimage.total_qubits == total_qubits
    assert quantumimage.circuit.depth() == depth
    # Add more assertions as needed

def test_FRQI_failure():
    with pytest.raises(Exception) as excinfo:  
            # Create a QuantumImage object for testing
        req_qubits = 6
        total_qubits = 7
        depth = 128


        quantumimage = QuantumImage(generate_example_image(8))
        # Call the xyfrqi function
        FRQI(quantumimage)
        FRQI(quantumimage)
    assert str(excinfo.value) == "The image has allready been encoded"

