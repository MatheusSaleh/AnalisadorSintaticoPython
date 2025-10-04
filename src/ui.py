import tkinter as tk
from tkinter import scrolledtext
from parser import load_parser
from semantic import SemanticAnalyzer
from lark.exceptions import UnexpectedToken, UnexpectedCharacters


TOKEN_DESCRICOES = {
    "IDENT": "um identificador (ex: sgt_soldado)",
    "NUMBER": "um número (ex: 10, 25, 3.14)",
    "STRING": "uma string entre aspas (ex: \"texto\")",
    "TIPO": "um tipo de dado (inf, art, comandante, ordem)",
    "OPERADOR_LOGICO": "um operador lógico (!!, ??, #=, ##)",
    "LPAR": "um parêntese de abertura '('",
    "RPAR": "um parêntese de fechamento ')'",
    "LBRACE": "uma chave de abertura '{'",
    "RBRACE": "uma chave de fechamento '}'",
    "SEMICOLON": "um ponto e vírgula ';'",
    "RELATE": "a palavra reservada 'relate'",
    "RECEBA": "a palavra reservada 'receba'",
    "ORDEM_SE": "a palavra reservada 'ordem_se'",
    "CONTRAMARCHA": "a palavra reservada 'contramarcha'",
    "PATRULHA": "a palavra reservada 'patrulha'",
    "MISSAO": "a palavra reservada 'missao'",
}


def traduzir_tokens(tokens):
    descricoes = []
    for t in tokens:
        if t in TOKEN_DESCRICOES:
            descricoes.append(TOKEN_DESCRICOES[t])
        else:
            descricoes.append(t)  # se não tiver tradução, mostra o nome cru
    return ", ".join(descricoes)




def formatar_lista(tokens):
    """Formata tokens esperados para exibição mais clara."""
    return ", ".join(sorted(tokens))


def analisar():
    codigo = entrada.get("1.0", tk.END).strip()
    parser = load_parser()
    saida.config(state="normal")
    saida.delete("1.0", tk.END)

    try:
        arvore = parser.parse(codigo)
        semantica = SemanticAnalyzer()
        semantica.transform(arvore)

        saida.insert(tk.END, "✅ Código válido!\n\n", "success")
        saida.insert(tk.END, arvore.pretty(), "tree")

    except UnexpectedToken as e:
        saida.insert(tk.END, "❌ ERRO DE SINTAXE DETECTADO\n", "error")
        saida.insert(tk.END, f"   ➤ Linha {e.line}, Coluna {e.column}\n", "error")
        saida.insert(tk.END, f"   ➤ Símbolo inesperado encontrado: «{e.token}»\n", "error")
        if e.expected:
            saida.insert(tk.END, "   ➤ Possíveis símbolos esperados:\n", "warning")
            saida.insert(tk.END, f"      {traduzir_tokens(e.expected)}\n", "warning")
        contexto = e.get_context(codigo)
        saida.insert(tk.END, "   ➤ Contexto do erro:\n", "error")
        saida.insert(tk.END, contexto + "\n", "warning")

    except UnexpectedCharacters as e:
        saida.insert(tk.END, "❌ ERRO DE CARACTERE INVÁLIDO\n", "error")
        saida.insert(tk.END, f"   ➤ Linha {e.line}, Coluna {e.column}\n", "error")
        saida.insert(tk.END, f"   ➤ Caractere inválido encontrado: «{e.char}»\n", "error")
        saida.insert(tk.END, "   ➤ Talvez você tenha digitado um símbolo errado ou fora do lugar.\n", "warning")
        contexto = e.get_context(codigo)
        saida.insert(tk.END, "   ➤ Contexto do erro:\n", "error")
        saida.insert(tk.END, contexto + "\n", "warning")

    saida.config(state="disabled")  # bloqueia edição da saída


# Criar janela
root = tk.Tk()
root.title("Analisador Sintático MILCODE")
root.geometry("900x700")

# Caixa de entrada
entrada_label = tk.Label(root, text="Digite seu código MILCODE:", font=("Arial", 12, "bold"))
entrada_label.pack(anchor="w", padx=10, pady=(10, 0))

entrada = scrolledtext.ScrolledText(root, height=15, width=100, font=("Courier", 11))
entrada.pack(padx=10, pady=10)

# Botão
botao = tk.Button(root, text="Analisar Código", font=("Arial", 12, "bold"), command=analisar)
botao.pack(pady=5)

# Caixa de saída
saida_label = tk.Label(root, text="Resultado da análise:", font=("Arial", 12, "bold"))
saida_label.pack(anchor="w", padx=10, pady=(10, 0))

saida = scrolledtext.ScrolledText(root, height=15, width=100, font=("Courier", 11))
saida.pack(padx=10, pady=10)

# Estilos de cores
saida.tag_config("success", foreground="green", font=("Courier", 11, "bold"))
saida.tag_config("error", foreground="red", font=("Courier", 11, "bold"))
saida.tag_config("warning", foreground="orange", font=("Courier", 11, "italic"))
saida.tag_config("tree", foreground="blue")

saida.config(state="disabled")  # bloqueia edição inicial

root.mainloop()
