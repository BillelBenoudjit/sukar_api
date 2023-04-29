from qiskit import *
from random import randint
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
    
def get_outcome(input):
    print(input)
    inputs = []
    c = randint(1, 2)
    if c == 1:
        inputs.append("r" + str(randint(1, 3)))
    else:    
        inputs.append("c" + str(randint(1, 3)))
    
    print("Inputs are: ", inputs)
        
    for d in inputs:
        qc = QuantumCircuit(5,3)
        qc = mps(qc,d)
    
        # Transpile for simulator
        simulator = Aer.get_backend('aer_simulator')
        circ = transpile(qc, simulator)

        # Run and get counts
        result = simulator.run(circ, shots=1).result()
        counts = (result.get_counts(circ))
        print(f'{d}: {sorted(counts)}')
        return(counts)
        qc.draw('mpl')
        
qc = QuantumCircuit(5,3)

def mps(qc, decision):
    if decision == 'r1':
        # XI, IX, XX
        # rotating 0 to X Basis
        rotate_X(qc, 0, 2)
        # rotating 1 to X basis
        rotate_X(qc, 1, 3)
        # rotating 0 and 1 to X basis
        rotate_X(qc, 0, 4)
        rotate_X(qc, 1, 4)
        
    if decision == 'r2':
        # IY, YI, YY
        # rotating 1 to Y Basis
        rotate_Y(qc, 1, 2)
        # rotating 0 to Y Basis
        rotate_Y(qc, 0, 3)
        # rotating 0 and 1 to Y basis
        rotate_Y(qc, 0, 4)
        rotate_Y(qc, 1, 4)
        
    if decision == 'r3':
        # XY, YX, ZZ
        # rotating 0 to the X basis
        rotate_X(qc, 0, 2)
        # rotating 1 to the Y basis
        rotate_Y(qc, 1, 2)
        # rotating 0 to the y basis and back
        rotate_Y(qc, 0, 3)
        # rotating 1 to the x basis and back
        rotate_X(qc, 1, 3)
        # rotating 0 and 1 to the Z basis
        rotate_Z(qc, 0, 4)
        rotate_Z(qc, 1, 4)  

    if decision == 'c1':
        # XI, IY, XY
        # rotating 0 to the X basis
        rotate_X(qc, 0, 2)
        # rotating 1 to the Y basis
        rotate_Y(qc, 1, 3)
        # rotating 0 to the X basis and 1 to the Y basis
        rotate_X(qc, 0, 4)
        rotate_Y(qc, 1, 4)

    if decision == 'c2':
        # IX, YI, YX
        # rotating 1 to the X basis
        rotate_X(qc, 1, 2)
        # rotating 0 to the Y basis
        rotate_Y(qc, 0, 3) 
        # rotating 0 to the Y basis and 1 to the X basis
        rotate_Y(qc, 0, 4)
        rotate_X(qc, 1, 4)
        
    if decision == 'c3':
        # XX, YY, ZZ
        # rotating 0 to the X basis
        rotate_X(qc, 0, 2)
        # rotating 1 to the x basis
        rotate_X(qc, 1, 2)
        # rotating 0 to the Y basis
        rotate_Y(qc, 0, 3)
        # rotating 1 to the Y basis
        rotate_Y(qc, 1, 3)
        # rotating 0 and 1 to the Z basis
        rotate_Z(qc, 0, 4)
        rotate_Z(qc, 1, 4)
        
    measure(qc)
    return qc

# get_outcome()        
