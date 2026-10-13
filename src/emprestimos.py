def resumo_emprestimo(nome, dias, estado):
    nome = nome.strip()
 
    if not nome:
        nome = "Sem identificação"
 
    valor_valido = type(dias) == int and 1 <= dias <= 30
 
    estado_aceite = estado in {"confirmado", "pendente"}
 
    return nome, valor_valido, estado_aceite
 
 
if __name__ == "__main__":
    nome, valor_valido, estado_aceite = resumo_emprestimo(
        "João", 10, "confirmado"
    )
    
    # Apresentação do resultado com f-string (Ponto 4)
    print(f"Identificação: {nome} | Valor válido: {valor_valido} | Estado aceite: {estado_aceite}")

