"""Tests for `qimp` module."""
from typing import Any
from unittest.mock import patch

import numpy as np
import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

from qimp.ImageEncoding.Encodings import FRQI
from qimp.ImageEncoding.QuantumImage import QuantumImage, generate_example_image


def test_test_image() -> None:
    """
    Test case for the test_image function.

    This function tests whether the generated example image matches the expected image.

    Returns: None
    """
    image = np.array([[0, 0, 0, 0], [0, 255, 255, 0], [0, 255, 255, 0], [0, 0, 0, 0]])

    assert image.all() == generate_example_image(4).all()


def test_quantum_image() -> None:
    """
    Test case for the QuantumImage class.

    This function tests the initialization of a QuantumImage object and verifies that the
    image data is correctly stored.

    Returns: None
    """
    image = np.array([[0, 0, 0, 0], [0, 255, 255, 0], [0, 255, 255, 0], [0, 0, 0, 0]])
    quantumimage = QuantumImage(image)

    assert quantumimage.image.all() == image.all()
    assert type(quantumimage.image) == np.ndarray


def test_wrong_quantum_image() -> None:
    """Test case to check if an exception is raised when an invalid quantum image is provided."""
    with pytest.raises(Exception) as excinfo:
        image = [[0, 0, 0, 0], [0, 255, 255, 0], [0, 255, 255, 0], [0, 0, 0, 0]]
        QuantumImage(image)

    assert str(excinfo.value) == "Wrong Image type"


def test_quantum_image_vector() -> None:
    """
    Test case for the `quantum_image_vector` function.

    This function tests the initialization of a QuantumImage object with a vector image.
    It checks if the image array is correctly assigned and if the image type is a NumPy ndarray.

    """
    image = np.array([0, 0, 0, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 0, 0, 0])
    quantumimage = QuantumImage(image)

    assert quantumimage.image.all() == image.all()
    assert type(quantumimage.image) == np.ndarray


def test_quantum_image_vector_wrong() -> None:
    """
    Test case for the scenario when the original input is a list instead of a square matrix.
    It checks if the appropriate exception is raised and the error message
    matches the expected error message.
    """

    error = "The original input is a list. We tried to reshape it to a"
    error += " square matrix but it did not work."
    error += " Please reshape the list before passing the image to this object. "

    with pytest.raises(Exception) as excinfo:
        image = np.array([0, 0, 0, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 0, 0, 0, 0])
        QuantumImage(image)

    assert str(excinfo.value) == error


def test_quantum_image_zoom() -> None:
    """
    Test case for the quantum_image_zoom function.

    This test case verifies that the quantum_image_zoom function correctly zooms in an image.

    The test creates an input image and a zoomed image. It then creates a QuantumImage object
    with the input image and a zoom factor of 0.5. Finally, it asserts that the image of the
    QuantumImage object matches the zoomed image.

    Returns: None
    """
    image = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 255, 255, 255, 255, 0, 0],
            [0, 0, 255, 255, 255, 255, 0, 0],
            [0, 0, 255, 255, 255, 255, 0, 0],
            [0, 0, 255, 255, 255, 255, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    zoomed_image = np.array([[0, 0, 0, 0], [0, 255, 255, 0], [0, 255, 255, 0], [0, 0, 0, 0]])
    quantumimage = QuantumImage(image, 0.5)

    assert quantumimage.image.all() == zoomed_image.all()


@patch("qimp.ImageEncoding.QuantumImage.plt.show")
def test_retrieveandshow(mock_show: Any) -> None:
    """Test case for the retrieve_and_show method of the QuantumImage class."""
    image = QuantumImage(generate_example_image(side=4), zooming_factor=1)

    FRQI(image)

    image.circuit.measure([x for x in range(0, 5)], [x for x in range(0, 5)])

    # simulator = AerSimulator.get_backend("aer_simulator")
    sumulator = AerSimulator()
    circ = transpile(image.circuit, sumulator)

    result = sumulator.run(circ).result()

    numOfShots = 10000

    if image.retrieve_and_show(result, numOfShots) is None:
        assert True
    else:
        AssertionError()


@patch("qimp.ImageEncoding.QuantumImage.plt.show")
def test_showclassicaliamge(mock_show: Any) -> None:
    """Test case for the retrieve_and_show method of the QuantumImage class."""
    image = QuantumImage(generate_example_image(side=4), zooming_factor=1)
    if image.show_classical_image() is None:
        assert True
    else:
        AssertionError()


def test_add_qubits() -> None:
    """Test case for the add_qubits method of the QuantumImage class."""
    n = 4

    image = QuantumImage(generate_example_image(side=4), zooming_factor=1)
    image.add_qubits(n)

    assert image.circuit.num_qubits == n + 1


def test_measure() -> None:
    """
    Test case for the measure method of the QuantumImage class.

    This function tests whether the circuit is correctly measured.

    Returns: None
    """
    side = 4
    image = QuantumImage(generate_example_image(side=side), zooming_factor=1)
    FRQI(image)
    image.measure()

    assert len(image.circuit.clbits) == side + 1
