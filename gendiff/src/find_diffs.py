import json
import yaml
import os
import re


def _get_dict(file_path: str) -> dict:
    _, ext = os.path.splitext(os.path.basename(file_path))
    fp = os.path.join(os.getcwd(), file_path)
    ret = {}
    try:
        with open(fp, "rb") as f:
            if ext.lower() in [".yaml", ".yml"]:
                ret = yaml.load(f, Loader=yaml.Loader)[0]
            if ext.lower() == ".json":
                ret = json.load(f)
    except Exception as e:
        raise e
    return ret


def _flat_vals(_dict: dict) -> dict:
    ret = {}
    keys = _dict.keys()
    for key in keys:
        _dict[key] = _dict[key][0] if isinstance(_dict[key], list) else _dict[key]
        if isinstance(_dict[key], dict):
            ret[key] = _flat_vals(_dict[key])
        else:
            ret[key] = _dict[key]
    return ret


def _make_diffs(dict1: dict, dict2: dict) -> dict:  # noqa C901
    keys1 = sorted(dict1.keys())
    keys2 = sorted(dict2.keys())
    dict_diffs = {}
    for key in keys1:
        if key in keys2:
            if not (isinstance(dict1[key], dict) or isinstance(dict2[key], dict)):
                if dict1[key] == dict2[key]:
                    dict_diffs[f"{key}="] = dict1[key]
                else:
                    dict_diffs[f"{key}+"] = dict1[key]
                    dict_diffs[f"{key}-"] = dict2[key]
            else:
                if dict1[key] == dict2[key]:
                    dict_diffs[f"{key}="] = dict1[key]
                else:
                    if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        dict_diffs[f"{key}="] = _make_diffs(dict1[key], dict2[key])
                    else:
                        dict_diffs[f"{key}+"] = dict1[key]
                        dict_diffs[f"{key}-"] = dict2[key]
        else:
            dict_diffs[f"{key}+"] = dict1[key]
    for key in keys2:
        if key not in keys1:
            dict_diffs[f"{key}-"] = dict2[key]
    return dict_diffs


def _sub_key(string: str) -> str:
    match = re.search(r"\w+[+-=]:", string)
    if match:
        match match.group()[-2]:
            case "+":
                return re.sub(r"\w+\+:", f"- {match.group()[:-2]}:", string)
            case "-":
                return re.sub(r"\w+-:", f"+ {match.group()[:-2]}:", string)
            case "=":
                return re.sub(r"\w+=:", f"  {match.group()[:-2]}:", string)
    return f"  {string}"


def generate_diff(file_path1: str, file_path2: str, format_name: str) -> str:
    ret = ""
    dict1 = _flat_vals(_get_dict(file_path1))
    dict2 = _flat_vals(_get_dict(file_path2))
    diff_dict = _make_diffs(dict1, dict2)
    match format_name:
        case "stylish":
            diff_prev = json.dumps(diff_dict, indent=4, separators=["", ": "], sort_keys=True)
            diff = diff_prev.replace('"', "")
            new_list = []
            list_diff = diff.split("\n")
            for sd in list_diff:
                new_list.append(_sub_key(sd)[2:])
            ret = "\n".join(new_list)
        case "plain":
            ret = "\n".join(_plain(diff_dict, ""))
        case _:
            pass
    return ret


def _plain(_dict: dict, key_name: str) -> str:  # noqa C901
    _list = []
    keys = sorted(_dict.keys())
    for key in keys:
        skey = f"{key_name}.{key[:-1]}" if key_name else key[:-1]
        if key.endswith("+"):
            _list.append(f"Property '{skey}' was removed")
        elif key.endswith("-"):
            key_plus = f"{key[:-1]}+"
            if key_plus in keys:
                _list.pop()
                if isinstance(_dict[key_plus], dict):
                    prev = "[complex value]"
                else:
                    prev = json.dumps(_dict[key_plus])
                if isinstance(_dict[key], dict):
                    _list.append(f"Property '{skey}' was updated. From {prev} to [complex value]")
                else:
                    _list.append(
                        f"Property '{skey}' was updated. From {prev} to {json.dumps(_dict[key])}"
                    )
            else:
                if isinstance(_dict[key], dict):
                    _list.append(f"Property '{skey}' was added with value: [complex value]")
                else:
                    _list.append(
                        f"Property '{skey}' was added with value: {json.dumps(_dict[key])}"
                    )
        else:
            if isinstance(_dict[key], dict):
                _list.extend(_plain(_dict[key], skey))
    return list(map(lambda row: row.replace('"', "'"), _list))
    # return _list


# gen_dicts_diffs('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml')
# generate_diff("tests/fixtures/struct_file1.yaml", "tests/fixtures/struct_file2.yaml", "plain")
