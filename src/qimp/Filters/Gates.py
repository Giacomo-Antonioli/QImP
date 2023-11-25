import qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import ControlledGate

import qimp.ImageEncoding.QuantumImage


def make_sum_gate() -> qiskit.QuantumCircuit:
    """Create sum gate function."""
    # Quantum sum gate
    c = QuantumRegister(1, "c")
    a = QuantumRegister(1, "a")
    b = QuantumRegister(1, "b")
    # create the quantum circuit for the image
    summing = QuantumCircuit(c, a, b, name="Sum")

    summing.cx(1, 2)
    summing.cx(0, 2)
    return summing


summing_gate = make_sum_gate()


def make_carry_gate() -> qiskit.QuantumCircuit:
    """Create sum gate."""
    # Quantum carry gate
    c = QuantumRegister(1, "c")
    a = QuantumRegister(1, "a")
    b = QuantumRegister(1, "b")
    d = QuantumRegister(1, "c[i+1]")

    # create the quantum circuit for the image
    carry = QuantumCircuit(c, a, b, d, name="Carry")

    carry.ccx(1, 2, 3)
    carry.cx(1, 2)
    carry.ccx(0, 2, 3)
    return carry


carry_gate = make_carry_gate()


def make_translation(
    num_summing: int, num_carry: int, auxiliary: int, skipped: bool
) -> ControlledGate:
    """
    Create traslation circuit.

    Args:
        num_summing (int): number of wires
        num_carry (int): number of wires +1
        auxiliary (int): auxiliary qubits
        skipped (bool): skip one of the auxiliary qubits or not

    Returns: Gate

    """
    original = QuantumRegister(num_summing, "original")
    shift = QuantumRegister(num_summing, "shift")
    carryqubits = QuantumRegister(num_carry, "carry")
    translation = QuantumCircuit(original, shift, carryqubits, name="Traslation")

    for index in range(num_summing):
        translation.compose(
            carry_gate,
            [index + 2 * num_summing, index, index + num_summing, index + 2 * num_summing + 1],
            inplace=True,
        )
        # translation.cx(index,index+num_summing)
    translation.cx(num_summing - 1, 2 * num_summing - 1)
    for index in reversed(range(num_summing)):
        carry_sum = translation.num_qubits - (num_carry - index - 1) - 1
        add_1 = index
        add_2 = translation.num_qubits - num_carry - (num_summing - index)
        if index != num_summing - 1:
            carry_post = carry_sum + 1

            # inversecarrygate=carry.inverse().to_gate()
            translation.compose(
                carry_gate.inverse(), [carry_sum, add_1, add_2, carry_post], inplace=True
            )
        translation.compose(summing_gate, [carry_sum, add_1, add_2], inplace=True)
    print("carry and sum gates added")
    for index in range(num_summing):
        translation.swap(index, num_summing + index)
    print("swap gates added")
    print(auxiliary)
    controlled_translation = translation.to_gate().control(auxiliary)
    controlled_translation_skipped = translation.to_gate().control(auxiliary - 1)
    print("gate made")
    if skipped:
        return controlled_translation_skipped
    else:
        return controlled_translation


def encode_number(quantumImage: qimp.ImageEncoding.QuantumImage.QuantumImage, shift: int) -> None:
    """Encode number in binary with x gates."""
    number = format(shift, "0" + str(quantumImage.num_summing) + "b")
    for index, element in enumerate(number[::-1]):
        if element == "1":
            # print("SI, shift["+str(index)+"]")
            print("total qubits: " + str(quantumImage.total_qubits + quantumImage.n_aux_qubit))
            print(quantumImage.total_qubits + index)
            quantumImage.circuit.x(
                quantumImage.total_qubits + quantumImage.n_aux_qubit + index
            )  # da fare fuori


def traslate_circuit(
    quantumImage: qimp.ImageEncoding.QuantumImage.QuantumImage,
    axis: str,
    shift: int,
    skip: bool = False,
) -> None:
    """
    Create a traslation circuit.

    Args:
        quantumImage (qimp.ImageEncoding.QuantumImage.QuantumImage): Quantum image
        axis (str): axis on which to perform traslation
        shift (int): number of positions to shift
        skip (bool): True if control is on 3 rather than 4 qubits

    Returns: None

    """
    print("encoding")
    encode_number(quantumImage, shift)
    print("Post encoding")
    control_qubits = [i for i in range(quantumImage.n_aux_qubit - (0 if not skip else 1))]
    print("#1")
    if axis == "x":
        control_qubits = control_qubits + [
            i
            for i in range(
                quantumImage.n_aux_qubit, quantumImage.n_aux_qubit + quantumImage.num_summing
            )
        ]
        print("#2")
    elif axis == "y":
        control_qubits = control_qubits + [
            i
            for i in range(
                quantumImage.n_aux_qubit + quantumImage.num_summing,
                quantumImage.n_aux_qubit + 2 * quantumImage.num_summing,
            )
        ]
        print("#2")
    control_qubits = control_qubits + [
        i
        for i in range(
            quantumImage.n_aux_qubit + quantumImage.total_qubits,
            quantumImage.n_aux_qubit
            + quantumImage.total_qubits
            + quantumImage.num_summing
            + quantumImage.num_carry,
        )
    ]
    print("#3")
    quantumImage.circuit.append(
        make_translation(
            quantumImage.num_summing, quantumImage.num_carry, quantumImage.n_aux_qubit, skip
        ),
        control_qubits,
    )
    print("#4")
    for index in range(quantumImage.num_summing):
        quantumImage.circuit.reset(quantumImage.n_aux_qubit + quantumImage.total_qubits + index)
    print("#5")
