import pytest

import template_guard as tg


def test_1_attribute_access_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{user.__class__}", {"user": "alice"})


def test_2_mro_access_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{user.__class__.__mro__}", {"user": "alice"})


def test_3_base_class_access_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{().__class__.__bases__}", {})


def test_4_subclasses_access_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{''.__class__.__mro__[1].__subclasses__()}", {})


def test_5_import_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{__import__('os').getcwd()}", {})


def test_6_file_read_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{open('README.md').read()}", {})


def test_7_eval_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{eval('1+1')}", {})


def test_8_exec_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{exec('x=1')}", {})


def test_9_lambda_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{(lambda: 1)()}", {})


def test_10_comprehension_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{[x for x in range(3)]}", {})


def test_11_nested_expression_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{user:{width}}", {"user": "alice"})


def test_12_invalid_syntax_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{user", {"user": "alice"})


def test_13_non_string_template_is_rejected():
    with pytest.raises(TypeError):
        tg.render(123, {})


def test_14_dunder_dict_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{user.__dict__}", {"user": "alice"})


def test_15_function_globals_is_rejected():
    with pytest.raises(ValueError):
        tg.render("{render.__globals__}", {"user": "alice"})
