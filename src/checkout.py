"""
Módulo de Checkout do E-Commerce
Responsável pelo cálculo de valores finais, cupons e taxas de frete.
"""
from typing import Optional


def calcular_valor_final(valor_compra: float, cupom: Optional[str] = None, e_vip: bool = False) -> float:
    """
    Calcula o valor final da compra considerando regras de desconto e frete:
    - Cupom 'VERAO10': concede 10% de desconto no valor das mercadorias.
    - Cupom 'FESTA20': concede 20% de desconto no valor das mercadorias.
    - Cupom 'INVERNO20': cupom expirado que deve lançar ValueError.
    - Frete Grátis: para subtotal (após desconto) >= R$ 200.00 ou para clientes VIP.
    - Frete Padrão: R$ 20.00 para os demais casos.
    """
    if valor_compra <= 0:
        raise ValueError("O valor da compra deve ser maior que zero.")

    desconto = 0.0

    if cupom:
        cupom_limpo = cupom.strip().upper()
        if cupom_limpo == "VERAO10":
            desconto = 0.10
        elif cupom_limpo == "FESTA20":
            desconto = 0.20
        elif cupom_limpo == "INVERNO20":
            raise ValueError("O cupom informado esta expirado.")
        else:
            raise ValueError("Cupom invalido.")

    valor_com_desconto = valor_compra * (1 - desconto)

    # Regra de Frete
    if e_vip or valor_com_desconto >= 200.0:
        frete = 0.0
    else:
        frete = 20.0

    return round(valor_com_desconto + frete, 2)
