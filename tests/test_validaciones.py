import pytest

from despachos.validaciones import (
    ErrorValidacion,
    normalizar_cliente,
    validar_cantidad,
    validar_codigo,
    validar_peso,
    validar_sku,
)


def test_codigo_valido():
    assert validar_codigo("PED-000101") == "PED-000101"


def test_codigo_vacio():
    with pytest.raises(ErrorValidacion):
        validar_codigo("")


def test_codigo_con_formato_invalido():
    with pytest.raises(ErrorValidacion):
        validar_codigo("PEDIDO-1")


def test_sku_valido():
    assert validar_sku("ABC-1001") == "ABC-1001"


def test_sku_invalido():
    with pytest.raises(ErrorValidacion):
        validar_sku("abc-1")


def test_cantidad_valida():
    assert validar_cantidad(3) == 3


def test_cantidad_cero():
    with pytest.raises(ErrorValidacion):
        validar_cantidad(0)


def test_normalizar_cliente():
    assert normalizar_cliente("  comercial   andina  ") == "Comercial Andina"


def test_normalizar_cliente_corto():
    with pytest.raises(ErrorValidacion):
        normalizar_cliente("ab")

def test_peso_valido():
    assert validar_peso(10.0) == 10.0


def test_peso_excede_maximo():
    with pytest.raises(ErrorValidacion):
        validar_peso(80.0)


def test_peso_cero():
    with pytest.raises(ErrorValidacion):
        validar_peso(0)