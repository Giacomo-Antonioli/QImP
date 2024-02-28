from ImageEncoding.Encodings import FRQI
from ImageEncoding.QuantumImage import QuantumImage, generate_example_image

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    image = QuantumImage(generate_example_image(side=4), zooming_factor=1)
    print(image.__info__())

    image.show_classical_image()
    print("Encoding")
    FRQI(image)

    print("Sobel")
    # sobel(image)

    print("drawing circ")
    # image.draw_circuit()
    image.circuit.measure([x for x in range(0, 5)], [x for x in range(0, 5)])
    print(image.circuit)
    import time

    from qiskit import Aer, transpile

    # qasm = aer.QasmSimulator(method="statevector")
    simulator = Aer.get_backend("aer_simulator")
    circ = transpile(image.circuit, simulator)

    # Run and get unitary
    result = simulator.run(circ).result()
    # In[ ]:
    #############################################
    numOfShots = 10000

    start_time = time.time()

    # result = execute(image.circuit, qasm, shots=numOfShots).result()  # ,,optimization_level=3
    # result = sim.run(circuit,shots=numOfShots,seed_simulator=12345).result()
    print("--------------------")
    print(result)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print(len(result.get_counts(image.circuit)))
    image.retrieve_and_show(result, numOfShots)
    # Create an empty array to save the retrieved image
    # original = True
    # counts = result.get_counts(image.circuit)
    # print(counts)
    # plt.figure(2)
    # plot_histogram(counts)
    # plt.show()
    # image.retrieve_and_show(result, numOfShots)
    # Create an empty array to save the retrieved image
    # retrieve_image = np.zeros((int(pow(2, image.required_qubits / 2)),
    # int(pow(2, image.required_qubits / 2))))
