import numpy as np

from qiskit import *
from qiskit.test.mock import *

def check_result(results, col, row):
    print_tut = True
    for i in results: 
        if print_tut:
            winning_alice, winning_bob = explain(i, col, row)
            print_tut = False
            return winning_alice, winning_bob

        print("Quantum circuit solution")
        print(i+"\n")
        i = np.array(list(i.split())).astype(int)[::-1]
        # bring array in correct i.e. from incoming y2,y1,x2,x1 -> x1,x2,y1,y2
        a = i[0:2]
        a_sum = np.sum(a)
        a3 = int(np.mod(a_sum+1,2))
        a = np.append(a,a3)
        winning_alice = np.mod(a_sum + a3, 2) == 1
        # compute x3 by x1+x2+1 mod 2 and save to array

        b = i[2:]
        b_sum = np.sum(b)
        b3 = int(np.mod(b_sum,2))
        b = np.append(b,b3)
        winning_bob = np.mod(b_sum + b3, 2) == 0   
        # compute y3 by y1+y2 mod 2 and save to array

        # compute overall winning condition -> alice at index of bob's row and vice versa
        print("Alice's selection. Column:"+str(col)+"\n"+str(a.reshape(3,1))+"\n")
        print("Bob's circuit solution. Row:"+str(row)+"\n"+str(b)+"\n")
        
        if(winning_bob & winning_alice & (a[row-1]==b[col-1])):
            print("Victory!")    
            print("The following magic square wins the game!")
            k = np.empty((3,3,))
            k[:] = np.nan
            k[:,col-1] = a
            k[row-1,:] = b
            print(k)
        else:
            print("The Game is lost!")
        print("------------------------------------------")  
        print("\n")

def explain(result, col, row):
    print("Resultant quantum circuit solution:"+"\n")
    print(result+"\n")
    example = np.array(list(result.split())).astype(int)[::-1]
    print("Bring array in correct bit order i.e. from incoming y2,y1,x2,x1 -> x1,x2,y1,y2"+"\n")
    print(str(example)+"\n")
    print("Compute missing x3 with x1+x2+1 mod 2 for Alice and save to array for further processing")
    print("Compute missing y3 with y1+y2 mod 2 for Bob and save to array for further processing"+"\n")
   
    a = example[0:2]
    a_sum = np.sum(a)
    a3 = int(np.mod(a_sum+1,2))
    a = np.append(a,a3)
    winning_alice = np.mod(a_sum + a3, 2) == 1

    b = example[2:]
    b_sum = np.sum(b)
    b3 = int(np.mod(b_sum,2))
    b = np.append(b,b3)
    winning_bob = np.mod(b_sum + b3, 2) == 0   

    print("Alice's column solution"+"\n"+str(a.reshape(3,1))+"\n" + "Winning conditions fullfilled (Odd quantitude of 1)?: "+str(winning_alice)+"\n")
    print("Bob's row solution"+"\n"+str(b)+"\n"+ "Winning conditions fullfilled (Even quantitude of 1)?: "+str(winning_bob)+"\n")
    print("Create matrix to show results"+"\n")
    k = np.empty((3,3,))
    k[:] = np.nan
    k[:,col-1] = a
    k[row-1,:] = b
    print(k)
    print("------------------------------------------")  
    print("------------------------------------------") 
    
    return str(a.reshape(3,1)), str(b)

def get_state_accuracy(counts): # funciton to calculate state accuracy
    expected_counts = 0
    for state in counts.keys():
        if state in expected_states:
            expected_counts = expected_counts + counts[state]
    state_accuracy = expected_counts / shots
    return str(state_accuracy*100)+"%"

#The following function sets up the initial entanglement between Alice and Bob
def share_bell_state(qc,a,b,c,d): 
    qc.h(a)
    qc.h(b)
    qc.cx(a,c)
    qc.cx(b,d)
    
# The following functions represent the U(gamma) and V(gamma) controlled Cliffords.
def U(qc,gamma,a,b):
    if gamma==1:
        qc.h(a)
        qc.i(b)
    elif gamma==2:
        qc.swap(a,b)
        qc.h(a)
        qc.i(b)

    elif gamma==3:
        qc.cx(a,b)
        qc.h(a)
        qc.i(b)

def V(qc,gamma,a,b):
    if gamma==1:
        qc.h(a)
        qc.h(b)
    if gamma==2:
        qc.swap(a,b)
    elif gamma==3:
        qc.z(a)
        qc.z(b)
        qc.cz(a,b)
        qc.h(a)
        qc.h(b)


def get_non_local_outcome(alpha, beta):
    #We will ask the user to select the row and column on Alice and Bob's behalf.
    alpha = int(alpha)
    beta = int(beta)

    #Create the quantum register and the classical register to store our final bit values
    aliceQR = QuantumRegister(2)
    x1CR = ClassicalRegister(1)
    x2CR = ClassicalRegister(1)
    bobQR = QuantumRegister(2)
    y1CR = ClassicalRegister(1)
    y2CR = ClassicalRegister(1)

    #Create the circuit
    magicsquare_circuit = QuantumCircuit(aliceQR,bobQR,x1CR,x2CR,y1CR,y2CR)

    #Generate the Bell state on the circuit
    share_bell_state(magicsquare_circuit,0,1,2,3)

    magicsquare_circuit.barrier()

    #Draw the rest of the circuit based on Alice and Bob's selection   
    if 4>alpha>0 and 4>beta>0:
        U(magicsquare_circuit,alpha,0,1) 
        V(magicsquare_circuit,beta,2,3)
        magicsquare_circuit.barrier()
        magicsquare_circuit.measure(0,0)
        magicsquare_circuit.measure(1,1)
        magicsquare_circuit.measure(2,2)
        magicsquare_circuit.measure(3,3)
        
        magicsquare_circuit.draw(output='mpl')
        # print(magicsquare_circuit)

        backend = BasicAer.get_backend('qasm_simulator') # define the backend
        job = execute(magicsquare_circuit, backend, shots=1) # run the job simulation
        results = job.result().get_counts()
        print(results)
        col, row = check_result(results, alpha, beta)
        
        print(col)
        print(row)
        
        return(results)
    
results = get_non_local_outcome(1, 2)
# print(results)