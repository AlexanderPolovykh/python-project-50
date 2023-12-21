import argparse
from gendiff import gen_dicts_diffs, stylish


def cli_gendiff():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file", type=str, help="first file to compare")
    parser.add_argument("second_file", type=str, help="second file to compare")
    parser.add_argument(
        "-f",
        "--format",
        dest="FORMAT",
        default="stylish",
        help="set format of output (default: stylish)",
    )
    args = parser.parse_args()
    args_dict = vars(args)
    arg_first_file = args_dict.get("first_file")
    arg_second_file = args_dict.get("second_file")
    arg_format = args_dict.get("FORMAT")
    diff = gen_dicts_diffs(arg_first_file, arg_second_file)
    match arg_format:
        case "stylish":
            diff_str = stylish(diff)
        case _:
            diff_str = ""
    print(arg_format)
    print(diff_str)
