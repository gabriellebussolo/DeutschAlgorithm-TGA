#!/usr/bin/env python3
"""
ALGORITMO DE DEUTSCH - Corrigido para QAMExecutionResult
"""

from pyquil import Program, get_qc
from pyquil.gates import H, X, CNOT
from pyquil.quilatom import MemoryReference
import numpy as np

def deutsch_algorithm(funcao):
    """Implementa o algoritmo de Deutsch"""
    print(f"🔍 Analisando função: f(0)={funcao[0]}, f(1)={funcao[1]}")
    print("=" * 50)
    
    program = Program()
    program.declare('ro', 'BIT', 2)
    
    # Estado inicial: |01⟩
    program += X(1) # Aplica X no qubit 1: |0⟩ → |1⟩
    program += H(0) # Aplica Hadamart no qubit 0: |0⟩ → (|0⟩ + |1⟩)/√2
    program += H(1) # Aplica Hadamart no qubit 1: |1⟩ → (|0⟩ - |1⟩)/√2
    
    # Oracle
    if funcao == {0: 0, 1: 0}:       # Constante 0
        print("📦 Oracle: Função constante 0")
        pass
        
    elif funcao == {0: 1, 1: 1}:     # Constante 1
        print("📦 Oracle: Função constante 1")
        program += X(1)
        
    elif funcao == {0: 0, 1: 1}:     # Identidade
        print("📦 Oracle: Função identidade")
        program += CNOT(0, 1)
        
    elif funcao == {0: 1, 1: 0}:     # NOT
        print("📦 Oracle: Função NOT")
        program += X(0)
        program += CNOT(0, 1)
        program += X(0)
    
    program += H(0)
    program.measure(0, MemoryReference('ro', 0))
    
    return program

def executar_deutsch(funcao, num_shots=100):
    """Executa o algoritmo com acesso correto aos dados"""
    
    circuito = deutsch_algorithm(funcao)
    
    try:
        qc = get_qc('2q-qvm')
        compilado = qc.compile(circuito)
        
        # O resultado é QAMExecutionResult, precisamos extrair os dados
        resultado = qc.run(compilado, trials=num_shots)
        
        print(f"📊 Resultados ({num_shots} execuções):")
        
        dados = resultado.readout_data
        
        if dados is not None:
            print(f"Dados extraídos: {dados}")
            
            # Se for um dicionário com 'ro'
            if hasattr(dados, 'get') and 'ro' in dados:
                resultados_array = dados['ro']
                print(f"Array de resultados: {resultados_array}")
                
                if hasattr(resultados_array, 'shape'):
                    primeiro_qubit = resultados_array[:, 0]
                    zeros = np.sum(primeiro_qubit == 0)
                    uns = np.sum(primeiro_qubit == 1)
                    
                    print(f"\n🎯 Distribuição:")
                    print(f"|0⟩: {zeros} vezes ({zeros/num_shots*100:.1f}%)")
                    print(f"|1⟩: {uns} vezes ({uns/num_shots*100:.1f}%)")
                    
                    if uns > zeros * 2:
                        print("✅ BALANCEADA")
                        return "balanceada"
                    else:
                        print("✅ CONSTANTE")
                        return "constante"
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

# Executar
if __name__ == "__main__":
    print("🎯 ALGORITMO DE DEUTSCH")
    print("=" * 60)
    
    # Depois testar o algoritmo
    funcao = {0: 1, 1: 0}  # NOT - balanceada
    resultado = executar_deutsch(funcao, num_shots=10)
    
    print(f"\n🎯 Esperado: BALANCEADA")
    print(f"📋 Obtido: {resultado}")