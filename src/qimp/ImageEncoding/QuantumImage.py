"""Quantum image class."""
import math
import typing

import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from scipy.ndimage import zoom
from tqdm import tqdm


def test_image(side: int = 8) -> numpy.ndarray:
    """
    Creates a test image.

    Args:
        side (int): side of the test image square

    Returns: an image

    """
    # Create an 8x8 matrix filled with zeros
    ar = np.zeros((side, side))

    # Define the size of the 4x4 square of ones
    square_size = side // 2

    # Calculate the starting and ending indices for the square
    start_row = (side - square_size) // 2
    end_row = start_row + square_size
    start_col = (side - square_size) // 2
    end_col = start_col + square_size

    # Fill the square region with ones
    ar[start_row:end_row, start_col:end_col] = 255

    ar = np.transpose(ar.reshape((side, side)))
    return ar


class QuantumImage(object):
    """General class to implement represent a classical image in Qiskit."""

    angles: typing.List[float] = []
    circuit = QuantumCircuit()
    x_qubits = QuantumRegister()
    y_qubits = QuantumRegister()
    color_qubit = QuantumRegister()
    total_qubits = 0
    initial_qubits = 0
    x_wires: typing.List[int] = []
    y_wires: typing.List[int] = []
    c_wire: int = 0
    pos_wires: typing.List[int] = []
    total_wires: typing.List[int] = []
    n_aux_qubit = 0
    encoding = str
    num_carry = 0
    num_summing = 0
    circuit = QuantumCircuit()
    image = np.ndarray

    def __init__(self, image: numpy.ndarray, zooming_factor: int = 1) -> None:
        """
        Returns an object Quantum Image.

        Arguments:
            image (numpy.ndarray): Input image to be transformed
            zooming_factor (int): Method required to encode the given image (default=FRQI)

        Returns: None

        Raises:
            Exception: Wrong image format.
        """

        if isinstance(image, (list, pd.core.series.Series)):  # Check if the input type is valid
            self.image = np.array(image)
        elif isinstance(image, np.ndarray):
            self.image = image
        else:
            raise Exception("wrong type")

        if self.image.ndim == 1:
            reshapeto = math.sqrt(len(self.image))
            if reshapeto.is_integer():
                self.image = self.image.reshape(int(reshapeto), int(reshapeto))
            else:
                raise Exception(
                    "The original input is a list. We tried to reshape it to a"
                    + " square matrix but it did not work."
                    + " Please reshape the list before passing the image to this object. "
                )

        self.zooming_factor = zooming_factor

        if (
            self.zooming_factor < 1.0
        ):  # If the zooming factor is smaller than one then we apply the zoom
            self.image = zoom(self.image, self.zooming_factor)
            self.image = np.abs(self.image)
            self.image[self.image > 255] = 255

        # compute the padding dimensions for row and cols.
        # works also for rectangular images
        maxval = max(self.image.shape)
        padding_target = pow(2, math.ceil(math.log2(maxval)))

        xpad = padding_target - self.image.shape[0]
        ypad = padding_target - self.image.shape[1]

        xl = int(xpad / 2) + (1 if xpad % 2 == 1 else 0)
        xr = int(xpad / 2)
        yl = int(ypad / 2) + (1 if ypad % 2 == 1 else 0)
        yr = int(ypad / 2)

        self.image = np.pad(self.image, pad_width=((xr, xl), (yr, yl)))

        self.required_qubits = int(math.log2(np.shape(self.image)[0]) * 2)
        # Compute the number of required qubits to index rows and cols

    def show_classical_image(self) -> None:
        """Show in a figure the original image, padded and eventually zoomed."""
        plt.figure()
        plt.imshow(self.image, cmap="gray")
        plt.show()

    def compute_angles(self) -> None:
        """Transform the luminosity values of the image into angles to encode them."""
        normalized_pixels = self.image / 255.0
        self.angles = np.arcsin(normalized_pixels)

    def init_circuit(self) -> None:
        """Initialize circuit for the image."""
        self.x_qubits = QuantumRegister(self.required_qubits / 2, "x")
        self.y_qubits = QuantumRegister(self.required_qubits / 2, "y")

        self.x_wires = list(range(0, int(self.required_qubits / 2)))
        self.y_wires = list(range(int(self.required_qubits / 2), self.required_qubits))
        self.c_wire = self.required_qubits
        self.pos_wires = list(self.x_wires) + list(self.y_wires)
        self.total_wires = list(self.pos_wires) + [self.c_wire]
        self.color_qubit = QuantumRegister(1, "c")
        cr = ClassicalRegister(self.total_qubits, "classical")

        self.circuit = QuantumCircuit(self.x_qubits, self.y_qubits, self.color_qubit, cr)

        self.initial_qubits = self.circuit.num_qubits

    def draw_circuit(self) -> None:
        """Draws the circuit."""
        plt.figure(1)
        self.circuit.draw(output="mpl")
        plt.show()

    def insert_qubits(self, n: int, name: str = "") -> None:
        """Insert qubits in the image circuit.

        Args:
            n (int): number of qubits.
            name (str): name to associate to the qubits.

        Returns: None

        """
        qr1 = QuantumRegister(n, name)
        self.circuit.regs.insert(0, qr1)
        # TODO: Modify for insertion on top

    def add_qubits(self, n: int, name: str = "") -> None:
        """Append qubits.

        Args:
            n (int): number of qubits to append.
            name (str): name to associate to the qubits

        Returns: None

        """
        extra = QuantumRegister(n, name)
        self.circuit.add_register(extra)

    def reverse(self) -> None:
        """Revert circuit.

        Returns: None

        """
        self.circuit = self.circuit.reverse_bits()

    def retrieve_and_show(self, result: dict, numOfShots: int) -> None:
        """Run experiments and show result, it requires measurements.

        Args:
            result (dict): where to store the results.
            numOfShots (int): number of experiments to run.

        Returns: None

        """
        retrieve_image_0 = np.zeros(
            (
                int(pow(2, self.required_qubits / 2)),
                int(pow(2, self.required_qubits / 2)),
            )
        )
        with tqdm(total=pow(2, self.n_aux_qubit) * pow(2, self.required_qubits)) as pbar:
            for i in range(pow(2, self.n_aux_qubit) * pow(2, self.required_qubits)):
                try:
                    bitsneeded = "{0:0" + str(int(self.required_qubits) + self.n_aux_qubit) + "b}"
                    s = bitsneeded.format(i)
                    new_s = "1" + s
                    extracted_value = np.sqrt(result.get_counts(self.circuit)[new_s] / numOfShots)
                    y = s[: int(self.required_qubits / 2)]
                    x = s[int(self.required_qubits / 2) : self.required_qubits]
                    x_index = 0
                    y_index = 0

                    for index in range(int(self.required_qubits / 2)):
                        if x[-index - 1] == "1":
                            y_index += pow(2, index)
                        if y[-index - 1] == "1":
                            x_index += pow(2, index)

                    retrieve_image_0[int(x_index)][int(y_index)] = extracted_value
                    pbar.update(1)
                except KeyError:
                    pbar.update(1)
                    pass
        plt.figure(1)
        multip = 32

        retrieve_image_0 *= multip * 255.0
        retrieve_image_0 = retrieve_image_0.astype("int")
        retrieve_image_0 = retrieve_image_0.reshape(
            (
                pow(2, int(self.required_qubits / 2)),
                pow(2, int(self.required_qubits / 2)),
            )
        )
        # Plot the retrieved image to see if it is the same as the one encoded
        plt.imshow(retrieve_image_0, cmap="gray", vmin=0, vmax=255)
        plt.title("retrieved image")
        plt.show()

    def __info__(self) -> str:
        """Show the state of the saved data of the image, useful for the reader.

        Returns: str
        """
        return (
            f"Input image of dimension "
            f"{int(math.pow(np.shape(self.image)[0], 2))}"
            f" with a zooming factor of "
            f"{self.zooming_factor}.\n"
            f"The chosen encoding is {self.encoding}. The total qubits required "
            f"are {self.total_qubits}"
        )

    def measure(self) -> None:
        """Measures the circuit.

        Returns: None

        """
        self.circuit.measure([int(x) for x in range(self.total_qubits)], self.total_wires)
