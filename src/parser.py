from lark import Lark

def load_parser():
    with open("grammar/milcode.lark", "r", encoding="utf-8") as f:
        grammar = f.read()
    parser = Lark(grammar, start="start", parser="lalr")
    return parser

if __name__ == "__main__":
    parser = load_parser()
    codigo = """
    sgt_soldado: inf;
    sgt_soldado >> 10;
    relate "Quantidade de soldados:";
    ordem_se (sgt_soldado !! 50) {
        relate "Tropa Reforçada";
    } contramarcha {
        relate "Precisa de reforços";
    };
    """
    arvore = parser.parse(codigo)
    print(arvore.pretty())
