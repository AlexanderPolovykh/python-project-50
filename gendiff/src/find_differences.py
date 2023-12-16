import argparse
import json

INDENT = " " * 2


def cli_gendiff():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", metavar="FORMAT", help="set format of output")
    args = parser.parse_args()
    args_dict = vars(args)
    arg_first_file = args_dict.get("first_file")
    arg_second_file = args_dict.get("second_file")
    diff = generate_diff(arg_first_file, arg_second_file)
    print(diff)


def generate_diff(file_path1: str, file_path2: str) -> str:
    json1 = json.load(open(file_path1))
    json2 = json.load(open(file_path2))
    output = ["{"]
    for key, val in json1.items():
        if key in json2.keys():
            val2 = json2.get(key)
            if val == val2:
                output.append(f"{INDENT}  {key}: {val}")
            else:
                output.append(f"{INDENT}- {key}: {val}")
                output.append(f"{INDENT}+ {key}: {val2}")
        else:
            output.append(f"{INDENT}- {key}: {val}")
    for key, val in json2.items():
        if key not in json1.keys():
            output.append(f"{INDENT}+ {key}: {val}")
    output.append("}")
    return "\n".join(output)
