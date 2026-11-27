import pytest
from src.checkout import calcular_valor_final


def test_compra_simples_sem_desconto_com_frete():
    # R$ 100.00 + R$ 20.00 de frete = R$ 120.00
    assert calcular_valor_final(100.0) == 120.00


def test_compra_com_cupom_valido_e_frete():
    # R$ 100.00 com 10% de desconto = R$ 90.00 + R$ 20.00 frete = R$ 110.00
    assert calcular_valor_final(100.0, cupom="VERAO10") == 110.00


def test_compra_com_cupom_festa20():
    # R$ 100.00 com 20% de desconto = R$ 80.00 + R$ 20.00 frete = R$ 100.00
    assert calcular_valor_final(100.0, cupom="FESTA20") == 100.00


def test_frete_gratis_por_valor_compra():
    # R$ 250.00 sem cupom -> >= R$ 200.00 -> Frete Grátis = R$ 250.00
    assert calcular_valor_final(250.0) == 250.00


def test_cliente_vip_com_frete_gratis():
    # R$ 50.00 para VIP -> Frete Grátis = R$ 50.00
    assert calcular_valor_final(50.0, e_vip=True) == 50.00


def test_erro_cupom_expirado():
    with pytest.raises(ValueError, match="O cupom informado esta expirado."):
        calcular_valor_final(100.0, cupom="INVERNO20")


def test_erro_valor_compra_invalido():
    with pytest.raises(ValueError, match="O valor da compra deve ser maior que zero."):
        calcular_valor_final(0.0)


def test_cupom_invalido_levanta_value_error():
    with pytest.raises(ValueError, match="Cupom invalido."):
        calcular_valor_final(100.0, "CUPOM_QUE_NAO_EXISTE", False)



# Teste Parametrizado (Análise de Valor Limite e Combinações)
@pytest.mark.parametrize("valor, cupom, vip, esperado", [
    (199.99, None, False, 219.99),      # Logo abaixo do limite -> cobra R$ 20
    (200.0, None, False, 200.00),       # Exatamente no limite (>= 200) -> frete grátis
    (200.01, None, False, 200.01),      # Acima do limite -> frete grátis
    (222.23, "VERAO10", False, 200.01), # R$ 200.007 com desconto -> R$ 200.01 final (>= 200 -> frete grátis)
    (250.0, "FESTA20", False, 200.00),  # 20% de desconto -> exatamente R$ 200 -> frete grátis
    (100.0, "verao10", True, 90.00),    # Cupom minúsculo para cliente VIP -> R$ 90 + frete grátis
])
def test_cenarios_limite_e_combinados(valor, cupom, vip, esperado):
    assert calcular_valor_final(valor, cupom, vip) == esperado
