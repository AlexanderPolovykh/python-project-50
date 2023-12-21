import argparse
from gendiff import generate_diff


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
    diff_str = generate_diff(arg_first_file, arg_second_file, arg_format)
    print(diff_str)
