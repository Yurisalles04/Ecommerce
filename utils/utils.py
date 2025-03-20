def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    if isinstance(carrinho, dict):
        return sum([item['quantidade'] for item in carrinho.values() if isinstance(item, dict) and 'quantidade' in item])
    return 0

def cart_totals(carrinho):
    return sum(
        [item.get('preco_quantitativo_promocional') 
         if item.get('preco_quantitativo_promocional') 
         else item.get('preco_quantitativo')
         
         for item in carrinho.values()
         ])