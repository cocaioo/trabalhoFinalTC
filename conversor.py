from afn import Estado, AFN


class ConversorERparaAFN:
    def __init__(self, expressao_regular):
        self.er = expressao_regular
        self.posicao = 0

    def converter(self):
        Estado.contador = 0
        return self._expressao()

    def _proximo_char(self):
        if self.posicao < len(self.er):
            return self.er[self.posicao]
        return None

    def _consumir_char(self):
        char = self._proximo_char()
        self.posicao += 1
        return char

    def _expressao(self):
        termo = self._termo()

        if self._proximo_char() == '|':
            self._consumir_char()
            expressao_direita = self._expressao()
            return self._uniao(termo, expressao_direita)

        return termo

    def _termo(self):
        fator = self._fator()

        proximo = self._proximo_char()
        if proximo and proximo not in ['|', ')', None]:
            termo_direita = self._termo()
            return self._concatenacao(fator, termo_direita)

        return fator

    def _fator(self):
        base = self._base()

        if self._proximo_char() == '*':
            self._consumir_char()
            return self._fechamento(base)

        return base

    def _base(self):
        char = self._proximo_char()

        if char == '(':
            self._consumir_char()
            expressao = self._expressao()
            self._consumir_char()
            return expressao

        simbolo = self._consumir_char()
        return self._simbolo(simbolo)

    def _simbolo(self, simbolo):
        inicial = Estado()
        final = Estado()
        inicial.adicionar_transicao(simbolo, final)
        return AFN(inicial, final)

    def _concatenacao(self, afn1, afn2):
        afn1.estado_final.eh_final = False
        afn1.estado_final.adicionar_transicao('ε', afn2.estado_inicial)
        return AFN(afn1.estado_inicial, afn2.estado_final)

    def _uniao(self, afn1, afn2):
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
        novo_inicial = Estado()
        novo_final = Estado()

        novo_inicial.adicionar_transicao('ε', afn.estado_inicial)
        novo_inicial.adicionar_transicao('ε', novo_final)

        afn.estado_final.eh_final = False

        afn.estado_final.adicionar_transicao('ε', afn.estado_inicial)
        afn.estado_final.adicionar_transicao('ε', novo_final)

        return AFN(novo_inicial, novo_final)