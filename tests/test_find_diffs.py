# import pytest
from gendiff import gen_dicts_diffs, stylish
from os import getcwd, path


def get_file_path(file_name: str) -> str:
    return path.join(getcwd(), "tests/fixtures", file_name)


def test_plain_json_diff():
    file1_path = get_file_path("file1.json")
    file2_path = get_file_path("file2.json")
    result = stylish(gen_dicts_diffs(file1_path, file2_path))
    result_path = get_file_path("plain_diffs.txt")
    with open(result_path, "rt") as file:
        text = file.read()
    assert text == result


def test_plain_yaml_diff():
    file1_path = get_file_path("file1.yaml")
    file2_path = get_file_path("file2.yaml")
    result = stylish(gen_dicts_diffs(file1_path, file2_path))
    result_path = get_file_path("plain_diffs.txt")
    with open(result_path, "rt") as file:
        text = file.read()
    assert text == result


def test_struct_json_diff():
    file1_path = get_file_path("struct_file1.json")
    file2_path = get_file_path("struct_file2.json")
    result = stylish(gen_dicts_diffs(file1_path, file2_path))
    result_path = get_file_path("struct_diffs.txt")
    with open(result_path, "rt") as file:
        text = file.read()
    assert text == result


def test_struct_yaml_diff():
    file1_path = get_file_path("struct_file1.yaml")
    file2_path = get_file_path("struct_file2.yaml")
    result = stylish(gen_dicts_diffs(file1_path, file2_path))
    result_path = get_file_path("struct_diffs.txt")
    with open(result_path, "rt") as file:
        text = file.read()
    assert text == result
