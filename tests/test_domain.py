from decimal import Decimal
import pytest
from app.errors import DataError
from app.modules.domain.rule import evaluate


def test_twoway(cases):
    actual, evidence = evaluate(cases['twoway'])
    assert actual == Decimal('0.37')
    assert evidence and all(len(row)==3 for row in evidence)


def test_exact(cases):
    actual, evidence = evaluate(cases['exact'])
    assert actual == Decimal('0.30')


def test_branch(cases):
    actual, evidence = evaluate(cases['branch'])
    assert actual == Decimal('3')


def test_one_sided(cases):
    # TRAP-21
    with pytest.raises(DataError) as error:
        evaluate(cases['one_sided'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}


def test_loop(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['loop'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}


def test_break(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['break'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}


def test_over(cases):
    with pytest.raises(DataError) as error:
        evaluate(cases['over'])
    assert error.value.code in {'BUSINESS','NUMBER','RANGE','TIMESTAMP'}

