"""
main_terminal.py - Versão terminal (original)

Trabalho Final - Teoria da Computação
TEMA 1: Conversão de Expressão Regular para AFN-ε
"""

from afn import Estado
from conversor import ConversorERparaAFN
from reconhecedor import ReconhecedorAFN


def main():
    """Função principal do programa em modo terminal"""
    print("="*60)
    print("CONVERSOR DE EXPRESSÃO REGULAR PARA AFN-ε")
    print("Trabalho Final - Teoria da Computação")
    print("="*60)
    
    print("\nNotação suportada:")
    print("  • Concatenação: ab (símbolos adjacentes)")
    print("  • União: a|b")
    print("  • Fechamento de Kleene: a*")
    print("  • Parênteses: (a|b)*")
    print("  • Símbolos: letras, dígitos e caracteres especiais")
    
    # Entrada da expressão regular
    print("\n" + "-"*60)
    expressao = input("Digite a expressão regular: ").strip()
    
    if not expressao:
        print("Erro: Expressão vazia!")
        return
    
    try:
        # Converte ER para AFN-ε
        print(f"\nConvertendo ER '{expressao}' para AFN-ε...")
        conversor = ConversorERparaAFN(expressao)
        afn = conversor.converter()
        
        # Exibe o AFN-ε
        print(afn.exibir_texto())
        
        # Reconhecimento de cadeias
        print("\n" + "="*60)
        print("RECONHECIMENTO DE CADEIAS")
        print("="*60)
        print("Digite as cadeias para testar (uma por linha)")
        print("Digite 'fim' para encerrar\n")
        
        reconhecedor = ReconhecedorAFN(afn)
        
        while True:
            cadeia = input("Cadeia: ").strip()
            
            if cadeia.lower() == 'fim':
                break
            
            print(f"\nProcessando cadeia: '{cadeia}'")
            print("-"*60)
            aceita, motivo = reconhecedor.reconhecer(cadeia)
            print(reconhecedor.obter_historico_texto())
            
            if aceita:
                print(f"\n✓ ACEITA - {motivo}")
            else:
                print(f"\n✗ REJEITADA - {motivo}")
            print()
    
    except Exception as e:
        print(f"\nErro ao processar: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()