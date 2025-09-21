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
    
    # Inicializar: |01⟩
    program += X(1)
    program += H(0)
    program += H(1)
    
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
        
        # ACESSO CORRETO: resultado é um objeto, não array direto
        # Precisamos acessar a propriedade correta
        if hasattr(resultado, 'readout_data'):
            # Tentativa 1: readout_data
            dados = resultado.readout_data
            print("✅ Usando readout_data")
        elif hasattr(resultado, 'result_data'):
            # Tentativa 2: result_data
            dados = resultado.result_data
            print("✅ Usando result_data")
        else:
            # Tentativa 3: inspecionar o objeto
            print("🔍 Inspecionando objeto resultado...")
            print(f"Atributos: {[attr for attr in dir(resultado) if not attr.startswith('_')]}")
            dados = None
        
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
        
        # Se não conseguimos extrair, tentar método alternativo
        print("🔄 Tentando método alternativo de extração...")
        return executar_deutsch_alternativo(funcao, num_shots)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def executar_deutsch_alternativo(funcao, num_shots=100):
    """Método alternativo mais simples"""
    print("🔄 Usando método alternativo...")
    
    try:
        qc = get_qc('2q-qvm')
        
        # Circuito mais simples para debug
        program = Program()
        program.declare('ro', 'BIT', 1)
        program += X(0)
        program.measure(0, MemoryReference('ro', 0))
        
        compilado = qc.compile(program)
        resultado = qc.run(compilado, trials=num_shots)
        
        print(f"🔍 Resultado alternativo: {resultado}")
        print(f"Tipo: {type(resultado)}")
        
        # Tentar converter para string e analisar
        resultado_str = str(resultado)
        print(f"Como string: {resultado_str}")
        
        # Contar manualmente '1's e '0's
        uns = resultado_str.count('1')
        zeros = resultado_str.count('0')
        
        print(f"Zeros: {zeros}, Uns: {uns}")
        
        return "debug"
        
    except Exception as e:
        print(f"❌ Erro no método alternativo: {e}")
        return None

def teste_debug():
    """Teste simples para debug do formato de resultado"""
    print("🐛 TESTE DE DEBUG - Formato do Resultado")
    print("=" * 50)
    
    try:
        qc = get_qc('1q-qvm')
        
        program = Program()
        program.declare('ro', 'BIT', 1)
        program += X(0)  # Coloca em |1⟩
        program.measure(0, MemoryReference('ro', 0))
        
        compilado = qc.compile(program)
        resultado = qc.run(compilado, trials=5)
        
        print("🔍 ANALISANDO OBJETO RESULTADO:")
        print(f"Representação: {resultado}")
        
        # Listar todos os atributos públicos
        atributos = [attr for attr in dir(resultado) if not attr.startswith('_')]
        print(f"Atributos: {atributos}")
        
        # Testar atributos comuns
        for attr in atributos:
            try:
                valor = getattr(resultado, attr)
                print(f"{attr}: {type(valor)} = {valor}")
            except:
                print(f"{attr}: <erro ao acessar>")
                
    except Exception as e:
        print(f"❌ Erro no debug: {e}")

# Executar
if __name__ == "__main__":
    print("🎯 ALGORITMO DE DEUTSCH - Versão Debug")
    print("=" * 60)
    
    # Depois testar o algoritmo
    funcao = {0: 1, 1: 0}  # NOT - balanceada
    resultado = executar_deutsch(funcao, num_shots=10)
    
    print(f"\n🎯 Esperado: BALANCEADA")
    print(f"📋 Obtido: {resultado}")