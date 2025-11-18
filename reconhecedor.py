class ReconhecedorAFN:
    def __init__(self, afn):
        self.afn = afn
        self.historico = []

    def _epsilon_fecho(self, estados):
        fecho = set(estados)
        pilha = list(estados)

        while pilha:
            estado = pilha.pop()

            if 'ε' in estado.transicoes:
                for destino in estado.transicoes['ε']:
                    if destino not in fecho:
                        fecho.add(destino)
                        pilha.append(destino)

        return fecho

    def reconhecer(self, cadeia):
        self.historico = []

        estados_atuais = self._epsilon_fecho([self.afn.estado_inicial])

        self.historico.append({
            'passo': 'Inicial',
            'simbolo': '',
            'estados': sorted(estados_atuais, key=lambda x: x.id)
        })

        for i, simbolo in enumerate(cadeia):
            novos_estados = set()

            for estado in estados_atuais:
                if simbolo in estado.transicoes:
                    novos_estados.update(estado.transicoes[simbolo])

            estados_atuais = self._epsilon_fecho(novos_estados)

            self.historico.append({
                'passo': f'Após ler {i+1}',
                'simbolo': simbolo,
                'estados': sorted(estados_atuais, key=lambda x: x.id)
            })

            if not estados_atuais:
                return False, "Nenhum estado alcançável"

        for estado in estados_atuais:
            if estado.eh_final:
                return True, f"Estado final {estado} alcançado"

        return False, "Nenhum estado final alcançado"

    def obter_historico_texto(self):
        resultado = []
        for item in self.historico:
            estados_str = ', '.join(str(e) for e in item['estados'])
            if item['passo'] == 'Inicial':
                resultado.append(f"{item['passo']}: {{{estados_str}}}")
            else:
                resultado.append(f"{item['passo']} '{item['simbolo']}': {{{estados_str}}}")
        return '\n'.join(resultado)