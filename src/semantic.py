from lark import Transformer, v_args

class SemanticAnalyzer(Transformer):
    def __init__(self):
        self.symbols = {}  # tabela de símbolos: {nome: tipo}

    def declaracao(self, items):
        ident, tipo = items
        self.symbols[str(ident)] = str(tipo)
        return f"Declarado {ident} como {tipo}"

    def atribuicao(self, items):
        ident, valor = items[0], items[1]
        nome = str(ident)
        if nome not in self.symbols:
            raise Exception(f"Erro: variável {nome} não declarada.")
        return f"Atribuição em {nome}"

    def condicional(self, items):
        return "Verificação de condicional"

    def saida(self, items):
        return f"Saída: {items[0]}"
