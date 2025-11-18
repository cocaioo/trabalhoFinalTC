"""
conversor.py - Módulo de conversão de ER para AFN-ε

Trabalho Final - Teoria da Computação
TEMA 1: Conversão de Expressão Regular para AFN-ε
"""

from afn import Estado, AFN


class ConversorERparaAFN:
    """Converte Expressão Regular para AFN-ε usando o Algoritmo de Thompson"""
    
    def __init__(self, expressao_regular):
        self.er = expressao_regular
        self.posicao = 0
    
    def converter(self):
        """Converte a expressão regular em AFN-ε"""
        Estado.contador = 0  # Reinicia contador de estados
        return self._expressao()
    
    def _proximo_char(self):
        """Retorna o próximo caractere sem avançar"""
        if self.posicao < len(self.er):
            return self.er[self.posicao]
        return None
    
    def _consumir_char(self):
        """Consome e retorna o próximo caractere"""
        char = self._proximo_char()
        self.posicao += 1
        return char
    
    def _expressao(self):
        """Processa união (|)"""
        termo = self._termo()
        
        if self._proximo_char() == '|':
            self._consumir_char()  # consome '|'
            expressao_direita = self._expressao()
            return self._uniao(termo, expressao_direita)
        
        return termo
    
    def _termo(self):
        """Processa concatenação"""
        fator = self._fator()
        
        proximo = self._proximo_char()
        if proximo and proximo not in ['|', ')', None]:
            termo_direita = self._termo()
            return self._concatenacao(fator, termo_direita)
        
        return fator
    
    def _fator(self):
        """Processa fechamento de Kleene (*)"""
        base = self._base()
        
        if self._proximo_char() == '*':
            self._consumir_char()  # consome '*'
            return self._fechamento(base)
        
        return base
    
    def _base(self):
        """Processa símbolos básicos e parênteses"""
        char = self._proximo_char()
        
        if char == '(':
            self._consumir_char()  # consome '('
            expressao = self._expressao()
            self._consumir_char()  # consome ')'
            return expressao
        
        # Símbolo simples
        simbolo = self._consumir_char()
        return self._simbolo(simbolo)
    
    def _simbolo(self, simbolo):
        """Cria AFN para um símbolo simples"""
        inicial = Estado()
        final = Estado()
        inicial.adicionar_transicao(simbolo, final)
        return AFN(inicial, final)
    
    def _concatenacao(self, afn1, afn2):
        """Concatena dois AFNs"""
        afn1.estado_final.eh_final = False
        afn1.estado_final.adicionar_transicao('ε', afn2.estado_inicial)
        return AFN(afn1.estado_inicial, afn2.estado_final)
    
    def _uniao(self, afn1, afn2):
        """Une dois AFNs"""
        novo_inicial = Estado()
        novo_final = Estado()
        
        novo_inicial.adicionar_transicao('ε', afn1.estado_inicial)
        novo_inicial.adicionar_transicao('ε', afn2.estado_inicial)
        
        afn1.estado_final.eh_final = False
        afn2.estado_final.eh_final = False
        
        afn1.estado_final.adicionar_transicao('ε', novo_final)
        afn2.estado_final.adicionar_transicao('ε', novo_final)
        
        return AFN(novo_inicial, novo_final)
    
    def _fechamento(self, afn):
        """Aplica fechamento de Kleene (*)"""
        novo_inicial = Estado()
        novo_final = Estado()
        
        novo_inicial.adicionar_transicao('ε', afn.estado_inicial)
        novo_inicial.adicionar_transicao('ε', novo_final)
        
        afn.estado_final.eh_final = False
        
        afn.estado_final.adicionar_transicao('ε', afn.estado_inicial)
        afn.estado_final.adicionar_transicao('ε', novo_final)
        
        return AFN(novo_inicial, novo_final)