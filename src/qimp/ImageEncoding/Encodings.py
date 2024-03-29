"""Encodings File."""
import numpy as np
import qiskit
from qiskit.circuit.library.standard_gates import RYGate
from tqdm import tqdm

from .QuantumImage import QuantumImage


def hadamard(circ: qiskit.QuantumCircuit, n: list) -> None:
    """Hadamard gate applied to n wires.

    Args:
        circ (qiskit.QuantumCircuit): Target circuit.
        n (list): List of target Wires.

    Returns: None

    """
    for i in n:
        circ.h(i)


def xyfrqi(quantumimage: QuantumImage) -> None:
    """FRQI encoding with xy variant.

    Args:
        quantumimage (QuantumImage): Target Image.


    Returns: None

    """
    n = [
        int(x)
        for x in range(
            quantumimage.n_aux_qubit,
            quantumimage.total_qubits + quantumimage.n_aux_qubit - 1,
        )
    ]
    t = int(quantumimage.total_qubits + quantumimage.n_aux_qubit - 1)
    bitsneeded = "{0:0" + str(int(quantumimage.required_qubits / 2)) + "b}"
    print(bitsneeded)
    nqubits: int = quantumimage.circuit.num_qubits
    print("TOTQUB: " + str(nqubits))
    print("requiredqubits:" + str(quantumimage.required_qubits))
    y_old = ""
    for index_row, rows in enumerate(tqdm(quantumimage.angles)):
        x_old = bitsneeded.format(index_row - 1)[::-1]
        if index_row == 0:
            changed = False
        else:
            changed = True

        for index_cols, i in enumerate(rows):  # i: np.ndarray
            y = bitsneeded.format(index_cols)

            if index_row + index_cols > 0:
                if changed:
                    changed = False
                    x = bitsneeded.format(index_row)
                    tonegatex = []
                    for index, element in enumerate(x[::-1]):
                        if element != x_old[index]:
                            # print("adding 1")
                            # print(nqubits+index-required_qubits/2-1)
                            tonegatex.append(
                                int(
                                    nqubits
                                    + index
                                    - quantumimage.required_qubits / 2
                                    - 1
                                    - quantumimage.n_aux_qubit
                                )
                            )
                            # print("tonegatx:"+str(int(nqubits+index-required_qubits/2-1-n_aux_qubit)))

                    quantumimage.circuit.x(np.abs(tonegatex) + quantumimage.n_aux_qubit)
                tonegatey = []
                for index, element in enumerate(y[::-1]):
                    if element != y_old[index]:
                        tonegatey.append(
                            int(
                                nqubits
                                + index
                                - quantumimage.required_qubits
                                - 1
                                - quantumimage.n_aux_qubit
                            )
                        )
                        # print("tonegaty:"+str(int(nqubits+index-required_qubits-1-n_aux_qubit)))

                quantumimage.circuit.x(np.abs(tonegatey) + quantumimage.n_aux_qubit)
            y_old = bitsneeded.format(index_cols)[::-1]

            controls = len(n)
            cry = RYGate(2 * i).control(controls)
            aux = np.append(n, t).tolist()
            quantumimage.circuit.append(cry, aux)
            # circ.barrier()


def FRQI(quantumImage: QuantumImage) -> None:
    """
    FRQI encoding for a quantum image.

    Args:
        quantumImage (QuantumImage): Target Image.

    Returns: None

    Raises:
        Exception: If the image has already been encoded."""

    if quantumImage.encoding == "":
        quantumImage.total_qubits = int(quantumImage.required_qubits + 1)
        quantumImage.compute_angles()
        quantumImage.init_circuit(1)
        quantumImage.encoding = "FRQI"
    else:
        raise Exception("The image has allready been encoded")

    hadamard(quantumImage.circuit, [x for x in range(quantumImage.total_qubits - 1)])
    xyfrqi(quantumImage)  # 1


def binarization(image: np.ndarray) -> np.chararray:
    """Binarization of a grayscale image.

    Args:
        image (np.ndarray): Grayscale Image.

    Returns:
        list: Binary values of the pixels of the image.
    """
    binarizedangles = np.chararray((image.shape[0], image.shape[1]), itemsize=8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            binarizedangles[i][j] = np.binary_repr(int(image[i][j]), width=8)

    return binarizedangles


def NEQR(quantumimage: QuantumImage) -> None:
    """
    NEQR encoding for a quantum image.

    Args:
        quantumimage (QuantumImage): Target Image.

    Returns: None

    Raises:
        Exception: If the image has already been encoded."""

    if quantumimage.encoding == "":
        quantumimage.total_qubits = int(quantumimage.required_qubits + 8)
        binarizedangles = binarization(quantumimage.image)
        print(binarizedangles)
        quantumimage.init_circuit(8)
        quantumimage.encoding = "NEQR"
    else:
        raise Exception("The image has allready been encoded")

    hadamard(quantumimage.circuit, [x for x in range(quantumimage.required_qubits)])
    bitsneeded = "{0:0" + str(int(quantumimage.required_qubits / 2)) + "b}"

    nqubits: int = quantumimage.circuit.num_qubits

    y_old = ""
    for index_row, rows in enumerate(tqdm(binarizedangles)):
        x_old = bitsneeded.format(index_row - 1)[::-1]
        if index_row == 0:
            changed = False
        else:
            changed = True

        for index_cols, i in enumerate(rows):  # i: np.ndarray
            y = bitsneeded.format(index_cols)

            if index_row + index_cols > 0:
                if changed:
                    changed = False
                    x = bitsneeded.format(index_row)
                    tonegatex = []
                    for index, element in enumerate(x[::-1]):
                        if element != x_old[index]:
                            # print("adding 1")
                            # print(nqubits+index-required_qubits/2-1)
                            tonegatex.append(
                                int(
                                    nqubits
                                    + index
                                    - quantumimage.required_qubits / 2
                                    - 8
                                    - quantumimage.n_aux_qubit
                                )
                            )
                            # print("tonegatx:"+str(int(nqubits+index-required_qubits/2-1-n_aux_qubit)))

                    quantumimage.circuit.x(np.abs(tonegatex) + quantumimage.n_aux_qubit)
                tonegatey = []
                for index, element in enumerate(y[::-1]):
                    if element != y_old[index]:
                        tonegatey.append(
                            int(
                                nqubits
                                + index
                                - quantumimage.required_qubits
                                - 8
                                - quantumimage.n_aux_qubit
                            )
                        )
                        # print("tonegaty:"+str(int(nqubits+index-required_qubits-1-n_aux_qubit)))

                quantumimage.circuit.x(np.abs(tonegatey) + quantumimage.n_aux_qubit)

                print("printing i:", i)
                for index, element in enumerate(list(str(i))):
                    if element != "b" and element != "'":
                        print("printing element:", element)
                        if element == "1":
                            quantumimage.circuit.mcx(
                                list(
                                    range(
                                        quantumimage.n_aux_qubit,
                                        quantumimage.n_aux_qubit + quantumimage.required_qubits,
                                    )
                                ),
                                quantumimage.required_qubits
                                + quantumimage.n_aux_qubit
                                + index
                                - 2,
                            )
            y_old = bitsneeded.format(index_cols)[::-1]
        quantumimage.circuit.barrier()
