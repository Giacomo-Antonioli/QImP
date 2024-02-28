from qiskit import QuantumCircuit, QuantumRegister

from qimp.Filters import Gates


def test_make_sum_gate() -> QuantumCircuit:
    """Test the make_sum_gate function."""
    expected_circuit = QuantumCircuit(
        QuantumRegister(1, "c"), QuantumRegister(1, "a"), QuantumRegister(1, "b"), name="Sum"
    )
    expected_circuit.cx(1, 2)
    expected_circuit.cx(0, 2)

    result = Gates.make_sum_gate()

    assert result == expected_circuit


def test_make_carry_gate() -> QuantumCircuit:
    """Test the make_carry_gate function."""
    expected_circuit = QuantumCircuit(
        QuantumRegister(1, "c"),
        QuantumRegister(1, "a"),
        QuantumRegister(1, "b"),
        QuantumRegister(1, "c[i+1]"),
        name="Carry",
    )
    expected_circuit.ccx(1, 2, 3)
    expected_circuit.cx(1, 2)
    expected_circuit.ccx(0, 2, 3)

    result = Gates.make_carry_gate()

    assert result == expected_circuit
