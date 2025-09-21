from pyquil import Program, get_qc
from pyquil.gates import H, X, CNOT
from pyquil.quilatom import MemoryReference
import numpy as np

def deutsch_algorithm(funcao):
    print("=" * 50)
    print(f"Analisando função: f(0)={funcao[0]}, f(1)={funcao[1]}")
    print("=" * 50)
    
    program = Program() # Cria um novo programa Quil
    program.declare('ro', 'BIT', 2) # Declara registradores clássicos
    
    # Estado inicial: |01⟩
    program += X(1) # Aplica X no qubit 1: |0⟩ → |1⟩
    program += H(0) # Aplica Hadamart no qubit 0: |0⟩ → (|0⟩ + |1⟩)/√2
    program += H(1) # Aplica Hadamart no qubit 1: |1⟩ → (|0⟩ - |1⟩)/√2
    
    # Oracle - funções possíveis
    if funcao == {0: 0, 1: 0}:       # Constante 0 - f(0) = 0, f(1) = 0
        print("Oracle: Função constante 0")
        pass

    elif funcao == {0: 1, 1: 1}:     # Constante 1 - f(0) = 1, f(1) = 1
        print("Oracle: Função constante 1")
        program += X(1)
        
    elif funcao == {0: 0, 1: 1}:     # Identidade - f(0) = 0, f(1) = 1
        print("Oracle: Função identidade")
        program += CNOT(0, 1)
        
    elif funcao == {0: 1, 1: 0}:     # NOT - f(0) = 1, f(1) = 0
        print("Oracle: Função NOT")
        program += X(0)
        program += CNOT(0, 1)
        program += X(0)
    
    program += H(0)
    program.measure(0, MemoryReference('ro', 0))
    
    return program

def executar_deutsch(funcao, num_shots):
    
    circuito = deutsch_algorithm(funcao)
    
    qc = get_qc('2q-qvm')
    compilado = qc.compile(circuito)
        
    resultado = qc.run(compilado, trials=num_shots)
        
    print(f"Resultados ({num_shots} execuções):")
        
    dados = resultado.readout_data
        
    if dados is not None:    
        resultados_array = dados['ro']
                
        primeiro_qubit = resultados_array[:, 0]
        zeros = np.sum(primeiro_qubit == 0)
        uns = np.sum(primeiro_qubit == 1)
                    
        if uns > zeros:
            return "balanceada"
        else:
            return "constante"

# Testando o algoritmo -  constante
funcaoConst0 = {0: 0, 1: 0}  # constante 0
resultado = executar_deutsch(funcaoConst0, num_shots=10)
    
print(f"\nEsperado: CONSTANTE")
print(f"Obtido: {resultado}")

funcaoConst1 = {0: 1, 1: 1}  # constante 1
resultado = executar_deutsch(funcaoConst1, num_shots=10)
    
print(f"\nEsperado: CONSTANTE")
print(f"Obtido: {resultado}")
    
# Testando o algoritmo - balanceada
funcaoIdentidade = {0: 0, 1: 1}  # Identidade - balanceada
resultado = executar_deutsch(funcaoIdentidade, num_shots=10)
    
print(f"\nEsperado: BALANCEADA")
print(f"Obtido: {resultado}")

funcaoNOT = {0: 1, 1: 0}  # NOT - balanceada
resultado = executar_deutsch(funcaoNOT, num_shots=10)
    
print(f"\nEsperado: BALANCEADA")
print(f"Obtido: {resultado}")
