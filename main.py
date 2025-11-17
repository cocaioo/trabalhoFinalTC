class GrammarCNF:
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.productions = {}
        self.start_symbol = None
        self.new_var_counter = 0

    def add_production(self, left, right):
        if left not in self.productions:
            self.productions[left] = []
        self.productions[left].append(right)
        self.non_terminals.add(left)

        for symbol in right:
            if symbol.isupper():
                self.non_terminals.add(symbol)
            elif symbol != 'ε':
                self.terminals.add(symbol)

    def set_start_symbol(self, symbol):
        self.start_symbol = symbol

    def generate_new_variable(self):
        while True:
            new_var = f"X{self.new_var_counter}"
            self.new_var_counter += 1
            if new_var not in self.non_terminals:
                self.non_terminals.add(new_var)
                return new_var

    def print_grammar(self, title="Gramática"):
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(f"Símbolo Inicial: {self.start_symbol}")
        print(f"Não-terminais: {sorted(self.non_terminals)}")
        print(f"Terminais: {sorted(self.terminals)}")
        print("\nProduções:")
        for left in sorted(self.productions.keys()):
            for right in self.productions[left]:
                right_str = ''.join(right) if right != ['ε'] else 'ε'
                print(f"  {left} → {right_str}")
        print(f"{'='*60}\n")

    def remove_epsilon_productions(self):
        print("Passo 1: Removendo produções ε...")

        nullable = set()
        changed = True
        while changed:
            changed = False
            for left, rights in self.productions.items():
                if left not in nullable:
                    for right in rights:
                        if right == ['ε'] or all(symbol in nullable for symbol in right):
                            nullable.add(left)
                            changed = True
                            break

        print(f"Variáveis anuláveis: {nullable}")

        new_productions = {}
        for left, rights in self.productions.items():
            new_productions[left] = []
            for right in rights:
                if right == ['ε']:
                    continue

                combinations = self._generate_combinations(right, nullable)
                for combo in combinations:
                    if combo and combo not in new_productions[left]:
                        new_productions[left].append(combo)

        if self.start_symbol in nullable:
            new_start = self.generate_new_variable()
            new_productions[new_start] = [[self.start_symbol], ['ε']]
            self.start_symbol = new_start

        self.productions = new_productions

    def _generate_combinations(self, production, nullable):
        if not production:
            return [[]]

        result = []
        first = production[0]
        rest_combinations = self._generate_combinations(production[1:], nullable)

        for combo in rest_combinations:
            result.append([first] + combo)
            if first in nullable:
                result.append(combo)

        return result

    def remove_unit_productions(self):
        print("Passo 2: Removendo produções unitárias...")

        unit_pairs = {}
        for var in self.non_terminals:
            unit_pairs[var] = {var}

        changed = True
        while changed:
            changed = False
            for left in self.non_terminals:
                for right in self.productions.get(left, []):
                    if len(right) == 1 and right[0] in self.non_terminals:
                        B = right[0]
                        for C in unit_pairs[B]:
                            if C not in unit_pairs[left]:
                                unit_pairs[left].add(C)
                                changed = True

        new_productions = {}
        for left in self.non_terminals:
            new_productions[left] = []
            for B in unit_pairs[left]:
                for right in self.productions.get(B, []):
                    if not (len(right) == 1 and right[0] in self.non_terminals):
                        if right not in new_productions[left]:
                            new_productions[left].append(right)

        self.productions = new_productions

    def convert_to_cnf(self):
        print("Passo 3: Convertendo para Forma Normal de Chomsky...")

        terminal_vars = {}
        for terminal in self.terminals:
            new_var = self.generate_new_variable()
            terminal_vars[terminal] = new_var
            self.productions[new_var] = [[terminal]]

        new_productions = {}
        for left, rights in self.productions.items():
            new_productions[left] = []
            for right in rights:
                if len(right) == 1:
                    new_productions[left].append(right)
                elif len(right) == 2:
                    new_right = []
                    for symbol in right:
                        if symbol in self.terminals:
                            new_right.append(terminal_vars[symbol])
                        else:
                            new_right.append(symbol)
                    new_productions[left].append(new_right)
                else:
                    new_right = []
                    for symbol in right:
                        if symbol in self.terminals:
                            new_right.append(terminal_vars[symbol])
                        else:
                            new_right.append(symbol)

                    current = new_right[0]
                    for i in range(1, len(new_right) - 1):
                        new_var = self.generate_new_variable()
                        new_productions[new_var] = [[current, new_right[i]]]
                        current = new_var
                    new_productions[left].append([current, new_right[-1]])

        self.productions = new_productions

    def to_cnf(self):
        print("\n" + "="*60)
        print("CONVERSÃO PARA FORMA NORMAL DE CHOMSKY")
        print("="*60)

        self.print_grammar("Gramática Original")
        self.remove_epsilon_productions()
        self.print_grammar("Após remover produções ε")
        self.remove_unit_productions()
        self.print_grammar("Após remover produções unitárias")
        self.convert_to_cnf()
        self.print_grammar("Gramática em Forma Normal de Chomsky (FNC)")


class CYKParser:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, string):
        print(f"\n{'='*60}")
        print(f"ALGORITMO CYK - Reconhecimento da cadeia: '{string}'")
        print(f"{'='*60}\n")

        if not string:
            accepts_empty = any(['ε'] in prods for prods in self.grammar.productions.values())
            print("Cadeia vazia")
            print(f"Resultado: {'ACEITA' if accepts_empty else 'REJEITA'}")
            return accepts_empty

        n = len(string)

        table = [[set() for _ in range(n)] for _ in range(n)]

        print("Preenchendo diagonal (subcadeias de tamanho 1):")
        for i in range(n):
            char = string[i]
            for left, rights in self.grammar.productions.items():
                for right in rights:
                    if len(right) == 1 and right[0] == char:
                        table[i][i].add(left)
            print(f"  Posição [{i},{i}] ('{char}'): {table[i][i]}")

        print("\nPreenchendo tabela CYK:")
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                substring = string[i:j+1]

                for k in range(i, j):
                    for left, rights in self.grammar.productions.items():
                        for right in rights:
                            if len(right) == 2:
                                B, C = right
                                if B in table[i][k] and C in table[k+1][j]:
                                    table[i][j].add(left)

                print(f"  Posição [{i},{j}] ('{substring}'): {table[i][j]}")

        self._print_table(table, string)

        result = self.grammar.start_symbol in table[0][n-1]
        print(f"\nSímbolo inicial '{self.grammar.start_symbol}' está em [{0},{n-1}]? {result}")
        print(f"\nResultado: {'ACEITA' if result else 'REJEITA'}")
        print(f"{'='*60}\n")

        return result

    def _print_table(self, table, string):
        n = len(string)
        print("\nTabela CYK completa:")
        print("-" * 60)

        for i in range(n-1, -1, -1):
            row_str = f"Linha {i}: "
            for j in range(n):
                if j >= i:
                    cell = table[i][j]
                    cell_str = '{' + ','.join(sorted(cell)) + '}' if cell else '∅'
                    row_str += f"{cell_str:15}"
                else:
                    row_str += f"{'':15}"
            print(row_str)

        col_str = "        "
        for j in range(n):
            col_str += f"{j:15}"
        print(col_str)

        char_str = "        "
        for char in string:
            char_str += f"'{char}'{' '*12}"
        print(char_str)
        print("-" * 60)


def load_grammar_from_input():
    print("\n" + "="*60)
    print("ENTRADA DA GRAMÁTICA")
    print("="*60)
    print("Formato: A -> BC | a | ε")
    print("Digite 'FIM' para terminar a entrada de produções\n")

    grammar = GrammarCNF()

    start = input("Símbolo inicial: ").strip()
    grammar.set_start_symbol(start)

    print("\nDigite as produções (uma por linha):")
    print("Exemplo: S -> AB | a")
    print("         A -> a")

    while True:
        line = input("Produção: ").strip()
        if line.upper() == 'FIM':
            break

        if '->' not in line:
            print("Formato inválido! Use: A -> BC | a")
            continue

        left, right_side = line.split('->')
        left = left.strip()

        alternatives = right_side.split('|')
        for alt in alternatives:
            alt = alt.strip()
            if alt == 'ε' or alt == 'epsilon':
                grammar.add_production(left, ['ε'])
            else:
                symbols = list(alt.replace(' ', ''))
                grammar.add_production(left, symbols)

    return grammar


def load_grammar_example():
    grammar = GrammarCNF()
    grammar.set_start_symbol('S')

    grammar.add_production('S', ['a', 'S', 'b'])
    grammar.add_production('S', ['a', 'b'])

    return grammar


def main():
    print("="*60)
    print("TRABALHO FINAL - TEORIA DA COMPUTAÇÃO")
    print("Conversão para FNC e Algoritmo CYK")
    print("="*60)

    print("\nEscolha o modo de entrada:")
    print("1 - Digitar gramática manualmente")
    print("2 - Usar gramática de exemplo (a^n b^n)")

    choice = input("\nOpção: ").strip()

    if choice == '1':
        grammar = load_grammar_from_input()
    else:
        grammar = load_grammar_example()
        grammar.print_grammar("Gramática de Exemplo")

    grammar.to_cnf()

    parser = CYKParser(grammar)

    print("\n" + "="*60)
    print("TESTE DE CADEIAS")
    print("="*60)
    print("Digite as cadeias para testar (uma por linha)")
    print("Digite 'FIM' para encerrar\n")

    while True:
        string = input("Cadeia: ").strip()
        if string.upper() == 'FIM':
            break

        parser.parse(string)

    print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()