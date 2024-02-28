from qimp.ImageEncoding.QuantumImage import QuantumImage

from .Gates import traslate_circuit


def sobel(quantumImage: QuantumImage) -> None:
    """Quantum implementation of the Sobel filter, it takes in input a quantum image object and
        applies the required transformations.


    Args:
        quantumImage (QuantumImage): Input quantum image.
    """
    quantumImage.reverse()
    quantumImage.add_qubits(4, "aux")
    quantumImage.n_aux_qubit = 4
    quantumImage.reverse()

    quantumImage.num_summing = int(quantumImage.required_qubits / 2)
    quantumImage.num_carry = quantumImage.num_summing + 1
    quantumImage.add_qubits(quantumImage.num_summing)
    quantumImage.add_qubits(quantumImage.num_carry)
    # quantumImage.draw_circuit()
    print("Traslating")
    traslate_circuit(quantumImage, "x", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    print("#1")
    traslate_circuit(quantumImage, "y", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))

    quantumImage.circuit.x(3)  # 1110    0001
    quantumImage.circuit.barrier()
    traslate_circuit(quantumImage, "x", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    traslate_circuit(quantumImage, "y", 1)
    quantumImage.circuit.x(3)
    quantumImage.circuit.x(2)  # 1101     0010
    traslate_circuit(
        quantumImage, "x", int(pow(2, int(quantumImage.required_qubits) / 2) - 1), True
    )

    quantumImage.circuit.x(1)
    traslate_circuit(quantumImage, "x", 1, True)
    quantumImage.circuit.x(2)
    traslate_circuit(quantumImage, "y", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    traslate_circuit(quantumImage, "x", 1)

    quantumImage.circuit.x(3)
    traslate_circuit(quantumImage, "x", 1)
    traslate_circuit(quantumImage, "y", 1)
    quantumImage.circuit.x(1)
    quantumImage.circuit.x(3)

    quantumImage.circuit.x(0)
    quantumImage.circuit.barrier()
    traslate_circuit(quantumImage, "y", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    traslate_circuit(quantumImage, "x", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    quantumImage.circuit.x(3)  # 1110    0001
    quantumImage.circuit.barrier()
    traslate_circuit(quantumImage, "y", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    traslate_circuit(quantumImage, "x", 1)
    quantumImage.circuit.x(3)
    quantumImage.circuit.x(2)  # 1101     0010
    traslate_circuit(
        quantumImage, "y", int(pow(2, int(quantumImage.required_qubits) / 2) - 1), True
    )

    quantumImage.circuit.x(1)
    traslate_circuit(quantumImage, "y", 1, True)
    quantumImage.circuit.x(2)
    traslate_circuit(quantumImage, "x", int(pow(2, int(quantumImage.required_qubits) / 2) - 1))
    traslate_circuit(quantumImage, "y", 1)

    quantumImage.circuit.x(3)
    traslate_circuit(quantumImage, "y", 1)
    traslate_circuit(quantumImage, "x", 1)
    quantumImage.circuit.x(1)
    quantumImage.circuit.x(3)
    quantumImage.circuit.x(0)
    quantumImage.circuit.barrier()
