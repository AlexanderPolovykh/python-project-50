import argparse
from gendiff import gen_dicts_diffs


def cli_gendiff():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f",
        "--format",
        metavar="FORMAT",
        help="set format of output",
    )
    args = parser.parse_args()
    args_dict = vars(args)
    arg_first_file = args_dict.get("first_file")
    arg_second_file = args_dict.get("second_file")
    diff = gen_dicts_diffs(arg_first_file, arg_second_file)
    print(diff)
