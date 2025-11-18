class Estado:
    contador = 0

    def __init__(self):
        self.id = Estado.contador
        Estado.contador += 1
        self.transicoes = {}
        self.eh_final = False

    def adicionar_transicao(self, simbolo, estado_destino):
        if simbolo not in self.transicoes:
            self.transicoes[simbolo] = []
        self.transicoes[simbolo].append(estado_destino)

    def __repr__(self):
        return f"q{self.id}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Estado) and self.id == other.id


class AFN:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        estado_final.eh_final = True

    def obter_todos_estados(self):
        visitados = set()
        pilha = [self.estado_inicial]

        while pilha:
            estado = pilha.pop()
            if estado in visitados:
                continue
            visitados.add(estado)

            for simbolo, destinos in estado.transicoes.items():
                for destino in destinos:
                    if destino not in visitados:
                        pilha.append(destino)

        return sorted(visitados, key=lambda e: e.id)

    def obter_transicoes(self):
        transicoes = []
        estados = self.obter_todos_estados()

        for estado in estados:
            for simbolo, destinos in estado.transicoes.items():
                for destino in destinos:
                    transicoes.append((estado, simbolo, destino))

        return transicoes

    def exibir_texto(self):
        estados = self.obter_todos_estados()

        resultado = []
        resultado.append("="*60)
        resultado.append("ESTRUTURA DO AFN-ε")
        resultado.append("="*60)
        resultado.append(f"Estado Inicial: {self.estado_inicial}")
        resultado.append(f"Estado Final: {self.estado_final}")
        resultado.append(f"\nTotal de Estados: {len(estados)}")
        resultado.append("\nTransições:")
        resultado.append("-"*60)

        for estado in estados:
            marcador = " (INICIAL)" if estado == self.estado_inicial else ""
            marcador += " (FINAL)" if estado.eh_final else ""
            resultado.append(f"\n{estado}{marcador}:")

            if not estado.transicoes:
                resultado.append("  (sem transições)")
            else:
                for simbolo, destinos in sorted(estado.transicoes.items()):
                    destinos_str = ", ".join(str(d) for d in destinos)
                    simbolo_exibir = "ε" if simbolo == "ε" else simbolo
                    resultado.append(f"  {simbolo_exibir} → {destinos_str}")

        resultado.append("="*60)
        return "\n".join(resultado)