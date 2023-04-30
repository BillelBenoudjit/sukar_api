from qiskit.circuit.random import random_circuit
from random import randint
from qiskit import *
from qiskit.tools.visualization import plot_histogram, plot_state_city

# rotation in X basis and back
def rotate_X(qc, main_circuit_qubit, measuring_qubit):
    qc.h(main_circuit_qubit)
    qc.cx(main_circuit_qubit,measuring_qubit)
    qc.h(main_circuit_qubit)
    qc.barrier()

# rotation in the Y basis and back
def rotate_Y(qc, main_circuit_qubit, measuring_qubit):
    qc.sdg(main_circuit_qubit)
    qc.h(main_circuit_qubit)
    qc.cx(main_circuit_qubit, measuring_qubit)
    qc.h(main_circuit_qubit)
    qc.s(main_circuit_qubit)
    qc.barrier()
    
# rotation in the Z basis and back
def rotate_Z(qc, main_circuit_qubit, measuring_qubit):
    qc.cx(main_circuit_qubit, measuring_qubit)

# all measurements
def measure(qc):
    qc.measure([2,3,4], [0,1,2])
    
def get_local_outcome():
    inputs = []
    c = randint(1, 2)
    if c == 1:
        inputs.append("r" + str(randint(1, 3)))
    else:    
        inputs.append("c" + str(randint(1, 3)))
    
    d = inputs[0]
    print(inputs)
    
    qc = QuantumCircuit(5,3)
    qc = mps(qc,d)

    # Transpile for simulator
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc, simulator)

    # Run and get counts
    result = simulator.run(circ, shots=1).result()
    counts = (result.get_counts(circ))
    print(f'{d}: {sorted(counts)}')

    return(f'{d}: {sorted(counts)}')

qc = QuantumCircuit(5,3)

def mps(qc, decision):
    if decision == 'r1':
        # ZI, IZ, ZZ
        # rotating 0 to Z Basis
        rotate_Z(qc, 0, 2)
        # rotating 1 to Z basis
        rotate_Z(qc, 1, 3)
        # rotating 0 and 1 to Z basis
        rotate_Z(qc, 0, 4)
        rotate_Z(qc, 1, 4)
        
    if decision == 'r2':
        # IX, XI, XX
        # rotating 1 to X Basis
        rotate_X(qc, 1, 2)
        # rotating 0 to X Basis
        rotate_X(qc, 0, 3)
        # rotating 0 and 1 to X basis
        rotate_X(qc, 0, 4)
        rotate_X(qc, 1, 4)
        
    if decision == 'r3':
        # ZX, XZ, YY
        # rotating 0 to the Z basis
        rotate_Z(qc, 0, 2)
        # rotating 1 to the X basis
        rotate_X(qc, 1, 2)
        # rotating 0 to the X basis
        rotate_X(qc, 0, 3)
        # rotating 1 to the Z basis
        rotate_Z(qc, 1, 3)
        # rotating 0 and 1 to the Y basis
        rotate_Y(qc, 0, 4)
        rotate_Y(qc, 1, 4)  

    if decision == 'c1':
        # ZI, IX, ZX
        # rotating 0 to the Z basis
        rotate_Z(qc, 0, 2)
        # rotating 1 to the X basis
        rotate_X(qc, 1, 3)
        # rotating 0 to the Z basis
        rotate_Z(qc, 0, 4)
        # rotating 1 to the X basis
        rotate_X(qc, 1, 4)

    if decision == 'c2':
        # IZ, XI, XZ
        # rotating 1 to the Z basis
        rotate_Z(qc, 1, 2)
        # rotating 0 to the X basis
        rotate_X(qc, 0, 3) 
        # rotating 0 to the X basis
        rotate_X(qc, 0, 4)
        # rotating 1 to the Z basis
        rotate_Z(qc, 1, 4)
        
    if decision == 'c3':
        # ZZ, XX, YY
        # rotating 0 to the Z basis
        rotate_Z(qc, 0, 2)
        # rotating 1 to the X basis
        rotate_Z(qc, 1, 2)
        # rotating 0 to the X basis
        rotate_X(qc, 0, 3)
        # rotating 1 to the Z basis
        rotate_X(qc, 1, 3)
        # rotating 0 and 1 to the Y basis
        rotate_Y(qc, 0, 4)
        rotate_Y(qc, 1, 4)
        
    measure(qc)
    return qc

get_local_outcome()
