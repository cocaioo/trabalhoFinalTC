"""
visualizador.py - Módulo de visualização gráfica do AFN-ε

Trabalho Final - Teoria da Computação
TEMA 1: Conversão de Expressão Regular para AFN-ε
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import math


class VisualizadorAFN:
    """Visualiza graficamente um AFN-ε"""
    
    def __init__(self, afn):
        self.afn = afn
        self.posicoes = {}
    
    def _calcular_posicoes(self):
        """Calcula posições dos estados usando layout em camadas"""
        estados = self.afn.obter_todos_estados()
        
        # Organiza estados em níveis (BFS)
        niveis = {}
        visitados = set()
        fila = [(self.afn.estado_inicial, 0)]
        
        while fila:
            estado, nivel = fila.pop(0)
            if estado in visitados:
                continue
            
            visitados.add(estado)
            if nivel not in niveis:
                niveis[nivel] = []
            niveis[nivel].append(estado)
            
            for simbolo, destinos in estado.transicoes.items():
                for destino in destinos:
                    if destino not in visitados:
                        fila.append((destino, nivel + 1))
        
        # Calcula posições
        max_nivel = max(niveis.keys()) if niveis else 0
        largura = 10
        altura = 6
        
        for nivel, estados_nivel in niveis.items():
            n = len(estados_nivel)
            x = (nivel / max(max_nivel, 1)) * largura
            
            for i, estado in enumerate(estados_nivel):
                if n == 1:
                    y = altura / 2
                else:
                    y = (i / (n - 1)) * altura
                
                self.posicoes[estado] = (x, y)
        
        return self.posicoes
    
    def visualizar(self, titulo="AFN-ε"):
        """Cria visualização gráfica do autômato"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 7)
        ax.axis('off')
        
        # Calcula posições
        self._calcular_posicoes()
        
        # Desenha transições primeiro (para ficarem atrás dos estados)
        transicoes_desenhadas = {}
        
        for origem, simbolo, destino in self.afn.obter_transicoes():
            pos_origem = self.posicoes[origem]
            pos_destino = self.posicoes[destino]
            
            # Agrupa transições entre mesmos estados
            chave = (origem.id, destino.id)
            if chave not in transicoes_desenhadas:
                transicoes_desenhadas[chave] = []
            transicoes_desenhadas[chave].append(simbolo)
        
        # Desenha as transições agrupadas
        for (origem_id, destino_id), simbolos in transicoes_desenhadas.items():
            # Encontra os estados
            origem = next(e for e in self.posicoes.keys() if e.id == origem_id)
            destino = next(e for e in self.posicoes.keys() if e.id == destino_id)
            
            pos_origem = self.posicoes[origem]
            pos_destino = self.posicoes[destino]
            
            # Junta símbolos
            label = ', '.join('ε' if s == 'ε' else s for s in simbolos)
            
            # Auto-loop
            if origem == destino:
                circle = Circle(
                    (pos_origem[0], pos_origem[1] + 0.5),
                    0.3,
                    fill=False,
                    edgecolor='black',
                    linewidth=1.5
                )
                ax.add_patch(circle)
                ax.text(
                    pos_origem[0], pos_origem[1] + 1.0,
                    label,
                    ha='center', va='bottom',
                    fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none')
                )
            else:
                # Calcula ângulo e posições ajustadas
                dx = pos_destino[0] - pos_origem[0]
                dy = pos_destino[1] - pos_origem[1]
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist > 0:
                    # Ajusta para começar/terminar na borda dos círculos
                    raio = 0.35
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    
                    x1 = pos_origem[0] + dx_norm * raio
                    y1 = pos_origem[1] + dy_norm * raio
                    x2 = pos_destino[0] - dx_norm * raio
                    y2 = pos_destino[1] - dy_norm * raio
                    
                    import matplotlib.pyplot as plt
                    from matplotlib.patches import FancyArrowPatch, Circle
                    import math


                    class VisualizadorAFN:
                        def __init__(self, afn):
                            self.afn = afn
                            self.posicoes = {}

                        def _calcular_posicoes(self):
                            estados = self.afn.obter_todos_estados()

                            niveis = {}
                            visitados = set()
                            fila = [(self.afn.estado_inicial, 0)]

                            while fila:
                                estado, nivel = fila.pop(0)
                                if estado in visitados:
                                    continue

                                visitados.add(estado)
                                if nivel not in niveis:
                                    niveis[nivel] = []
                                niveis[nivel].append(estado)

                                for simbolo, destinos in estado.transicoes.items():
                                    for destino in destinos:
                                        if destino not in visitados:
                                            fila.append((destino, nivel + 1))

                            max_nivel = max(niveis.keys()) if niveis else 0
                            largura = 10
                            altura = 6

                            for nivel, estados_nivel in niveis.items():
                                n = len(estados_nivel)
                                x = (nivel / max(max_nivel, 1)) * largura

                                for i, estado in enumerate(estados_nivel):
                                    if n == 1:
                                        y = altura / 2
                                    else:
                                        y = (i / (n - 1)) * altura

                                    self.posicoes[estado] = (x, y)

                            return self.posicoes

                        def visualizar(self, titulo="AFN-ε"):
                            fig, ax = plt.subplots(figsize=(14, 8))
                            ax.set_xlim(-1, 11)
                            ax.set_ylim(-1, 7)
                            ax.axis('off')

                            self._calcular_posicoes()

                            transicoes_desenhadas = {}

                            for origem, simbolo, destino in self.afn.obter_transicoes():
                                pos_origem = self.posicoes[origem]
                                pos_destino = self.posicoes[destino]

                                chave = (origem.id, destino.id)
                                if chave not in transicoes_desenhadas:
                                    transicoes_desenhadas[chave] = []
                                transicoes_desenhadas[chave].append(simbolo)

                            for (origem_id, destino_id), simbolos in transicoes_desenhadas.items():
                                origem = next(e for e in self.posicoes.keys() if e.id == origem_id)
                                destino = next(e for e in self.posicoes.keys() if e.id == destino_id)

                                pos_origem = self.posicoes[origem]
                                pos_destino = self.posicoes[destino]

                                label = ', '.join('ε' if s == 'ε' else s for s in simbolos)

                                if origem == destino:
                                    circle = Circle((pos_origem[0], pos_origem[1] + 0.5), 0.3, fill=False, edgecolor='black', linewidth=1.5)
                                    ax.add_patch(circle)
                                    ax.text(
                                        pos_origem[0], pos_origem[1] + 1.0,
                                        label,
                                        ha='center', va='bottom',
                                        fontsize=10,
                                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none')
                                    )
                                else:
                                    dx = pos_destino[0] - pos_origem[0]
                                    dy = pos_destino[1] - pos_origem[1]
                                    dist = math.sqrt(dx**2 + dy**2)

                                    if dist > 0:
                                        raio = 0.35
                                        dx_norm = dx / dist
                                        dy_norm = dy / dist

                                        x1 = pos_origem[0] + dx_norm * raio
                                        y1 = pos_origem[1] + dy_norm * raio
                                        x2 = pos_destino[0] - dx_norm * raio
                                        y2 = pos_destino[1] - dy_norm * raio

                                        arrow = FancyArrowPatch(
                                            (x1, y1), (x2, y2),
                                            arrowstyle='->,head_width=0.4,head_length=0.8',
                                            color='black',
                                            linewidth=1.5,
                                            connectionstyle="arc3,rad=0.1"
                                        )
                                        ax.add_patch(arrow)

                                        mid_x = (pos_origem[0] + pos_destino[0]) / 2
                                        mid_y = (pos_origem[1] + pos_destino[1]) / 2

                                        ax.text(
                                            mid_x, mid_y + 0.2,
                                            label,
                                            ha='center', va='bottom',
                                            fontsize=10,
                                            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none')
                                        )

                            for estado, (x, y) in self.posicoes.items():
                                cor = 'lightgreen' if estado == self.afn.estado_inicial else 'lightblue'

                                circle = Circle((x, y), 0.35, color=cor, ec='black', linewidth=2, zorder=10)
                                ax.add_patch(circle)

                                if estado.eh_final:
                                    circle2 = Circle((x, y), 0.28, fill=False, ec='black', linewidth=2, zorder=11)
                                    ax.add_patch(circle2)

                                ax.text(x, y, str(estado), ha='center', va='center', fontsize=12, fontweight='bold', zorder=12)

                            pos_inicial = self.posicoes[self.afn.estado_inicial]
                            arrow_start = FancyArrowPatch(
                                (pos_inicial[0] - 1, pos_inicial[1]),
                                (pos_inicial[0] - 0.4, pos_inicial[1]),
                                arrowstyle='->,head_width=0.4,head_length=0.8',
                                color='green',
                                linewidth=2.5,
                                zorder=5
                            )
                            ax.add_patch(arrow_start)

                            ax.text(0.5, 6.5, titulo, fontsize=16, fontweight='bold', ha='left')
                            ax.text(0.5, 6.1, '● Verde: Estado Inicial  ● Azul: Estados  ◎ Círculo Duplo: Estado Final', fontsize=10, ha='left')

                            plt.tight_layout()
                            return fig