from parser import load_parser
from semantic import SemanticAnalyzer

def executar(codigo: str):
    parser = load_parser()
    arvore = parser.parse(codigo)
    print("=== Árvore Sintática ===")
    print(arvore.pretty())

    print("=== Análise Semântica ===")
    semantica = SemanticAnalyzer()
    resultado = semantica.transform(arvore)
    print(resultado)

if __name__ == "__main__":
    with open("examples/exemplo2.mil", "r", encoding="utf-8") as f:
        codigo = f.read()
    executar(codigo)
