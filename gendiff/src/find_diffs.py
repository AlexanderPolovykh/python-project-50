import json
import yaml
import os
import re

INDENT = " " * 2


def get_dict(file_path: str) -> dict:
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


def make_diffs(dict1: dict, dict2: dict) -> dict:  # noqa C901
    # dict1 = dict1[0] if isinstance(dict1, list) else dict1
    # dict2 = dict2[0] if isinstance(dict2, list) else dict2
    keys1 = sorted(dict1.keys())
    keys2 = sorted(dict2.keys())
    dict_diffs = {}
    for key in keys1:
        # dict1[key] = dict1[key][0] if isinstance(dict1[key], list) else dict1[key]
        if key in keys2:
            # dict2[key] = dict2[key][0] if isinstance(dict2[key], list) else dict2[key]
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
                        dict_diffs[f"{key}="] = make_diffs(dict1[key], dict2[key])
                    else:
                        dict_diffs[f"{key}+"] = dict1[key]
                        dict_diffs[f"{key}-"] = dict2[key]
        else:
            dict_diffs[f"{key}+"] = dict1[key]
    for key in keys2:
        if key not in keys1:
            # dict2[key] = dict2[key][0] if isinstance(dict2[key], list) else dict2[key]
            dict_diffs[f"{key}-"] = dict2[key]
    return dict_diffs


def sub_key(string: str) -> str:
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


def gen_dicts_diffs(file_path1: str, file_path2: str) -> str:
    dict1 = _flat_vals(get_dict(file_path1))
    dict2 = _flat_vals(get_dict(file_path2))
    diffs = make_diffs(dict1, dict2)
    diff_prev = json.dumps(diffs, indent=4, separators=["", ": "], sort_keys=True)
    diff = diff_prev.replace('"', "")
    list_diff = diff.split("\n")
    new_list = []
    for sd in list_diff:
        new_list.append(sub_key(sd)[2:])
    return "\n".join(new_list)

    # output = ["{"]
    # for key, val in dict1.items():
    #     if key in dict2.keys():
    #         val2 = dict2.get(key)
    #         if val == val2:
    #             output.append(f"{INDENT}  {key}: {val}")
    #         else:
    #             output.append(f"{INDENT}- {key}: {val}")
    #             output.append(f"{INDENT}+ {key}: {val2}")
    #     else:
    #         output.append(f"{INDENT}- {key}: {val}")
    # for key, val in dict2.items():
    #     if key not in dict1.keys():
    #         output.append(f"{INDENT}+ {key}: {val}")
    # output.append("}")

    # return "\n".join(output)


# gen_dicts_diffs('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml')
# gen_dicts_diffs("tests/fixtures/struct_file1.yaml","tests/fixtures/struct_file2.yaml")
