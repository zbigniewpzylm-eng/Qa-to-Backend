import pytest
from scripts.sandbox import parse_data, InvalidApiResponseError  

def test_case_1_correct():
    test_case = {"first": 1, "second": 2}
    res = parse_data(test_case)
    assert isinstance(res, list)
    assert all(k in res[0] for k in ["first", "second"])
    assert res[0]["first"] == 1
    assert res[0]["second"] == 2

def test_case_2_list_of_dicts_correct():
    test_case = [
        {"first": 1, "second": 2},
        {"first": 10, "second": 20}
    ]
    res = parse_data(test_case)
    assert isinstance(res, list)
    assert all("first" in d and "second" in d for d in res)
    assert res[1]["first"] == 10
    assert res[1]["second"] == 20

def test_case_3_missing_second_key():
    test_case = {"first": 1}  # brak 'second'
    with pytest.raises(KeyError) as exc_info:
        parse_data(test_case)
    assert "Missing required key" in str(exc_info.value)

def test_case_4_list_with_missing_key():
    test_case = [
        {"first": 1, "second": 2},
        {"first": 10}  # brak 'second'
    ]
    with pytest.raises(KeyError) as exc_info:
        parse_data(test_case)
    assert "Missing required key" in str(exc_info.value)

def test_case_5_wrong_type():
    test_case = "nie dict ani lista"
    with pytest.raises(TypeError) as exc_info:
        parse_data(test_case)
    assert "Input data must be a dictionary or a list" in str(exc_info.value)

def test_case_6_empty_list():
    test_case = []
    res = parse_data(test_case)
    assert isinstance(res, list)
    assert res == []

def test_case_7_extra_keys_in_dict():
    test_case = {"first": 100, "second": 200, "extra": 999}
    res = parse_data(test_case)
    assert isinstance(res, list)
    assert all(k in res[0] for k in ["first", "second"])
    assert "extra" not in res[0]  # parse_data powinno ignorować 'extra'

def test_case_8_list_of_dicts_with_extra_keys():
    test_case = [
        {"first": 1, "second": 2, "extra": 99},
        {"first": 10, "second": 20, "another": 123}
    ]
    res = parse_data(test_case)
    assert isinstance(res, list)
    for d in res:
        assert all(k in d for k in ["first", "second"])
        assert "extra" not in d
        assert "another" not in d
