import pytest
import qiskit

from qimp.ImageEncoding.Encodings import FRQI, NEQR, hadamard
from qimp.ImageEncoding.QuantumImage import QuantumImage, generate_example_image

"""Tests for `qimp` module."""


def test_hadamard() -> None:
    """
    Test the hadamard function.

    This function tests the correctness of the hadamard function by creating a test circuit,
    applying the hadamard gate to the circuit, and checking if the gates were applied correctly.

    Returns: None
    """
    # Create a test circuit
    circ = qiskit.QuantumCircuit(3)
    n = [0, 1, 2]

    # Apply the hadamard gate
    hadamard(circ, n)

    # Check if the gates were applied correctly
    assert (
        str(circ)
        == "     ┌───┐\nq_0: ┤ H ├\n     ├───┤\nq_1: ┤ H ├\n     ├───┤\nq_2: ┤ H ├\n     └───┘"
    )

    # Add more assertions if needed


def test_FRQI() -> None:
    """
    Test case for the FRQI function.

    This test case creates a QuantumImage object for testing and calls the FRQI function on it.
    It then adds assertions to check the expected behavior of the function.

    Assertions:
    - quantumimage.required_qubits should be equal to req_qubits
    - quantumimage.total_qubits should be equal to total_qubits
    - quantumimage.circuit.depth() should be equal to depth
    """
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


def test_FRQI_failure() -> None:
    """
    Test case for the failure scenario of the FRQI function.

    This test case verifies that an exception is raised when the FRQI function is called
    on a QuantumImage object that has already been encoded.

    Raises:
        Any exception that occurs when calling the FRQI function on an already
        encoded QuantumImage object.

        Exception: If the image has already been encoded.

    """
    with pytest.raises(Exception) as excinfo:
        # Create a QuantumImage object for testing
        quantumimage = QuantumImage(generate_example_image(8))
        # Call the xyfrqi function
        FRQI(quantumimage)
        FRQI(quantumimage)
    assert str(excinfo.value) == "The image has allready been encoded"


def test_NEQR_encoding() -> None:
    """
    Test case for NEQR encoding.

    This function tests the behavior of the NEQR encoding function by
    performing the following steps:
    1. Create a QuantumImage object with a generated example image.
    2. Call the NEQR function on the QuantumImage object.
    3. Assert that the encoding of the QuantumImage object is set to "NEQR".
    4. Assert that the total qubits of the QuantumImage object is calculated correctly.
    5. Add more assertions to test the behavior of the NEQR function.

    Returns: None
    """
    quantumimage = QuantumImage(generate_example_image(8))

    # Call the NEQR function
    NEQR(quantumimage)

    # Assert that the encoding is set to "NEQR"
    assert quantumimage.encoding == "NEQR"

    # Assert that the total qubits is calculated correctly
    assert quantumimage.total_qubits == quantumimage.required_qubits + 8

    # Add more assertions to test the behavior of the NEQR function
    # ...


def test_NEQR_encoding_failure() -> None:
    """
    Test case for NEQR encoding failure.

    This test case checks if an exception is raised when trying to encode an image
    that has already been encoded using NEQR encoding.
    """
    with pytest.raises(Exception) as excinfo:
        # Create a QuantumImage object for testing
        quantumimage = QuantumImage(generate_example_image(8))
        # Call the NEQR function twice
        NEQR(quantumimage)
        NEQR(quantumimage)
    assert str(excinfo.value) == "The image has allready been encoded"
